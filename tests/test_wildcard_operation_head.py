# -*- coding: utf-8 -*-
"""Tests for WILDCARD OPERATION HEADS.

A pattern built with :class:`WildcardOperationHead` matches an application of ANY
operation head (e.g. Rubi's ``F_[v_]``, "any function F applied to v"), binding the
matched head to a variable while its operands match in the ordinary way.
"""
import pytest

from matchpy.expressions.expressions import (
    Arity, Operation, OperationHead, Pattern, Symbol, SymbolWrapper, Wildcard,
    WildcardOperationHead,
)
from matchpy.matching.many_to_one import ManyToOneMatcher

SIN = OperationHead(name='SIN', arity=Arity.unary)
COS = OperationHead(name='COS', arity=Arity.unary)
F2 = OperationHead(name='F2', arity=Arity.binary)
ADD = OperationHead(name='ADD', arity=Arity.variadic, commutative=True,
                    associative=True, one_identity=True)
MUL = OperationHead(name='MUL', arity=Arity.variadic, commutative=True,
                    associative=True, one_identity=True)


def _match_one(pattern, subject):
    m = ManyToOneMatcher()
    m.add(pattern, label='p')
    return list(m.match(subject))


class TestWildcardOperationHead:

    def test_matches_any_head_and_binds_it(self):
        pat = Pattern(Operation(WildcardOperationHead(name='__any__', variable_name='F'),
                                Wildcard.dot('v')))
        for head in (SIN, COS):
            got = _match_one(pat, Operation(head, Symbol('x')))
            assert len(got) == 1, f"no match for {head.name}"
            _, subst = got[0]
            assert subst['F'].value is head      # head bound (wrapped)
            assert subst['v'] == Symbol('x')     # operand bound normally

    def test_operands_match_normally(self):
        """Argument wildcards bind during matching, exactly like a normal pattern."""
        pat = Pattern(Operation(WildcardOperationHead(name='__any__', variable_name='F'),
                                Operation(ADD, Wildcard.dot('a'),
                                          Operation(MUL, Wildcard.dot('b'), Symbol('x')))))
        subject = Operation(SIN, Operation(ADD, Symbol('2'),
                                           Operation(MUL, Symbol('3'), Symbol('x'))))
        got = _match_one(pat, subject)
        assert len(got) == 1
        _, subst = got[0]
        assert subst['F'].value is SIN
        assert subst['a'] == Symbol('2')
        assert subst['b'] == Symbol('3')

    def test_works_inside_commutative_operation(self):
        pat = Pattern(Operation(MUL, Wildcard.dot('u'),
                                Operation(WildcardOperationHead(name='__any__',
                                                                variable_name='G'),
                                          Wildcard.dot('v'))))
        subject = Operation(MUL, Symbol('w'), Operation(SIN, Symbol('y')))
        got = _match_one(pat, subject)
        assert len(got) == 1
        _, subst = got[0]
        assert subst['G'].value is SIN
        assert subst['v'] == Symbol('y')
        assert subst['u'] == Symbol('w')

    def test_arity_still_constrained_by_operands(self):
        """A 1-operand wildcard-head pattern must not match a 2-ary application."""
        pat = Pattern(Operation(WildcardOperationHead(name='__any__', variable_name='F'),
                                Wildcard.dot('v')))
        assert _match_one(pat, Operation(F2, Symbol('x'), Symbol('y'))) == []

    def test_does_not_match_a_plain_symbol(self):
        pat = Pattern(Operation(WildcardOperationHead(name='__any__', variable_name='F'),
                                Wildcard.dot('v')))
        assert _match_one(pat, Symbol('x')) == []

    def test_concrete_head_patterns_are_unaffected(self):
        """A normal (concrete-head) pattern must not be broadened by this feature."""
        pat = Pattern(Operation(SIN, Wildcard.dot('v')))
        assert len(_match_one(pat, Operation(SIN, Symbol('x')))) == 1
        assert _match_one(pat, Operation(COS, Symbol('x'))) == []

    def test_wildcard_head_not_equal_to_plain_head_of_same_name(self):
        assert WildcardOperationHead(name='SIN', variable_name='F') != SIN
