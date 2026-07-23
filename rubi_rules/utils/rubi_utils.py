# -*- coding: utf-8 -*-
"""Rubi utility expression wrappers — the DEFERRED half of the utility layer.

Rubi's rules are RuleDelayed (``:>``): a utility call on the right-hand side,
e.g. ``ExpandToSum[v, x]``, must evaluate only WHEN THE RULE FIRES, with the
matched value of ``v`` — never at rule-definition/import time while ``v`` is
still a symbolic wildcard.

To model that, every RUBI utility exists in two forms with the SAME name:

* ``utility_functions.<Name>`` — an EAGER plain Python function that computes
  immediately. This is the real implementation.
* ``rubi_utils.<Name>`` — a DEFERRED ``MathematicaExpr`` subclass. Constructing
  it (``ExpandToSum(v_, x)``) just builds an unevaluated node; its ``_evaluate``
  (invoked by ``.doit()``) delegates to the eager ``utility_functions.<Name>``.

Generated rule modules import the DEFERRED classes (via ``from rubi_utils import *``)
so replacement expressions hold unevaluated nodes. ``_make_replacement_fn``
(rubi_rules/base_objects.py) substitutes the matched wildcard values first and
only then calls ``.doit()`` — so the eager function runs at fire time on concrete
arguments, exactly like Mathematica's ``:>``.

Rule of thumb: a deferred ``_evaluate`` should call its eager counterpart rather
than re-implement the logic (e.g. ``ExpandToSum._evaluate`` must delegate — plain
``sympy.expand`` does NOT collect ``x - I*x`` into ``(1-I)*x``, so it would not
produce the canonical ``a+b*x+c*x**2`` the rule patterns match).

Common Wolfram Mathematica expression classes shared with other packages are
re-exported from ``sympy_wolfram.objects``. Only RUBI-specific
expressions and wrappers around RUBI utility functions are defined locally.

Mathematica originals are documented in:
    Rubi/Rubi/IntegrationUtilityFunctions.m
"""
import sympy
from sympy import (Symbol, Integer, Rational, Add, Mul, Pow, S,
                   expand, simplify, together, gcd, numer, sign,
                   Poly, frac, floor, Expr)

from sympy_matching import RubiConstraint
from sympy_wolfram.objects import (
    CompoundExpression,
    Condition,   # standard Wolfram node; defined in sympy_wolfram, re-exported here
    Head,
    If,
    List,
    MathematicaExpr,
    Module,
    Set,
    With,
    D,
    _condition_holds,
)
from sympy_wolfram.objects import (
    Gamma,
)

# =============================================================================
# Coefficient[expr, x, n] — coefficient of x^n in expr
# =============================================================================

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
            return Poly(expr, x).nth(int(n))
        except Exception:
            return expr.coeff(x, int(n))


# =============================================================================
# Subst[expr, x, v] — substitute x=v in expr
# =============================================================================

class Subst(MathematicaExpr):
    """Rubi Subst[expr, x, v] -> substitute x=v in expr.

    In Rubi, Subst also simplifies constant terms to 0 in antiderivatives,
    but for rule generation we use plain substitution.

    Special case ``Subst[Int[g, x], x, v]``: Rubi integrates the inner ``Int``
    first (``G = ∫g dx``) and only then substitutes ``x -> v`` (giving ``G(v)``).
    Substituting *before* the integral is resolved would capture the ``Int``'s
    bound variable — and ``v`` often reintroduces ``x`` (e.g. ``v = log(x)``),
    which silently produces a wrong answer. So while ``expr`` still holds an
    unevaluated ``Int`` we stay deferred; the DFS integrator reduces that ``Int``
    to an antiderivative and then performs the substitution itself (see
    ``_dfs_reduce_result`` in ``base_objects``).
    """

    def __new__(cls, expr, x, v):
        return Expr.__new__(cls, expr, x, v)

    def _evaluate(self, **kwargs):
        expr, x, v = self.args
        if any(type(a).__name__ == 'Int' for a in expr.atoms(sympy.Function)):
            return self
        return expr.subs(x, v)


# =============================================================================
# Simp[expr] or Simp[expr, x] — simplify expression
# =============================================================================

