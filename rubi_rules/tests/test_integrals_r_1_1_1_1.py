# -*- coding: utf-8 -*-
"""Integration tests for rules defined in r_1_1_1_1.py — (a+b*x)^m.

This test module loads ONLY the r_1_1_1_1.py rule file (5 rules for
powers of linear expressions) and verifies that rubi_integrate produces
correct antiderivatives.

Rules covered:
  1. Int(1/x, x) → log(x)
  2. Int(x^m, x) → x^(m+1)/(m+1)  [m ≠ -1, FreeQ(m, x)]
  3. Int(1/(a+b*x), x) → log(a+b*x)/b  [FreeQ([a,b], x)]
  4. Int((a+b*x)^m, x) → (a+b*x)^(m+1)/(b*(m+1))  [FreeQ([a,b,m], x), m ≠ -1]
  5. Int((a+b*u)^m, x) → Subst(...)  [u linear in x, u ≠ x]
"""
import pytest
import sympy
from sympy import Symbol, Integer, Rational, log, sqrt, simplify, S

from rubi_rules.base_objects import build_replacer, _matchpy_integrate


# ---------------------------------------------------------------------------
# Fixture: build a replacer from ONLY r_1_1_1_1.py rules
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def replacer():
    """Build a ManyToOneReplacer containing only r_1_1_1_1 rules."""
    from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products.r_1_1_1_linear.r_1_1_1_1 import RULES
    return build_replacer(RULES)


# ---------------------------------------------------------------------------
# Integration variable and free parameters
# ---------------------------------------------------------------------------

x = Symbol('x')
a, b, m, n = sympy.symbols('a b m n')


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _integrate(expr, replacer):
    """Integrate expr w.r.t. x using the provided replacer."""
    return _matchpy_integrate(expr, x, replacer)


# ---------------------------------------------------------------------------
# Rule 1: Int(1/x, x) → log(x)
# ---------------------------------------------------------------------------

class TestRule1:
    """Rule 1: Int(1/x) = log(x)."""

    def test_one_over_x(self, replacer):
        result = _integrate(1/x, replacer)
        assert result == log(x)


# ---------------------------------------------------------------------------
# Rule 2: Int(x^m, x) → x^(m+1)/(m+1)  [m ≠ -1]
# ---------------------------------------------------------------------------

class TestRule2:
    """Rule 2: Int(x^m) = x^(m+1)/(m+1), m free of x, m ≠ -1."""

    def test_x_squared(self, replacer):
        result = _integrate(x**2, replacer)
        expected = x**3 / 3
        assert simplify(result - expected) == 0

    def test_x_fifth(self, replacer):
        result = _integrate(x**5, replacer)
        expected = x**6 / 6
        assert simplify(result - expected) == 0

    def test_x_half(self, replacer):
        """Int(sqrt(x)) = 2*x^(3/2)/3."""
        result = _integrate(sqrt(x), replacer)
        expected = Rational(2, 3) * x**Rational(3, 2)
        assert simplify(result - expected) == 0

    def test_x_neg_half(self, replacer):
        """Int(1/sqrt(x)) = 2*sqrt(x)."""
        result = _integrate(x**Rational(-1, 2), replacer)
        expected = 2 * sqrt(x)
        assert simplify(result - expected) == 0

    def test_x_symbolic(self, replacer):
        """Int(x^n) = x^(n+1)/(n+1) for symbolic n."""
        result = _integrate(x**n, replacer)
        expected = x**(n + 1) / (n + 1)
        assert simplify(result - expected) == 0

    def test_x_rational_exponent(self, replacer):
        """Int(x^(2/3)) = x^(5/3)/(5/3) = 3*x^(5/3)/5."""
        result = _integrate(x**Rational(2, 3), replacer)
        expected = Rational(3, 5) * x**Rational(5, 3)
        assert simplify(result - expected) == 0

    def test_x_neg_two(self, replacer):
        """Int(x^(-2)) = -1/x."""
        result = _integrate(x**Integer(-2), replacer)
        expected = -1 / x
        assert simplify(result - expected) == 0


# ---------------------------------------------------------------------------
# Rule 3: Int(1/(a+b*x), x) → log(a+b*x)/b
# ---------------------------------------------------------------------------

class TestRule3:
    """Rule 3: Int(1/(a+b*x)) = log(a+b*x)/b."""

    def test_one_over_1_plus_2x(self, replacer):
        result = _integrate(1/(1 + 2*x), replacer)
        expected = log(1 + 2*x) / 2
        assert simplify(result - expected) == 0

    def test_one_over_3_plus_5x(self, replacer):
        result = _integrate(1/(3 + 5*x), replacer)
        expected = log(3 + 5*x) / 5
        assert simplify(result - expected) == 0

    def test_one_over_a_plus_bx_symbolic(self, replacer):
        result = _integrate(1/(a + b*x), replacer)
        expected = log(a + b*x) / b
        assert simplify(result - expected) == 0


# ---------------------------------------------------------------------------
# Rule 4: Int((a+b*x)^m, x) → (a+b*x)^(m+1)/(b*(m+1))  [m ≠ -1]
# ---------------------------------------------------------------------------

class TestRule4:
    """Rule 4: Int((a+b*x)^m) = (a+b*x)^(m+1)/(b*(m+1))."""

    def test_linear_squared(self, replacer):
        """Int((1+2*x)^2) = (1+2*x)^3/6."""
        result = _integrate((1 + 2*x)**2, replacer)
        expected = (1 + 2*x)**3 / 6
        assert simplify(result - expected) == 0

    def test_linear_cubed(self, replacer):
        """Int((3+5*x)^3) = (3+5*x)^4/20."""
        result = _integrate((3 + 5*x)**3, replacer)
        expected = (3 + 5*x)**4 / 20
        assert simplify(result - expected) == 0

    def test_linear_sqrt(self, replacer):
        """Int(sqrt(a+b*x)) = 2*(a+b*x)^(3/2)/(3*b)."""
        result = _integrate(sqrt(a + b*x), replacer)
        expected = Rational(2, 3) * (a + b*x)**Rational(3, 2) / b
        assert simplify(result - expected) == 0

    def test_linear_symbolic_power(self, replacer):
        """Int((a+b*x)^m) = (a+b*x)^(m+1)/(b*(m+1)) for symbolic m."""
        result = _integrate((a + b*x)**m, replacer)
        expected = (a + b*x)**(m + 1) / (b * (m + 1))
        assert simplify(result - expected) == 0

    def test_linear_neg_half(self, replacer):
        """Int(1/sqrt(2+3*x)) = 2*sqrt(2+3*x)/3."""
        result = _integrate((2 + 3*x)**Rational(-1, 2), replacer)
        expected = Rational(2, 3) * sqrt(2 + 3*x)
        assert simplify(result - expected) == 0

    def test_linear_neg_two(self, replacer):
        """Int(1/(a+b*x)^2) = -1/(b*(a+b*x))."""
        result = _integrate((a + b*x)**Integer(-2), replacer)
        expected = -1 / (b * (a + b*x))
        assert simplify(result - expected) == 0
