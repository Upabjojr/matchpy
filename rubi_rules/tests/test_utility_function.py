
from rubi_rules.utils.utility_functions import (eager_Set, eager_With, eager_Module,
                                                eager_Scan, MapAnd, eager_FalseQ, ZeroQ, eager_NegativeQ, NonzeroQ, eager_FreeQ, eager_List, Log,
                                                eager_PositiveQ, PositiveIntegerQ, NegativeIntegerQ, eager_IntegerQ, eager_IntegersQ,
                                                eager_ComplexNumberQ, RealNumericQ, PositiveOrZeroQ,
                                                eager_FractionOrNegativeQ, eager_NegQ, Equal, Unequal, eager_IntPart,
                                                eager_FracPart, eager_RationalQ, eager_ProductQ, eager_SumQ, eager_NonsumQ, eager_First, eager_Rest,
                                                eager_SqrtNumberQ, eager_LinearQ, Sqrt, ArcCosh, eager_Coefficient,
                                                eager_Denominator, eager_Hypergeometric2F1, eager_Not, eager_Simplify, FractionalPart, IntegerPart,
                                                AppellF1, eager_PolynomialQuotient, ArcTan, ArcTanh, ArcSin, ArcSinh, ArcCos,
                                                Sinh, Coth, LessEqual, Less, Greater,
                                                GreaterEqual, eager_FractionQ, IntLinearcQ, Expand, eager_IndependentQ, eager_PowerQ,
                                                eager_IntegerPowerQ, eager_FractionalPowerQ, eager_AtomQ, ExpQ, eager_LogQ,
                                                eager_Head, eager_MemberQ, eager_TrigQ, SinQ, CosQ, TanQ, CotQ, SecQ, CscQ, eager_HyperbolicQ,
                                                SinhQ, CoshQ, TanhQ, CothQ, SechQ, CschQ, eager_InverseTrigQ, SinhCoshQ,
                                                eager_LeafCount, eager_Numerator, eager_NumberQ, eager_NumericQ, eager_Length, ListQ, Im, Re,
                                                eager_InverseHyperbolicQ, eager_InverseFunctionQ, eager_EqQ, eager_FractionalPowerFreeQ,
                                                eager_ComplexFreeQ, eager_PolynomialQ, FactorSquareFree, eager_PowerOfLinearQ, eager_Exponent,
                                                eager_QuadraticQ, eager_LinearPairQ, BinomialParts, TrinomialParts, eager_PolyQ, eager_EvenQ, eager_OddQ,
                                                eager_PerfectSquareQ, NiceSqrtAuxQ, eager_NiceSqrtQ, eager_Together, PosAux, eager_PosQ,
                                                CoefficientList, eager_ReplaceAll, eager_ExpandLinearProduct, eager_GCD, ContentFactor,
                                                NumericFactor, NonnumericFactors, MakeAssocList, GensymSubst, KernelSubst,
                                                eager_ExpandExpression, eager_Apart, SmartApart, eager_MatchQ, PolynomialQuotientRemainder,
                                                eager_FreeFactors, eager_NonfreeFactors, RemoveContentAux, RemoveContent, FreeTerms,
                                                NonfreeTerms, ExpandAlgebraicFunction, CollectReciprocals, ExpandCleanup,
                                                eager_AlgebraicFunctionQ, eager_Coeff, LeadTerm, RemainingTerms, LeadFactor,
                                                RemainingFactors, LeadBase, LeadDegree, eager_Numer, eager_Denom, eager_Expon,
                                                MergeMonomials, eager_PolynomialDivide, eager_BinomialQ, eager_TrinomialQ,
                                                eager_GeneralizedBinomialQ, eager_GeneralizedTrinomialQ, FactorSquareFreeList,
                                                PerfectPowerTest, SquareFreeFactorTest, eager_RationalFunctionQ,
                                                RationalFunctionFactors, NonrationalFunctionFactors, Reverse,
                                                eager_RationalFunctionExponents, eager_RationalFunctionExpand, eager_ExpandIntegrand, eager_SimplerQ,
                                                eager_SimplerSqrtQ, eager_SumSimplerQ, eager_BinomialDegree, eager_TrinomialDegree,
                                                CancelCommonFactors, eager_SimplerIntegrandQ, GeneralizedBinomialDegree,
                                                GeneralizedBinomialParts, eager_GeneralizedTrinomialDegree,
                                                GeneralizedTrinomialParts, eager_MonomialQ, MonomialSumQ, eager_MinimumMonomialExponent,
                                                MonomialExponent, eager_LinearMatchQ, eager_PowerOfLinearMatchQ, eager_QuadraticMatchQ,
                                                CubicMatchQ, eager_BinomialMatchQ, eager_TrinomialMatchQ, eager_GeneralizedBinomialMatchQ,
                                                eager_GeneralizedTrinomialMatchQ, QuotientOfLinearsMatchQ, PolynomialTermQ,
                                                PolynomialTerms, NonpolynomialTerms, PseudoBinomialParts,
                                                eager_NormalizePseudoBinomial, eager_PseudoBinomialPairQ, PseudoBinomialQ,
                                                PolynomialGCD, eager_PolyGCD, AlgebraicFunctionFactors, NonalgebraicFunctionFactors,
                                                QuotientOfLinearsP, eager_QuotientOfLinearsParts, eager_QuotientOfLinearsQ, Flatten,
                                                Sort, AbsurdNumberQ, AbsurdNumberFactors, NonabsurdNumberFactors,
                                                SumSimplerAuxQ, Prepend, Drop, CombineExponents, FactorInteger,
                                                FactorAbsurdNumber, eager_SubstForInverseFunction, SubstForFractionalPower,
                                                eager_SubstForFractionalPowerOfQuotientOfLinears, FractionalPowerOfQuotientOfLinears,
                                                eager_SubstForFractionalPowerQ, SubstForFractionalPowerAuxQ, FractionalPowerOfSquareQ,
                                                FractionalPowerSubexpressionQ, eager_Apply, FactorNumericGcd, MergeableFactorQ,
                                                MergeFactor, MergeFactors, eager_TrigSimplifyQ, eager_TrigSimplify, TrigSimplifyRecur,
                                                Order, FactorOrder, Smallest, OrderedQ, MinimumDegree, PositiveFactors, eager_Sign,
                                                NonpositiveFactors, PolynomialInAuxQ, eager_PolynomialInQ, ExponentInAux, ExponentIn,
                                                PolynomialInSubstAux, eager_PolynomialInSubst, eager_Distrib, DistributeDegree,
                                                FunctionOfPower, DivideDegreesOfFactors, MonomialFactor, eager_FullSimplify,
                                                FunctionOfLinearSubst, eager_FunctionOfLinear, eager_NormalizeIntegrand,
                                                NormalizeIntegrandAux, NormalizeIntegrandFactor, NormalizeIntegrandFactorBase,
                                                NormalizeTogether, NormalizeLeadTermSigns, AbsorbMinusSign,
                                                NormalizeSumFactors, SignOfFactor, eager_NormalizePowerOfLinear,
                                                eager_SimplifyIntegrand, SimplifyTerm, TogetherSimplify, SmartSimplify,
                                                SubstForExpn, eager_ExpandToSum, UnifySum, UnifyTerms, UnifyTerm, CalculusQ,
                                                FunctionOfInverseLinear, PureFunctionOfSinhQ, PureFunctionOfTanhQ,
                                                PureFunctionOfCoshQ, IntegerQuotientQ, OddQuotientQ, EvenQuotientQ,
                                                FindTrigFactor, FunctionOfSinhQ, FunctionOfCoshQ, OddHyperbolicPowerQ,
                                                FunctionOfTanhQ, FunctionOfTanhWeight, FunctionOfHyperbolicQ, SmartNumerator,
                                                SmartDenominator, eager_ActivateTrig, eager_ExpandTrig, TrigExpand,
                                                SubstForTrig, SubstForHyperbolic, eager_InertTrigFreeQ, LCM,
                                                eager_SubstForFractionalPowerOfLinear, FractionalPowerOfLinear,
                                                eager_InverseFunctionOfLinear, eager_InertTrigQ, InertReciprocalQ, eager_DeactivateTrig,
                                                FixInertTrigFunction, DeactivateTrigAux, PowerOfInertTrigSumQ,
                                                eager_PiecewiseLinearQ, KnownTrigIntegrandQ, eager_KnownSineIntegrandQ,
                                                eager_KnownTangentIntegrandQ, eager_KnownCotangentIntegrandQ, eager_KnownSecantIntegrandQ,
                                                eager_TryPureTanSubst, TryTanhSubst, TryPureTanhSubst, AbsurdNumberGCD,
                                                AbsurdNumberGCDList, eager_ExpandTrigExpand, eager_ExpandTrigReduce, ExpandTrigReduceAux,
                                                NormalizeTrig, TrigToExp, eager_ExpandTrigToExp, TrigReduce, eager_FunctionOfTrig,
                                                AlgebraicTrigFunctionQ, FunctionOfHyperbolic, eager_FunctionOfQ, FunctionOfExpnQ,
                                                PureFunctionOfSinQ, PureFunctionOfCosQ, PureFunctionOfTanQ, PureFunctionOfCotQ,
                                                FunctionOfCosQ, FunctionOfSinQ, OddTrigPowerQ, FunctionOfTanQ,
                                                FunctionOfTanWeight, FunctionOfTrigQ, FunctionOfDensePolynomialsQ,
                                                eager_FunctionOfLog, eager_PowerVariableExpn, PowerVariableDegree, PowerVariableSubst,
                                                eager_EulerIntegrandQ, eager_FunctionOfSquareRootOfQuadratic, SquareRootOfQuadraticSubst,
                                                eager_Divides, EasyDQ, ProductOfLinearPowersQ, eager_Rt, NthRoot, AtomBaseQ, eager_SumBaseQ,
                                                NegSumBaseQ, AllNegTermQ, SomeNegTermQ, TrigSquareQ, RtAux, TrigSquare,
                                                eager_IntSum, IntTerm, Map2, ConstantFactor, SameQ, ReplacePart, CommonFactors,
                                                MostMainFactorPosition, eager_FunctionOfExponentialQ, eager_FunctionOfExponential,
                                                eager_FunctionOfExponentialFunction, FunctionOfExponentialFunctionAux,
                                                FunctionOfExponentialTest, FunctionOfExponentialTestAux, stdev, eager_If, eager_IntQuadraticQ, eager_IntBinomialQ, RectifyTangent, RectifyCotangent,
                                                Inequality, eager_Condition, eager_Simp, SimpHelp, eager_SplitProduct, SplitSum, eager_SubstFor,
                                                SubstForAux, FresnelS, FresnelC, Erfc, Erfi, Gamma, eager_FunctionOfTrigOfLinearQ,
                                                ElementaryFunctionQ, eager_Complex, eager_UnsameQ, _SimpFixFactor, Tanh,
                                                eager_DerivativeDivides, SimpFixFactor, _FixSimplify, FixSimplify,
                                                _SimplifyAntiderivativeSum, SimplifyAntiderivativeSum, PureFunctionOfCothQ,
                                                _SimplifyAntiderivative, SimplifyAntiderivative, _TrigSimplifyAux,
                                                TrigSimplifyAux, Cancel, eager_Part, PolyLog, eager_D, eager_Dist, eager_IntegralFreeQ, Sum_doit,
                                                eager_PolynomialRemainder, CoprimeQ, Distribute, ProductLog,
                                                eager_Floor, PolyGamma, process_trig, ExponentList)
# TODO - Add tests for: Int, PureComplexNumberQ, EllipticPi, # ArcCot, ArcCoth, Tanh, Cosh, Sech, Subst,
# SqrtNumberSumQ, Sin, Cos, Tan, Cot, Sec, Csc, Csch, TrigHyperbolicFreeQ,
# InverseFunctionFreeQ, RealQ,

import pytest

from sympy.core.add import Add
from sympy.core.expr import unchanged
from sympy.core.numbers import (E, I, oo, pi, zoo)
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import (symbols, Symbol, Wild)
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.hyperbolic import acosh, asinh, atanh, acsch, cosh, sinh, tanh, coth, sech, csch, acoth
from sympy.functions.elementary.miscellaneous import Min, sqrt
from sympy.functions.elementary.trigonometric import (cos, cot, csc, sec, sin, tan, atan, acsc, asin, acot, acos, asec, atan2)
from sympy.functions.special.error_functions import (Chi, Ci, Ei, Shi, Si, expint, li)
from sympy.functions.special.gamma_functions import (gamma, loggamma, polygamma)
from sympy.functions.special.hyper import hyper
from sympy.functions.special.zeta_functions import (polylog, zeta)
from sympy.integrals.integrals import Integral
from sympy.simplify.simplify import (nsimplify, simplify)


A, B, a, b, c, d, e, f, g, h, y, z, m, n, p, q, u, v, w, F = symbols('A B a b c d e f g h y z m n p q u v w F', real=True, imaginary=False)
x = Symbol('x')

def test_ZeroQ():
    e = b*(n*p + n + 1)
    d = a
    assert ZeroQ(a*e - b*d*(n*(p + S(1)) + S(1)))
    assert ZeroQ(S(0))
    assert not ZeroQ(S(10))
    assert not ZeroQ(S(-2))
    assert ZeroQ(0, 2-2)
    assert ZeroQ([S(2), (4), S(0), S(8)]) == [False, False, True, False]
    assert ZeroQ([S(2), S(4), S(8)]) == [False, False, False]

def test_NonzeroQ():
    assert NonzeroQ(S(1)) == True


def test_PosQ_LinearQ_cached_values_match_rubi():
    """PosQ and LinearQ are memoised (pure predicates, 96-99% call-repeat during the
    DFS). Caching must not change a verdict. The PosQ expectations below were checked
    against real Rubi (``<<Rubi`IntegrationUtilityFunctions``; PosQ[...]``): symbols
    are treated as positive, only explicitly-negated forms are negative.

    NB: PosQ of a SUM (e.g. ``b*c - a*d``) follows Mathematica's canonical term order
    for ``First``, which SymPy does not reproduce, so those are deliberately excluded
    -- a known, pre-existing divergence unrelated to caching.
    """
    from sympy import sqrt, Rational
    from rubi_rules.utils.utility_functions import eager_PosQ, eager_LinearQ
    xx, aa, bb, cc, dd = (Symbol(s) for s in 'x a b c d'.split())
    # `==` not `is`: PosAux returns a SymPy Boolean for numeric inputs (3 > 0), a
    # Python bool for symbolic ones.
    for u, want in [(aa, True), (-aa, False), (aa*bb, True), (-aa*bb, False),
                    (aa**2, True), (S(3), True), (S(-3), False), (aa/bb, True),
                    (sqrt(aa), True), ((aa + bb)**2, True), (-(aa + bb)**2, False),
                    (-xx, False), ((cc/dd)**Rational(1, 3), True)]:
        assert bool(eager_PosQ(u)) == want, (u, eager_PosQ(u), want)
        assert bool(eager_PosQ(u)) == want  # second call hits the cache -> same verdict
    for u, want in [(aa, False), (3*xx + bb, True), (xx**2, False),
                    (aa + bb*xx, True), (sqrt(xx), False)]:
        assert bool(eager_LinearQ(u, xx)) == want, (u, eager_LinearQ(u, xx), want)
        assert bool(eager_LinearQ(u, xx)) == want


def test_ZeroQ_numeric_pretest_is_sound():
    """ZeroQ has a fast numeric pre-test that returns False (nonzero) when the
    expression is provably nonzero at a probe point, skipping the expensive
    sympy.simplify. It must never flip a verdict:
      * generically-nonzero -> False (may take the fast path);
      * identically-zero (even when unexpanded) -> True (falls back to Simplify);
      * nonzero but ZERO at the probe points -> still False (the pre-test declines,
        Simplify decides) -- guards against a probe root causing a wrong `True`.
    """
    from sympy.core.numbers import Rational
    from rubi_rules.utils.utility_functions import _provably_nonzero, _ZEROQ_PROBE_POINTS
    # generically nonzero
    assert ZeroQ(b*c - a*d) is False
    assert _provably_nonzero(b*c - a*d) is True
    # identically zero but not auto-expanded -> pre-test declines, Simplify -> True
    assert ZeroQ((a + b)**2 - a**2 - 2*a*b - b**2) is True
    assert _provably_nonzero((a + b)**2 - a**2 - 2*a*b - b**2) is False
    # a nonzero expression whose ROOTS are exactly the probe points for `a`
    p0 = list(_ZEROQ_PROBE_POINTS[0].values())[0]
    p1 = list(_ZEROQ_PROBE_POINTS[1].values())[0]
    tricky = (a - p0) * (a - p1)          # zero at both probe points, nonzero symbolically
    assert _provably_nonzero(tricky) is False   # pre-test correctly declines
    assert ZeroQ(tricky) is False               # ...and Simplify gives the right answer
    # pure numbers are decided exactly, not by the probe
    assert ZeroQ(S(0)) is True
    assert ZeroQ(S(5)) is False

# FreeQ, PositiveQ, IntegerQ, MemberQ moved to sympy_wolfram (standard Wolfram
# predicates); their eager unit tests live in
# sympy_wolfram/tests/test_mathematica_functions.py.

def test_List():
    assert eager_List(a, b, c) == [a, b, c]


def test_PositiveIntegerQ():
    assert PositiveIntegerQ(S(1))
    assert not PositiveIntegerQ(S(-3))
    assert not PositiveIntegerQ(S(0))

def test_NegativeIntegerQ():
    assert not NegativeIntegerQ(S(1))
    assert NegativeIntegerQ(S(-3))
    assert not NegativeIntegerQ(S(0))

def test_IntegersQ():
    assert eager_IntegersQ(S(1), S(0))
    assert not eager_IntegersQ(S(-1.9), S(1))
    assert not eager_IntegersQ(S(0.0), S(0))
    assert eager_IntegersQ(S(-1), S(0), S(2))

def test_FracPart():
    assert eager_FracPart(S(10)) == 0
    assert eager_FracPart(S(10)+0.5) == 10.5

def test_IntPart():
    assert eager_IntPart(m*n) == 0
    assert eager_IntPart(S(10)) == 10
    assert eager_IntPart(1 + m) == 1

def test_NegQ():
    assert eager_NegQ(-S(3))
    assert not eager_NegQ(S(0))
    assert not eager_NegQ(S(0))

def test_RationalQ():
    assert eager_RationalQ(S(5)/6)
    assert eager_RationalQ(S(5)/6, S(4)/5)
    assert not eager_RationalQ(Sqrt(1.6))
    assert not eager_RationalQ(Sqrt(1.6), S(5)/6)
    assert not eager_RationalQ(log(2))

def test_ArcCosh():
    assert ArcCosh(x) == acosh(x)

def test_LinearQ():
    assert not eager_LinearQ(a, x)
    assert eager_LinearQ(3*x + y**2, x)
    assert not eager_LinearQ(3*x + y**2, y)
    assert not eager_LinearQ(S(3), x)

def test_Sqrt():
    assert Sqrt(x) == sqrt(x)
    assert Sqrt(25) == 5

def test_Util_Coefficient():
    from rubi_rules.utils.utility_functions import Util_Coefficient
    assert unchanged(Util_Coefficient, a + b*x + c*x**3, x, a)
    assert Util_Coefficient(a + b*x + c*x**3, x, 4).doit() == 0

def test_Coefficient():
    assert eager_Coefficient(7 + 2*x + 4*x**3, x, 1) == 2
    assert eager_Coefficient(a + b*x + c*x**3, x, 0) == a
    assert eager_Coefficient(a + b*x + c*x**3, x, 4) == 0
    assert eager_Coefficient(b*x + c*x**3, x, 3) == c
    assert eager_Coefficient(x, x, -1) == 0

# First/Rest/Numerator/Denominator/Part/Apart/Simplify are standard Wolfram functions
# that now live in sympy_wolfram; their behaviour tests moved to
# sympy_wolfram/tests/test_mathematica_functions.py. The Rubi-integration behaviour of
# Simplify (resolving deferred Rubi nodes / Boolean-from-non-binomial) is still tested
# below, since that scenario is Rubi-specific.

def test_Hypergeometric2F1():
    assert eager_Hypergeometric2F1(1, 2, 3, x) == hyper((1, 2), (3,), x)

def test_ArcTan():
    assert ArcTan(x) == atan(x)
    assert ArcTan(x, y) == atan2(x, y)

def test_Not():
    a = 10
    assert eager_Not(a == 2)

def test_FractionalPart():
    assert FractionalPart(S(3.0)) == 0

def test_IntegerPart():
    assert IntegerPart(3.6) == 3
    assert IntegerPart(-3.6) == -3   # Mathematica truncates toward zero

def test_AppellF1():
    assert AppellF1(1,0,0.5,1,0.5,0.25).evalf() == 1.154700538379251529018298
    assert unchanged(AppellF1, a, b, c, d, e, f)

def test_ArcTanh():
    assert ArcTanh(a) == atanh(a)

def test_ArcSin():
    assert ArcSin(a) == asin(a)

def test_ArcSinh():
    assert ArcSinh(a) == asinh(a)

def test_ArcCos():
    assert ArcCos(a) == acos(a)

def test_Equal():
    assert Equal(a, a)
    assert not Equal(a, b)

def test_LessEqual():
    assert LessEqual(1, 2, 3)
    assert LessEqual(1, 1)
    assert not LessEqual(3, 2, 1)

def test_With():
    assert eager_With(eager_Set(x, 3), x + y) == 3 + y
    assert eager_With(eager_List(eager_Set(x, 3), eager_Set(y, c)), x + y) == 3 + c

def test_Module():
    # Same as With
    assert eager_Module(eager_Set(x, 3), x + y) == 3 + y
    assert eager_Module(eager_List(eager_Set(x, 3), eager_Set(y, c)), x + y) == 3 + c

def test_Less():
    assert Less(1, 2, 3)
    assert not Less(1, 1, 3)

def test_Greater():
    assert Greater(3, 2, 1)
    assert not Greater(3, 2, 2)

def test_GreaterEqual():
    assert GreaterEqual(3, 2, 1)
    assert GreaterEqual(3, 2, 2)
    assert not GreaterEqual(2, 3)

def test_Unequal():
    assert Unequal(1, 2)
    assert not Unequal(1, 1)

def test_FractionQ():
    assert not eager_FractionQ(S('3'))
    assert eager_FractionQ(S('3')/S('2'))

def test_Expand():
    assert Expand((1 + x)**10) == x**10 + 10*x**9 + 45*x**8 + 120*x**7 + 210*x**6 + 252*x**5 + 210*x**4 + 120*x**3 + 45*x**2 + 10*x + 1

def test_Scan():
    assert list(eager_Scan(sin, [a, b])) == [sin(a), sin(b)]

def test_MapAnd():
    assert MapAnd(eager_PositiveQ, [S(1), S(2), S(3), S(0)]) == False
    assert MapAnd(eager_PositiveQ, [S(1), S(2), S(3)]) == True

def test_FalseQ():
    assert eager_FalseQ(True) == False
    assert eager_FalseQ(False) == True

def test_ComplexNumberQ():
    assert eager_ComplexNumberQ(1 + I*2, I) == True
    assert eager_ComplexNumberQ(a + b, I) == False

def test_Re():
    assert Re(1 + I) == 1

def test_Im():
    assert Im(1 + 2*I) == 2
    assert Im(a*I) == a

def test_PositiveOrZeroQ():
    assert PositiveOrZeroQ(S(0)) == True
    assert PositiveOrZeroQ(S(1)) == True
    assert PositiveOrZeroQ(-S(1)) == False

def test_RealNumericQ():
    assert RealNumericQ(S(1)) == True
    assert RealNumericQ(-S(1)) == True