class Simp(MathematicaExpr):
    """Rubi Simp[expr] or Simp[expr, x] -> simplify expression."""

    def __new__(cls, expr, x=None):
        if x is None:
            return Expr.__new__(cls, expr)
        return Expr.__new__(cls, expr, x)

    def _evaluate(self, **kwargs):
        expr = self.args[0]
        return simplify(expr)


# =============================================================================
# FracPart[u] — sum of non-integer terms
# =============================================================================

class FracPart(MathematicaExpr):
    """Rubi FracPart[u] -> sum of non-integer terms of u.

    For a rational number: returns the fractional part.
    For a sum: returns the sum of non-integer terms.
    """

    def __new__(cls, u, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, n)

    def _evaluate(self, **kwargs):
        u, n = self.args
        if u.is_Rational:
            return frac(n * u)
        if u.is_Add:
            result = S.Zero
            for term in u.args:
                result += FracPart(term, n).doit()
            return result
        return n * u


# =============================================================================
# IntPart[u] — sum of integer terms
# =============================================================================

class IntPart(MathematicaExpr):
    """Rubi IntPart[u] -> sum of integer terms of u.

    For a rational number: returns the integer part (floor).
    For a sum: returns the sum of integer parts.
    """

    def __new__(cls, u, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, n)

    def _evaluate(self, **kwargs):
        u, n = self.args
        if u.is_Rational:
            return floor(n * u)
        if u.is_Add:
            result = S.Zero
            for term in u.args:
                result += IntPart(term, n).doit()
            return result
        return S.Zero


# =============================================================================
# ExpandToSum[u, x] — expand into sum of monomials
# =============================================================================

class ExpandToSum(MathematicaExpr):
    """Rubi ExpandToSum[u, x] or ExpandToSum[u, v, x].

    2-arg: expand u into sum of monomials in x.
    3-arg: ExpandToSum[u, v, x] -> distributes u over expand(v).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        # Delegate to the eager implementation, which collects into canonical
        # a + b*x + c*x**2 form (plain sympy.expand does NOT combine terms like
        # x - I*x, so the result would not match the a+b*x+c*x**2 rule patterns).
        from .utility_functions import ExpandToSum as _ExpandToSum
        return _ExpandToSum(*self.args)


# =============================================================================
# ExpandIntegrand[u, x] or ExpandIntegrand[u, v, x]
# =============================================================================

class ExpandIntegrand(MathematicaExpr):
    """Rubi ExpandIntegrand[u, x] or ExpandIntegrand[u, v, x].

    2-arg: expand u as integrand w.r.t. x.
    3-arg: expand u*v as integrand w.r.t. x.
    """

    def __new__(cls, *args):
        args = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *args)

    def _evaluate(self, **kwargs):
        # Delegate to the EAGER ExpandIntegrand, never re-implement it. A plain
        # sympy.expand here is wrong: for x/(a+b*x)^2 it multiplies the denominator
        # out to x/(a^2+2*a*b*x+b^2*x^2) instead of the partial-fraction expansion
        # 1/(b*(a+b*x)) - a/(b*(a+b*x)^2). The mis-expansion made rule 1.1.1.2#12
        # feed a re-expandable form back into itself (via 9.1#47), an infinite
        # descent with geometrically growing coefficients that the exact-match cycle
        # detector cannot see -- so x/(a+b*x)^2 timed out and x^2/(a+b*x)^2 "solved"
        # to a junk form carrying 1073741824*b**30.
        from .utility_functions import ExpandIntegrand as _ExpandIntegrand
        return _ExpandIntegrand(*self.args)


# =============================================================================
# Coeff[u, x, n] — coefficient (Rubi internal variant)
# =============================================================================

class Coeff(MathematicaExpr):
    """Rubi Coeff[u, x, n] -> coefficient of x^n in u."""

    def __new__(cls, u, x, n):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, x, n)

    def _evaluate(self, **kwargs):
        # Delegate to the eager utility, which handles a symbolic n (via
        # Util_Coefficient) -- `u.coeff(x, int(n))` crashed on symbolic n
        # ('Cannot convert symbols to int').
        from .utility_functions import Coeff as _Coeff
        u, x, n = self.args
        return _Coeff(u, x, n)


# =============================================================================
# Expon[u, x] — degree of polynomial
# =============================================================================

class Expon(MathematicaExpr):
    """Rubi Expon[u, x] or Expon[u, x, Min/Max] -> degree of u in x.

    2-arg: maximum (leading) degree.
    3-arg with Symbol('Min'): minimum non-zero degree.
    3-arg with Symbol('Max'): maximum degree (same as 2-arg).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        args = self.args
        u, x = args[0], args[1]
        order_func = args[2] if len(args) >= 3 else None
        try:
            p = Poly(u, x)
            monoms = [m[0] for m in p.monoms()]
            if order_func is not None and str(order_func) == 'Min':
                return Integer(min(monoms))
            return Integer(max(monoms))
        except Exception:
            return S.Zero


