# -*- coding: utf-8 -*-
"""Integration tests for rules defined in r_1_1_2_1.py — (a+b*x^2)^p.

This test module loads ONLY the r_1_1_2_1.py rule file (18 rules for
powers of quadratic binomials in x^2) and verifies that rubi_integrate
produces correct antiderivatives.

Key rules tested:
  2.  Int(1/(a+b*x^2)^(3/2)) → x/(a*sqrt(a+b*x^2))
  10. Int(1/(a+b*x^2)) → atan(sqrt(b)*x/sqrt(a))/(sqrt(b)*sqrt(a))  [PosQ(a/b), a>0|b>0]
  13. Int(1/(a+b*x^2)) → atanh(x*sqrt(-b)/sqrt(a))/(sqrt(a)*sqrt(-b))  [NegQ(a/b), a>0|b<0]
  16. Int(1/sqrt(a+b*x^2)) → asinh(sqrt(b)*x/sqrt(a))/sqrt(b)  [a>0, b>0]
  17. Int(1/sqrt(a+b*x^2)) → asin(x*sqrt(-b)/sqrt(a))/sqrt(-b)  [a>0, b<0]
"""
import pytest
import sympy
from sympy import (
    Symbol, Integer, Rational, log, sqrt, simplify, S,
    atan, atanh, asinh, asin, diff,
)

from rubi_rules.base_objects import build_replacer, _matchpy_integrate, Int


# ---------------------------------------------------------------------------
# Fixture: build a replacer from ONLY r_1_1_2_1.py rules
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def replacer():
    """Build a ManyToOneReplacer containing only r_1_1_2_1 rules."""
    from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products.r_1_1_2_quadratic.r_1_1_2_1 import RULES
    return build_replacer(RULES)


# ---------------------------------------------------------------------------
# Integration variable
# ---------------------------------------------------------------------------

x = Symbol('x')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _integrate(expr, replacer):
    """Integrate expr w.r.t. x using the provided replacer."""
    return _matchpy_integrate(expr, x, replacer)


def _to_real_sympy(expr):
    """Recursively replace MatchPy-roundtripped function classes with real SymPy ones.

    The matchpy_to_sympy conversion can produce function objects (e.g. atan)
    that print identically but are not ``is``-identical to the canonical SymPy
    classes, preventing simplification and differentiation.  This helper
    reconstructs the expression using the real SymPy functions.
    """
    if expr.is_Number or expr.is_Symbol:
        return expr
    if hasattr(expr, 'func') and hasattr(expr.func, '__name__'):
        name = expr.func.__name__
        real_func = getattr(sympy, name, None)
        if real_func is not None and real_func is not expr.func:
            new_args = [_to_real_sympy(a) for a in expr.args]
            return real_func(*new_args)
    if expr.args:
        new_args = [_to_real_sympy(a) for a in expr.args]
        return expr.func(*new_args)
    return expr


def _check_antiderivative(result, integrand):
    """Verify result is an antiderivative of integrand by differentiation."""
    fixed = _to_real_sympy(result)
    derivative = diff(fixed, x)
    assert simplify(derivative - integrand) == 0, (
        f"d/dx({fixed}) = {derivative}, expected {integrand}"
    )


# ---------------------------------------------------------------------------
# Rule 2: Int(1/(a+b*x^2)^(3/2)) → x/(a*sqrt(a+b*x^2))
# ---------------------------------------------------------------------------

class TestRule2:
    """Rule 2: Int(1/(a+b*x^2)^(3/2)) = x/(a*sqrt(a+b*x^2))."""

    def test_1_plus_x2_pow_neg3half(self, replacer):
        """Int(1/(1+x^2)^(3/2)) = x/sqrt(1+x^2)."""
        integrand = (1 + x**2)**Rational(-3, 2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_plus_4x2_pow_neg3half(self, replacer):
        """Int(1/(1+4*x^2)^(3/2)) = x/sqrt(1+4*x^2)."""
        integrand = (1 + 4*x**2)**Rational(-3, 2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)


# ---------------------------------------------------------------------------
# Rule 10: Int(1/(a+b*x^2)) → atan(sqrt(b)*x/sqrt(a))/(sqrt(b)*sqrt(a))
#           when PosQ(a/b), GtQ(a,0) or GtQ(b,0)
# ---------------------------------------------------------------------------

class TestRule10:
    """Rule 10: Int(1/(a+b*x^2)) with a>0, b>0 → atan form."""

    def test_1_over_1_plus_x2(self, replacer):
        """Int(1/(1+x^2)) = atan(x)."""
        integrand = 1 / (1 + x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_over_1_plus_4x2(self, replacer):
        """Int(1/(1+4*x^2)) = atan(2*x)/2."""
        integrand = 1 / (1 + 4*x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_over_4_plus_9x2(self, replacer):
        """Int(1/(4+9*x^2)) = atan(3*x/2)/6."""
        integrand = 1 / (4 + 9*x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)


# ---------------------------------------------------------------------------
# Rule 13: Int(1/(a+b*x^2)) → atanh form
#           when NegQ(a/b), GtQ(a,0) or LtQ(b,0)
# ---------------------------------------------------------------------------

class TestRule13:
    """Rule 13: Int(1/(a+b*x^2)) with a>0, b<0 → atanh form."""

    def test_1_over_1_minus_x2(self, replacer):
        """Int(1/(1-x^2)) = atanh(x)."""
        integrand = 1 / (1 - x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_over_4_minus_x2(self, replacer):
        """Int(1/(4-x^2)) = atanh(x/2)/2."""
        integrand = 1 / (4 - x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)


# ---------------------------------------------------------------------------
# Rule 16: Int(1/sqrt(a+b*x^2)) → asinh(sqrt(b)*x/sqrt(a))/sqrt(b)
#           when a>0, b>0
# ---------------------------------------------------------------------------

class TestRule16:
    """Rule 16: Int(1/sqrt(a+b*x^2)) with a>0, b>0 → asinh form."""

    def test_1_over_sqrt_1_plus_x2(self, replacer):
        """Int(1/sqrt(1+x^2)) = asinh(x)."""
        integrand = 1 / sqrt(1 + x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_over_sqrt_1_plus_4x2(self, replacer):
        """Int(1/sqrt(1+4*x^2)) = asinh(2*x)/2."""
        integrand = 1 / sqrt(1 + 4*x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)


# ---------------------------------------------------------------------------
# Rule 17: Int(1/sqrt(a+b*x^2)) → asin(x*sqrt(-b)/sqrt(a))/sqrt(-b)
#           when a>0, b<0
# ---------------------------------------------------------------------------

class TestRule17:
    """Rule 17: Int(1/sqrt(a+b*x^2)) with a>0, b<0 → asin form."""

    def test_1_over_sqrt_1_minus_x2(self, replacer):
        """Int(1/sqrt(1-x^2)) = asin(x)."""
        integrand = 1 / sqrt(1 - x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)

    def test_1_over_sqrt_4_minus_x2(self, replacer):
        """Int(1/sqrt(4-x^2)) = asin(x/2)."""
        integrand = 1 / sqrt(4 - x**2)
        result = _integrate(integrand, replacer)
        assert not result.has(Int)
        _check_antiderivative(result, integrand)
