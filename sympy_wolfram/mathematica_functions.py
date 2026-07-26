# -*- coding: utf-8 -*-
"""Standard Wolfram-language function nodes (deferred, SymPy-backed).

These model Mathematica *standard-library* functions (``GCD``, ``Sign``, ``Floor``,
``Together``, ``ProductLog``, ``LeafCount``, …) as :class:`~sympy_wolfram.objects.MathematicaExpr`
subclasses.  They used to live in ``rubi_rules.utils.rubi_utils``, but they are not
Rubi-specific — they belong to the generic Wolfram layer, so they live here and are
re-exported from ``rubi_utils`` for backward compatibility.

Only functions whose evaluation depends *solely* on SymPy (directly, or via the
self-contained eager helpers in :mod:`sympy_wolfram.functions_eager`) live here.
That includes ``First``/``Rest``/``Exponent``/``Apart``/``Part``: their seemingly
Rubi-coupled bodies (``SumQ``/``Sort``/``PolynomialQ``/``RationalFunctionQ``/
``Util_Part``) turned out to be generic SymPy operations, so those deferred classes
live HERE too, not in ``rubi_rules``.

Note: the deferred class keeps the bare Mathematica name while its eager counterpart
is prefixed with ``eager_`` and lives in a different module — the node class
``LeafCount`` is here, the eager function ``eager_LeafCount`` is in
:mod:`sympy_wolfram.functions_eager`.
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
        # Delegate to the eager helper (see functions_eager.PolynomialQuotient), which
        # handles the RATIONAL-p case Rubi relies on (Pq*(c x)^m with m<0). The old inline
        # sympy.quo(...) here returned 0 on such inputs -- e.g.
        # PolynomialQuotient[(A+Bx)/x^2, a+b x^2] -> 0 -- silently zeroing whole integrals.
        from sympy_wolfram.functions_eager import eager_PolynomialQuotient
        return eager_PolynomialQuotient(*self.args)


class PolynomialRemainder(MathematicaExpr):
    """Mathematica PolynomialRemainder[p, q, x] -> remainder of p/q in x."""

    def __new__(cls, p, q, x):
        return Expr.__new__(cls, p, q, x)

    def _evaluate(self, **kwargs):
        # Delegate to the eager helper (see functions_eager.PolynomialRemainder), which
        # reduces a RATIONAL p modulo q; the old inline sympy.rem(...) returned the whole
        # input p on such Rubi inputs, breaking the rules that use the remainder's coeffs.
        from sympy_wolfram.functions_eager import eager_PolynomialRemainder
        return eager_PolynomialRemainder(*self.args)


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
            # Mathematica ``Sum`` iterates ``i`` in unit steps from ``imin``, stopping
            # at the largest value <= ``imax``. So a non-integer bound truncates toward
            # the interior (imax -> floor, imin -> ceiling). The binomial-Pq rules
            # (e.g. r_1_1_2_12) build limits like (q-r)/n = 5/4, and sympy.Sum leaves a
            # fractional-bound sum UNEVALUATED -- a symbolic Sum that then drives
            # simplify() into unbounded recursion (crashed (x^4+1)/(x^8+1)). Floor/ceil
            # the concrete bounds so the sum actually expands to its finite terms.
            if getattr(imax, "is_number", False) and imax.is_integer is False:
                imax = sympy.floor(imax)
            if getattr(imin, "is_number", False) and imin.is_integer is False:
                imin = sympy.ceiling(imin)
            return sympy.Sum(expr, (i, imin, imax)).doit()
        return sympy.Sum(expr, limits)


# Trick used to avoid name conflict with SymPy's Sum class:
Sum = SumWolfram


class Numerator(MathematicaExpr):
    """Mathematica Numerator[expr] -> numerator of rational expression.

    Delegates to the eager helper (which recurses through integer powers, pairing
    with :class:`Denominator`) rather than a bare ``sympy.numer``.
    """

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return _eager.eager_Numerator(self.args[0])


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
        return Integer(_eager.eager_LeafCount(self.args[0]))


class Length(MathematicaExpr):
    """Mathematica Length[expr] — number of elements."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return Integer(_eager.eager_Length(self.args[0]))


class Not(MathematicaExpr):
    """Mathematica Not[expr] — logical negation."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return _eager.eager_Not(self.args[0])


class Complex(MathematicaExpr):
    """Mathematica Complex[re, im] — construct complex number re + I*im.

    Like the original in ``rubi_utils``, this is eager: ``__new__`` returns the
    SymPy value directly rather than a deferred node.
    """

    def __new__(cls, re, im):
        return _eager.eager_Complex(re, im)

    def _evaluate(self, **kwargs):
        return self


class Denominator(MathematicaExpr):
    """Mathematica Denominator[expr] — denominator of a rational expression."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        return _eager.eager_Denominator(*self.args)


class First(MathematicaExpr):
    """Mathematica First[expr] — first element."""

    def __new__(cls, expr, d=None):
        if d is None:
            return Expr.__new__(cls, expr)
        return Expr.__new__(cls, expr, d)

    def _evaluate(self, **kwargs):
        return _eager.eager_First(*self.args)


class Rest(MathematicaExpr):
    """Mathematica Rest[expr] — all elements but the first."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        return _eager.eager_Rest(self.args[0])


class Part(MathematicaExpr):
    """Mathematica Part[expr, n] — extract the n-th part (1-based)."""

    def __new__(cls, expr, *indices):
        return Expr.__new__(cls, expr, *indices)

    def _evaluate(self, **kwargs):
        return _eager.eager_Part(*self.args)


class Exponent(MathematicaExpr):
    """Mathematica Exponent[expr, form] / Exponent[expr, form, h]."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        return _eager.eager_Exponent(*self.args)


class Apart(MathematicaExpr):
    """Mathematica Apart[expr, x] — partial-fraction decomposition in x."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        return _eager.eager_Apart(*self.args)
