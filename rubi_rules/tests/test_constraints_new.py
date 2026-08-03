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
    """Tests for FractionalPowerFactorQ constraint. Values cross-checked against real
    Rubi (ssh pi): Head[u]===Complex for atoms, FractionQ[exponent] for powers, and for
    products First[u] || Rest[u].

    Guards two bugs that made it wrong / crash:
      * ``ProductQ`` inside ``check`` resolved to the CONSTRAINT CLASS (always truthy, since
        this module defines a ``ProductQ`` class), so the product branch fired for EVERY u
        -- e.g. a bare sum ``a+I`` wrongly recursed into its terms and returned True.
      * the product branch used ``u.args[1:]`` (a raw tuple) instead of ``Rest[u]`` (the
        product of the remaining factors), so the recursion peeled down to an empty args
        tuple and raised IndexError (Int[x^2 (d+e x)/Sqrt[d^2-e^2 x^2]] etc. crashed).
      * the atom branch returned ``u.is_complex`` -- True for reals in SymPy -- instead of
        Head[u]===Complex.
    """

    def _q(self, u):
        c = FractionalPowerFactorQ('u')
        return bool(c.check(u=u))

    def test_atoms(self):
        a = Symbol('a')
        assert self._q(I) is True          # Head===Complex
        assert self._q(a) is False         # real symbol is NOT complex (was wrongly True)
        assert self._q(Integer(2)) is False

    def test_powers(self):
        assert self._q(x**Rational(1, 2)) is True    # fractional exponent
        assert self._q(x**2) is False                # integer exponent

    def test_products(self):
        a, b = Symbol('a'), Symbol('b')
        assert self._q(a * x**Rational(1, 2)) is True   # a fractional-power factor
        assert self._q(2 * I) is True                    # a complex factor
        assert self._q(a * b) is False                   # neither

    def test_a_bare_sum_is_false(self):
        """Regression for the ProductQ-class shadow: a Plus is neither atom/power/product,
        so it must be False -- it must NOT recurse into its terms as if it were a product."""
        a = Symbol('a')
        assert self._q(a + I) is False       # was wrongly True
        assert self._q(a + x**Rational(1, 2)) is False

    def test_deep_product_does_not_crash(self):
        """Regression for the u.args[1:] tuple IndexError on longer products."""
        a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
        assert self._q(a * b * c * x**Rational(1, 3)) is True
        assert self._q(a * b * c) is False


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


# These four predicates test Rubi's INERT trig markers, not the active functions.
# Rubi calls `KnownTrigIntegrandQ[{sin,cos},u,x]` with LOWERCASE heads, which in Rubi
# are the inert markers (`Rubi`sin`). The rules guarded by these predicates all match
# on `InertSin(...)`/`InertTan(...)` patterns, so the bound `u` is always inert trig.
# Every value below was read off Rubi 4.17.3.0. The earlier version of these tests
# asserted `check(u=sin(x)) == True` for ACTIVE trig, which Rubi answers False -- they
# were written from the port's behaviour rather than from Rubi, and so kept a defect
# alive that disabled all 64 rules guarded by these predicates.
from rubi_rules.utils.inert_functions import (InertSin, InertCos, InertTan,
                                              InertCot, InertSec, InertCsc)


class TestKnownSineIntegrandQ:
    """Tests for KnownSineIntegrandQ constraint."""

    def test_sine_integrand(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=InertSin(x)) == True
        assert c.check(u=InertCos(2*x + 1)) == True

    def test_active_trig_is_not_a_known_sine_integrand(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=sin(x)) == False
        assert c.check(u=cos(2*x + 1)) == False

    def test_unity(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=S.One) == True

    def test_not_sine(self):
        c = KnownSineIntegrandQ('u', x)
        assert c.check(u=InertTan(x)) == False
        assert c.check(u=tan(x)) == False


