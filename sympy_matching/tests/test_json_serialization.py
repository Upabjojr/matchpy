# -*- coding: utf-8 -*-
"""Tests for JSON serialization roundtrip of SymPy-based patterns and matchers."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
import sympy
from sympy import symbols, sin, cos, tan, exp, log, Integer, Rational, Eq, pi, E, I, oo

from omnimatch.expressions.expressions import (
    Operation, NamedAtom, SymbolWrapper, Wildcard, Pattern, to_omnimatch_expression,
)
from omnimatch.matching.many_to_one import ManyToOneMatcher
from omnimatch.matching.json_serialization import to_json, from_json

import sympy_matching  # registers conversion + json_ext handlers
from sympy_matching.operations import ADD, MUL, POW, SIN, COS, TAN, EXP, LOG, EQUALITY


x, y, z = symbols('x y z')

SW = SymbolWrapper
sw_x = SW(sympy.Symbol('x'))
sw_y = SW(sympy.Symbol('y'))
sw_0 = SW(Integer(0))
sw_1 = SW(Integer(1))
sw_2 = SW(Integer(2))
sw_3 = SW(Integer(3))

a_ = Wildcard.dot('a')
b_ = Wildcard.dot('b')
u_ = Wildcard.dot('u')
n_ = Wildcard.dot('n')


class TestSymbolWrapperSerialization:
    """Test that individual SymbolWrapper values roundtrip correctly."""

    @pytest.mark.parametrize('sympy_val', [
        sympy.Integer(0),
        sympy.Integer(1),
        sympy.Integer(-42),
        sympy.Integer(99999),
        sympy.Rational(1, 2),
        sympy.Rational(-3, 7),
        sympy.Float(3.14159),
        sympy.Symbol('x'),
        sympy.Symbol('hello_world'),
        sympy.pi,
        sympy.E,
        sympy.I,
        sympy.oo,
        -sympy.oo,
        sympy.zoo,
        sympy.nan,
    ])
    def test_symbol_wrapper_roundtrip(self, sympy_val):
        """SymbolWrapper containing various SymPy objects survives JSON roundtrip."""
        pattern = Pattern(Operation(SIN, SW(sympy_val)))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        # Verify the inner expression reconstructed correctly
        pat2 = matcher2.patterns[0][0]
        inner = pat2.expression.operands[0]
        assert isinstance(inner, SymbolWrapper)
        assert inner.value == sympy_val


class TestMatcherRoundtrip:
    """Test full ManyToOneMatcher JSON roundtrip with SymPy patterns."""

    def test_sin_pattern(self):
        """sin(a) pattern matches after JSON roundtrip."""
        pattern = Pattern(Operation(SIN, a_))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(sin(x))
        results = list(matcher2.match(subject))
        assert len(results) == 1
        _, subst = results[0]
        assert subst['a'] == sw_x

    def test_power_pattern(self):
        """x**3 matches pow(a, n) pattern after JSON roundtrip."""
        pattern = Pattern(Operation(POW, a_, n_))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(x ** 3)
        results = list(matcher2.match(subject))
        assert len(results) == 1
        _, subst = results[0]
        assert subst['a'] == sw_x
        assert subst['n'] == sw_3

    def test_sin_squared_pattern(self):
        """sin(u)**2 pattern matches after roundtrip."""
        pattern = Pattern(Operation(POW, Operation(SIN, u_), sw_2))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(sin(x) ** 2)
        results = list(matcher2.match(subject))
        assert len(results) == 1
        _, subst = results[0]
        assert subst['u'] == sw_x

    def test_multiple_patterns(self):
        """Multiple trig patterns all match correctly after roundtrip."""
        sin_pat = Pattern(Operation(SIN, a_))
        cos_pat = Pattern(Operation(COS, a_))
        tan_pat = Pattern(Operation(TAN, a_))

        matcher = ManyToOneMatcher(sin_pat, cos_pat, tan_pat)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        # sin(x) should match sin pattern
        results = list(matcher2.match(to_omnimatch_expression(sin(x))))
        labels = [p for p, _ in results]
        assert sin_pat in labels
        assert cos_pat not in labels

        # cos(y) should match cos pattern
        results = list(matcher2.match(to_omnimatch_expression(cos(y))))
        labels = [p for p, _ in results]
        assert cos_pat in labels
        assert sin_pat not in labels

    def test_commutative_add_pattern(self):
        """Commutative Add pattern matches after roundtrip."""
        rest_ = Wildcard(0, False, variable_name='rest')
        pattern = Pattern(Operation(ADD, Operation(POW, Operation(SIN, u_), sw_2), rest_))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(sin(x) ** 2 + cos(x) ** 2)
        results = list(matcher2.match(subject))
        assert len(results) >= 1
        found_x = any(subst.get('u') == sw_x for _, subst in results)
        assert found_x

    def test_equation_pattern(self):
        """Eq(expr, 0) pattern matches after roundtrip."""
        pattern = Pattern(Operation(EQUALITY, a_, sw_0))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(Eq(x ** 2 - 1, 0))
        results = list(matcher2.match(subject))
        assert len(results) == 1

    def test_sympy_constants_in_pattern(self):
        """Patterns using pi, E survive roundtrip."""
        # pi * a
        pattern = Pattern(Operation(MUL, SW(sympy.pi), a_))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(sympy.pi * x)
        results = list(matcher2.match(subject))
        assert len(results) == 1
        _, subst = results[0]
        assert subst['a'] == sw_x

    def test_rational_in_pattern(self):
        """Patterns using Rational numbers survive roundtrip."""
        half = SW(Rational(1, 2))
        pattern = Pattern(Operation(MUL, half, a_))
        matcher = ManyToOneMatcher(pattern)

        json_str = to_json(matcher)
        matcher2 = from_json(json_str)

        subject = to_omnimatch_expression(Rational(1, 2) * x)
        results = list(matcher2.match(subject))
        assert len(results) == 1
        _, subst = results[0]
        assert subst['a'] == sw_x
