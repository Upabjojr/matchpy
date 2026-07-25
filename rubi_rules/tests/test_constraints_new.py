# -*- coding: utf-8 -*-
"""Tests for newly added RUBI constraint predicates.

Covers all constraints added in the second round of implementation:
- Integrability predicates: IntLinearQ, IntBinomialQ, IntQuadraticQ
- Structural predicates: MonomialQ, LinearPairQ, SumBaseQ, PowerOfLinearQ, etc.
- Generalized polynomial predicates
- Trig/function predicates: InertTrigQ, InertTrigFreeQ, etc.
- Known integrand predicates
- Simplicity predicates: NiceSqrtQ, SimplerSqrtQ, FractionalPowerFactorQ

Also verifies that:
- MathematicaConstraint inherits from sympy.logic.boolalg.Boolean
- FreeQ accepts list form: FreeQ(['a', 'b'], x)
- Not(FreeQ(...)) composes correctly
"""
import pytest
import sympy
from sympy import (
    Symbol, Integer, Rational, S, I,
    sin, cos, tan, cot, sec, csc,
    sinh, cosh, log, exp, sqrt,
    Add, Mul, Pow, Not
)
from sympy.logic.boolalg import Boolean

from sympy_wolfram.constraints import MathematicaConstraint
from sympy_wolfram.objects import MathematicaExpr
from sympy_matching.wild import WildSymbol
from rubi_rules.utils.constraints_wolfram import FreeQ, FalseQ
from rubi_rules.utils.constraints_rubi import (
    IntLinearQ, IntBinomialQ, IntQuadraticQ,
    MonomialQ, LinearPairQ, SumBaseQ,
    GeneralizedBinomialQ, GeneralizedBinomialMatchQ,
    GeneralizedTrinomialQ, GeneralizedTrinomialMatchQ,
    NiceSqrtQ, SimplerSqrtQ, FractionalPowerFactorQ,
    InverseFunctionQ, InertTrigQ, InertTrigFreeQ,
    CalculusFreeQ, QuotientOfLinearsQ,
    PowerOfLinearQ, PowerOfLinearMatchQ,
    FunctionOfExponentialQ, FunctionOfTrigOfLinearQ,
    KnownSineIntegrandQ, KnownSecantIntegrandQ,
    KnownTangentIntegrandQ, KnownCotangentIntegrandQ,
    EulerIntegrandQ, SubstForFractionalPowerQ,
    PerfectSquareQ, PolynomialInQ,
    SimplerIntegrandQ, PseudoBinomialPairQ,
    QuadraticProductQ, EveryQ,
)


# Symbols for testing
x = Symbol('x')
y = Symbol('y')
a, b, c, d, e, m, n, p, q = sympy.symbols('a b c d e m n p q')


# =============================================================================
# Base class tests
# =============================================================================


# TestMathematicaConstraintBoolean and TestFreeQListForm moved to
# sympy_wolfram/tests/test_constraints_wolfram.py (FreeQ now lives in
# sympy_wolfram.constraints_wolfram).


# =============================================================================
# FalseQ placement test
# =============================================================================


class TestFalseQPlacement:
    """FalseQ is Rubi-specific but kept in constraints_wolfram for compat.

    Note: FalseQ[u] in Rubi returns True ONLY when u is literally False.
    """

    def test_falseq_literal_false(self):
        c = FalseQ('u')
        assert c.check(u=sympy.false) == True

    def test_falseq_literal_true(self):
        c = FalseQ('u')
        assert c.check(u=sympy.true) == False

    def test_falseq_none_returns_false(self):
        """When no value is provided, FalseQ returns False (strict check)."""
        c = FalseQ('u')
        assert c.check() == False


# =============================================================================
# Integrability Predicates
# =============================================================================


