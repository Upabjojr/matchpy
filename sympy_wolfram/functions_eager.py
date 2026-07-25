# -*- coding: utf-8 -*-
"""Self-contained EAGER Wolfram-standard helpers (plain functions).

These are the eager implementations of a few Mathematica standard-library
functions whose logic depends *solely* on SymPy.  They used to live in
``rubi_rules.utils.utility_functions``; they are not Rubi-specific, so they live
here and ``utility_functions`` imports them back (the correct layer direction:
rubi_rules -> sympy_wolfram).

Deferred (``MathematicaExpr``) counterparts of the same name live in
``sympy_wolfram.mathematica_functions`` and delegate here.

Only functions with a purely-SymPy body belong here.  ``First``/``Rest``/
``Numerator``/``Denominator``/``Part``/``Apart``/``Simplify`` used to *look* Rubi-coupled
because their Rubi bodies called ``SumQ``/``ProductQ``/``Sort``/``RationalFunctionQ``/
``Util_Part`` -- but every one of those is itself a generic Wolfram/SymPy operation
(``is_Add``/``is_Mul``/sort-by-``sort_key``/``is_rational_function``/part-extraction),
so the coupling was spurious.  They are inlined below and the functions live here.
"""
import sympy
from sympy import (
    Add, Basic, I, Integer, Mul, Pow, S, Symbol, Tuple,
    expand, postorder_traversal, sympify, together,
)
from sympy.core.function import Function
from sympy.polys.partfrac import apart
from sympy.simplify.simplify import fraction, simplify


def LeafCount(expr):
    """Mathematica LeafCount[expr] — number of nodes in the expression tree."""
    return len(list(postorder_traversal(expr)))


def _term_exponent(term, form):
    """Power of ``form`` in a single multiplicative ``term`` (form itself -> 1,
    ``form**e`` -> e, any other factor -> 0, even one that merely contains ``form``
    like ``sin(form)`` -- exactly as Mathematica treats it)."""
    e = S.Zero
    for f in Mul.make_args(term):
        if f == form:
            e += 1
        elif f.is_Pow and f.base == form:
            e += f.exp
    return e


def _exponent_multiset(expr, form):
    """Exponents of ``form`` in ``expr`` viewed as a rational function.

    Matches Mathematica's ``Exponent``: writing ``expr = num/den`` (via
    ``Together``), the exponent set is ``{e - deg(den) : e over terms of num}``,
    i.e. every numerator-term exponent shifted down by the denominator's degree.
    So ``Exponent[x/(a+b x)^2, x] = 1 - 2 = -1`` and ``Exponent[Sqrt[x]+x, x] = 1``
    -- NOT restricted to polynomials the way a ``PolynomialQ`` guard would be.
    """
    num, den = fraction(together(sympify(expr)))
    ne = [_term_exponent(t, form) for t in Add.make_args(expand(num))]
    de = [_term_exponent(t, form) for t in Add.make_args(expand(den))]
    shift = max(de) if de else S.Zero
    return [e - shift for e in ne] or [S.Zero]


def Exponent(expr, form, h=None):
    """Mathematica ``Exponent[expr, form]`` / ``Exponent[expr, form, h]``.

    Returns the maximum (default) or minimum (``h`` = ``Min``) power of ``form``
    in ``expr``, treating ``expr`` as a rational function -- so it is correct for
    non-polynomials (``Sqrt[x]+x -> 1``, ``1/x+x -> 1``, ``Sin[x] x^2 -> 2``),
    unlike a polynomial-only implementation which wrongly returns 0 for those.

    This is what Rubi's ``Expon[u, x] := Exponent[Together[u], x]`` needs; the
    ``Together`` is already folded in here.
    """
    exps = _exponent_multiset(expr, form)
    is_min = h is not None and (getattr(h, 'name', None) == 'Min' or str(h) == 'Min')
    try:
        return min(exps) if is_min else max(exps)
    except TypeError:
        # Non-comparable (symbolic) exponents -- fall back to 0 rather than crash.
        return S.Zero


def Length(expr):
    """Mathematica Length[expr] — number of elements."""
    if isinstance(expr, (tuple, list, sympy.Tuple)):
        return len(expr)
    return len(expr.args)


