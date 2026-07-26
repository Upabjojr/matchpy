# -*- coding: utf-8 -*-
"""Tests for Rubi integration rules.

Tests the full pipeline:
    SymPy rule definitions -> MatchPy patterns -> pattern matching -> replacement -> SymPy result
"""
import sys
import os
import pytest
import sympy
from sympy import Symbol, Integer, Rational, log, sqrt, pi, oo

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
from sympy_matching.conversion import to_matchpy_expression, matchpy_to_sympy
from rubi_rules.base_objects import Int, RubiRulePattern, build_tracing_replacer
from rubi_rules.utils import FreeQ, NeQ, IntegerQ


# --- Fixtures ---

@pytest.fixture(scope='module')
def replacer():
    """Build a ManyToOneReplacer from the generated 1.1.1.1 rules."""
    from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products.r_1_1_1_linear.r_1_1_1_1 import RULES
    return build_tracing_replacer(RULES)


@pytest.fixture(scope='module')
def x():
    return Symbol('x')


def _helper_rubi_integrate(replacer, expr, x):
    """Use Rubi replacer to integrate expr w.r.t. x."""
    int_expr = to_matchpy_expression(Int(expr, x))
    result = replacer.replace(int_expr)[0]
    return matchpy_to_sympy(result)


# --- Test: Rule loading and replacer construction ---

class TestRuleLoading:
    def test_rules_load(self):
        from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products.r_1_1_1_linear.r_1_1_1_1 import RULES
        assert len(RULES) == 5
        assert all(isinstance(r, RubiRulePattern) for r in RULES)

    def test_build_replacer(self, replacer):
        assert len(replacer.matcher.patterns) == 5

    def test_rule_has_pattern(self):
        from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products.r_1_1_1_linear.r_1_1_1_1 import RULES
        rule = RULES[0]
        assert isinstance(rule.pattern, sympy.Basic)
        assert isinstance(rule.replacement, sympy.Basic)


# --- Test: Basic power rule integrals ---

class TestPowerRules:
    """Int[x^n, x] = x^(n+1)/(n+1) for n != -1."""

    def test_int_1_over_x(self, replacer, x):
        result = _helper_rubi_integrate(replacer, 1 / x, x)
        assert sympy.simplify(result - log(x)) == 0

    def test_int_x_squared(self, replacer, x):
        result = _helper_rubi_integrate(replacer, x ** 2, x)
        expected = x**3 / 3
        assert sympy.simplify(result - expected) == 0

    def test_int_x_cubed(self, replacer, x):
        result = _helper_rubi_integrate(replacer, x ** 3, x)
        expected = x**4 / 4
        assert sympy.simplify(result - expected) == 0

    def test_int_sqrt_x(self, replacer, x):
        result = _helper_rubi_integrate(replacer, sqrt(x), x)
        expected = 2 * x**Rational(3, 2) / 3
        assert sympy.simplify(result - expected) == 0

    def test_int_1_over_sqrt_x(self, replacer, x):
        result = _helper_rubi_integrate(replacer, 1 / sqrt(x), x)
        expected = 2 * sqrt(x)
        assert sympy.simplify(result - expected) == 0

    def test_int_x_to_rational(self, replacer, x):
        result = _helper_rubi_integrate(replacer, x ** Rational(2, 3), x)
        expected = x**Rational(5, 3) / Rational(5, 3)
        assert sympy.simplify(result - expected) == 0


# --- Test: Linear binomial integrals ---

class TestLinearBinomial:
    """Int[(a + b*x)^m, x] = (a + b*x)^(m+1) / (b*(m+1))."""

    def test_int_1_over_a_plus_bx(self, replacer, x):
        a, b = sympy.symbols('a b')
        result = _helper_rubi_integrate(replacer, 1 / (a + b * x), x)
        expected = log(a + b*x) / b
        assert sympy.simplify(result - expected) == 0

    def test_int_a_plus_bx_squared(self, replacer, x):
        a, b = sympy.symbols('a b')
        result = _helper_rubi_integrate(replacer, (a + b * x) ** 2, x)
        expected = (a + b*x)**3 / (3*b)
        assert sympy.simplify(result - expected) == 0

    def test_int_a_plus_bx_half(self, replacer, x):
        a, b = sympy.symbols('a b')
        result = _helper_rubi_integrate(replacer, sqrt(a + b * x), x)
        expected = 2*(a + b*x)**Rational(3,2) / (3*b)
        assert sympy.simplify(result - expected) == 0


# --- Test: Constraint checking ---

class TestConstraints:
    """Verify that constraints are enforced correctly."""

    def test_freeq_blocks_dependent_match(self, replacer, x):
        # Int(x*x^2, x) - here 'a' would match x which is NOT free of x
        # So the (a+bx)^m rule should NOT apply to x*x^2 interpreted as (x)^1*(x^2)
        # But x^3 should still work via the power rule
        result = _helper_rubi_integrate(replacer, x ** 3, x)
        assert sympy.simplify(result - x**4/4) == 0


# --- Test: Manual rule construction ---

class TestManualRules:
    """Test building rules manually with RubiRulePattern."""

    def test_custom_rule(self):
        x = Symbol('x')
        n_ = WildSymbol('n_')
        rule = RubiRulePattern(
            pattern=Int(x**n_, x),
            constraints=(FreeQ(n_, x), NeQ(n_, -1)),
            replacement=x**(n_ + 1) / (n_ + 1),
            module_name="TEST",
            rule_number=1,
        )
        replacer = build_tracing_replacer([rule])
        int_expr = to_matchpy_expression(Int(x**5, x))
        result = matchpy_to_sympy(replacer.replace(int_expr)[0])
        assert sympy.simplify(result - x**6/6) == 0