# =============================================================================
# Simplify — wraps sympy.simplify
# =============================================================================

class RubiSimplify(MathematicaExpr):
    """Rubi Simplify[expr] -> simplify expression."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return simplify(expr)


# =============================================================================
# PolynomialQuotient[p, q, x] — polynomial division quotient
# =============================================================================

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


# =============================================================================
# PolynomialRemainder[p, q, x] — polynomial division remainder
# =============================================================================

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


# =============================================================================
# CannotIntegrate[expr, x] — integration failure sentinel
# =============================================================================

class CannotIntegrate(MathematicaExpr):
    """Mathematica CannotIntegrate[expr, x] — integration failure sentinel.

    Returned unevaluated when no Rubi rule applies to the integrand.
    _evaluate returns self so the sentinel propagates unchanged through
    any further .doit() calls.
    """

    def __new__(cls, expr, x):
        return Expr.__new__(cls, expr, x)

    def _evaluate(self, **kwargs):
        # Terminal sentinel: stays unevaluated.
        return self


# =============================================================================
# Condition[expr, test] — conditional expression
# =============================================================================

# =============================================================================
# Rule[lhs, rhs] — Mathematica substitution rule (lhs -> rhs)
# =============================================================================

class Rule(MathematicaExpr):
    """Mathematica Rule[lhs, rhs] — a (lhs -> rhs) substitution descriptor.

    Used as argument to ReplaceAll. _evaluate returns self because Rule
    is structural rather than a reducible expression.
    """

    def __new__(cls, lhs, rhs):
        return Expr.__new__(cls, lhs, rhs)

    def _evaluate(self, **kwargs):
        return self


# =============================================================================
# ReplaceAll[expr, Rule[lhs, rhs]] — apply substitution rule
# =============================================================================

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


# =============================================================================
# Unintegrable[expr, x] — integration failure sentinel
# =============================================================================

class Unintegrable(MathematicaExpr):
    """Rubi Unintegrable[expr, x] — marks that no rule could integrate expr.

    Different from CannotIntegrate; used for trig/special-function integrands
    that Rubi declines to reduce. Stays unevaluated.
    """

    def __new__(cls, expr, x):
        return Expr.__new__(cls, expr, x)

    def _evaluate(self, **kwargs):
        return self


# =============================================================================
# IntHide[u, x] — integrate with step display suppressed
# =============================================================================

class IntHide(MathematicaExpr):
    """Rubi ``IntHide[u, x] := Block[{$ShowSteps=False}, Int[u, x]]``.

    IntHide actually integrates ``u`` (only the step display is suppressed). Many
    rules bind a local to ``IntHide[...]`` and then use its antiderivative (3.1.4,
    the inverse-hyperbolic families, …); leaving it unevaluated breaks all of them.
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)

    def _evaluate(self, **kwargs):
        u, x = self.args
        from rubi_rules.base_objects import rubi_integrate, Int
        result = rubi_integrate(u, x)
        # If integration didn't finish, fall back to the passive Int so the caller
        # can proceed (and never leave an unevaluated IntHide behind).
        if result.has(Int) or 'CannotIntegrate' in str(result) or 'Unintegrable' in str(result):
            return Int(u, x)
        return result


# =============================================================================
# Sum[expr, limits] — symbolic summation
# =============================================================================

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

# =============================================================================
# Numerator[expr] — numerator of a rational expression
# =============================================================================

class Numerator(MathematicaExpr):
    """Mathematica Numerator[expr] -> numerator of rational expression."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return numer(expr)


# =============================================================================
# Together[expr] — combine fractions over a common denominator
# =============================================================================

class Together(MathematicaExpr):
    """Mathematica Together[expr] -> combine fractions."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return together(expr)