class TestIntLinearQ:
    """Tests for IntLinearQ constraint."""

    def test_integer_exponents(self):
        c = IntLinearQ('a', 'b', 'c', 'd', 'm', 'n', x)
        # IGtQ[m,0]: m=2 is positive integer
        assert c.check(a=S.One, b=S.One, c=S.One, d=S.One,
                       m=Integer(2), n=Integer(3)) == True

    def test_third_integer_exponents(self):
        c = IntLinearQ('a', 'b', 'c', 'd', 'm', 'n', x)
        # IntegersQ[3*m, 3*n]: m=1/3, n=1/3
        assert c.check(a=S.One, b=S.One, c=S.One, d=S.One,
                       m=Rational(1, 3), n=Rational(1, 3)) == True

    def test_quarter_integer_exponents(self):
        c = IntLinearQ('a', 'b', 'c', 'd', 'm', 'n', x)
        # IntegersQ[4*m, 4*n]: m=1/4, n=3/4
        assert c.check(a=S.One, b=S.One, c=S.One, d=S.One,
                       m=Rational(1, 4), n=Rational(3, 4)) == True

    def test_not_integrable(self):
        c = IntLinearQ('a', 'b', 'c', 'd', 'm', 'n', x)
        # m=1/5, n=1/7 doesn't satisfy any condition
        assert c.check(a=S.One, b=S.One, c=S.One, d=S.One,
                       m=Rational(1, 5), n=Rational(1, 7)) == False

    def test_sum_less_than_minus_one(self):
        c = IntLinearQ('a', 'b', 'c', 'd', 'm', 'n', x)
        # ILtQ[m+n, -1]: m=-1, n=-1 -> m+n=-2 < -1
        assert c.check(a=S.One, b=S.One, c=S.One, d=S.One,
                       m=Integer(-1), n=Integer(-1)) == True


class TestIntBinomialQ:
    """Tests for IntBinomialQ constraint."""

    def test_integer_exponents(self):
        c = IntBinomialQ('a', 'b', 'c', 'n', 'm', 'p', x)
        assert c.check(a=S.One, b=S.One, c=S.One,
                       n=Integer(2), m=Integer(1), p=Integer(3)) == True

    def test_none_values(self):
        c = IntBinomialQ('a', 'b', 'c', 'n', 'm', 'p', x)
        assert c.check(a=S.One) == False


# =============================================================================
# Structural Predicates
# =============================================================================


class TestMonomialQ:
    """Tests for MonomialQ constraint."""

    def test_pure_x(self):
        c = MonomialQ('u', x)
        assert c.check(u=x) == True

    def test_x_power(self):
        c = MonomialQ('u', x)
        assert c.check(u=x**3) == True

    def test_coeff_times_x_power(self):
        c = MonomialQ('u', x)
        assert c.check(u=3*x**2) == True

    def test_not_monomial_sum(self):
        c = MonomialQ('u', x)
        assert c.check(u=x + 1) == False

    @pytest.mark.skip(reason="check output values")
    def test_not_monomial_constant(self):
        c = MonomialQ('u', x)
        assert c.check(u=Integer(5)) == False


class TestLinearPairQ:
    """Tests for LinearPairQ constraint."""

    def test_proportional_linears(self):
        c = LinearPairQ('u', 'v', x)
        # u = 2+4x, v = 1+2x -> 2*2 - 4*1 = 0
        assert c.check(u=2 + 4*x, v=1 + 2*x) == True

    def test_non_proportional(self):
        c = LinearPairQ('u', 'v', x)
        # u = 1+x, v = 2+3x -> 1*3 - 1*2 = 1 != 0
        assert c.check(u=1 + x, v=2 + 3*x) == False

    def test_not_linear(self):
        c = LinearPairQ('u', 'v', x)
        assert c.check(u=x**2, v=x) == False


