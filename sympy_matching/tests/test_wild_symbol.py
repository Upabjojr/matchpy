# -*- coding: utf-8 -*-
"""Tests for WildSymbol, IDENTITY_ELEMENT, and optional_value behavior.

Covers:
- IDENTITY_ELEMENT in Add (default 0), Mul (default 1), Pow exponent (default 1)
- Explicit optional_value (non-IDENTITY)
- Mixed IDENTITY_ELEMENT and explicit optional_value in the same pattern
- Patterns without optional_value (plain dot wildcards)
- Optional exponent wildcards matching bare bases (x**w_ vs subject x = x**1)
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sympy
from sympy import symbols, Eq, Integer, sin, cos, Rational, simplify

from omnimatch.expressions.expressions import (
    Operation, Wildcard, Pattern, to_omnimatch_expression,
)
from omnimatch.expressions.constraints import FreeOf
from omnimatch.matching.one_to_one import match as match_one
from omnimatch.matching.many_to_one import ManyToOneMatcher

from sympy_matching.operations import ADD, MUL, POW, SIN
from sympy_matching.conversion import omnimatch_to_sympy
from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

x, y, z = symbols('x y z')


# ─── IDENTITY_ELEMENT in Add (identity = 0) ──────────────────────────────

class TestIdentityElementAdd:
    """IDENTITY_ELEMENT inside Add resolves to 0."""

    def test_add_identity_matches_bare_symbol(self):
        """Pattern: a_ + x, subject: x → a_ = 0 (Add identity)."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ + x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(0)

    def test_add_identity_matches_with_value(self):
        """Pattern: a_ + x, subject: 5 + x → a_ = 5."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ + x))
        subject = to_omnimatch_expression(5 + x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(5)

    def test_add_identity_with_symbolic(self):
        """Pattern: c_ + x, subject: y + x → c_ = y."""
        c_ = WildSymbol('c_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(c_ + x))
        subject = to_omnimatch_expression(y + x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['c']) == y


# ─── IDENTITY_ELEMENT in Mul (identity = 1) ──────────────────────────────

class TestIdentityElementMul:
    """IDENTITY_ELEMENT inside Mul resolves to 1."""

    def test_mul_identity_matches_bare_symbol(self):
        """Pattern: a_ * x, subject: x → a_ = 1 (Mul identity)."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ * x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(1)

    def test_mul_identity_matches_with_coefficient(self):
        """Pattern: a_ * x, subject: 3*x → a_ = 3."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ * x))
        subject = to_omnimatch_expression(3 * x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(3)

    def test_mul_identity_with_symbolic(self):
        """Pattern: k_ * x, subject: y*x → k_ = y."""
        k_ = WildSymbol('k_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(k_ * x))
        subject = to_omnimatch_expression(y * x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['k']) == y


# ─── IDENTITY_ELEMENT in Pow exponent (identity = 1) ────────────────────

class TestIdentityElementPow:
    """IDENTITY_ELEMENT in the exponent of Pow resolves to 1.

    x**w_ with subject x means w_ = 1 (since x = x**1).
    """

    def test_pow_identity_matches_with_exponent(self):
        """Pattern: x**w_, subject: x**3 → w_ = 3."""
        w_ = WildSymbol('w_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(x**w_))
        subject = to_omnimatch_expression(x**3)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['w']) == Integer(3)

    def test_pow_identity_symbolic_exponent(self):
        """Pattern: x**n_, subject: x**y → n_ = y."""
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(x**n_))
        subject = to_omnimatch_expression(x**y)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['n']) == y

    def test_pow_identity_rational_exponent(self):
        """Pattern: x**n_, subject: x**(1/2) = sqrt(x) → n_ = 1/2."""
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(x**n_))
        subject = to_omnimatch_expression(x**Rational(1, 2))
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['n']) == Rational(1, 2)

    def test_pow_identity_combined_with_coefficient(self):
        """Pattern: a_*x**n_, subject: 5*x**3 → a_=5, n_=3."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ * x**n_))
        subject = to_omnimatch_expression(5 * x**3)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(5)
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(3)


# ─── Explicit optional_value (non-IDENTITY) ──────────────────────────────