class TestKnownTangentIntegrandQ:
    """Tests for KnownTangentIntegrandQ constraint."""

    def test_tangent_integrand(self):
        c = KnownTangentIntegrandQ('u', x)
        assert c.check(u=InertTan(x)) == True
        assert c.check(u=InertTan(3*x + 2)) == True

    def test_active_tangent_is_rejected(self):
        c = KnownTangentIntegrandQ('u', x)
        assert c.check(u=tan(x)) == False

    def test_not_tangent(self):
        c = KnownTangentIntegrandQ('u', x)
        assert c.check(u=InertSin(x)) == False


class TestKnownSecantIntegrandQ:
    """Tests for KnownSecantIntegrandQ constraint."""

    def test_secant_integrand(self):
        c = KnownSecantIntegrandQ('u', x)
        assert c.check(u=InertSec(x)) == True
        assert c.check(u=InertCsc(2*x)) == True

    def test_active_secant_is_rejected(self):
        c = KnownSecantIntegrandQ('u', x)
        assert c.check(u=sec(x)) == False

    def test_not_secant(self):
        c = KnownSecantIntegrandQ('u', x)
        assert c.check(u=InertSin(x)) == False


class TestKnownCotangentIntegrandQ:
    """Tests for KnownCotangentIntegrandQ constraint."""

    def test_cotangent_integrand(self):
        c = KnownCotangentIntegrandQ('u', x)
        assert c.check(u=InertCot(x)) == True
        assert c.check(u=S.One) == True

    def test_active_cotangent_is_rejected(self):
        c = KnownCotangentIntegrandQ('u', x)
        assert c.check(u=cot(x)) == False

    def test_not_cotangent(self):
        c = KnownCotangentIntegrandQ('u', x)
        assert c.check(u=InertCos(x)) == False


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
#      pattern variables are local to it, and declaring them made OmniMatch's
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
    """OmniMatch's CustomConstraint returns True when a declared variable is missing
    from the match. Declaring a MatchQ-local variable therefore silenced the whole
    guard, so only pattern-bound variables may be declared."""

    def test_only_pattern_bound_variables_are_declared(self):
        from rubi_rules.base_objects import _make_omnimatch_constraint
        from rubi_rules.utils.constraints_wolfram import MatchQ
        from sympy_matching.wild import WildSymbol
        u_, local_ = WildSymbol('u'), WildSymbol('localvar')
        cc = _make_omnimatch_constraint(MatchQ(u_, local_ * Symbol('x')), {'u'})
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
        # ENFORCE_MATCHQ + the machinery live in sympy_matching.matching_rule now
        # (rubi_rules.base_objects only re-exports them). _make_constraint_checker reads
        # the flag from matching_rule's namespace, so patch it THERE.
        import sympy_matching.matching_rule as mr
        saved = mr.ENFORCE_MATCHQ
        mr.ENFORCE_MATCHQ = enforce
        try:
            return mr._make_omnimatch_constraint(constraint, {'u'})
        finally:
            mr.ENFORCE_MATCHQ = saved

    def _mq(self):
        from rubi_rules.utils.constraints_wolfram import MatchQ
        from sympy_matching.wild import WildSymbol
        return MatchQ(WildSymbol('u'), Symbol('x') ** WildSymbol('m'))

    def test_default_is_permissive_for_a_requirement(self):
        from omnimatch.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(self._mq(), enforce=False)
        assert cc(Substitution({'u': sympy.cos(xx)})) is True    # not refused

    def test_default_is_permissive_for_an_exclusion(self):
        """A false positive here would REFUSE a rule, which is the harmful direction."""
        from omnimatch.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(sympy.Not(self._mq()), enforce=False)
        assert cc(Substitution({'u': xx ** 2})) is True

    def test_when_enforced_a_requirement_discriminates(self):
        from omnimatch.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(self._mq(), enforce=True)
        assert cc(Substitution({'u': xx ** 2})) is True
        assert cc(Substitution({'u': sympy.cos(xx)})) is False

    def test_when_enforced_an_exclusion_discriminates(self):
        from omnimatch.expressions.substitution import Substitution
        xx = Symbol('x')
        cc = self._cc(sympy.Not(self._mq()), enforce=True)
        assert cc(Substitution({'u': xx ** 2})) is False
        assert cc(Substitution({'u': sympy.cos(xx)})) is True

    def test_a_non_matchq_constraint_is_unaffected_by_the_gate(self):
        """The gate must catch MatchQ only, never a neighbouring guard."""
        from omnimatch.expressions.substitution import Substitution
        from rubi_rules.utils.constraints_wolfram import FreeQ
        from sympy_matching.wild import WildSymbol
        xx = Symbol('x')
        cc = self._cc(FreeQ(WildSymbol('u'), xx), enforce=False)
        assert cc(Substitution({'u': Symbol('a')})) is True
        assert cc(Substitution({'u': xx})) is False