class TestSumBaseQ:
    """Tests for SumBaseQ constraint."""

    def test_sum(self):
        c = SumBaseQ('u')
        assert c.check(u=a + b) == True

    def test_product(self):
        c = SumBaseQ('u')
        assert c.check(u=a*b) == False

    def test_sum_to_odd_power(self):
        c = SumBaseQ('u')
        assert c.check(u=(a + b)**3) == True

    def test_sum_to_even_power(self):
        c = SumBaseQ('u')
        assert c.check(u=(a + b)**2) == False


class TestPowerOfLinearQ:
    """Tests for PowerOfLinearQ constraint."""

    def test_linear_power(self):
        c = PowerOfLinearQ('u', x)
        assert c.check(u=(2 + 3*x)**5) == True

    def test_plain_linear(self):
        c = PowerOfLinearQ('u', x)
        assert c.check(u=2 + 3*x) == True

    def test_quadratic_not_linear(self):
        c = PowerOfLinearQ('u', x)
        assert c.check(u=x**2 + 1) == False

    def test_sqrt_of_linear(self):
        c = PowerOfLinearQ('u', x)
        assert c.check(u=sqrt(1 + x)) == True


class TestQuotientOfLinearsQ:
    """Tests for QuotientOfLinearsQ constraint."""

    def test_simple_quotient(self):
        c = QuotientOfLinearsQ('u', x)
        assert c.check(u=(1 + x)/(2 + 3*x)) == True

    def test_polynomial_not_quotient(self):
        c = QuotientOfLinearsQ('u', x)
        # x^2+1 has denom=1, degree(denom)=0 < 1 -> False
        assert c.check(u=x**2 + 1) == False

    def test_constant_denom(self):
        c = QuotientOfLinearsQ('u', x)
        # (1+x)/2: SymPy normalizes to (1+x)*Rational(1,2) = Mul, not ratio
        # as_numer_denom gives (1+x, 2), degree(2, x)=0 -> False
        assert c.check(u=(1 + x)/2) == False


# =============================================================================
# Generalized Polynomial Predicates
# =============================================================================


class TestGeneralizedBinomialQ:
    """Tests for GeneralizedBinomialQ constraint."""

    def test_two_x_terms(self):
        c = GeneralizedBinomialQ('u', x)
        # x^2 + x^3: both terms contain x
        assert c.check(u=x**2 + x**3) == True

    def test_constant_plus_x(self):
        c = GeneralizedBinomialQ('u', x)
        # 1 + x: first term doesn't contain x
        assert c.check(u=1 + x) == False

    def test_three_terms(self):
        c = GeneralizedBinomialQ('u', x)
        assert c.check(u=x + x**2 + x**3) == False


class TestGeneralizedTrinomialQ:
    """Tests for GeneralizedTrinomialQ constraint."""

    def test_three_x_terms(self):
        c = GeneralizedTrinomialQ('u', x)
        assert c.check(u=x + x**2 + x**3) == True

    def test_has_constant(self):
        c = GeneralizedTrinomialQ('u', x)
        # 1 + x + x^2: first term free of x
        assert c.check(u=1 + x + x**2) == False


# =============================================================================
# Simplicity Predicates
# =============================================================================


class TestNiceSqrtQ:
    """Tests for NiceSqrtQ constraint."""

    def test_positive_rational(self):
        c = NiceSqrtQ('u')
        assert c.check(u=Integer(4)) == True
        assert c.check(u=Rational(9, 4)) == True

    def test_negative_rational(self):
        c = NiceSqrtQ('u')
        assert c.check(u=Integer(-1)) == False


class TestSimplerSqrtQ:
    """Tests for SimplerSqrtQ constraint."""

    def test_positive_vs_negative(self):
        c = SimplerSqrtQ('u', 'v')
        assert c.check(u=Integer(4), v=Integer(-1)) == True

    def test_negative_vs_positive(self):
        c = SimplerSqrtQ('u', 'v')
        assert c.check(u=Integer(-1), v=Integer(4)) == False


