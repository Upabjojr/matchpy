# -*- coding: utf-8 -*-
"""Rubi utility functions as SymPy Expr subclasses.

Each Rubi internal function is implemented as a SymPy expression class:
- The constructor (__new__) registers parameters as class fields via args.
- The evaluation logic lives in _evaluate().
- doit() triggers evaluation by calling _evaluate().

This design allows these objects to live unevaluated in SymPy expression
trees (for pattern matching) and be evaluated on demand via .doit().

Mathematica originals are documented in:
    Rubi/Rubi/IntegrationUtilityFunctions.m
"""
import sympy
from sympy import (Symbol, Integer, Rational, Add, Mul, Pow, S,
                   expand, simplify, together, gcd, numer, sign,
                   Poly, degree, frac, floor, Expr)
from sympy.core.function import Application

from sympy_objects import RubiConstraint


# =============================================================================
# Base class for Rubi utility expressions
# =============================================================================

class RubiFunction(Expr):
    """Base class for Rubi utility function expressions.

    Subclasses define _evaluate() with the actual computation.
    Calling .doit() triggers evaluation.
    """

    def doit(self, **kwargs):
        """Evaluate this Rubi function."""
        # Recursively doit on args first if deep=True (default)
        deep = kwargs.get('deep', True)
        if deep:
            new_args = [a.doit(**kwargs) if hasattr(a, 'doit') else a for a in self.args]
            instance = Expr.__new__(self.__class__, *new_args)
        else:
            instance = self
        return instance._evaluate()

    def _evaluate(self):
        """Override in subclasses with the actual computation."""
        raise NotImplementedError


# =============================================================================
# Coefficient[expr, x, n] — coefficient of x^n in expr
# =============================================================================

class Coefficient(RubiFunction):
    """Mathematica Coefficient[expr, x, n] -> coefficient of x^n in expr."""

    def __new__(cls, expr, x, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, expr, x, n)

    def _evaluate(self):
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

class Subst(RubiFunction):
    """Rubi Subst[expr, x, v] -> substitute x=v in expr.

    In Rubi, Subst also simplifies constant terms to 0 in antiderivatives,
    but for rule generation we use plain substitution.
    """

    def __new__(cls, expr, x, v):
        return Expr.__new__(cls, expr, x, v)

    def _evaluate(self):
        expr, x, v = self.args
        return expr.subs(x, v)


# =============================================================================
# Simp[expr] or Simp[expr, x] — simplify expression
# =============================================================================

class Simp(RubiFunction):
    """Rubi Simp[expr] or Simp[expr, x] -> simplify expression."""

    def __new__(cls, expr, x=None):
        if x is None:
            return Expr.__new__(cls, expr)
        return Expr.__new__(cls, expr, x)

    def _evaluate(self):
        expr = self.args[0]
        return simplify(expr)


# =============================================================================
# FracPart[u] — sum of non-integer terms
# =============================================================================

class FracPart(RubiFunction):
    """Rubi FracPart[u] -> sum of non-integer terms of u.

    For a rational number: returns the fractional part.
    For a sum: returns the sum of non-integer terms.
    """

    def __new__(cls, u, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, n)

    def _evaluate(self):
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

class IntPart(RubiFunction):
    """Rubi IntPart[u] -> sum of integer terms of u.

    For a rational number: returns the integer part (floor).
    For a sum: returns the sum of integer parts.
    """

    def __new__(cls, u, n=S.One):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, n)

    def _evaluate(self):
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