def test_FractionOrNegativeQ():
    assert eager_FractionOrNegativeQ(S(1)/2) == True
    assert eager_FractionOrNegativeQ(-S(1)) == True
    assert eager_FractionOrNegativeQ(-S(1)/2) == True
    assert eager_FractionOrNegativeQ(S(1)) == False

def test_NegativeQ():
    assert eager_NegativeQ(-S(1)) == True
    assert eager_NegativeQ(S(1)) == False
    assert eager_NegativeQ(oo) == False

def test_ProductQ():
    assert eager_ProductQ(a*b) == True
    assert eager_ProductQ(a + b) == False

def test_SumQ():
    assert eager_SumQ(a*b) == False
    assert eager_SumQ(a + b) == True

def test_NonsumQ():
    assert eager_NonsumQ(a*b) == True
    assert eager_NonsumQ(a + b) == False

def test_SqrtNumberQ():
    assert eager_SqrtNumberQ(sqrt(2)) == True

def test_IntLinearcQ():
    assert IntLinearcQ(1, 2, 3, 4, 5, 6, x) == True
    assert IntLinearcQ(S(1)/100, S(2)/100, S(3)/100, S(4)/100, S(5)/100, S(6)/100, x) == False

def test_IndependentQ():
    assert eager_IndependentQ(a + b*x, x) == False
    assert eager_IndependentQ(a + b, x) == True

def test_PowerQ():
    assert eager_PowerQ(a**b) == True
    assert eager_PowerQ(a + b) == False

def test_IntegerPowerQ():
    assert eager_IntegerPowerQ(a**2) == True
    assert eager_IntegerPowerQ(a**0.5) == False

def test_FractionalPowerQ():
    assert eager_FractionalPowerQ(a**(S(2)/S(3)))
    assert eager_FractionalPowerQ(a**sqrt(2)) == False

# test_AtomQ moved to sympy_wolfram/tests/test_mathematica_functions.py::test_eager_AtomQ
# (AtomQ is a standard Wolfram predicate, now defined in sympy_wolfram).

def test_ExpQ():
    assert ExpQ(E**2)
    assert not ExpQ(2**E)

def test_LogQ():
    assert eager_LogQ(log(x))
    assert not eager_LogQ(sin(x) + log(x))

def test_Head():
    assert eager_Head(sin(x)) == sin
    assert eager_Head(log(x**3 + 3)) == log

# test_MemberQ (plain membership) and the MemberQ head-wildcard assertions moved to
# sympy_wolfram/tests/test_mathematica_functions.py (MemberQ now lives in that layer).


def test_TrigQ_InverseTrigQ_head_wildcard_matches_by_class():
    """A function-head wildcard F_[...] binds its head to a HeadRef; the Rubi trig
    classifiers (which pass bare function classes to MemberQ) must still fire on such a
    head. Regression: these head-checks otherwise silently failed and the FHW rule
    never fired. Plain MemberQ head-matching is covered in the sympy_wolfram tests."""
    from sympy_matching.wild import HeadRef
    from sympy import asin
    assert eager_TrigQ(HeadRef(sin))
    assert eager_InverseTrigQ(HeadRef(asin))

def test_TrigQ():
    assert eager_TrigQ(sin(x))
    assert eager_TrigQ(tan(x**2 + 2))
    assert not eager_TrigQ(sin(x) + tan(x))

def test_SinQ():
    assert SinQ(sin(x))
    assert not SinQ(tan(x))

def test_CosQ():
    assert CosQ(cos(x))
    assert not CosQ(csc(x))

def test_TanQ():
    assert TanQ(tan(x))
    assert not TanQ(cot(x))

def test_CotQ():
    assert not CotQ(tan(x))
    assert CotQ(cot(x))

def test_SecQ():
    assert SecQ(sec(x))
    assert not SecQ(csc(x))

def test_CscQ():
    assert not CscQ(sec(x))
    assert CscQ(csc(x))

def test_HyperbolicQ():
    assert eager_HyperbolicQ(sinh(x))
    assert eager_HyperbolicQ(cosh(x))
    assert eager_HyperbolicQ(tanh(x))
    assert not eager_HyperbolicQ(sinh(x) + cosh(x) + tanh(x))

def test_SinhQ():
    assert SinhQ(sinh(x))
    assert not SinhQ(cosh(x))

def test_CoshQ():
    assert not CoshQ(sinh(x))
    assert CoshQ(cosh(x))

def test_TanhQ():
    assert TanhQ(tanh(x))
    assert not TanhQ(coth(x))

def test_CothQ():
    assert not CothQ(tanh(x))
    assert CothQ(coth(x))

def test_SechQ():
    assert SechQ(sech(x))
    assert not SechQ(csch(x))

def test_CschQ():
    assert not CschQ(sech(x))
    assert CschQ(csch(x))

def test_InverseTrigQ():
    assert eager_InverseTrigQ(acot(x))
    assert eager_InverseTrigQ(asec(x))
    assert not eager_InverseTrigQ(acsc(x) + asec(x))

def test_SinhCoshQ():
    assert not SinhCoshQ(sin(x))
    assert SinhCoshQ(cosh(x))
    assert SinhCoshQ(sech(x))
    assert SinhCoshQ(csch(x))

def test_LeafCount():
    assert eager_LeafCount(1 + a + x**2) == 6

def test_Length():
    assert eager_Length(a + b) == 2
    assert eager_Length(sin(a)*cos(a)) == 2

def test_ListQ():
    assert ListQ([1, 2])
    assert not ListQ(a)

def test_InverseHyperbolicQ():
    assert eager_InverseHyperbolicQ(acosh(a))

def test_InverseFunctionQ():
    assert eager_InverseFunctionQ(log(a))
    assert eager_InverseFunctionQ(acos(a))
    assert not eager_InverseFunctionQ(a)
    assert eager_InverseFunctionQ(acosh(a))
    assert eager_InverseFunctionQ(polylog(a, b))

def test_EqQ():
    assert eager_EqQ(a, a)
    assert not eager_EqQ(a, b)


def test_EqQ_head_wildcard_identity():
    """EqQ[F, Sin] on a function-head wildcard F (bound to a HeadRef) compares by the
    underlying class. The codegen emits the head literal as HeadRef(sympy.sin), so both
    sides are HeadRefs; comparing by class avoids subtracting two unequal symbols.
    Regression for FHW rules gated on a specific head."""
    from sympy_matching.wild import HeadRef
    from sympy import sin, cos, tan
    assert eager_EqQ(HeadRef(sin), HeadRef(sin))
    assert eager_EqQ(HeadRef(tan), HeadRef(tan))
    assert not eager_EqQ(HeadRef(sin), HeadRef(cos))
    # ordinary EqQ unaffected
    assert eager_EqQ(a + b, b + a)
    assert not eager_EqQ(x, 2 * x)

def test_FactorSquareFree():
    assert FactorSquareFree(x**5 - x**3 - x**2 + 1) == (x**3 + 2*x**2 + 2*x + 1)*(x - 1)**2

def test_FactorSquareFreeList():
    assert FactorSquareFreeList(x**5-x**3-x**2 + 1) == [[1, 1], [x**3 + 2*x**2 + 2*x + 1, 1], [x - 1, 2]]
    assert FactorSquareFreeList(x**4 - 2*x**2 + 1) == [[1, 1], [x**2 - 1, 2]]

def test_PerfectPowerTest():
    assert not PerfectPowerTest(sqrt(x), x)
    assert not PerfectPowerTest(x**5-x**3-x**2 + 1, x)
    assert PerfectPowerTest(x**4 - 2*x**2 + 1, x) == (x**2 - 1)**2

def test_SquareFreeFactorTest():
    assert not SquareFreeFactorTest(sqrt(x), x)
    assert SquareFreeFactorTest(x**5 - x**3 - x**2 + 1, x) == (x**3 + 2*x**2 + 2*x + 1)*(x - 1)**2

def test_ComplexFreeQ():
    assert eager_ComplexFreeQ(a)
    assert not eager_ComplexFreeQ(a + 2*I)

def test_FractionalPowerFreeQ():
    assert not eager_FractionalPowerFreeQ(x**(S(2)/3))
    assert eager_FractionalPowerFreeQ(x)

# ExponentList is Rubi-specific and stays here; Exponent itself moved to
# sympy_wolfram (behaviour tested in test_mathematica_functions.py).
def test_ExponentList():
    assert Min(*ExponentList(x**2 + x + 1 + 5, x)) == 0
    assert ExponentList(x**2 + x + 1 + 5, x) == [0, 1, 2]
    assert ExponentList(x**2 + x + 1, x) == [0, 1, 2]
    assert ExponentList(x**2 + 2*x + 1, x) == [0, 1, 2]
    assert ExponentList(x**3, x) == [3]

def test_Expon():
    assert eager_Expon(x**2+2*x+1, x) == 2

def test_QuadraticQ():
    assert not eager_QuadraticQ([x**2+x+1, 5*x**2], x)
    assert eager_QuadraticQ([x**2+x+1, 5*x**2+3*x+6], x)
    assert not eager_QuadraticQ(x**2+1+x**3, x)
    assert eager_QuadraticQ(x**2+1+x, x)
    assert not eager_QuadraticQ(x**2, x)
    assert not eager_QuadraticQ(sin(x), x)
    assert not eager_QuadraticQ([sin(x), cos(x)], x)

def test_BinomialQ():
    assert eager_BinomialQ(x**9, x)
    assert not eager_BinomialQ((1 + x)**3, x)

def test_BinomialParts():
    assert BinomialParts(2 + x*(9*x), x) == [2, 9, 2]
    assert BinomialParts(x**9, x) == [0, 1, 9]
    assert BinomialParts(2*x**3, x) == [0, 2, 3]
    assert BinomialParts(2 + x, x) == [2, 1, 1]

def test_BinomialDegree():
    assert eager_BinomialDegree(b + 2*c*x**n, x) == n
    assert eager_BinomialDegree(2 + x*(9*x), x) == 2
    assert eager_BinomialDegree(x**9, x) == 9

# test_PolynomialQ moved to sympy_wolfram/tests/test_mathematica_functions.py::test_eager_PolynomialQ
# (PolynomialQ is a standard Wolfram predicate, now defined in sympy_wolfram).

def test_PolyQ():
    assert eager_PolyQ(-2*a*d**3*e**2 + x**6*(a*e**5 - b*d*e**4 + c*d**2*e**3)\
        + x**4*(-2*a*d*e**4 + 2*b*d**2*e**3 - 2*c*d**3*e**2) + x**2*(2*a*d**2*e**3 - 2*b*d**3*e**2), x)
    assert not eager_PolyQ(1/sqrt(a + b*x**2 - c*x**4), x**2)
    assert eager_PolyQ(x, x, 1)
    assert eager_PolyQ(x**2, x, 2)
    assert not eager_PolyQ(x**3, x, 2)

def test_EvenQ():
    assert eager_EvenQ(S(2))
    assert not eager_EvenQ(S(1))

def test_OddQ():
    assert eager_OddQ(S(1))
    assert not eager_OddQ(S(2))

def test_PerfectSquareQ():
    assert eager_PerfectSquareQ(S(4))
    assert eager_PerfectSquareQ(a**S(2)*b**S(4))
    assert not eager_PerfectSquareQ(S(1)/3)

def test_NiceSqrtQ():
    assert eager_NiceSqrtQ(S(1)/3)
    assert not eager_NiceSqrtQ(-S(1))
    assert eager_NiceSqrtQ(pi**2)
    assert eager_NiceSqrtQ(pi**2*sin(4)**4)
    assert not eager_NiceSqrtQ(pi**2*sin(4)**3)

def test_Together():
    assert eager_Together(1/a + b/2) == (a*b + 2)/(2*a)

def test_PosQ():
    #assert not PosQ((b*e - c*d)/(c*e))
    assert not eager_PosQ(S(0))
    assert eager_PosQ(S(1))
    assert eager_PosQ(pi)
    assert eager_PosQ(pi**3)
    assert eager_PosQ((-pi)**4)
    assert eager_PosQ(sin(1)**2*pi**4)

def test_NumericQ():
    assert eager_NumericQ(sin(cos(2)))

# test_NumberQ moved to sympy_wolfram/tests/test_mathematica_functions.py::test_eager_NumberQ
# (NumberQ is a standard Wolfram predicate, now defined in sympy_wolfram). The SignOfFactor
# interaction it guards is still covered by test_SignOfFactor_complex_numeric_factor below.

def test_CoefficientList():
    assert CoefficientList(1 + a*x, x) == [1, a]
    assert CoefficientList(1 + a*x**3, x) == [1, 0, 0, a]
    assert CoefficientList(sqrt(x), x) == []

def test_ReplaceAll():
    assert eager_ReplaceAll(x, {x: a}) == a
    assert eager_ReplaceAll(a*x, {x: a + b}) == a*(a + b)
    assert eager_ReplaceAll(a*x, {a: b, x: a + b}) == b*(a + b)

def test_ExpandLinearProduct():
    assert eager_ExpandLinearProduct(log(x), x**2, a, b, x) == a**2*log(x)/b**2 - 2*a*(a + b*x)*log(x)/b**2 + (a + b*x)**2*log(x)/b**2
    assert eager_ExpandLinearProduct((a + b*x)**n, x**3, a, b, x) == -a**3*(a + b*x)**n/b**3 + 3*a**2*(a + b*x)**(n + 1)/b**3 - 3*a*(a + b*x)**(n + 2)/b**3 + (a + b*x)**(n + 3)/b**3

def test_PolynomialDivide():
    assert eager_PolynomialDivide((a*c - b*c*x)**2, (a + b*x)**2, x) == -4*a*b*c**2*x/(a + b*x)**2 + c**2
    assert eager_PolynomialDivide(x + x**2, x, x) == x + 1
    assert eager_PolynomialDivide((1 + x)**3, (1 + x)**2, x) == x + 1
    assert eager_PolynomialDivide((a + b*x)**3, x**3, x) == a*(a**2 + 3*a*b*x + 3*b**2*x**2)/x**3 + b**3
    assert eager_PolynomialDivide(x**3*(a + b*x), S(1), x) == b*x**4 + a*x**3
    assert eager_PolynomialDivide(x**6, (a + b*x)**2, x) == -a**5*(5*a + 6*b*x)/(b**6*(a + b*x)**2) + 5*a**4/b**6 - 4*a**3*x/b**5 + 3*a**2*x**2/b**4 - 2*a*x**3/b**3 + x**4/b**2

def test_MatchQ():
    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x])
    c_ = Wild('c', exclude=[x])
    assert eager_MatchQ(a*b + c, a_*b_ + c_, a_, b_, c_) == (a, b, c)

def test_PolynomialQuotientRemainder():
    assert PolynomialQuotientRemainder(x**2, x+a, x) == [-a + x, a**2]

def test_FreeFactors():
    assert eager_FreeFactors(a, x) == a
    assert eager_FreeFactors(x + a, x) == 1
    assert eager_FreeFactors(a*b*x, x) == a*b

def test_NonfreeFactors():
    assert eager_NonfreeFactors(a, x) == 1
    assert eager_NonfreeFactors(x + a, x) == x + a
    assert eager_NonfreeFactors(a*b*x, x) == x

def test_FreeTerms():
    assert FreeTerms(a, x) == a
    assert FreeTerms(x*a, x) == 0
    assert FreeTerms(a*x + b, x) == b

def test_NonfreeTerms():
    assert NonfreeTerms(a, x) == 0
    assert NonfreeTerms(a*x, x) == a*x
    assert NonfreeTerms(a*x + b, x) == a*x

def test_RemoveContent():
    assert RemoveContent(a + b*x, x) == a + b*x

def test_ExpandAlgebraicFunction():
    assert ExpandAlgebraicFunction((a + b)*x, x) == a*x + b*x
    assert ExpandAlgebraicFunction((a + b)**2*x, x)== a**2*x + 2*a*b*x + b**2*x
    assert ExpandAlgebraicFunction((a + b)**2*x**2, x) == a**2*x**2 + 2*a*b*x**2 + b**2*x**2

def test_CollectReciprocals():
    assert CollectReciprocals(-1/(1 + 1*x) - 1/(1 - 1*x), x) == -2/(-x**2 + 1)
    assert CollectReciprocals(1/(1 + 1*x) - 1/(1 - 1*x), x) == -2*x/(-x**2 + 1)

def test_ExpandCleanup():
    assert ExpandCleanup(a + b, x) == a*(1 + b/a)
    assert ExpandCleanup(b**2/(a**2*(a + b*x)**2) + 1/(a**2*x**2) + 2*b**2/(a**3*(a + b*x)) - 2*b/(a**3*x), x) == b**2/(a**2*(a + b*x)**2) + 1/(a**2*x**2) + 2*b**2/(a**3*(a + b*x)) - 2*b/(a**3*x)

def test_AlgebraicFunctionQ():
    assert not eager_AlgebraicFunctionQ(1/(a + c*x**(2*n)), x)
    assert eager_AlgebraicFunctionQ(a, x) == True
    assert eager_AlgebraicFunctionQ(a*b, x) == True
    assert eager_AlgebraicFunctionQ(x**2, x) == True
    assert eager_AlgebraicFunctionQ(x**2*a, x) == True
    assert eager_AlgebraicFunctionQ(x**2 + a, x) == True
    assert eager_AlgebraicFunctionQ(sin(x), x) == False
    assert eager_AlgebraicFunctionQ([], x) == True
    assert eager_AlgebraicFunctionQ([a, a*b], x) == True
    assert eager_AlgebraicFunctionQ([sin(x)], x) == False

def test_MonomialQ():
    assert not eager_MonomialQ(2*x**7 + 6, x)
    assert eager_MonomialQ(2*x**7, x)
    assert not eager_MonomialQ(2*x**7 + 5*x**3, x)
    assert not eager_MonomialQ([2*x**7 + 6, 2*x**7], x)
    assert eager_MonomialQ([2*x**7, 5*x**3], x)

def test_MonomialSumQ():
    assert MonomialSumQ(2*x**7 + 6, x) == True
    assert MonomialSumQ(x**2 + x**3 + 5*x, x) == True

def test_MinimumMonomialExponent():
    assert eager_MinimumMonomialExponent(x**2 + 5*x**2 + 3*x**5, x) == 2
    assert eager_MinimumMonomialExponent(x**2 + 5*x**2 + 1, x) == 0

def test_MonomialExponent():
    assert MonomialExponent(3*x**7, x) == 7
    assert not MonomialExponent(3+x**3, x)

def test_LinearMatchQ():
    assert eager_LinearMatchQ(2 + 3*x, x)
    assert eager_LinearMatchQ(3*x, x)
    assert not eager_LinearMatchQ(3*x**2, x)

def test_SimplerQ():
    a1, b1 = symbols('a1 b1')
    assert eager_SimplerQ(a1, b1)

    assert eager_SimplerQ(2*a, a + 2)
    assert eager_SimplerQ(2, x)
    assert not eager_SimplerQ(x**2, x)
    assert eager_SimplerQ(2*x, x + 2 + 6*x**3)

def test_GeneralizedTrinomialParts():
    assert not GeneralizedTrinomialParts((7 + 2*x**6 + 3*x**12), x)
    assert GeneralizedTrinomialParts(x**2 + x**3 + x**4, x) == [1, 1, 1, 3, 2]
    assert not GeneralizedTrinomialParts(2*x + 3*x + 4*x, x)

def test_TrinomialQ():
    assert eager_TrinomialQ((7 + 2*x**6 + 3*x**12), x)
    assert not eager_TrinomialQ(x**2, x)

def test_GeneralizedTrinomialDegree():
    assert not eager_GeneralizedTrinomialDegree((7 + 2*x**6 + 3*x**12), x)
    assert eager_GeneralizedTrinomialDegree(x**2 + x**3 + x**4, x) == 1

def test_GeneralizedBinomialParts():
    assert GeneralizedBinomialParts(3*x*(3 + x**6), x) == [9, 3, 7, 1]
    assert GeneralizedBinomialParts((3*x + x**7), x) == [3, 1, 7, 1]

def test_GeneralizedBinomialDegree():
    assert GeneralizedBinomialDegree(3*x*(3 + x**6), x) == 6
    assert GeneralizedBinomialDegree((3*x + x**7), x) == 6

def test_PowerOfLinearQ():
    assert eager_PowerOfLinearQ((6*x), x)
    assert not eager_PowerOfLinearQ((3 + 6*x**3), x)
    assert eager_PowerOfLinearQ((3 + 6*x)**3, x)

def test_LinearPairQ():
    assert not eager_LinearPairQ(6*x**2 + 4, 3*x**2 + 2, x)
    assert eager_LinearPairQ(6*x + 4, 3*x + 2, x)
    assert not eager_LinearPairQ(6*x, 3*x + 2, x)
    assert eager_LinearPairQ(6*x, 3*x, x)

def test_LeadTerm():
    assert LeadTerm(a*b*c) == a*b*c
    assert LeadTerm(a + b + c) == a

def test_RemainingTerms():
    assert RemainingTerms(a*b*c) == a*b*c
    assert RemainingTerms(a + b + c) == b + c

def test_LeadFactor():
    assert LeadFactor(a*b*c) == a
    assert LeadFactor(a + b + c) == a + b + c
    assert LeadFactor(b*I) == I
    assert LeadFactor(c*a**b) == a**b
    assert LeadFactor(S(2)) == S(2)

def test_RemainingFactors():
    assert RemainingFactors(a*b*c) == b*c
    assert RemainingFactors(a + b + c) == 1
    assert RemainingFactors(a*I) == a

def test_LeadBase():
    assert LeadBase(a**b) == a
    assert LeadBase(a**b*c) == a

def test_LeadDegree():
    assert LeadDegree(a**b) == b
    assert LeadDegree(a**b*c) == b

def test_Numer():
    assert eager_Numer(a/b) == a
    assert eager_Numer(a**(-2)) == 1
    assert eager_Numer(a**(-2)*a/b) == 1

def test_Denom():
    assert eager_Denom(a/b) == b
    assert eager_Denom(a**(-2)) == a**2
    assert eager_Denom(a**(-2)*a/b) == a*b

def test_Coeff():
    assert eager_Coeff(7 + 2*x + 4*x**3, x, 1) == 2
    assert eager_Coeff(a + b*x + c*x**3, x, 0) == a
    assert eager_Coeff(a + b*x + c*x**3, x, 4) == 0
    assert eager_Coeff(b*x + c*x**3, x, 3) == c

def test_MergeMonomials():
    assert MergeMonomials(x**2*(1 + 1*x)**3*(1 + 1*x)**n, x) == x**2*(x + 1)**(n + 3)
    assert MergeMonomials(x**2*(1 + 1*x)**2*(1*(1 + 1*x)**1)**2, x) == x**2*(x + 1)**4
    assert MergeMonomials(b**2/a**3, x) == b**2/a**3

def test_RationalFunctionQ():
    assert eager_RationalFunctionQ(a, x)
    assert eager_RationalFunctionQ(x**2, x)
    assert eager_RationalFunctionQ(x**3 + x**4, x)
    assert eager_RationalFunctionQ(x**3*S(2), x)
    assert not eager_RationalFunctionQ(x**3 + x**(0.5), x)
    assert not eager_RationalFunctionQ(x**(S(2)/3)*(a + b*x)**2, x)

# Apart moved to sympy_wolfram (behaviour tested there). It used to gate on Rubi's
# RationalFunctionQ; the relocated version uses SymPy's is_rational_function. This test
# stays here (RationalFunctionQ is Rubi-specific) and documents that the swap is safe:
# the two predicates agree, so Apart's behaviour is unchanged.
def test_Apart_guard_matches_RationalFunctionQ():
    cases = [1/(x*(x + 1)), x + sqrt(x), sin(x)/(x + 1),
             x**3/(a + b*x), 1/x + x, (a + b*x)/(c + x**2)]
    for u in cases:
        assert bool(eager_RationalFunctionQ(u, x)) == bool(u.is_rational_function(x))