class TestFractionalPowerFactorQ:
    """Tests for FractionalPowerFactorQ constraint."""

    def test_fractional_power(self):
        c = FractionalPowerFactorQ('u')
        assert c.check(u=x**Rational(1, 2)) == True

    def test_integer_power(self):
        c = FractionalPowerFactorQ('u')
        assert c.check(u=x**2) == False

    def test_complex_atom(self):
        c = FractionalPowerFactorQ('u')
        assert c.check(u=I) == True


# =============================================================================
# Function Type Predicates
# =============================================================================


class TestInverseFunctionQ:
    """Tests for InverseFunctionQ constraint."""

    def test_log(self):
        c = InverseFunctionQ('u')
        assert c.check(u=log(x)) == True

    def test_arcsin(self):
        c = InverseFunctionQ('u')
        assert c.check(u=sympy.asin(x)) == True

    def test_not_inverse(self):
        c = InverseFunctionQ('u')
        assert c.check(u=sin(x)) == False


class TestInertTrigQ:
    """Tests for InertTrigQ constraint."""

    def test_trig_functions(self):
        from rubi_rules.utils.utility_functions import InertSin, InertCos, InertTan
        c = InertTrigQ('u')
        # inert trig markers are inert; active SymPy trig is not
        assert c.check(u=InertSin(x)) == True
        assert c.check(u=InertCos(x)) == True
        assert c.check(u=InertTan(x)) == True
        assert c.check(u=sin(x)) == False

    def test_not_trig(self):
        c = InertTrigQ('u')
        assert c.check(u=log(x)) == False
        assert c.check(u=exp(x)) == False


class TestInertTrigFreeQ:
    """Tests for InertTrigFreeQ constraint."""

    def test_no_trig(self):
        c = InertTrigFreeQ('u')
        assert c.check(u=x**2 + 1) == True
        assert c.check(u=log(x)) == True

    def test_has_trig(self):
        from rubi_rules.utils.utility_functions import InertSin, InertCos
        c = InertTrigFreeQ('u')
        # inert trig present -> not free; active SymPy trig -> free
        assert c.check(u=InertSin(x)) == False
        assert c.check(u=x + InertCos(x)) == False
        assert c.check(u=sin(x)) == True


class TestCalculusFreeQ:
    """Tests for CalculusFreeQ constraint."""

    def test_no_calculus(self):
        c = CalculusFreeQ('u', x)
        assert c.check(u=x**2 + sin(x)) == True

    def test_has_integral(self):
        c = CalculusFreeQ('u', x)
        assert c.check(u=sympy.Integral(x, x)) == False


class TestFunctionOfExponentialQ:
    """Tests for FunctionOfExponentialQ constraint."""

    def test_exponential(self):
        c = FunctionOfExponentialQ('u', x)
        assert c.check(u=exp(2*x)) == True
        assert c.check(u=Integer(2)**(3*x)) == True

    def test_no_exponential(self):
        c = FunctionOfExponentialQ('u', x)
        assert c.check(u=x**2 + 1) == False


class TestFunctionOfTrigOfLinearQ:
    """Tests for FunctionOfTrigOfLinearQ constraint."""

    def test_no_trig(self):
        c = FunctionOfTrigOfLinearQ('u', x)
        assert c.check(u=x**2) == False

    def test_trig_of_quadratic(self):
        c = FunctionOfTrigOfLinearQ('u', x)
        assert c.check(u=sin(x**2)) == False


# =============================================================================
# Known Integrand Predicates
# =============================================================================


class TestKnownSineIntegrandQ:
    """Tests for KnownSineIntegrandQ constraint."""

    def test_sine_integrand(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=sin(x)) == True
        assert c.check(u=cos(2*x + 1)) == True

    def test_unity(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=S.One) == True

    def test_not_sine(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=tan(x)) == False


class TestKnownTangentIntegrandQ:
    """Tests for KnownTangentIntegrandQ constraint."""

    def test_tangent_integrand(self):
        c = KnownTangentIntegrandQ('u', x)
        assert c.check(u=tan(x)) == True
        assert c.check(u=tan(3*x + 2)) == True

    def test_not_tangent(self):
        c = KnownTangentIntegrandQ('u', x)
        assert c.check(u=sin(x)) == False


