# -*- coding: utf-8 -*-
"""Tests for RubiConstraint integration with concrete rubi_rules constraints.

Tests that concrete constraint subclasses (FreeQ, IntegerQ, EqQ, etc.) properly
integrate with the RubiConstraint base class from sympy_objects:
- Re-export: rubi_rules.utils.constraints.RubiConstraint is the same object
- Boolean inheritance and logic composition with concrete constraints
- Argument normalisation with concrete constraints
- The SymPy invariant: constraint == constraint.func(*constraint.args)
- Hash consistency
- JSON round-trip via sympy_objects.json_ext
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
import sympy
from sympy import Symbol, Integer, Rational, Tuple
from sympy.logic.boolalg import Boolean, Not, And, Or

import sympy_objects
from sympy_objects.constraints import RubiConstraint
from sympy_objects.json_ext import serialize_wrapped_value, deserialize_wrapped_value


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _roundtrip(constraint):
    """Serialize then deserialize a constraint; return the restored object."""
    data = serialize_wrapped_value(constraint)
    return deserialize_wrapped_value(data)


# ---------------------------------------------------------------------------
# 1. Re-export identity
# ---------------------------------------------------------------------------

class TestReExport:
    def test_re_export_is_same_class(self):
        """rubi_rules.utils.constraints re-exports the identical class object."""
        from rubi_rules.utils.constraints import RubiConstraint as RC_rubi
        assert RC_rubi is RubiConstraint


# ---------------------------------------------------------------------------
# 2. Boolean inheritance with concrete constraints
# ---------------------------------------------------------------------------

class TestBooleanInheritance:
    def test_freeq_is_boolean_subclass(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ
        assert issubclass(FreeQ, Boolean)
        assert issubclass(FreeQ, RubiConstraint)

    def test_instance_is_boolean(self):
        from rubi_rules.utils.constraints_wolfram import IntegerQ
        assert isinstance(IntegerQ('n'), Boolean)

    def test_not_composition(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ
        x = Symbol('x')
        result = Not(FreeQ('a', x))
        assert isinstance(result, Boolean)

    def test_and_composition(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ, IntegerQ
        x = Symbol('x')
        result = And(FreeQ('a', x), IntegerQ('n'))
        assert isinstance(result, Boolean)

    def test_or_composition(self):
        from rubi_rules.utils.constraints_rubi import EqQ
        result = Or(EqQ('n', 0), EqQ('n', 1))
        assert isinstance(result, Boolean)


# ---------------------------------------------------------------------------
# 3. Argument normalisation with concrete constraints
# ---------------------------------------------------------------------------

class TestArgNormalisation:
    """_normalize_constraint_arg converts Python primitives to SymPy."""

    def test_str_to_symbol(self):
        from rubi_rules.utils.constraints_wolfram import IntegerQ
        c = IntegerQ('n_')   # trailing _ stripped
        assert c.args[0] == Symbol('n')

    def test_str_no_underscore(self):
        from rubi_rules.utils.constraints_wolfram import IntegerQ
        c = IntegerQ('n')
        assert c.args[0] == Symbol('n')

    def test_int_to_integer(self):
        from rubi_rules.utils.constraints_rubi import EqQ
        c = EqQ('n', 2)
        assert c.args[1] == Integer(2)

    def test_list_to_tuple(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ
        x = Symbol('x')
        c = FreeQ(['a', 'b'], x)
        assert isinstance(c.args[0], Tuple)
        assert c.args[0] == (Symbol('a'), Symbol('b'))

    def test_dict_to_sorted_tuple_of_pairs(self):
        from rubi_rules.utils.constraints_rubi import ExpressionEqQ
        c = ExpressionEqQ({'m': 1, 'p': 2}, 3, 0)
        assert isinstance(c.args[0], tuple)
        pairs = dict(c.args[0])
        assert pairs[Symbol('m')] == Integer(1)
        assert pairs[Symbol('p')] == Integer(2)

    def test_sympy_passthrough(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ
        x = Symbol('x')
        a = Symbol('a')
        c = FreeQ(a, x)
        assert c.args[0] == Symbol('a')


# ---------------------------------------------------------------------------
# 4. The SymPy invariant: constraint == constraint.func(*constraint.args)
# ---------------------------------------------------------------------------

def _make_concrete_constraints():
    from rubi_rules.utils.constraints_wolfram import (
        FreeQ, IntegerQ, OddQ, EvenQ, NumberQ, AtomQ,
        PositiveQ, NegativeQ, MemberQ,
    )
    from rubi_rules.utils.constraints_rubi import (
        EqQ, NeQ, IGtQ, ILtQ, GtQ, LtQ, ExpressionEqQ,
    )
    x = Symbol('x')
    return [
        IntegerQ('n_'),
        OddQ('n'),
        EvenQ('n'),
        NumberQ('n'),
        AtomQ('a'),
        PositiveQ('p'),
        NegativeQ('p'),
        FreeQ('a_', x),
        FreeQ(['a_', 'b_'], x),
        MemberQ('n_', [Integer(-1), Integer(1)]),
        EqQ('n_', 2),
        NeQ('n_', 0),
        IGtQ('n_', 1),
        ILtQ('n_', 0),
        GtQ('p_', 0),
        LtQ('p_', 1),
        ExpressionEqQ({'m': 1, 'p': 2}, 3, 0),
    ]


@pytest.fixture(params=_make_concrete_constraints(),
                ids=lambda c: type(c).__name__ + str(c.args))
def constraint(request):
    return request.param


class TestInvariant:
    """constraint == constraint.func(*constraint.args) for every concrete type."""

    def test_func_args_identity(self, constraint):
        reconstructed = constraint.func(*constraint.args)
        assert constraint == reconstructed, (
            f"{type(constraint).__name__}: "
            f"args={constraint.args!r}  reconstructed.args={reconstructed.args!r}"
        )

    def test_hash_consistency(self, constraint):
        reconstructed = constraint.func(*constraint.args)
        assert hash(constraint) == hash(reconstructed)

    def test_args_are_hashable(self, constraint):
        for a in constraint.args:
            hash(a)  # must not raise


# ---------------------------------------------------------------------------
# 5. JSON serialization round-trip
# ---------------------------------------------------------------------------

class TestJsonRoundtrip:
    """Every constraint must survive serialize/deserialize with equality."""

    def test_roundtrip(self, constraint):
        restored = _roundtrip(constraint)
        assert constraint == restored, (
            f"{type(constraint).__name__} roundtrip failed: "
            f"original.args={constraint.args!r}  restored.args={restored.args!r}"
        )

    def test_roundtrip_preserves_check_behaviour(self):
        from rubi_rules.utils.constraints_wolfram import IntegerQ
        c = IntegerQ('n')
        restored = _roundtrip(c)
        assert c.check(n=Integer(3)) == restored.check(n=Integer(3))
        assert c.check(n=Rational(1, 2)) == restored.check(n=Rational(1, 2))

    def test_freeq_multivar_roundtrip(self):
        from rubi_rules.utils.constraints_wolfram import FreeQ
        x = Symbol('x')
        c = FreeQ(['a', 'b'], x)
        restored = _roundtrip(c)
        assert c == restored
        assert restored.check(a=Integer(1), b=Integer(2)) is True
        assert restored.check(a=x, b=Integer(2)) is False

    def test_expression_eqq_roundtrip(self):
        from rubi_rules.utils.constraints_rubi import ExpressionEqQ
        c = ExpressionEqQ({'m': 1, 'p': 2}, 3, 0)
        restored = _roundtrip(c)
        assert c == restored
        assert restored.check(m=Integer(1), p=Integer(-2)) is True
        assert restored.check(m=Integer(0), p=Integer(0)) is False
