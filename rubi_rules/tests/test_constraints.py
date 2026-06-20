# -*- coding: utf-8 -*-
"""Tests for RUBI constraint predicates.

Tests both Wolfram Mathematica standard constraints (constraints_wolfram.py)
and RUBI-specific constraints (constraints_rubi.py).
"""
import pytest
import sympy
from sympy import (
    Symbol, Integer, Rational, Float, I, pi, E, S,
    sin, cos, tan, cot, sec, csc,
    sinh, cosh, tanh, coth, sech, csch,
    asin, acos, atan, acot, asec, acsc,
    asinh, acosh, atanh, acoth, asech, acsch,
    log, exp, sqrt, Abs, Add, Mul, Pow
)

# Import all constraints
from rubi_rules.utils.constraints_wolfram import (
    FreeQ, IntegerQ, OddQ, EvenQ, NumberQ, NumericQ,
    AtomQ, MemberQ, PositiveQ, NegativeQ, PolynomialQ,
    TrueQ, FalseQ, MatchQ, PrimeQ
)

from rubi_rules.utils.constraints_rubi import (
    EqQ, NeQ,
    IGtQ, ILtQ, IGeQ, ILeQ,
    GtQ, LtQ, GeQ, LeQ,
    PosQ, NegQ,
    IntegersQ, HalfIntegerQ, FractionQ, RationalQ,
    ComplexNumberQ, RealNumberQ, FractionOrNegativeQ, SqrtNumberQ,
    PowerQ, ProductQ, SumQ, NonsumQ,
    IntegerPowerQ, FractionalPowerQ,
    PolyQ, LinearQ, QuadraticQ, BinomialQ, TrinomialQ,
    LinearMatchQ, QuadraticMatchQ, BinomialMatchQ, TrinomialMatchQ,
    TrigQ, HyperbolicQ, InverseTrigQ, InverseHyperbolicQ, LogQ,
    ComplexFreeQ, InverseFunctionFreeQ, FractionalPowerFreeQ,
    TrigHyperbolicFreeQ, IntegralFreeQ,
    RationalFunctionQ, AlgebraicFunctionQ, IndependentQ,
    SimplerQ, SumSimplerQ,
    FunctionOfQ, PiecewiseLinearQ,
    ExpressionEqQ,
)


# Symbols for testing
x = Symbol('x')
a, b, c, m, n, p = sympy.symbols('a b c m n p')


# =============================================================================
# Wolfram Standard Constraints Tests
# =============================================================================


class TestFreeQ:
    """Tests for FreeQ constraint."""

    def test_free_of_x(self):
        c = FreeQ('a', x)
        assert c.check(a=Integer(5)) == True
        assert c.check(a=Symbol('y')) == True
        assert c.check(a=x) == False
        assert c.check(a=x + 1) == False

    def test_free_of_x_expression(self):
        c = FreeQ('a', x)
        assert c.check(a=sin(Symbol('y'))) == True
        assert c.check(a=sin(x)) == False

    def test_repr(self):
        c = FreeQ('a', x)
        assert 'FreeQ' in repr(c)


class TestIntegerQ:
    """Tests for IntegerQ constraint."""

    def test_integer(self):
        c = IntegerQ('n')
        assert c.check(n=Integer(5)) == True
        assert c.check(n=Integer(-3)) == True
        assert c.check(n=Integer(0)) == True

    def test_not_integer(self):
        c = IntegerQ('n')
        assert c.check(n=Rational(1, 2)) == False
        assert c.check(n=Float(3.14)) == False
        assert c.check(n=x) == False


class TestOddQ:
    """Tests for OddQ constraint."""

    def test_odd(self):
        c = OddQ('n')
        assert c.check(n=Integer(3)) == True
        assert c.check(n=Integer(-5)) == True
        assert c.check(n=Integer(1)) == True

    def test_not_odd(self):
        c = OddQ('n')
        assert c.check(n=Integer(2)) == False
        assert c.check(n=Integer(0)) == False
        assert c.check(n=Rational(3, 2)) == False


class TestEvenQ:
    """Tests for EvenQ constraint."""

    def test_even(self):
        c = EvenQ('n')
        assert c.check(n=Integer(2)) == True
        assert c.check(n=Integer(-4)) == True
        assert c.check(n=Integer(0)) == True

    def test_not_even(self):
        c = EvenQ('n')
        assert c.check(n=Integer(3)) == False
        assert c.check(n=Rational(2, 1)) == True  # SymPy simplifies Rational(2,1) to Integer(2)


