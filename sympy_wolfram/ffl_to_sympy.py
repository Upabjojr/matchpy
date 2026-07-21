# -*- coding: utf-8 -*-
"""Convert Wolfram Mathematica Full-Form List (FFL) AST to SymPy code strings.

This module provides a generic, self-contained converter from Mathematica FFL
(JSON-serialized nested lists) into Python/SymPy expression code strings.

No dependency on rubi_rules or any other domain-specific package.

Wildcard naming convention:
    - Pattern[name, Blank[]]        -> ``name_``   (non-optional wildcard)
    - Optional[Pattern[name, ...]]  -> ``_name_``  (optional wildcard, identity element)

The generated code strings can be ``eval``'d in a namespace containing SymPy
objects and the appropriate wildcard symbols.
"""
from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional, Set, Tuple

import sympy
from sympy import Integer, Rational, Symbol
from sympy.printing.str import StrPrinter

from sympy_matching.wild import (IDENTITY_ELEMENT, WildHeadApp, WildHeadDeriv,
                                 WildSymbol)


# =============================================================================
# Wild printer (stateless module-level instance)
# =============================================================================

class _WildStrPrinter(StrPrinter):
    """Custom StrPrinter that prints WildSymbol using variable-name convention.

    Non-optional WildSymbol('m') -> ``m_``
    Optional WildSymbol('m', optional_value=IDENTITY_ELEMENT) -> ``_m_``
    """

    def _print_WildSymbol(self, expr):
        name = expr.wildcard_name
        if expr.optional_value is not None:
            return f'_{name}_'
        return f'{name}_'

    def _print_Half(self, expr):
        return "sympy.S.Half"

    def _print_Rational(self, expr: Rational):
        num = self._print(expr.numerator)
        denom = self._print(expr.denominator)
        return f"sympy.S({num})/{denom}"


# Module-level printer instance (stateless)
_wild_printer = _WildStrPrinter()


# =============================================================================
# FFLConverter
# =============================================================================