class TestGenericBooleanConstraintChecker:
    """Regression + design guard for a generic SymPy-Boolean rule guard -- a bare
    relational like ``Ne(GCD(m+1, n), 1)``, NOT a MathematicaConstraint.

    Its variables are WildSymbols, which cross the SymPy<->OmniMatch boundary as
    Wildcards; a plain ``Symbol`` crosses as a ``SymbolWrapper`` CONSTANT. So the matcher
    returns the bound values by wildcard NAME, as ``SymbolWrapper``s (e.g.
    ``'m' -> SymbolWrapper(1)``). The checker must therefore resolve the guard's own
    wildcards BY NAME -- via ``_resolve_with_substitution``, the same resolver every other
    constraint uses -- with the values converted back to SymPy. The old code instead
    built a ``.subs({Symbol(name): value})`` key: a ``Symbol`` is the constant side, so it
    matched neither the guard's WildSymbol nor even a fresh ``WildSymbol(name)`` (a
    WildSymbol is instance-unique via its ``_wild_index``) -- a silent no-op that left the
    relational symbolic, made ``== True`` False, and disabled the ``x^m/(a+b x^n)``
    GCD-reduction rules (so ``Int[x/(a+b x^6)]`` gave a wrong ``I*ArcTan``). The deferred
    ``GCD`` node also has to be ``doit()``'d before the truth test.
    """

    def _checker(self, constraint):
        from rubi_rules.base_objects import _make_omnimatch_constraint
        return _make_omnimatch_constraint(constraint, {'m', 'n'})

    def test_ne_gcd_guard_evaluates_with_wildsymbols_and_deferred_node(self):
        from omnimatch.expressions.substitution import Substitution
        from rubi_rules.utils.rubi_utils import GCD
        m_, n_ = WildSymbol('m'), WildSymbol('n')
        cc = self._checker(sympy.Ne(GCD(m_ + 1, n_), 1))
        # GCD(1+1, 6) = 2 != 1 -> guard holds (this is the case that used to fail)
        assert cc(Substitution({'m': sympy.Integer(1), 'n': sympy.Integer(6)})) is True
        # GCD(3+1, 6) = 2 != 1 -> holds
        assert cc(Substitution({'m': sympy.Integer(3), 'n': sympy.Integer(6)})) is True
        # GCD(1+1, 3) = 1 -> guard correctly FAILS (Ne(1, 1) is False)
        assert cc(Substitution({'m': sympy.Integer(1), 'n': sympy.Integer(3)})) is False

    def test_guard_resolves_the_symbolwrapper_values_the_matcher_delivers(self):
        """The bound values arrive as OmniMatch ``SymbolWrapper`` constants (that is how the
        matcher hands back what a Wildcard matched), NOT as bare SymPy numbers. The checker
        must unwrap them -- ``SymbolWrapper(1) -> Integer(1)`` -- before evaluating."""
        from omnimatch.expressions.substitution import Substitution
        from omnimatch.expressions.expressions import SymbolWrapper
        from rubi_rules.utils.rubi_utils import GCD
        m_, n_ = WildSymbol('m'), WildSymbol('n')
        cc = self._checker(sympy.Ne(GCD(m_ + 1, n_), 1))
        sw = lambda k: SymbolWrapper(sympy.Integer(k))
        assert cc(Substitution({'m': sw(1), 'n': sw(6)})) is True   # GCD(2,6)=2 != 1
        assert cc(Substitution({'m': sw(1), 'n': sw(3)})) is False  # GCD(2,3)=1

    def test_a_fresh_symbol_or_wildsymbol_would_not_have_substituted(self):
        """Documents WHY the resolver keys by name: neither a plain ``Symbol('m')`` nor a
        freshly built ``WildSymbol('m')`` is equal to the guard's own wildcard, so a
        ``.subs()`` keyed on either is a silent no-op (this was the original bug)."""
        m_ = WildSymbol('m')
        guard = sympy.Ne(m_, 1)
        assert guard.subs({Symbol('m'): sympy.Integer(1)}) == guard          # no-op
        assert guard.subs({WildSymbol('m'): sympy.Integer(1)}) == guard      # no-op (diff instance)
        assert guard.subs({m_: sympy.Integer(1)}).doit() is sympy.false      # only the real instance

    def test_eq_guard_with_wildsymbol_still_works(self):
        """A plain Eq guard over a WildSymbol substitutes and evaluates too."""
        from omnimatch.expressions.substitution import Substitution
        n_ = WildSymbol('n')
        cc = self._checker(sympy.Eq(n_, 6))
        assert cc(Substitution({'n': sympy.Integer(6)})) is True
        assert cc(Substitution({'n': sympy.Integer(5)})) is False