def test_RationalFunctionFactors():
    assert RationalFunctionFactors(a, x) == a
    assert RationalFunctionFactors(sqrt(x), x) == 1
    assert RationalFunctionFactors(x*x**3, x) == x*x**3
    assert RationalFunctionFactors(x*sqrt(x), x) == 1

def test_NonrationalFunctionFactors():
    assert NonrationalFunctionFactors(x, x) == 1
    assert NonrationalFunctionFactors(sqrt(x), x) == sqrt(x)
    assert NonrationalFunctionFactors(sqrt(x)*log(x), x) == sqrt(x)*log(x)

def test_Reverse():
    assert Reverse([1, 2, 3]) == [3, 2, 1]
    assert Reverse(a**b) == b**a

def test_RationalFunctionExponents():
    assert eager_RationalFunctionExponents(sqrt(x), x) == [0, 0]
    assert eager_RationalFunctionExponents(a, x) == [0, 0]
    assert eager_RationalFunctionExponents(x, x) == [1, 0]
    assert eager_RationalFunctionExponents(x**(-1), x)== [0, 1]
    assert eager_RationalFunctionExponents(x**(-1)*a, x) == [0, 1]
    assert eager_RationalFunctionExponents(x**(-1) + a, x) == [1, 1]

def test_PolynomialGCD():
    assert PolynomialGCD(x**2 - 1, x**2 - 3*x + 2) == x - 1

def test_PolyGCD():
    assert eager_PolyGCD(x**2 - 1, x**2 - 3*x + 2, x) == x - 1

def test_AlgebraicFunctionFactors():
    assert AlgebraicFunctionFactors(sin(x)*x, x) == x
    assert AlgebraicFunctionFactors(sin(x), x) == 1
    assert AlgebraicFunctionFactors(x, x) == x

def test_NonalgebraicFunctionFactors():
    assert NonalgebraicFunctionFactors(sin(x)*x, x) == sin(x)
    assert NonalgebraicFunctionFactors(sin(x), x) == sin(x)
    assert NonalgebraicFunctionFactors(x, x) == 1

def test_QuotientOfLinearsP():
    assert QuotientOfLinearsP((a + b*x)/(x), x)
    assert QuotientOfLinearsP(x*a, x)
    assert not QuotientOfLinearsP(x**2*a, x)
    assert not QuotientOfLinearsP(x**2 + a, x)
    assert QuotientOfLinearsP(x + a, x)
    assert QuotientOfLinearsP(x, x)
    assert QuotientOfLinearsP(1 + x, x)

def test_QuotientOfLinearsParts():
    assert eager_QuotientOfLinearsParts((b*x)/(c), x) == [0, b/c, 1, 0]
    assert eager_QuotientOfLinearsParts((b*x)/(c + x), x) == [0, b, c, 1]
    assert eager_QuotientOfLinearsParts((b*x)/(c + d*x), x) == [0, b, c, d]
    assert eager_QuotientOfLinearsParts((a + b*x)/(c + d*x), x) == [a, b, c, d]
    assert eager_QuotientOfLinearsParts(x**2 + a, x) == [a + x**2, 0, 1, 0]
    assert eager_QuotientOfLinearsParts(a/x, x) == [a, 0, 0, 1]
    assert eager_QuotientOfLinearsParts(1/x, x) == [1, 0, 0, 1]
    assert eager_QuotientOfLinearsParts(a*x + 1, x) == [1, a, 1, 0]
    assert eager_QuotientOfLinearsParts(x, x) == [0, 1, 1, 0]
    assert eager_QuotientOfLinearsParts(a, x) == [a, 0, 1, 0]

def test_QuotientOfLinearsQ():
    assert not eager_QuotientOfLinearsQ((a + x), x)
    assert eager_QuotientOfLinearsQ((a + x)/(x), x)
    assert eager_QuotientOfLinearsQ((a + b*x)/(x), x)

def test_Flatten():
    assert Flatten([a, b, [c, [d, e]]]) == [a, b, c, d, e]

def test_Sort():
    assert Sort([b, a, c]) == [a, b, c]
    assert Sort([b, a, c], True) == [c, b, a]

def test_AbsurdNumberQ():
    assert AbsurdNumberQ(S(1))
    assert not AbsurdNumberQ(a*x)
    assert not AbsurdNumberQ(a**(S(1)/2))
    assert AbsurdNumberQ((S(1)/3)**(S(1)/3))

def test_AbsurdNumberFactors():
    assert AbsurdNumberFactors(S(1)) == S(1)
    assert AbsurdNumberFactors((S(1)/3)**(S(1)/3)) == S(3)**(S(2)/3)/S(3)
    assert AbsurdNumberFactors(a) == S(1)

def test_NonabsurdNumberFactors():
    assert NonabsurdNumberFactors(a) == a
    assert NonabsurdNumberFactors(S(1)) == S(1)
    assert NonabsurdNumberFactors(a*S(2)) == a

def test_NumericFactor():
    assert NumericFactor(S(1)) == S(1)
    assert NumericFactor(1*I) == S(1)
    assert NumericFactor(S(1) + I) == S(1)
    assert NumericFactor(a**(S(1)/3)) == S(1)
    assert NumericFactor(a*S(3)) == S(3)
    assert NumericFactor(a + b) == S(1)
    # Radical / symbolic-constant arguments are NOT Mathematica numbers, so they take
    # the Sum/Power branch. Cross-checked vs real Rubi (ssh pi):
    assert NumericFactor((S(1)/3)**(S(1)/3)) == Rational(1, 3)   # MMA: 1/3
    assert NumericFactor(pi) == S(1)                              # MMA: 1


def test_NumericFactor_complex_value_returns_real():
    """Regression: NumericFactor of a Plus-of-Powers that is REALLY a real number
    (e.g. -(-1)^(3/4)+(-1)^(1/4), which equals Sqrt[2]) must not be mistaken for an
    explicit complex number. Mathematica returns 1 here (NumberQ is False -> Sum branch),
    and the old SymPy is_number path returned the complex-looking value and crashed a
    later `< 0` test. Cross-checked vs real Rubi (ssh pi)."""
    val = -(-1)**(S(3)/4) + (-1)**(S(1)/4)
    assert NumericFactor(val) == S(1)

def test_NonnumericFactors():
    assert NonnumericFactors(S(3)) == S(1)
    assert NonnumericFactors(I) == I
    assert NonnumericFactors(S(3) + I) == S(3) + I
    # (1/3)^(1/3) is a radical (NOT a Mathematica number), so its numeric factor is 1/3
    # and the non-numeric part is 3^(2/3) -- cross-checked against real Rubi (ssh pi).
    # (Previously NumberQ wrongly accepted the radical and this returned 1.)
    assert NonnumericFactors((S(1)/3)**(S(1)/3)) == S(3)**(S(2)/3)
    assert NonnumericFactors(log(a)) == log(a)

def test_Prepend():
    assert Prepend([1, 2, 3], [4, 5]) == [4, 5, 1, 2, 3]

def test_SumSimplerQ():
    assert not eager_SumSimplerQ(S(4 + x),S(3 + x**3))
    assert eager_SumSimplerQ(S(4 + x), S(3 - x))

def test_SumSimplerAuxQ():
    assert SumSimplerAuxQ(S(4 + x), S(3 - x))
    assert not SumSimplerAuxQ(S(4), S(3))

def test_SimplerSqrtQ():
    assert eager_SimplerSqrtQ(S(2), S(16*x**3))
    assert not eager_SimplerSqrtQ(S(x*2), S(16))
    assert not eager_SimplerSqrtQ(S(-4), S(16))
    assert eager_SimplerSqrtQ(S(4), S(16))
    assert not eager_SimplerSqrtQ(S(4), S(0))

def test_TrinomialParts():
    assert TrinomialParts((1 + 5*x**3)**2, x) == [1, 10, 25, 3]
    assert TrinomialParts(1 + 5*x**3 + 2*x**6, x) == [1, 5, 2, 3]
    assert TrinomialParts(((1 + 5*x**3)**2) + 6, x) == [7, 10, 25, 3]
    assert not TrinomialParts(1 + 5*x**3 + 2*x**5, x)

def test_TrinomialDegree():
    assert eager_TrinomialDegree((7 + 2*x**6)**2, x) == 6
    assert eager_TrinomialDegree(1 + 5*x**3 + 2*x**6, x) == 3
    assert not eager_TrinomialDegree(1 + 5*x**3 + 2*x**5, x)

def test_CubicMatchQ():
    assert not CubicMatchQ(S(3 + x**6), x)
    assert CubicMatchQ(S(x**3), x)
    assert not CubicMatchQ(S(3), x)
    assert CubicMatchQ(S(3 + x**3), x)
    assert CubicMatchQ(S(3 + x**3 + 2*x), x)

def test_BinomialMatchQ():
    assert eager_BinomialMatchQ(x, x)
    assert eager_BinomialMatchQ(2 + 3*x**5, x)
    assert eager_BinomialMatchQ(3*x**5, x)
    assert eager_BinomialMatchQ(3*x, x)
    assert not eager_BinomialMatchQ(x + x**2 + x**3, x)

def test_TrinomialMatchQ():
    assert not eager_TrinomialMatchQ((5 + 2*x**6)**2, x)
    assert not eager_TrinomialMatchQ((7 + 8*x**6), x)
    assert eager_TrinomialMatchQ((7 + 2*x**6 + 3*x**3), x)
    assert eager_TrinomialMatchQ(b*x**2 + c*x**4, x)

def test_GeneralizedBinomialMatchQ():
    assert not eager_GeneralizedBinomialMatchQ((1 + x**4), x)
    assert eager_GeneralizedBinomialMatchQ((3*x + x**7), x)

def test_QuadraticMatchQ():
    assert not eager_QuadraticMatchQ((a + b*x)*(c + d*x), x)
    assert eager_QuadraticMatchQ(x**2 + x, x)
    assert eager_QuadraticMatchQ(x**2+1+x, x)
    assert eager_QuadraticMatchQ(x**2, x)

def test_PowerOfLinearMatchQ():
    assert eager_PowerOfLinearMatchQ(x, x)
    assert not eager_PowerOfLinearMatchQ(S(6)**3, x)
    assert not eager_PowerOfLinearMatchQ(S(6 + 3*x**2)**3, x)
    assert eager_PowerOfLinearMatchQ(S(6 + 3*x)**3, x)

def test_GeneralizedTrinomialMatchQ():
    assert not eager_GeneralizedTrinomialMatchQ(7 + 2*x**6 + 3*x**12, x)
    assert not eager_GeneralizedTrinomialMatchQ(7 + 2*x**6 + 3*x**3, x)
    assert not eager_GeneralizedTrinomialMatchQ(7 + 2*x**6 + 3*x**5, x)
    assert eager_GeneralizedTrinomialMatchQ(x**2 + x**3 + x**4, x)

def test_QuotientOfLinearsMatchQ():
    assert QuotientOfLinearsMatchQ((1 + x)*(3 + 4*x**2)/(2 + 4*x), x)
    assert not QuotientOfLinearsMatchQ(x*(3 + 4*x**2)/(2 + 4*x**3), x)
    assert QuotientOfLinearsMatchQ(x*(3 + 4*x)/(2 + 4*x), x)
    assert QuotientOfLinearsMatchQ(2*(3 + 4*x)/(2 + 4*x), x)

def test_PolynomialTermQ():
    assert PolynomialTermQ(S(3), x)   # Rubi: FreeQ constant is a polynomial term
    assert PolynomialTermQ(3*x**6, x)
    assert not PolynomialTermQ(3*x**6+5*x, x)

def test_PolynomialTerms():
    assert PolynomialTerms(x + 6*x**3 + log(x), x) == 6*x**3 + x
    assert PolynomialTerms(x + 6*x**3 + 6*x, x) == 6*x**3 + 7*x
    assert PolynomialTerms(x + 6*x**3 + 6, x) == 6*x**3 + x + 6   # the 6 is a poly term

def test_NonpolynomialTerms():
    assert NonpolynomialTerms(x + 6*x**3 + log(x), x) == log(x)
    assert NonpolynomialTerms(x + 6*x**3 + 6*x, x) == 0
    assert NonpolynomialTerms(x + 6*x**3 + 6, x) == 0

def test_PseudoBinomialQ():
    assert PseudoBinomialQ(3 + 5*(x)**6, x)
    assert PseudoBinomialQ(3 + 5*(2 + 5*x)**6, x)

def test_PseudoBinomialParts():
    assert PseudoBinomialParts(3 + 7*(1 + x)**6, x) == [3, 1, 7**(S(1)/S(6)), 7**(S(1)/S(6)), 6]
    assert PseudoBinomialParts(3 + 7*(1 + x)**3, x) == [3, 1, 7**(S(1)/S(3)), 7**(S(1)/S(3)), 3]
    assert not PseudoBinomialParts(3 + 7*(1 + x)**2, x)
    assert PseudoBinomialParts(3 + 7*(x)**5, x) == [3, 1, 0, 7**(S(1)/S(5)), 5]

def test_PseudoBinomialPairQ():
    assert not eager_PseudoBinomialPairQ(3 + 5*(x)**6,3 + (x)**6, x)
    assert not eager_PseudoBinomialPairQ(3 + 5*(1 + x)**6,3 + (1 + x)**6, x)

def test_NormalizePseudoBinomial():
    assert eager_NormalizePseudoBinomial(3 + 5*(1 + x)**6, x) == 3+(5**(S(1)/S(6))+5**(S(1)/S(6))*x)**S(6)
    assert eager_NormalizePseudoBinomial(3 + 5*(x)**6, x) == 3+5*x**6

def test_CancelCommonFactors():
    assert CancelCommonFactors(S(x*y*S(6))**S(6), S(x*y*S(6))) == [46656*x**6*y**6, 6*x*y]
    assert CancelCommonFactors(S(y*6)**S(6), S(x*y*S(6))) == [46656*y**6, 6*x*y]
    assert CancelCommonFactors(S(6), S(3)) == [6, 3]

def test_SimplerIntegrandQ():
    assert eager_SimplerIntegrandQ(S(5), 4*x, x)
    assert not eager_SimplerIntegrandQ(S(x + 5*x**3), S(x**2 + 3*x), x)
    assert eager_SimplerIntegrandQ(S(x + 8), S(x**2 + 3*x), x)

def test_Drop():
    assert Drop([1, 2, 3, 4, 5, 6], [2, 4]) == [1, 5, 6]
    assert Drop([1, 2, 3, 4, 5, 6], -3) == [1, 2, 3]
    assert Drop([1, 2, 3, 4, 5, 6], 2) == [3, 4, 5, 6]
    assert Drop(a*b*c, 1) == b*c

def test_SubstForInverseFunction():
    assert eager_SubstForInverseFunction(x, a, b, x) == b
    assert eager_SubstForInverseFunction(a, a, b, x) == a
    assert eager_SubstForInverseFunction(x**a, x**a, b, x) == x
    assert eager_SubstForInverseFunction(a*x**a, a, b, x) == a*b**a

def test_SubstForFractionalPower():
    assert SubstForFractionalPower(a, b, n, c, x) == a
    assert SubstForFractionalPower(x, b, n, c, x) == c
    assert SubstForFractionalPower(a**(S(1)/2), a, n, b, x) == x**(n/2)

def test_CombineExponents():
    """Merge adjacent equal bases in a base-sorted (base, exponent) list.

    This was a bare ``assert True``, which is why the helper could stay broken: it
    built results with the Rubi ``Prepend``, which CONCATENATES when handed a list,
    so prepending a ``[base, exp]`` pair spliced its elements into the result.
    """
    assert CombineExponents([[S(2), S(1)], [S(3), S(1)]]) == [[S(2), S(1)], [S(3), S(1)]]
    assert CombineExponents([[S(2), S(1)], [S(2), S(2)]]) == [[S(2), S(3)]]
    assert CombineExponents([[S(2), S(1)], [S(2), Rational(1, 2)], [S(3), S(1)]]) == [
        [S(2), Rational(3, 2)], [S(3), S(1)]]
    assert CombineExponents([[S(5), S(4)]]) == [[S(5), S(4)]]
    assert CombineExponents([]) == []


def test_FactorAbsurdNumber_power_and_product_branches():
    """Prime factorisation with rational exponents, verified against Mathematica.

    Two branches were broken. The POWER branch read
    ``r = FactorInteger(m.base); [r[0], r[1]*m.exp]``, treating a LIST of
    (prime, exponent) pairs as one pair -- an IndexError for any single-prime base,
    so ``FactorAbsurdNumber(Sqrt[3])`` raised. The PRODUCT branch was never written
    and returned ``[(m, 1)]``, leaving the whole product as one opaque base.
    """
    assert FactorAbsurdNumber(sqrt(S(3))) == [(S(3), Rational(1, 2))]
    assert FactorAbsurdNumber(S(2)*sqrt(S(3))) == [[S(2), S(1)], [S(3), Rational(1, 2)]]
    assert FactorAbsurdNumber(S(4)*sqrt(S(3))) == [[S(2), S(2)], [S(3), Rational(1, 2)]]
    assert FactorAbsurdNumber(S(6)*sqrt(S(2))) == [[S(2), Rational(3, 2)], [S(3), S(1)]]


def test_AbsurdNumberGCD_over_surds():
    """Mathematica: AbsurdNumberGCD[2 Sqrt[3], 4 Sqrt[3]] = 2 Sqrt[3].

    Came out 1 while FactorAbsurdNumber's product branch left 2*Sqrt[3] and
    4*Sqrt[3] as opaque, unequal bases.
    """
    assert AbsurdNumberGCD(S(2)*sqrt(S(3)), S(4)*sqrt(S(3))) == S(2)*sqrt(S(3))
    assert AbsurdNumberGCD(S(6)*sqrt(S(2)), S(9)*sqrt(S(2))) == S(3)*sqrt(S(2))


@pytest.mark.parametrize('terms, expected', [
    # Mathematica/Rubi values, captured from Rubi 4.17.3.0
    ([S(2)*a*b, S(4)*a*c], [S(2)*a, b, S(2)*c]),
    ([S(2)*sqrt(S(3)), S(4)*sqrt(S(3))], [S(2)*sqrt(S(3)), S(1), S(2)]),
    ([S(2)*x, S(4)*x], [S(2)*x, S(1), S(2)]),
    ([S(6), S(9)], [S(3), S(2), S(3)]),
    ([x**2, x**3], [x**2, S(1), x]),
])
def test_CommonFactors_matches_rubi(terms, expected):
    assert CommonFactors(list(terms)) == expected


@pytest.mark.parametrize('terms', [
    [S(2)*a*b, S(4)*a*c], [S(2)*sqrt(S(3)), S(4)*sqrt(S(3))], [S(2)*x, S(4)*x],
    [S(6), S(9)], [x**2, x**3], [S(3)*a*b, S(6)*a*b*c], [a*b*c, a*b],
])
def test_CommonFactors_preserves_the_product(terms):
    """CommonFactors[lst] = {common, lst/common...}, so common * residual_i == lst_i.

    Rubi is ONE nested If -- exactly one branch per iteration. Ported as two
    independent if-chains, control fell through after the SameQ branch and ran a
    second branch on a stale lst3, so CommonFactors[{2 a b, 4 a c}] returned
    {2a, a, 2c}: 2a*a is 2a^2, not 2ab. The decomposition silently stopped
    reconstructing its own input.
    """
    result = CommonFactors(list(terms))
    common, residuals = result[0], result[1:]
    assert len(residuals) == len(terms)
    for residual, original in zip(residuals, terms):
        assert simplify(common*residual - original) == 0

def test_FractionalPowerOfSquareQ():
    assert not FractionalPowerOfSquareQ(x)
    assert not FractionalPowerOfSquareQ((a + b)**(S(2)/S(3)))
    assert not FractionalPowerOfSquareQ((a + b)**(S(2)/S(3))*c)
    assert FractionalPowerOfSquareQ(((a + b*x)**(S(2)))**(S(1)/3)) == (a + b*x)**S(2)

def test_FractionalPowerSubexpressionQ():
    assert not FractionalPowerSubexpressionQ(x, a, x)
    assert FractionalPowerSubexpressionQ(x**(S(2)/S(3)), a, x)
    assert not FractionalPowerSubexpressionQ(b*a, a, x)

def test_FactorNumericGcd():
    assert FactorNumericGcd(5*a**2*e**4 + 2*a*b*d*e**3 + 2*a*c*d**2*e**2 + b**2*d**2*e**2 - 6*b*c*d**3*e + 21*c**2*d**4) ==\
        5*a**2*e**4 + 2*a*b*d*e**3 + 2*a*c*d**2*e**2 + b**2*d**2*e**2 - 6*b*c*d**3*e + 21*c**2*d**4
    assert FactorNumericGcd(x**(S(2))) == x**S(2)
    assert FactorNumericGcd(log(x)) == log(x)
    assert FactorNumericGcd(log(x)*x) == x*log(x)
    assert FactorNumericGcd(log(x) + x**S(2)) == log(x) + x**S(2)

def test_Apply():
    assert eager_Apply(eager_List, [a, b, c]) == [a, b, c]

def test_TrigSimplify():
    assert eager_TrigSimplify(a*sin(x)**2 + a*cos(x)**2 + v) == a + v
    assert eager_TrigSimplify(a*sec(x)**2 - a*tan(x)**2 + v) == a + v
    assert eager_TrigSimplify(a*csc(x)**2 - a*cot(x)**2 + v) == a + v
    assert eager_TrigSimplify(S(1) - sin(x)**2) == cos(x)**2
    assert eager_TrigSimplify(1 + tan(x)**2) == sec(x)**2
    assert eager_TrigSimplify(1 + cot(x)**2) == csc(x)**2
    assert eager_TrigSimplify(-S(1) + sec(x)**2) == tan(x)**2
    assert eager_TrigSimplify(-1 + csc(x)**2) == cot(x)**2

def test_MergeFactors():
    assert simplify(MergeFactors(b/(a - c)**3 , 8*c**3*(b*x + c)**(S(3)/2)/(3*b**4) - 24*c**2*(b*x + c)**(S(5)/2)/(5*b**4) + \
        24*c*(b*x + c)**(S(7)/2)/(7*b**4) - 8*(b*x + c)**(S(9)/2)/(9*b**4)) - (8*c**3*(b*x + c)**(S(3)/2)/(3*b**3) - 24*c**2*(b*x + c)**(S(5)/2)/(5*b**3) + \
        24*c*(b*x + c)**(S(7)/2)/(7*b**3) - 8*(b*x + c)**(S(9)/2)/(9*b**3))/(a - c)**3) == 0
    assert MergeFactors(x, x) == x**2
    assert MergeFactors(x*y, x) == x**2*y

def test_FactorInteger():
    assert FactorInteger(2434500) == [(2, 2), (3, 2), (5, 3), (541, 1)]

def test_ContentFactor():
    assert ContentFactor(a*b + a*c) == a*(b + c)

def test_Order():
    assert Order(a, b) == 1
    assert Order(b, a) == -1
    assert Order(a, a) == 0

def test_FactorOrder():
    assert FactorOrder(1, 1) == 0
    assert FactorOrder(1, 2) == -1
    assert FactorOrder(2, 1) == 1
    assert FactorOrder(a, b) == 1

def test_Smallest():
    assert Smallest([2, 1, 3, 4]) == 1
    assert Smallest(1, 2) == 1
    assert Smallest(-1, -2) == -2

def test_MostMainFactorPosition():
    assert MostMainFactorPosition([S(1), S(2), S(3)]) == 1
    assert MostMainFactorPosition([S(1), S(7), S(3), S(4), S(5)]) == 2

def test_OrderedQ():
    assert OrderedQ([a, b])
    assert not OrderedQ([b, a])