class FunctionOfExponential(MathematicaExpr):
    """Deferred FunctionOfExponential[u, x] -- delegates to the eager utility.

    Returns the base exponential ``E^(a+b x)`` that ``u`` is a function of.
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, sympy.sympify(u), sympy.sympify(x))

    def _evaluate(self, **kwargs):
        from .utility_functions import FunctionOfExponential as _f
        return _f(*self.args)


class FunctionOfExponentialFunction(MathematicaExpr):
    """Deferred FunctionOfExponentialFunction[u, x] -- delegates to the eager utility.

    Rewrites ``u`` as a function of a new variable standing in for the exponential.
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, sympy.sympify(u), sympy.sympify(x))

    def _evaluate(self, **kwargs):
        from .utility_functions import FunctionOfExponentialFunction as _f
        return _f(*self.args)


# =============================================================================
# GCD[a, b, ...] — greatest common divisor
# =============================================================================

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
        result = gcd(args[0], args[1])
        for a in args[2:]:
            result = gcd(result, a)
        return result


# =============================================================================
# Sign[expr] — sign of expression (-1, 0, or 1)
# =============================================================================

class Sign(MathematicaExpr):
    """Mathematica Sign[expr] -> sign (-1, 0, or 1)."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self, **kwargs):
        expr, = self.args
        return sign(expr)


# =============================================================================
# Quotient[a, b] — integer quotient floor(a/b)
# =============================================================================

class Quotient(MathematicaExpr):
    """Mathematica Quotient[a, b] -> floor(a/b)."""

    def __new__(cls, a, b):
        return Expr.__new__(cls, a, b)

    def _evaluate(self, **kwargs):
        a, b = self.args
        return floor(a / b)


# =============================================================================
# EllipticPi — elliptic integral of the third kind
# =============================================================================

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


# =============================================================================
# PolynomialDivide[u, v, x] — quotient + remainder/v as one expression
# =============================================================================

class PolynomialDivide(MathematicaExpr):
    """Rubi PolynomialDivide[u, v, x] = quo(u,v,x) + rem(u,v,x)/v."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        args = self.args
        if len(args) == 3:
            u, v, x = args
        elif len(args) == 4:
            u, v, w, x = args
            u = u.subs(w, x)
            v = v.subs(w, x)
        else:
            return self
        try:
            q = sympy.quo(u, v, x)
            r = sympy.rem(u, v, x)
            return together(q + r / v)
        except Exception:
            return self


# =============================================================================
# NormalizePseudoBinomial[u, x] — rewrite pseudo-binomial as a+b*(c+d*x)^n
# =============================================================================

class NormalizePseudoBinomial(MathematicaExpr):
    """Rubi NormalizePseudoBinomial[u, x] — rewrite as a + b*(c+d*x)^n.

    Falls back to u unchanged if the form cannot be detected.
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)

    def _evaluate(self, **kwargs):
        u, x = self.args
        try:
            p = Poly(u, x)
            n = p.degree()
            if n <= 2:
                return u
            coeffs = p.all_coeffs()
            d = sympy.root(coeffs[0], n)
            c_coeff = coeffs[1] / (n * d**(n - 1)) if n >= 2 else S.Zero
            a = expand(u - (c_coeff + d * x)**n)
            if a.is_number or (not a.has(x) and a != S.Zero):
                return a + (c_coeff + d * x)**n
        except Exception:
            pass
        return u


# =============================================================================
# SubstFor[v, u, x] or SubstFor[w, v, u, x] — substitution in integrand
# =============================================================================

class SubstFor(MathematicaExpr):
    """Rubi SubstFor[v, u, x] or SubstFor[w, v, u, x].

    3-arg SubstFor[v, u, x]: returns u with v replaced by x.
    4-arg SubstFor[w, v, u, x]: returns simplify(w * SubstFor[v, u, x]).

    Mathematica originals (IntegrationUtilityFunctions.m):
        SubstFor[v_, u_, x_] := Subst[u, v, x]
        SubstFor[w_, v_, u_, x_] := SimplifyIntegrand[w * SubstFor[v, u, x], x]
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        # Delegate to the eager implementation. The naive `u.subs(v, x)` used before
        # is wrong when v has a free factor: SubstFor[b*x, x, x] must be x/b (the
        # eager one factors it out), not x — the missing 1/b silently multiplied
        # many symbolic-coefficient results by the linear coefficient.
        from .utility_functions import SubstFor as _SubstFor
        return _SubstFor(*self.args)


