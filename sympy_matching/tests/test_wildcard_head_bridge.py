# -*- coding: utf-8 -*-
"""Tests for the SymPy <-> MatchPy bridge for WILDCARD OPERATION HEADS.

Three pieces are covered:

``WildHeadApp(F_, *args)``
    the SymPy-level pattern node for ``F_[args]``; converts to a MatchPy
    ``Operation`` whose head is a ``WildcardOperationHead``.

``HeadRef(func)``
    a matched function head wrapped as a substitutable SymPy Symbol (a function
    *class* is not a SymPy expression, so it cannot be substituted directly).

``matchpy_to_sympy`` / ``from_expression``
    a matched head arrives as ``SymbolWrapper(OperationHead)`` and MUST come back
    as a ``HeadRef`` -- never as the raw ``OperationHead``, which would blow up on
    the first arithmetic operation.
"""
import pytest
import sympy

from matchpy.expressions.expressions import (
    Arity, Operation, OperationHead, Pattern, SymbolWrapper, Wildcard,
    WildcardOperationHead,
)
from matchpy.matching.many_to_one import ManyToOneMatcher

from sympy_matching.conversion import matchpy_to_sympy, to_expression
from sympy_matching.operations import HEAD_TO_SYMPY_FUNC, SYMPY_FUNC_TO_HEAD
from sympy_matching.wild import HeadRef, WildHeadApp, WildSymbol

x = sympy.Symbol('x')


# =============================================================================
# WildHeadApp -- the SymPy-level pattern node
# =============================================================================

class TestWildHeadApp:

    def test_construction_and_accessors(self):
        F, v = WildSymbol('F'), WildSymbol('v')
        app = WildHeadApp(F, v)
        assert app.head_wild is F
        assert app.applied_args == (v,)

    def test_multiple_arguments(self):
        F, u, v = WildSymbol('F'), WildSymbol('u'), WildSymbol('v')
        app = WildHeadApp(F, u, v)
        assert app.applied_args == (u, v)

    def test_compound_argument_is_preserved(self):
        F, a, b = WildSymbol('F'), WildSymbol('a'), WildSymbol('b')
        app = WildHeadApp(F, a + b * x)
        assert app.applied_args == (a + b * x,)

    def test_is_a_sympy_expr_and_structurally_comparable(self):
        F, v = WildSymbol('F'), WildSymbol('v')
        assert isinstance(WildHeadApp(F, v), sympy.Basic)
        assert WildHeadApp(F, v) == WildHeadApp(F, v)


class TestWildHeadAppConversion:

    def test_converts_to_operation_with_wildcard_head(self):
        F, v = WildSymbol('F'), WildSymbol('v')
        expr = to_expression(WildHeadApp(F, v))
        assert isinstance(expr, Operation)
        assert isinstance(expr.head, WildcardOperationHead)
        assert expr.head.variable_name == 'F'
        assert len(expr.operands) == 1

    def test_head_variable_name_follows_the_wildcard(self):
        for name in ('F', 'G', 'trig'):
            expr = to_expression(WildHeadApp(WildSymbol(name), WildSymbol('v')))
            assert expr.head.variable_name == name

    def test_operands_are_converted_recursively(self):
        F, a, b = WildSymbol('F'), WildSymbol('a'), WildSymbol('b')
        expr = to_expression(WildHeadApp(F, a + b * x))
        # the single operand is the converted `a + b*x`, an ADD operation
        assert len(expr.operands) == 1
        assert isinstance(expr.operands[0], Operation)

    def test_arity_follows_the_number_of_arguments(self):
        F, u, v = WildSymbol('F'), WildSymbol('u'), WildSymbol('v')
        assert len(to_expression(WildHeadApp(F, u)).operands) == 1
        assert len(to_expression(WildHeadApp(F, u, v)).operands) == 2


# =============================================================================
# HeadRef -- a matched head, wrapped so SymPy can substitute it
# =============================================================================