def test_MinimumDegree():
    assert MinimumDegree(S(1), S(2)) == 1
    assert MinimumDegree(S(1), sqrt(2)) == 1
    assert MinimumDegree(sqrt(2), S(1)) == 1
    assert MinimumDegree(sqrt(3), sqrt(2)) == sqrt(2)
    assert MinimumDegree(sqrt(2), sqrt(2)) == sqrt(2)

def test_PositiveFactors():
    assert PositiveFactors(S(0)) == 1
    assert PositiveFactors(-S(1)) == S(1)
    assert PositiveFactors(sqrt(2)) == sqrt(2)
    assert PositiveFactors(-log(2)) == log(2)
    assert PositiveFactors(sqrt(2)*S(-1)) == sqrt(2)

def test_NonpositiveFactors():
    assert NonpositiveFactors(S(0)) == 0
    assert NonpositiveFactors(-S(1)) == -1
    assert NonpositiveFactors(sqrt(2)) == 1
    assert NonpositiveFactors(-log(2)) == -1

def test_Sign():
    assert eager_Sign(S(0)) == 0
    assert eager_Sign(S(1)) == 1
    assert eager_Sign(-S(1)) == -1

def test_PolynomialInQ():
    v = log(x)
    assert eager_PolynomialInQ(S(1), v, x)
    assert eager_PolynomialInQ(v, v, x)
    assert eager_PolynomialInQ(1 + v**2, v, x)
    assert eager_PolynomialInQ(1 + a*v**2, v, x)
    assert not eager_PolynomialInQ(sqrt(v), v, x)


def test_ExponentIn():
    v = log(x)
    assert ExponentIn(S(1), log(x), x) == 0
    assert ExponentIn(S(1) + v, log(x), x) == 1
    assert ExponentIn(S(1) + v + v**3, log(x), x) == 3
    assert ExponentIn(S(2)*sqrt(v)*v**3, log(x), x) == S(7)/2

def test_PolynomialInSubst():
    v = log(x)
    assert eager_PolynomialInSubst(S(1) + log(x)**3, log(x), x) == 1 + x**3
    assert eager_PolynomialInSubst(S(1) + log(x), log(x), x) == x + 1

def test_Distrib():
    assert eager_Distrib(x, a) == x*a
    assert eager_Distrib(x, a + b) == a*x + b*x

def test_DistributeDegree():
    assert DistributeDegree(x, m) == x**m
    assert DistributeDegree(x**a, m) == x**(a*m)
    assert DistributeDegree(a*b, m) == a**m * b**m

def test_FunctionOfPower():
    assert FunctionOfPower(a, x) == None
    assert FunctionOfPower(x, x) == 1
    assert FunctionOfPower(x**3, x) == 3
    assert FunctionOfPower(x**3*cos(x**6), x) == 3

def test_DivideDegreesOfFactors():
    assert DivideDegreesOfFactors(a**b, S(3)) == a**(b/3)
    # Mathematica: DivideDegreesOfFactors[a^b*c, 3] = a^(b/3)*c^(1/3)
    assert DivideDegreesOfFactors(a**b*c, S(3)) == a**(b/3)*c**(S(1)/3)

def test_MonomialFactor():
    assert MonomialFactor(a, x) == [0, a]
    assert MonomialFactor(x, x) == [1, 1]
    assert MonomialFactor(x + y, x) == [0, x + y]
    assert MonomialFactor(log(x), x) == [0, log(x)]
    assert MonomialFactor(log(x)*x, x) == [1, log(x)]

def test_NormalizeIntegrand():
    assert eager_NormalizeIntegrand((x**2 + 8), x) == x**2 + 8
    assert eager_NormalizeIntegrand((x**2 + 3*x)**2, x) == x**2*(x + 3)**2
    assert eager_NormalizeIntegrand(a**2*(a + b*x)**2, x) == a**2*(a + b*x)**2
    assert eager_NormalizeIntegrand(b**2/(a**2*(a + b*x)**2), x) == b**2/(a**2*(a + b*x)**2)

def test_NormalizeIntegrandAux():
    v = (6*A*a*c - 2*A*b**2 + B*a*b)/(a*x**2) - (6*A*a**2*c**2 - 10*A*a*b**2*c - 8*A*a*b*c**2*x + 2*A*b**4 + 2*A*b**3*c*x + 5*B*a**2*b*c + 4*B*a**2*c**2*x - B*a*b**3 - B*a*b**2*c*x)/(a**2*(a + b*x + c*x**2)) + (-2*A*b + B*a)*(4*a*c - b**2)/(a**2*x)
    assert NormalizeIntegrandAux(v, x) == (6*A*a*c - 2*A*b**2 + B*a*b)/(a*x**2) - (6*A*a**2*c**2 - 10*A*a*b**2*c + 2*A*b**4 + 5*B*a**2*b*c - B*a*b**3 + x*(-8*A*a*b*c**2 + 2*A*b**3*c + 4*B*a**2*c**2 - B*a*b**2*c))/(a**2*(a + b*x + c*x**2)) + (-2*A*b + B*a)*(4*a*c - b**2)/(a**2*x)
    assert NormalizeIntegrandAux((x**2 + 3*x)**2, x) == x**2*(x + 3)**2
    assert NormalizeIntegrandAux((x**2 + 8), x) == x**2 + 8

def test_NormalizeIntegrandFactor():
    assert NormalizeIntegrandFactor((3*x + x**3)**2, x) == x**2*(x**2 + 3)**2
    assert NormalizeIntegrandFactor((x**2 + 8), x) == x**2 + 8

def test_NormalizeIntegrandFactorBase():
    assert NormalizeIntegrandFactorBase((x**2 + 8)**3, x) == (x**2 + 8)**3
    assert NormalizeIntegrandFactorBase((x**2 + 8), x) == x**2 + 8
    assert NormalizeIntegrandFactorBase(a**2*(a + b*x)**2, x) == a**2*(a + b*x)**2

def test_AbsorbMinusSign():
    assert AbsorbMinusSign((x + 2)**5*(x + 3)**5) == (-x - 3)**5*(x + 2)**5
    assert  AbsorbMinusSign((x + 2)**5*(x + 3)**2) == -(x + 2)**5*(x + 3)**2

def test_NormalizeLeadTermSigns():
    assert NormalizeLeadTermSigns((-x + 3)*(x**2 + 3)) == (-x + 3)*(x**2 + 3)
    assert NormalizeLeadTermSigns(x + 3) == x + 3

def test_SignOfFactor():
    assert SignOfFactor(S(-x + 3)) == [1, -x + 3]
    assert SignOfFactor(S(-x)) == [-1, x]


def test_SignOfFactor_complex_numeric_factor():
    """Regression for the 1/(x^4+1) crash: SignOfFactor tests ``NumericFactor(First(u)) < 0``
    on a sum whose leading term's numeric factor SymPy has not simplified to an obvious
    real (here it equals Sqrt[2]). A bare ``< 0`` raised TypeError; matching Mathematica
    (Less on a non-real stays falsy) it must return sign 1, no exception. Cross-checked
    vs real Rubi (ssh pi): SignOfFactor[u] = {1, u}."""
    val = -(-1)**(S(3)/4) + (-1)**(S(1)/4)
    u = (((-1)**(S(3)/4) + (-1)**(S(1)/4))/(4*I*x + 4*(-1)**(S(1)/4))
         + ((-1)**(S(3)/4) + (-1)**(S(1)/4))/(-4*I*x + 4*(-1)**(S(1)/4))
         + val/(4*x + 4*(-1)**(S(1)/4))
         + val/(-4*x + 4*(-1)**(S(1)/4)))
    sign, rest = SignOfFactor(u)
    assert sign == 1
    assert rest == u

def test_NormalizePowerOfLinear():
    assert eager_NormalizePowerOfLinear((x + 3)**5, x) == (x + 3)**5
    assert eager_NormalizePowerOfLinear(((x + 3)**2) + 3, x) == x**2 + 6*x + 12

def test_SimplifyIntegrand():
    assert eager_SimplifyIntegrand((x**2 + 3)**2, x) == (x**2 + 3)**2
    assert eager_SimplifyIntegrand(x**2 + 3 + (x**6) + 6, x) == x**6 + x**2 + 9

def test_SimplifyTerm():
    assert SimplifyTerm(a**2/b**2, x) == a**2/b**2
    assert SimplifyTerm(-6*x/5 + (5*x + 3)**2/25 - S(9)/25, x) == x**2

def test_togetherSimplify():
    assert TogetherSimplify(-6*x/5 + (5*x + 3)**2/25 - S(9)/25) == x**2

def test_ExpandToSum():

    qq = 6
    Pqq = e**3
    Pq = (d+e*x**2)**3
    aa = 2
    nn = 2
    cc = 1
    pp = -S.Half
    bb = 3
    assert nsimplify(eager_ExpandToSum(Pq - Pqq*x**qq - Pqq*(aa*x**(-2*nn + qq)*(-2*nn + qq + 1) + bb*x**(-nn + qq)*(nn*(pp - 1) + qq + 1))/(cc*(2*nn*pp + qq + 1)), x) - \
        (d**3 + x**4*(3*d*e**2 - 2.4*e**3) + x**2*(3*d**2*e - 1.2*e**3))) == 0
    assert eager_ExpandToSum(x**2 + 3*x + 3, x**3 + 3, x) == x**3*(x**2 + 3*x + 3) + 3*x**2 + 9*x + 9
    assert eager_ExpandToSum(x**3 + 6, x) == x**3 + 6
    assert eager_ExpandToSum(S(x**2 + 3*x + 3)*3, x) == 3*x**2 + 9*x + 9
    assert eager_ExpandToSum((a + b*x), x) == a + b*x

def test_UnifySum():
    assert UnifySum((3 + x + 6*x**3 + sin(x)), x) == 6*x**3 + x + sin(x) + 3
    assert UnifySum((3 + x + 6*x**3)*3, x) == 18*x**3 + 3*x + 9

def test_FunctionOfInverseLinear():
    assert FunctionOfInverseLinear((x)/(a + b*x), x) == [a, b]
    assert FunctionOfInverseLinear((c + d*x)/(a + b*x), x) == [a, b]
    assert not FunctionOfInverseLinear(1/(a + b*x), x)

def test_PureFunctionOfSinhQ():
    v = log(x)
    f = sinh(v)
    assert PureFunctionOfSinhQ(f, v, x)
    assert not PureFunctionOfSinhQ(cosh(v), v, x)
    assert PureFunctionOfSinhQ(f**2, v, x)

def test_PureFunctionOfTanhQ():
    v = log(x)
    f = tanh(v)
    assert PureFunctionOfTanhQ(f, v, x)
    assert not PureFunctionOfTanhQ(cosh(v), v, x)
    assert PureFunctionOfTanhQ(f**2, v, x)

def test_PureFunctionOfCoshQ():
    v = log(x)
    f = cosh(v)
    assert PureFunctionOfCoshQ(f, v, x)
    assert not PureFunctionOfCoshQ(sinh(v), v, x)
    assert PureFunctionOfCoshQ(f**2, v, x)

def test_IntegerQuotientQ():
    u = S(2)*sin(x)
    v = sin(x)
    assert IntegerQuotientQ(u, v)
    assert IntegerQuotientQ(u, u)
    assert not IntegerQuotientQ(S(1), S(2))

def test_OddQuotientQ():
    u = S(3)*sin(x)
    v = sin(x)
    assert OddQuotientQ(u, v)
    assert OddQuotientQ(u, u)
    assert not OddQuotientQ(S(1), S(2))

def test_EvenQuotientQ():
    u = S(2)*sin(x)
    v = sin(x)
    assert EvenQuotientQ(u, v)
    assert not EvenQuotientQ(u, u)
    assert not EvenQuotientQ(S(1), S(2))

def test_FunctionOfSinhQ():
    v = log(x)
    assert FunctionOfSinhQ(cos(sinh(v)), v, x)
    assert FunctionOfSinhQ(sinh(v), v, x)
    assert FunctionOfSinhQ(sinh(v)*cos(sinh(v)), v, x)

def test_FunctionOfCoshQ():
    v = log(x)
    assert FunctionOfCoshQ(cos(cosh(v)), v, x)
    assert FunctionOfCoshQ(cosh(v), v, x)
    assert FunctionOfCoshQ(cosh(v)*cos(cosh(v)), v, x)

def test_FunctionOfTanhQ():
    v = log(x)
    t = Tanh(v)
    c = Coth(v)
    assert FunctionOfTanhQ(t, v, x)
    assert FunctionOfTanhQ(c, v, x)
    assert FunctionOfTanhQ(t + c, v, x)
    assert FunctionOfTanhQ(t*c, v, x)
    assert not FunctionOfTanhQ(sin(x), v, x)

def test_FunctionOfTanhWeight():
    v = log(x)
    t = Tanh(v)
    c = Coth(v)
    assert FunctionOfTanhWeight(x, v, x) == 0
    assert FunctionOfTanhWeight(sinh(v), v, x) == 0
    assert FunctionOfTanhWeight(tanh(v), v, x) == 1
    assert FunctionOfTanhWeight(coth(v), v, x) == -1
    assert FunctionOfTanhWeight(t**2, v, x) == 1
    assert FunctionOfTanhWeight(sinh(v)**2, v, x) == -1
    assert FunctionOfTanhWeight(coth(v)*sinh(v)**2, v, x) == -2

def test_FunctionOfHyperbolicQ():
    v = log(x)
    s = Sinh(v)
    t = Tanh(v)
    assert not FunctionOfHyperbolicQ(x, v, x)
    assert FunctionOfHyperbolicQ(s + t, v, x)
    assert FunctionOfHyperbolicQ(sinh(t), v, x)

def test_SmartNumerator():
    assert SmartNumerator(x**(-2)) == 1
    assert SmartNumerator(x**(2)*a) == x**2*a

def test_SmartDenominator():
    assert SmartDenominator(x**(-2)) == x**2
    assert SmartDenominator(x**(-2)*1/S(3)) == x**2*3

def test_SubstForAux():
    v = log(x)
    assert SubstForAux(v, v, x) == x
    assert SubstForAux(v**2, v, x) == x**2
    assert SubstForAux(x, v, x) == x
    assert SubstForAux(v**2, v**4, x) == sqrt(x)
    assert SubstForAux(v**2*v, v, x) == x**3

def test_SubstForTrig():
    v = log(x)
    s, c, t = sin(v), cos(v), tan(v)
    assert SubstForTrig(cos(a/2 + b*x/2), x/sqrt(x**2 + 1), 1/sqrt(x**2 + 1), a/2 + b*x/2, x) == 1/sqrt(x**2 + 1)
    assert SubstForTrig(s, sin, cos, v, x) == sin
    assert SubstForTrig(t, sin(v), cos(v), v, x) == sin(log(x))/cos(log(x))
    assert SubstForTrig(sin(2*v), sin(x), cos(x), v, x) == 2*sin(x)*cos(x)
    assert SubstForTrig(s*t, sin(x), cos(x), v, x) == sin(x)**2/cos(x)

def test_SubstForHyperbolic():
    v = log(x)
    s, c, t = sinh(v), cosh(v), tanh(v)
    assert SubstForHyperbolic(s, sinh(x), cosh(x), v, x) == sinh(x)
    assert SubstForHyperbolic(t, sinh(x), cosh(x), v, x) == sinh(x)/cosh(x)
    assert SubstForHyperbolic(sinh(2*v), sinh(x), cosh(x), v, x) == 2*sinh(x)*cosh(x)
    assert SubstForHyperbolic(s*t, sinh(x), cosh(x), v, x) == sinh(x)**2/cosh(x)

def test_SubstForFractionalPowerOfLinear():
    u = a + b*x
    assert not eager_SubstForFractionalPowerOfLinear(u, x)
    assert not eager_SubstForFractionalPowerOfLinear(u**(S(2)), x)
    assert eager_SubstForFractionalPowerOfLinear(u**(S(1)/2), x) == [x**2, 2, a + b*x, 1/b]

def test_SubstPower():
    """Rubi IntegrationUtilityFunctions.m — replace x by x**n throughout.
    Expected values cross-checked against real Rubi on Mathematica 12.2."""
    from rubi_rules.utils.utility_functions import eager_SubstPower
    assert eager_SubstPower(x**3, x, 2) == x**6          # SubstPower[x^3,x,2] == x^6
    assert eager_SubstPower(x, x, 2) == x**2
    assert eager_SubstPower(a + x**2, x, 3) == a + x**6
    # recurses into non-power heads: Sin[x]+x^2 -> Sin[x^2]+x^4
    assert eager_SubstPower(sin(x) + x**2, x, 2) == sin(x**2) + x**4
    # x-free atoms are untouched
    assert eager_SubstPower(a, x, 2) == a


def test_SubstPower_deferred_node():
    from rubi_rules.utils.rubi_utils import SubstPower
    assert SubstPower(x**3, x, 2).doit() == x**6


def test_SubstForInverseFunction_three_argument_form():
    """The 3-arg form builds w = (g^-1[x] - a)/b from v = g[a+b x]; it used to raise
    NameError because InverseFunction was never implemented.
    Mathematica 12.2: SubstForInverseFunction[x^2, ArcTan[a+b x], x] == (-a+Tan[x])^2/b^2."""
    from rubi_rules.utils.utility_functions import eager_SubstForInverseFunction as _S
    assert simplify(_S(x**2, atan(a + b*x), x) - (-a + tan(x))**2/b**2) == 0
    # 4-arg form (Mathematica-verified)
    assert _S(a, a, b, x) == a
    assert _S(x, a, b, x) == b
    assert _S(a*x**a, a, b, x) == a*b**a
    w = Symbol('w')
    assert _S(sin(a + b*x) + x, sin(a + b*x), w, x) == w + x


def test_InverseFunction_table():
    """Mathematica InverseFunction for the heads Rubi inverts."""
    import sympy
    from rubi_rules.utils.utility_functions import eager_InverseFunction
    assert eager_InverseFunction(atan) is tan
    assert eager_InverseFunction(tan) is atan
    assert eager_InverseFunction(asin) is sin
    assert eager_InverseFunction(log) is exp
    assert eager_InverseFunction(acosh) is cosh
    assert eager_InverseFunction(sympy.Abs) is None       # not invertible -> None


def test_ExpandTrigExpand():
    """Rubi ExpandTrigExpand[u,F,v,m,n,x] = Map[u*#, Expand[TrigExpand[F[n x]]^m] /. x->v].
    F is a HEAD that Mathematica APPLIES to n*x. Mathematica 12.2 values below."""
    from rubi_rules.utils.utility_functions import eager_ExpandTrigExpand
    u, v = symbols('u v')
    # ExpandTrigExpand[u, Sin, x, 2, 2, x] == 4 u Cos[x]^2 Sin[x]^2
    assert simplify(eager_ExpandTrigExpand(u, sin, x, 2, 2, x) - 4*u*cos(x)**2*sin(x)**2) == 0
    # ExpandTrigExpand[1, Sin, x, 1, 2, x] == 2 Cos[x] Sin[x]
    assert simplify(eager_ExpandTrigExpand(1, sin, x, 1, 2, x) - 2*sin(x)*cos(x)) == 0
    # ExpandTrigExpand[1, Cos, v, 1, 2, x] == Cos[v]^2 - Sin[v]^2 (SymPy normalises it
    # to 2 Cos[v]^2 - 1; same value)
    assert simplify(eager_ExpandTrigExpand(1, cos, v, 1, 2, x) - (cos(v)**2 - sin(v)**2)) == 0


def test_FunctionOfSquareRootOfQuadratic():
    """Rubi's Euler substitution helper; returns {v, subst, n} or False.
    Expected values from real Rubi on Mathematica 12.2."""
    from rubi_rules.utils.utility_functions import eager_FunctionOfSquareRootOfQuadratic as _F
    got = _F(sqrt(1 + x + x**2), x)
    assert got[1] == x + sqrt(1 + x + x**2) and got[2] == 2
    assert simplify(got[0] - (1 + x + x**2)**2/(1 + 2*x)**3) == 0
    got = _F(1/sqrt(1 + x**2), x)
    assert got == [1/(2*x), x + sqrt(1 + x**2), 2]
    assert _F(x**2, x) is False


def test_FunctionOfSquareRootOfQuadratic_deferred_node():
    from rubi_rules.utils.rubi_utils import FunctionOfSquareRootOfQuadratic as _F
    from sympy_wolfram.objects import List as _List
    assert isinstance(_F(1/sqrt(1 + x**2), x).doit(), _List)
    assert _F(x**2, x).doit() is S.false


def test_InverseFunctionOfLinear():
    """Rubi IntegrationUtilityFunctions.m:6084. Expected values cross-checked against
    real Rubi on Mathematica 12.2."""
    u = a + b*x
    assert eager_InverseFunctionOfLinear(log(u)*sin(x), x) == log(u)
    assert eager_InverseFunctionOfLinear(log(u), x) == log(u)
    # returns the inverse-function subexpression itself...
    assert eager_InverseFunctionOfLinear(atan(u), x) == atan(u)
    assert eager_InverseFunctionOfLinear(log(u)**2, x) == log(u)
    # ...found at any depth
    assert eager_InverseFunctionOfLinear(x*asin(2 + 3*x), x) == asin(2 + 3*x)
    # False when there is none, when the argument is not LINEAR in x,
    # and for atoms / x-free expressions
    assert eager_InverseFunctionOfLinear(sin(u), x) is False
    assert eager_InverseFunctionOfLinear(atan(x**2), x) is False
    assert eager_InverseFunctionOfLinear(x**2, x) is False
    assert eager_InverseFunctionOfLinear(a, x) is False


def test_InverseFunctionOfLinear_deferred_node():
    """The deferred node maps Rubi's False onto SymPy's S.false so a rule guard can
    test it (a bare Python False is not a SymPy object)."""
    from rubi_rules.utils.rubi_utils import InverseFunctionOfLinear
    assert InverseFunctionOfLinear(atan(a + b*x), x).doit() == atan(a + b*x)
    assert InverseFunctionOfLinear(sin(a + b*x), x).doit() is S.false

def test_InertTrigQ():
    # InertTrigQ detects *inert* trig markers (Function('sin')(...)), not the
    # active SymPy trig functions.
    from rubi_rules.utils.utility_functions import InertSin, InertCos, InertCsc
    isin, icos, icsc = InertSin(x), InertCos(x), InertCsc(x)
    assert not eager_InertTrigQ(isin, icsc, InertCos(h))
    assert eager_InertTrigQ(isin, icsc)          # sin/csc reciprocal pair
    assert not eager_InertTrigQ(isin, icos)
    assert eager_InertTrigQ(icos)
    # active SymPy trig is not inert
    assert not eager_InertTrigQ(sin(x))
    assert not eager_InertTrigQ(cos(x))

def test_InertTrigFreeQ():
    from rubi_rules.utils.utility_functions import InertSin
    assert eager_InertTrigFreeQ(x)
    assert eager_InertTrigFreeQ(exp(x)*x)
    # active SymPy trig is inert-trig-free (that is the whole point of the fix)
    assert eager_InertTrigFreeQ(sin(x))
    assert eager_InertTrigFreeQ(x*sin(x))
    assert eager_InertTrigFreeQ(x*sin(x**2 + x))
    # inert markers ARE detected
    assert not eager_InertTrigFreeQ(InertSin(x))
    assert not eager_InertTrigFreeQ(x*InertSin(x))

def test_PowerOfInertTrigSumQ():
    func = sin
    assert PowerOfInertTrigSumQ((1 + S(2)*(S(3)*func(x**2))**S(5))**3, func, x)
    assert PowerOfInertTrigSumQ((1 + 2*(S(3)*func(x**2))**3 + 4*(S(5)*func(x**2))**S(3))**2, func, x)