# Backward-compatible alias (user listed 'SubstrFor'; Rubi calls it 'SubstFor')
SubstrFor = SubstFor


# =============================================================================
# Re-export all utility functions from utility_functions.py
#
# rubi_utils.py is NOT a generated file, so it can import from utility_functions.
# Generated rule files (rubi_rules/rules/*.py) import from rubi_utils, not from
# utility_functions, keeping the generated code clean.
# =============================================================================


# =============================================================================
# Additional RUBI utility wrappers for generated code
# These wrap utility_functions.* implementations for use in generated rules
# =============================================================================

class Dist(MathematicaExpr):
    """Rubi Dist[u, v, x] — distribute u over v.

    Rubi also uses a 2-arg ``Dist[u, v]`` (e.g. 3.1.4#3, several inverse-hyperbolic
    rules) with no integration variable: it just distributes ``u`` over the terms of
    ``v`` (there is no free-of-x normalisation to do without ``x``).
    """
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        if len(self.args) == 2:
            u, v = self.args
            if getattr(v, 'is_Add', False):
                return sympy.Add(*[u * t for t in v.args])
            return u * v
        from .utility_functions import Dist as _Dist
        return _Dist(*self.args)


class Star(MathematicaExpr):
    """Rubi Star[u, v] — display-friendly product; u distributed over terms of v.

    Rubi co-opts Wolfram's meaning-free ``\\[Star]`` infix operator as a product
    that displays as ``u*v`` and evaluates by distributing ``u`` over the terms of
    ``v`` (see the module docstring on deferred vs eager nodes). Delegates to the
    eager :func:`utility_functions.Star`.

    In the source rules this arrives as an infix ``u \\[Star] Int[...]``; the
    code generator reconstructs it into ``Star(u, v)`` (see
    ``rubi_rules/codegen/generate.py``), so the coefficient/integral structure is
    preserved for step reporting and collapses to ``u*v`` on ``doit()``.
    """
    def __new__(cls, u, v):
        return Expr.__new__(cls, sympy.sympify(u), sympy.sympify(v))
    def _evaluate(self, **kwargs):
        from .utility_functions import Star as _Star
        return _Star(*self.args)