class ExpandToSum(RubiFunction):
    """Rubi ExpandToSum[u, x] or ExpandToSum[u, v, x].

    2-arg: expand u into sum of monomials in x.
    3-arg: ExpandToSum[u, v, x] -> distributes u over expand(v).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
        if len(self.args) == 2:
            u, x = self.args
            return expand(u)
        # 3-arg form: ExpandToSum[u, v, x]
        u, v, x = self.args[0], self.args[1], self.args[2]
        w = expand(v)
        if isinstance(w, Add):
            return Add(*[expand(u * t) for t in w.args])
        return expand(u * w)


# =============================================================================
# ExpandIntegrand[u, x] or ExpandIntegrand[u, v, x]
# =============================================================================

class ExpandIntegrand(RubiFunction):
    """Rubi ExpandIntegrand[u, x] or ExpandIntegrand[u, v, x].

    2-arg: expand u as integrand w.r.t. x.
    3-arg: expand u*v as integrand w.r.t. x.
    """

    def __new__(cls, *args):
        args = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *args)

    def _evaluate(self):
        args = self.args
        if len(args) == 2:
            u, x = args
            return expand(u)
        else:
            u, v, x = args
            return expand(u * v)


# =============================================================================
# Coeff[u, x, n] — coefficient (Rubi internal variant)
# =============================================================================

class Coeff(RubiFunction):
    """Rubi Coeff[u, x, n] -> coefficient of x^n in u."""

    def __new__(cls, u, x, n):
        n = sympy.sympify(n)
        return Expr.__new__(cls, u, x, n)

    def _evaluate(self):
        u, x, n = self.args
        return u.coeff(x, int(n))


# =============================================================================
# Expon[u, x] — degree of polynomial
# =============================================================================

class Expon(RubiFunction):
    """Rubi Expon[u, x] or Expon[u, x, Min/Max] -> degree of u in x.

    2-arg: maximum (leading) degree.
    3-arg with Symbol('Min'): minimum non-zero degree.
    3-arg with Symbol('Max'): maximum degree (same as 2-arg).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class RubiSimplify(RubiFunction):
    """Rubi Simplify[expr] -> simplify expression."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self):
        expr, = self.args
        return simplify(expr)


# =============================================================================
# PolynomialQuotient[p, q, x] — polynomial division quotient
# =============================================================================

class PolynomialQuotient(RubiFunction):
    """Mathematica PolynomialQuotient[p, q, x] -> quotient of p/q in x."""

    def __new__(cls, p, q, x):
        return Expr.__new__(cls, p, q, x)

    def _evaluate(self):
        p, q, x = self.args
        return sympy.quo(p, q, x)


# =============================================================================
# PolynomialRemainder[p, q, x] — polynomial division remainder
# =============================================================================

class PolynomialRemainder(RubiFunction):
    """Mathematica PolynomialRemainder[p, q, x] -> remainder of p/q in x."""

    def __new__(cls, p, q, x):
        return Expr.__new__(cls, p, q, x)

    def _evaluate(self):
        p, q, x = self.args
        return sympy.rem(p, q, x)


# =============================================================================
# Set[symbol, expr] — Mathematica local variable binding
# =============================================================================

class Set(RubiFunction):
    """Mathematica Set[symbol, expr] — a local variable binding.

    Used as an element inside List[...] passed to With or Module.
    _evaluate returns self so the binding structure is preserved for
    With/Module to inspect when building the substitution dict.
    """

    def __new__(cls, symbol, expr):
        return Expr.__new__(cls, symbol, expr)

    def _evaluate(self):
        # Return self: Set is a structured binding marker, not a reducible expr.
        return self


# =============================================================================
# List[*items] — Mathematica ordered list
# =============================================================================

class List(RubiFunction):
    """Mathematica List[...] — an ordered container of expressions.

    Primarily used to wrap Set bindings passed to With or Module, e.g.:\n        List(Set(Symbol('q'), val), Set(Symbol('k'), val2))

    _evaluate returns self so the structure is preserved for With/Module.
    """

    def __new__(cls, *items):
        items = [sympy.sympify(i) if not isinstance(i, sympy.Basic) else i
                 for i in items]
        return Expr.__new__(cls, *items)

    def _evaluate(self):
        # Return self: List is a container, not a reducible expression.
        return self

    def __iter__(self):
        yield from self.args


# =============================================================================
# With[List(...), body] — Mathematica local constant bindings
# =============================================================================

class With(RubiFunction):
    """Mathematica With[{Set[var, val], ...}, body] — local constant bindings.

    Evaluates the value of each Set binding, substitutes all bindings into
    the *unevaluated* body, then evaluates the result.  The body is kept
    unevaluated until after substitution so that expressions depending on
    the local variables are not evaluated prematurely.

    Example::

        q = Symbol('q')
        With(List(Set(q, sympy.sqrt(2))), q**2 + 1).doit()
        # -> 3

    doit() is overridden here because the base-class implementation
    deep-evaluates all args before calling _evaluate(), which would
    evaluate the body before q is bound — producing wrong results.
    """

    def __new__(cls, bindings, body):
        return Expr.__new__(cls, bindings, body)

    def doit(self, **kwargs):
        """Evaluate bindings first, then substitute into the unevaluated body."""
        deep = kwargs.get('deep', True)
        bindings_raw, body_raw = self.args

        # Step 1: evaluate only the bindings side (List of Set nodes).
        if deep and hasattr(bindings_raw, 'doit'):
            bindings_eval = bindings_raw.doit(**kwargs)
        else:
            bindings_eval = bindings_raw

        # Step 2: build substitution dict from List(Set(sym, val), ...).
        subs = {}
        if isinstance(bindings_eval, List):
            for item in bindings_eval.args:
                if isinstance(item, Set):
                    sym, val = item.args
                    subs[sym] = val

        # Step 3: substitute into the un-doit'd body, then evaluate the result.
        result = body_raw
        for sym, val in subs.items():
            result = result.subs(sym, val)
        if deep and hasattr(result, 'doit'):
            result = result.doit(**kwargs)
        return result

    def _evaluate(self):
        # Fallback only; the evaluation path goes through the overridden doit().
        return self


# =============================================================================
# Module[List(...), body] — Mathematica local variable scope
# =============================================================================

class Module(RubiFunction):
    """Mathematica Module[{var, ...}, body] — local variable scope.

    In Rubi's generated rules, Module behaves like With: the locals list
    contains Set bindings that are substituted into the body.  Plain symbol
    entries (without a Set) are replaced with fresh unique symbols to avoid
    name collisions.

    doit() is overridden for the same reason as With: the body must not be
    evaluated before the local bindings are substituted.
    """

    def __new__(cls, locals_list, body):
        return Expr.__new__(cls, locals_list, body)

    def doit(self, **kwargs):
        """Evaluate bindings first, then substitute into the unevaluated body."""
        deep = kwargs.get('deep', True)
        locals_raw, body_raw = self.args

        if deep and hasattr(locals_raw, 'doit'):
            locals_eval = locals_raw.doit(**kwargs)
        else:
            locals_eval = locals_raw

        subs = {}
        if isinstance(locals_eval, List):
            for item in locals_eval.args:
                if isinstance(item, Set):
                    sym, val = item.args
                    subs[sym] = val
                elif isinstance(item, Symbol):
                    # Plain local declaration: introduce a fresh unique symbol.
                    subs[item] = Symbol(f'_mod_{item.name}')

        result = body_raw
        for sym, val in subs.items():
            result = result.subs(sym, val)
        if deep and hasattr(result, 'doit'):
            result = result.doit(**kwargs)
        return result

    def _evaluate(self):
        # Fallback only; the evaluation path goes through the overridden doit().
        return self


# =============================================================================
# CannotIntegrate[expr, x] — integration failure sentinel
# =============================================================================

class CannotIntegrate(RubiFunction):
    """Mathematica CannotIntegrate[expr, x] — integration failure sentinel.

    Returned unevaluated when no Rubi rule applies to the integrand.
    _evaluate returns self so the sentinel propagates unchanged through
    any further .doit() calls.
    """

    def __new__(cls, expr, x):
        return Expr.__new__(cls, expr, x)

    def _evaluate(self):
        # Terminal sentinel: stays unevaluated.
        return self


# =============================================================================
# Condition[expr, test] — conditional expression
# =============================================================================

class Condition(RubiFunction):
    """Mathematica Condition[expr, test].

    Returns expr at evaluation time. The condition was already verified by the
    Rubi pattern-matching constraints at match time.
    """

    def __new__(cls, expr, test):
        return Expr.__new__(cls, expr, test)

    def _evaluate(self):
        expr, test = self.args
        # By the time _evaluate() is called, With.doit() has already substituted
        # the local variable bindings (e.g. Symbol('v') -> actual simplified value),
        # so test.args contain actual SymPy expressions, not WildSymbols.
        # We check the condition and raise StopIteration on failure — this propagates
        # through _make_replacement_fn and is caught by ManyToOneReplacer.replace()
        # as "no match", matching Mathematica's Condition[expr, test] semantics.
        if isinstance(test, RubiConstraint):
            if not test.check():   # no kwargs needed: args are already resolved
                raise StopIteration
        elif test is False or test == sympy.S.false:
            raise StopIteration
        return expr.doit() if hasattr(expr, 'doit') else expr


# =============================================================================
# Rule[lhs, rhs] — Mathematica substitution rule (lhs -> rhs)
# =============================================================================

class Rule(RubiFunction):
    """Mathematica Rule[lhs, rhs] — a (lhs -> rhs) substitution descriptor.

    Used as argument to ReplaceAll. _evaluate returns self because Rule
    is structural rather than a reducible expression.
    """

    def __new__(cls, lhs, rhs):
        return Expr.__new__(cls, lhs, rhs)

    def _evaluate(self):
        return self


# =============================================================================
# ReplaceAll[expr, Rule[lhs, rhs]] — apply substitution rule
# =============================================================================

class ReplaceAll(RubiFunction):
    """Mathematica ReplaceAll[expr, Rule[lhs, rhs]] — substitute lhs -> rhs."""

    def __new__(cls, expr, rule):
        return Expr.__new__(cls, expr, rule)

    def _evaluate(self):
        expr, rule = self.args
        if isinstance(rule, Rule):
            lhs, rhs = rule.args
            return expr.subs(lhs, rhs)
        return expr


# =============================================================================
# Unintegrable[expr, x] — integration failure sentinel
# =============================================================================

class Unintegrable(RubiFunction):
    """Rubi Unintegrable[expr, x] — marks that no rule could integrate expr.

    Different from CannotIntegrate; used for trig/special-function integrands
    that Rubi declines to reduce. Stays unevaluated.
    """

    def __new__(cls, expr, x):
        return Expr.__new__(cls, expr, x)

    def _evaluate(self):
        return self


# =============================================================================
# IntHide[u, x] — integrate with step display suppressed
# =============================================================================

class IntHide(RubiFunction):
    """Rubi IntHide[u, x] — calls Int[u, x] with step display suppressed.

    Kept unevaluated in this implementation (no step display machinery).
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)

    def _evaluate(self):
        return self