class TestPolyQResolvesSecondArg:
    """Regression for the PolyQ constraint dropping the offset in Int[atanh(a+b x)^2/x^3].

    The 'P(x) (a+b x^n)^p' rules pass PolyQ(Pq_, v_**n_) -- the 2nd arg is a WILDCARD
    expression, not the bare integration variable. PolyQ.check() must RESOLVE it; left
    unresolved it stayed a WildSymbol Pow that every integrand is a trivial degree-0
    'polynomial' in, so PolyQ was ALWAYS True. That let rule 1.1.3.7#46 fire on
    atanh(a+b x)/(x^2 (1-(a+b x)^2)) and drop the offset via SubstFor, giving a
    numerically-WRONG (PolyLog-free) antiderivative.
    """
    def _polyq(self, Pq_val, v_val, n_val):
        from rubi_rules.utils.constraints_rubi import PolyQ
        Pq, v, n = WildSymbol('Pq'), WildSymbol('v'), WildSymbol('n')
        return PolyQ(Pq, v**n).check(Pq=Pq_val, v=v_val, n=n_val)

    def test_rejects_non_polynomial_in_v(self):
        from sympy import atanh
        a, b = Symbol('a'), Symbol('b')
        # atanh(a+bx)/x^2 is NOT a polynomial in (a+bx)^2 -> PolyQ must be falsy
        assert not self._polyq(atanh(a + b*x)/x**2, a + b*x, Integer(2))

    def test_accepts_genuine_polynomial_in_v(self):
        a, b = Symbol('a'), Symbol('b')
        assert self._polyq((a + b*x)**4 + (a + b*x)**2, a + b*x, Integer(2))


