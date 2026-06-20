# -*- coding: utf-8 -*-
"""Core objects for Rubi integration rules."""
import os
import sympy
from typing import Any, List, Tuple
from pydantic import BaseModel

from matchpy.expressions.expressions import (
    Operation, SymbolWrapper, Wildcard, Pattern, OperationHead, Arity,
    to_expression,
)
from matchpy.expressions.constraints import CustomConstraint
from matchpy.matching.many_to_one import ManyToOneReplacer
from matchpy.functions import ReplacementRule

from sympy_objects.conversion import register_sympy_head, matchpy_to_sympy
from sympy_objects.wild import WildSymbol, IDENTITY_ELEMENT

from sympy_objects.constraints import RubiConstraint


class Int(sympy.Function):
    """Symbolic integration function for Rubi pattern matching."""
    nargs = 2


INT = OperationHead(name='Int', arity=Arity.binary)
register_sympy_head(Int, INT)


class RubiRulePattern(BaseModel):
    """A single Rubi integration rule in SymPy form."""
    model_config = dict(arbitrary_types_allowed=True)

    pattern: Any
    constraints: Tuple[Any, ...] = ()
    replacement: Any
    module_name: str = ''
    rule_number: int = 0


def _collect_wild_symbols(expr) -> dict:
    wilds = {}
    if isinstance(expr, WildSymbol):
        wilds[expr.wildcard_name] = expr
    elif hasattr(expr, 'args'):
        for arg in expr.args:
            wilds.update(_collect_wild_symbols(arg))
    return wilds


def _make_replacement_fn(replacement_expr, wild_names, rule):
    def _replacement(**match_dict):
        sympy_subs = {}
        for name, matchpy_val in match_dict.items():
            sympy_subs[name] = matchpy_to_sympy(matchpy_val)
        result = replacement_expr
        for ws in _collect_wild_symbols(replacement_expr).values():
            if ws.wildcard_name in sympy_subs:
                result = result.subs(ws, sympy_subs[ws.wildcard_name])
        # Evaluate RubiFunction nodes (With, Condition, SimplifyIntegrand, …).
        # A Condition whose test fails raises StopIteration, which propagates
        # here and is caught by ManyToOneReplacer.replace() as "no match" —
        # the rule is silently skipped, matching Mathematica's Condition semantics.
        if hasattr(result, 'doit'):
            result = result.doit()
        return to_expression(result)

    _replacement.__qualname__ = f"{rule.module_name}:[{rule.rule_number}]"
    _replacement.__module__ = ""
    return _replacement


def _extract_wild_names(constraint_obj):
    """Extract WildSymbol/Symbol names from a constraint.

    Handles RubiConstraint (via .variables), and Boolean wrappers
    Not(...), Or(...), And(...) by recursing into their args.
    """
    # Handle Not/Or/And wrappers by recursing into args
    if isinstance(constraint_obj, sympy.logic.boolalg.Not):
        inner = constraint_obj.args[0]
        return _extract_wild_names(inner)
    if isinstance(constraint_obj, (sympy.logic.boolalg.Or, sympy.logic.boolalg.And)):
        names = set()
        for arg in constraint_obj.args:
            names.update(_extract_wild_names(arg))
        return sorted(names)

    try:
        free_syms = constraint_obj.free_symbols
        names = []
        for s in free_syms:
            if isinstance(s, WildSymbol):
                names.append(s.wildcard_name)
            elif hasattr(s, 'name') and s.name.endswith('_'):
                names.append(s.name)
        if names:
            return sorted(set(names))
    except (AttributeError, TypeError):
        pass
    if hasattr(constraint_obj, 'variables'):
        return [v for v in constraint_obj.variables if v.isidentifier()]
    return []


def _make_constraint_checker(constraint_obj, variables):
    """Build a checker function for a single constraint (possibly compound).

    Returns a callable(**kwargs) -> bool.
    """
    # Not(inner): negate inner check
    if isinstance(constraint_obj, sympy.logic.boolalg.Not):
        inner = constraint_obj.args[0]
        inner_checker = _make_constraint_checker(inner, variables)
        def check_not(**kwargs):
            return not inner_checker(**kwargs)
        return check_not

    # Or(a, b, ...): any inner check passes
    if isinstance(constraint_obj, sympy.logic.boolalg.Or):
        inner_checkers = [_make_constraint_checker(arg, variables) for arg in constraint_obj.args]
        def check_or(**kwargs):
            return any(c(**kwargs) for c in inner_checkers)
        return check_or

    # And(a, b, ...): all inner checks pass
    if isinstance(constraint_obj, sympy.logic.boolalg.And):
        inner_checkers = [_make_constraint_checker(arg, variables) for arg in constraint_obj.args]
        def check_and(**kwargs):
            return all(c(**kwargs) for c in inner_checkers)
        return check_and

    # RubiConstraint: use .check() directly
    if isinstance(constraint_obj, RubiConstraint):
        def check_rubi(**kwargs):
            return constraint_obj.check(**kwargs)
        return check_rubi

    # Generic SymPy Boolean: use .subs() approach
    def check_subs(**kwargs):
        subs_dict = {}
        for name in variables:
            if name in kwargs:
                val = kwargs[name]
                val = matchpy_to_sympy(val)
                # Try to find WildSymbol in constraint's free_symbols
                subs_dict[sympy.Symbol(name)] = val
        result = constraint_obj.subs(subs_dict)
        return result == True
    return check_subs