# =============================================================================
# Sum[expr, limits] — symbolic summation
# =============================================================================

class SumWolfram(RubiFunction):
    """Mathematica Sum[expr, {i, imin, imax}] — symbolic summation.

    Delegates to sympy.Sum when limits is a List of three elements.
    """

    def __new__(cls, expr, limits):
        return Expr.__new__(cls, expr, limits)

    def _evaluate(self):
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

class Numerator(RubiFunction):
    """Mathematica Numerator[expr] -> numerator of rational expression."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self):
        expr, = self.args
        return numer(expr)


# =============================================================================
# Together[expr] — combine fractions over a common denominator
# =============================================================================

class Together(RubiFunction):
    """Mathematica Together[expr] -> combine fractions."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self):
        expr, = self.args
        return together(expr)


# =============================================================================
# GCD[a, b, ...] — greatest common divisor
# =============================================================================

class GCD(RubiFunction):
    """Mathematica GCD[a, b, ...] -> greatest common divisor."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class Sign(RubiFunction):
    """Mathematica Sign[expr] -> sign (-1, 0, or 1)."""

    def __new__(cls, expr):
        return Expr.__new__(cls, expr)

    def _evaluate(self):
        expr, = self.args
        return sign(expr)


# =============================================================================
# Quotient[a, b] — integer quotient floor(a/b)
# =============================================================================

class Quotient(RubiFunction):
    """Mathematica Quotient[a, b] -> floor(a/b)."""

    def __new__(cls, a, b):
        return Expr.__new__(cls, a, b)

    def _evaluate(self):
        a, b = self.args
        return floor(a / b)


# =============================================================================
# EllipticPi — elliptic integral of the third kind
# =============================================================================

class EllipticPi(RubiFunction):
    """Mathematica EllipticPi[n, m] or EllipticPi[n, phi, m].

    Maps to sympy.elliptic_pi(n, m) or sympy.elliptic_pi(n, phi, m).
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class PolynomialDivide(RubiFunction):
    """Rubi PolynomialDivide[u, v, x] = quo(u,v,x) + rem(u,v,x)/v."""

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class NormalizePseudoBinomial(RubiFunction):
    """Rubi NormalizePseudoBinomial[u, x] — rewrite as a + b*(c+d*x)^n.

    Falls back to u unchanged if the form cannot be detected.
    """

    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)

    def _evaluate(self):
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