def test_PiecewiseLinearQ():
    assert eager_PiecewiseLinearQ(a + b*x, x)
    assert not eager_PiecewiseLinearQ(Log(c*sin(a)**S(3)), x)
    assert not eager_PiecewiseLinearQ(x**3, x)
    assert eager_PiecewiseLinearQ(atanh(tanh(a + b*x)), x)
    assert eager_PiecewiseLinearQ(tanh(atanh(a + b*x)), x)
    assert not eager_PiecewiseLinearQ(coth(atanh(a + b*x)), x)

def test_KnownTrigIntegrandQ():
    func = sin(a + b*x)
    assert KnownTrigIntegrandQ([sin], S(1), x)
    assert KnownTrigIntegrandQ([sin], (a + b*func)**m, x)
    assert KnownTrigIntegrandQ([sin], (a + b*func)**m*(1 + 2*func), x)
    assert KnownTrigIntegrandQ([sin], a + c*func**2, x)
    assert KnownTrigIntegrandQ([sin], a + b*func + c*func**2, x)
    assert KnownTrigIntegrandQ([sin], (a + b*func)**m*(c + d*func**2), x)
    assert KnownTrigIntegrandQ([sin], (a + b*func)**m*(c + d*func + e*func**2), x)
    assert not KnownTrigIntegrandQ([cos], (a + b*func)**m, x)

def test_KnownSineIntegrandQ():
    assert eager_KnownSineIntegrandQ((a + b*sin(a + b*x))**m, x)

def test_KnownTangentIntegrandQ():
    assert eager_KnownTangentIntegrandQ((a + b*tan(a + b*x))**m, x)

def test_KnownCotangentIntegrandQ():
    assert eager_KnownCotangentIntegrandQ((a + b*cot(a + b*x))**m, x)

def test_KnownSecantIntegrandQ():
    assert eager_KnownSecantIntegrandQ((a + b*sec(a + b*x))**m, x)

def test_TryPureTanSubst():
    assert eager_TryPureTanSubst(atan(c*(a + b*tan(a + b*x))), x)
    assert eager_TryPureTanSubst(atanh(c*(a + b*cot(a + b*x))), x)
    assert not eager_TryPureTanSubst(tan(c*(a + b*cot(a + b*x))), x)

def test_TryPureTanhSubst():
    assert not TryPureTanhSubst(log(x), x)
    assert TryPureTanhSubst(sin(x), x)
    assert not TryPureTanhSubst(atanh(a*tanh(x)), x)
    assert not TryPureTanhSubst((a + b*x)**S(2), x)

def test_TryTanhSubst():
    assert not TryTanhSubst(log(x), x)
    assert not TryTanhSubst(a*(b + c)**3, x)
    assert not TryTanhSubst(1/(a + b*sinh(x)**S(3)), x)
    assert not TryTanhSubst(sinh(S(3)*x)*cosh(S(4)*x), x)
    assert not TryTanhSubst(a*(b*sech(x)**3)**c, x)

def test_GeneralizedBinomialQ():
    assert eager_GeneralizedBinomialQ(a*x**q + b*x**n, x)
    assert not eager_GeneralizedBinomialQ(a*x**q, x)

def test_GeneralizedTrinomialQ():
    assert not eager_GeneralizedTrinomialQ(7 + 2*x**6 + 3*x**12, x)
    assert not eager_GeneralizedTrinomialQ(a*x**q + c*x**(2*n-q), x)

def test_SubstForFractionalPowerOfQuotientOfLinears():
    """Rubi IntegrationUtilityFunctions.m:1801 — returns {v, n, (a+b x)/(c+d x), b c-a d}.
    Expected values cross-checked against real Rubi on Mathematica 12.2."""
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(((a + b*x)/(c + d*x))**(S(3)/2), x) == [x**4/(b - d*x**2)**2, 2, (a + b*x)/(c + d*x), -a*d + b*c]
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(((1 + x)/(1 - x))**(S(1)/2), x) == [x**2/(x**2 + 1)**2, 2, (1 + x)/(1 - x), 2]
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(((1 + x)/(1 - x))**(S(1)/3), x) == [x**3/(x**3 + 1)**2, 3, (1 + x)/(1 - x), 2]
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(x*((a + b*x)/(c + d*x))**(S(1)/2), x) == [x**2*(-a + c*x**2)/(b - d*x**2)**3, 2, (a + b*x)/(c + d*x), -a*d + b*c]
    # no fractional power of a quotient of linears -> False
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(x**2, x) is False
    assert eager_SubstForFractionalPowerOfQuotientOfLinears(sqrt(1 + x), x) is False


def test_SubstForFractionalPowerOfQuotientOfLinears_deferred_node():
    """The node returns a Wolfram List (Rubi reads it with Part), or S.false."""
    from rubi_rules.utils.rubi_utils import SubstForFractionalPowerOfQuotientOfLinears as _S
    from sympy_wolfram.objects import List as _List
    got = _S(((1 + x)/(1 - x))**(S(1)/2), x).doit()
    assert isinstance(got, _List)
    assert list(got.args) == [x**2/(x**2 + 1)**2, S(2), (1 + x)/(1 - x), S(2)]
    assert _S(x**2, x).doit() is S.false

def test_SubstForFractionalPowerQ():
    assert eager_SubstForFractionalPowerQ(x, sin(x), x)
    assert eager_SubstForFractionalPowerQ(x**2, sin(x), x)
    assert not eager_SubstForFractionalPowerQ(x**(S(3)/2), sin(x), x)
    assert eager_SubstForFractionalPowerQ(sin(x)**(S(3)/2), sin(x), x)

def test_AbsurdNumberGCD():
    assert AbsurdNumberGCD(S(4)) == 4
    assert AbsurdNumberGCD(S(4), S(8), S(12)) == 4
    assert AbsurdNumberGCD(S(2), S(3), S(12)) == 1

def test_TrigReduce():
    assert TrigReduce(cos(x)**2) == cos(2*x)/2 + S.Half
    assert TrigReduce(cos(x)**2*sin(x)) == sin(x)/4 + sin(3*x)/4
    assert TrigReduce(cos(x)**2+sin(x)) == sin(x) + cos(2*x)/2 + S.Half
    assert TrigReduce(cos(x)**2*sin(x)**5) == 5*sin(x)/64 + sin(3*x)/64 - 3*sin(5*x)/64 + sin(7*x)/64
    assert TrigReduce(2*sin(x)*cos(x) + 2*cos(x)**2) == sin(2*x) + cos(2*x) + 1
    assert TrigReduce(sinh(a + b*x)**2) == cosh(2*a + 2*b*x)/2 - S.Half
    assert TrigReduce(sinh(a + b*x)*cosh(a + b*x)) == sinh(2*a + 2*b*x)/2

def test_FunctionOfDensePolynomialsQ():
    assert FunctionOfDensePolynomialsQ(x**2 + 3, x)
    assert not FunctionOfDensePolynomialsQ(x**2, x)
    assert not FunctionOfDensePolynomialsQ(x, x)
    assert FunctionOfDensePolynomialsQ(S(2), x)

def test_PureFunctionOfSinQ():
    v = log(x)
    f = sin(v)
    assert PureFunctionOfSinQ(f, v, x)
    assert not PureFunctionOfSinQ(cos(v), v, x)
    assert PureFunctionOfSinQ(f**2, v, x)

def test_PureFunctionOfTanQ():
    v = log(x)
    f = tan(v)
    assert PureFunctionOfTanQ(f, v, x)
    assert not PureFunctionOfTanQ(cos(v), v, x)
    assert PureFunctionOfTanQ(f**2, v, x)

def test_PowerVariableSubst():
    assert PowerVariableSubst((2*x)**3, 2, x) == 8*x**(S(3)/2)
    assert PowerVariableSubst((2*x)**3, 2, x) == 8*x**(S(3)/2)
    assert PowerVariableSubst((2*x), 2, x) == 2*x
    assert PowerVariableSubst((2*x)**3, 2, x) == 8*x**(S(3)/2)
    assert PowerVariableSubst((2*x)**7, 2, x) == 128*x**(S(7)/2)
    assert PowerVariableSubst((6+2*x)**7, 2, x) == (2*x + 6)**7
    assert PowerVariableSubst((2*x)**7+3, 2, x) == 128*x**(S(7)/2) + 3

def test_PowerVariableDegree():
    assert PowerVariableDegree(S(2), 0, 2*x, x) == [0, 2*x]
    assert PowerVariableDegree((2*x)**2, 0, 2*x, x) == [2, 1]
    assert PowerVariableDegree(x**2, 0, 2*x, x) == [2, 1]
    assert PowerVariableDegree(S(4), 0, 2*x, x) == [0, 2*x]

def test_PowerVariableExpn():
    assert not eager_PowerVariableExpn((x)**3, 2, x)
    assert not eager_PowerVariableExpn((2*x)**3, 2, x)
    assert eager_PowerVariableExpn((2*x)**2, 4, x) == [4*x**3, 2, 1]

def test_FunctionOfQ():
    assert eager_FunctionOfQ(x**2, sqrt(-exp(2*x**2) + 1)*exp(x**2),x)
    assert not eager_FunctionOfQ(S(x**3), x*2, x)
    assert eager_FunctionOfQ(S(a), x*2, x)
    assert eager_FunctionOfQ(S(3*x), x*2, x)


# FunctionOfQ(v, u, x, PureFlag): "is u a function of v?". The values below were
# CROSS-CHECKED against real Rubi 4.17.3 in Mathematica (ssh pi@192.168.1.119,
# 2026-07-23); each pair is (our result, Rubi result) and they must agree.
#
# The PureFlag distinction matters and is subtle, so it is pinned here:
#   1/(a+b sech^2) is NOT a PURE function of tanh (PureFlag=True -> False), because
#   the pure test only accepts Tanh/Coth heads directly; but it IS a function of
#   tanh (PureFlag=False -> True) since sech^2 = 1 - tanh^2. This exact pair is why
#   the 4.7.5 inert-trig rule (which uses FunctionOfQ[...,True]) does NOT fire on
#   sech^2/(a+b sech^2) -- in Rubi either -- a fact confirmed on the Pi, not a bug.
_FUNCTION_OF_Q_CASES = [
    # (v, u, PureFlag, expected)   -- expected verified against Rubi on the Pi
    (lambda A: tanh(A), lambda A: 1/(a + b*sech(A)**2), True,  False),
    (lambda A: tanh(A), lambda A: 1/(a + b*sech(A)**2), False, True),
    (lambda A: sin(A),  lambda A: sin(A)**2 + sin(A),   True,  True),
    (lambda A: sin(A),  lambda A: cos(A),               True,  False),
    (lambda A: cos(A),  lambda A: sec(A)**2,            True,  True),
    (lambda A: tanh(A), lambda A: sech(A),              True,  False),
    (lambda A: tanh(A), lambda A: sech(A),              False, False),  # odd power: needs sqrt
    (lambda A: cosh(A), lambda A: 1/(a + b*cosh(A)**2), False, True),
]


def test_FunctionOfQ_matches_rubi_pure_flag():
    A = c + d*x
    for build_v, build_u, pure, expected in _FUNCTION_OF_Q_CASES:
        got = bool(eager_FunctionOfQ(build_v(A), build_u(A), x, pure))
        assert got == expected, (build_v(A), build_u(A), pure, got, expected)


def test_FunctionOfQ_atom_and_exp_cases():
    """Non-trig cases, also Pi-verified."""
    assert eager_FunctionOfQ(x, x**2 + x, x, True) is True
    assert eager_FunctionOfQ(exp(x), a + b*exp(x), x, False) is True


def test_FunctionOfQ_sech_squared_is_a_function_of_tanh_but_not_purely():
    """The specific pair behind the sech^2/(a+b sech^2) investigation, pinned so a
    future change to the pure/non-pure split cannot silently drift from Rubi."""
    A = c + d*x
    u = 1/(a + b*sech(A)**2)
    assert eager_FunctionOfQ(tanh(A), u, x, PureFlag=True) is False
    assert eager_FunctionOfQ(tanh(A), u, x, PureFlag=False) is True

def test_ExpandTrigExpand():
    assert eager_ExpandTrigExpand(1, cos(x), x**2, 2, 2, x) == 4*cos(x**2)**4 - 4*cos(x**2)**2 + 1
    assert eager_ExpandTrigExpand(1, cos(x) + sin(x), x**2, 2, 2, x) == 4*sin(x**2)**2*cos(x**2)**2 + 8*sin(x**2)*cos(x**2)**3 - 4*sin(x**2)*cos(x**2) + 4*cos(x**2)**4 - 4*cos(x**2)**2 + 1

def test_TrigToExp():
    assert TrigToExp(sin(x)) == -I*(exp(I*x) - exp(-I*x))/2
    assert TrigToExp(cos(x)) == exp(I*x)/2 + exp(-I*x)/2
    assert TrigToExp(cos(x)*tan(x**2)) == I*(exp(I*x)/2 + exp(-I*x)/2)*(-exp(I*x**2) + exp(-I*x**2))/(exp(I*x**2) + exp(-I*x**2))
    assert TrigToExp(cos(x) + sin(x)**2) == -(exp(I*x) - exp(-I*x))**2/4 + exp(I*x)/2 + exp(-I*x)/2
    assert eager_Simplify(TrigToExp(cos(x)*tan(x**S(2))*sin(x)**S(2))-(-I*(exp(I*x)/S(2) + exp(-I*x)/S(2))*(exp(I*x) - exp(-I*x))**S(2)*(-exp(I*x**S(2)) + exp(-I*x**S(2)))/(S(4)*(exp(I*x**S(2)) + exp(-I*x**S(2)))))) == 0

def test_ExpandTrigReduce():
    assert eager_ExpandTrigReduce(2*cos(3 + x)**3, x) == 3*cos(x + 3)/2 + cos(3*x + 9)/2
    assert eager_ExpandTrigReduce(2*sin(x)**3+cos(2 + x), x) == 3*sin(x)/2 - sin(3*x)/2 + cos(x + 2)
    assert eager_ExpandTrigReduce(cos(x + 3)**2, x) == cos(2*x + 6)/2 + S.Half

def test_NormalizeTrig():
    assert NormalizeTrig(S(2*sin(2 + x)), x) == 2*sin(x + 2)
    assert NormalizeTrig(S(2*sin(2 + x)**3), x) == 2*sin(x + 2)**3
    assert NormalizeTrig(S(2*sin((2 + x)**2)**3), x) == 2*sin(x**2 + 4*x + 4)**3

def test_FunctionOfTrigQ():
    v = log(x)
    s = sin(v)
    t = tan(v)
    assert not FunctionOfTrigQ(x, v, x)
    assert FunctionOfTrigQ(s + t, v, x)
    assert FunctionOfTrigQ(sin(t), v, x)

def test_RationalFunctionExpand():
    assert eager_RationalFunctionExpand(x**S(5)*(e + f*x)**n/(a + b*x**S(3)), x) == -a*x**2*(e + f*x)**n/(b*(a + b*x**3)) +\
        e**2*(e + f*x)**n/(b*f**2) - 2*e*(e + f*x)**(n + 1)/(b*f**2) + (e + f*x)**(n + 2)/(b*f**2)
    assert eager_RationalFunctionExpand(x**S(3)*(S(2)*x + 2)**S(2)/(2*x**2 + 1), x) == 2*x**3 + 4*x**2 + x + (- x + 2)/(2*x**2 + 1) - 2
    assert eager_RationalFunctionExpand((a + b*x + c*x**4)*log(x)**3, x) == a*log(x)**3 + b*x*log(x)**3 + c*x**4*log(x)**3
    assert eager_RationalFunctionExpand(a + b*x + c*x**4, x) == a + b*x + c*x**4

def test_SameQ():
    assert SameQ(1, 1, 1)
    assert not SameQ(1, 1, 2)

def test_Map2():
    assert Map2(Add, [a, b, c], [x, y, z]) == [a + x, b + y, c + z]

def test_ConstantFactor():
    assert ConstantFactor(a + a*x**3, x) == [a, x**3 + 1]
    assert ConstantFactor(a, x) == [a, 1]
    assert ConstantFactor(x, x) == [1, x]
    assert ConstantFactor(x**S(3), x) == [1, x**3]
    assert ConstantFactor(x**(S(3)/2), x) == [1, x**(S(3)/2)]
    assert ConstantFactor(a*x**3, x) == [a, x**3]
    assert ConstantFactor(a + x**3, x) == [1, a + x**3]

def test_CommonFactors():
    assert CommonFactors([a, a, a]) == [a, 1, 1, 1]
    # Mathematica: CommonFactors[{2x,2x^3,2x Sin[x]}] = {2x, 1, x^2, Sin[x]}
    assert CommonFactors([x*S(2), x**S(3)*S(2), sin(x)*x*S(2)]) == [2*x, 1, x**2, sin(x)]
    assert CommonFactors([x, x**S(3), sin(x)*x]) == [x, 1, x**2, sin(x)]
    assert CommonFactors([S(2), S(4), S(6)]) == [2, 1, 2, 3]

def test_FunctionOfLinear():
    f = sin(a + b*x)
    assert eager_FunctionOfLinear(f, x) == [sin(x), a, b]
    assert eager_FunctionOfLinear(a + b*x, x) == [x, a, b]
    assert not eager_FunctionOfLinear(a, x)

def test_FunctionOfExponentialQ():
    assert eager_FunctionOfExponentialQ(exp(x + exp(x) + exp(exp(x))), x)
    assert eager_FunctionOfExponentialQ(a**(a + b*x), x)
    assert eager_FunctionOfExponentialQ(a**(b*x), x)
    assert not eager_FunctionOfExponentialQ(a**sin(a + b*x), x)

def test_FunctionOfExponential():
    assert eager_FunctionOfExponential(a**(a + b*x), x)

def test_FunctionOfExponentialFunction():
    assert eager_FunctionOfExponentialFunction(a**(a + b*x), x) == x
    assert eager_FunctionOfExponentialFunction(S(2)*a**(a + b*x), x) == 2*x

def test_FunctionOfTrig():
    assert eager_FunctionOfTrig(sin(x + 1), x + 1, x) == x + 1
    assert eager_FunctionOfTrig(sin(x), x) == x
    assert not eager_FunctionOfTrig(cos(x**2 + 1), x)
    assert eager_FunctionOfTrig(sin(a+b*x)**3, x) == a+b*x

def test_AlgebraicTrigFunctionQ():
    assert AlgebraicTrigFunctionQ(sin(x + 3), x)
    assert AlgebraicTrigFunctionQ(x, x)
    assert AlgebraicTrigFunctionQ(x + 1, x)
    assert AlgebraicTrigFunctionQ(sinh(x + 1), x)
    assert AlgebraicTrigFunctionQ(sinh(x + 1)**2, x)
    assert not AlgebraicTrigFunctionQ(sinh(x**2 + 1)**2, x)

def test_FunctionOfHyperbolic():
    assert eager_FunctionOfTrig(sin(x + 1), x + 1, x) == x + 1
    assert eager_FunctionOfTrig(sin(x), x) == x
    assert not eager_FunctionOfTrig(cos(x**2 + 1), x)

def test_FunctionOfExpnQ():
    assert FunctionOfExpnQ(x, x, x) == 1
    assert FunctionOfExpnQ(x**2, x, x) == 2
    assert FunctionOfExpnQ(x**2.1, x, x) == 1
    assert not FunctionOfExpnQ(x, x**2, x)
    assert not FunctionOfExpnQ(x + 1, (x + 5)**2, x)
    assert not FunctionOfExpnQ(x + 1, (x + 1)**2, x)

def test_PureFunctionOfCosQ():
    v = log(x)
    f = cos(v)
    assert PureFunctionOfCosQ(f, v, x)
    assert not PureFunctionOfCosQ(sin(v), v, x)
    assert PureFunctionOfCosQ(f**2, v, x)

def test_PureFunctionOfCotQ():
    v = log(x)
    f = cot(v)
    assert PureFunctionOfCotQ(f, v, x)
    assert not PureFunctionOfCotQ(sin(v), v, x)
    assert PureFunctionOfCotQ(f**2, v, x)

def test_FunctionOfSinQ():
    v = log(x)
    assert FunctionOfSinQ(cos(sin(v)), v, x)
    assert FunctionOfSinQ(sin(v), v, x)
    assert FunctionOfSinQ(sin(v)*cos(sin(v)), v, x)

def test_FunctionOfCosQ():
    v = log(x)
    assert FunctionOfCosQ(cos(cos(v)), v, x)
    assert FunctionOfCosQ(cos(v), v, x)
    assert FunctionOfCosQ(cos(v)*cos(cos(v)), v, x)

def test_FunctionOfTanQ():
    v = log(x)
    t = tan(v)
    c = cot(v)
    assert FunctionOfTanQ(t, v, x)
    assert FunctionOfTanQ(c, v, x)
    assert FunctionOfTanQ(t + c, v, x)
    assert FunctionOfTanQ(t*c, v, x)
    assert not FunctionOfTanQ(sin(x), v, x)

def test_FunctionOfTanWeight():
    v = log(x)
    t = tan(v)
    c = cot(v)
    assert FunctionOfTanWeight(x, v, x) == 0
    assert FunctionOfTanWeight(sin(v), v, x) == 0
    assert FunctionOfTanWeight(tan(v), v, x) == 1
    assert FunctionOfTanWeight(cot(v), v, x) == -1
    assert FunctionOfTanWeight(t**2, v, x) == 1
    assert FunctionOfTanWeight(sin(v)**2, v, x) == -1
    assert FunctionOfTanWeight(cot(v)*sin(v)**2, v, x) == -2

def test_OddTrigPowerQ():
    assert not OddTrigPowerQ(sin(x)**3, 1, x)
    assert OddTrigPowerQ(sin(3),1,x)
    assert OddTrigPowerQ(sin(3*x),x,x)
    assert OddTrigPowerQ(sin(3*x)**3,x,x)

def test_FunctionOfLog():
    assert not eager_FunctionOfLog(x**2*(a + b*x)**3*exp(-a - b*x) ,False, False, x)
    assert eager_FunctionOfLog(log(2*x**8)*2 + log(2*x**8) + 1, x) == [3*x + 1, 2*x**8, 8]
    assert eager_FunctionOfLog(log(2*x)**2,x) == [x**2, 2*x, 1]
    assert eager_FunctionOfLog(log(3*x**3)**2 + 1,x) == [x**2 + 1, 3*x**3, 3]
    assert eager_FunctionOfLog(log(2*x**8)*2,x) == [2*x, 2*x**8, 8]
    assert not eager_FunctionOfLog(2*sin(x)*2,x)

def test_EulerIntegrandQ():
    assert eager_EulerIntegrandQ((2*x + 3*((x + 1)**3)**(S(3)/2))**(-3), x)
    assert not eager_EulerIntegrandQ((2*x + (2*x**2)**2)**3, x)
    assert not eager_EulerIntegrandQ(3*x**2 + 5*x + 1, x)

def test_Divides():
    assert not eager_Divides(x, a*x**2, x)
    assert eager_Divides(x, a*x, x) == a

def test_EasyDQ():
    assert EasyDQ(3*x**2, x)
    assert EasyDQ(3*x**3 - 6, x)
    assert EasyDQ(x**3, x)
    assert EasyDQ(sin(x**log(3)), x)

def test_ProductOfLinearPowersQ():
    assert ProductOfLinearPowersQ(S(1), x)
    assert ProductOfLinearPowersQ((x + 1)**3, x)
    assert not ProductOfLinearPowersQ((x**2 + 1)**3, x)
    assert ProductOfLinearPowersQ(x + 1, x)

def test_Rt():
    b = symbols('b')
    assert eager_Rt(-b**2, 4) == (-b**2)**(S(1)/S(4))
    assert eager_Rt(x**2, 2) == x
    assert eager_Rt(S(2 + 3*I), S(8)) == (2 + 3*I)**(S(1)/8)
    assert eager_Rt(x**2 + 4 + 4*x, 2) == x + 2
    assert eager_Rt(S(8), S(3)) == 2
    assert eager_Rt(S(16807), S(5)) == 7