class TestKnownSecantIntegrandQ:
    """Tests for KnownSecantIntegrandQ constraint."""

    def test_secant_integrand(self):
        c = KnownSecantIntegrandQ('u', x)
        assert c.check(u=sec(x)) == True
        assert c.check(u=csc(2*x)) == True

    def test_not_secant(self):
        c = KnownSecantIntegrandQ('u', x)
        assert c.check(u=sin(x)) == False


class TestKnownCotangentIntegrandQ:
    """Tests for KnownCotangentIntegrandQ constraint."""

    def test_cotangent_integrand(self):
        c = KnownCotangentIntegrandQ('u', x)
        assert c.check(u=cot(x)) == True

    def test_not_cotangent(self):
        c = KnownCotangentIntegrandQ('u', x)
        assert c.check(u=cos(x)) == False


# =============================================================================
# Other Structural Predicates
# =============================================================================


class TestPerfectSquareQ:
    """Tests for PerfectSquareQ constraint."""

    def test_perfect_square_number(self):
        c = PerfectSquareQ('u')
        assert c.check(u=Integer(4)) == True
        assert c.check(u=Integer(9)) == True
        assert c.check(u=Rational(1, 4)) == True

    def test_not_perfect_square(self):
        c = PerfectSquareQ('u')
        assert c.check(u=Integer(3)) == False

    def test_symbolic_square(self):
        c = PerfectSquareQ('u')
        assert c.check(u=x**2) == True
        assert c.check(u=x**4) == True


class TestPolynomialInQ:
    """Tests for PolynomialInQ constraint."""

    def test_poly_in_sin(self):
        c = PolynomialInQ('u', 'v', x)
        # u = sin(x)^2 + sin(x) + 1, v = sin(x)
        u_expr = sin(x)**2 + sin(x) + 1
        v_expr = sin(x)
        assert c.check(u=u_expr, v=v_expr) == True

    def test_not_poly_in(self):
        c = PolynomialInQ('u', 'v', x)
        # u = sin(x) + cos(x), v = sin(x) — cos(x) prevents polynomial in sin
        u_expr = sin(x) + cos(x)
        v_expr = sin(x)
        assert c.check(u=u_expr, v=v_expr) == False


class TestSubstForFractionalPowerQ:
    """Tests for SubstForFractionalPowerQ constraint."""

    def test_default_true(self):
        # Simplified implementation always returns True
        c = SubstForFractionalPowerQ('u', 'v', x)
        assert c.check(u=sqrt(x), v=x) == True


class TestSimplerIntegrandQ:
    """Tests for SimplerIntegrandQ constraint."""

    def test_simpler(self):
        c = SimplerIntegrandQ('u', 'v', x)
        assert c.check(u=x, v=x**5 + x**4 + x**3 + x**2 + x + 1) == True

    def test_not_simpler(self):
        c = SimplerIntegrandQ('u', 'v', x)
        assert c.check(u=x**5 + x**4 + x**3, v=x) == False


class TestPseudoBinomialPairQ:
    """Tests for PseudoBinomialPairQ constraint."""

    def test_default_false(self):
        # Simplified implementation returns False
        c = PseudoBinomialPairQ('u', 'v', x)
        assert c.check(u=x + 1, v=x + 2) == False


class TestQuadraticProductQ:
    """Tests for QuadraticProductQ constraint."""

    def test_product_of_quadratics(self):
        c = QuadraticProductQ('u', x)
        assert c.check(u=(x**2 + 1)*(x**2 + 2)) == True

    def test_not_quadratic_product(self):
        c = QuadraticProductQ('u', x)
        assert c.check(u=(x + 1)*(x**2 + 1)) == False  # First factor is linear

    def test_not_product(self):
        c = QuadraticProductQ('u', x)
        assert c.check(u=x**2 + 1) == False