class SubstFor(RubiFunction):
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

    def _evaluate(self):
        if len(self.args) == 3:
            v, u, x = self.args
            return u.subs(v, x)
        elif len(self.args) == 4:
            w, v, u, x = self.args
            inner = SubstFor(v, u, x).doit()
            return simplify(w * inner)
        return self


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
# Additional RubiFunction wrappers for generated code
# These wrap utility_functions.* implementations for use in generated rules
# =============================================================================

class Dist(RubiFunction):
    """Rubi Dist[u, v, x] — distribute u over v."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Dist as _Dist
        return _Dist(*self.args)


class SimplifyIntegrand(RubiFunction):
    """Rubi SimplifyIntegrand[u, x] — simplify integrand."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import SimplifyIntegrand as _SimplifyIntegrand
        return _SimplifyIntegrand(*self.args)


class FreeFactors(RubiFunction):
    """Rubi FreeFactors[u, x] — product of factors free of x."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self):
        from .utility_functions import FreeFactors as _FreeFactors
        return _FreeFactors(*self.args)


class NonfreeFactors(RubiFunction):
    """Rubi NonfreeFactors[u, x] — product of factors not free of x."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self):
        from .utility_functions import NonfreeFactors as _NonfreeFactors
        return _NonfreeFactors(*self.args)