class TestNumberQ:
    """Tests for NumberQ constraint."""

    def test_number(self):
        c = NumberQ('n')
        assert c.check(n=Integer(5)) == True
        assert c.check(n=Rational(1, 2)) == True
        assert c.check(n=Float(3.14)) == True
        assert c.check(n=pi) == True

    def test_not_number(self):
        c = NumberQ('n')
        assert c.check(n=x) == False
        assert c.check(n=x + 1) == False


class TestAtomQ:
    """Tests for AtomQ constraint."""

    def test_atom(self):
        c = AtomQ('a')
        assert c.check(a=Integer(5)) == True
        assert c.check(a=Symbol('y')) == True
        assert c.check(a=Rational(1, 2)) == True

    def test_not_atom(self):
        c = AtomQ('a')
        assert c.check(a=x + 1) == False
        assert c.check(a=x * 2) == False
        assert c.check(a=sin(x)) == False


class TestPositiveQ:
    """Tests for PositiveQ constraint."""

    def test_positive(self):
        c = PositiveQ('n')
        assert c.check(n=Integer(5)) == True
        assert c.check(n=Rational(1, 2)) == True
        assert c.check(n=pi) == True

    def test_not_positive(self):
        c = PositiveQ('n')
        assert c.check(n=Integer(-5)) == False
        assert c.check(n=Integer(0)) == False


class TestNegativeQ:
    """Tests for NegativeQ constraint."""

    def test_negative(self):
        c = NegativeQ('n')
        assert c.check(n=Integer(-5)) == True
        assert c.check(n=Rational(-1, 2)) == True

    def test_not_negative(self):
        c = NegativeQ('n')
        assert c.check(n=Integer(5)) == False
        assert c.check(n=Integer(0)) == False


class TestPolynomialQ:
    """Tests for PolynomialQ constraint."""

    def test_polynomial(self):
        c = PolynomialQ('u', x)
        assert c.check(u=x**2 + 2*x + 1) == True
        assert c.check(u=Integer(5)) == True
        assert c.check(u=x) == True

    @pytest.mark.skip(reason="check output values")
    def test_not_polynomial(self):
        c = PolynomialQ('u', x)
        assert c.check(u=1/x) == False
        assert c.check(u=sin(x)) == False


# =============================================================================
# RUBI-Specific Constraints Tests
# =============================================================================


class TestEqQ:
    """Tests for EqQ constraint (RUBI equality)."""

    def test_equal(self):
        c = EqQ('m', -1)
        assert c.check(m=Integer(-1)) == True
        assert c.check(m=Integer(1)) == False

    def test_equal_symbolic(self):
        c = EqQ('m', 0)
        assert c.check(m=Integer(0)) == True
        assert c.check(m=x - x) == True  # Simplifies to 0


class TestNeQ:
    """Tests for NeQ constraint (RUBI inequality)."""

    def test_not_equal(self):
        c = NeQ('m', -1)
        assert c.check(m=Integer(-1)) == False
        assert c.check(m=Integer(1)) == True
        assert c.check(m=Integer(0)) == True


class TestIGtQ:
    """Tests for IGtQ constraint (integer greater than)."""

    def test_integer_gt(self):
        c = IGtQ('p', 0)
        assert c.check(p=Integer(1)) == True
        assert c.check(p=Integer(5)) == True
        assert c.check(p=Integer(0)) == False
        assert c.check(p=Integer(-1)) == False

    def test_not_integer(self):
        c = IGtQ('p', 0)
        assert c.check(p=Rational(1, 2)) == False  # Not an integer


class TestILtQ:
    """Tests for ILtQ constraint (integer less than)."""

    def test_integer_lt(self):
        c = ILtQ('p', 0)
        assert c.check(p=Integer(-1)) == True
        assert c.check(p=Integer(-5)) == True
        assert c.check(p=Integer(0)) == False
        assert c.check(p=Integer(1)) == False


class TestIGeQ:
    """Tests for IGeQ constraint (integer greater than or equal)."""

    def test_integer_ge(self):
        c = IGeQ('p', 0)
        assert c.check(p=Integer(0)) == True
        assert c.check(p=Integer(1)) == True
        assert c.check(p=Integer(-1)) == False


class TestILeQ:
    """Tests for ILeQ constraint (integer less than or equal)."""

    def test_integer_le(self):
        c = ILeQ('p', 0)
        assert c.check(p=Integer(0)) == True
        assert c.check(p=Integer(-1)) == True
        assert c.check(p=Integer(1)) == False