def test_Rt_matches_mathematica():
    """Cross-checked against the real Rubi ``Rt`` in Mathematica (ssh pi, Rubi`
    IntegrationUtilityFunctions`). Generic (assumption-free) symbols so SymPy matches
    Mathematica's own no-assumptions evaluation."""
    aa, bb, cc = symbols('aa bb cc')
    # numeric: simplest nth root, sign handling for odd/even n
    assert eager_Rt(S(-8), 3) == -2                      # Mathematica: -2
    assert eager_Rt(S(-27), 3) == -3
    assert eager_Rt(S(-4), 2) == 2*I                     # even n, negative -> principal complex
    assert eager_Rt(S(12), 2) == 2*sqrt(3)
    assert eager_Rt(S(-12), 2) == 2*I*sqrt(3)
    assert eager_Rt(Rational(1, 4), 2) == Rational(1, 2)
    # symbolic: pull perfect powers out of products/powers
    assert eager_Rt(9*aa**2, 2) == 3*aa
    assert eager_Rt(aa**2*bb**4, 2) == aa*bb**2
    assert eager_Rt(8*aa**3, 3) == 2*aa
    assert eager_Rt(-8*aa**3, 3) == -2*aa
    assert eager_Rt((aa + bb)**2, 2) == aa + bb
    assert eager_Rt(-aa**3, 3) == -aa
    assert eager_Rt(bb**2/aa**2, 2) == bb/aa
    # sign distributed across factors (Mathematica: Sqrt[-a]*Sqrt[b]*Sqrt[c])
    assert eager_Rt(-aa*bb*cc, 2) == sqrt(-aa)*sqrt(bb)*sqrt(cc)


def test_NthRoot():
    assert NthRoot(S(14580), S(3)) == 9*2**(S(2)/S(3))*5**(S(1)/S(3))
    assert NthRoot(9, 2) == 3
    assert NthRoot(81, 2) == 9
    assert NthRoot(81, 4) == 3


def test_NthRoot_matches_mathematica():
    """NthRoot[u,n] := u^(1/n). Cross-checked against Mathematica: a rational radicand
    is factored into primes with 1/n distributed (14580^(1/3) -> 9*2^(2/3)*5^(1/3)),
    while a complex radicand stays a plain principal root (NOT expanded to a+b*I)."""
    aa = symbols('aa')
    assert NthRoot(S(8), 3) == 2
    assert NthRoot(S(-8), 3) == 2*(-1)**(S(1)/3)   # principal (complex) cube root
    assert NthRoot(S(-4), 2) == 2*I
    assert NthRoot(S(14580), 3) == 9*2**(S(2)/3)*5**(S(1)/3)
    assert NthRoot(aa, 2) == sqrt(aa)
    # complex radicand: plain principal root, matching Mathematica's Sqrt[2+3*I]
    assert NthRoot(S(2 + 3*I), 2) == sqrt(2 + 3*I)


def test_Rt_deferred_class():
    """rubi_utils.Rt is the DEFERRED node emitted into generated rules (codegen maps
    Rt -> Rt, not sympy.root). Constructing it must NOT evaluate -- the exponent n_
    is a wildcard at import time -- and .doit() must delegate to the eager Rt at fire
    time, once n is a concrete integer."""
    from rubi_rules.utils.rubi_utils import Rt as RtNode
    from rubi_rules.utils.utility_functions import eager_Rt
    from sympy_wolfram.objects import MathematicaExpr
    aa, bb = symbols('aa bb')
    node = RtNode(aa/bb, 2)
    assert isinstance(node, MathematicaExpr)           # unevaluated node
    assert node.func is RtNode
    assert node.doit() == eager_Rt(aa/bb, 2) == sqrt(aa)/sqrt(bb)
    # numeric evaluation through the node matches the eager function
    assert RtNode(S(8), 3).doit() == 2
    assert RtNode(S(-8), 3).doit() == -2

def test_AtomBaseQ():
    assert not AtomBaseQ(x**2)
    assert AtomBaseQ(x**3)
    assert AtomBaseQ(x)
    assert AtomBaseQ(S(2)**3)
    assert not AtomBaseQ(sin(x))

def test_SumBaseQ():
    assert not eager_SumBaseQ((x + 1)**2)
    assert eager_SumBaseQ((x + 1)**3)
    assert eager_SumBaseQ(3*x+3)
    assert not eager_SumBaseQ(x)

def test_NegSumBaseQ():
    assert not NegSumBaseQ(-x + 1)
    assert NegSumBaseQ(x - 1)
    assert not NegSumBaseQ((x - 1)**2)
    assert NegSumBaseQ((x - 1)**3)

def test_AllNegTermQ():
    x = Symbol('x', negative=True)
    assert AllNegTermQ(x)
    assert not AllNegTermQ(x + 2)
    assert AllNegTermQ(x - 2)
    assert AllNegTermQ((x - 2)**3)
    assert not AllNegTermQ((x - 2)**2)

def test_TrigSquareQ():
    assert TrigSquareQ(sin(x)**2)
    assert TrigSquareQ(cos(x)**2)
    assert not TrigSquareQ(tan(x)**2)

def test_Inequality():
    assert not Inequality(S('0'), Less, m, LessEqual, S('1'))
    assert Inequality(S('0'), Less, S('1'))
    assert Inequality(S('0'), Less, S('1'), LessEqual, S('5'))

def test_SplitProduct():
    assert eager_SplitProduct(eager_OddQ, S(3)*x) == [3, x]
    assert not eager_SplitProduct(eager_OddQ, S(2)*x)

def test_SplitSum():
    assert SplitSum(eager_FracPart, sin(x)) == [sin(x), 0]
    assert SplitSum(eager_FracPart, sin(x) + S(2)) == [sin(x), S(2)]

def test_Complex():
    assert eager_Complex(a, b) == a + I*b

def test_SimpFixFactor():
    assert SimpFixFactor((a*c + b*c)**S(4), x) == (a*c + b*c)**4
    assert SimpFixFactor((a*eager_Complex(0, c) + b*eager_Complex(0, d))**S(3), x) == -I*(a*c + b*d)**3
    assert SimpFixFactor((a*eager_Complex(0, d) + b*eager_Complex(0, e) + c*eager_Complex(0, f))**S(2), x) == -(a*d + b*e + c*f)**2
    assert SimpFixFactor((a + b*x**(-1/S(2))*x**S(3))**S(3), x) == (a + b*x**(S(5)/2))**3
    assert SimpFixFactor((a*c + b*c**S(2)*x**S(2))**S(3), x) == c**3*(a + b*c*x**2)**3
    assert SimpFixFactor((a*c**S(2) + b*c**S(1)*x**S(2))**S(3), x) == c**3*(a*c + b*x**2)**3
    assert SimpFixFactor(a*cos(x)**2 + a*sin(x)**2 + v, x) == a*cos(x)**2 + a*sin(x)**2 + v

def test_SimplifyAntiderivative():
    assert SimplifyAntiderivative(acoth(coth(x)), x) == x
    assert SimplifyAntiderivative(a*x, x) == a*x
    assert SimplifyAntiderivative(atanh(cot(x)), x) == atanh(2*sin(x)*cos(x))/2
    assert SimplifyAntiderivative(a*cos(x)**2 + a*sin(x)**2 + v, x) == a*cos(x)**2 + a*sin(x)**2

def test_FixSimplify():
    assert FixSimplify(x*eager_Complex(0, a)*(v*eager_Complex(0, b) + w)**S(3)) == a*x*(b*v - I*w)**3

def test_TrigSimplifyAux():
    assert TrigSimplifyAux(a*cos(x)**2 + a*sin(x)**2 + v) == a + v
    assert TrigSimplifyAux(x**2) == x**2

def test_SubstFor():
    assert eager_SubstFor(x**2 + 1, tanh(x), x) == tanh(x)
    assert eager_SubstFor(x**2, sinh(x), x) == sinh(sqrt(x))

def test_FresnelS():
    assert  FresnelS(oo) == S.Half
    assert FresnelS(0) == 0

def test_FresnelC():
    assert FresnelC(0) == 0
    assert FresnelC(oo) == S.Half

def test_Erfc():
    assert Erfc(0) == 1
    assert Erfc(oo) == 0

def test_Erfi():
    assert Erfi(oo) is oo
    assert Erfi(0) == 0

def test_Gamma():
    assert Gamma(u) == gamma(u)

def test_ElementaryFunctionQ():
    assert  ElementaryFunctionQ(x + y)
    assert ElementaryFunctionQ(sin(x + y))
    assert ElementaryFunctionQ(E**(x*a))

# Part / Util_Part moved to sympy_wolfram (behaviour tested in test_mathematica_functions.py).

def test_PolyLog():
    assert PolyLog(a, b) == polylog(a, b)

def test_PureFunctionOfCothQ():
    v = log(x)
    assert PureFunctionOfCothQ(coth(v), v, x)
    assert PureFunctionOfCothQ(a + coth(v), v, x)
    assert not PureFunctionOfCothQ(sin(v), v, x)

def test_ExpandIntegrand():
    assert eager_ExpandIntegrand(sqrt(a + b*x**S(2) + c*x**S(4)), (f*x)**(S(3)/2)*(d + e*x**S(2)), x) == \
        d*(f*x)**(S(3)/2)*sqrt(a + b*x**2 + c*x**4) + e*(f*x)**(S(7)/2)*sqrt(a + b*x**2 + c*x**4)/f**2
    assert eager_ExpandIntegrand((6*A*a*c - 2*A*b**2 + B*a*b - 2*c*x*(A*b - 2*B*a))/(x**2*(a + b*x + c*x**2)), x) == \
        (6*A*a*c - 2*A*b**2 + B*a*b)/(a*x**2) + (-6*A*a**2*c**2 + 10*A*a*b**2*c - 2*A*b**4 - 5*B*a**2*b*c + B*a*b**3 + x*(8*A*a*b*c**2 - 2*A*b**3*c - 4*B*a**2*c**2 + B*a*b**2*c))/(a**2*(a + b*x + c*x**2)) + (-2*A*b + B*a)*(4*a*c - b**2)/(a**2*x)
    assert eager_ExpandIntegrand(x**2*(e + f*x)**3*F**(a + b*(c + d*x)**1), x) == F**(a + b*(c + d*x))*e**2*(e + f*x)**3/f**2 - 2*F**(a + b*(c + d*x))*e*(e + f*x)**4/f**2 + F**(a + b*(c + d*x))*(e + f*x)**5/f**2
    assert eager_ExpandIntegrand((x)*(a + b*x)**2*f**(e*(c + d*x)**n), x) == a**2*f**(e*(c + d*x)**n)*x + 2*a*b*f**(e*(c + d*x)**n)*x**2 + b**2*f**(e*(c + d*x)**n)*x**3
    assert eager_ExpandIntegrand(sin(x)**3*(a + b*(1/sin(x)))**2, x) == a**2*sin(x)**3 + 2*a*b*sin(x)**2 + b**2*sin(x)
    assert eager_ExpandIntegrand(x*(a + b*ArcSin(c + d*x))**n, x) == -c*(a + b*asin(c + d*x))**n/d + (a + b*asin(c + d*x))**n*(c + d*x)/d
    assert simplify(eager_ExpandIntegrand((a + b*x)**S(3)*(A + B*x)/(c + d*x), x) - (B*(a + b*x)**3/d + b*(a + b*x)**2*(A*d - B*c)/d**2 + b*(a + b*x)*(A*d - B*c)*(a*d - b*c)/d**3 + b*(A*d - B*c)*(a*d - b*c)**2/d**4 + (A*d - B*c)*(a*d - b*c)**3/(d**4*(c + d*x)))) == 0
    assert eager_ExpandIntegrand((x**2)*(S(3)*x)**(S(1)/2), x) ==sqrt(3)*x**(S(5)/2)
    assert eager_ExpandIntegrand((x)*(sin(x))**(S(1)/2), x) == x*sqrt(sin(x))
    assert eager_ExpandIntegrand(x*(e + f*x)**2*F**(b*(c + d*x)), x) == -F**(b*(c + d*x))*e*(e + f*x)**2/f + F**(b*(c + d*x))*(e + f*x)**3/f
    assert eager_ExpandIntegrand(x**m*(e + f*x)**2*F**(b*(c + d*x)**n), x) == F**(b*(c + d*x)**n)*e**2*x**m + 2*F**(b*(c + d*x)**n)*e*f*x*x**m + F**(b*(c + d*x)**n)*f**2*x**2*x**m
    assert simplify(eager_ExpandIntegrand((S(1) - S(1)*x**S(2))**(-S(3)), x) - (-S(3)/(8*(x**2 - 1)) + S(3)/(16*(x + 1)**2) + S(1)/(S(8)*(x + 1)**3) + S(3)/(S(16)*(x - 1)**2) - S(1)/(S(8)*(x - 1)**3))) == 0
    assert eager_ExpandIntegrand(-S(1), 1/((-q - x)**3*(q - x)**3), x) == 1/(8*q**3*(q + x)**3) - 1/(8*q**3*(-q + x)**3) - 3/(8*q**4*(-q**2 + x**2)) + 3/(16*q**4*(q + x)**2) + 3/(16*q**4*(-q + x)**2)
    assert eager_ExpandIntegrand((1 + 1*x)**(3)/(2 + 1*x), x) == x**2 + x + 1 - 1/(x + 2)
    assert eager_ExpandIntegrand((c + d*x**1 + e*x**2)/(1 - x**3), x) == (c - (-1)**(S(1)/3)*d + (-1)**(S(2)/3)*e)/(-3*(-1)**(S(2)/3)*x + 3) + (c + (-1)**(S(2)/3)*d - (-1)**(S(1)/3)*e)/(3*(-1)**(S(1)/3)*x + 3) + (c + d + e)/(-3*x + 3)
    assert eager_ExpandIntegrand((c + d*x**1 + e*x**2 + f*x**3)/(1 - x**4), x) == (c + I*d - e - I*f)/(4*I*x + 4) + (c - I*d - e + I*f)/(-4*I*x + 4) + (c - d + e - f)/(4*x + 4) + (c + d + e + f)/(-4*x + 4)
    assert eager_ExpandIntegrand((d + e*(f + g*x))/(2 + 3*x + 1*x**2), x) == (-2*d - 2*e*f + 4*e*g)/(2*x + 4) + (2*d + 2*e*f - 2*e*g)/(2*x + 2)
    assert eager_ExpandIntegrand(x/(a*x**3 + b*Sqrt(c + d*x**6)), x) == a*x**4/(-b**2*c + x**6*(a**2 - b**2*d)) + b*x*sqrt(c + d*x**6)/(b**2*c + x**6*(-a**2 + b**2*d))
    assert simplify(eager_ExpandIntegrand(x**1*(1 - x**4)**(-2), x) - (x/(S(4)*(x**2 + 1)) + x/(S(4)*(x**2 + 1)**2) - x/(S(4)*(x**2 - 1)) + x/(S(4)*(x**2 - 1)**2))) == 0
    assert simplify(eager_ExpandIntegrand((-1 + x**S(6))**(-3), x) - (S(3)/(S(8)*(x**6 - 1)) - S(3)/(S(16)*(x**S(3) + S(1))**S(2)) - S(1)/(S(8)*(x**S(3) + S(1))**S(3)) - S(3)/(S(16)*(x**S(3) - S(1))**S(2)) + S(1)/(S(8)*(x**S(3) - S(1))**S(3)))) == 0
    assert simplify(eager_ExpandIntegrand(u**1*(a + b*u**2 + c*u**4)**(-1), x)) == simplify(1/(2*b*(u + sqrt(-(a + c*u**4)/b))) - 1/(2*b*(-u + sqrt(-(a + c*u**4)/b))))
    assert simplify(eager_ExpandIntegrand((1 + 1*u + 1*u**2)**(-2), x) - (S(1)/(S(2)*(-u - 1)*(-u**2 - u - 1)) + S(1)/(S(4)*(-u - 1)*(u + sqrt(-u - 1))**2) + S(1)/(S(4)*(-u - 1)*(u - sqrt(-u - 1))**2))) == 0
    assert eager_ExpandIntegrand(x*(a + b*Log(c*(d*(e + f*x)**p)**q))**n, x) == -e*(a + b*log(c*(d*(e + f*x)**p)**q))**n/f + (a + b*log(c*(d*(e + f*x)**p)**q))**n*(e + f*x)/f
    assert eager_ExpandIntegrand(x*f**(e*(c + d*x)*S(1)), x) == f**(e*(c + d*x))*x
    assert simplify(eager_ExpandIntegrand((x)*(a + b*x)**m*Log(c*(d + e*x**n)**p), x) - (-a*(a + b*x)**m*log(c*(d + e*x**n)**p)/b + (a + b*x)**(m + S(1))*log(c*(d + e*x**n)**p)/b)) == 0
    assert simplify(eager_ExpandIntegrand(u*(a + b*F**v)**S(2)*(c + d*F**v)**S(-3), x) - (b**2*u/(d**2*(F**v*d + c)) + 2*b*u*(a*d - b*c)/(d**2*(F**v*d + c)**2) + u*(a*d - b*c)**2/(d**2*(F**v*d + c)**3))) == 0
    assert simplify(eager_ExpandIntegrand((S(1) + 1*x)**S(2)*f**(e*(1 + S(1)*x)**n)/(g + h*x), x) - (f**(e*(x + 1)**n)*(x + 1)/h + f**(e*(x + 1)**n)*(-g + h)/h**2 + f**(e*(x + 1)**n)*(g - h)**2/(h**2*(g + h*x)))) == 0

    assert eager_ExpandIntegrand((a*c - b*c*x)**2/(a + b*x)**2, x) == 4*a**2*c**2/(a + b*x)**2 - 4*a*c**2/(a + b*x) + c**2
    assert simplify(eager_ExpandIntegrand(x**2*(1 - 1*x**2)**(-2), x) - (1/(S(2)*(x**2 - 1)) + 1/(S(4)*(x + 1)**2) + 1/(S(4)*(x - 1)**2))) == 0
    assert eager_ExpandIntegrand((a + x)**2, x) == a**2 + 2*a*x + x**2
    assert eager_ExpandIntegrand((a + b*x)**S(2)/x**3, x) == a**2/x**3 + 2*a*b/x**2 + b**2/x
    assert eager_ExpandIntegrand(1/(x**2*(a + b*x)**2), x) == b**2/(a**2*(a + b*x)**2) + 1/(a**2*x**2) + 2*b**2/(a**3*(a + b*x)) - 2*b/(a**3*x)
    assert eager_ExpandIntegrand((1 + x)**3/x, x) == x**2 + 3*x + 3 + 1/x
    assert eager_ExpandIntegrand((1 + 2*(3 + 4*x**2))/(2 + 3*x**2 + 1*x**4), x) == 18/(2*x**2 + 4) - 2/(2*x**2 + 2)
    assert eager_ExpandIntegrand((c + d*x**2 + e*x**3)/(1 - 1*x**4), x) == (c - d - I*e)/(4*I*x + 4) + (c - d + I*e)/(-4*I*x + 4) + (c + d - e)/(4*x + 4) + (c + d + e)/(-4*x + 4)
    assert simplify(eager_ExpandIntegrand((a + b*x)**2/(c + d*x), x) - (b*(a + b*x)/d + b*(a*d - b*c)/d**2 + (a*d - b*c)**2/(d**2*(c + d*x)))) == 0
    assert eager_ExpandIntegrand(x**2*(a + b*Log(c*(d*(e + f*x)**p)**q))**n, x) == e**2*(a + b*log(c*(d*(e + f*x)**p)**q))**n/f**2 - 2*e*(a + b*log(c*(d*(e + f*x)**p)**q))**n*(e + f*x)/f**2 + (a + b*log(c*(d*(e + f*x)**p)**q))**n*(e + f*x)**2/f**2
    assert eager_ExpandIntegrand(x*(1 + 2*x)**3*log(2*(1 + 1*x**2)**1), x) == 8*x**4*log(2*x**2 + 2) + 12*x**3*log(2*x**2 + 2) + 6*x**2*log(2*x**2 + 2) + x*log(2*x**2 + 2)
    assert simplify(eager_ExpandIntegrand((1 + 1*x)**S(3)*f**(e*(1 + 1*x)**n)/(g + h*x), x) - (f**(e*(x + 1)**n)*(x + 1)**2/h + f**(e*(x + 1)**n)*(-g + h)*(x + 1)/h**2 + f**(e*(x + 1)**n)*(-g + h)**2/h**3 - f**(e*(x + 1)**n)*(g - h)**3/(h**3*(g + h*x)))) == 0

def test_Dist():
    assert eager_Dist(x, a + b, x) == a*x + b*x
    assert eager_Dist(x, Integral(a + b , x), x) == x*Integral(a + b, x)
    assert eager_Dist(3*x,(a+b), x) - eager_Dist(2*x, (a+b), x) == a*x + b*x
    assert eager_Dist(3*x,(a+b), x) + eager_Dist(2*x, (a+b), x) == 5*a*x + 5*b*x
    assert eager_Dist(x, c*Integral((a + b), x), x) == c*x*Integral(a + b, x)

def test_IntegralFreeQ():
    assert not eager_IntegralFreeQ(Integral(a, x))
    assert eager_IntegralFreeQ(a + b)

def test_DerivativeDivides():
    assert not eager_DerivativeDivides(x, x, x)
    assert not eager_DerivativeDivides(a, x + y, b)
    assert eager_DerivativeDivides(a + x, a, x) == a
    assert eager_DerivativeDivides(a + b, x + y, b) == x + y

def test_LogIntegral():
    from rubi_rules.utils.utility_functions import LogIntegral
    assert LogIntegral(a) == li(a)

def test_SinIntegral():
    from rubi_rules.utils.utility_functions import SinIntegral
    assert SinIntegral(a) == Si(a)

def test_CosIntegral():
    from rubi_rules.utils.utility_functions import CosIntegral
    assert CosIntegral(a) == Ci(a)

def test_SinhIntegral():
    from rubi_rules.utils.utility_functions import SinhIntegral
    assert SinhIntegral(a) == Shi(a)

def test_CoshIntegral():
    from rubi_rules.utils.utility_functions import CoshIntegral
    assert CoshIntegral(a) == Chi(a)

def test_ExpIntegralEi():
    from rubi_rules.utils.utility_functions import ExpIntegralEi
    assert ExpIntegralEi(a) == Ei(a)

def test_ExpIntegralE():
    # standard Wolfram builtin -> now a sympy_wolfram deferred node, so .doit() it
    from rubi_rules.utils.utility_functions import ExpIntegralE
    assert ExpIntegralE(a, z).doit() == expint(a, z)

def test_LogGamma():
    from rubi_rules.utils.utility_functions import LogGamma
    assert LogGamma(a) == loggamma(a)

def test_Factorial():
    from rubi_rules.utils.utility_functions import Factorial
    assert Factorial(S(5)).doit() == 120

def test_Zeta():
    from rubi_rules.utils.utility_functions import Zeta
    assert Zeta(a, z).doit() == zeta(a, z)

def test_HypergeometricPFQ():
    from rubi_rules.utils.utility_functions import HypergeometricPFQ
    assert HypergeometricPFQ([a, b], [c], z) == hyper([a, b], [c], z)

def test_PolyGamma():
    assert PolyGamma(S(2), S(3)).doit() == polygamma(2, 3)

def test_ProductLog():
    from sympy.core.evalf import N
    assert N(ProductLog(S(5.0)).doit(), 5) == N(1.32672466524220, 5)
    assert N(ProductLog(S(2), S(3.5)).doit(), 5) == N(-1.14064876353898 + 10.8912237027092*I, 5)