class ActivateTrig(RubiFunction):
    """Rubi ActivateTrig[u] — activate trig expressions."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self):
        from .utility_functions import ActivateTrig as _ActivateTrig
        return _ActivateTrig(self.args[0])


class DeactivateTrig(RubiFunction):
    """Rubi DeactivateTrig[u, x] — deactivate trig expressions."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import DeactivateTrig as _DeactivateTrig
        return _DeactivateTrig(*self.args)


class ExpandTrig(RubiFunction):
    """Rubi ExpandTrig[u, x] — expand trig expressions."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import ExpandTrig as _ExpandTrig
        return _ExpandTrig(*self.args)


class ExpandTrigReduce(RubiFunction):
    """Rubi ExpandTrigReduce[u, x] — expand and reduce trig."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import ExpandTrigReduce as _ExpandTrigReduce
        return _ExpandTrigReduce(*self.args)


class DerivativeDivides(RubiFunction):
    """Rubi DerivativeDivides[u, v, x] — check derivative divides."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import DerivativeDivides as _DerivativeDivides
        return _DerivativeDivides(*self.args)


class BinomialDegree(RubiFunction):
    """Rubi BinomialDegree[u, x] — degree of binomial."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self):
        from .utility_functions import BinomialDegree as _BinomialDegree
        return _BinomialDegree(*self.args)


class TrinomialDegree(RubiFunction):
    """Rubi TrinomialDegree[u, x] — degree of trinomial."""
    def __new__(cls, u, x):
        return Expr.__new__(cls, u, x)
    def _evaluate(self):
        from .utility_functions import TrinomialDegree as _TrinomialDegree
        return _TrinomialDegree(*self.args)


class LeafCount(RubiFunction):
    """Mathematica LeafCount[expr] — count nodes in expression tree."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from .utility_functions import LeafCount as _LeafCount
        return Integer(_LeafCount(self.args[0]))


class Part(RubiFunction):
    """Mathematica Part[expr, n] — extract nth part."""
    def __new__(cls, expr, *indices):
        return Expr.__new__(cls, expr, *indices)
    def _evaluate(self):
        from .utility_functions import Part as _Part
        return _Part(*self.args)


class First(RubiFunction):
    """Mathematica First[expr] — first element."""
    def __new__(cls, expr, d=None):
        if d is None:
            return Expr.__new__(cls, expr)
        return Expr.__new__(cls, expr, d)
    def _evaluate(self):
        from .utility_functions import First as _First
        return _First(*self.args)


class Rest(RubiFunction):
    """Mathematica Rest[expr] — all but first element."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from .utility_functions import Rest as _Rest
        return _Rest(self.args[0])


class Head(RubiFunction):
    """Mathematica Head[expr] — head (type) of expression."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from .utility_functions import Head as _Head
        return _Head(self.args[0])


class Length(RubiFunction):
    """Mathematica Length[expr] — number of elements."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from .utility_functions import Length as _Length
        return Integer(_Length(self.args[0]))


class If(RubiFunction):
    """Mathematica If[condition, true, false] — conditional."""
    def __new__(cls, cond, t, f=None):
        if f is None:
            return Expr.__new__(cls, cond, t)
        return Expr.__new__(cls, cond, t, f)
    def _evaluate(self):
        from .utility_functions import If as _If
        return _If(*self.args)


