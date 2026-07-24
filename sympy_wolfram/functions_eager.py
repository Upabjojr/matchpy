# -*- coding: utf-8 -*-
"""Self-contained EAGER Wolfram-standard helpers (plain functions).

These are the eager implementations of a few Mathematica standard-library
functions whose logic depends *solely* on SymPy.  They used to live in
``rubi_rules.utils.utility_functions``; they are not Rubi-specific, so they live
here and ``utility_functions`` imports them back (the correct layer direction:
rubi_rules -> sympy_wolfram).

Deferred (``MathematicaExpr``) counterparts of the same name live in
``sympy_wolfram.mathematica_functions`` and delegate here.

Only functions with a purely-SymPy body belong here.  Rubi's ``First``/``Rest``/
``Exponent``/``Apart``/``Part`` are excluded: their bodies call Rubi integration
utilities (``SumQ``/``Sort``/``PolynomialQ``/``RationalFunctionQ``/``Util_Part``)
and stay in ``rubi_rules``.
"""
import sympy
from sympy import Basic, I, postorder_traversal


def LeafCount(expr):
    """Mathematica LeafCount[expr] — number of nodes in the expression tree."""
    return len(list(postorder_traversal(expr)))


def Length(expr):
    """Mathematica Length[expr] — number of elements."""
    if isinstance(expr, (tuple, list, sympy.Tuple)):
        return len(expr)
    return len(expr.args)


def Complex(a, b):
    """Mathematica Complex[re, im] — construct a complex number a + I*b."""
    return a + I * b


def Not(var):
    """Mathematica Not[expr] — logical negation (tolerant of bool/None/Relational)."""
    if isinstance(var, bool):
        return not var
    elif var is None:
        return None
    elif isinstance(var, Basic) and var.is_Relational:
        var = False
    return not var
