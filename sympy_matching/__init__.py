# -*- coding: utf-8 -*-
"""MatchPy integration for SymPy symbolic mathematics.

This package provides:
- OperationHead definitions for SymPy operations (Add, Mul, Pow, sin, cos, ...)
- Singledispatch converters between SymPy and MatchPy expression trees
- WildSymbol: a SymPy type that converts to MatchPy Wildcard via to_matchpy_expression
- Pattern matching utilities for symbolic math

Usage:
    from sympy_matching import to_matchpy_expression, matchpy_to_sympy, WildSymbol
    from sympy_matching.operations import ADD, MUL, POW, SIN, COS

    import sympy
    from sympy import Eq
    from matchpy import to_matchpy_expression, Pattern
    from matchpy.expressions.constraints import FreeOf

    # Define wildcards as SymPy-compatible symbols
    a_ = WildSymbol('a')
    b_ = WildSymbol('b')
    var = sympy.Symbol('x')

    # Write patterns naturally using SymPy arithmetic
    linear = Pattern(to_matchpy_expression(Eq(a_*var + b_, 0)),
                     FreeOf('a', 'x'), FreeOf('b', 'x'))
"""
from .operations import ADD, MUL, POW, SIN, COS, TAN, EXP, LOG, EQUALITY
from .wild import WildSymbol, IDENTITY_ELEMENT
from . import conversion  # registers singledispatch handlers
from . import registered_heads  # registers additional SymPy function heads
from . import json_ext  # registers JSON serialization extensions

# Re-export the key conversion functions (to_matchpy_expression is matchpy's ingestion dispatch)
from matchpy.expressions.expressions import to_matchpy_expression
matchpy_to_sympy = conversion.matchpy_to_sympy

# Reusable SymPy -> matchpy pattern-matching-rule machinery. Everything needed to build
# a matchpy ManyToOneReplacer from rules made of SymPy patterns/replacements/constraints
# (ordinary SymPy objects mixed with WildSymbol) -- with NO dependency on sympy_wolfram
# or rubi_rules. Import matchpy + sympy_matching and you can define your own matcher.
from .constraint import SympyMatchingConstraint
from .matching_rule import SympyMatchingRule, build_replacer, build_tracing_replacer
from .conversion import register_head_converter