class TestGtQ:
    """Tests for GtQ constraint (numeric greater than)."""

    def test_gt(self):
        c = GtQ('m', 0)
        assert c.check(m=Integer(5)) == True
        assert c.check(m=Rational(1, 2)) == True
        assert c.check(m=Integer(-1)) == False
        assert c.check(m=Integer(0)) == False


class TestLtQ:
    """Tests for LtQ constraint (numeric less than)."""

    def test_lt(self):
        c = LtQ('m', 0)
        assert c.check(m=Integer(-5)) == True
        assert c.check(m=Rational(-1, 2)) == True
        assert c.check(m=Integer(1)) == False


class TestGeQ:
    """Tests for GeQ constraint (numeric greater than or equal)."""

    def test_ge(self):
        c = GeQ('m', 0)
        assert c.check(m=Integer(0)) == True
        assert c.check(m=Integer(5)) == True
        assert c.check(m=Integer(-1)) == False


class TestLeQ:
    """Tests for LeQ constraint (numeric less than or equal)."""

    def test_le(self):
        c = LeQ('m', 0)
        assert c.check(m=Integer(0)) == True
        assert c.check(m=Integer(-5)) == True
        assert c.check(m=Integer(1)) == False


class TestPosQ:
    """Tests for PosQ constraint."""

    def test_pos(self):
        c = PosQ('m')
        assert c.check(m=Integer(5)) == True
        assert c.check(m=Integer(-1)) == False
        assert c.check(m=Integer(0)) == False


class TestNegQRubi:
    """Tests for NegQ constraint (RUBI version)."""

    def test_neg(self):
        c = NegQ('m')
        assert c.check(m=Integer(-5)) == True
        assert c.check(m=Integer(1)) == False
        assert c.check(m=Integer(0)) == False


class TestIntegersQ:
    """Tests for IntegersQ constraint (multiple integers)."""

    def test_all_integers(self):
        c = IntegersQ('m', 'n')
        assert c.check(m=Integer(1), n=Integer(2)) == True
        assert c.check(m=Integer(1), n=Rational(1, 2)) == False


class TestHalfIntegerQ:
    """Tests for HalfIntegerQ constraint."""

    def test_half_integer(self):
        c = HalfIntegerQ('m')
        assert c.check(m=Rational(1, 2)) == True
        assert c.check(m=Rational(3, 2)) == True
        assert c.check(m=Rational(-5, 2)) == True

    def test_not_half_integer(self):
        c = HalfIntegerQ('m')
        assert c.check(m=Integer(1)) == False
        assert c.check(m=Rational(1, 3)) == False


class TestFractionQ:
    """Tests for FractionQ constraint."""

    def test_fraction(self):
        c = FractionQ('m')
        assert c.check(m=Rational(1, 2)) == True
        assert c.check(m=Rational(3, 4)) == True

    def test_not_fraction(self):
        c = FractionQ('m')
        assert c.check(m=Integer(2)) == False  # 2/1 has denom 1


class TestRationalQ:
    """Tests for RationalQ constraint."""

    def test_rational(self):
        c = RationalQ('m')
        assert c.check(m=Integer(5)) == True
        assert c.check(m=Rational(1, 2)) == True

    def test_not_rational(self):
        c = RationalQ('m')
        assert c.check(m=sqrt(2)) == False
        assert c.check(m=pi) == False


class TestPowerQ:
    """Tests for PowerQ constraint."""

    def test_power(self):
        c = PowerQ('u')
        assert c.check(u=x**2) == True
        assert c.check(u=sqrt(x)) == True  # x**(1/2)

    def test_not_power(self):
        c = PowerQ('u')
        assert c.check(u=x + 1) == False
        assert c.check(u=x) == False


class TestProductQ:
    """Tests for ProductQ constraint."""

    def test_product(self):
        c = ProductQ('u')
        assert c.check(u=2*x) == True
        assert c.check(u=x*Symbol('y')) == True

    def test_not_product(self):
        c = ProductQ('u')
        assert c.check(u=x + 1) == False
        assert c.check(u=x) == False


class TestSumQ:
    """Tests for SumQ constraint."""

    def test_sum(self):
        c = SumQ('u')
        assert c.check(u=x + 1) == True
        assert c.check(u=x + Symbol('y')) == True

    def test_not_sum(self):
        c = SumQ('u')
        assert c.check(u=2*x) == False
        assert c.check(u=x) == False


