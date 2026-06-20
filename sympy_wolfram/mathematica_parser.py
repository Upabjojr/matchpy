# -*- coding: utf-8 -*-
"""Parse Mathematica standard-notation strings into Full-Form List (FFL).

This module wraps SymPy's internal ``MathematicaParser`` tokenizer/parser to
convert Mathematica notation (e.g. ``"Sin[x] + x^2"``) into the nested-list
FFL representation used by the rest of ``sympy_wolfram``.

Public API
----------
mathematica_to_ffl(expr_str)
    Convert a Mathematica expression string to FFL (nested list).

ffl_to_sympy_code(ffl)
    FFL → Python code string (eval-able to SymPy).

ffl_to_sympy_short_code(ffl)
    Like ffl_to_sympy_code but with a simplification round-trip.

mathematica_to_sympy_code(expr_str)
    Mathematica string → FFL → Python code string (eval-able to SymPy).

mathematica_to_sympy_short_code(expr_str)
    Like mathematica_to_sympy_code but with a str(eval(...)) round-trip
    simplification pass for shorter output when safe.

mathematica_to_sympy(expr_str)
    End-to-end: Mathematica string → FFL → SymPy expression object.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

import sympy
from sympy import Integer, Rational, Symbol
from sympy.parsing.mathematica import MathematicaParser

from .ffl_to_sympy import FFLConverter, _wild_printer


# Module-level parser instance (stateless for tokenization)
_PARSER = MathematicaParser()

# Type alias for the custom_functions dict expected by public APIs.
# Maps Wolfram head name → (qualified_code_str, python_object)
CustomFunctionsDict = Dict[str, Tuple[str, Any]]


def mathematica_to_ffl(expr_str: str) -> List:
    """Convert a Mathematica standard-notation string to a Full-Form List.

    Uses SymPy's ``MathematicaParser`` tokenizer and FFL builder internally.

    Parameters
    ----------
    expr_str : str
        A Mathematica expression in standard notation, e.g.
        ``"(a + b*x)^m"``, ``"Sin[x] + Cos[x]"``, ``"Log[1 + x]/x"``.

    Returns
    -------
    list
        Nested list in Full-Form List format, e.g.
        ``['Power', ['Plus', 'a', ['Times', 'b', 'x']], 'm']``.

    Examples
    --------
    >>> mathematica_to_ffl("x^2")
    ['Power', 'x', '2']
    >>> mathematica_to_ffl("Sin[x] + 1")
    ['Plus', ['Sin', 'x'], '1']
    """
    tokens = _PARSER._from_mathematica_to_tokens(expr_str)
    return _PARSER._from_tokens_to_fullformlist(tokens)


# ---------------------------------------------------------------------------
# FFL-level API (skip Mathematica parsing)
# ---------------------------------------------------------------------------


def ffl_to_sympy_code(
    ffl: Any,
    fixed_var: str = "x",
    custom_functions: Optional[CustomFunctionsDict] = None,
    wildcards: Optional[Set[str]] = None,
    optional_wildcards: Optional[Set[str]] = None,
) -> Tuple[str, Dict[str, Any], List[str], list[str]]:
    """Convert a Full-Form List to an eval-able Python code string.

    This is the lower-level entry point that operates directly on an FFL
    structure, skipping the Mathematica string-parsing step.

    Parameters
    ----------
    ffl : list or str
        A Full-Form List (nested list), e.g. ``['Power', 'x', '2']``.
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    custom_functions : dict, optional
        Mapping from Wolfram head names to custom callables.  Each value is
        a 2-tuple ``(qualified_code_str, obj)``—see
        :class:`~.ffl_to_sympy.FFLConverter` for details.
    wildcards : set of str, optional
        Pre-known non-optional wildcard names.  Bare atoms matching these
        names will be emitted as ``name_`` references (useful when processing
        replacement/constraint FFL where wildcards appear as plain atoms
        rather than ``['Pattern', ...]`` nodes).
    optional_wildcards : set of str, optional
        Pre-known optional wildcard names.  Bare atoms matching these names
        will be emitted as ``_name_`` references.

    Returns
    -------
    code : str
        A Python expression string that evaluates to a SymPy ``Basic`` object.
    eval_ns : dict
        A namespace dictionary suitable for passing to ``eval(code, eval_ns)``.
    wild_defs : list of str
        Variable definition statements for WildSymbol declarations.

    Examples
    --------
    >>> code, ns, defs, _symbols = ffl_to_sympy_code(['Power', 'x', '2'])
    >>> code
    '(x)**(Integer(2))'
    >>> eval(code, ns)
    x**2
    """
    converter = FFLConverter(fixed_var=fixed_var, custom_functions=custom_functions)
    if wildcards:
        converter._wildcards_non_optional.update(wildcards)
    if optional_wildcards:
        converter._wildcards_optional.update(optional_wildcards)
        converter._wildcards_non_optional.update(optional_wildcards)
    code = converter.convert(ffl)

    # Build eval namespace
    ns: Dict[str, Any] = dict(converter._eval_ns)
    ns["x"] = Symbol(fixed_var)

    symbols = sorted(converter._symbols)

    return code, ns, converter.wild_defs, symbols


def _simplify_code(code: str, ns: Dict[str, Any]) -> str:
    """Try ``_wild_printer.doprint(eval(code))`` round-trip for a shorter form.

    Uses :data:`_wild_printer` so that WildSymbol instances are printed with
    their variable-name convention (``m_`` / ``_m_``) rather than the bare
    SymPy name.  Returns the printed form only when ``eval(printed, ns)``
    reproduces the same SymPy ``Basic`` object.  Otherwise returns *code*.
    """
    try:
        obj = eval(code, ns)
        short = _wild_printer.doprint(obj)
        recovered = eval(short, ns)
        if isinstance(recovered, sympy.Basic):
            if recovered == obj:
                return short
            if (recovered - obj).simplify() == 0:
                return short
    except Exception:
        pass
    return code


def ffl_to_sympy_short_code(
    ffl: Any,
    fixed_var: str = "x",
    extra_symbols: Optional[Dict[str, Symbol]] = None,
    custom_functions: Optional[CustomFunctionsDict] = None,
    wildcards: Optional[Set[str]] = None,
    optional_wildcards: Optional[Set[str]] = None,
) -> Tuple[str, Dict[str, Any], List[str], list[str]]:
    """Like :func:`ffl_to_sympy_code` but with a simplification pass.

    Operates directly on an FFL structure, skipping Mathematica parsing.

    Parameters
    ----------
    ffl : list or str
        A Full-Form List (nested list).
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    extra_symbols : dict, optional
        Mapping of ``{name: Symbol}`` to inject into the eval namespace.
    custom_functions : dict, optional
        Mapping from Wolfram head names to custom callables.
    wildcards : set of str, optional
        Pre-known non-optional wildcard names (see :func:`ffl_to_sympy_code`).
    optional_wildcards : set of str, optional
        Pre-known optional wildcard names (see :func:`ffl_to_sympy_code`).

    Returns
    -------
    short_code : str
        A (possibly simplified) Python expression string.
    eval_ns : dict
        Namespace for ``eval(short_code, eval_ns)``.
    wild_defs : list of str
        WildSymbol variable definitions.

    Examples
    --------
    >>> short, ns, defs, _symbols = ffl_to_sympy_short_code(['Power', 'x', '2'])
    >>> short
    'x**2'
    """
    code, ns, wild_defs, _symbols = ffl_to_sympy_code(
        ffl, fixed_var, custom_functions=custom_functions,
        wildcards=wildcards, optional_wildcards=optional_wildcards,
    )
    if extra_symbols:
        ns.update(extra_symbols)

    short = _simplify_code(code, ns)
    return short, ns, wild_defs, _symbols


# ---------------------------------------------------------------------------
# Mathematica-string-level API (parse + delegate to FFL API)
# ---------------------------------------------------------------------------


def mathematica_to_sympy_code(
    expr_str: str,
    fixed_var: str = "x",
    custom_functions: Optional[CustomFunctionsDict] = None,
) -> Tuple[str, Dict[str, Any], List[str], list[str]]:
    """Convert a Mathematica expression string to an eval-able Python code string.

    Pipeline: Mathematica notation → FFL → SymPy code string.
    Equivalent to ``ffl_to_sympy_code(mathematica_to_ffl(expr_str), ...)``.

    Parameters
    ----------
    expr_str : str
        Mathematica expression in standard notation.
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    custom_functions : dict, optional
        Mapping from Wolfram head names to custom callables.  Each value is
        a 2-tuple ``(qualified_code_str, obj)``—see
        :class:`~.ffl_to_sympy.FFLConverter` for details.

    Returns
    -------
    code : str
        A Python expression string that evaluates to a SymPy ``Basic`` object.
        Uses ``sympy.*`` qualified names, ``Integer(...)``, ``Rational(...)``,
        ``Symbol(...)`` etc.  Pattern variables are referenced by name
        (e.g. ``m_`` or ``_m_``) and defined in *wild_defs*.
    eval_ns : dict
        A namespace dictionary suitable for passing to ``eval(code, eval_ns)``.
        Contains ``sympy``, common functions, a ``Symbol`` for the
        fixed variable, and any WildSymbol variables.
    wild_defs : list of str
        Variable definition statements for WildSymbol declarations.  Each
        entry is a Python assignment string (e.g.
        ``"m_ = WildSymbol('m')"``) that should be exec'd before eval'ing
        *code* if building a standalone script.  The eval_ns already contains
        these bindings, so they are informational for code-generation use.

    Examples
    --------
    >>> code, ns, defs, _symbols = mathematica_to_sympy_code("Sin[x] + x^2")
    >>> code
    '(sympy.sin(x) + (x)**(Integer(2)))'
    >>> eval(code, ns)
    x**2 + sin(x)

    >>> code, ns, defs, _symbols = mathematica_to_sympy_code("m_")
    >>> code
    'm_'
    >>> defs
    ["m_ = WildSymbol('m')"]
    """
    ffl = mathematica_to_ffl(expr_str)
    return ffl_to_sympy_code(ffl, fixed_var, custom_functions=custom_functions)


def mathematica_to_sympy_short_code(
    expr_str: str,
    fixed_var: str = "x",
    extra_symbols: Optional[Dict[str, Symbol]] = None,
    custom_functions: Optional[CustomFunctionsDict] = None,
) -> Tuple[str, Dict[str, Any], List[str], list[str]]:
    """Like :func:`mathematica_to_sympy_code` but with a simplification pass.

    Pipeline: Mathematica notation → FFL → simplified code string.
    Equivalent to ``ffl_to_sympy_short_code(mathematica_to_ffl(expr_str), ...)``.

    Parameters
    ----------
    expr_str : str
        Mathematica expression in standard notation.
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    extra_symbols : dict, optional
        Mapping of ``{name: Symbol}`` to inject into the eval namespace
        (needed when the expression contains free parameters beyond *x*).
    custom_functions : dict, optional
        Mapping from Wolfram head names to custom callables.  See
        :class:`~.ffl_to_sympy.FFLConverter` for details.

    Returns
    -------
    short_code : str
        A (possibly simplified) Python expression string.
    eval_ns : dict
        Namespace for ``eval(short_code, eval_ns)``.
    wild_defs : list of str
        WildSymbol variable definitions (same as from
        :func:`mathematica_to_sympy_code`).

    Examples
    --------
    >>> short, ns, defs, _symbols = mathematica_to_sympy_short_code("Sin[x] + x^2")
    >>> short
    'x**2 + sin(x)'
    >>> eval(short, ns)
    x**2 + sin(x)

    >>> short, ns, defs, _symbols = mathematica_to_sympy_short_code(
    ...     "(a + b*x)^m",
    ...     extra_symbols={'a': Symbol('a'), 'b': Symbol('b'), 'm': Symbol('m')},
    ... )
    >>> short
    '(a + b*x)**m'
    """
    ffl = mathematica_to_ffl(expr_str)
    return ffl_to_sympy_short_code(
        ffl, fixed_var, extra_symbols=extra_symbols,
        custom_functions=custom_functions,
    )


def mathematica_to_sympy(
    expr_str: str,
    fixed_var: str = "x",
    extra_symbols: Optional[Dict[str, Symbol]] = None,
    custom_functions: Optional[CustomFunctionsDict] = None,
) -> sympy.Basic:
    """Convert a Mathematica expression string directly to a SymPy object.

    Pipeline: Mathematica notation → FFL → SymPy code string → eval.

    Parameters
    ----------
    expr_str : str
        Mathematica expression in standard notation.
    fixed_var : str
        Name of the fixed (non-wildcard) variable (default ``'x'``).
    extra_symbols : dict, optional
        Mapping of ``{name: Symbol}`` to add to the eval namespace so that
        free parameters evaluate to the correct SymPy symbols.
    custom_functions : dict, optional
        Mapping from Wolfram head names to custom callables.  See
        :class:`~.ffl_to_sympy.FFLConverter` for details.

    Returns
    -------
    sympy.Basic
        The resulting SymPy expression.

    Examples
    --------
    >>> from sympy import Symbol, sin
    >>> mathematica_to_sympy("Sin[x]") == sin(Symbol('x'))
    True
    >>> a, b, x = Symbol('a'), Symbol('b'), Symbol('x')
    >>> mathematica_to_sympy("(a + b*x)^2", extra_symbols={'a': a, 'b': b})
    (a + b*x)**2
    """
    code, ns, _wild_defs, _symbols = mathematica_to_sympy_code(
        expr_str, fixed_var, custom_functions=custom_functions
    )
    if extra_symbols:
        ns.update(extra_symbols)

    return eval(code, ns)
