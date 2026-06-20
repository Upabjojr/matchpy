# -*- coding: utf-8 -*-
"""MatchPy integration for SymPy symbolic mathematics.

This package provides:
- OperationHead definitions for SymPy operations (Add, Mul, Pow, sin, cos, ...)
- Singledispatch converters between SymPy and MatchPy expression trees
- WildSymbol: a SymPy type that converts to MatchPy Wildcard via to_expression
- Pattern matching utilities for symbolic math

Usage:
    from sympy_objects import to_sympy_expression, from_sympy_expression, WildSymbol
    from sympy_objects.operations import ADD, MUL, POW, SIN, COS

    import sympy
    from sympy import Eq
    from matchpy import to_expression, Pattern
    from matchpy.expressions.constraints import FreeQ

    # Define wildcards as SymPy-compatible symbols
    a_ = WildSymbol('a')
    b_ = WildSymbol('b')
    var = sympy.Symbol('x')

    # Write patterns naturally using SymPy arithmetic
    linear = Pattern(to_expression(Eq(a_*var + b_, 0)),
                     FreeQ('a', 'x'), FreeQ('b', 'x'))
"""
from .operations import ADD, MUL, POW, SIN, COS, TAN, EXP, LOG, EQUALITY
from .wild import WildSymbol, IDENTITY_ELEMENT
from .constraints import RubiConstraint
from . import conversion  # registers singledispatch handlers
from . import registered_heads  # registers additional SymPy function heads
from . import json_ext  # registers JSON serialization extensions

# Re-export the key conversion functions
from matchpy.expressions.expressions import to_expression

# Aliases for clarity
to_expression = to_expression
matchpy_to_sympy = conversion.matchpy_to_sympy