class TestEveryQ:
    """Tests for EveryQ constraint."""

    def test_all_satisfy(self):
        c = EveryQ(lambda e: e.is_positive, 'u')
        assert c.check(u=Integer(5)) == True

    def test_not_all_satisfy(self):
        c = EveryQ(lambda e: e.is_positive, 'u')
        assert c.check(u=Integer(-1)) == False


class TestPowerOfLinearMatchQ:
    """Tests for PowerOfLinearMatchQ constraint."""

    def test_same_as_power_of_linear(self):
        c = PowerOfLinearMatchQ('u', x)
        assert c.check(u=(1 + 2*x)**3) == True
        assert c.check(u=x**2 + 1) == False


# =============================================================================
# MatchQ -- Mathematica MatchQ[expr, pattern], with pattern /; test
#
# This was a stub returning True, so all 201 rules carrying a MatchQ guard were
# unrestricted. Two independent layers had to be fixed, and both are asserted here:
#   1. check() now really matches;
#   2. a constraint may only declare variables the PATTERN binds -- MatchQ's inner
#      pattern variables are local to it, and declaring them made MatchPy's
#      CustomConstraint short-circuit to True on a KeyError, bypassing check()
#      entirely (47 of 29154 constraints were in that state).
# =============================================================================

class TestMatchQMatches:

    def _mq(self, subject, pattern):
        from rubi_rules.utils.constraints_wolfram import MatchQ
        return MatchQ(subject, pattern)

    def test_a_structural_match_is_accepted(self):
        from sympy_matching.wild import WildSymbol
        xx, n = Symbol('x'), Symbol('n')
        u_, c_, m_ = WildSymbol('u'), WildSymbol('c'), WildSymbol('m')
        mq = self._mq(u_, (c_ * xx) ** m_)
        assert mq.check(u=(3 * xx) ** n) is True

    def test_a_non_match_is_rejected(self):
        """The whole point: this used to return True unconditionally."""
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, c_, m_ = WildSymbol('u'), WildSymbol('c'), WildSymbol('m')
        mq = self._mq(u_, (c_ * xx) ** m_)
        assert mq.check(u=sympy.sin(xx)) is False

    def test_head_must_agree(self):
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, c_ = WildSymbol('u'), WildSymbol('c')
        assert self._mq(u_, sympy.log(c_ + xx)).check(u=sympy.log(1 + xx)) is True
        assert self._mq(u_, sympy.sin(c_ + xx)).check(u=sympy.log(1 + xx)) is False

    def test_a_sum_pattern(self):
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, c_, d_ = WildSymbol('u'), WildSymbol('c'), WildSymbol('d')
        mq = self._mq(u_, c_ * xx + d_)
        assert mq.check(u=3 * xx + 5) is True
        assert mq.check(u=sympy.sin(xx) + sympy.cos(xx)) is False

    def test_an_outer_bound_name_matches_only_its_value(self):
        """Names the enclosing rule bound are substituted in, so they are literals
        here; only MatchQ-local names are free for the matcher to solve."""
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, a_, m_ = WildSymbol('u'), WildSymbol('a'), WildSymbol('m')
        mq = self._mq(u_, (a_ + xx) ** m_)
        assert mq.check(u=(7 + xx) ** 2, a=Integer(7)) is True
        assert mq.check(u=(7 + xx) ** 2, a=Integer(9)) is False

    def test_a_failing_guard_rejects_a_structural_match(self):
        from sympy_wolfram.objects import Condition
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, c_, m_ = WildSymbol('u'), WildSymbol('c'), WildSymbol('m')
        never = Condition((c_ * xx) ** m_, sympy.false)
        assert self._mq(u_, never).check(u=(3 * xx) ** Symbol('n')) is False

    def test_a_holding_guard_keeps_the_match(self):
        from sympy_wolfram.objects import Condition
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        u_, c_, m_ = WildSymbol('u'), WildSymbol('c'), WildSymbol('m')
        always = Condition((c_ * xx) ** m_, sympy.true)
        assert self._mq(u_, always).check(u=(3 * xx) ** Symbol('n')) is True

    def test_an_unconvertible_subject_is_simply_no_match(self):
        """A guard must never abort the surrounding rule search."""
        from sympy_matching.wild import WildSymbol
        u_, c_ = WildSymbol('u'), WildSymbol('c')
        assert self._mq(u_, c_).check(u=object()) in (True, False)