def test_PolynomialQuotient():
    # value-equal to log(...)/((a+b x)(c+d x)); the consolidated eager uses sympy.quo
    # (as the deferred node the rules already used), which expands the denominator.
    got = eager_PolynomialQuotient(log((-a*d + b*c)/(b*(c + d*x)))/(c + d*x), a + b*x, e)
    assert (got - log((-a*d + b*c)/(b*(c + d*x)))/((a + b*x)*(c + d*x))).simplify() == 0
    assert eager_PolynomialQuotient(x**2, x + a, x) == -a + x


def test_PolynomialQuotient_rational_laurent():
    """A RATIONAL p (Rubi's Pq*(c x)^m with m<0, e.g. (A+Bx)/x^2) must divide as a Laurent
    polynomial, NOT return 0. Cross-checked vs real Rubi (ssh pi):
    PolynomialQuotient[(A+Bx)/x^2, a+b x^2, x] = (A+Bx)/(a x^2)."""
    A, B = symbols('A B')
    assert eager_PolynomialQuotient((A + B*x)/x**2, a + b*x**2, x) == (A + B*x)/(a*x**2)
    assert eager_PolynomialQuotient((A + B*x)/x, a + b*x**2, x) == A/(a*x)
    # denominator shares q -> quotient absorbs everything (value = (A+Bx)/(a+bx^2)^2,
    # returned with the denominator expanded), remainder 0
    got = eager_PolynomialQuotient((A + B*x)/(a + b*x**2), a + b*x**2, x)
    assert (got - (A + B*x)/(a + b*x**2)**2).simplify() == 0


def test_PolynomialRemainder():
    assert eager_PolynomialRemainder(log((-a*d + b*c)/(b*(c + d*x)))/(c + d*x), a + b*x, e) == 0
    assert eager_PolynomialRemainder(x**2, x + a, x) == a**2


def test_PolynomialRemainder_rational_laurent():
    """PolynomialRemainder[(A+Bx)/x^2, a+b x^2, x] = -b(A+Bx)/a (p reduced mod q, since
    x^2 == -a/b mod (a+b x^2) so x^-2 == -b/a). Cross-checked vs real Rubi (ssh pi)."""
    A, B = symbols('A B')
    assert eager_PolynomialRemainder((A + B*x)/x**2, a + b*x**2, x) == -A*b/a - B*b*x/a
    assert eager_PolynomialRemainder((A + B*x)/x, a + b*x**2, x) == B - A*b*x/a
    assert eager_PolynomialRemainder((A + B*x)/(a + b*x**2), a + b*x**2, x) == 0

def test_Floor():
    assert eager_Floor(S(7.5)) == 7
    assert eager_Floor(S(15.5), S(6)) == 12

def test_Factor():
    from rubi_rules.utils.utility_functions import Factor
    assert Factor(a*b + a*c) == a*(b + c)

def test_Rule():
    from rubi_rules.utils.utility_functions import eager_Rule
    assert eager_Rule(x, S(5)) == {x: 5}

def test_Distribute():
    assert Distribute((a + b)*c + (a + b)*d, Add) == c*(a + b) + d*(a + b)
    assert Distribute((a + b)*(c + e), Add) == a*c + a*e + b*c + b*e

def test_CoprimeQ():
    assert CoprimeQ(S(7), S(5))
    assert not CoprimeQ(S(6), S(3))

def test_Discriminant():
    """Mathematica-verified (12.2). Discriminant is a standard Wolfram builtin, so it
    lives in sympy_wolfram; the degenerate cases are where SymPy differs from MMA."""
    from sympy_wolfram.functions_eager import eager_Discriminant
    from sympy_wolfram.mathematica_functions import Discriminant
    assert eager_Discriminant(a*x**2 + b*x + c, x) == b**2 - 4*a*c
    assert eager_Discriminant(x**2 + 2*x + 1, x) == 0
    assert eager_Discriminant(x**4 - 1, x) == -256
    assert eager_Discriminant(3*x**2 - 5*x + 2, x) == 1
    assert eager_Discriminant(a*x + b, x) == 1
    # degree 0: MMA gives p^-2, NOT SymPy's 0
    assert eager_Discriminant(c, x) == 1/c**2
    assert eager_Discriminant(S(5), x) == S(1)/25
    assert eager_Discriminant(a + b, x) == (a + b)**-2
    assert eager_Discriminant(S(0), x) == 0
    # not a polynomial in x -> Mathematica leaves it unevaluated
    assert eager_Discriminant(sin(x), x) is None
    assert Discriminant(sin(x), x).doit() == Discriminant(sin(x), x)
    # the deferred node evaluates to the eager value
    assert Discriminant(a*x**2 + b*x + c, x).doit() == b**2 - 4*a*c

def test_Sum_doit():
    assert Sum_doit(2*x + 2, [x, 0, 1.7]) == 6

def test_DeactivateTrig():
    # DeactivateTrig turns active trig into inert markers AND canonicalizes the
    # co-functions into the primary family the way Rubi does (Pi-verified via the
    # DeactivateTrig battery): sec -> csc with a +pi/2 argument shift.
    from rubi_rules.utils.utility_functions import InertCsc
    assert eager_DeactivateTrig(sec(a + b*x), x) == InertCsc(a + b*x + pi/2)

def test_Quotient():
    from rubi_rules.utils.utility_functions import eager_Quotient
    assert eager_Quotient(17, 5) == 3

def test_process_trig():
    assert process_trig(x*cot(x)) == x/tan(x)
    assert process_trig(coth(x)*csc(x)) == S(1)/(tanh(x)*sin(x))


# ============================================================================
# Mathematica cross-verified tests
# ----------------------------------------------------------------------------
# Every expected value below was checked against the ACTUAL output of the
# corresponding Rubi function run in Wolfram Mathematica (Rubi 4.17.3.0, loaded
# via <<Rubi`IntegrationUtilityFunctions`), by comparing InputForm results and
# letting Mathematica judge equality (Simplify[ours == rubis]). They pin our
# behaviour to the Mathematica reference and guard the bugs fixed alongside them.
#
# Rubi 4.17 renamed several predicates (we keep the older names); those were
# verified against the equivalent form: ZeroQ(u)=EqQ[u,0], NonzeroQ=NeQ[,0],
# PositiveQ=GtQ[,0], NegativeQ=LtQ[,0], PositiveIntegerQ=IGtQ[,0],
# NegativeIntegerQ=ILtQ[,0].
# ============================================================================
import pytest as _pytest
from rubi_rules.utils import utility_functions as _U
from sympy_wolfram import functions_eager as _EAGER
from sympy import (Rational, sympify, simplify, sqrt, sin, cos, exp, log, pi, I,
                   sinh, asin, asinh, S)


def _meq(got, expected):
    """Boolean/list exact match, else symbolic equality (Simplify == 0)."""
    if isinstance(expected, bool) or isinstance(got, bool):
        return bool(got) == bool(expected)
    if isinstance(expected, (list, tuple)):
        return list(got) == list(expected)
    return simplify(sympify(got) - sympify(expected)) == 0


_MMA_PREDICATES = [
    (lambda: _U.eager_IntegerQ(S(7)), True),
    (lambda: _U.eager_IntegerQ(Rational(7, 2)), False),
    (lambda: _U.eager_RationalQ(Rational(3, 4)), True),
    (lambda: _U.eager_FractionQ(Rational(3, 4)), True),
    (lambda: _U.eager_FractionQ(S(3)), False),
    (lambda: _U.eager_EvenQ(S(6)), True),
    (lambda: _U.eager_OddQ(S(5)), True),
    (lambda: _U.eager_SumQ(a + b), True),
    (lambda: _U.eager_ProductQ(2 * a), True),
    (lambda: _U.eager_PowerQ(a**2), True),
    (lambda: _U.eager_IntegerPowerQ(a**2), True),
    (lambda: _U.eager_FractionalPowerQ(a**Rational(1, 2)), True),
    (lambda: _U.eager_LinearQ(2 + 3 * x, x), True),
    (lambda: _U.eager_LinearQ(x**2, x), False),
    (lambda: _U.eager_QuadraticQ(1 + x + x**2, x), True),
    (lambda: _U.eager_BinomialQ(1 + x**3, x), True),
    (lambda: _U.eager_TrinomialQ(1 + x**2 + x**4, x), True),
    (lambda: _U.eager_PolynomialQ(1 + x + x**5, x), True),
    (lambda: _U.eager_PolyQ(1 + x**2, x, S(2)), True),
    (lambda: _U.eager_PolyQ(x**3 + 1, x, S(3)), True),
    (lambda: _U.eager_TrigQ(sin(x)), True),
    (lambda: _U.eager_TrigQ(exp(x)), False),
    (lambda: _U.eager_HyperbolicQ(sinh(x)), True),
    (lambda: _U.eager_InverseTrigQ(asin(x)), True),
    (lambda: _U.eager_InverseHyperbolicQ(asinh(x)), True),
    (lambda: _U.eager_LogQ(log(x)), True),
    (lambda: _U.eager_AtomQ(x), True),
    (lambda: _U.eager_AtomQ(a + b), False),
    (lambda: _U.eager_ComplexNumberQ(2 + 3 * I), True),
    (lambda: _U.eager_IntegersQ(S(2), S(3)), True),
    (lambda: _U.eager_IntegersQ(S(2), Rational(3, 2)), False),
    (lambda: _U.eager_SqrtNumberQ(sqrt(2)), True),
    (lambda: _U.eager_NumberQ(S(3)), True),
    (lambda: _U.eager_NumericQ(pi), True),
    (lambda: _U.eager_RationalFunctionQ((1 + x) / (1 + x**2), x), True),
    (lambda: _U.eager_AlgebraicFunctionQ(sqrt(1 + x), x), True),
    (lambda: _U.eager_MonomialQ(3 * x**2, x), True),
    (lambda: _U.eager_LinearMatchQ(2 + 3 * x, x), True),
    (lambda: _U.eager_QuadraticMatchQ(1 + x + x**2, x), True),
    (lambda: _U.eager_BinomialMatchQ(1 + x**3, x), True),
    (lambda: _U.AbsurdNumberQ(sqrt(2)), True),
    (lambda: _U.eager_SumSimplerQ(x - 1, S(1)), True),
    (lambda: _U.eager_PosQ(a), True),
    (lambda: _U.eager_NegQ(-a), True),
    (lambda: _U.eager_NiceSqrtQ(S(4)), True),
    (lambda: _U.eager_NiceSqrtQ(S(2)), True),
    (lambda: _U.eager_PiecewiseLinearQ(2 + 3 * x, x), True),
    (lambda: _U.eager_QuotientOfLinearsQ((1 + x) / (2 + x), x), True),
    (lambda: _U.eager_InertTrigFreeQ(x**2), True),
    (lambda: _U.PolynomialTermQ(3 * x**2, x), True),
    (lambda: _U.eager_PerfectSquareQ(S(9)), True),
    (lambda: _U.eager_PerfectSquareQ(x**2), True),
    (lambda: _U.CalculusQ(x**2), False),
    (lambda: _U.SqrtNumberSumQ(1 + sqrt(2)), True),
    (lambda: _U.SqrtNumberSumQ(1 + x), False),
    (lambda: _U.eager_TrigSimplifyQ(x**2), False),
    (lambda: _U.eager_TrigHyperbolicFreeQ(x**2, x), True),
    (lambda: _U.eager_TrigHyperbolicFreeQ(sin(x), x), False),
    (lambda: _U.eager_InverseFunctionFreeQ(x**2, x), True),
    (lambda: _U.eager_InverseFunctionFreeQ(asin(x), x), False),
    (lambda: _U.eager_FunctionOfExponentialQ(exp(x) + exp(2 * x), x), True),
    (lambda: _U.eager_FunctionOfTrigOfLinearQ(sin(1 + 2 * x), x), True),
    (lambda: _U.eager_FunctionOfTrigOfLinearQ(x**2, x), False),
    (lambda: _U.SomeNegTermQ(-a + b), True),
    (lambda: _U.MergeableFactorQ(x, S(2), x), True),
    (lambda: _U.MergeableFactorQ(x, S(2), a), False),
]

# Our (older) predicate name verified against the Rubi 4.17 renamed equivalent.
_MMA_RENAMED = [
    (lambda: _U.ZeroQ(S(0)), True),                     # EqQ[0, 0]
    (lambda: _U.ZeroQ(a * e - b * d * S(0)), False),    # EqQ[a*e, 0]
    (lambda: _U.NonzeroQ(S(1)), True),                  # NeQ[1, 0]
    (lambda: _U.eager_PositiveQ(S(3)), True),                 # GtQ[3, 0]
    (lambda: _U.eager_NegativeQ(S(-3)), True),                # LtQ[-3, 0]
    (lambda: _U.PositiveIntegerQ(S(5)), True),          # IGtQ[5, 0]
    (lambda: _U.NegativeIntegerQ(S(-5)), True),         # ILtQ[-5, 0]
]

_MMA_EXPRESSIONS = [
    (lambda: _U.eager_Coeff(a + b * x + c * x**2, x, 2), c),
    (lambda: _U.eager_Coeff(a + b * x, x, 0), a),
    (lambda: _U.eager_Coeff(2 + 3 * x + 4 * x**2 + 5 * x**3, x, 3), S(5)),
    (lambda: _U.eager_Coefficient(3 + 5 * x + 7 * x**2, x, 1), S(5)),
    (lambda: _U.eager_Numerator((a + b) / c), a + b),
    (lambda: _U.eager_Numerator((a + b) / (c - d)), a + b),
    (lambda: _U.eager_Denominator((a + b) / (c * d)), c * d),
    (lambda: _U.eager_Denominator(a / (b**2 * c)), b**2 * c),
    (lambda: _U.eager_Numer((a + b) / c), a + b),
    (lambda: _U.eager_Denom(a / (b * c)), b * c),
    (lambda: _U.SmartNumerator(a / b), a),
    (lambda: _U.SmartDenominator(a / b**2), b**2),
    (lambda: _U.NumericFactor(6 * x * y), S(6)),
    (lambda: _U.NumericFactor(Rational(3, 5) * a), Rational(3, 5)),
    (lambda: _U.NumericFactor(2 * a + 4 * b), S(2)),
    (lambda: _U.NumericFactor(-3 * x), S(-3)),
    (lambda: _U.NumericFactor(-2 * a - 6 * b), S(-2)),
    (lambda: _U.eager_Expon(a + b * x**2 + c * x**5, x), S(5)),
    (lambda: _U.eager_Expon(x**7 + x**2, x), S(7)),
    (lambda: _U.eager_LeafCount(a * x**2 + b), S(7)),
    (lambda: _U.eager_ExpandToSum((2 * x + 1) * (x - 3), x), 2 * x**2 - 5 * x - 3),
    (lambda: _U.eager_ExpandIntegrand(1 / (x * (x + 1)), x), 1 / x - 1 / (1 + x)),
    (lambda: _U.eager_Together(1 / x + 1 / (x + 1)), (1 + 2 * x) / (x * (1 + x))),
    (lambda: _U.eager_Together(1 / a + 1 / b + 1 / c), (a * b + a * c + b * c) / (a * b * c)),
    (lambda: _U.eager_Rt(S(27), S(3)), S(3)),
    (lambda: _U.eager_Rt(S(9), S(2)), S(3)),
    (lambda: _U.eager_Rt(S(-27), S(3)), S(-3)),
    (lambda: _U.eager_Rt(x**2, S(2)), x),
    (lambda: _U.eager_Rt(x**4, S(2)), x**2),
    (lambda: _U.eager_Rt(S(16), S(4)), S(2)),
    (lambda: _U.eager_Simplify(sin(x)**2 + cos(x)**2), S(1)),
    (lambda: _U.eager_Sign(S(5)), S(1)),
    (lambda: _U.eager_FreeFactors(a * b * x, x), a * b),
    (lambda: _U.eager_NonfreeFactors(a * b * x, x), x),
    (lambda: _U.eager_FreeFactors(a**2 * x**3, x), a**2),
    (lambda: _U.eager_NonfreeFactors(a**2 * x**3, x), x**3),
    (lambda: _U.FreeTerms(a + b * x + c, x), a + c),
    (lambda: _U.NonfreeTerms(a + b * x + c, x), b * x),
    (lambda: _U.LeadTerm(a + b + c), a),
    (lambda: _U.RemainingTerms(a + b + c), b + c),
    (lambda: _U.LeadFactor(a * b * c), a),
    (lambda: _U.RemainingFactors(a * b * c), b * c),
    (lambda: _U.LeadBase(a**3), a),
    (lambda: _U.BinomialParts(3 + 5 * x**2, x), [S(3), S(5), S(2)]),
    (lambda: _U.BinomialParts(5 - 2 * x**3, x), [S(5), S(-2), S(3)]),
    (lambda: _U.eager_BinomialDegree(3 + 5 * x**4, x), S(4)),
    (lambda: _U.TrinomialParts(1 + 2 * x**2 + 3 * x**4, x), [S(1), S(2), S(3), S(2)]),
    (lambda: _U.TrinomialParts(2 + 3 * x**3 + 4 * x**6, x), [S(2), S(3), S(4), S(3)]),
    (lambda: _U.eager_TrinomialDegree(1 + x**2 + x**4, x), S(2)),
    (lambda: _U.GeneralizedBinomialParts(a * x + b * x**3, x), [a, b, S(3), S(1)]),
    (lambda: _U.eager_PolynomialQuotient(x**2 - 1, x - 1, x), 1 + x),
    (lambda: _U.eager_PolynomialQuotient(x**3 - 1, x - 1, x), 1 + x + x**2),
    (lambda: _U.eager_PolynomialRemainder(x**2 + 1, x - 1, x), S(2)),
    (lambda: _U.eager_PolynomialRemainder(x**3 + x + 1, x**2 + 1, x), S(1)),
    (lambda: _U.RemoveContent(6 * x + 9, x), 3 + 2 * x),
    (lambda: _EAGER.eager_Discriminant(a + b * x + c * x**2, x), b**2 - 4 * a * c),
    (lambda: _EAGER.eager_Discriminant(x**2 + 2 * x + 5, x), S(-16)),
    (lambda: _U.CoefficientList(1 + 2 * x + 3 * x**2, x), [S(1), S(2), S(3)]),
    (lambda: _U.eager_MinimumMonomialExponent(x**2 + x**3, x), S(2)),
    (lambda: _U.eager_ExpandTrigReduce(sin(x) * cos(x), x), sin(2 * x) / 2),
    (lambda: _U.eager_NormalizeIntegrand(x / x**2, x), 1 / x),
    (lambda: _U.eager_SimplifyIntegrand(x / x**2, x), 1 / x),
    (lambda: _U.eager_SimplifyIntegrand((x**2 - 1) / (x - 1), x), 1 + x),
    (lambda: _U.eager_IntPart(Rational(7, 2)), S(3)),
    (lambda: _U.eager_FracPart(Rational(7, 2)), Rational(1, 2)),
    (lambda: _U.eager_ExpandTrig(sin(2 * x), x), sin(2 * x)),
    (lambda: _U.NormalizeTogether(1 / x + 1 / (x + 1)), (1 + 2 * x) / (x * (1 + x))),
    (lambda: _U.SmartSimplify(sin(x)**2 + cos(x)**2), S(1)),
    (lambda: _U.eager_ExpandExpression((x + 1) * (x + 2), x), 2 + 3 * x + x**2),
    (lambda: _U.NormalizeSumFactors(2 * a + 2 * b), 2 * a + 2 * b),
    (lambda: _U.eager_Simp(2 * x + 3 * x, x), 5 * x),
    (lambda: _U.SmartApart(1 / (x * (x + 1)), x), 1 / x - 1 / (x + 1)),
    (lambda: _U.FactorAbsurdNumber(S(12)), [(2, 2), (3, 1)]),
    (lambda: _U.AbsurdNumberGCD(S(4), S(6)), S(2)),
    (lambda: _U.AbsurdNumberGCD(S(12), S(18), S(30)), S(6)),
    (lambda: _U.ExpandTrigReduceAux(sin(x) * cos(x), x), sin(2 * x) / 2),
]

# Regression guards for bugs found & fixed via Mathematica cross-checking.
_MMA_BUGFIXES = [
    # IntPart/FracPart: Mathematica truncates toward zero (was floor-based).
    (lambda: _U.eager_IntPart(Rational(-7, 2)), S(-3)),              # was -4
    (lambda: _U.eager_FracPart(Rational(-7, 2)), Rational(-1, 2)),   # was 1/2
    (lambda: _U.eager_IntPart(Rational(-5, 3)), S(-1)),
    (lambda: _U.eager_FracPart(Rational(-5, 3)), Rational(-2, 3)),
    (lambda: _U.IntegerPart(S(-3.6)), S(-3)),                  # was -4
    (lambda: _U.IntegerPart(Rational(-7, 2)), S(-3)),
    (lambda: _U.FractionalPart(Rational(-7, 2)), Rational(-1, 2)),
    # LeadDegree of a non-power lead factor is 1 (was returning the factor).
    (lambda: _U.LeadDegree(8 * x**3), S(1)),                   # LeadFactor is 8 -> degree 1
    (lambda: _U.LeadDegree(x**3), S(3)),
    (lambda: _U.LeadDegree(a**b), b),
    # RemoveContent of an x-free sum is 1 (was crashing on a bare atom).
    (lambda: _U.RemoveContent(2 * a + 4 * b, x), S(1)),
    # SubstForExpn rebuilds with the arg's head (Map); was summing -> x^2 gave a+2.
    (lambda: _U.SubstForExpn(x**2, x, a), a**2),
    (lambda: _U.SubstForExpn(x**2 + x, x, a), a**2 + a),
    # PolynomialTermQ: a constant is a polynomial term (Rubi's FreeQ clause).
    (lambda: _U.PolynomialTermQ(S(3), x), True),
    (lambda: _U.PolynomialTerms(x + 6 * x**3 + 6, x), 6 * x**3 + x + 6),
    (lambda: _U.NonpolynomialTerms(x + 6 * x**3 + 6, x), S(0)),
]


@_pytest.mark.parametrize("call, expected", _MMA_PREDICATES, ids=range(len(_MMA_PREDICATES)))
def test_mma_predicates(call, expected):
    assert _meq(call(), expected)


@_pytest.mark.parametrize("call, expected", _MMA_RENAMED, ids=range(len(_MMA_RENAMED)))
def test_mma_renamed_predicates(call, expected):
    assert _meq(call(), expected)


@_pytest.mark.parametrize("call, expected", _MMA_EXPRESSIONS, ids=range(len(_MMA_EXPRESSIONS)))
def test_mma_expressions(call, expected):
    assert _meq(call(), expected)


@_pytest.mark.parametrize("call, expected", _MMA_BUGFIXES, ids=range(len(_MMA_BUGFIXES)))
def test_mma_bugfix_regressions(call, expected):
    assert _meq(call(), expected)


# ============================================================================
# Deferred MathematicaExpr node fixes (rubi_utils) verified against Mathematica
# ============================================================================
def test_deferred_SubstFor_delegates_to_eager():
    # The deferred SubstFor used a naive u.subs(v, x); it must delegate to the eager
    # implementation, so SubstFor(b*x, x, x) = x/b (NOT x). The missing 1/b silently
    # multiplied symbolic-coefficient integrals by the linear coefficient.
    from rubi_rules.utils.rubi_utils import SubstFor as _DSubstFor
    xx, bb = Symbol('x'), Symbol('b')
    assert _DSubstFor(bb*xx, xx, xx).doit() == xx/bb
    assert _DSubstFor(xx, xx, xx).doit() == xx