class TestExplicitOptionalValue:
    """WildSymbol with a concrete optional_value (not IDENTITY_ELEMENT)."""

    def test_explicit_zero_in_mul(self):
        """Pattern: b_*x with b_ defaulting to 0.
        Subject: x → b_ = 0 (explicit default, NOT identity)."""
        b_ = WildSymbol('b_', optional_value=0)
        pattern = Pattern(to_omnimatch_expression(b_ * x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['b']) == Integer(0)

    def test_explicit_two_in_add(self):
        """Pattern: c_ + x with c_ defaulting to 2.
        Subject: x → c_ = 2 (explicit, not identity)."""
        c_ = WildSymbol('c_', optional_value=2)
        pattern = Pattern(to_omnimatch_expression(c_ + x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['c']) == Integer(2)

    def test_explicit_value_matches_present_operand(self):
        """When the subject HAS the operand, use that — not the default.
        Pattern: c_ + x with default 2; subject: 7 + x → c_ = 7."""
        c_ = WildSymbol('c_', optional_value=2)
        pattern = Pattern(to_omnimatch_expression(c_ + x))
        subject = to_omnimatch_expression(7 + x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['c']) == Integer(7)

    def test_explicit_half_in_pow_exponent(self):
        """Pattern: x**n_ with n_ defaulting to 1/2.
        Subject: x**3 → n_ = 3 (default not used; wildcard matches subject)."""
        n_ = WildSymbol('n_', optional_value=Rational(1, 2))
        pattern = Pattern(to_omnimatch_expression(x**n_))
        subject = to_omnimatch_expression(x**3)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(3)

    def test_explicit_negative_one_in_mul(self):
        """Pattern: s_*x with s_ defaulting to -1.
        Subject: x → s_ = -1."""
        s_ = WildSymbol('s_', optional_value=-1)
        pattern = Pattern(to_omnimatch_expression(s_ * x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['s']) == Integer(-1)


# ─── Mixed IDENTITY_ELEMENT and explicit optional_value ───────────────────

class TestMixedOptionalValues:
    """Patterns combining IDENTITY_ELEMENT and explicit optional_value."""

    def test_identity_coeff_explicit_constant(self):
        """Pattern: a_*x + b_ where a_ uses IDENTITY (1 in Mul) and b_ uses explicit 0.
        Subject: x → a_=1, b_=0."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=0)
        pattern = Pattern(to_omnimatch_expression(a_ * x + b_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(1)
        assert omnimatch_to_sympy(matches[0]['b']) == Integer(0)

    def test_identity_coeff_explicit_constant_with_subject(self):
        """Pattern: a_*x + b_ where a_ uses IDENTITY, b_ uses explicit 0.
        Subject: 3*x + 7 → a_=3, b_=7."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=0)
        pattern = Pattern(to_omnimatch_expression(a_ * x + b_))
        subject = to_omnimatch_expression(3 * x + 7)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(3)
        assert omnimatch_to_sympy(matches[0]['b']) == Integer(7)

    def test_identity_exponent_explicit_coeff(self):
        """Pattern: c_*x**n_ where c_ defaults to 5 (explicit), n_ uses IDENTITY.
        Subject: x**2 → c_=5 (from MUL one_identity), n_=2."""
        c_ = WildSymbol('c_', optional_value=5)
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(c_ * x**n_))
        subject = to_omnimatch_expression(x**2)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['c']) == Integer(5)
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(2)

    def test_all_identity_monomial(self):
        """Pattern: a_*x**n_ + b_ with all IDENTITY.
        Subject: x**2 (= 1*x**2 + 0) → a_=1, n_=2, b_=0."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ * x**n_ + b_))
        subject = to_omnimatch_expression(x**2)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(1)
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(2)
        assert omnimatch_to_sympy(matches[0]['b']) == Integer(0)

    def test_all_identity_monomial_with_values(self):
        """Pattern: a_*x**n_ + b_ with all IDENTITY.
        Subject: 2*x**3 + 7 → a_=2, n_=3, b_=7."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(a_ * x**n_ + b_))
        subject = to_omnimatch_expression(2 * x**3 + 7)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(2)
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(3)
        assert omnimatch_to_sympy(matches[0]['b']) == Integer(7)

    def test_mixed_with_freeq_constraint(self):
        """Pattern: a_*x**n_ + b_ with FreeOf on a_ and b_.
        Subject: y*x**2 + z → a_=y, n_=2, b_=z (all free of x)."""
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        n_ = WildSymbol('n_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(
            to_omnimatch_expression(a_ * x**n_ + b_),
            FreeOf('a', 'x'), FreeOf('b', 'x'),
        )
        subject = to_omnimatch_expression(y * x**2 + z)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == y
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(2)
        assert omnimatch_to_sympy(matches[0]['b']) == z


# ─── No optional_value (plain dot wildcards) ─────────────────────────────

class TestPlainWildSymbol:
    """WildSymbol without optional_value becomes a mandatory dot wildcard."""

    def test_plain_must_match_something(self):
        """Pattern: a_*x with a_ mandatory. Subject: x alone does NOT match
        because the MUL needs 2 operands and a_ has no default."""
        a_ = WildSymbol('a_')
        pattern = Pattern(to_omnimatch_expression(a_ * x))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        # No match: a_ is required and MUL pattern needs explicit coefficient
        assert len(matches) == 0

    def test_plain_matches_when_present(self):
        """Pattern: a_*x, subject: 3*x → a_ = 3."""
        a_ = WildSymbol('a_')
        pattern = Pattern(to_omnimatch_expression(a_ * x))
        subject = to_omnimatch_expression(3 * x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['a']) == Integer(3)

    def test_plain_in_pow_exponent(self):
        """Pattern: x**n_ (mandatory), subject: x**5 → n_ = 5."""
        n_ = WildSymbol('n_')
        pattern = Pattern(to_omnimatch_expression(x**n_))
        subject = to_omnimatch_expression(x**5)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['n']) == Integer(5)

    def test_plain_pow_does_not_match_bare_base(self):
        """Pattern: x**n_ (mandatory), subject: x → no match (no exponent)."""
        n_ = WildSymbol('n_')
        pattern = Pattern(to_omnimatch_expression(x**n_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 0


# ─── Optional exponent matching bare base (x**w_ vs subject x) ───────────
#
# SymPy normalises x**1 to x, so the subject `x` carries no explicit exponent.
# With POW having one_identity=True, OmniMatch treats SymbolWrapper(x) as the
# 1-operand POW(x) during matching.  An optional exponent wildcard (default 1)
# then fires and yields w_=1.  A mandatory wildcard still requires a second
# operand and produces no match.

class TestPowOptionalMatchesBareBase:
    """x**w_ with an optional exponent wildcard should match bare x (= x**1)."""

    def test_identity_element_matches_bare_base(self):
        """Pattern: x**w_ with optional_value=IDENTITY_ELEMENT, subject: x → w_=1.

        This is the key case for Rubi Rule 2: Int(x**m_, x) must match Int(x, x)
        when m_ carries optional_value=IDENTITY_ELEMENT.
        """
        w_ = WildSymbol('w_', optional_value=IDENTITY_ELEMENT)
        pattern = Pattern(to_omnimatch_expression(x**w_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1, "Expected one match; got none"
        assert omnimatch_to_sympy(matches[0]['w']) == Integer(1)

    def test_explicit_one_matches_bare_base(self):
        """Pattern: x**w_ with optional_value=Integer(1), subject: x → w_=1.

        An explicit default of 1 is equivalent to IDENTITY_ELEMENT for Pow.
        """
        w_ = WildSymbol('w_', optional_value=Integer(1))
        pattern = Pattern(to_omnimatch_expression(x**w_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 1, "Expected one match; got none"
        assert omnimatch_to_sympy(matches[0]['w']) == Integer(1)

    def test_no_optional_does_not_match_bare_base(self):
        """Pattern: x**w_ with NO optional_value, subject: x → no match.

        Without optional_value the wildcard is mandatory, so bare x (which has
        no explicit exponent node) does not match.
        """
        w_ = WildSymbol('w_')   # no optional_value
        pattern = Pattern(to_omnimatch_expression(x**w_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        assert len(matches) == 0, "Mandatory wildcard must not match bare base"

    def test_different_optional_does_not_yield_one(self):
        """Pattern: x**w_ with optional_value=Integer(2), subject: x → w_=2 (not 1).

        A default of 2 fires correctly when the subject is bare x, but the
        matched value is the declared default (2), not the Pow identity (1).
        This verifies that only optional_value=1 / IDENTITY_ELEMENT produces
        the mathematically correct exponent for bare-base matching.
        """
        w_ = WildSymbol('w_', optional_value=Integer(2))
        pattern = Pattern(to_omnimatch_expression(x**w_))
        subject = to_omnimatch_expression(x)
        matches = list(match_one(subject, pattern))
        # There IS a match, but w_ takes the declared default 2, not 1.
        assert len(matches) == 1
        assert omnimatch_to_sympy(matches[0]['w']) == Integer(2)
        assert omnimatch_to_sympy(matches[0]['w']) != Integer(1)
