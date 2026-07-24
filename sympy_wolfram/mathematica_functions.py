# -*- coding: utf-8 -*-
"""Standard Wolfram-language function nodes (deferred, SymPy-backed).

These model Mathematica *standard-library* functions (``GCD``, ``Sign``, ``Floor``,
``Together``, ``ProductLog``, ``LeafCount``, …) as :class:`~sympy_wolfram.objects.MathematicaExpr`
subclasses.  They used to live in ``rubi_rules.utils.rubi_utils``, but they are not
Rubi-specific — they belong to the generic Wolfram layer, so they live here and are
re-exported from ``rubi_utils`` for backward compatibility.

Only functions whose evaluation depends *solely* on SymPy (directly, or via the
self-contained eager helpers in :mod:`sympy_wolfram.functions_eager`) live here.
Anything whose evaluation delegates to Rubi's integration utilities
(``First``/``Rest``/``Exponent``/``Apart``/``Part`` — which need ``SumQ``/``Sort``/
``PolynomialQ``/``RationalFunctionQ``/``Util_Part``) stays in ``rubi_rules`` to avoid
a wrong-direction import.

Note: the deferred class and its eager counterpart share the Mathematica name but
live in different modules — the node class ``LeafCount`` is here, the eager function
``LeafCount`` is in :mod:`sympy_wolfram.functions_eager` — exactly as before, when the
class was in ``rubi_utils`` and the function in ``utility_functions``.
"""
import sympy
from sympy import Expr, Integer, S

from sympy_wolfram.objects import List, MathematicaExpr
from sympy_wolfram import functions_eager as _eager


# ---------------------------------------------------------------------------
# Bucket A — evaluation depends solely on SymPy.
# ---------------------------------------------------------------------------

class Coefficient(MathematicaExpr):
    """Mathematica Coefficient[expr, x, n] -> coefficient of x^n in expr."""

    def __new__(cls, expr, x, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, expr, x, n)

    def _evaluate(self, **kwargs):
        expr, x, n = self.args
        if n == S.Zero:
            return expr.coeff(x, 0)
        try:
            return sympy.Poly(expr, x).nth(int(n))
        except Exception:
            return expr.coeff(x, int(n))


class PolynomialQuotient(MathematicaExpr):
    """Mathematica PolynomialQuotient[p, q, x] -> quotient of p/q in x."""

    def __new__(cls, p, q, x):
        return Expr.__new__(cls, p, q, x)

    def _evaluate(self, **kwargs):
        p, q, x = self.args
        try:
            return sympy.quo(p, q, x)
        except sympy.polys.polyerrors.BasePolynomialError:
            # Either p is transcendental in x (e.g. contains log(...x...)) --
            # Mathematica treats such a term as degree 0 in x, so the quotient by a
            # positive-degree q is 0 (remainder is p) -- OR SymPy could not perform
            # the division (PolynomialDivisionFailed in the EX domain, e.g. surd
            # coefficients Mathematica would cancel symbolically). Either way fall
            # back to quotient 0 rather than crashing the whole integration.
            return sympy.Integer(0)


class PolynomialRemainder(MathematicaExpr):
    """Mathematica PolynomialRemainder[p, q, x] -> remainder of p/q in x."""

    def __new__(cls, p, q, x):
        return Expr.__new__(cls, p, q, x)

    def _evaluate(self, **kwargs):
        p, q, x = self.args
        try:
            return sympy.rem(p, q, x)
        except sympy.polys.polyerrors.BasePolynomialError:
            # p is transcendental in x (Mathematica treats it as degree 0, so it is
            # its own remainder mod a positive-degree q) OR SymPy could not perform
            # the division (PolynomialDivisionFailed in the EX domain, e.g. surd
            # coefficients). Either way return p rather than crashing integration.
            return p


class Rule(MathematicaExpr):
    """Mathematica Rule[lhs, rhs] — a (lhs -> rhs) substitution descriptor.

    Used as argument to ReplaceAll. _evaluate returns self because Rule
    is structural rather than a reducible expression.
    """

    def __new__(cls, lhs, rhs):
        return Expr.__new__(cls, lhs, rhs)

    def _evaluate(self, **kwargs):
        return self


class ReplaceAll(MathematicaExpr):
    """Mathematica ReplaceAll[expr, Rule[lhs, rhs]] — substitute lhs -> rhs."""

    def __new__(cls, expr, rule):
        return Expr.__new__(cls, expr, rule)

    def _evaluate(self, **kwargs):
        expr, rule = self.args
        if isinstance(rule, Rule):
            lhs, rhs = rule.args
            return expr.subs(lhs, rhs)
        return expr


class SumWolfram(MathematicaExpr):
    """Mathematica Sum[expr, {i, imin, imax}] — symbolic summation.

    Delegates to sympy.Sum when limits is a List of three elements.
    """

    def __new__(cls, expr, limits):
        return Expr.__new__(cls, expr, limits)

    def _evaluate(self, **kwargs):
        expr, limits = self.args
        if isinstance(limits, List) and len(limits.args) == 3:
            i, imin, imax = limits.args
            return sympy.Sum(expr, (i, imin, imax)).doit()
        return sympy.Sum(expr, limits)