def test_deferred_PolynomialRemainder_transcendental():
    # Mathematica treats a transcendental-in-x expression as degree 0 in x:
    # PolynomialRemainder[log(...x...), q, x] = log(...), PolynomialQuotient = 0.
    # sympy.rem/quo raise PolynomialError there; the nodes now match Mathematica.
    from rubi_rules.utils.rubi_utils import PolynomialRemainder as _PRem, PolynomialQuotient as _PQuo
    from sympy import log
    xx, bb, aa = Symbol('x'), Symbol('b'), Symbol('a')
    p = log(-bb*xx/aa)
    assert _PRem(p, xx**2 + 1, xx).doit() == p
    assert _PQuo(p, xx**2 + 1, xx).doit() == 0
    # ordinary polynomial division still works
    assert _PRem(xx**2 + 1, xx - 1, xx).doit() == 2
    assert _PQuo(xx**2 - 1, xx - 1, xx).doit() == xx + 1


def test_Simplify_resolves_deferred_nodes_no_recursion():
    # Simplify must resolve deferred MathematicaExpr nodes (Coeff, …) before
    # sympy.simplify: a product of unevaluated ones like Coeff(6x+4,x,0)*Coeff(6x+4,x,4)
    # (= 4*0 = 0) otherwise drives sympy's nc_simplify into a RecursionError.
    from rubi_rules.utils.rubi_utils import Coeff as _DCoeff
    from rubi_rules.utils.utility_functions import eager_Simplify
    xx = Symbol('x')
    assert eager_Simplify(_DCoeff(6*xx + 4, xx, 0) * _DCoeff(6*xx + 4, xx, 4)) == 0
    # ordinary expressions still simplify normally
    assert eager_Simplify((xx**2 - 1) / (xx - 1)) == xx + 1


# NOTE: IntHide's end-to-end integration behaviour needs the full rule set, so its
# test lives in the single consolidated slow test (test_integrate_exp_gaussian.py::
# test_full_ruleset_integrals -> _check_inthide), keeping all full-rule-set-loading
# tests in one place.


def test_Dist_two_arg_distributes():
    # Rubi also uses a 2-arg Dist[u, v] (no integration variable) -- distribute u
    # over the terms of v. Passing 2 args to the eager 3-arg Dist raised TypeError.
    from rubi_rules.utils.rubi_utils import Dist as _Dist
    aa, bb, xx = Symbol('a'), Symbol('b'), Symbol('x')
    assert _Dist(aa, bb*xx + xx**2).doit() == aa*bb*xx + aa*xx**2
    assert _Dist(aa, xx**2).doit() == aa*xx**2


def test_deferred_Coeff_symbolic_n_delegates():
    # Deferred Coeff[u, x, n] used `u.coeff(x, int(n))`, which crashed on a symbolic
    # n ('Cannot convert symbols to int') -- aborting the DFS for e.g.
    # x^3*(a+b*atanh(c*x)). It must delegate to the eager Coeff (which handles it).
    from rubi_rules.utils.rubi_utils import Coeff as _Coeff
    from rubi_rules.utils.utility_functions import eager_Coeff
    aa, bb, cc, xx, nn = symbols('a b c x n')
    expr = aa + bb*xx + cc*xx**3
    # concrete n still works
    assert _Coeff(expr, xx, 3).doit() == cc
    assert _Coeff(expr, xx, 0).doit() == aa
    # symbolic n no longer crashes; matches the eager utility
    assert _Coeff(expr, xx, nn).doit() == eager_Coeff(expr, xx, nn)


def test_comparisons_on_non_real_do_not_crash():
    # sympy raises TypeError on an ordering comparison of a non-real (e.g. -2*I).
    # Mathematica leaves Less/Greater unevaluated there, so TrueQ[...] is False.
    # Verified on the Pi: TrueQ[Less[-2 I, 3]] -> False. Our predicates must return
    # False (not crash) -- this used to abort the DFS for e.g. atanh(a+b*x)^2.
    from rubi_rules.utils.utility_functions import (
        Less, Greater, LessEqual, GreaterEqual)
    for fn in (Less, Greater, LessEqual, GreaterEqual):
        assert fn(-2*I, 3) is False
        assert fn(I, 2) is False
    # real comparisons still work
    assert Less(1, 2, 3) is True
    assert Less(1, 3, 2) is False
    assert Greater(3, 2, 1) is True


def test_PosAux_robust_to_nan_and_non_real():
    """PosAux/PosQ used a bare `Re(u) > 0` / `u > 0` that aborted the DFS when the
    value was NaN ("Invalid NaN comparison") or non-real ("cannot determine truth
    value of Relational"). Two corpus integrands crashed here:
    1/((d+e*x)*(c*(d+e*x)^2)) and x^6/(3*x^4+2). Must not raise; sign of an
    undeterminable numeric value is treated as not-positive (rule just doesn't apply)."""
    from sympy import S, I, root
    from rubi_rules.utils.utility_functions import PosAux, eager_PosQ
    crash_vals = [S.NaN,
                  -3*root(6, 4)*(1 + I)**3 + 6*root(6, 4)*(1 + I)]  # from x^6/(3x^4+2)
    for v in crash_vals:
        PosAux(v)   # must not raise
        eager_PosQ(v)     # must not raise
    assert PosAux(S.NaN) is False
    # normal behaviour preserved (symbols positive; negatives negative)
    aa = Symbol('a')
    assert bool(eager_PosQ(aa)) is True
    assert bool(eager_PosQ(-aa)) is False


def test_Simplify_robust_to_boolean_from_non_binomial():
    # BinomialDegree/TrinomialDegree return False on a non-binomial/-trinomial.
    # An EqQ of two such degrees (used as a rule constraint) forms
    # `BinomialDegree(u1,x) - BinomialDegree(u2,x)`, whose doit/simplify hits a
    # BooleanFalse inside arithmetic ('BooleanFalse has no as_coeff_Mul'). Simplify
    # must swallow that and ZeroQ/EqQ must return a plain bool, not crash.
    from rubi_rules.utils.utility_functions import eager_Simplify, ZeroQ as _Z, eager_EqQ
    from rubi_rules.utils.rubi_utils import BinomialDegree as _BD
    xx, aa, bb = Symbol('x'), Symbol('a'), Symbol('b')
    expr = _BD(exp(xx), xx) - _BD(aa + bb*exp(xx), xx)
    eager_Simplify(expr)  # must not raise
    assert _Z(expr) in (True, False)
    assert eager_EqQ(_BD(exp(xx), xx), _BD(aa + bb*exp(xx), xx)) in (True, False)


def test_MinimumMonomialExponent_skips_non_monomial_terms():
    # A sum with a non-monomial-in-x term (e.g. b*exp(x)) must not crash: in
    # Mathematica MonomialExponent stays unevaluated there, so the term is skipped.
    # Previously `n - MonomialExponent(...)` raised `Zero - None` TypeError, which
    # aborted the whole DFS search for e.g. Int[(a+b*E^x)^n*E^x, x].
    aa, bb, xx = Symbol('a'), Symbol('b'), Symbol('x')
    assert _U.eager_MinimumMonomialExponent(aa + bb*exp(xx), xx) == 0
    # ordinary monomial sums still give the smallest exponent
    assert _U.eager_MinimumMonomialExponent(xx**2 + 5*xx**2 + 3*xx**5, xx) == 2
    assert _U.eager_MinimumMonomialExponent(xx**2 + 5*xx**2 + 1, xx) == 0


def test_WFApply_applies_a_bound_wildcard_head():
    # A Rubi rule `F_[v_]` binds F to a function HEAD; the replacement re-applies
    # it as `F[newarg]`. The matched head arrives as a HeadRef (a function class is
    # not a substitutable SymPy object), and WFApply applies it on doit.
    from rubi_rules.utils.rubi_utils import WFApply
    from sympy_matching.wild import HeadRef
    from sympy import sin, asin, Function
    xx, yy = Symbol('x'), Symbol('y')
    assert WFApply(HeadRef(sin), yy).doit() == sin(yy)
    assert WFApply(HeadRef(asin), 2*yy).doit() == asin(2*yy)
    f = Function('f')
    assert WFApply(HeadRef(f), yy + 1).doit() == f(yy + 1)
    # a whole matched application is also accepted (its .func is used)
    assert WFApply(sin(xx), yy).doit() == sin(yy)


def test_WFApply_stays_unevaluated_until_the_head_is_known():
    # Before substitution the head slot still holds a wildcard, so WFApply must
    # remain unevaluated rather than return None (which would break the enclosing
    # Add/Mul via sympify(None)).
    from rubi_rules.utils.rubi_utils import WFApply
    from sympy_matching.wild import WildSymbol
    F, xx = WildSymbol('F'), Symbol('x')
    node = WFApply(F, xx)
    assert node.doit() is not None
    assert isinstance(node.doit(), WFApply)
    assert (Symbol('y') * node).doit() is not None


def test_WFApply_multiple_arguments():
    from rubi_rules.utils.rubi_utils import WFApply
    from sympy_matching.wild import HeadRef
    from sympy import Function
    g = Function('g')
    xx, yy = Symbol('x'), Symbol('y')
    assert WFApply(HeadRef(g), xx, yy).doit() == g(xx, yy)


def test_WFDeriv_differentiates_a_bound_wildcard_head():
    # WFDeriv[f, x, n] is the replacement-side counterpart of the
    # Derivative[n_][f_][x_] pattern: once f is bound to a real function head it
    # must rebuild a genuine SymPy Derivative.
    from rubi_rules.utils.rubi_utils import WFDeriv
    from sympy_matching.wild import HeadRef
    from sympy import Function, Derivative
    f = Function('f')
    xx = Symbol('x')
    assert WFDeriv(HeadRef(f), xx, 2).doit() == Derivative(f(xx), (xx, 2))
    assert WFDeriv(HeadRef(f), xx, 1).doit() == Derivative(f(xx), xx)


def test_WFDeriv_order_zero_is_the_plain_application():
    from rubi_rules.utils.rubi_utils import WFDeriv
    from sympy_matching.wild import HeadRef
    from sympy import Function
    f = Function('f')
    xx = Symbol('x')
    assert WFDeriv(HeadRef(f), xx, 0).doit() == f(xx)


def test_WFDeriv_accepts_an_applied_head_like_WFApply():
    # A head slot may arrive already applied (sin(x)); the func is taken from it.
    from rubi_rules.utils.rubi_utils import WFDeriv
    from sympy import sin, Derivative
    xx = Symbol('x')
    assert WFDeriv(sin(xx), xx, 1).doit() == Derivative(sin(xx), xx)


def test_WFDeriv_stays_unevaluated_until_the_head_is_known():
    # Before substitution the head slot still holds a wildcard: there is nothing
    # to differentiate, so the node must survive doit() intact.
    from rubi_rules.utils.rubi_utils import WFDeriv
    from sympy_matching.wild import WildSymbol
    F = WildSymbol('F')
    xx = Symbol('x')
    node = WFDeriv(F, xx, 2)
    assert isinstance(node.doit(), WFDeriv)


def test_WFDeriv_of_a_known_function_evaluates_through():
    # sin is differentiable, so SymPy's Derivative collapses it.
    from rubi_rules.utils.rubi_utils import WFDeriv
    from sympy_matching.wild import HeadRef
    from sympy import sin, cos
    xx = Symbol('x')
    assert WFDeriv(HeadRef(sin), xx, 1).doit().doit() == cos(xx)


# ---------------------------------------------------------------------------
# Expon[u, x, Min/Max] -- Rubi passes the selector as a bare SYMBOL, not a call.
# ---------------------------------------------------------------------------

def test_Expon_two_arg_gives_the_maximum_degree():
    from rubi_rules.utils.rubi_utils import Expon
    xx = Symbol('x')
    assert Expon(2*xx**5 + 3*xx**3, xx).doit() == 5


def test_Expon_Min_selector_gives_the_minimum_degree():
    from rubi_rules.utils.rubi_utils import Expon
    xx = Symbol('x')
    assert Expon(2*xx**5 + 3*xx**3, xx, Symbol('Min')).doit() == 3


def test_Expon_Max_selector_matches_the_two_arg_form():
    from rubi_rules.utils.rubi_utils import Expon
    xx = Symbol('x')
    p = 2*xx**5 + 3*xx**3
    assert Expon(p, xx, Symbol('Max')).doit() == Expon(p, xx).doit() == 5


def test_Expon_Min_on_a_polynomial_with_a_constant_term_is_zero():
    from rubi_rules.utils.rubi_utils import Expon
    xx = Symbol('x')
    assert Expon(xx**4 + 7, xx, Symbol('Min')).doit() == 0


def test_Expon_Min_on_a_monomial_is_its_degree():
    from rubi_rules.utils.rubi_utils import Expon
    xx = Symbol('x')
    assert Expon(5*xx**3, xx, Symbol('Min')).doit() == 3


# ---------------------------------------------------------------------------
# RationalFunctionExponents -- Mathematica scales a list by a scalar
# element-wise (n*{a,b} == {n a, n b}); Python REPEATS it (n*[a,b]), so this
# used to return e.g. [0,1,0,1] for (x+1)^-2. Expected values below were read
# off real Rubi in Mathematica.
# ---------------------------------------------------------------------------

_RFE_CASES = [
    (lambda x: (x + 1)**-2,      [0, 2]),
    (lambda x: (x + 1)**-3,      [0, 3]),
    (lambda x: (x + 1)**2,       [2, 0]),
    (lambda x: 1/(x**2 + 1),     [0, 2]),
    (lambda x: x/(x**2 + 1),     [1, 2]),
    (lambda x: (x**2 + 1)**-2,   [0, 4]),
    (lambda x: x**3/(x + 1)**2,  [3, 2]),
]


def test_RationalFunctionExponents_matches_mathematica():
    xx = Symbol('x')
    for expr_fn, expected in _RFE_CASES:
        e = expr_fn(xx)
        assert list(eager_RationalFunctionExponents(e, xx)) == expected, e


def test_RationalFunctionExponents_always_returns_a_pair():
    """The list-repetition bug showed up as a 4- or 6-element result."""
    xx = Symbol('x')
    for expr_fn, _ in _RFE_CASES:
        assert len(eager_RationalFunctionExponents(expr_fn(xx), xx)) == 2


# ---------------------------------------------------------------------------
# A sympy `.match()` can SUCCEED while binding only SOME of its wildcards.
# Indexing the result unconditionally then raises KeyError mid-integration --
# found by the corpus runner on x**(m+1)/sqrt(a+b*x), x**m/sqrt(-3*x-2) and
# (-x)**m/sqrt(3*x-2), which aborted with `KeyError: u_` / `KeyError: n_`.
# ---------------------------------------------------------------------------

def test_PowerOfLinearQ_on_a_constant_does_not_crash():
    """1 matches u**m as m=0 with u UNBOUND, so Match[u] used to raise."""
    xx = Symbol('x')
    assert eager_PowerOfLinearQ(S(1), xx) is False


def test_PowerOfLinearQ_still_recognises_a_power_of_a_linear():
    xx = Symbol('x')
    assert eager_PowerOfLinearQ((2 + 3*xx)**4, xx) is True


def test_PowerOfLinearQ_rejects_a_non_linear_base():
    xx = Symbol('x')
    assert eager_PowerOfLinearQ((1 + xx**2)**3, xx) is False


def test_GeneralizedBinomialMatchQ_rejects_a_single_monomial():
    """A single monomial is not a binomial: -3*x/2 used to slip through on a
    spurious -x/2 + -x split and GeneralizedBinomialParts was then handed a
    non-binomial.

    The reason Rubi rejects it is purely structural -- a two-addend Plus pattern
    cannot bind a one-term expression -- NOT a PosQ[n-q] side condition, which this
    docstring used to claim. Rubi 4.17.3.0 defines
    ``MatchQ[u, a_.*x^q_. + b_.*x^n_. /; FreeQ[{a,b,n,q}, x]]`` with no such guard;
    confirmed directly, ``MatchQ[-3x/2, a_. x^q_. + b_. x^n_.]`` is False.
    """
    xx = Symbol('x')
    assert eager_GeneralizedBinomialMatchQ(Rational(-3, 2)*xx, xx) is False
    assert eager_GeneralizedBinomialMatchQ(3*xx, xx) is False


def test_GeneralizedBinomialMatchQ_accepts_equal_exponents():
    """Rubi's pattern has NO q != n condition, so `a*x^2 + b*x^2` matches.

    Verified against Rubi 4.17.3.0: GeneralizedBinomialMatchQ[a x^2 + b x^2, x] is
    True (while GeneralizedBinomialParts of the same input is False -- the MatchQ
    pre-filter is deliberately looser than Parts). SymPy keeps that as a two-term
    Add, since it only collects addends differing by a numeric factor, so an added
    distinctness test really did make us answer False where Rubi answers True.
    """
    xx, aa, bb = Symbol('x'), Symbol('a'), Symbol('b')
    assert eager_GeneralizedBinomialMatchQ(aa*xx**2 + bb*xx**2, xx) is True
    assert eager_GeneralizedBinomialMatchQ(aa*xx**3 + bb*xx**3, xx) is True
    assert eager_GeneralizedBinomialMatchQ(aa*xx**2 + bb*xx**5, xx) is True
    # a term free of x still cannot bind `x^q_.`, so this stays False
    assert eager_GeneralizedBinomialMatchQ(aa + bb*xx**2, xx) is False


def test_GeneralizedBinomialParts_on_a_single_monomial_is_False():
    """Rubi's final clause: GeneralizedBinomialParts[u_, x_] := False."""
    xx = Symbol('x')
    assert GeneralizedBinomialParts(Rational(-3, 2)*xx, xx) is False
    assert GeneralizedBinomialParts(3*xx, xx) is False


def test_GeneralizedBinomialParts_still_decomposes_a_genuine_one():
    xx = Symbol('x')
    assert GeneralizedBinomialParts(3*xx**5 + 2*xx**2, xx) == [2, 3, 5, 2]


def test_GeneralizedBinomialParts_uses_the_same_wildcards_as_its_gate():
    """The gate and the decomposition must agree on what a generalized binomial is.
    With looser exclusions the re-match could return a DEGENERATE solution the gate
    had rejected (b=0, leaving n unbound) and raise KeyError."""
    xx = Symbol('x')
    for expr in (Rational(-3, 2)*xx, 3*xx**5 + 2*xx**2, xx**3, S(4)):
        gated = eager_GeneralizedBinomialMatchQ(expr, xx)
        parts = GeneralizedBinomialParts(expr, xx)      # must never raise
        assert gated is True or parts is False, (expr, gated, parts)


# ---------------------------------------------------------------------------
# The DEFERRED ExpandIntegrand must delegate to the eager one, not re-implement
# it with sympy.expand. Re-implementing gave x/(a+b*x)^2 -> x/(a^2+2abx+b^2x^2)
# (denominator multiplied out) instead of the partial-fraction expansion, which
# fed rule 1.1.1.2#12 a re-expandable form and caused an infinite descent with
# geometrically growing coefficients (x/(a+b*x)^2 timed out; x^2/(a+b*x)^2
# "solved" to a junk form carrying 1073741824*b**30).
# ---------------------------------------------------------------------------

def test_deferred_ExpandIntegrand_matches_eager():
    from rubi_rules.utils.rubi_utils import ExpandIntegrand as Deferred
    from rubi_rules.utils.utility_functions import eager_ExpandIntegrand
    xx, a, b = Symbol('x'), Symbol('a'), Symbol('b')
    for u in [xx/(a + b*xx)**2, xx**2/(a + b*xx)**2, 1/(xx*(a + b*xx))]:
        assert Deferred(u, xx).doit() == eager_ExpandIntegrand(u, xx), u


def test_deferred_ExpandIntegrand_does_partial_fractions_not_denominator_expansion():
    from rubi_rules.utils.rubi_utils import ExpandIntegrand as Deferred
    xx, a, b = Symbol('x'), Symbol('a'), Symbol('b')
    result = Deferred(xx/(a + b*xx)**2, xx).doit()
    # partial fractions: 1/(b(a+bx)) - a/(b(a+bx)^2); the WRONG (plain expand)
    # answer x/(a^2+2abx+b^2x^2) has an expanded denominator, so (a+b*x)**2 must
    # still appear as a factor in the correct result.
    assert result.has((a + b*xx)**2) or result.has((a + b*xx)**(-2)), result
    assert not result.has(a**2 + 2*a*b*xx + b**2*xx**2)


def test_deferred_ExpandIntegrand_three_arg_still_expands_product():
    """The 3-arg form (u, v, x) legitimately expands u*v; delegation preserves it."""
    from rubi_rules.utils.rubi_utils import ExpandIntegrand as Deferred
    from rubi_rules.utils.utility_functions import eager_ExpandIntegrand
    xx = Symbol('x')
    u, v = (xx + 1), (xx + 2)
    assert Deferred(u, v, xx).doit() == eager_ExpandIntegrand(u, v, xx)


# ---------------------------------------------------------------------------
# Hyperbolic secant/cosecant via Rubi's inert-trig unification.
# Rubi has no sech^m(a+b sech^n)^p rules; it DeactivateTrig's sech(z)->sec(I z)
# (inert) and lets the CIRCULAR sec rules integrate it (Tan[I z] -> Tanh). Our
# generated rules match ACTIVE sympy.sec, and sympy.sec(I z) auto-collapses to
# 1/cosh, so DeactivateTrig builds InertSec=Function('sec'); its matcher head is
# registered (forward only) to the active sec head so it matches those rules.
# ---------------------------------------------------------------------------

def test_DeactivateTrig_sech_becomes_inert_sec_of_imaginary_argument():
    """Pi-verified: DeactivateTrig[Sech^2/(a+b Sech^2)] = sec[I z]^2/(a+b sec[I z]^2)."""
    from rubi_rules.utils.utility_functions import eager_DeactivateTrig, InertSec
    xx, a, b, c, d = symbols('x a b c d')
    u = sech(c + d*xx)**2/(a + b*sech(c + d*xx)**2)
    dz = eager_DeactivateTrig(u, xx)
    # the sech factor became InertSec of I*(c+d*x)
    import sympy as _sp
    inert = [t for t in dz.atoms(_sp.Function) if t.func is InertSec]
    assert inert, dz
    assert _sp.expand(inert[0].args[0] - _sp.I*(c + d*xx)) == 0


def test_inert_trig_heads_are_distinct_from_active():
    """Inert markers must NOT share a MatchPy head with the active SymPy functions.
    Rubi's trig rules are inert and match only after DeactivateTrig; an inert leaf
    has to stay a distinct head so it can never masquerade as a solved active
    result. (Supersedes the old head-registration approach.)"""
    from rubi_rules.utils.utility_functions import InertSec
    from sympy_matching.conversion import to_matchpy_expression
    import sympy as _sp
    xx = Symbol('x')
    assert to_matchpy_expression(InertSec(xx)).head != to_matchpy_expression(_sp.sec(xx)).head


def test_deactivation_dispatch_solves_cofunction_integrals():
    """Rubi's DeactivateTrig dispatch (the general FunctionOfTrigOfLinearQ fallback
    rule) routes active circular AND hyperbolic co-functions through the inert
    circular rules. Every case below returned CannotIntegrate/timed out before the
    faithful FixInertTrigFunction + UnifyInertTrigFunction port."""
    from rubi_rules.base_objects import rubi_integrate, Int as _Int
    xx, a, b, c, d = symbols('x a b c d')
    # sec^2 integrates to the clean tan(x)
    assert simplify(rubi_integrate(sec(xx)**2, xx).diff(xx) - sec(xx)**2) == 0
    # cos^2 (circular), cosh^2 (hyperbolic) and sech^2/(a+b sech^2) all now solve
    for u in (cos(xx)**2, cosh(xx)**2, sech(c + d*xx)**2/(a + b*sech(c + d*xx)**2)):
        r = rubi_integrate(u, xx)
        assert 'CannotIntegrate' not in str(r) and not r.has(_Int), u