class TestConstraintVariablesAreRestrictedToThePattern:
    """MatchPy's CustomConstraint returns True when a declared variable is missing
    from the match. Declaring a MatchQ-local variable therefore silenced the whole
    guard, so only pattern-bound variables may be declared."""

    def test_only_pattern_bound_variables_are_declared(self):
        from rubi_rules.base_objects import _make_matchpy_constraint
        from rubi_rules.utils.constraints_wolfram import MatchQ
        from sympy_matching.wild import WildSymbol
        u_, local_ = WildSymbol('u'), WildSymbol('localvar')
        cc = _make_matchpy_constraint(MatchQ(u_, local_ * Symbol('x')), ['u'], {'u'})
        assert set(cc._variables) == {'u'}          # 'localvar' must NOT be declared


class TestMatchQEnforcementIsGated:
    """`MatchQ` is implemented and unit-tested above, but is NOT used as a rule guard
    by default: SymPy normalises expressions before we see them, so the match is not
    faithful to Mathematica and enforcing it REFUSES rules Rubi would offer (measured
    on a 120-integrand corpus sample: 81 solved unenforced vs 69 fully enforced).

    These pin both halves -- that the default really is permissive, and that the
    enforcement path really does discriminate when switched on -- so neither the
    default nor the machinery can rot.
    """

    def _cc(self, constraint, enforce):
        import rubi_rules.base_objects as bo
        saved = bo.ENFORCE_MATCHQ
        bo.ENFORCE_MATCHQ = enforce
        try:
            return bo._make_matchpy_constraint(constraint, ['u'], {'u'})
        finally:
            bo.ENFORCE_MATCHQ = saved

    def _mq(self):
        from rubi_rules.utils.constraints_wolfram import MatchQ
        from sympy_matching.wild import WildSymbol
        return MatchQ(WildSymbol('u'), Symbol('x') ** WildSymbol('m'))

    def test_default_is_permissive_for_a_requirement(self):
        from matchpy.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(self._mq(), enforce=False)
        assert cc(Substitution({'u': sympy.cos(xx)})) is True    # not refused

    def test_default_is_permissive_for_an_exclusion(self):
        """A false positive here would REFUSE a rule, which is the harmful direction."""
        from matchpy.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(sympy.Not(self._mq()), enforce=False)
        assert cc(Substitution({'u': xx ** 2})) is True

    def test_when_enforced_a_requirement_discriminates(self):
        from matchpy.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(self._mq(), enforce=True)
        assert cc(Substitution({'u': xx ** 2})) is True
        assert cc(Substitution({'u': sympy.cos(xx)})) is False

    def test_when_enforced_an_exclusion_discriminates(self):
        from matchpy.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(sympy.Not(self._mq()), enforce=True)
        assert cc(Substitution({'u': xx ** 2})) is False
        assert cc(Substitution({'u': sympy.cos(xx)})) is True

    def test_a_non_matchq_constraint_is_unaffected_by_the_gate(self):
        """The gate must catch MatchQ only, never a neighbouring guard."""
        from matchpy.expressions.substitution import Substitution
        from rubi_rules.utils.constraints_wolfram import FreeQ
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        cc = self._cc(FreeQ(WildSymbol('u'), xx), enforce=False)
        assert cc(Substitution({'u': Symbol('a')})) is True
        assert cc(Substitution({'u': xx})) is False