class TestBooleanPoisonedEvaluationDoesNotCrash:
    """A deferred node that signals "no result" by returning False must not crash guards.

    Several Rubi helpers return False as their failure value. When such a node sits
    under arithmetic in a guard's argument (e.g. a negation), ``doit(deep=True)``
    rebuilds the parent as ``Mul(-1, False)`` -- sympy 1.x still constructs it, with a
    deprecation warning -- and the poisoned value later drives ``simplify`` into
    infinite recursion, aborting the WHOLE integration with a RecursionError (seen on
    ``Int[(c+d x)^4 Gamma[n, a+b x]]``). The `_resolve` in ``sympy_wolfram.constraints``
    now treats a boolean NESTED inside arithmetic as a failed evaluation and keeps the
    unevaluated form, so the guard compares symbolically and simply answers False --
    which is what Mathematica does.
    """

    def test_eqq_over_a_false_returning_node_is_false_not_a_crash(self):
        import sympy
        from sympy_wolfram.objects import MathematicaExpr
        from rubi_rules.utils.constraints_rubi import EqQ

        class _FailsWithFalse(MathematicaExpr):
            """Minimal Rubi-style helper: evaluation signals failure by returning False."""
            def __new__(cls, u):
                return sympy.Expr.__new__(cls, u)

            def _evaluate(self, **kwargs):
                return False

        u_ = WildSymbol('u')
        guard = EqQ(1 - _FailsWithFalse(u_), 2)
        # must neither raise nor return True; the comparison cannot hold
        assert guard.check(u=Symbol('z')) is False

    def test_a_whole_boolean_result_is_still_passed_through(self):
        """Only NESTED booleans are poison; a node that legitimately evaluates to a
        bare boolean keeps doing so (predicates handle those natively)."""
        import sympy
        from sympy_wolfram.objects import MathematicaExpr

        class _EvaluatesToFalse(MathematicaExpr):
            def __new__(cls, u):
                return sympy.Expr.__new__(cls, u)

            def _evaluate(self, **kwargs):
                return sympy.false

        node = _EvaluatesToFalse(Symbol('z'))
        assert node.doit() is sympy.false


class TestMathematicaExprIsCommutative:
    """Every Wolfram node models a scalar, so it must DECLARE commutativity.

    With ``is_commutative`` left as None, sympy computed **False** for any Add
    containing a Wolfram node and then refused to distribute numeric coefficients over
    it; ``Abs``/``signsimp`` flip-flopped between the two sign forms of
    ``-1 - IntPart(m, 1)`` forever, aborting ``Int[(c+d x)^4 Gamma[n, a+b x]]`` with a
    RecursionError. A generic ``Function('f')(m, 1)`` -- which is commutative -- never
    looped, which is what isolated the missing declaration.
    """

    def test_nodes_and_containing_adds_are_commutative(self):
        from rubi_rules.utils.rubi_utils import IntPart
        m = Symbol('m')
        assert IntPart(m, 1).is_commutative is True
        assert (-1 - IntPart(m, 1)).is_commutative is True

    def test_negation_distributes_and_abs_terminates(self):
        import sympy
        from rubi_rules.utils.rubi_utils import IntPart
        m = Symbol('m')
        assert -(-1 - IntPart(m, 1)) == IntPart(m, 1) + 1
        # this exact call used to recurse to the interpreter limit
        assert sympy.Abs(-1 - IntPart(m, 1)) == sympy.Abs(IntPart(m, 1) + 1)


class TestExpensiveGuardDeferralPolicy:
    """The Rubi-side policy for `build_replacer(defer_constraint=...)`.

    Guards that recursively invoke the integrator (`IntHide` is literally `Int` with
    steps hidden) or do heavy algebra must be DEFERRED to attempt time; with them
    attached to the omnimatch Pattern, sorting the matcher's yields by priority paid a
    full sub-integration per catch-all candidate before the first (correct, cheap)
    rule was ever attempted -- `Int[(c+d x)^7/(a+b x)^7]` hung >120 s while its
    winning rule `1.1.1.2:[12]` sorted first the whole time (defects §33).
    """

    def test_expensive_heads_are_deferred(self):
        from rubi_rules.base_objects import _defer_expensive_guard, EXPENSIVE_GUARD_HEADS
        from rubi_rules.utils.constraints_wolfram import FreeQ
        from sympy import Symbol
        u_ = WildSymbol('u')
        x = Symbol('x')
        # a real shape from the ruleset: InverseFunctionFreeQ(IntHide(v, x), x)
        from rubi_rules.utils.rubi_utils import IntHide
        from rubi_rules.utils.constraints_rubi import EqQ
        assert _defer_expensive_guard(EqQ(IntHide(u_, x), 0)) is True
        for head in EXPENSIVE_GUARD_HEADS:
            assert _defer_expensive_guard(Symbol(head)) is True

    def test_cheap_guards_stay_on_the_pattern(self):
        from rubi_rules.base_objects import _defer_expensive_guard
        from rubi_rules.utils.constraints_wolfram import FreeQ, IntegerQ
        from sympy import Symbol
        u_ = WildSymbol('u')
        x = Symbol('x')
        assert _defer_expensive_guard(FreeQ(u_, x)) is False
        assert _defer_expensive_guard(IntegerQ(u_)) is False