class WFApply(MathematicaExpr):
    """Apply a wildcard-bound function head to arguments — Rubi's ``F[args]``.

    A Rubi pattern ``F_[v_]`` binds ``F`` to a function HEAD (any function); the
    replacement then re-applies that head, e.g. ``F[a+b*x]``. A function class such
    as ``sin`` is not a substitutable SymPy object, so the matched head arrives as
    a :class:`~sympy_matching.wild.HeadRef` wrapper; this node applies it on
    ``doit``: ``HeadRef(sin)`` + ``(y,)`` -> ``sin(y)``.

    For robustness it also accepts a whole matched application in the first slot
    (using its ``.func``), so ``WFApply(sin(x), y)`` -> ``sin(y)`` as well.
    """
    def __new__(cls, head, *args):
        safe = [sympy.sympify(head)] + [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        head, *args = self.args
        func = getattr(head, 'func_class', None)          # HeadRef -> the function
        if func is None and getattr(head, 'args', None):  # a matched application
            func = getattr(head, 'func', None)
        if func is None:
            return None  # head not resolved yet -> stay unevaluated (see base doit)
        return func(*args)


class WFDeriv(MathematicaExpr):
    """The n-th derivative of a wildcard-bound function — Rubi's ``Derivative[n][f][x]``.

    The companion of :class:`WFApply` for the derivative rules: a pattern
    ``Derivative[n_][f_][x_]`` binds ``f`` to a function HEAD (arriving as a
    :class:`~sympy_matching.wild.HeadRef`) and ``n`` to the order, and the
    replacement rebuilds e.g. ``Derivative[n-1][f][x]``. On ``doit`` this becomes
    ``Derivative(f(x), (x, order))`` -- or just ``f(x)`` when the order is 0.
    """
    def __new__(cls, head, var, order):
        return Expr.__new__(cls, sympy.sympify(head), sympy.sympify(var),
                            sympy.sympify(order))

    def _evaluate(self, **kwargs):
        head, var, order = self.args
        func = getattr(head, 'func_class', None)
        if func is None and getattr(head, 'args', None):
            func = getattr(head, 'func', None)
        if func is None:
            return None  # head not resolved yet -> stay unevaluated (see base doit)
        applied = func(var)
        if order == 0:
            return applied
        return sympy.Derivative(applied, (var, order))


class SimplifyIntegrand(MathematicaExpr):
    """Rubi SimplifyIntegrand[u, x] — simplify integrand."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import SimplifyIntegrand as _SimplifyIntegrand
        return _SimplifyIntegrand(*self.args)


class FreeFactors(MathematicaExpr):
    """Rubi FreeFactors[u, x] — product of factors free of x."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self, **kwargs):
        from .utility_functions import FreeFactors as _FreeFactors
        return _FreeFactors(*self.args)


class NonfreeFactors(MathematicaExpr):
    """Rubi NonfreeFactors[u, x] — product of factors not free of x."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self, **kwargs):
        from .utility_functions import NonfreeFactors as _NonfreeFactors
        return _NonfreeFactors(*self.args)


class ActivateTrig(MathematicaExpr):
    """Rubi ActivateTrig[u] — activate trig expressions."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self, **kwargs):
        from .utility_functions import ActivateTrig as _ActivateTrig
        return _ActivateTrig(self.args[0])


class DeactivateTrig(MathematicaExpr):
    """Rubi DeactivateTrig[u, x] — deactivate trig expressions."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import DeactivateTrig as _DeactivateTrig
        return _DeactivateTrig(*self.args)


class ExpandTrig(MathematicaExpr):
    """Rubi ExpandTrig[u, x] — expand trig expressions."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import ExpandTrig as _ExpandTrig
        return _ExpandTrig(*self.args)


class ExpandTrigReduce(MathematicaExpr):
    """Rubi ExpandTrigReduce[u, x] — expand and reduce trig."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import ExpandTrigReduce as _ExpandTrigReduce
        return _ExpandTrigReduce(*self.args)


class DerivativeDivides(MathematicaExpr):
    """Rubi DerivativeDivides[u, v, x] — check derivative divides."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import DerivativeDivides as _DerivativeDivides
        return _DerivativeDivides(*self.args)


class BinomialDegree(MathematicaExpr):
    """Rubi BinomialDegree[u, x] — degree of binomial."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self, **kwargs):
        from .utility_functions import BinomialDegree as _BinomialDegree
        return _BinomialDegree(*self.args)


class TrinomialDegree(MathematicaExpr):
    """Rubi TrinomialDegree[u, x] — degree of trinomial."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self, **kwargs):
        from .utility_functions import TrinomialDegree as _TrinomialDegree
        return _TrinomialDegree(*self.args)


class LeafCount(MathematicaExpr):
    """Mathematica LeafCount[expr] — count nodes in expression tree."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        from .utility_functions import LeafCount as _LeafCount
        return Integer(_LeafCount(self.args[0]))


class Part(MathematicaExpr):
    """Mathematica Part[expr, n] — extract nth part."""
    def __new__(cls, expr, *indices):
        return Expr.__new__(cls, expr, *indices)
    def _evaluate(self, **kwargs):
        from .utility_functions import Part as _Part
        return _Part(*self.args)


class First(MathematicaExpr):
    """Mathematica First[expr] — first element."""
    def __new__(cls, expr, d=None):
        if d is None:
            return Expr.__new__(cls, expr)
        return Expr.__new__(cls, expr, d)
    def _evaluate(self, **kwargs):
        from .utility_functions import First as _First
        return _First(*self.args)


class Rest(MathematicaExpr):
    """Mathematica Rest[expr] — all but first element."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        from .utility_functions import Rest as _Rest
        return _Rest(self.args[0])


class Length(MathematicaExpr):
    """Mathematica Length[expr] — number of elements."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        from .utility_functions import Length as _Length
        return Integer(_Length(self.args[0]))


class Complex(MathematicaExpr):
    """Mathematica Complex[re, im] — construct complex number."""
    def __new__(cls, re, im):
        from .utility_functions import Complex as _Complex
        return _Complex(re, im)
    def _evaluate(self, **kwargs):
        pass


class Numer(MathematicaExpr):
    """Rubi Numer[u] — numerator (simple form)."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self, **kwargs):
        from .utility_functions import Numer as _Numer
        return _Numer(self.args[0])


class Denom(MathematicaExpr):
    """Rubi Denom[u] — denominator (simple form)."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self, **kwargs):
        from .utility_functions import Denom as _Denom
        return _Denom(self.args[0])


class Apply(MathematicaExpr):
    """Mathematica Apply[f, {a, b, ...}] — apply f to list elements."""
    def __new__(cls, f, args):
        return Expr.__new__(cls, f, args)
    def _evaluate(self, **kwargs):
        f, args = self.args
        if hasattr(args, 'args'):
            return f(*args.args)
        return f(*args)


class Not(MathematicaExpr):
    """Mathematica Not[expr] — logical negation."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        from .utility_functions import Not as _Not
        return _Not(self.args[0])




# =============================================================================
# Additional Rubi utility function wrappers
# =============================================================================

class NormalizePowerOfLinear(MathematicaExpr):
    """Rubi NormalizePowerOfLinear[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import NormalizePowerOfLinear as _NormalizePowerOfLinear
        return _NormalizePowerOfLinear(*self.args)


class NormalizeIntegrand(MathematicaExpr):
    """Rubi NormalizeIntegrand[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import NormalizeIntegrand as _NormalizeIntegrand
        return _NormalizeIntegrand(*self.args)


class Exponent(MathematicaExpr):
    """Mathematica Exponent[expr, form]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import Exponent as _Exponent
        return _Exponent(*self.args)


class FullSimplify(MathematicaExpr):
    """Mathematica FullSimplify[expr]."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        return simplify(self.args[0])


class Simplify(MathematicaExpr):
    """Mathematica Simplify[expr]."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        return simplify(self.args[0])


class FunctionExpand(MathematicaExpr):
    """Mathematica FunctionExpand[expr]."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self, **kwargs):
        from sympy import expand_func
        return expand_func(self.args[0])


class ExpandLinearProduct(MathematicaExpr):
    """Rubi ExpandLinearProduct[v, u, a, b, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import ExpandLinearProduct as _ExpandLinearProduct
        return _ExpandLinearProduct(*self.args)


class Divides(MathematicaExpr):
    """Rubi Divides[u, v, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import Divides as _Divides
        return _Divides(*self.args)


class RationalFunctionExpand(MathematicaExpr):
    """Rubi RationalFunctionExpand[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import RationalFunctionExpand as _RationalFunctionExpand
        return _RationalFunctionExpand(*self.args)


class PowerVariableExpn(MathematicaExpr):
    """Rubi PowerVariableExpn[u, m, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import PowerVariableExpn as _PowerVariableExpn
        return _PowerVariableExpn(*self.args)


class FunctionOfLinear(MathematicaExpr):
    """Rubi FunctionOfLinear[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import FunctionOfLinear as _FunctionOfLinear
        return _FunctionOfLinear(*self.args)


class SplitProduct(MathematicaExpr):
    """Rubi SplitProduct[f, u]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import SplitProduct as _SplitProduct
        return _SplitProduct(*self.args)


class PolyGCD(MathematicaExpr):
    """Rubi PolyGCD[a, b, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import PolyGCD as _PolyGCD
        return _PolyGCD(*self.args)


class GeneralizedTrinomialDegree(MathematicaExpr):
    """Rubi GeneralizedTrinomialDegree[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import GeneralizedTrinomialDegree as _GeneralizedTrinomialDegree
        return _GeneralizedTrinomialDegree(*self.args)


class ExpandTrigToExp(MathematicaExpr):
    """Rubi ExpandTrigToExp[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import ExpandTrigToExp as _ExpandTrigToExp
        return _ExpandTrigToExp(*self.args)


class Binomial(MathematicaExpr):
    """Mathematica Binomial[n, k]."""
    def __new__(cls, n, k):
        return Expr.__new__(cls, n, k)
    def _evaluate(self, **kwargs):
        from sympy import binomial
        return binomial(*self.args)


# =============================================================================
# ProductLog[z] or ProductLog[k, z] — Lambert W function
# Mathematica: ProductLog[k, z] where k=branch index, z=value
# SymPy:       LambertW(z, k)   where z=value, k=branch  (args REVERSED)
# =============================================================================

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


# =============================================================================
# Floor[x] or Floor[x, a] — round toward -inf / to nearest multiple of a
# =============================================================================

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
            return floor(self.args[0])
        elif len(self.args) == 2:
            x, a = self.args
            return a * floor(x / a)
        return self


# =============================================================================
# Hypergeometric2F1[a, b, c, z] — Gauss hypergeometric function
# SymPy uses hyper([a, b], [c], z) — numerator params packed into a list
# =============================================================================

class Hypergeometric2F1(MathematicaExpr):
    """Mathematica Hypergeometric2F1[a, b, c, z] -> hyper([a, b], [c], z)."""

    def __new__(cls, a, b, c, z):
        return Expr.__new__(cls, a, b, c, z)

    def _evaluate(self, **kwargs):
        a, b, c, z = self.args
        from sympy.functions.special.hyper import hyper
        return hyper([a, b], [c], z)


# =============================================================================
# Lazy MathematicaExpr wrappers for utility_functions plain callables
# =============================================================================
# Additional MathematicaExpr wrappers for functions used in generated rules.
# These were previously missing explicit class definitions.
# =============================================================================

class MinimumMonomialExponent(MathematicaExpr):
    """Rubi MinimumMonomialExponent[u, x] — minimum monomial exponent."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import MinimumMonomialExponent as _f
        return _f(*self.args)


class Distrib(MathematicaExpr):
    """Rubi Distrib[u, v] — distribute u over v."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import Distrib as _f
        return _f(*self.args)


class Apart(MathematicaExpr):
    """Rubi Apart[u, x] — partial fraction decomposition."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import Apart as _f
        return _f(*self.args)


class ExpandExpression(MathematicaExpr):
    """Rubi ExpandExpression[u, x] — expand expression."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import ExpandExpression as _f
        return _f(*self.args)


class FunctionOfTrig(MathematicaExpr):
    """Rubi FunctionOfTrig[u, ...] — function of trig."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import FunctionOfTrig as _f
        return _f(*self.args)


class PolynomialInSubst(MathematicaExpr):
    """Rubi PolynomialInSubst[u, v, x] — polynomial in substitution."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import PolynomialInSubst as _f
        return _f(*self.args)


class QuotientOfLinearsParts(MathematicaExpr):
    """Rubi QuotientOfLinearsParts[u, x] — parts of quotient of linears."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import QuotientOfLinearsParts as _f
        return _f(*self.args)


class SubstForFractionalPowerOfLinear(MathematicaExpr):
    """Rubi SubstForFractionalPowerOfLinear[u, x] — substitution for fractional power."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import SubstForFractionalPowerOfLinear as _f
        return _f(*self.args)


class TrigSimplify(MathematicaExpr):
    """Rubi TrigSimplify[u] — simplify trig expression."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import TrigSimplify as _f
        return _f(*self.args)


class RationalFunctionExponents(MathematicaExpr):
    """Rubi RationalFunctionExponents[u, x] — exponents of rational function."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import RationalFunctionExponents as _f
        return _f(*self.args)


class Denominator(MathematicaExpr):
    """Rubi Denominator[expr] — denominator of expression (lazy, not eagerly evaluated)."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self, **kwargs):
        from .utility_functions import Denominator as _f
        return _f(*self.args)


# =============================================================================
# Gamma[z] or Gamma[a, z] — gamma and upper incomplete gamma function
# =============================================================================
# Mathematica: Gamma[z] -> gamma(z), Gamma[a, z] -> uppergamma(a, z)
# Needs a wrapper because sympy.gamma only takes 1 arg.

class Gamma(MathematicaExpr):
    """Mathematica Gamma[z] or Gamma[a, z] -> sympy.gamma / sympy.uppergamma."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self, **kwargs):
        if len(self.args) == 1:
            return sympy.gamma(self.args[0])
        else:
            return sympy.uppergamma(self.args[0], self.args[1])