class FFLConverter:
    """Convert Mathematica FFL AST nodes to SymPy code strings.

    Parameters
    ----------
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    custom_functions : dict, optional
        Mapping from Wolfram/Mathematica head names to custom callables.
        Each value is a 2-tuple ``(qualified_code_str, obj)`` where:

        * *qualified_code_str* -- the Python code string to emit
          (e.g. ``"my_module.MyFunc"``).
        * *obj* -- the actual Python object for the eval namespace.  If the
          code string contains a dot (e.g. ``"mod.Func"``), *obj* should be
          the module (added as ``mod``).  If there is no dot, *obj* should be
          the callable itself.
    extra_sympy_funcs : dict, optional
        Additional ``{MathematicaHead: 'python.callable'}`` mappings.
    extra_constants : dict, optional
        Additional ``{MathematicaAtom: 'sympy.constant_code'}`` mappings.
    """

    # Type alias for custom_functions dict value
    CustomFuncEntry = Tuple[str, Any]

    # Mathematica head -> SymPy callable code
    SYMPY_FUNC_MAP: Dict[str, str] = {
        # Wildcard function head applied to args (F_[v_]) -- see WildHeadApp
        'WildHeadApp': 'WildHeadApp',
        'WildHeadDeriv': 'WildHeadDeriv',
        # Trigonometric
        'Sin': 'sympy.sin', 'Cos': 'sympy.cos', 'Tan': 'sympy.tan',
        'Sec': 'sympy.sec', 'Csc': 'sympy.csc', 'Cot': 'sympy.cot',
        'ArcSin': 'sympy.asin', 'ArcCos': 'sympy.acos',
        'ArcSec': 'sympy.asec', 'ArcCsc': 'sympy.acsc', 'ArcCot': 'sympy.acot',
        # Lowercase trig (some FFL use them)
        'sin': 'sympy.sin', 'cos': 'sympy.cos', 'tan': 'sympy.tan',
        'sec': 'sympy.sec', 'csc': 'sympy.csc', 'cot': 'sympy.cot',
        'sinh': 'sympy.sinh', 'cosh': 'sympy.cosh', 'tanh': 'sympy.tanh',
        'sech': 'sympy.sech', 'csch': 'sympy.csch', 'coth': 'sympy.coth',
        # Hyperbolic
        'Sinh': 'sympy.sinh', 'Cosh': 'sympy.cosh', 'Tanh': 'sympy.tanh',
        'Sech': 'sympy.sech', 'Csch': 'sympy.csch', 'Coth': 'sympy.coth',
        'ArcSinh': 'sympy.asinh', 'ArcCosh': 'sympy.acosh', 'ArcTanh': 'sympy.atanh',
        'ArcSech': 'sympy.asech', 'ArcCsch': 'sympy.acsch', 'ArcCoth': 'sympy.acoth',
        # Elementary
        'Exp': 'sympy.exp', 'Log': 'sympy.log', 'Sqrt': 'sympy.sqrt',
        'Abs': 'sympy.Abs',
        # Special functions
        'EllipticE': 'sympy.elliptic_e', 'EllipticF': 'sympy.elliptic_f',
        'AppellF1': 'sympy.appellf1',
        'Gamma': 'Gamma', 'LogGamma': 'sympy.loggamma',
        'Erf': 'sympy.erf',
        'Erfi': 'sympy.erfi', 'Erfc': 'sympy.erfc',
        'PolyLog': 'sympy.polylog',
        # Calculus / algebra
        'D': 'D', 'Denominator': 'sympy.denom',
        'Rt': 'sympy.root', 'Simplify': 'Simplify',
        'FractionalPart': 'sympy.frac', 'IntegerPart': 'sympy.floor',
        # List functions:
        'Min': 'sympy.Min', 'Max': 'sympy.Max',
    }

    # Mathematica predicates that map to native SymPy relational/logic objects
    SYMPY_LOGIC_MAP: Dict[str, str] = {
        'Equal': 'sympy.Eq',
        'Unequal': 'sympy.Ne',
        'Less': 'sympy.Lt',
        'Greater': 'sympy.Gt',
        'LessEqual': 'sympy.Le',
        'GreaterEqual': 'sympy.Ge',
    }

    CONSTANT_MAP: Dict[str, str] = {
        'Pi': 'sympy.pi', 'E': 'sympy.E',
        'I': 'sympy.I', 'Infinity': 'sympy.oo',
        'True': 'sympy.true', 'False': 'sympy.false',
        'EulerGamma': 'sympy.EulerGamma',
    }

    def __init__(
        self,
        fixed_var: str = 'x',
        custom_functions: Optional[Dict[str, "FFLConverter.CustomFuncEntry"]] = None,
        extra_sympy_funcs: Optional[Dict[str, str]] = None,
        extra_constants: Optional[Dict[str, str]] = None,
    ) -> None:
        self._fixed_var = fixed_var
        # Per-rule wildcard tracking (reset per rule via reset())
        self._wildcards_non_optional: Set[str] = set()
        self._wildcards_optional: Set[str] = set()
        self._symbols: Set[str] = set()
        self._wild_defs: List[str] = []
        # Slot mapping for Function/Lambda conversion (slot_number -> var_name)
        self._slot_vars: Dict[str, str] = {}
        self._custom_functions: Dict[str, Tuple[str, Any]] = custom_functions or {}

        self.func_map: Dict[str, str] = {**self.SYMPY_FUNC_MAP, **self.SYMPY_LOGIC_MAP}
        # Allow caller to extend the maps
        if extra_sympy_funcs:
            self.func_map = {**self.func_map, **extra_sympy_funcs}
        if extra_constants:
            self.CONSTANT_MAP = {**self.CONSTANT_MAP, **extra_constants}

        # Eval namespace for simplify_code round-trip
        self._eval_ns: Dict[str, Any] = {
            'sympy': sympy, 'Integer': Integer, 'Rational': Rational,
            'Symbol': Symbol, 'WildSymbol': WildSymbol,
            'WildHeadApp': WildHeadApp, 'WildHeadDeriv': WildHeadDeriv,
            'IDENTITY_ELEMENT': IDENTITY_ELEMENT,
            'x': Symbol('x'),
            'log': sympy.log, 'sqrt': sympy.sqrt,
            'pi': sympy.pi, 'I': sympy.I, 'oo': sympy.oo,
            # Trig
            'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
            'sec': sympy.sec, 'csc': sympy.csc, 'cot': sympy.cot,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
            'atan2': sympy.atan2,
            'asec': sympy.asec, 'acsc': sympy.acsc, 'acot': sympy.acot,
            # Hyperbolic
            'sinh': sympy.sinh, 'cosh': sympy.cosh, 'tanh': sympy.tanh,
            'sech': sympy.sech, 'csch': sympy.csch, 'coth': sympy.coth,
            'asinh': sympy.asinh, 'acosh': sympy.acosh, 'atanh': sympy.atanh,
            'asech': sympy.asech, 'acsch': sympy.acsch, 'acoth': sympy.acoth,
            # Other
            'exp': sympy.exp, 'Abs': sympy.Abs,
            'elliptic_e': sympy.elliptic_e, 'elliptic_f': sympy.elliptic_f,
            'appellf1': sympy.appellf1,
            'root': sympy.root, 'diff': sympy.diff,
            'denom': sympy.denom, 'frac': sympy.frac, 'floor': sympy.floor,
            'simplify': sympy.simplify, 'hyper': sympy.hyper,
            # Logical operators — use unevaluated wrappers so simplify_code
            # round-trip preserves And(...)/Or(...)/Not(...) form rather than
            # the &/|/~ infix operators that sympy.And/Or/Not would produce.
            'And': sympy.Function('And'),
            'Or': sympy.Function('Or'),
            'Not': sympy.Function('Not'),
        }

        # Register custom functions in the eval namespace
        for wolfram_name, (code_str, obj) in self._custom_functions.items():
            if obj is None:
                continue
            if '.' in code_str:
                # Only register the namespace prefix (e.g. 'rubi_utils') so that
                # eval('rubi_utils.Subst(...)') works.  Do NOT register the short
                # name ('Subst') — the generated code uses the qualified form and
                # simplify_code must preserve it.
                ns_key = code_str.split('.')[0]
                self._eval_ns[ns_key] = obj
            else:
                self._eval_ns[code_str] = obj

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def fixed_var(self) -> str:
        return self._fixed_var

    @fixed_var.setter
    def fixed_var(self, val: str) -> None:
        self._fixed_var = val

    @property
    def wildcards_non_optional(self) -> Set[str]:
        return self._wildcards_non_optional

    @property
    def wildcards_optional(self) -> Set[str]:
        return self._wildcards_optional

    @property
    def eval_ns(self) -> Dict[str, Any]:
        return self._eval_ns

    @property
    def wild_defs(self) -> List[str]:
        """Variable definition strings for WildSymbol declarations."""
        return list(self._wild_defs)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def reset(self) -> None:
        """Reset per-rule state (wildcard sets and defs)."""
        self._wildcards_non_optional = set()
        self._wildcards_optional = set()
        self._symbols = set()
        self._wild_defs = []

    def convert(self, ffl: Any, *, is_pattern: bool = False) -> str:
        """Convert an FFL node to a SymPy code string.

        Parameters
        ----------
        ffl : list or str
            A Mathematica Full-Form List node.
        is_pattern : bool
            If True, Pattern/Optional nodes produce wildcard references.

        Returns
        -------
        str
            Python code string that evaluates to a SymPy expression.
        """
        if isinstance(ffl, str):
            return self._atom_to_code(ffl, is_pattern)

        if not isinstance(ffl, list) or not ffl:
            return repr(ffl)

        head = ffl[0]

        # Non-string head (e.g., F_[x_]) -- unsupported
        if not isinstance(head, str):
            raise ValueError(
                f"Non-string function head {head!r} -- function-head wildcard "
                f"patterns (e.g., F_[x_]) are not yet supported."
            )

        # -- Pattern / Optional ------------------------------------------------
        if head == 'Pattern':
            return self._pattern_to_code(ffl)
        if head == 'Optional':
            return self._optional_to_code(ffl)

        # -- Slot (pure function argument placeholder) --------------------------
        if head == 'Slot':
            slot_num = ffl[1] if len(ffl) > 1 else '1'
            if slot_num in self._slot_vars:
                return self._slot_vars[slot_num]
            # Outside a Function context, fall back to a generic representation
            return f"Symbol('xi{slot_num}')"

        # -- Function (pure function / Lambda) ---------------------------------
        # Function[body]         -> Lambda(xi1, body_with_Slot1_replaced)
        # Function[param, body]  -> Lambda(param, body)
        # Function[{p1,p2}, body] -> Lambda((p1,p2), body)
        if head == 'Function':
            return self._function_to_code(ffl, is_pattern=is_pattern)

        # -- Arithmetic --------------------------------------------------------
        if head == 'Plus':
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"({' + '.join(args)})"
        if head == 'Times':
            if len(ffl) > 1 and ffl[1] == '1':
                if len(ffl) == 3:
                    return self.convert(ffl[2], is_pattern=is_pattern)
                args = [self.convert(a, is_pattern=is_pattern) for a in ffl[2:]]
            else:
                args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"({' * '.join(args)})"
        if head == 'Power':
            base = self.convert(ffl[1], is_pattern=is_pattern)
            exp_code = self.convert(ffl[2], is_pattern=is_pattern)
            return f"({base})**({exp_code})"

        # -- Boolean / logical operators ---------------------------------------
        # Emit as bare And(...)/Or(...)/Not(...) calls so the generated code is
        # independent of the execution namespace (the caller decides whether
        # And means sympy.And, a constraint combiner, etc.).
        # The eval_ns maps these to sympy.Function wrappers so that
        # simplify_code round-trips correctly without &/|/~ infix rewriting.
        if head == 'And':
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"And({', '.join(args)})"
        if head == 'Or':
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"Or({', '.join(args)})"
        if head == 'Not':
            arg = self.convert(ffl[1], is_pattern=is_pattern)
            return f"Not({arg})"

        # -- ArcTan (1 or 2 args) ----------------------------------------------
        if head == 'ArcTan':
            if len(ffl) == 3:
                x_arg = self.convert(ffl[1], is_pattern=is_pattern)
                y_arg = self.convert(ffl[2], is_pattern=is_pattern)
                return f'sympy.atan2({y_arg}, {x_arg})'
            arg = self.convert(ffl[1], is_pattern=is_pattern)
            return f'sympy.atan({arg})'

        # -- Hypergeometric2F1 -------------------------------------------------
        if head == 'Hypergeometric2F1' and len(ffl) == 5:
            a = self.convert(ffl[1], is_pattern=is_pattern)
            b = self.convert(ffl[2], is_pattern=is_pattern)
            c = self.convert(ffl[3], is_pattern=is_pattern)
            z = self.convert(ffl[4], is_pattern=is_pattern)
            return f"sympy.hyper([{a}, {b}], [{c}], {z})"

        # -- List: custom_functions override or Python list literal -------------
        if head == 'List':
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            if head in self._custom_functions:
                code_str, _ = self._custom_functions[head]
                return f"{code_str}({', '.join(args)})"
            return f"[{', '.join(args)}]"

        # -- N-ary comparison operators (chain with And) -----------------------
        # MUST be checked before custom_functions: LessEqual[3, Denom[p], 4]
        # has 3 args and must become And(LeQ(3,x), LeQ(x,4)), not LeQ(3,x,4).
        # In constraint context the caller registers LessEqual→LeQ etc. via
        # custom_functions; we honour that mapping so the chain uses the deferred
        # constraint class instead of an eagerly-evaluated sympy.Le.
        _CHAINED_COMPARISON_WOLFRAM = {'Less', 'Greater', 'LessEqual', 'GreaterEqual'}
        _CHAINED_COMPARISON_DEFAULT = {
            'Less': 'sympy.Lt',
            'Greater': 'sympy.Gt',
            'LessEqual': 'sympy.Le',
            'GreaterEqual': 'sympy.Ge',
        }
        if head in _CHAINED_COMPARISON_WOLFRAM and len(ffl) > 3:
            # Use custom mapping if provided (e.g. LeQ in constraint context),
            # otherwise fall back to the eager sympy.Le etc.
            if head in self._custom_functions:
                op = self._custom_functions[head][0]
            else:
                op = _CHAINED_COMPARISON_DEFAULT[head]
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            pairs = [f"{op}({args[i]}, {args[i+1]})" for i in range(len(args) - 1)]
            if len(pairs) == 1:
                return pairs[0]
            return f"And({', '.join(pairs)})"

        # -- Custom functions (before built-in map) ----------------------------
        if head in self._custom_functions:
            code_str, _ = self._custom_functions[head]
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"{code_str}({', '.join(args)})"

        # -- Known SymPy functions ---------------------------------------------
        if head in self.func_map:
            func = self.func_map[head]
            args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
            return f"{func}({', '.join(args)})"

        # -- RemoveContent (pass through) --------------------------------------
        if head == 'RemoveContent':
            return self.convert(ffl[1], is_pattern=is_pattern)

        # -- Generic fallback: sympy.Function('Head')(...) ---------------------
        args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
        return f"sympy.Function('{head}')({', '.join(args)})"

    # Alias for backward compatibility with code using the old class name
    ffl_to_sympy_expr = convert

    def preprocess_test_ffl(self, ffl: Any) -> Any:
        """Normalize test-suite specific constructs before conversion."""
        if not isinstance(ffl, list):
            return ffl
        if ffl[0] == 'If' and len(ffl) >= 3:
            return self.preprocess_test_ffl(ffl[2])
        return [self.preprocess_test_ffl(item) for item in ffl]

    def wildcard_ref(self, name: str) -> Optional[str]:
        """Get the Python reference for a wildcard name, or None."""
        if name in self._wildcards_non_optional:
            return f"{name}_"
        if name in self._wildcards_optional:
            return f"_{name}_"
        return None

    # -------------------------------------------------------------------------
    # Internals
    # -------------------------------------------------------------------------

    def _atom_to_code(self, atom: str, is_pattern: bool) -> str:
        """Convert an atom (string) to SymPy code."""
        if atom in self.CONSTANT_MAP:
            return self.CONSTANT_MAP[atom]
        try:
            n = int(atom)
            return f'Integer({n})'
        except ValueError:
            pass
        try:
            float(atom)
            return f"Rational('{atom}')"
        except ValueError:
            pass
        # Fixed variable (non-wildcard)
        if atom == self._fixed_var:
            return 'x'
        # Known wildcard references
        if atom in self._wildcards_optional:
            var_name = f'_{atom}_'
            if var_name not in self._eval_ns:
                ws = WildSymbol(atom, optional_value=IDENTITY_ELEMENT)
                self._eval_ns[var_name] = ws
            return var_name
        if atom in self._wildcards_non_optional:
            var_name = f'{atom}_'
            if var_name not in self._eval_ns:
                ws = WildSymbol(atom)
                self._eval_ns[var_name] = ws
            return var_name
        # Plain symbol
        self._symbols.add(atom)
        symbol_code = f"Symbol('{atom}')"
        self._eval_ns.setdefault(atom, Symbol(atom))
        return symbol_code

    def _pattern_to_code(self, ffl) -> str:
        """['Pattern', name, ['Blank', ...]] -> wildcard reference."""
        name = ffl[1]
        if name == self._fixed_var:
            return 'x'
        self._wildcards_non_optional.add(name)
        var_name = f'{name}_'
        def_str = f"{var_name} = WildSymbol('{name}')"
        self._wild_defs.append(def_str)
        ws = WildSymbol(name)
        self._eval_ns[var_name] = ws
        return var_name

    def _optional_to_code(self, ffl) -> str:
        """['Optional', ['Pattern', name, ['Blank']]] -> optional wildcard."""
        inner = ffl[1]
        if isinstance(inner, list) and inner[0] == 'Pattern':
            name = inner[1]
            if name == self._fixed_var:
                # ``x_.`` where ``x`` is ALSO bound as the fixed variable (``x_Symbol``).
                # Both bind the same name, so the "absent" branch would have to give
                # ``x`` the Times identity 1 -- which then fails ``x_Symbol``. The
                # optional branch is therefore unreachable and the factor is in fact
                # mandatory. Verified in Mathematica: ``g[x_.*h[x_], x_Symbol]``
                # matches ``g[z h[z], z]`` but NOT ``g[h[z], z]``.
                return 'x'
            self._wildcards_non_optional.add(name)
            self._wildcards_optional.add(name)
            var_name = f'_{name}_'
            def_str = f"{var_name} = WildSymbol('{name}', optional_value=IDENTITY_ELEMENT)"
            self._wild_defs.append(def_str)
            ws = WildSymbol(name, optional_value=IDENTITY_ELEMENT)
            self._eval_ns[var_name] = ws
            return var_name
        return self.convert(inner, is_pattern=True)

    def _function_to_code(self, ffl, *, is_pattern: bool = False) -> str:
        """Convert Mathematica Function[...] to sympy.Lambda(...).

        Supported forms:
          ["Function", body]             -> Lambda(Symbol('xi1'), body)
            where Slot[1] in body is replaced with Symbol('xi1')
          ["Function", param, body]      -> Lambda(Symbol(param), body)
          ["Function", ["List", ...], body] -> Lambda(tuple_of_symbols, body)
        """
        if len(ffl) == 2:
            # Pure function with Slot references: Function[body]
            body = ffl[1]
            # Find all Slot numbers used in body
            slot_nums = self._collect_slots(body)
            if not slot_nums:
                slot_nums = {'1'}  # default single arg
            # Build slot variable mapping
            old_slot_vars = self._slot_vars.copy()
            self._slot_vars = {n: f"Symbol('xi{n}')" for n in slot_nums}
            try:
                body_code = self.convert(body, is_pattern=is_pattern)
            finally:
                self._slot_vars = old_slot_vars
            # Build Lambda
            sorted_nums = sorted(slot_nums, key=int)
            if len(sorted_nums) == 1:
                param_code = f"Symbol('xi{sorted_nums[0]}')"
            else:
                params = ', '.join(f"Symbol('xi{n}')" for n in sorted_nums)
                param_code = f"({params})"
            return f"Lambda({param_code}, {body_code})"

        elif len(ffl) == 3:
            # Named parameter form: Function[param, body] or Function[{params}, body]
            params_ffl = ffl[1]
            body = ffl[2]
            if isinstance(params_ffl, str):
                # Single named parameter
                old_slot_vars = self._slot_vars.copy()
                self._slot_vars = {}  # no Slot mapping needed
                try:
                    body_code = self.convert(body, is_pattern=is_pattern)
                finally:
                    self._slot_vars = old_slot_vars
                return f"Lambda(Symbol('{params_ffl}'), {body_code})"
            elif isinstance(params_ffl, list) and params_ffl[0] == 'List':
                # Multiple named parameters: Function[{x, y}, body]
                param_names = params_ffl[1:]
                old_slot_vars = self._slot_vars.copy()
                self._slot_vars = {}
                try:
                    body_code = self.convert(body, is_pattern=is_pattern)
                finally:
                    self._slot_vars = old_slot_vars
                params = ', '.join(f"Symbol('{p}')" for p in param_names)
                return f"Lambda(({params}), {body_code})"

        # Fallback — shouldn't normally be reached
        args = [self.convert(a, is_pattern=is_pattern) for a in ffl[1:]]
        return f"Lambda({', '.join(args)})"

    @staticmethod
    def _collect_slots(ffl) -> Set[str]:
        """Recursively collect all Slot numbers from an FFL subtree."""
        result: Set[str] = set()
        if isinstance(ffl, list) and len(ffl) > 0:
            if ffl[0] == 'Slot':
                result.add(ffl[1] if len(ffl) > 1 else '1')
            else:
                for child in ffl[1:]:
                    result.update(FFLConverter._collect_slots(child))
        return result