# Trick used to avoid name conflict with SymPy's Sum class:
Sum = SumWolfram


class Numerator(MathematicaExpr):
    """Mathematica Numerator[expr] -> numerator of rational expression."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return sympy.numer(expr)


class Together(MathematicaExpr):
    """Mathematica Together[expr] -> combine fractions."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return sympy.together(expr)


class GCD(MathematicaExpr):
    """Mathematica GCD[a, b, ...] -> greatest common divisor."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        args = self.args
        if len(args) == 0:
            return S.Zero
        if len(args) == 1:
            return args[0]
        result = sympy.gcd(args[0], args[1])
        for a in args[2:]:
            result = sympy.gcd(result, a)
        return result


class Sign(MathematicaExpr):
    """Mathematica Sign[expr] -> sign (-1, 0, or 1)."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return sympy.sign(expr)


class Quotient(MathematicaExpr):
    """Mathematica Quotient[a, b] -> floor(a/b)."""

    def __new__(cls, a, b):
        return Expr.__new__(cls, a, b)

    def _evaluate(self, **kwargs):
        a, b = self.args
        return sympy.floor(a / b)


class EllipticPi(MathematicaExpr):
    """Mathematica EllipticPi[n, m] or EllipticPi[n, phi, m].

    Maps to sympy.elliptic_pi(n, m) or sympy.elliptic_pi(n, phi, m).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        if len(self.args) == 2:
            n, m = self.args
            return sympy.elliptic_pi(n, m)
        elif len(self.args) == 3:
            n, phi, m = self.args
            return sympy.elliptic_pi(n, phi, m)
        return self


class Apply(MathematicaExpr):
    """Mathematica Apply[f, {a, b, ...}] — apply f to list elements."""

    def __new__(cls, f, args):
        return Expr.__new__(cls, f, args)

    def _evaluate(self, **kwargs):
        f, args = self.args
        if hasattr(args, 'args'):
            return f(*args.args)
        return f(*args)


class FullSimplify(MathematicaExpr):
    """Mathematica FullSimplify[expr]."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return sympy.simplify(self.args[0])


class Simplify(MathematicaExpr):
    """Mathematica Simplify[expr]."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return sympy.simplify(self.args[0])


class FunctionExpand(MathematicaExpr):
    """Mathematica FunctionExpand[expr]."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return sympy.expand_func(self.args[0])


class Binomial(MathematicaExpr):
    """Mathematica Binomial[n, k]."""

    def __new__(cls, n, k):
        return Expr.__new__(cls, n, k)

    def _evaluate(self, **kwargs):
        return sympy.binomial(*self.args)


class ProductLog(MathematicaExpr):
    """Mathematica ProductLog[z] or ProductLog[k, z] -> LambertW.

    1-arg: ProductLog(z)    -> LambertW(z)
    2-arg: ProductLog(k, z) -> LambertW(z, k)  [Mathematica arg order reversed vs SymPy]
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        if len(self.args) == 1:
            z = self.args[0]
            return sympy.LambertW(z)
        elif len(self.args) == 2:
            k, z = self.args          # Mathematica: ProductLog[k, z]
            return sympy.LambertW(z, k)  # SymPy:       LambertW(z, k)
        return self


class Floor(MathematicaExpr):
    """Mathematica Floor[x] or Floor[x, a].

    1-arg: Floor(x)    -> floor(x)
    2-arg: Floor(x, a) -> a * floor(x / a)   [rounds to nearest multiple of a]
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        if len(self.args) == 1:
            return sympy.floor(self.args[0])
        elif len(self.args) == 2:
            x, a = self.args
            return a * sympy.floor(x / a)
        return self


class Hypergeometric2F1(MathematicaExpr):
    """Mathematica Hypergeometric2F1[a, b, c, z] -> hyper([a, b], [c], z)."""

    def __new__(cls, a, b, c, z):
        return Expr.__new__(cls, a, b, c, z)

    def _evaluate(self, **kwargs):
        a, b, c, z = self.args
        return sympy.hyper([a, b], [c], z)


# ---------------------------------------------------------------------------
# Bucket B1 — deferred nodes over the self-contained eager helpers.
# ---------------------------------------------------------------------------

class LeafCount(MathematicaExpr):
    """Mathematica LeafCount[expr] — count nodes in expression tree."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return Integer(_eager.LeafCount(self.args[0]))


class Length(MathematicaExpr):
    """Mathematica Length[expr] — number of elements."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return Integer(_eager.Length(self.args[0]))


class Not(MathematicaExpr):
    """Mathematica Not[expr] — logical negation."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return _eager.Not(self.args[0])


class Complex(MathematicaExpr):
    """Mathematica Complex[re, im] — construct complex number re + I*im.

    Like the original in ``rubi_utils``, this is eager: ``__new__`` returns the
    SymPy value directly rather than a deferred node.
    """

    def __new__(cls, re, im):
        return _eager.Complex(re, im)

    def _evaluate(self, **kwargs):
        return self