class TestPolynomialDivideKeepsTheSplit:
    """`PolynomialDivide[u, v, x]` must return quotient + remainder/v AS A SUM.

    The deferred node used to wrap its result in ``together(q + r/v)``, recombining
    quotient and remainder over the common denominator -- exactly UNDOING the division
    the firing rule exists to perform. `1.1.2.3#21` then handed the DFS back the same
    rational function (numerator merely expanded), the search wandered into a
    trinomial give-up, and ``Int[(a+b tan(c+d x)^2)^2]`` -- which Rubi solves in
    0.2 s -- returned Unintegrable. Same recombination anti-pattern as the termwise
    `apart` fix (defects §34/§35).
    """

    def test_node_returns_the_split_form(self):
        from rubi_rules.utils.rubi_utils import PolynomialDivide
        x, a, b = Symbol('x'), Symbol('a'), Symbol('b')
        result = PolynomialDivide((a + b*x**2)**2, x**2 + 1, x).doit()
        # a polynomial part plus a proper fraction -- NOT one combined quotient.
        # The remainder numerator stays EXPANDED: Mathematica's Together (now
        # ported faithfully, without the old full-factor behaviour) leaves a
        # content-free sum alone -- Together[a^2-2ab+b^2] does not factor it.
        assert result == b**2*x**2 + b*(2*a - b) + (a**2 - 2*a*b + b**2)/(x**2 + 1)

    def test_node_agrees_with_the_eager_implementation(self):
        from rubi_rules.utils.rubi_utils import PolynomialDivide
        from rubi_rules.utils.utility_functions import eager_PolynomialDivide
        x, a, b = Symbol('x'), Symbol('a'), Symbol('b')
        u, v = (a + b*x**2)**2, x**2 + 1
        assert PolynomialDivide(u, v, x).doit() == eager_PolynomialDivide(u, v, x)


class TestReciprocalInertPowersNormalise:
    """Pure negative powers of inert trig heads must become their reciprocal heads
    at deactivation time (1/InertSin^2 -> InertCsc^2): the rule corpus, like
    Rubi's own, patterns on csc/sec/cot, while Rubi's half-angle rules emit
    Sin[...]^(2n) with n < 0. Without the bridge, Int[(c+dx)^2/(a+a cos)] and
    x/Sqrt[a+a cos] dead-ended in Unintegrable (defects §44)."""

    def test_helper_rewrites_bare_negative_powers_only(self):
        from sympy import Symbol
        from rubi_rules.utils.inert_functions import (
            InertSin, InertCsc, InertCos, InertSec, fix_reciprocal_inert_powers)
        v = Symbol('v')
        a, c, d = Symbol('a'), Symbol('c'), Symbol('d')
        u = (c + d*v)**2/InertSin(v)**2
        assert fix_reciprocal_inert_powers(u) == (c + d*v)**2*InertCsc(v)**2
        assert fix_reciprocal_inert_powers(1/InertCos(v)) == InertSec(v)
        # composite bases stay untouched (wildcard exponents bind those)
        w = (a + InertSin(v))**-2
        assert fix_reciprocal_inert_powers(w) == w
        # positive powers stay untouched
        assert fix_reciprocal_inert_powers(InertSin(v)**3) == InertSin(v)**3

    def test_half_angle_chain_solves(self):
        from sympy import Symbol, cos, sqrt, diff, N, Rational
        from rubi_rules.base_objects import rubi_integrate, Int as _Int
        xx, a, c, d = Symbol('x'), Symbol('a'), Symbol('c'), Symbol('d')
        g = xx/sqrt(a*cos(c + d*xx) + a)
        r = rubi_integrate(g, xx)
        assert not r.has(_Int) and 'Unintegrable' not in str(r)