def Complex(a, b):
    """Mathematica Complex[re, im] — construct a complex number a + I*b."""
    return a + I * b


def _sort(args):
    """Wolfram ``Sort`` for an argument sequence — canonical ``sort_key`` order."""
    return sorted(args, key=lambda t: t.sort_key())


def Simplify(expr):
    """Mathematica ``Simplify[expr]`` (eager).

    First resolves any unevaluated deferred ``MathematicaExpr`` nodes (a product of
    such nodes drives ``sympy.simplify``'s nc_simplify into unbounded recursion), then
    delegates to ``sympy.simplify``.  A ``Boolean`` (e.g. a ``BinomialDegree`` returning
    ``False`` on a non-binomial) sitting inside an arithmetic node has no numeric value,
    so we return the expression unevaluated rather than crash.
    """
    from sympy_wolfram.objects import MathematicaExpr
    if isinstance(expr, Basic) and expr.has(MathematicaExpr):
        try:
            expr = expr.doit()
        except (AttributeError, TypeError):
            return expr
    try:
        return simplify(expr)
    except (AttributeError, TypeError):
        return expr


def First(expr, d=None):
    """Mathematica ``First[expr]`` — first element (``d`` unused, kept for arity)."""
    if isinstance(expr, (tuple, list, Tuple)):
        return expr[0]
    if isinstance(expr, Symbol):
        return expr
    if expr.is_Add or expr.is_Mul:
        return _sort(expr.args)[0]
    return expr.args[0]


def Rest(expr):
    """Mathematica ``Rest[expr]`` — all elements but the first."""
    if isinstance(expr, (tuple, list, Tuple)):
        return expr[1:]
    if expr.is_Add or expr.is_Mul:
        return expr.func(*_sort(expr.args)[1:])
    return expr.args[1]


def Numerator(u):
    """Mathematica ``Numerator[expr]`` — numerator, recursing through integer powers."""
    u = Simplify(u)
    if isinstance(u, Pow) and isinstance(u.exp, Integer):
        if u.exp > 0:
            return Pow(Numerator(u.base), u.exp)
        if u.exp < 0:
            return Pow(Denominator(u.base), -1 * u.exp)
    elif isinstance(u, Add):
        u = together(u)
    return fraction(u)[0]


def Denominator(var):
    """Mathematica ``Denominator[expr]`` — denominator, recursing through integer powers."""
    var = Simplify(var)
    if isinstance(var, Pow) and isinstance(var.exp, Integer):
        if var.exp > 0:
            return Pow(Denominator(var.base), var.exp)
        if var.exp < 0:
            return Pow(Numerator(var.base), -1 * var.exp)
    elif isinstance(var, Add):
        var = together(var)
    return fraction(var)[1]


class Util_Part(Function):
    """Helper for :func:`Part` — deferred until its index simplifies to an integer."""

    def doit(self):
        i = Simplify(self.args[0])
        if len(self.args) > 2:
            lst = list(self.args[1:])
        else:
            lst = self.args[1]
        if isinstance(i, (int, Integer)):
            if isinstance(lst, (tuple, list)):
                return lst[i - 1]
            if getattr(lst, 'is_Atom', False):
                return lst
            return lst.args[i - 1]
        return self


def Part(lst, i):
    """Mathematica ``Part[expr, i]`` — 1-based part extraction (``i = -1`` = last)."""
    if isinstance(lst, (tuple, list)):
        return Util_Part(i, *lst).doit()
    return Util_Part(i, lst).doit()


def Apart(u, x):
    """Mathematica ``Apart[expr, x]`` — partial-fraction decomposition in ``x``.

    Only rational functions of ``x`` decompose; anything else is returned unchanged
    (matching Mathematica, and guarding SymPy's ``apart`` which raises on non-rational
    input).  The rational-function test is SymPy's own ``is_rational_function`` -- the
    generic equivalent of what Rubi's ``RationalFunctionQ`` computes here.
    """
    u = sympify(u)
    if u.is_rational_function(x):
        return apart(u, x)
    return u


def Not(var):
    """Mathematica Not[expr] — logical negation (tolerant of bool/None/Relational)."""
    if isinstance(var, bool):
        return not var
    elif var is None:
        return None
    elif isinstance(var, Basic) and var.is_Relational:
        var = False
    return not var