class Complex(RubiFunction):
    """Mathematica Complex[re, im] — construct complex number."""
    def __new__(cls, re, im):
        from .utility_functions import Complex as _Complex
        return _Complex(re, im)
    def _evaluate(self):
        pass


class Numer(RubiFunction):
    """Rubi Numer[u] — numerator (simple form)."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self):
        from .utility_functions import Numer as _Numer
        return _Numer(self.args[0])


class Denom(RubiFunction):
    """Rubi Denom[u] — denominator (simple form)."""
    def __new__(cls, u):
        return Expr.__new__(cls, u)
    def _evaluate(self):
        from .utility_functions import Denom as _Denom
        return _Denom(self.args[0])


class CompoundExpression(RubiFunction):
    """Mathematica CompoundExpression[e1, e2, ...] — evaluate in sequence, return last."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        # Evaluate all args, return last result
        result = None
        for arg in self.args:
            result = arg.doit() if hasattr(arg, 'doit') else arg
        return result


class Apply(RubiFunction):
    """Mathematica Apply[f, {a, b, ...}] — apply f to list elements."""
    def __new__(cls, f, args):
        return Expr.__new__(cls, f, args)
    def _evaluate(self):
        f, args = self.args
        if hasattr(args, 'args'):
            return f(*args.args)
        return f(*args)