def _make_matchpy_constraint(constraint_obj, wild_names, pattern_wilds):
    """Convert a constraint into a MatchPy CustomConstraint.

    Handles RubiConstraint, Not/Or/And wrappers, and generic SymPy Booleans.
    """
    variables = _extract_wild_names(constraint_obj)
    if not variables:
        return CustomConstraint(lambda: True)

    checker = _make_constraint_checker(constraint_obj, variables)

    # Build lambda with proper parameter names for MatchPy introspection
    params = ', '.join(variables)
    fn_code = f"lambda {params}: __checker__({', '.join(f'{v}={v}' for v in variables)})"
    fn = eval(fn_code, {'__checker__': checker})

    return CustomConstraint(fn)


def build_replacer(rules: List[RubiRulePattern]) -> ManyToOneReplacer:
    replacer = ManyToOneReplacer()
    for i, rule in enumerate(rules):
        matchpy_pattern_expr = to_expression(rule.pattern)
        wilds = _collect_wild_symbols(rule.pattern)
        wild_names = list(wilds.keys())
        matchpy_constraints = []
        for constraint in rule.constraints:
            mc = _make_matchpy_constraint(constraint, wild_names, wilds)
            matchpy_constraints.append(mc)
        pattern = Pattern(matchpy_pattern_expr, *matchpy_constraints)
        replacement_fn = _make_replacement_fn(rule.replacement, wild_names, rule)
        replacer.add(ReplacementRule(pattern, replacement_fn))
    return replacer


_RULES_DIR = os.path.join(os.path.dirname(__file__), 'rules')


def load_rules(pattern: str = '**') -> ManyToOneReplacer:
    import importlib
    import importlib.util
    from pathlib import Path

    rules_dir = Path(_RULES_DIR)
    all_rules = []

    if not pattern.endswith('.py') and not pattern.endswith('*'):
        pattern = pattern.rstrip('/') + '/**/*.py'
    elif pattern.endswith('**'):
        pattern = pattern + '/*.py'
    elif pattern.endswith('*') and not pattern.endswith('*.py'):
        pattern = pattern + '.py'

    for py_file in sorted(rules_dir.glob(pattern)):
        if py_file.name.startswith('_'):
            continue
        module_name = f"rubi_rules.rules.{py_file.relative_to(rules_dir).with_suffix('').as_posix().replace('/', '.')}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'RULES'):
                all_rules.extend(mod.RULES)
        except Exception as e:
            import warnings, traceback
            warnings.warn(
                f"Failed to load rules from {py_file.name}: {e}\n"
                + traceback.format_exc()
            )

    return build_replacer(all_rules)


_CACHED_REPLACER = None


def _matchpy_integrate(expr, x, replacer):
    mp_expr = to_expression(Int(expr, x))
    result = replacer.replace(mp_expr)
    return matchpy_to_sympy(result)


def _preprocess_integrate(expr, x, replacer):
    expr = sympy.sympify(expr)
    if x not in expr.free_symbols:
        return expr * x
    if expr.is_Add:
        return sympy.Add(*[_preprocess_integrate(t, x, replacer) for t in expr.args])
    if expr.is_Mul:
        free_factors = [f for f in expr.args if x not in f.free_symbols]
        x_factors = [f for f in expr.args if x in f.free_symbols]
        if free_factors:
            const = sympy.Mul(*free_factors)
            core = x_factors[0] if len(x_factors) == 1 else sympy.Mul(*x_factors)
            return const * _preprocess_integrate(core, x, replacer)
    return _matchpy_integrate(expr, x, replacer)


def rubi_integrate(expr, x, pattern: str = '**'):
    """Integrate expr with respect to x using the Rubi rule set.

    The rule files are written with Symbol('x') as the canonical integration
    variable.  When the caller passes a different variable (e.g. Symbol('y')),
    we perform a three-step substitution so the rules still apply:

        1. Replace the existing Symbol('x') in expr with a Dummy symbol to
           avoid a name collision when the user's variable is renamed to 'x'.
        2. Replace the user's integration variable with Symbol('x').
        3. Integrate with respect to Symbol('x').
        4. Undo the substitution: Symbol('x') → original variable,
           Dummy → Symbol('x').

    Examples
    --------
    >>> from sympy import symbols
    >>> x, y = symbols('x y')
    >>> rubi_integrate(x * y, x)   # x**2*y/2
    >>> rubi_integrate(x * y, y)   # x*y**2/2
    """
    global _CACHED_REPLACER
    if _CACHED_REPLACER is None:
        _CACHED_REPLACER = load_rules(pattern)

    expr = sympy.sympify(expr)
    x = sympy.sympify(x)
    x_canonical = sympy.Symbol('x')

    if x == x_canonical:
        # Integration variable is already Symbol('x') — no substitution needed.
        return _preprocess_integrate(expr, x_canonical, _CACHED_REPLACER)

    # Replace existing Symbol('x') in expr with a Dummy to avoid it being
    # renamed to the integration variable in the next step.
    dummy = sympy.Dummy('_x_var')
    expr_sub = expr.subs(x_canonical, dummy).subs(x, x_canonical)
    result = _preprocess_integrate(expr_sub, x_canonical, _CACHED_REPLACER)
    # Undo the substitution: canonical x → original variable, dummy → x.
    return result.subs(x_canonical, x).subs(dummy, x_canonical)


def reset_cache():
    global _CACHED_REPLACER
    _CACHED_REPLACER = None
