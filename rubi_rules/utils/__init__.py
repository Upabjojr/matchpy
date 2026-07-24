# -*- coding: utf-8 -*-
"""RUBI utility modules.

This package contains:
- constraints.py: Base MathematicaConstraint class (re-exported from sympy_wolfram)
- constraints_wolfram.py: Standard Wolfram Mathematica constraint predicates
- constraints_rubi.py: RUBI-specific constraint predicates
- rubi_utils.py: Utility functions for RUBI rules
"""

# Base constraint class (formerly RubiConstraint; RubiConstraint kept as a
# deprecated alias in constraints.py for backward compatibility).
from sympy_wolfram.constraints import MathematicaConstraint

# Standard Wolfram Mathematica constraints
from .constraints_wolfram import (
    FreeQ,
    IntegerQ,
    OddQ,
    EvenQ,
    NumberQ,
    NumericQ,
    AtomQ,
    MemberQ,
    PositiveQ,
    NegativeQ,
    PolynomialQ,
    TrueQ,
    FalseQ,
    MatchQ,
    PrimeQ,
    UnsameQ,
)

# RUBI-specific constraints
from .constraints_rubi import (
    TryPureTanSubst,
    # Equality/Inequality
    EqQ, NeQ,
    # Integer comparisons
    IGtQ, ILtQ, IGeQ, ILeQ,
    # Numeric comparisons
    GtQ, LtQ, GeQ, LeQ,
    # Sign
    PosQ, NegQ,
    # Numeric types
    IntegersQ, HalfIntegerQ, FractionQ, RationalQ,
    ComplexNumberQ, RealNumberQ, FractionOrNegativeQ, SqrtNumberQ,
    # Expression types
    PowerQ, ProductQ, SumQ, NonsumQ,
    IntegerPowerQ, FractionalPowerQ,
    # Polynomials
    PolyQ, LinearQ, QuadraticQ, BinomialQ, TrinomialQ,
    LinearMatchQ, QuadraticMatchQ, BinomialMatchQ, TrinomialMatchQ,
    # Trig functions
    TrigQ, HyperbolicQ, InverseTrigQ, InverseHyperbolicQ, LogQ,
    # Free predicates
    ComplexFreeQ, InverseFunctionFreeQ, FractionalPowerFreeQ,
    TrigHyperbolicFreeQ, IntegralFreeQ,
    # Function types
    RationalFunctionQ, AlgebraicFunctionQ, IndependentQ,
    # Simplicity
    SimplerQ, SumSimplerQ,
    # Function of
    FunctionOfQ, PiecewiseLinearQ,
    # Expression constraints
    EqM, ExpressionEqQ,
    # Integration-type predicates
    IntLinearQ, IntBinomialQ, IntQuadraticQ,
    MonomialQ, LinearPairQ,
    # Generalized polynomials
    GeneralizedBinomialQ, GeneralizedBinomialMatchQ,
    GeneralizedTrinomialQ, GeneralizedTrinomialMatchQ,
    # Sqrt predicates
    NiceSqrtQ, SimplerSqrtQ, FractionalPowerFactorQ,
    # Structure predicates
    SumBaseQ, InverseFunctionQ, InertTrigQ, InertTrigFreeQ,
    CalculusFreeQ, QuotientOfLinearsQ,
    PowerOfLinearQ, PowerOfLinearMatchQ,
    FunctionOfExponentialQ,
    # Known integrand types
    KnownSineIntegrandQ, KnownSecantIntegrandQ,
    KnownTangentIntegrandQ, KnownCotangentIntegrandQ,
    EulerIntegrandQ, SubstForFractionalPowerQ,
    # Misc
    PerfectSquareQ, PolynomialInQ, FunctionOfTrigOfLinearQ,
    SimplerIntegrandQ, PseudoBinomialPairQ, QuadraticProductQ,
    EveryQ, TrigSimplifyQ,
)

# Utility functions
from . import rubi_utils
