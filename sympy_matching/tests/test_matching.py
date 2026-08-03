# -*- coding: utf-8 -*-
"""Tests for pattern matching on SymPy expressions using OmniMatch.

Tests are parametrized across matching modes (one-to-one, many-to-one,
code-generated, json-roundtrip) via the `match` fixture in conftest.py.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sympy
from sympy import symbols, sin, cos, tan, exp, log, Integer, Eq

from omnimatch.expressions.expressions import (
    Operation, NamedAtom, SymbolWrapper, Wildcard, Pattern, to_omnimatch_expression,
)
from omnimatch.expressions.constraints import CustomConstraint
from omnimatch.matching.one_to_one import match as match_one_to_one
from omnimatch.matching.many_to_one import ManyToOneMatcher, ManyToOneReplacer
from omnimatch import functions as omnimatch_functions

from sympy_matching import to_omnimatch_expression, omnimatch_to_sympy
from sympy_matching.operations import ADD, MUL, POW, SIN, COS, TAN, EXP, LOG, EQUALITY
from sympy_matching.conversion import omnimatch_to_sympy


x, y, z = symbols('x y z')

# ─── SymbolWrapper shorthand for building patterns ────────────────────────────
SW = SymbolWrapper
sw_x = SW(sympy.Symbol('x'))
sw_y = SW(sympy.Symbol('y'))
sw_0 = SW(Integer(0))
sw_1 = SW(Integer(1))
sw_2 = SW(Integer(2))
sw_3 = SW(Integer(3))

# ─── Wildcard helpers ─────────────────────────────────────────────────────────
a_ = Wildcard.dot('a')
b_ = Wildcard.dot('b')
u_ = Wildcard.dot('u')
v_ = Wildcard.dot('v')
w_ = Wildcard.dot('w')
n_ = Wildcard.dot('n')


def _is_numeric_symbol(expr):
    """Check if a SymbolWrapper wraps a SymPy number."""
    if not isinstance(expr, SymbolWrapper):
        return False
    return hasattr(expr.value, 'is_number') and expr.value.is_number


class TestBasicPatternMatching:
    """Test basic pattern matching on SymPy-derived OmniMatch expressions.

    These tests use the `match` fixture and run across all matching modes.
    """

    def test_match_sin_x(self, match):
        """Match sin(anything) → extract the argument."""
        subject = to_omnimatch_expression(sin(x))
        pattern = Pattern(Operation(SIN, a_))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_x

    def test_match_power(self, match):
        """Match expr**n → extract base and exponent."""
        subject = to_omnimatch_expression(x ** 3)
        pattern = Pattern(Operation(POW, a_, n_))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_x
        assert results[0]['n'] == sw_3

    def test_match_sin_squared(self, match):
        """Match sin(u)**2."""
        subject = to_omnimatch_expression(sin(x) ** 2)
        pattern = Pattern(Operation(POW, Operation(SIN, u_), sw_2))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['u'] == sw_x

    def test_match_product_with_coefficient(self, match):
        """Match 2*x as Mul(2, x)."""
        subject = to_omnimatch_expression(2 * x)
        pattern = Pattern(Operation(MUL, sw_2, a_))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_x

    def test_match_equation(self, match):
        """Match Eq(expr, 0) → extract the expression."""
        subject = to_omnimatch_expression(Eq(x ** 2 - 1, 0))
        pattern = Pattern(Operation(EQUALITY, a_, sw_0))
        results = list(match(subject, pattern))
        assert len(results) == 1

    def test_match_cos(self, match):
        """Match cos(anything)."""
        subject = to_omnimatch_expression(cos(y))
        pattern = Pattern(Operation(COS, a_))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_y

    def test_match_exp(self, match):
        """Match exp(anything)."""
        subject = to_omnimatch_expression(exp(x))
        pattern = Pattern(Operation(EXP, a_))
        results = list(match(subject, pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_x

    def test_no_match(self, match):
        """sin(x) should not match cos(a) pattern."""
        subject = to_omnimatch_expression(sin(x))
        pattern = Pattern(Operation(COS, a_))
        results = list(match(subject, pattern))
        assert len(results) == 0


class TestCommutativeMatching:
    """Test commutative matching (Add, Mul are commutative+associative).

    Uses `match` fixture — runs across all modes.
    """

    def test_find_sin_squared_in_sum(self, match):
        """In sin(x)**2 + cos(x)**2, match the sin² term."""
        subject = to_omnimatch_expression(sin(x) ** 2 + cos(x) ** 2)
        rest_ = Wildcard(0, False, variable_name='rest')
        pattern = Pattern(Operation(ADD, Operation(POW, Operation(SIN, u_), sw_2), rest_))
        results = list(match(subject, pattern))
        assert len(results) >= 1
        found_x = any(r['u'] == sw_x for r in results)
        assert found_x

    def test_commutative_mul_match(self, match):
        """x*y should match regardless of order in Mul pattern."""
        subject = to_omnimatch_expression(x * y)
        pattern = Pattern(Operation(MUL, b_, a_))
        results = list(match(subject, pattern))
        assert len(results) >= 1


class TestManyToOneMatcher:
    """Test ManyToOneMatcher with multiple SymPy patterns simultaneously.

    Uses `match_many` fixture — runs across many-to-one, generated, json-roundtrip.
    """

    def test_identify_trig_functions(self, match_many):
        """Identify which trig function an expression uses."""
        sin_pattern = Pattern(Operation(SIN, a_))
        cos_pattern = Pattern(Operation(COS, a_))
        tan_pattern = Pattern(Operation(TAN, a_))

        # match_many gives substitutions for all matching patterns
        subject = to_omnimatch_expression(sin(x))
        results = list(match_many(subject, sin_pattern, cos_pattern, tan_pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_x

        subject = to_omnimatch_expression(cos(y))
        results = list(match_many(subject, sin_pattern, cos_pattern, tan_pattern))
        assert len(results) == 1
        assert results[0]['a'] == sw_y

    def test_identify_power_patterns(self, match_many):
        """Multiple power patterns match the right subjects."""
        square_pattern = Pattern(Operation(POW, a_, sw_2))
        cube_pattern = Pattern(Operation(POW, a_, sw_3))
        any_power = Pattern(Operation(POW, a_, n_))

        subject = to_omnimatch_expression(x ** 2)
        results = list(match_many(subject, square_pattern, cube_pattern, any_power))
        # square_pattern and any_power should both match
        assert len(results) == 2

        subject = to_omnimatch_expression(x ** 3)
        results = list(match_many(subject, square_pattern, cube_pattern, any_power))
        assert len(results) == 2


class TestTrigSimplification:
    """Test trigonometric identity simplification: sin²(x) + cos²(x) → 1."""

    def _make_trig_replacer(self):
        """Create a replacer that applies sin²(u) + cos²(u) → 1."""
        u_ = Wildcard.dot('u')
        trig_pattern = Pattern(
            Operation(ADD, Operation(POW, Operation(SIN, u_), sw_2),
                           Operation(POW, Operation(COS, u_), sw_2))
        )

        def trig_replacement(u):
            return SW(Integer(1))

        rule = omnimatch_functions.ReplacementRule(trig_pattern, trig_replacement)
        return ManyToOneReplacer(rule)

    def test_simple_identity(self):
        """sin²(x) + cos²(x) → 1"""
        replacer = self._make_trig_replacer()
        subject = to_omnimatch_expression(sin(x)**2 + cos(x)**2)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == 1

    def test_identity_with_different_arg(self):
        """sin²(2y) + cos²(2y) → 1"""
        replacer = self._make_trig_replacer()
        subject = to_omnimatch_expression(sin(2*y)**2 + cos(2*y)**2)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == 1

    def test_identity_in_larger_expression(self):
        """3 + sin²(x) + cos²(x) → 3 + 1 = 4 (when simplified)."""
        replacer = self._make_trig_replacer()
        subject = to_omnimatch_expression(3 + sin(x)**2 + cos(x)**2)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy.simplify(sympy_result - 4) == 0

    def test_no_match_different_args(self):
        """sin²(x) + cos²(y) should NOT simplify (different arguments)."""
        replacer = self._make_trig_replacer()
        subject = to_omnimatch_expression(sin(x)**2 + cos(y)**2)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        expected = sin(x)**2 + cos(y)**2
        assert sympy.simplify(sympy_result - expected) == 0


class TestDoubleAngleFormula:
    """Test double angle formula: 2*sin(x)*cos(x) → sin(2*x)."""

    def _make_double_angle_replacer(self):
        u_ = Wildcard.dot('u')
        pattern = Pattern(
            Operation(MUL, sw_2, Operation(SIN, u_), Operation(COS, u_))
        )

        def double_angle(u):
            u_sym = omnimatch_to_sympy(u)
            return to_omnimatch_expression(sin(2 * u_sym))

        rule = omnimatch_functions.ReplacementRule(pattern, double_angle)
        return ManyToOneReplacer(rule)

    def test_double_angle(self):
        """2*sin(x)*cos(x) → sin(2*x)"""
        replacer = self._make_double_angle_replacer()
        subject = to_omnimatch_expression(2 * sin(x) * cos(x))
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == sin(2*x)

    def test_double_angle_compound_arg(self):
        """2*sin(x+1)*cos(x+1) → sin(2*(x+1))"""
        replacer = self._make_double_angle_replacer()
        subject = to_omnimatch_expression(2 * sin(x + 1) * cos(x + 1))
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        expected = sin(2 * (x + 1))
        assert sympy.simplify(sympy_result - expected) == 0


class TestPowerRules:
    """Test power simplification rules using pattern matching."""

    def _make_power_replacer(self):
        a_ = Wildcard.dot('a')
        b_ = Wildcard.dot('b')
        u_ = Wildcard.dot('u')

        pattern_zero = Pattern(Operation(POW, u_, sw_0))
        def replace_zero(u):
            return SW(Integer(1))

        pattern_one = Pattern(Operation(POW, u_, sw_1))
        def replace_one(u):
            return u

        pattern_power_of_power = Pattern(
            Operation(POW, Operation(POW, u_, a_), b_)
        )
        def replace_power_of_power(u, a, b):
            a_sym = omnimatch_to_sympy(a)
            b_sym = omnimatch_to_sympy(b)
            u_sym = omnimatch_to_sympy(u)
            return to_omnimatch_expression(u_sym ** (a_sym * b_sym))

        return ManyToOneReplacer(
            omnimatch_functions.ReplacementRule(pattern_zero, replace_zero),
            omnimatch_functions.ReplacementRule(pattern_one, replace_one),
            omnimatch_functions.ReplacementRule(pattern_power_of_power, replace_power_of_power),
        )

    def test_x_to_zero(self):
        """x**0 → 1"""
        replacer = self._make_power_replacer()
        subject = Operation(POW, sw_x, sw_0)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == 1

    def test_x_to_one(self):
        """x**1 → x"""
        replacer = self._make_power_replacer()
        subject = Operation(POW, sw_x, sw_1)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == sympy.Symbol('x')

    def test_power_of_power(self):
        """(x**2)**3 → x**6"""
        replacer = self._make_power_replacer()
        subject = Operation(POW, Operation(POW, sw_x, sw_2), sw_3)
        result = replacer.replace(subject)
        sympy_result = omnimatch_to_sympy(result)
        assert sympy_result == x**6