class TestHeadRef:

    @pytest.mark.parametrize('func', [sympy.sin, sympy.cos, sympy.exp,
                                      sympy.atan, sympy.atanh, sympy.log])
    def test_wraps_a_function_and_exposes_it(self, func):
        ref = HeadRef(func)
        assert ref.func_class is func
        assert ref.name == func.__name__

    def test_is_a_substitutable_sympy_symbol(self):
        """The whole point: a function class is not substitutable, a HeadRef is."""
        ref = HeadRef(sympy.sin)
        assert isinstance(ref, sympy.Symbol)
        F = WildSymbol('F')
        assert (F + x).subs(F, ref) == ref + x        # substitution works
        with pytest.raises((TypeError, ValueError, AttributeError)):
            (F + x).subs(F, sympy.sin)               # the bare class does not

    def test_supports_arithmetic(self):
        """Regression: a raw OperationHead raised TypeError on `-`."""
        ref = HeadRef(sympy.sin)
        assert (ref - x).has(ref)
        assert (2 * ref).has(ref)

    def test_wraps_an_undefined_function(self):
        f = sympy.Function('f')
        assert HeadRef(f).func_class is f


# =============================================================================
# Matched head -> SymPy  (the leak this guards against)
# =============================================================================

class TestMatchedHeadConversion:

    @pytest.mark.parametrize('func', [sympy.sin, sympy.cos, sympy.exp,
                                      sympy.atan, sympy.atanh])
    def test_registered_head_becomes_a_headref(self, func):
        head = SYMPY_FUNC_TO_HEAD[func]
        got = matchpy_to_sympy(SymbolWrapper(head))
        assert isinstance(got, HeadRef)
        assert got.func_class is func

    def test_unregistered_head_degrades_to_an_undefined_function(self):
        """An unmapped head must still produce a HeadRef, never a raw OperationHead."""
        head = OperationHead(name='NotRegisteredAnywhere', arity=Arity.unary)
        assert head not in HEAD_TO_SYMPY_FUNC
        got = matchpy_to_sympy(SymbolWrapper(head))
        assert isinstance(got, HeadRef)
        assert got.name == 'NotRegisteredAnywhere'

    @pytest.mark.parametrize('head', [
        SYMPY_FUNC_TO_HEAD[sympy.sin],
        OperationHead(name='Unmapped', arity=Arity.unary),
    ])
    def test_never_returns_a_raw_operation_head(self, head):
        """The exact bug: `OperationHead - Symbol` raises TypeError."""
        got = matchpy_to_sympy(SymbolWrapper(head))
        assert not isinstance(got, OperationHead)
        got - x   # must not raise

    def test_ordinary_symbol_wrappers_are_unaffected(self):
        assert matchpy_to_sympy(SymbolWrapper(x)) is x
        assert matchpy_to_sympy(SymbolWrapper(sympy.Integer(3))) == sympy.Integer(3)


# =============================================================================
# End-to-end: SymPy pattern -> match -> SymPy head
# =============================================================================

class TestEndToEnd:

    def _match(self, sympy_pattern, sympy_subject):
        m = ManyToOneMatcher()
        m.add(Pattern(to_expression(sympy_pattern)), label='p')
        return [subst for _, subst in m.match(to_expression(sympy_subject))]

    @pytest.mark.parametrize('func', [sympy.sin, sympy.cos, sympy.atan])
    def test_wild_head_app_matches_any_function_and_returns_a_headref(self, func):
        F, v = WildSymbol('F'), WildSymbol('v')
        got = self._match(WildHeadApp(F, v), func(x))
        assert len(got) == 1
        head = matchpy_to_sympy(got[0]['F'])
        assert isinstance(head, HeadRef) and head.func_class is func
        assert matchpy_to_sympy(got[0]['v']) == x

    def test_compound_argument_wildcards_bind_during_matching(self):
        """The key advantage: argument wildcards bind natively, not post-hoc."""
        F, a, b = WildSymbol('F'), WildSymbol('a'), WildSymbol('b')
        got = self._match(WildHeadApp(F, a + b * x), sympy.sin(2 + 3 * x))
        assert len(got) == 1
        assert matchpy_to_sympy(got[0]['a']) == 2
        assert matchpy_to_sympy(got[0]['b']) == 3

    def test_does_not_match_a_non_application(self):
        F, v = WildSymbol('F'), WildSymbol('v')
        assert self._match(WildHeadApp(F, v), x) == []

    def test_matched_head_can_be_reapplied(self):
        """A recovered HeadRef re-applies to build a new application."""
        F, v = WildSymbol('F'), WildSymbol('v')
        got = self._match(WildHeadApp(F, v), sympy.sin(x))
        head = matchpy_to_sympy(got[0]['F'])
        assert head.func_class(2 * x) == sympy.sin(2 * x)