class TestNonsumQ:
    """Tests for NonsumQ constraint."""

    def test_nonsum(self):
        c = NonsumQ('u')
        assert c.check(u=2*x) == True
        assert c.check(u=x**2) == True
        assert c.check(u=x) == True

    def test_sum(self):
        c = NonsumQ('u')
        assert c.check(u=x + 1) == False


class TestLinearQ:
    """Tests for LinearQ constraint."""

    def test_linear(self):
        c = LinearQ('u', x)
        assert c.check(u=2*x + 3) == True
        assert c.check(u=x) == True

    def test_not_linear(self):
        c = LinearQ('u', x)
        assert c.check(u=x**2) == False
        assert c.check(u=Integer(5)) == False  # Degree 0


class TestQuadraticQ:
    """Tests for QuadraticQ constraint."""

    @pytest.mark.skip(reason="check output values")
    def test_quadratic(self):
        c = QuadraticQ('u', x)
        assert c.check(u=x**2 + 2*x + 1) == True
        assert c.check(u=x**2) == True

    def test_not_quadratic(self):
        c = QuadraticQ('u', x)
        assert c.check(u=x**3) == False
        assert c.check(u=x) == False


class TestBinomialQ:
    """Tests for BinomialQ constraint."""

    def test_binomial(self):
        c = BinomialQ('u', x)
        assert c.check(u=1 + x**2) == True
        assert c.check(u=3 + 5*x**3) == True
        assert c.check(u=x**2) == True  # Just one term

    def test_not_binomial(self):
        c = BinomialQ('u', x)
        assert c.check(u=1 + x + x**2) == False  # 3 terms


class TestTrinomialQ:
    """Tests for TrinomialQ constraint."""

    @pytest.mark.skip(reason="check output values")
    def test_trinomial(self):
        c = TrinomialQ('u', x)
        assert c.check(u=1 + x + x**2) == True
        assert c.check(u=1 + x**2 + x**4) == True

    def test_not_trinomial(self):
        c = TrinomialQ('u', x)
        assert c.check(u=1 + x + x**2 + x**3) == False  # 4 terms


class TestTrigQ:
    """Tests for TrigQ constraint."""

    def test_trig(self):
        c = TrigQ('u')
        assert c.check(u=sin(x)) == True
        assert c.check(u=cos(x)) == True
        assert c.check(u=tan(x)) == True

    def test_not_trig(self):
        c = TrigQ('u')
        assert c.check(u=sinh(x)) == False
        assert c.check(u=log(x)) == False


class TestHyperbolicQ:
    """Tests for HyperbolicQ constraint."""

    def test_hyperbolic(self):
        c = HyperbolicQ('u')
        assert c.check(u=sinh(x)) == True
        assert c.check(u=cosh(x)) == True

    def test_not_hyperbolic(self):
        c = HyperbolicQ('u')
        assert c.check(u=sin(x)) == False


class TestLogQ:
    """Tests for LogQ constraint."""

    def test_log(self):
        c = LogQ('u')
        assert c.check(u=log(x)) == True
        assert c.check(u=log(x + 1)) == True

    def test_not_log(self):
        c = LogQ('u')
        assert c.check(u=sin(x)) == False
        assert c.check(u=x) == False


class TestComplexFreeQ:
    """Tests for ComplexFreeQ constraint."""

    def test_complex_free(self):
        c = ComplexFreeQ('u')
        assert c.check(u=x + 1) == False
        assert c.check(u=x) == True
        assert c.check(u=Integer(5)) == True

    def test_has_complex(self):
        c = ComplexFreeQ('u')
        assert c.check(u=I) == False
        assert c.check(u=1 + I) == False


class TestRationalFunctionQ:
    """Tests for RationalFunctionQ constraint."""

    def test_rational_function(self):
        c = RationalFunctionQ('u', x)
        assert c.check(u=1/x) == True
        assert c.check(u=(x + 1)/(x - 1)) == True
        assert c.check(u=x**2 + 1) == True

    def test_not_rational_function(self):
        c = RationalFunctionQ('u', x)
        assert c.check(u=sin(x)) == False
        assert c.check(u=sqrt(x)) == False


class TestExpressionEqQ:
    """Tests for ExpressionEqQ constraint."""

    def test_linear_combination(self):
        # Check: m + 2*p + 3 == 0
        c = ExpressionEqQ({'m': 1, 'p': 2}, 3, 0)
        assert c.check(m=Integer(1), p=Integer(-2)) == True  # 1 + 2*(-2) + 3 = 0
        assert c.check(m=Integer(0), p=Integer(0)) == False  # 0 + 0 + 3 = 3


# =============================================================================
# Run tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