class Not(RubiFunction):
    """Mathematica Not[expr] — logical negation."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from .utility_functions import Not as _Not
        return _Not(self.args[0])




# =============================================================================
# Additional Rubi utility function wrappers
# =============================================================================

class NormalizePowerOfLinear(RubiFunction):
    """Rubi NormalizePowerOfLinear[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import NormalizePowerOfLinear as _NormalizePowerOfLinear
        return _NormalizePowerOfLinear(*self.args)


class NormalizeIntegrand(RubiFunction):
    """Rubi NormalizeIntegrand[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import NormalizeIntegrand as _NormalizeIntegrand
        return _NormalizeIntegrand(*self.args)


class Exponent(RubiFunction):
    """Mathematica Exponent[expr, form]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Exponent as _Exponent
        return _Exponent(*self.args)


class FullSimplify(RubiFunction):
    """Mathematica FullSimplify[expr]."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        return simplify(self.args[0])


class FunctionExpand(RubiFunction):
    """Mathematica FunctionExpand[expr]."""
    def __new__(cls, expr):
        return Expr.__new__(cls, expr)
    def _evaluate(self):
        from sympy import expand_func
        return expand_func(self.args[0])


class ExpandLinearProduct(RubiFunction):
    """Rubi ExpandLinearProduct[v, u, a, b, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import ExpandLinearProduct as _ExpandLinearProduct
        return _ExpandLinearProduct(*self.args)


class Divides(RubiFunction):
    """Rubi Divides[u, v, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Divides as _Divides
        return _Divides(*self.args)


class RationalFunctionExpand(RubiFunction):
    """Rubi RationalFunctionExpand[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import RationalFunctionExpand as _RationalFunctionExpand
        return _RationalFunctionExpand(*self.args)


class PowerVariableExpn(RubiFunction):
    """Rubi PowerVariableExpn[u, m, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import PowerVariableExpn as _PowerVariableExpn
        return _PowerVariableExpn(*self.args)


class FunctionOfLinear(RubiFunction):
    """Rubi FunctionOfLinear[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import FunctionOfLinear as _FunctionOfLinear
        return _FunctionOfLinear(*self.args)


class SplitProduct(RubiFunction):
    """Rubi SplitProduct[f, u]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import SplitProduct as _SplitProduct
        return _SplitProduct(*self.args)


class PolyGCD(RubiFunction):
    """Rubi PolyGCD[a, b, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import PolyGCD as _PolyGCD
        return _PolyGCD(*self.args)


class GeneralizedTrinomialDegree(RubiFunction):
    """Rubi GeneralizedTrinomialDegree[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import GeneralizedTrinomialDegree as _GeneralizedTrinomialDegree
        return _GeneralizedTrinomialDegree(*self.args)


class ExpandTrigToExp(RubiFunction):
    """Rubi ExpandTrigToExp[u, x]."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import ExpandTrigToExp as _ExpandTrigToExp
        return _ExpandTrigToExp(*self.args)


class Binomial(RubiFunction):
    """Mathematica Binomial[n, k]."""
    def __new__(cls, n, k):
        return Expr.__new__(cls, n, k)
    def _evaluate(self):
        from sympy import binomial
        return binomial(*self.args)


# =============================================================================
# ProductLog[z] or ProductLog[k, z] — Lambert W function
# Mathematica: ProductLog[k, z] where k=branch index, z=value
# SymPy:       LambertW(z, k)   where z=value, k=branch  (args REVERSED)
# =============================================================================

class ProductLog(RubiFunction):
    """Mathematica ProductLog[z] or ProductLog[k, z] -> LambertW.

    1-arg: ProductLog(z)    -> LambertW(z)
    2-arg: ProductLog(k, z) -> LambertW(z, k)  [Mathematica arg order reversed vs SymPy]
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class Floor(RubiFunction):
    """Mathematica Floor[x] or Floor[x, a].

    1-arg: Floor(x)    -> floor(x)
    2-arg: Floor(x, a) -> a * floor(x / a)   [rounds to nearest multiple of a]
    """

    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
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

class Hypergeometric2F1(RubiFunction):
    """Mathematica Hypergeometric2F1[a, b, c, z] -> hyper([a, b], [c], z)."""

    def __new__(cls, a, b, c, z):
        return Expr.__new__(cls, a, b, c, z)

    def _evaluate(self):
        a, b, c, z = self.args
        from sympy.functions.special.hyper import hyper
        return hyper([a, b], [c], z)


# =============================================================================
# Lazy RubiFunction wrappers for utility_functions plain callables
# =============================================================================
# Additional RubiFunction wrappers for functions used in generated rules.
# These were previously missing explicit class definitions.
# =============================================================================

class MinimumMonomialExponent(RubiFunction):
    """Rubi MinimumMonomialExponent[u, x] — minimum monomial exponent."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import MinimumMonomialExponent as _f
        return _f(*self.args)


class Distrib(RubiFunction):
    """Rubi Distrib[u, v] — distribute u over v."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Distrib as _f
        return _f(*self.args)


class Apart(RubiFunction):
    """Rubi Apart[u, x] — partial fraction decomposition."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Apart as _f
        return _f(*self.args)


class ExpandExpression(RubiFunction):
    """Rubi ExpandExpression[u, x] — expand expression."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import ExpandExpression as _f
        return _f(*self.args)


class FunctionOfTrig(RubiFunction):
    """Rubi FunctionOfTrig[u, ...] — function of trig."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import FunctionOfTrig as _f
        return _f(*self.args)


class PolynomialInSubst(RubiFunction):
    """Rubi PolynomialInSubst[u, v, x] — polynomial in substitution."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import PolynomialInSubst as _f
        return _f(*self.args)


class QuotientOfLinearsParts(RubiFunction):
    """Rubi QuotientOfLinearsParts[u, x] — parts of quotient of linears."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import QuotientOfLinearsParts as _f
        return _f(*self.args)


class SubstForFractionalPowerOfLinear(RubiFunction):
    """Rubi SubstForFractionalPowerOfLinear[u, x] — substitution for fractional power."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import SubstForFractionalPowerOfLinear as _f
        return _f(*self.args)


class TrigSimplify(RubiFunction):
    """Rubi TrigSimplify[u] — simplify trig expression."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import TrigSimplify as _f
        return _f(*self.args)


class RationalFunctionExponents(RubiFunction):
    """Rubi RationalFunctionExponents[u, x] — exponents of rational function."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import RationalFunctionExponents as _f
        return _f(*self.args)


class Denominator(RubiFunction):
    """Rubi Denominator[expr] — denominator of expression (lazy, not eagerly evaluated)."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)
    def _evaluate(self):
        from .utility_functions import Denominator as _f
        return _f(*self.args)


# =============================================================================
# Gamma[z] or Gamma[a, z] — gamma and upper incomplete gamma function
# =============================================================================
# Mathematica: Gamma[z] -> gamma(z), Gamma[a, z] -> uppergamma(a, z)
# Needs a wrapper because sympy.gamma only takes 1 arg.

class Gamma(RubiFunction):
    """Mathematica Gamma[z] or Gamma[a, z] -> sympy.gamma / sympy.uppergamma."""
    def __new__(cls, *args):
        safe = [sympy.sympify(a) for a in args]
        return Expr.__new__(cls, *safe)

    def _evaluate(self):
        if len(self.args) == 1:
            return sympy.gamma(self.args[0])
        else:
            return sympy.uppergamma(self.args[0], self.args[1])
