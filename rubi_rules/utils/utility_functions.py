"""
Utility functions for Rubi integration.

See: http://www.apmaths.uwo.ca/~arich/IntegrationRules/PortableDocumentFiles/Integration%20utility%20functions.pdf
"""
from functools import wraps, lru_cache


def _pure_expr_cache(maxsize):
    """Memoise a PURE predicate of hashable SymPy arguments.

    The wrapped predicates (PosQ, LinearQ, ...) are deterministic functions of their
    arguments -- their result depends only on the expression, never on mutable state
    -- so caching can never change a verdict; it only skips recomputation. During the
    backtracking DFS the SAME predicate is evaluated on identical sub-expressions
    thousands of times (measured repeat rates 96-99%), and each PosQ/LinearQ does real
    work (a Simplify / polynomial build). The cache is BOUNDED (``maxsize``) so a long
    corpus run cannot grow it without limit, and it falls back to a direct call on the
    rare unhashable argument.
    """
    def deco(fn):
        cached = lru_cache(maxsize=maxsize)(fn)
        @wraps(fn)
        def wrapper(*args):
            try:
                return cached(*args)
            except TypeError:  # unhashable arg -> compute without caching
                return fn(*args)
        wrapper.cache_clear = cached.cache_clear
        return wrapper
    return deco

from sympy.concrete.summations import Sum
from sympy.core.add import Add
from sympy.core.sorting import default_sort_key
from sympy.core.basic import Basic
from sympy.core.containers import Dict, Tuple
from sympy.core.evalf import N
from sympy.core.expr import UnevaluatedExpr
from sympy.core.exprtools import factor_terms
from sympy.core.function import (Function, WildFunction, expand, expand_trig, Derivative)
from sympy.core.mul import Mul, _keep_coeff
from sympy.core.numbers import (E, Float, I, Integer, Rational, oo, pi, zoo, Exp1)
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import (Dummy, Symbol, Wild, symbols)
from sympy.core.sympify import sympify, SympifyError
from sympy.core.traversal import postorder_traversal
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import im, re, Abs, sign
from sympy.functions.elementary.exponential import exp as sym_exp, log as sym_log, LambertW, exp, log
from sympy.functions.elementary.hyperbolic import acosh, asinh, atanh, acoth, acsch, asech, cosh, sinh, tanh, coth, sech, csch
from sympy.functions.elementary.integers import floor, frac, ceiling
from sympy.functions.elementary.miscellaneous import (Max, Min, sqrt)
from sympy.functions.elementary.trigonometric import atan, acsc, asin, acot, acos, asec, atan2, sin, cos, tan, cot, csc, sec
from sympy.functions.special.elliptic_integrals import elliptic_f, elliptic_e, elliptic_pi
from sympy.functions.special.error_functions import erf, fresnelc, fresnels, erfc, erfi, Ei, expint, li, Si, Ci, Shi, Chi
from sympy.functions.special.gamma_functions import (digamma, gamma, loggamma, polygamma, uppergamma)
from sympy.functions.special.hyper import (appellf1, hyper, TupleArg)
from sympy.functions.special.zeta_functions import polylog, zeta
from sympy.integrals.integrals import Integral
from sympy.logic.boolalg import And, Or, BooleanAtom
from sympy.ntheory.factor_ import (factorint, factorrat)
from sympy.polys.partfrac import apart
from sympy.polys.polyerrors import (PolynomialDivisionFailed, PolynomialError, UnificationFailed, NotInvertible, GeneratorsNeeded)
from sympy.polys.polytools import (discriminant, factor, gcd, lcm, poly, sqf, sqf_list, Poly, degree, quo, rem, total_degree, invert)
from sympy.sets.sets import FiniteSet
from sympy.simplify.powsimp import powdenest
from sympy.simplify.radsimp import collect
from sympy.simplify.simplify import fraction, simplify, cancel, powsimp, nsimplify
from sympy.polys.rationaltools import together as sym_together

from sympy.utilities.iterables import flatten
from sympy.core.random import randint

from sympy_matching import WildSymbol, IDENTITY_ELEMENT
from sympy_matching.conversion import matchpy_to_sympy

# Self-contained Wolfram-standard eager helpers now live in sympy_wolfram (the
# correct layer direction: rubi_rules -> sympy_wolfram). Imported here so the many
# in-module callers keep resolving these names; the local defs were removed.
from sympy_wolfram.mathematica_functions import (  # standard Wolfram nodes (moved out of this module)
    BesselJ, ExpIntegralE, Factorial, PolyGamma, Root, Zeta, ProductLog,
)
from sympy_wolfram.functions_eager import (
    eager_ExpIntegralEi as ExpIntegralEi, eager_LogIntegral as LogIntegral,
)
from sympy_wolfram.functions_eager import (
    eager_LeafCount, eager_Length, eager_Complex, eager_Not, eager_Exponent,
    eager_Simplify, eager_First, eager_Rest, eager_Numerator, eager_Denominator, eager_Part, Util_Part, eager_Apart,
    eager_FreeQ, _ensure_sympy,
    # Standard Wolfram predicates (bodies depend only on SymPy + Simplify/_ensure_sympy);
    # relocated here from utility_functions.
    eager_IntegerQ, eager_MemberQ, eager_PositiveQ, eager_NumberQ, eager_AtomQ, eager_PolynomialQ,
    # PolynomialQuotient/Remainder handle the rational-p Laurent case (single impl there).
    eager_PolynomialQuotient, eager_PolynomialRemainder,
)


from matchpy import Arity, Operation, CustomConstraint, Pattern, ReplacementRule, ManyToOneReplacer, from_matchpy_expression, \
    to_matchpy_expression
from matchpy import is_match, replace_all
from matchpy import match as matchpy_match
from matchpy.expressions.expressions import SymbolWrapper as _MatchPySymbolWrapper


# _ensure_sympy and FreeQ moved to sympy_wolfram.functions_eager (imported above):
# FreeQ is a standard Wolfram predicate and _ensure_sympy is the generic matchpy->sympy
# coercion it needs -- neither is Rubi-specific.


def _patched_custom_constraint_call(func):

    @wraps(func)
    def new_func(**kwargs):
        kwargs = {k: _ensure_sympy(v) for k, v in kwargs.items()}
        ret = func(**kwargs)
        return ret

    return CustomConstraint(new_func)


def _ReplacementRuleWrapped(pattern, replacement):
    """Wrap replacement function to auto-convert matchpy objects to SymPy."""
    def wrapped(**kwargs):
        converted = {k: _ensure_sympy(v) for k, v in kwargs.items()}
        result = replacement(**converted)
        # Ensure result is a matchpy Expression for replace_all
        if not isinstance(result, (Operation, _MatchPySymbolWrapper)):
            result = to_matchpy_expression(result)
        return result
    wrapped.__name__ = getattr(replacement, '__name__', 'replacement')
    wrapped.__qualname__ = getattr(replacement, '__qualname__', 'replacement')
    return ReplacementRule(pattern, wrapped)


UtilityOp = Operation.new(
    'UtilityOp',
    Arity.variadic,
    associative=True, commutative=False, one_identity=False)


def UtilityOperator(*args):
    return UtilityOp(*(to_matchpy_expression(arg) for arg in args))


A_, B_, C_, F_, G_, a_, b_, c_, d_, e_, f_, g_, h_, i_, j_, k_, l_, m_, \
n_, p_, q_, r_, t_, u_, v_, s_, w_, x_, z_ = [WildSymbol(i) for i in 'ABCFGabcdefghijklmnpqrtuvswxz']
a, b, c, d, e = symbols('a b c d e')

_a_ = WildSymbol("a", optional_value=IDENTITY_ELEMENT)


def everything_else_means_false(f):
    @wraps(f)
    def newf(*args, **kwargs):
        ret = f(*args, **kwargs)
        if ret is None:
            return False
        if ret != True:
            return False
        return ret

    return newf


def exception_means_false(f):
    @wraps(f)
    def newf(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return False
    return newf


# NOTE (measured 2026-07-21, do not re-attempt naively): during matching the SAME
# expression is simplified repeatedly as the DFS backtracks -- on `x/(a+b*x)^2`,
# 12679 Simplify calls over only 129 distinct arguments (99% repeats), with
# sympy.simplify accounting for ~62% of the runtime. Memoising this looks like an
# obvious win and IS NOT: a cold-process A/B (one process per arm, so SymPy's global
# caches cannot warm one arm for the other) showed the memo turning
# `x^3/(a+b*x)^2` and `x^4/(a+b*x)^2` from 14.5s/3.0s solves into >90s TIMEOUTS.
# The guard cost dominates -- every call pays an `expr.has(MathematicaExpr)` tree walk
# plus hashing a large expression, which exceeds what the hit saves. A worthwhile fix
# has to avoid re-deriving the same simplification in the first place (a cheaper
# equivalence test before falling back to full simplify, or hoisting the call out of
# the backtracking loop), not cache after the fact.
# Simplify moved to sympy_wolfram.functions_eager (imported above) — it is a standard
# Wolfram function whose body depends only on SymPy (+ MathematicaExpr for the deferred-
# node doit), so it lives in the generic Wolfram layer.

def eager_Set(expr, value):
    return {expr: value}

def eager_With(subs, expr):
    if isinstance(subs, dict):
        k = list(subs.keys())[0]
        expr = expr.xreplace({k: subs[k]})
    else:
        for i in subs:
            k = list(i.keys())[0]
            expr = expr.xreplace({k: i[k]})
    return expr

def eager_Module(subs, expr):
    return eager_With(subs, expr)

def eager_Scan(f, expr):
    # evaluates f applied to each element of expr in turn.
    for i in expr:
        yield f(i)

def MapAnd(f, l, x=None):
    # MapAnd[f,l] applies f to the elements of list l until False is returned; else returns True
    if x:
        for i in l:
            if f(i, x) == False:
                return False
        return True
    else:
        for i in l:
            if f(i) == False:
                return False
        return True

def eager_FalseQ(u):
    if isinstance(u, (Dict, dict)):
        return eager_FalseQ(*list(u.values()))

    return u == False

_ZEROQ_PROBE_POINTS = (
    {'i': Rational(7, 3), 'j': Rational(11, 5), 'k': Rational(13, 4), 'l': Rational(17, 6)},
    {'i': Rational(23, 9), 'j': Rational(5, 2), 'k': Rational(29, 7), 'l': Rational(9, 4)},
)


def _provably_nonzero(expr):
    """Sound fast pre-test for ZeroQ: True only if ``expr`` is provably NOT
    identically zero, established by evaluating it at cheap rational probe points.

    A nonzero numeric value at any point proves the symbolic expression is not
    identically zero, so returning True here can never change a ZeroQ verdict --
    every uncertain case (numerically zero, non-numeric, deferred node, undefined at
    the point) returns False and the caller falls back to the exact ``Simplify``.
    This avoids the (expensive) full ``sympy.simplify`` on the overwhelmingly common
    "generically nonzero discriminant" constraints (e.g. ``b*c - a*d``).
    """
    from sympy_wolfram.objects import MathematicaExpr
    if not isinstance(expr, Basic) or expr.has(MathematicaExpr):
        return False
    syms = sorted(expr.free_symbols, key=lambda s: s.sort_key())
    if not syms:
        return False  # a pure constant: let the exact `== 0` decide it
    cyc = list(_ZEROQ_PROBE_POINTS[0].values())
    for point in _ZEROQ_PROBE_POINTS:
        pv = list(point.values())
        subs = {s: pv[idx] if idx < len(pv) else cyc[idx % len(cyc)]
                for idx, s in enumerate(syms)}
        try:
            val = expr.xreplace(subs).evalf(15)
        except Exception:  # noqa: BLE001 -- any eval failure -> fall back to exact
            continue
        if val is None or not getattr(val, 'is_number', False):
            continue
        if val.has(zoo, oo, S.NaN) or val.is_finite is False:
            continue
        try:
            if abs(complex(val)) > 1e-9:
                return True
        except (TypeError, ValueError):
            continue
    return False


def ZeroQ(*expr):
    if len(expr) == 1:
        if isinstance(expr[0], list):
            return list(ZeroQ(i) for i in expr[0])
        else:
            u = _ensure_sympy(expr[0])
            if isinstance(u, BooleanAtom):
                return False        # a Boolean is not the number zero (see _boolean_operand)
            if _provably_nonzero(u):
                return False
            return eager_Simplify(u) == 0
    else:
        return all(ZeroQ(i) for i in expr)

def eager_NegativeQ(u):
    u = eager_Simplify(_ensure_sympy(u))
    if u in (zoo, oo):
        return False
    if u.is_comparable:
        res = u < 0
        if not res.is_Relational:
            return res
    return False

def NonzeroQ(expr):
    # Not[ZeroQ] -- reuses the sound numeric pre-test so a generically-nonzero
    # constraint avoids the expensive full Simplify (see _provably_nonzero).
    return not ZeroQ(expr)


def eager_List(*var):
    return list(var)

def PositiveIntegerQ(*args):
    return all(var.is_Integer and eager_PositiveQ(var) for var in args)

def NegativeIntegerQ(*args):
    return all(var.is_Integer and eager_NegativeQ(var) for var in args)

# PositiveQ, IntegerQ and MemberQ moved to sympy_wolfram.functions_eager
# (standard Wolfram predicates); imported at the top of this module.

def eager_IntegersQ(*var):
    return all(eager_IntegerQ(i) for i in var)

def _ComplexNumberQ(var):
    i = S(im(var))
    if isinstance(i, (Integer, Float)):
        return i != 0
    else:
        return False

def eager_ComplexNumberQ(*var):
    """
    ComplexNumberQ(m, n,...) returns True if m, n, ... are all explicit complex numbers, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import ComplexNumberQ
    >>> from sympy import I
    >>> ComplexNumberQ(1 + I*2, I)
    True
    >>> ComplexNumberQ(2, I)
    False

    """
    return all(_ComplexNumberQ(i) for i in var)

def PureComplexNumberQ(*var):
    return all((_ComplexNumberQ(i) and re(i)==0) for i in var)

def RealNumericQ(u):
    return u.is_real

def PositiveOrZeroQ(u):
    return u.is_real and u >= 0

def eager_FractionOrNegativeQ(u):
    return eager_FractionQ(u) or eager_NegativeQ(u)

def eager_NegQ(var):
    return eager_Not(eager_PosQ(var)) and NonzeroQ(var)


def Equal(a, b):
    return a == b

def Unequal(a, b):
    return a != b

def eager_IntPart(u):
    # IntPart[u] returns the sum of the integer terms of u.
    if eager_ProductQ(u):
        if eager_IntegerQ(eager_First(u)):
            return eager_First(u)*eager_IntPart(eager_Rest(u))
    elif eager_IntegerQ(u):
        return u
    elif eager_FractionQ(u):
        return IntegerPart(u)
    elif eager_SumQ(u):
        res = 0
        for i in u.args:
            res += eager_IntPart(i)
        return res
    return 0

def eager_FracPart(u):
    # FracPart[u] returns the sum of the non-integer terms of u.
    if eager_ProductQ(u):
        if eager_IntegerQ(eager_First(u)):
            return eager_First(u)*eager_FracPart(eager_Rest(u))

    if eager_IntegerQ(u):
        return 0
    elif eager_FractionQ(u):
        return FractionalPart(u)
    elif eager_SumQ(u):
        res = 0
        for i in u.args:
            res += eager_FracPart(i)
        return res
    else:
        return u

def eager_RationalQ(*nodes):
    return all(_ensure_sympy(var).is_Rational for var in nodes)

def eager_ProductQ(expr):
    return S(_ensure_sympy(expr)).is_Mul

def eager_SumQ(expr):
    expr = _ensure_sympy(expr)
    return expr.is_Add

def eager_NonsumQ(expr):
    return not eager_SumQ(expr)

def eager_Subst(a, x, y):
    if None in [a, x, y]:
        return None
    if a.has(Function('Integrate')):
        # substituting in `Function(Integrate)` won't take care of properties of Integral
        a = a.replace(Function('Integrate'), Integral)
    return a.subs(x, y)
    # return a.xreplace({x: y})

# First and Rest moved to sympy_wolfram.functions_eager (imported above). Their bodies
# used SumQ/ProductQ/Sort, all generic SymPy operations (is_Add/is_Mul/sort_key), so the
# functions belong to the generic Wolfram layer.

def eager_SqrtNumberQ(expr):
    # SqrtNumberQ[u] returns True if u^2 is a rational number; else it returns False.
    if eager_PowerQ(expr):
        m = expr.base
        n = expr.exp
        return (eager_IntegerQ(n) and eager_SqrtNumberQ(m)) or (eager_IntegerQ(n-S(1)/2) and eager_RationalQ(m))
    elif expr.is_Mul:
        return all(eager_SqrtNumberQ(i) for i in expr.args)
    else:
        return eager_RationalQ(expr) or expr == I

def SqrtNumberSumQ(u):
    u = _ensure_sympy(u)
    return eager_SumQ(u) and eager_SqrtNumberQ(eager_First(u)) and eager_SqrtNumberQ(eager_Rest(u)) or eager_ProductQ(u) and eager_SqrtNumberQ(eager_First(u)) and SqrtNumberSumQ(eager_Rest(u))

def eager_LinearQ(expr, x):
    """
    LinearQ(expr, x) returns True iff u is a polynomial of degree 1.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import LinearQ
    >>> from sympy.abc import x, y, a
    >>> LinearQ(a, x)
    False
    >>> LinearQ(3*x + y**2, x)
    True
    >>> LinearQ(3*x + y**2, y)
    False

    """
    if isinstance(expr, (tuple, list, Tuple)):
        return all(eager_LinearQ(i, x) for i in expr)
    return _LinearQ_scalar(expr, x)


@_pure_expr_cache(maxsize=20000)
def _LinearQ_scalar(expr, x):
    if expr.is_polynomial(x):
        if degree(Poly(expr, x), gen=x) == 1:
            return True
    return False

def Sqrt(a):
    return sqrt(a)

def ArcCosh(a):
    return acosh(a)

class Util_Coefficient(Function):
    def doit(self):
        if len(self.args) == 2:
            n = 1
        else:
            n = eager_Simplify(self.args[2])

        if eager_NumericQ(n):
            expr = expand(self.args[0])
            if isinstance(n, (int, Integer)):
                return expr.coeff(self.args[1], n)
            else:
                return expr.coeff(self.args[1]**n)
        else:
            return self

def eager_Coefficient(expr, var, n=1):
    """
    Coefficient(expr, var) gives the coefficient of form in the polynomial expr.
    Coefficient(expr, var, n) gives the coefficient of var**n in expr.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import Coefficient
    >>> from sympy.abc import x, a, b, c
    >>> Coefficient(7 + 2*x + 4*x**3, x, 1)
    2
    >>> Coefficient(a + b*x + c*x**3, x, 0)
    a
    >>> Coefficient(a + b*x + c*x**3, x, 4)
    0
    >>> Coefficient(b*x + c*x**3, x, 3)
    c

    """
    if eager_NumericQ(n):
        if expr == 0 or n in (zoo, oo):
            return 0
        expr = expand(expr)
        if isinstance(n, (int, Integer)):
            return expr.coeff(var, n)
        else:
            return expr.coeff(var**n)

    return Util_Coefficient(expr, var, n)

# Denominator moved to sympy_wolfram.functions_eager (imported above), paired with the
# recursive Numerator; both bodies are pure SymPy (Simplify/together/fraction).

def eager_Hypergeometric2F1(a, b, c, z):
    return hyper([a, b], [c], z)

def FractionalPart(a):
    # FractionalPart[a] = a - IntegerPart[a]; carries the sign of a (Mathematica),
    # e.g. FractionalPart[-7/2] = -1/2. sympy's frac() is floor-based (-> 1/2).
    a = sympify(a)
    return a - IntegerPart(a)

def IntegerPart(a):
    # Mathematica IntegerPart truncates toward zero (NOT floor): IntegerPart[-7/2]
    # = -3 and IntegerPart[-3.6] = -3. floor would give -4.
    a = sympify(a)
    if a.is_number and a.is_real:
        return floor(a) if a.is_nonnegative else ceiling(a)
    return floor(a)

AppellF1 = appellf1

def eager_EllipticPi(*args):
    return elliptic_pi(*args)

def ArcTan(a, b = None):
    if b is None:
        return atan(a)
    else:
        return atan2(a, b)

def ArcCot(a):
    return acot(a)

def ArcCoth(a):
    return acoth(a)

def ArcTanh(a):
    return atanh(a)

def ArcSin(a):
    return asin(a)

def ArcSinh(a):
    return asinh(a)

def ArcCos(a):
    return acos(a)

def Sinh(u):
    return sinh(u)

def Tanh(u):
    return tanh(u)

def Cosh(u):
    return cosh(u)

def Sech(u):
    return sech(u)

def Csch(u):
    return csch(u)

def Coth(u):
    return coth(u)

def LessEqual(*args):
    for i in range(0, len(args) - 1):
        try:
            if (args[i] > args[i + 1]) != False:
                return False
        except (IndexError, NotImplementedError, TypeError):
            # TypeError: sympy raises on an ordering comparison of a non-real
            # (e.g. -2*I). Mathematica leaves Less/Greater unevaluated there, so
            # the predicate is not provably true -> False (as for the other cases).
            return False
    return True

def Less(*args):
    for i in range(0, len(args) - 1):
        try:
            if (args[i] >= args[i + 1]) != False:
                return False
        except (IndexError, NotImplementedError, TypeError):
            # TypeError: sympy raises on an ordering comparison of a non-real
            # (e.g. -2*I). Mathematica leaves Less/Greater unevaluated there, so
            # the predicate is not provably true -> False (as for the other cases).
            return False
    return True

def Greater(*args):
    for i in range(0, len(args) - 1):
        try:
            if (args[i] <= args[i + 1]) != False:
                return False
        except (IndexError, NotImplementedError, TypeError):
            # TypeError: sympy raises on an ordering comparison of a non-real
            # (e.g. -2*I). Mathematica leaves Less/Greater unevaluated there, so
            # the predicate is not provably true -> False (as for the other cases).
            return False
    return True

def GreaterEqual(*args):
    for i in range(0, len(args) - 1):
        try:
            if (args[i] < args[i + 1]) != False:
                return False
        except (IndexError, NotImplementedError, TypeError):
            # TypeError: sympy raises on an ordering comparison of a non-real
            # (e.g. -2*I). Mathematica leaves Less/Greater unevaluated there, so
            # the predicate is not provably true -> False (as for the other cases).
            return False
    return True

def eager_FractionQ(*args):
    """
    FractionQ(m, n,...) returns True if m, n, ... are all explicit fractions, else it returns False.

    Examples
    ========

    >>> from sympy import S
    >>> from rubi_rules.utils.utility_functions import FractionQ
    >>> FractionQ(S('3'))
    False
    >>> FractionQ(S('3')/S('2'))
    True

    """
    args = [_ensure_sympy(i) for i in args]
    return all(i.is_Rational for i in args) and all(eager_Denominator(i) != S(1) for i in args)

def IntLinearcQ(a, b, c, d, m, n, x):
    # returns True iff (a+b*x)^m*(c+d*x)^n is integrable wrt x in terms of non-hypergeometric functions.
    return eager_IntegerQ(m) or eager_IntegerQ(n) or eager_IntegersQ(S(3)*m, S(3)*n) or eager_IntegersQ(S(4)*m, S(4)*n) or eager_IntegersQ(S(2)*m, S(6)*n) or eager_IntegersQ(S(6)*m, S(2)*n) or eager_IntegerQ(m + n)

Defer = UnevaluatedExpr

def Expand(expr):
    return expr.expand()

def eager_IndependentQ(u, x):
    """
    If u is free from x IndependentQ(u, x) returns True else False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import IndependentQ
    >>> from sympy.abc import x, a, b
    >>> IndependentQ(a + b*x, x)
    False
    >>> IndependentQ(a + b, x)
    True

    """
    return eager_FreeQ(u, x)

def eager_PowerQ(expr):
    return expr.is_Pow or ExpQ(expr)

def eager_IntegerPowerQ(u):
    if isinstance(u, sym_exp): #special case for exp
        return eager_IntegerQ(u.args[0])
    return eager_PowerQ(u) and eager_IntegerQ(u.args[1])

def eager_FractionalPowerQ(u):
    if isinstance(u, sym_exp):
        return eager_FractionQ(u.args[0])
    return eager_PowerQ(u) and eager_FractionQ(u.args[1])

# AtomQ moved to sympy_wolfram.functions_eager (standard Wolfram predicate,
# no Rubi coupling); imported at the top of this module.

def ExpQ(u):
    return eager_Head(u) in (sym_exp, exp)

def eager_LogQ(u):
    return u.func in (sym_log, Log)

def eager_Head(u):
    return u.func

def eager_TrigQ(u):
    if eager_AtomQ(u):
        x = u
    else:
        x = eager_Head(u)
    return eager_MemberQ([sin, cos, tan, cot, sec, csc], x)

def SinQ(u):
    return eager_Head(u) == sin

def CosQ(u):
    return eager_Head(u) == cos

def TanQ(u):
    return eager_Head(u) == tan

def CotQ(u):
    return eager_Head(u) == cot

def SecQ(u):
    return eager_Head(u) == sec

def CscQ(u):
    return eager_Head(u) == csc

def Sin(u):
    return sin(u)

def Cos(u):
    return cos(u)

def Tan(u):
    return tan(u)

def Cot(u):
    return cot(u)

def Sec(u):
    return sec(u)

def Csc(u):
    return csc(u)

def eager_HyperbolicQ(u):
    if eager_AtomQ(u):
        x = u
    else:
        x = eager_Head(u)
    return eager_MemberQ([sinh, cosh, tanh, coth, sech, csch], x)

def SinhQ(u):
    return eager_Head(u) == sinh

def CoshQ(u):
    return eager_Head(u) == cosh

def TanhQ(u):
    return eager_Head(u) == tanh

def CothQ(u):
    return eager_Head(u) == coth

def SechQ(u):
    return eager_Head(u) == sech

def CschQ(u):
    return eager_Head(u) == csch

def eager_InverseTrigQ(u):
    if eager_AtomQ(u):
        x = u
    else:
        x = eager_Head(u)
    return eager_MemberQ([asin, acos, atan, acot, asec, acsc], x)

def SinhCoshQ(f):
    return eager_MemberQ([sinh, cosh, sech, csch], eager_Head(f))

# Numerator moved to sympy_wolfram.functions_eager (imported above); see Denominator.

# NumberQ moved to sympy_wolfram.functions_eager (standard Wolfram predicate,
# no Rubi coupling); imported at the top of this module.

def eager_NumericQ(u):
    """Mathematica ``NumericQ[u]`` — True iff *u* is a numeric quantity.

    Decides the symbolic cases WITHOUT calling ``N()``. sympy's ``Derivative.evalf``
    is literally ``self.doit().evalf(prec, **options)``, and ``doit()`` cannot make
    progress on a derivative of an UNDEFINED function -- our ``Inert*`` trig markers
    are ``AppliedUndef``, so ``Derivative(InertSin(x), x).doit()`` returns the SAME
    object and ``evalf`` recurses until the stack dies.

    That path was reached during ordinary constraint checking
    (``NegQ -> PosQ -> PosAux -> NumericQ``) and killed integrals such as
    ``sec(e+f x)^3/sqrt(d tan(e+f x))``, ``(d tan(a+b x))^(5/2) csc(a+b x)^3`` and
    ``1/(sqrt(e sin(c+d x)) (a+b cos(c+d x)))`` with ``RecursionError``.

    The short-circuits are also what Mathematica answers: ``NumericQ`` is False for
    anything containing a symbol, and for a list.
    """
    if isinstance(u, (tuple, list, Tuple)):
        return False
    try:
        u = sympify(u)
    except (SympifyError, TypeError, AttributeError):
        return False
    if getattr(u, 'free_symbols', None):
        return False
    # An unevaluatable Derivative is not a numeric quantity -- and is exactly what
    # makes evalf loop, so it must be rejected before N() is reached.
    if u.has(Derivative):
        return False
    return N(u).is_number

def ListQ(u):
    return isinstance(u, (tuple, list, Tuple))

def Im(u):
    u = S(u)
    return im(u.doit())

def Re(u):
    u = S(u)
    return re(u.doit())

def eager_InverseHyperbolicQ(u):
    if not u.is_Atom:
        u = eager_Head(u)
    # Rubi $InverseHyperbolicFunctions = {ArcSinh, ArcCosh, ArcTanh, ArcCoth, ArcSech, ArcCsch};
    # asech was missing here (acsch was listed twice), so asech(...) integrands were
    # wrongly classified as containing no inverse function.
    return u in [acosh, asinh, atanh, acoth, asech, acsch]

def eager_InverseFunctionQ(u):
    # returns True if u is a call on an inverse function; else returns False.
    return eager_LogQ(u) or eager_InverseTrigQ(u) and eager_Length(u) <= 1 or eager_InverseHyperbolicQ(u) or u.func == polylog

def eager_TrigHyperbolicFreeQ(u, x):
    # If u is free of trig, hyperbolic and calculus functions involving x, TrigHyperbolicFreeQ[u,x] returns true; else it returns False.
    if eager_AtomQ(u):
        return True
    else:
        if eager_TrigQ(u) | eager_HyperbolicQ(u) | CalculusQ(u):
            return eager_FreeQ(u, x)
        else:
            for i in u.args:
                if not eager_TrigHyperbolicFreeQ(i, x):
                    return False
            return True

def eager_InverseFunctionFreeQ(u, x):
    # If u is free of inverse, calculus and hypergeometric functions involving x, InverseFunctionFreeQ[u,x] returns true; else it returns False.
    if eager_AtomQ(u):
        return True
    else:
        if eager_InverseFunctionQ(u) or CalculusQ(u) or u.func in (hyper, appellf1):
            return eager_FreeQ(u, x)
        else:
            # Rubi recurses into every operand (Scan[... InverseFunctionFreeQ[#,x] ...]).
            # This used to call ElementaryFunctionQ instead, which happily accepts
            # ArcTanh etc. -- so e.g. InverseFunctionFreeQ[(a+b ArcTanh[c x])^2, x]
            # was True and the 3.5 Log[u] IntHide rules misfired.
            for i in u.args:
                if not eager_InverseFunctionFreeQ(i, x):
                    return False
            return True

def RealQ(u):
    if ListQ(u):
        return MapAnd(RealQ, u)
    elif eager_NumericQ(u):
        return ZeroQ(Im(N(u)))
    elif eager_PowerQ(u):
        u = u.base
        v = u.exp
        return RealQ(u) & RealQ(v) & (eager_IntegerQ(v) | PositiveOrZeroQ(u))
    elif u.is_Mul:
        return all(RealQ(i) for i in u.args)
    elif u.is_Add:
        return all(RealQ(i) for i in u.args)
    elif u.is_Function:
        f = u.func
        u = u.args[0]
        if f in [sin, cos, tan, cot, sec, csc, atan, acot, erf]:
            return RealQ(u)
        else:
            if f in [asin, acos]:
                return LessEqual(-1, u, 1)
            else:
                if f == sym_log:
                    return PositiveOrZeroQ(u)
                else:
                    return False
    else:
        return False

def _boolean_operand(u, v):
    """True if either side is a Boolean atom, so arithmetic on it is meaningless.

    Rubi's guards are evaluated against EVERY integrand, and several read a part of a
    helper that returned False -- e.g. `EqQ[FunctionOfSquareRootOfQuadratic[u,x][[3]], 2]`.
    Mathematica keeps `False[[3]]` symbolic, so the subtraction just fails to be zero and
    the guard is False. SymPy instead raises `BooleanAtom not allowed in this context`
    from the subtraction, which aborted the whole match.
    """
    return isinstance(u, BooleanAtom) or isinstance(v, BooleanAtom)


def eager_EqQ(u, v):
    # A function-head wildcard F_[...] binds its head to a HeadRef carrying the SymPy
    # class; a head-identity test EqQ[F, Sin] is written against a named head
    # (Symbol('sin')/Symbol('Sin')/a class). Compare by the underlying class so the
    # HeadRef and the Mathematica/SymPy-spelled name reconcile instead of subtracting
    # two unequal symbols (which would always be non-zero -> the rule never fires).
    if _boolean_operand(u, v):
        return u is v or u == v
    from sympy_matching.wild import HeadRef
    if isinstance(u, HeadRef) or isinstance(v, HeadRef):
        from sympy_wolfram.functions_eager import head_to_class
        uc, vc = head_to_class(u), head_to_class(v)
        if uc is not None and vc is not None:
            return uc == vc
    return ZeroQ(u - v)

def eager_FractionalPowerFreeQ(u):
    if eager_AtomQ(u):
        return True
    elif eager_FractionalPowerQ(u):
        return False

def eager_ComplexFreeQ(u):
    if eager_AtomQ(u) and eager_Not(eager_ComplexNumberQ(u)):
        return True
    else:
         return False

# PolynomialQ moved to sympy_wolfram.functions_eager (standard Wolfram predicate,
# no Rubi coupling); imported at the top of this module.

def FactorSquareFree(u):
    return sqf(u)

def eager_PowerOfLinearQ(expr, x):
    u = Wild('u')
    w = Wild('w')
    m = Wild('m')
    n = Wild('n')
    Match = expr.match(u**m)
    # `.match` can succeed while binding only SOME wildcards: a constant such as 1
    # matches u**m as m=0 with u unbound, and indexing Match[u] then raises KeyError
    # mid-integration. Nothing that fails to bind the base is a power of a linear.
    if not Match or u not in Match or m not in Match:
        return False
    if eager_PolynomialQ(Match[u], x) and eager_FreeQ(Match[m], x):
        if eager_IntegerQ(Match[m]):
            e = FactorSquareFree(Match[u]).match(w**n)
            if eager_FreeQ(e[n], x) and eager_LinearQ(e[w], x):
                return True
            else:
                return False
        else:
            return eager_LinearQ(Match[u], x)
    else:
        return False

# NOTE: Exponent is imported from sympy_wolfram.functions_eager (Mathematica-faithful:
# deg(numerator) - deg(denominator), correct for non-polynomials). The former local
# definition wrongly returned 0 for any non-polynomial (e.g. Exponent(sqrt(x)+x, x)
# gave 0 instead of 1); see the Expon fix. ``Expand``/``PolynomialQ`` are no longer
# needed by it.

def ExponentList(expr, x):
    expr = Expand(S(expr))
    if S(expr).is_number or (not expr.has(x)):
        return [Integer(0)]
    if expr.is_Add:
        expr = collect(expr, x)
        lst = []
        k = 1
        for t in expr.args:
            if t.has(x):
                if isinstance(x, Rational):
                    lst += [degree(Poly(t, x), x)]
                else:
                    lst += [degree(t, gen = x)]
            else:
                if k == 1:
                    lst += [0]
                    k += 1
        lst.sort()
        return lst
    else:
        if isinstance(x, Rational):
            return [degree(Poly(expr, x), x)]
        else:
            return [degree(expr, gen = x)]


@everything_else_means_false
def eager_QuadraticQ(u, x):
    # QuadraticQ(u, x) returns True iff u is a polynomial of degree 2 and not a monomial of the form a x^2
    if ListQ(u):
        for expr in u:
            if eager_Not(eager_QuadraticQ(expr, x)):
                return False
        return True
    else:
        return eager_PolyQ(u, x, 2) and eager_Not(eager_Coefficient(u, x, 0) == 0 and eager_Coefficient(u, x, 1) == 0)


def eager_LinearPairQ(u, v, x):
    # LinearPairQ(u, v, x) returns True iff u and v are linear not equal x but u/v is a constant wrt x
    return eager_LinearQ(u, x) and eager_LinearQ(v, x) and NonzeroQ(u-x) and ZeroQ(eager_Coefficient(u, x, 0)*eager_Coefficient(v, x, 1)-eager_Coefficient(u, x, 1)*eager_Coefficient(v, x, 0))

def BinomialParts(u, x):
    if eager_PolynomialQ(u, x):
        if eager_Exponent(u, x) > 0:
            lst = ExponentList(u, x)
            if len(lst)==1:
                return [0, eager_Coefficient(u, x, eager_Exponent(u, x)), eager_Exponent(u, x)]
            elif len(lst) == 2 and lst[0] == 0:
                return [eager_Coefficient(u, x, 0), eager_Coefficient(u, x, eager_Exponent(u, x)), eager_Exponent(u, x)]
            else:
                return False
        else:
            return False
    elif eager_PowerQ(u):
        if u.base == x and eager_FreeQ(u.exp, x):
            return [0, 1, u.exp]
        else:
            return False
    elif eager_ProductQ(u):
        if eager_FreeQ(eager_First(u), x):
            lst2 = BinomialParts(eager_Rest(u), x)
            if eager_AtomQ(lst2):
                return False
            else:
                return [eager_First(u)*lst2[0], eager_First(u)*lst2[1], lst2[2]]
        elif eager_FreeQ(eager_Rest(u), x):
            lst1 = BinomialParts(eager_First(u), x)
            if eager_AtomQ(lst1):
                return False
            else:
                return [eager_Rest(u)*lst1[0], eager_Rest(u)*lst1[1], lst1[2]]
        lst1 = BinomialParts(eager_First(u), x)
        if eager_AtomQ(lst1):
            return False
        lst2 = BinomialParts(eager_Rest(u), x)
        if eager_AtomQ(lst2):
            return False
        a = lst1[0]
        b = lst1[1]
        m = lst1[2]
        c = lst2[0]
        d = lst2[1]
        n = lst2[2]
        if ZeroQ(a):
            if ZeroQ(c):
                return [0, b*d, m + n]
            elif ZeroQ(m + n):
                return [b*d, b*c, m]
            else:
                return False
        if ZeroQ(c):
            if ZeroQ(m + n):
                return [b*d, a*d, n]
            else:
                return False
        if eager_EqQ(m, n) and ZeroQ(a*d + b*c):
            return [a*c, b*d, 2*m]
        else:
            return False
    elif eager_SumQ(u):
        if eager_FreeQ(eager_First(u),x):
            lst2 = BinomialParts(eager_Rest(u), x)
            if eager_AtomQ(lst2):
                return False
            else:
                return [eager_First(u) + lst2[0], lst2[1], lst2[2]]
        elif eager_FreeQ(eager_Rest(u), x):
            lst1 = BinomialParts(eager_First(u), x)
            if eager_AtomQ(lst1):
                return False
            else:
                return[eager_Rest(u) + lst1[0], lst1[1], lst1[2]]
        lst1 = BinomialParts(eager_First(u), x)
        if eager_AtomQ(lst1):
            return False
        lst2 = BinomialParts(eager_Rest(u),x)
        if eager_AtomQ(lst2):
            return False
        if eager_EqQ(lst1[2], lst2[2]):
            return [lst1[0] + lst2[0], lst1[1] + lst2[1], lst1[2]]
        else:
            return False
    else:
        return False

def TrinomialParts(u, x):
    # If u is equivalent to a trinomial of the form a + b*x^n + c*x^(2*n) where n!=0, b!=0 and c!=0, TrinomialParts[u,x] returns the list {a,b,c,n}; else it returns False.
    u = sympify(u)
    if eager_PolynomialQ(u, x):
        lst = CoefficientList(u, x)
        if len(lst)<3 or eager_EvenQ(sympify(len(lst))) or ZeroQ((len(lst)+1)/2):
            return False
        #Catch(
         #   Scan(Function(if ZeroQ(lst), Null, Throw(False), Drop(Drop(Drop(lst, [(len(lst)+1)/2]), 1), -1];
          #  [First(lst), lst[(len(lst)+1)/2], Last(lst), (len(lst)-1)/2]):
    if eager_PowerQ(u):
        if eager_EqQ(u.exp, 2):
            lst = BinomialParts(u.base, x)
            if not lst or ZeroQ(lst[0]):
                return False
            else:
                return [lst[0]**2, 2*lst[0]*lst[1], lst[1]**2, lst[2]]
        else:
            return False
    if eager_ProductQ(u):
        if eager_FreeQ(eager_First(u), x):
            lst2 = TrinomialParts(eager_Rest(u), x)
            if not lst2:
                return False
            else:
                return [eager_First(u)*lst2[0], eager_First(u)*lst2[1], eager_First(u)*lst2[2], lst2[3]]
        if eager_FreeQ(eager_Rest(u), x):
            lst1 = TrinomialParts(eager_First(u), x)
            if not lst1:
                return False
            else:
                return [eager_Rest(u)*lst1[0], eager_Rest(u)*lst1[1], eager_Rest(u)*lst1[2], lst1[3]]
        lst1 = BinomialParts(eager_First(u), x)
        if not lst1:
            return False
        lst2 = BinomialParts(eager_Rest(u), x)
        if not lst2:
            return False
        a = lst1[0]
        b = lst1[1]
        m = lst1[2]
        c = lst2[0]
        d = lst2[1]
        n = lst2[2]
        if eager_EqQ(m, n) and NonzeroQ(a*d+b*c):
            return [a*c, a*d + b*c, b*d, m]
        else:
            return False
    if eager_SumQ(u):
        if eager_FreeQ(eager_First(u), x):
            lst2 = TrinomialParts(eager_Rest(u), x)
            if not lst2:
                return False
            else:
                return [eager_First(u)+lst2[0], lst2[1], lst2[2], lst2[3]]
        if eager_FreeQ(eager_Rest(u), x):
            lst1 = TrinomialParts(eager_First(u), x)
            if not lst1:
                return False
            else:
                return [eager_Rest(u)+lst1[0], lst1[1], lst1[2], lst1[3]]
        lst1 = TrinomialParts(eager_First(u), x)
        if not lst1:
            lst3 = BinomialParts(eager_First(u), x)
            if not lst3:
                return False
            lst2 = TrinomialParts(eager_Rest(u), x)
            if not lst2:
                lst4 = BinomialParts(eager_Rest(u), x)
                if not lst4:
                    return False
                if eager_EqQ(lst3[2], 2*lst4[2]):
                    return [lst3[0]+lst4[0], lst4[1], lst3[1], lst4[2]]
                if eager_EqQ(lst4[2], 2*lst3[2]):
                    return [lst3[0]+lst4[0], lst3[1], lst4[1], lst3[2]]
                else:
                    return False
            if eager_EqQ(lst3[2], lst2[3]) and NonzeroQ(lst3[1]+lst2[1]):
                return [lst3[0]+lst2[0], lst3[1]+lst2[1], lst2[2], lst2[3]]
            if eager_EqQ(lst3[2], 2*lst2[3]) and NonzeroQ(lst3[1]+lst2[2]):
                return [lst3[0]+lst2[0], lst2[1], lst3[1]+lst2[2], lst2[3]]
            else:
                return False
        lst2 = TrinomialParts(eager_Rest(u), x)
        if eager_AtomQ(lst2):
            lst4 = BinomialParts(eager_Rest(u), x)
            if not lst4:
                return False
            if eager_EqQ(lst4[2], lst1[3]) and NonzeroQ(lst1[1]+lst4[0]):
                return [lst1[0]+lst4[0], lst1[1]+lst4[1], lst1[2], lst1[3]]
            if eager_EqQ(lst4[2], 2*lst1[3]) and NonzeroQ(lst1[2]+lst4[1]):
                return [lst1[0]+lst4[0], lst1[1], lst1[2]+lst4[1], lst1[3]]
            else:
                return False
        if eager_EqQ(lst1[3], lst2[3]) and NonzeroQ(lst1[1]+lst2[1]) and NonzeroQ(lst1[2]+lst2[2]):
            return [lst1[0]+lst2[0], lst1[1]+lst2[1], lst1[2]+lst2[2], lst1[3]]
        else:
            return False
    else:
        return False


@exception_means_false
def eager_PolyQ(u, x, n=None):
    # returns True iff u is a polynomial of degree n.
    if ListQ(u):
        return all(eager_PolyQ(i, x) for i in u)

    if n is None:
        if u == x:
            return False
        elif isinstance(x, Pow):
            n = x.exp
            x_base = x.base
            if eager_FreeQ(n, x_base):
                if PositiveIntegerQ(n):
                    return eager_PolyQ(u, x_base) and (eager_PolynomialQ(u, x) or eager_PolynomialQ(eager_Together(u), x))
                elif eager_AtomQ(n):
                    return eager_PolynomialQ(u, x) and eager_FreeQ(CoefficientList(u, x), x_base)
                else:
                    return False

        return eager_PolynomialQ(u, x) or eager_PolynomialQ(u, eager_Together(x))

    else:
        return eager_PolynomialQ(u, x) and eager_Coefficient(u, x, n) != 0 and eager_Exponent(u, x) == n


def eager_EvenQ(u):
    # gives True if expr is an even integer, and False otherwise.
    u = _ensure_sympy(u)
    return isinstance(u, (Integer, int)) and u%2 == 0

def eager_OddQ(u):
    # gives True if expr is an odd integer, and False otherwise.
    u = _ensure_sympy(u)
    return isinstance(u, (Integer, int)) and u%2 == 1

def eager_PerfectSquareQ(u):
    # (* If u is a rational number whose squareroot is rational or if u is of the form u1^n1 u2^n2 ...
    # and n1, n2, ... are even, PerfectSquareQ[u] returns True; else it returns False. *)
    if eager_RationalQ(u):
        return Greater(u, 0) and eager_RationalQ(Sqrt(u))
    elif eager_PowerQ(u):
        return eager_EvenQ(u.exp)
    elif eager_ProductQ(u):
        return eager_PerfectSquareQ(eager_First(u)) and eager_PerfectSquareQ(eager_Rest(u))
    elif eager_SumQ(u):
        s = eager_Simplify(u)
        if eager_NonsumQ(s):
            return eager_PerfectSquareQ(s)
        return False
    else:
        return False

def NiceSqrtAuxQ(u):
    if eager_RationalQ(u):
        return u > 0
    elif eager_PowerQ(u):
        return eager_EvenQ(u.exp)
    elif eager_ProductQ(u):
        return NiceSqrtAuxQ(eager_First(u)) and NiceSqrtAuxQ(eager_Rest(u))
    elif eager_SumQ(u):
        s = eager_Simplify(u)
        return  eager_NonsumQ(s) and NiceSqrtAuxQ(s)
    else:
        return False

def eager_NiceSqrtQ(u):
    return eager_Not(eager_NegativeQ(u)) and NiceSqrtAuxQ(u)

def eager_Together(u):
    # Mathematica's Together leaves denominator-free expressions untouched
    # (Together[(x+1)^2] = (x+1)^2, Together[a x + a] = a x + a): only expressions
    # with a denominator get combined and cancelled. This used factor(u)
    # unconditionally, so every Together-based guard (PosQ via TogetherSimplify, ...)
    # FACTORED whatever a wildcard bound to -- fatal inside commutative match
    # enumeration, where degree-~300 chunks of the expanded (a x^2 + b x^27)^12
    # were factored per candidate partition (py-spy: dmp factorization leaves under
    # check_constraint). For genuine fractions the factor() behaviour is kept: it
    # combines over a common denominator AND cancels, with the factored-denominator
    # presentation the rest of the port expects from Rubi's Together.
    # Denominator-free: Mathematica still pulls the CONTENT out of sums --
    # Together[6x+9] = 3(2x+3), Together[a^3+3a^2 b x+3a b^2 x^2] = a(a^2+...) --
    # which RemoveContent and PolynomialDivide rely on. sympy's factor_terms does
    # exactly that (content extraction, no factorization).
    u = S(u)
    if not u.is_Atom and u.as_numer_denom()[1] == S.One:
        try:
            return factor_terms(u)
        except (AttributeError, TypeError):
            return u
    return factor(u)

def _cmp_gt0(val):
    """``val > 0`` guarded against a NaN / non-real comparison.

    Returns True/False for a determinate result, or None when the comparison
    cannot be decided -- SymPy raises ``TypeError`` ("Invalid NaN comparison" or
    "cannot determine truth value" for a complex value), where the old direct
    ``val > 0`` aborted the whole DFS. Mathematica leaves such an ordering
    unevaluated, so an undeterminable numeric comparison is treated as "not
    positive" by the callers below (faithful: the rule simply does not apply).
    """
    try:
        res = val > 0
    except TypeError:
        return None
    if res is S.true or res is True:
        return True
    if res is S.false or res is False:
        return False
    return None


def PosAux(u):
    if eager_RationalQ(u):
        return u>0
    elif eager_NumberQ(u):
        r = _cmp_gt0(Im(u) if ZeroQ(Re(u)) else Re(u))
        return bool(r)  # a genuine number whose sign is undeterminable (NaN) -> False
    elif eager_NumericQ(u):
        v = N(u)
        r = _cmp_gt0(Im(v) if ZeroQ(Re(v)) else Re(v))
        return bool(r)
    elif eager_PowerQ(u):
        if eager_OddQ(u.exp):
            return PosAux(u.base)
        else:
            return True
    elif eager_ProductQ(u):
        if PosAux(eager_First(u)):
            return PosAux(eager_Rest(u))
        else:
            return not PosAux(eager_Rest(u))
    elif eager_SumQ(u):
        return PosAux(eager_First(u))
    else:
        r = _cmp_gt0(u)
        if r is not None:
            return r
        return True  # symbolic/undeterminable form -> assume positive (Rubi default)

@_pure_expr_cache(maxsize=20000)
def eager_PosQ(u):
    # If u is not 0 and has a positive form, PosQ[u] returns True, else it returns False.
    return PosAux(TogetherSimplify(u))

def CoefficientList(u, x):
    """Mathematica's ``CoefficientList`` does NOT give up on a non-polynomial: it
    collects the terms whose power of x is a non-negative integer and drops everything
    else into the degree-0 slot. ``CoefficientList[Sqrt[x]+x^2, x]`` is
    ``{Sqrt[x], 0, 1}``, ``CoefficientList[1/x, x]`` is ``{1/x}`` and
    ``CoefficientList[Sin[x], x]`` is ``{Sin[x]}`` -- only ``CoefficientList[0, x]``
    is ``{}``. This used to return ``[]`` for every non-polynomial, which also made the
    ``lst[-1]`` in ExpandIntegrand's With31 raise IndexError instead of returning a
    value. Values cross-checked against Mathematica 12.2.
    """
    u = sympify(u)
    if u == S(0):
        return []
    if eager_PolynomialQ(u, x):
        return list(reversed(Poly(u, x).all_coeffs()))
    buckets = {}
    for term in Add.make_args(Expand(u)):
        coeff, expo = term.as_coeff_exponent(x)
        if expo.is_Integer and expo >= 0 and not coeff.has(x):
            key = int(expo)
        else:
            key, coeff = 0, term
        buckets[key] = buckets.get(key, S(0)) + coeff
    return [buckets.get(i, S(0)) for i in range(max(buckets) + 1)]

def eager_ReplaceAll(expr, args):
    if isinstance(args, (tuple, list)):
        n_args = {}
        for i in args:
            n_args.update(i)
        return expr.subs(n_args)
    return expr.subs(args)

def eager_ExpandLinearProduct(v, u, a, b, x):
    # If u is a polynomial in x, ExpandLinearProduct[v,u,a,b,x] expands v*u into a sum of terms of the form c*v*(a+b*x)^n.
    if eager_FreeQ([a, b], x) and eager_PolynomialQ(u, x):
        lst = CoefficientList(eager_ReplaceAll(u, {x: (x - a)/b}), x)
        lst = [SimplifyTerm(i, x) for i in lst]
        res = 0
        for k in range(1, len(lst)+1):
            res = res + eager_Simplify(v*lst[k-1]*(a + b*x)**(k - 1))
        return res
    return u*v

def eager_GCD(*args):
    args = S(args)
    if len(args) == 1:
        if isinstance(args[0], (int, Integer)):
            return args[0]
        else:
            return S(1)
    # Fold pairwise: sympy's gcd(f, g, *gens) treats a 3rd positional arg as a
    # GENERATOR, not an operand -- eager_GCD(6, 10, 15) returned 2 (true gcd 1).
    result = gcd(args[0], args[1])
    for a in args[2:]:
        result = gcd(result, a)
    return result

def UnifyNegativeBaseFactors(u):
    """Rubi ``UnifyNegativeBaseFactors``::

        UnifyNegativeBaseFactors[u_.*(-v_)^m_*v_^n_.] :=
            UnifyNegativeBaseFactors[(-1)^n*u*(-v)^(m+n)] /; IntegerQ[n]
        UnifyNegativeBaseFactors[u_] := u

    Merges a pair of factors whose bases differ only in sign, so that
    ``(-v)^m * v^n`` becomes ``(-1)^n * (-v)^(m+n)``. Only used by
    :func:`ContentFactorAux`, and only for INTEGER n (for a fractional n the
    branch cut makes the rewrite invalid).
    """
    if not eager_ProductQ(u):
        return u
    factors = list(u.args)
    for i in range(len(factors)):
        b_i, m = factors[i].as_base_exp()
        for j in range(len(factors)):
            if i == j:
                continue
            b_j, n = factors[j].as_base_exp()
            # v^n must have an INTEGER exponent; (-v)^m may have any.
            if not eager_IntegerQ(n):
                continue
            if not ZeroQ(b_i + b_j):
                continue
            rest = [f for k, f in enumerate(factors) if k not in (i, j)]
            rebuilt = Mul(*rest) * S(-1)**n * b_i**(m + n)
            return UnifyNegativeBaseFactors(rebuilt)
    return u


def _content_times(common, rest):
    """``common * rest`` WITHOUT SymPy distributing a number over the sum.

    ContentFactor's whole purpose is to expose a common factor, but SymPy
    auto-distributes a Number over an Add inside ``Mul`` -- ``Mul(1/3, 2 + 3*x)``
    evaluates straight back to ``x + 2/3``, undoing the factorisation. SymPy's own
    ``factor_terms`` avoids this with ``_keep_coeff``, which builds the Mul in a form
    that survives; we use the same mechanism. Only the NUMERIC part needs the
    treatment -- a symbolic common factor (``a*(x + 1)``) does not distribute.
    """
    coeff, other = S(common).as_coeff_Mul()
    body = other*rest if other != S(1) else rest
    if coeff == S(1):
        return body
    # Mathematica canonicalises a factor of exactly -1 INTO the Plus, so
    # Times[Rational[-1,q], Plus[t...]] is stored as Times[Rational[1,q], Plus[-t...]].
    # Verified on Mathematica 12.2: (-1/3)(2+3x) -> Times[Rational[1,3], Plus[-2,-3x]]
    # and (-1/2)(2+x) likewise, while (-3/2)(2+x), (-2)(2+x) and (-1/3)a(2+3x) all KEEP
    # the sign on the coefficient -- the rewrite needs the numerator to be -1 and the
    # sum to be the coefficient's only companion. NumericFactor walks those args, so
    # without this it reported -1/3 where Rubi reports 1/3 for NumericFactor[-2/3 - x].
    if other == S(1) and coeff.is_Rational and coeff.p == -1 and coeff.q != 1:
        return _keep_coeff(Rational(1, coeff.q), -rest)
    return _keep_coeff(coeff, body)


def _numeric_factor_is_negative(u):
    """``NumericFactor[u] < 0``, False when the comparison is not decidable."""
    try:
        return bool(NumericFactor(u) < 0)
    except TypeError:
        return False


def ContentFactorAux(expn):
    """Rubi ``ContentFactorAux`` -- factor the content out of sums, recursively.

    Faithful transcription of the Rubi 4.17.3.0 definition::

        If[AtomQ[expn], expn,
        If[IntegerPowerQ[expn],
          If[SumQ[expn[[1]]] && NumericFactor[expn[[1,1]]] < 0,
             (-1)^expn[[2]]*ContentFactorAux[-expn[[1]]]^expn[[2]],
             ContentFactorAux[expn[[1]]]^expn[[2]]],
        If[ProductQ[expn],
          Module[{num=1, tmp},
            tmp = Map[If[SumQ[#] && NumericFactor[#[[1]]] < 0,
                         num = -num; ContentFactorAux[-#], ContentFactorAux[#]]&, expn];
            num*UnifyNegativeBaseFactors[tmp]],
        If[SumQ[expn],
          With[{lst = CommonFactors[List @@ expn]},
            If[lst[[1]] === 1 || lst[[1]] === -1, expn, lst[[1]]*Plus @@ Rest[lst]]],
          expn]]]]

    This used to be ``factor_terms``, which is close but not the same function: it
    leaves the content in when no term already carries a denominator, so
    ``ContentFactor[2/3 + x]`` came back unchanged where Mathematica gives
    ``(2 + 3*x)/3``. That fed ``NumericFactor``, which answered 1 instead of 1/3.
    """
    if eager_AtomQ(expn):
        return expn

    if eager_IntegerPowerQ(expn):
        base, exponent = expn.base, expn.exp
        if eager_SumQ(base) and _numeric_factor_is_negative(eager_First(base)):
            return S(-1)**exponent*ContentFactorAux(-base)**exponent
        return ContentFactorAux(base)**exponent

    if eager_ProductQ(expn):
        num = S(1)
        tmp = []
        for factor in expn.args:
            if eager_SumQ(factor) and _numeric_factor_is_negative(eager_First(factor)):
                num = -num
                tmp.append(ContentFactorAux(-factor))
            else:
                tmp.append(ContentFactorAux(factor))
        return num*UnifyNegativeBaseFactors(Mul(*tmp))

    if eager_SumQ(expn):
        lst = CommonFactors(list(expn.args))
        common = lst[0]
        if common == S(1) or common == S(-1):
            return expn
        return _content_times(common, Add(*lst[1:]))

    return expn


# Bounded memo: ContentFactor sits under NumericFactor/NonnumericFactors, which the
# guards call constantly on the same subexpressions, and the faithful version is much
# more work than the old factor_terms one-liner.
_CONTENT_FACTOR_CACHE: dict = {}
_CONTENT_FACTOR_CACHE_MAX = 20000


def ContentFactor(expn):
    """Rubi: ``TimeConstrained[ContentFactorAux[expn], $TimeLimit, expn]``.

    Rubi's time limit exists because ContentFactorAux can be expensive; the
    fallback is simply to return the input unfactored. We keep that contract for
    any failure -- returning the input is always sound, since the result is only
    ever a re-association of the same expression.
    """
    try:
        key = expn
        hash(key)
    except TypeError:
        key = None
    if key is not None:
        cached = _CONTENT_FACTOR_CACHE.get(key)
        if cached is not None:
            return cached
    try:
        result = ContentFactorAux(expn)
    except (RecursionError, TypeError, ValueError, AttributeError, PolynomialError):
        result = expn
    if key is not None and len(_CONTENT_FACTOR_CACHE) < _CONTENT_FACTOR_CACHE_MAX:
        _CONTENT_FACTOR_CACHE[key] = result
    return result

def NumericFactor(u):
    # returns the real numeric factor of u.
    if eager_NumberQ(u):
        if ZeroQ(Im(u)):
            return u
        elif ZeroQ(Re(u)):
            return Im(u)
        else:
            return S(1)
    elif eager_PowerQ(u):
        # Rubi: If[RationalQ[u[[1]]] && FractionQ[u[[2]]],
        #          If[u[[2]]>0, 1/Denominator[u[[1]]], 1/Denominator[1/u[[1]]]], 1].
        # The old code tested RationalQ on the exponent (too broad) and simplified the
        # negative branch to Denominator[b] instead of 1/Denominator[1/b] (= 1/Numerator[b]).
        if eager_RationalQ(u.base) and eager_FractionQ(u.exp):
            if u.exp > 0:
                return 1/eager_Denominator(u.base)
            else:
                return 1/eager_Denominator(1/u.base)
        else:
            return S(1)
    elif eager_ProductQ(u):
        return Mul(*[NumericFactor(i) for i in u.args])
    elif eager_SumQ(u):
        if eager_LeafCount(u) < 50:
            c = ContentFactor(u)
            if eager_SumQ(c):
                return S(1)
            else:
                return NumericFactor(c)
        else:
            m = NumericFactor(eager_First(u))
            n = NumericFactor(eager_Rest(u))
            if Less(m, 0) and Less(n, 0):   # robust: see SignOfFactor note on Less vs <
                return -eager_GCD(-m, -n)
            else:
                return eager_GCD(m, n)
    return S(1)

def NonnumericFactors(u):
    if eager_NumberQ(u):
        if ZeroQ(Im(u)):
            return S(1)
        elif ZeroQ(Re(u)):
            return I
        return u
    elif eager_PowerQ(u):
        if eager_RationalQ(u.base) and eager_FractionQ(u.exp):
            return u/NumericFactor(u)
        return u
    elif eager_ProductQ(u):
        result = 1
        for i in u.args:
            result *= NonnumericFactors(i)
        return result
    elif eager_SumQ(u):
        if eager_LeafCount(u) < 50:
            i = ContentFactor(u)
            if eager_SumQ(i):
                return u
            else:
                return NonnumericFactors(i)
        n = NumericFactor(u)
        result = 0
        for i in u.args:
            result += i/n
        return result
    return u

def MakeAssocList(u, x, alst=None):
    # (* MakeAssocList[u,x,alst] returns an association list of gensymed symbols with the nonatomic
    # parameters of a u that are not integer powers, products or sums. *)
    # Rubi stores {gensym, kernel} PAIRS (Append[alst, {Unique["Rubi"], u}]); an earlier
    # port dropped the pair, so GensymSubst never substituted anything and KernelSubst
    # mistook a kernel's BASE for the gensym and substituted its EXPONENT -- turning the
    # bare -1 in `-(-1)^(1/3) b^(1/3)` into 1/3 and corrupting partial fractions of
    # cubics (wrong antiderivative for e.g. x^2 log(c (a+b/x^3)^p)/(d+e x)).
    if alst is None:
        alst = []
    if eager_AtomQ(u):
        return alst
    elif eager_IntegerPowerQ(u):
        return MakeAssocList(u.base, x, alst)
    elif eager_ProductQ(u) or eager_SumQ(u):
        return MakeAssocList(eager_Rest(u), x, MakeAssocList(eager_First(u), x, alst))
    elif eager_FreeQ(u, x):
        if not any(kernel == u for _, kernel in alst):
            alst.append((Dummy('rubikern'), u))
        return alst
    return alst

def GensymSubst(u, x, alst=None):
    # (* GensymSubst[u,x,alst] returns u with the kernels in alst free of x replaced by gensymed names. *)
    if alst is None:
        alst = []
    if eager_AtomQ(u):
        return u
    elif eager_IntegerPowerQ(u):
        return GensymSubst(u.base, x, alst)**u.exp
    elif eager_ProductQ(u) or eager_SumQ(u):
        return u.func(*[GensymSubst(i, x, alst) for i in u.args])
    elif eager_FreeQ(u, x):
        for sym, kernel in alst:
            if kernel == u:
                return sym
        return u
    return u

def KernelSubst(u, x, alst):
    # (* KernelSubst[u,x,alst] returns u with the gensymed names in alst replaced by kernels free of x. *)
    if eager_AtomQ(u):
        for sym, kernel in alst:
            if sym == u:
                return kernel
        return u
    elif eager_IntegerPowerQ(u):
        tmp = KernelSubst(u.base, x, alst)
        if u.exp < 0 and ZeroQ(tmp):
            return 'Indeterminate'
        return tmp**u.exp
    elif eager_ProductQ(u) or eager_SumQ(u):
        return u.func(*[KernelSubst(i, x, alst) for i in u.args])
    return u

def eager_ExpandExpression(u, x):
    if eager_AlgebraicFunctionQ(u, x) and eager_Not(eager_RationalFunctionQ(u, x)):
        v = ExpandAlgebraicFunction(u, x)
    else:
        v = S(0)
    if eager_SumQ(v):
        return ExpandCleanup(v, x)
    v = SmartApart(u, x)
    if eager_SumQ(v):
        return ExpandCleanup(v, x)
    v = SmartApart(RationalFunctionFactors(u, x), x, x)
    if eager_SumQ(v):
        w = NonrationalFunctionFactors(u, x)
        return ExpandCleanup(v.func(*[i*w for i in v.args]), x)
    v = Expand(u)
    if eager_SumQ(v):
        return ExpandCleanup(v, x)
    v = Expand(u)
    if eager_SumQ(v):
        return ExpandCleanup(v, x)
    return SimplifyTerm(u, x)

# Apart moved to sympy_wolfram.functions_eager (imported above). Its RationalFunctionQ
# guard is exactly SymPy's is_rational_function, so the function is not Rubi-specific.

def SmartApart(*args):
    if len(args) == 2:
        u, x = args
        alst = MakeAssocList(u, x)
        tmp = KernelSubst(eager_Apart(GensymSubst(u, x, alst), x), x, alst)
        if tmp == 'Indeterminate':
            return u
        return tmp

    u, v, x = args
    alst = MakeAssocList(u, x)
    tmp = KernelSubst(eager_Apart(GensymSubst(u, x, alst), x), x, alst)
    if tmp == 'Indeterminate':
        return u
    return tmp

def eager_MatchQ(expr, pattern, *var):
    # returns the matched arguments after matching pattern with expression
    match = expr.match(pattern)
    if match:
        return tuple(match[i] for i in var)
    else:
        return None

def PolynomialQuotientRemainder(p, q, x):
    return [eager_PolynomialQuotient(p, q, x), eager_PolynomialRemainder(p, q, x)]

def eager_FreeFactors(u, x):
    # returns the product of the factors of u free of x.
    if eager_ProductQ(u):
        result = 1
        for i in u.args:
            if eager_FreeQ(i, x):
                result *= i
        return result
    elif eager_FreeQ(u, x):
        return u
    else:
        return S(1)

def eager_NonfreeFactors(u, x):
    """
    Returns the product of the factors of u not free of x.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import NonfreeFactors
    >>> from sympy.abc import x, a, b
    >>> NonfreeFactors(a, x)
    1
    >>> NonfreeFactors(x + a, x)
    a + x
    >>> NonfreeFactors(a*b*x, x)
    x

    """
    if eager_ProductQ(u):
        result = 1
        for i in u.args:
            if not eager_FreeQ(i, x):
                result *= i
        return result
    elif eager_FreeQ(u, x):
        return 1
    else:
        return u

def RemoveContentAux(expr, x):
    # An expression free of x has no x-content to strip; Rubi returns it unchanged
    # (e.g. RemoveContent[2*a+4*b, x] reduces to RemoveContentAux[1, x] -> 1).
    # Guarding here also avoids feeding a bare atom to the matchpy replacer, which
    # would mis-bind it and raise (matchpy Symbol has no .is_Add).
    expr = sympify(expr)
    if not expr.has(x):
        return expr
    result = RemoveContentAux_replacer.replace(UtilityOperator(expr, x))
    if isinstance(result, Operation) and result.head == UtilityOp:
        return expr
    return matchpy_to_sympy(result)

def RemoveContent(u, x):
    v = eager_NonfreeFactors(u, x)
    w = eager_Together(v)

    if eager_EqQ(eager_FreeFactors(w, x), 1):
        return RemoveContentAux(v, x)
    else:
        return RemoveContentAux(eager_NonfreeFactors(w, x), x)


def FreeTerms(u, x):
    """
    Returns the sum of the terms of u free of x.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import FreeTerms
    >>> from sympy.abc import x, a, b
    >>> FreeTerms(a, x)
    a
    >>> FreeTerms(x*a, x)
    0
    >>> FreeTerms(a*x + b, x)
    b

    """
    if eager_SumQ(u):
        result = 0
        for i in u.args:
            if eager_FreeQ(i, x):
                result += i
        return result
    elif eager_FreeQ(u, x):
        return u
    else:
        return 0

def NonfreeTerms(u, x):
    # returns the sum of the terms of u free of x.
    if eager_SumQ(u):
        result = S(0)
        for i in u.args:
            if not eager_FreeQ(i, x):
                result += i
        return result
    elif not eager_FreeQ(u, x):
        return u
    else:
        return S(0)

def ExpandAlgebraicFunction(expr, x):
    """Port of Rubi's two ``ExpandAlgebraicFunction`` definitions::

        ExpandAlgebraicFunction[u_Plus*v_, x_Symbol] :=
            Map[Function[#*v], u] /; !FreeQ[u, x]
        ExpandAlgebraicFunction[v_.*u_Plus^n_, x_Symbol] :=
            With[{w = Expand[u^n, x]}, Map[Function[#*v], w] /; SumQ[w]] /;
                IGtQ[n, 0] && !FreeQ[u, x]

    The previous version declared ``u = Wild('u', exclude=[x])`` -- the exact OPPOSITE
    of Rubi's ``!FreeQ[u, x]`` -- so it was wrong in both directions: it expanded sums
    that are FREE of x (``(a+b)*x`` became ``a*x + b*x``; Rubi leaves it alone), and it
    failed to expand the ``u_Plus^n_`` form because the x-dependent base was excluded
    (``(a+x)**2*v`` came back unchanged; Rubi gives ``a^2 v + 2 a v x + v x^2``).

    Note Rubi maps over ONE Plus factor and leaves the rest intact -- it is not a full
    expand: ``(a+x)*(b+x)`` gives ``a*(b+x) + x*(b+x)``. All values cross-checked
    against Rubi 4.17.3.0.
    """
    if eager_ProductQ(expr):
        args = list(expr.args)
        # definition 1 -- a Plus factor that DEPENDS on x
        for i, factor in enumerate(args):
            if eager_SumQ(factor) and not eager_FreeQ(factor, x):
                v = Mul(*(args[:i] + args[i + 1:]))
                return Add(*[t*v for t in factor.args])
        # definition 2 -- (Plus)^n with n a positive integer and an x-dependent base
        for i, factor in enumerate(args):
            if (eager_PowerQ(factor) and eager_SumQ(factor.base)
                    and PositiveIntegerQ(factor.exp) and not eager_FreeQ(factor.base, x)):
                w = Expand(factor.base**factor.exp)
                if eager_SumQ(w):
                    v = Mul(*(args[:i] + args[i + 1:]))
                    return Add(*[t*v for t in w.args])
    elif (eager_PowerQ(expr) and eager_SumQ(expr.base)
            and PositiveIntegerQ(expr.exp) and not eager_FreeQ(expr.base, x)):
        # `v_.` is Optional, so a bare (a+x)^3 matches definition 2 with v -> 1
        w = Expand(expr.base**expr.exp)
        if eager_SumQ(w):
            return w

    return expr


def _reciprocal_of_linear_parts(term, x):
    """If ``term == e/(a + b*x)`` with ``e, a, b`` free of x and b != 0, return
    ``(e, a, b)``; else None. Structural classifier used by CollectReciprocals."""
    num, den = term.as_numer_denom()
    if x in num.free_symbols:
        return None
    try:
        poly = Poly(den, x)
    except (PolynomialError, GeneratorsNeeded):
        return None
    if poly.degree() != 1:
        return None
    b, a = poly.all_coeffs()
    if x in a.free_symbols or x in b.free_symbols:
        return None
    return (num, a, b)


@_pure_expr_cache(maxsize=20000)
def CollectReciprocals(expr, x):
    # Basis: e/(a+b x)+f/(c+d x)==(c e+a f+(d e+b f) x)/(a c+(b c+a d) x+b d x^2)
    #
    # STRUCTURAL scan instead of the old Wild .match: matching the 7-wildcard pattern
    # ``u_ + e_/(a_+b_*x) + f_/(c_+d_*x)`` against a COMMUTATIVE Add backtracks
    # exponentially per call (14% of a profiled log-family timeout, where every DFS
    # step feeds a DISTINCT sum so the memo cache cannot absorb it). The scan
    # classifies each term as e/(a+b*x) once (linear-time) and tests the zero
    # conditions pairwise -- same semantics, polynomial cost. Memoised on top.
    if eager_SumQ(expr):
        terms = list(expr.args)
        recips = [(i, _reciprocal_of_linear_parts(t, x)) for i, t in enumerate(terms)]
        recips = [(i, r) for i, r in recips if r is not None]
        for ii in range(len(recips)):
            i, (e, a, b) = recips[ii]
            for jj in range(ii + 1, len(recips)):
                j, (f, c, d) = recips[jj]
                if not ZeroQ(b*c + a*d):
                    continue
                rest = Add(*[t for k, t in enumerate(terms) if k not in (i, j)])
                if ZeroQ(d*e + b*f):
                    return CollectReciprocals(rest + (c*e + a*f)/(a*c + b*d*x**2), x)
                if ZeroQ(c*e + a*f):
                    return CollectReciprocals(rest + (d*e + b*f)*x/(a*c + b*d*x**2), x)
    return expr

def ExpandCleanup(u, x):
    v = CollectReciprocals(u, x)
    if eager_SumQ(v):
        res = 0
        for i in v.args:
            res += SimplifyTerm(i, x)
        v = res
        if eager_SumQ(v):
            return UnifySum(v, x)
        else:
            return v
    else:
        return v

def eager_AlgebraicFunctionQ(u, x, flag=False):
    if ListQ(u):
        if u == []:
            return True
        elif eager_AlgebraicFunctionQ(eager_First(u), x, flag):
            return eager_AlgebraicFunctionQ(eager_Rest(u), x, flag)
        else:
            return False

    elif eager_AtomQ(u) or eager_FreeQ(u, x):
        return True
    elif eager_PowerQ(u):
        if eager_RationalQ(u.exp) | flag & eager_FreeQ(u.exp, x):
            return eager_AlgebraicFunctionQ(u.base, x, flag)
    elif eager_ProductQ(u) | eager_SumQ(u):
        for i in u.args:
            if not eager_AlgebraicFunctionQ(i, x, flag):
                return False
        return True

    return False

def eager_Coeff(expr, form, n=1):
    if n == 1:
        return eager_Coefficient(eager_Together(expr), form, n)
    else:
        coef1 = eager_Coefficient(expr, form, n)
        coef2 = eager_Coefficient(eager_Together(expr), form, n)
        # Structurally equal coefficients need no Simplify -- the full
        # simplify(coef1 - coef2) below is brutally expensive on the nested-radical
        # coefficients partial fractions produce (py-spy: dominant cost of the
        # 1/((a+c x^4)(d+e x)^2) hang), and in the common case the two extractions
        # agree exactly.
        if coef1 == coef2:
            return coef1
        if eager_Simplify(coef1 - coef2) == 0:
            return coef1
        else:
            return coef2

def LeadTerm(u):
    if eager_SumQ(u):
        return eager_First(u)
    return u

def RemainingTerms(u):
    """Rubi: ``If[SumQ[u], Rest[u], 0]`` — a NON-sum has no remaining terms, so 0.
    This returned the input itself, which double-counts the term in every caller
    that adds ``LeadTerm(u) + RemainingTerms(u)`` back together."""
    if eager_SumQ(u):
        return eager_Rest(u)
    return S(0)

def LeadFactor(u):
    # returns the leading factor of u.
    if eager_ComplexNumberQ(u) and Re(u) == 0:
        if Im(u) == S(1):
            return u
        else:
            return LeadFactor(Im(u))
    elif eager_ProductQ(u):
            return LeadFactor(eager_First(u))
    return u

def RemainingFactors(u):
    # returns the remaining factors of u.
    if eager_ComplexNumberQ(u) and Re(u) == 0:
        if Im(u) == 1:
            return S(1)
        else:
            return I*RemainingFactors(Im(u))
    elif eager_ProductQ(u):
        return RemainingFactors(eager_First(u))*eager_Rest(u)
    return S(1)

def LeadBase(u):
    """
    returns the base of the leading factor of u.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import LeadBase
    >>> from sympy.abc import a, b, c
    >>> LeadBase(a**b)
    a
    >>> LeadBase(a**b*c)
    a
    """
    v = LeadFactor(u)
    if eager_PowerQ(v):
        return v.base
    return v

def LeadDegree(u):
    # returns the degree of the leading factor of u.
    v = LeadFactor(u)
    if eager_PowerQ(v):
        return v.exp
    return S(1)

def eager_Numer(expr):
    # returns the numerator of u.
    if eager_PowerQ(expr):
        if expr.exp < 0:
            return 1
    if eager_ProductQ(expr):
        return Mul(*[eager_Numer(i) for i in expr.args])
    return eager_Numerator(expr)

def eager_Denom(u):
    # returns the denominator of u
    if eager_PowerQ(u):
        if u.exp < 0:
            return u.args[0]**(-u.args[1])
    elif eager_ProductQ(u):
        return Mul(*[eager_Denom(i) for i in u.args])
    return eager_Denominator(u)

def eager_Expon(expr, form):
    return eager_Exponent(eager_Together(expr), form)

@_pure_expr_cache(maxsize=20000)
def MergeMonomials(expr, x):
    # MEMOISED: this runs two sympy Wild .match calls per invocation, and matching a
    # COMMUTATIVE product backtracks exponentially (_matches_commutative was the top
    # self-time frame of a profiled 60s+ trig timeout: NormalizeIntegrandAux ->
    # MergeMonomials held 60% of all samples, recomputed on the same expressions
    # throughout the DFS -- one NormalizeIntegrandFactor branch even calls it three
    # times with identical arguments).
    u_ = Wild('u')
    p_ = Wild('p', exclude=[x, 1, 0])
    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x, 0])
    c_ = Wild('c', exclude=[x])
    d_ = Wild('d', exclude=[x, 0])
    n_ = Wild('n', exclude=[x])
    m_ = Wild('m', exclude=[x])

    # Basis: If  m/n\[Element]\[DoubleStruckCapitalZ], then z^m (c z^n)^p==(c z^n)^(m/n+p)/c^(m/n)
    pattern = u_*(a_ + b_*x)**m_*(c_*(a_ + b_*x)**n_)**p_
    match = expr.match(pattern)
    if match:
        keys = [u_, a_, b_, m_, c_, n_, p_]
        if len(keys) == len(match):
            u, a, b, m, c, n, p = tuple([match[i] for i in keys])
            if eager_IntegerQ(m/n):
                if u*(c*(a + b*x)**n)**(m/n + p)/c**(m/n) is S.NaN:
                    return expr
                else:
                    return u*(c*(a + b*x)**n)**(m/n + p)/c**(m/n)


    # Basis: If  m\[Element]\[DoubleStruckCapitalZ] \[And] b c-a d==0, then (a+b z)^m==b^m/d^m (c+d z)^m
    pattern = u_*(a_ + b_*x)**m_*(c_ + d_*x)**n_
    match = expr.match(pattern)
    if match:
        keys = [u_, a_, b_, m_, c_, d_, n_]
        if len(keys) == len(match):
            u, a, b, m, c, d, n = tuple([match[i] for i in keys])
            if eager_IntegerQ(m) and ZeroQ(b*c - a*d):
                if u*b**m/d**m*(c + d*x)**(m + n) is S.NaN:
                    return expr
                else:
                    return u*b**m/d**m*(c + d*x)**(m + n)
    return expr

def eager_PolynomialDivide(u, v, x):


    quo = eager_PolynomialQuotient(u, v, x)
    rem = eager_PolynomialRemainder(u, v, x)
    s = 0
    for i in ExponentList(quo, x):
        s += eager_Simp(eager_Together(eager_Coefficient(quo, x, i)*x**i), x)
    quo = s
    rem = eager_Together(rem)
    free = eager_FreeFactors(rem, x)
    rem = eager_NonfreeFactors(rem, x)
    monomial = x**Min(*ExponentList(rem, x))
    if eager_NegQ(eager_Coefficient(rem, x, 0)):
        monomial = -monomial
    s = 0
    for i in ExponentList(rem, x):
        s += eager_Simp(eager_Together(eager_Coefficient(rem, x, i)*x**i/monomial), x)
    rem = s
    if eager_BinomialQ(v, x):
        return quo + free*monomial*rem/eager_ExpandToSum(v, x)
    else:
        return quo + free*monomial*rem/v



def eager_BinomialQ(u, x, n=None):
    """
    If u is equivalent to an expression of the form a + b*x**n, BinomialQ(u, x, n) returns True, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import BinomialQ
    >>> from sympy.abc import x
    >>> BinomialQ(x**9, x)
    True
    >>> BinomialQ((1 + x)**3, x)
    False

    """
    if ListQ(u):
        for i in u:
            if eager_Not(eager_BinomialQ(i, x, n)):
                return False
        return True
    elif eager_NumberQ(x):
        return False
    return ListQ(BinomialParts(u, x))

def eager_TrinomialQ(u, x):
    """
    If u is equivalent to an expression of the form a + b*x**n + c*x**(2*n) where n, b and c are not 0,
    TrinomialQ(u, x) returns True, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import TrinomialQ
    >>> from sympy.abc import x
    >>> TrinomialQ((7 + 2*x**6 + 3*x**12), x)
    True
    >>> TrinomialQ(x**2, x)
    False

    """
    if ListQ(u):
        for i in u.args:
            if eager_Not(eager_TrinomialQ(i, x)):
                return False
        return True

    check = False
    if eager_PowerQ(u):
        if u.exp == 2 and eager_BinomialQ(u.base, x):
            check = True

    return ListQ(TrinomialParts(u,x)) and eager_Not(eager_QuadraticQ(u, x)) and eager_Not(check)

def eager_GeneralizedBinomialQ(u, x):
    """
    If u is equivalent to an expression of the form a*x**q+b*x**n where n, q and b are not 0,
    GeneralizedBinomialQ(u, x) returns True, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import GeneralizedBinomialQ
    >>> from sympy.abc import a, x, q, b, n
    >>> GeneralizedBinomialQ(a*x**q, x)
    False

    """
    if ListQ(u):
        return all(eager_GeneralizedBinomialQ(i, x) for i in u)
    return ListQ(GeneralizedBinomialParts(u, x))

def eager_GeneralizedTrinomialQ(u, x):
    """
    If u is equivalent to an expression of the form a*x**q+b*x**n+c*x**(2*n-q) where n, q, b and c are not 0,
    GeneralizedTrinomialQ(u, x) returns True, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import GeneralizedTrinomialQ
    >>> from sympy.abc import x
    >>> GeneralizedTrinomialQ(7 + 2*x**6 + 3*x**12, x)
    False

    """
    if ListQ(u):
        return all(eager_GeneralizedTrinomialQ(i, x) for i in u)
    return ListQ(GeneralizedTrinomialParts(u, x))

def FactorSquareFreeList(poly):
    """Mathematica orders the factors by DEGREE ASCENDING; SymPy's ``sqf_list`` orders
    them by multiplicity, so ``x^5-x^3-x^2+1`` came back as
    ``{{1,1},{cubic,1},{-1+x,2}}`` where Mathematica gives
    ``{{1,1},{-1+x,2},{cubic,1}}``. Verified against Mathematica 12.2 on three
    polynomials. (The one caller, ``PerfectPowerTest``, is order-independent -- it
    takes a GCD of the exponents and a product -- so this is fidelity, not a fix.)
    """
    r = sqf_list(poly)
    factors = [list(i) for i in r[1]]
    factors.sort(key=lambda fe: (Poly(fe[0]).total_degree() if fe[0].free_symbols else 0,
                                 default_sort_key(fe[0])))
    return [[1, 1]] + factors

def PerfectPowerTest(u, x):
    # If u (x) is equivalent to a polynomial raised to an integer power greater than 1,
    # PerfectPowerTest[u,x] returns u (x) as an expanded polynomial raised to the power;
    # else it returns False.
    if eager_PolynomialQ(u, x):
        lst = FactorSquareFreeList(u)
        gcd = 0
        v = 1
        if lst[0] == [1, 1]:
            lst = eager_Rest(lst)
        for i in lst:
            gcd = eager_GCD(gcd, i[1])
        if gcd > 1:
            for i in lst:
                v = v*i[0]**(i[1]/gcd)
            return Expand(v)**gcd
        else:
            return False
    return False

def SquareFreeFactorTest(u, x):
    # If u (x) can be square free factored, SquareFreeFactorTest[u,x] returns u (x) in
    # factored form; else it returns False.
    if eager_PolynomialQ(u, x):
        v = FactorSquareFree(u)
        if eager_PowerQ(v) or eager_ProductQ(v):
            return v
        return False
    return False

def eager_RationalFunctionQ(u, x):
    # If u is a rational function of x, RationalFunctionQ[u,x] returns True; else it returns False.
    if eager_AtomQ(u) or eager_FreeQ(u, x):
        return True
    elif eager_IntegerPowerQ(u):
        return eager_RationalFunctionQ(u.base, x)
    elif eager_ProductQ(u) or eager_SumQ(u):
        for i in u.args:
            if eager_Not(eager_RationalFunctionQ(i, x)):
                return False
        return True
    return False

def RationalFunctionFactors(u, x):
    # RationalFunctionFactors[u,x] returns the product of the factors of u that are rational functions of x.
    if eager_ProductQ(u):
        res = 1
        for i in u.args:
            if eager_RationalFunctionQ(i, x):
                res *= i
        return res
    elif eager_RationalFunctionQ(u, x):
        return u
    return S(1)

def NonrationalFunctionFactors(u, x):
    if eager_ProductQ(u):
        res = 1
        for i in u.args:
            if not eager_RationalFunctionQ(i, x):
                res *= i
        return res
    elif eager_RationalFunctionQ(u, x):
        return S(1)
    return u

def Reverse(u):
    if isinstance(u, (tuple, list, Tuple)):
        return list(reversed(u))
    else:
        l = list(u.args)
        return u.func(*list(reversed(l)))

def eager_RationalFunctionExponents(u, x):
    """
    u is a polynomial or rational function of x.
    RationalFunctionExponents(u, x) returns a list of the exponent of the
    numerator of u and the exponent of the denominator of u.

    Examples
    ========
    >>> from rubi_rules.utils.utility_functions import RationalFunctionExponents
    >>> from sympy.abc import x, a
    >>> RationalFunctionExponents(x, x)
    [1, 0]
    >>> RationalFunctionExponents(x**(-1), x)
    [0, 1]
    >>> RationalFunctionExponents(x**(-1)*a, x)
    [0, 1]

    """
    if eager_PolynomialQ(u, x):
        return [eager_Exponent(u, x), 0]
    elif eager_IntegerPowerQ(u):
        # Rubi: u[[2]]*RationalFunctionExponents[u[[1]],x]. In Mathematica a
        # scalar times a list SCALES it element-wise; in Python `n * [a, b]`
        # REPEATS the list, so this silently returned e.g. [0,1,0,1] for
        # (x+1)^-2 instead of [0,2] (and 6 entries for ^-3). Scale explicitly.
        if eager_PositiveQ(u.exp):
            return [u.exp*i for i in eager_RationalFunctionExponents(u.base, x)]
        return [(-u.exp)*i for i in Reverse(eager_RationalFunctionExponents(u.base, x))]
    elif eager_ProductQ(u):
        lst1 = eager_RationalFunctionExponents(eager_First(u), x)
        lst2 = eager_RationalFunctionExponents(eager_Rest(u), x)
        return [lst1[0] + lst2[0], lst1[1] + lst2[1]]
    elif eager_SumQ(u):
        v = eager_Together(u)
        if eager_SumQ(v):
            lst1 = eager_RationalFunctionExponents(eager_First(u), x)
            lst2 = eager_RationalFunctionExponents(eager_Rest(u), x)
            return [Max(lst1[0] + lst2[1], lst2[0] + lst1[1]), lst1[1] + lst2[1]]
        else:
            return eager_RationalFunctionExponents(v, x)
    return [0, 0]

def eager_RationalFunctionExpand(expr, x):
    # expr is a polynomial or rational function of x.
    # RationalFunctionExpand[u,x] returns the expansion of the factors of u that are rational functions times the other factors.
    def cons_f1(n):
        return eager_FractionQ(n)
    cons1 = _patched_custom_constraint_call(cons_f1)

    def cons_f2(x, v):
        if not isinstance(x, Symbol):
            return False
        return eager_UnsameQ(v, x)
    cons2 = _patched_custom_constraint_call(cons_f2)

    def With1(n, u, x, v):
        w = eager_RationalFunctionExpand(u, x)
        return eager_If(eager_SumQ(w), Add(*[i*v**n for i in w.args]), v**n*w)
    pattern1 = Pattern(UtilityOperator(u_*v_**n_, x_), cons1, cons2)
    rule1 = _ReplacementRuleWrapped(pattern1, With1)
    def With2(u, x):
        v = eager_ExpandIntegrand(u, x)

        def _consf_u(a, b, c, d, p, m, n, x):
            return And(eager_FreeQ(eager_List(a, b, c, d, p), x), eager_IntegersQ(m, n), Equal(m, Add(n, S(-1))))
        cons_u = _patched_custom_constraint_call(_consf_u)
        pat = Pattern(UtilityOperator(x_**WildSymbol('m', optional_value=S(1))*(x_*WildSymbol('d', optional_value=S(1)) + c_)**p_/(x_**n_*WildSymbol('b', optional_value=S(1)) + a_), x_), cons_u)
        result_matchq = is_match(UtilityOperator(u, x), pat)
        if eager_UnsameQ(v, u) and not result_matchq:
            return v
        else:
            v = eager_ExpandIntegrand(RationalFunctionFactors(u, x), x)
            w = NonrationalFunctionFactors(u, x)
            if eager_SumQ(v):
                return Add(*[i*w for i in v.args])
            else:
                return v*w
    pattern2 = Pattern(UtilityOperator(u_, x_))
    rule2 = _ReplacementRuleWrapped(pattern2, With2)
    result = replace_all(UtilityOperator(expr, x), [rule1, rule2])
    if isinstance(result, Operation) and result.head == UtilityOp:
        res = expr
    else:
        res = matchpy_to_sympy(result)
    return res


def eager_ExpandIntegrand(expr, x, extra=None):
    if extra is not None:
        extra, x = x, extra
        w = eager_ExpandIntegrand(extra, x)
        r = NonfreeTerms(w, x)
        if eager_SumQ(r):
            result = [expr*FreeTerms(w, x)]
            for i in r.args:
                result.append(MergeMonomials(expr*i, x))
            return r.func(*result)
        else:
            return expr*FreeTerms(w, x) + MergeMonomials(expr*r, x)

    else:
        u_ = Wild('u', exclude=[0, 1])
        a_ = Wild('a', exclude=[x])
        b_ = Wild('b', exclude=[x, 0])
        F_ = Wild('F', exclude=[0])
        c_ = Wild('c', exclude=[x])
        d_ = Wild('d', exclude=[x, 0])
        n_ = Wild('n', exclude=[0, 1])
        pattern = u_*(a_ + b_*F_)**n_
        match = expr.match(pattern)
        if match:
            if eager_MemberQ([asin, acos, asinh, acosh], match[F_].func):
                keys = [u_, a_, b_, F_, n_]
                if len(match) == len(keys):
                    u, a, b, F, n = tuple([match[i] for i in keys])
                    match = F.args[0].match(c_ + d_*x)
                    if match:
                        keys = c_, d_
                        if len(keys) == len(match):
                            c, d = tuple([match[i] for i in keys])
                            if eager_PolynomialQ(u, x):
                                F = F.func
                                return eager_ExpandLinearProduct((a + b*F(c + d*x))**n, u, c, d, x)

        result = replace_all(UtilityOperator(expr, x), ExpandIntegrand_rules, max_count = 1)
        if isinstance(result, Operation) and result.head == UtilityOp:
            res = expr
        else:
            res = matchpy_to_sympy(result)
        return res


def eager_SimplerQ(u, v):
    # If u is simpler than v, SimplerQ(u, v) returns True, else it returns False.  SimplerQ(u, u) returns False
    if eager_IntegerQ(u):
        if eager_IntegerQ(v):
            if Abs(u)==Abs(v):
                return v<0
            else:
                return Abs(u)<Abs(v)
        else:
            return True
    elif eager_IntegerQ(v):
        return False
    elif eager_FractionQ(u):
        if eager_FractionQ(v):
            if eager_Denominator(u) == eager_Denominator(v):
                return eager_SimplerQ(eager_Numerator(u), eager_Numerator(v))
            else:
                return eager_Denominator(u)<eager_Denominator(v)
        else:
            return True
    elif eager_FractionQ(v):
        return False
    elif (Re(u)==0 or Re(u) == 0) and (Re(v)==0 or Re(v) == 0):
        return eager_SimplerQ(Im(u), Im(v))
    elif eager_ComplexNumberQ(u):
        if eager_ComplexNumberQ(v):
            if Re(u) == Re(v):
                return eager_SimplerQ(Im(u), Im(v))
            else:
                return eager_SimplerQ(Re(u),Re(v))
        else:
            return False
    elif eager_NumberQ(u):
        if eager_NumberQ(v):
            return OrderedQ([u,v])
        else:
            return True
    elif eager_NumberQ(v):
        return False
    elif eager_AtomQ(u) or (eager_Head(u) == re) or (eager_Head(u) == im):
        if eager_AtomQ(v) or (eager_Head(u) == re) or (eager_Head(u) == im):
            return OrderedQ([u,v])
        else:
            return True
    elif eager_AtomQ(v) or (eager_Head(u) == re) or (eager_Head(u) == im):
        return False
    elif eager_Head(u) == eager_Head(v):
        if eager_Length(u) == eager_Length(v):
            for i in range(len(u.args)):
                if not u.args[i] == v.args[i]:
                    return eager_SimplerQ(u.args[i], v.args[i])
            return False
        return eager_Length(u) < eager_Length(v)
    elif eager_LeafCount(u) < eager_LeafCount(v):
        return True
    elif eager_LeafCount(v) < eager_LeafCount(u):
        return False
    return eager_Not(OrderedQ([v,u]))

def eager_SimplerSqrtQ(u, v):
    # If Rt(u, 2) is simpler than Rt(v, 2), SimplerSqrtQ(u, v) returns True, else it returns False.  SimplerSqrtQ(u, u) returns False
    if eager_NegativeQ(v) and eager_Not(eager_NegativeQ(u)):
        return True
    if eager_NegativeQ(u) and eager_Not(eager_NegativeQ(v)):
        return False
    sqrtu = eager_Rt(u, S(2))
    sqrtv = eager_Rt(v, S(2))
    if eager_IntegerQ(sqrtu):
        if eager_IntegerQ(sqrtv):
            return sqrtu<sqrtv
        else:
            return True
    if eager_IntegerQ(sqrtv):
        return False
    if eager_RationalQ(sqrtu):
        if eager_RationalQ(sqrtv):
            return sqrtu<sqrtv
        else:
            return True
    if eager_RationalQ(sqrtv):
        return False
    if eager_PosQ(u):
        if eager_PosQ(v):
            return eager_LeafCount(sqrtu)<eager_LeafCount(sqrtv)
        else:
            return True
    if eager_PosQ(v):
        return False
    if eager_LeafCount(sqrtu)<eager_LeafCount(sqrtv):
        return True
    if eager_LeafCount(sqrtv)<eager_LeafCount(sqrtu):
        return False
    else:
        return eager_Not(OrderedQ([v, u]))

def eager_SumSimplerQ(u, v):
    """
    If u + v is simpler than u, SumSimplerQ(u, v) returns True, else it returns False.
    If for every term w of v there is a term of u equal to n*w where n<-1/2, u + v will be simpler than u.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import SumSimplerQ
    >>> from sympy.abc import x
    >>> from sympy import S
    >>> SumSimplerQ(S(4 + x),S(3 + x**3))
    False

    """
    if eager_RationalQ(u, v):
        if v == S(0):
            return False
        elif v > S(0):
            return u < -S(1)
        else:
            return u >= -v
    else:
        return SumSimplerAuxQ(Expand(u), Expand(v))

def eager_BinomialDegree(u, x):
    # if u is a binomial. BinomialDegree[u,x] returns the degree of x in u.
    bp = BinomialParts(u, x)
    if bp == False:
        return bp
    return bp[2]

def eager_TrinomialDegree(u, x):
    # If u is equivalent to a trinomial of the form a + b*x^n + c*x^(2*n) where n!=0, b!=0 and c!=0, TrinomialDegree[u,x] returns n
    t = TrinomialParts(u, x)
    if t:
        return t[3]
    return t

def CancelCommonFactors(u, v):
    def _delete_cases(a, b):
        # only for CancelCommonFactors
        lst = []
        deleted = False
        for i in a.args:
            if i == b and not deleted:
                deleted = True
                continue
            lst.append(i)
        return a.func(*lst)

    # CancelCommonFactors[u,v] returns {u',v'} are the noncommon factors of u and v respectively.
    if eager_ProductQ(u):
        if eager_ProductQ(v):
            if eager_MemberQ(v, eager_First(u)):
                return CancelCommonFactors(eager_Rest(u), _delete_cases(v, eager_First(u)))
            else:
                lst = CancelCommonFactors(eager_Rest(u), v)
                return [eager_First(u)*lst[0], lst[1]]
        else:
            if eager_MemberQ(u, v):
                return [_delete_cases(u, v), 1]
            else:
                return[u, v]
    elif eager_ProductQ(v):
        if eager_MemberQ(v, u):
            return [1, _delete_cases(v, u)]
        else:
            return [u, v]
    return[u, v]

def eager_SimplerIntegrandQ(u, v, x):
    lst = CancelCommonFactors(u, v)
    u1 = lst[0]
    v1 = lst[1]
    # Head/Length recursive branch was commented out in IntegrationUtilityFunctions.m
    # (lines 808-809) and must not be active.
    # Threshold: Mathematica uses 6/10 (line 810); integer form is 5*L < 3*L (not 4*L).
    if 5*eager_LeafCount(u1) < 3*eager_LeafCount(v1):
        return True
    if eager_RationalFunctionQ(u1, x):
        if eager_RationalFunctionQ(v1, x):
            t1 = 0
            t2 = 0
            for i in eager_RationalFunctionExponents(u1, x):
                t1 += i
            for i in eager_RationalFunctionExponents(v1, x):
                t2 += i
            return t1 < t2
        else:
            return True
    else:
        return False

def GeneralizedBinomialDegree(u, x):
    b = GeneralizedBinomialParts(u, x)
    if b:
        return b[2] - b[3]

def GeneralizedBinomialParts(expr, x):
    expr = Expand(expr)
    if eager_GeneralizedBinomialMatchQ(expr, x):
        # The exclusions MUST match GeneralizedBinomialMatchQ's above. With the
        # looser `exclude=[x]` this re-match could return a DEGENERATE solution the
        # gate had rejected (b=0, leaving n unbound) and then raise KeyError.
        a = Wild('a', exclude=[x, 0])
        b = Wild('b', exclude=[x, 0])
        n = Wild('n', exclude=[x, 0])
        q = Wild('q', exclude=[x, 0])
        Match = expr.match(a*x**q + b*x**n)
        if Match and len(Match) == 4:
            if eager_PosQ(Match[q] - Match[n]):
                return [Match[b], Match[a], Match[q], Match[n]]
            elif eager_PosQ(Match[n] - Match[q]):
                return [Match[a], Match[b], Match[n], Match[q]]
    else:
        return False

def eager_GeneralizedTrinomialDegree(u, x):
    t = GeneralizedTrinomialParts(u, x)
    if t:
        return t[3] - t[4]

def GeneralizedTrinomialParts(expr, x):
    expr = Expand(expr)
    if eager_GeneralizedTrinomialMatchQ(expr, x):
        a = Wild('a', exclude=[x, 0])
        b = Wild('b', exclude=[x, 0])
        c = Wild('c', exclude=[x])
        n = Wild('n', exclude=[x, 0])
        q = Wild('q', exclude=[x])
        Match = expr.match(a*x**q + b*x**n+c*x**(2*n-q))
        if Match and len(Match) == 5 and expr.is_Add:
            return [Match[c], Match[b], Match[a], Match[n], 2*Match[n]-Match[q]]
    else:
        return False

def eager_MonomialQ(u, x):
    # If u is of the form a*x^n where n!=0 and a!=0, MonomialQ[u,x] returns True; else False
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_MonomialQ(i, x) for i in u)
    else:
        a = Wild('a', exclude=[x])
        b = Wild('b', exclude=[x])
        re = u.match(a*x**b)
        if re:
            return True
    return False

def MonomialSumQ(u, x):
    # if u(x) is a sum and each term is free of x or an expression of the form a*x^n, MonomialSumQ(u, x) returns True; else it returns False
    if eager_SumQ(u):
        for i in u.args:
            if eager_Not(eager_FreeQ(i, x) or eager_MonomialQ(i, x)):
                return False
        return True


def eager_MinimumMonomialExponent(u, x):
    """
    u is sum whose terms are monomials.  MinimumMonomialExponent(u, x) returns the exponent of the term having the smallest exponent

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import MinimumMonomialExponent
    >>> from sympy.abc import x
    >>> MinimumMonomialExponent(x**2 + 5*x**2 + 3*x**5, x)
    2
    >>> MinimumMonomialExponent(x**2 + 5*x**2 + 1, x)
    0
    """

    # In Mathematica MonomialExponent[i,x] stays unevaluated for a non-monomial
    # term, so PosQ[n - <held>] is False and that term is skipped. The Python port
    # returns None instead, so skip those terms explicitly (else `n - None` raises).
    n = MonomialExponent(eager_First(u), x)
    for i in u.args:
        e = MonomialExponent(i, x)
        if e is None:
            continue
        if n is None or eager_PosQ(n - e):
            n = e

    return n

def MonomialExponent(u, x):
    # u is a monomial. MonomialExponent(u, x) returns the exponent of x in u
    a = Wild('a', exclude=[x])
    b = Wild('b', exclude=[x])
    re = u.match(a*x**b)
    if re:
        return re[b]

def eager_LinearMatchQ(u, x):
    # LinearMatchQ(u, x) returns True iff u matches patterns of the form a+b*x where a and b are free of x
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_LinearMatchQ(i, x) for i in u)
    else:
        a = Wild('a', exclude=[x])
        b = Wild('b', exclude=[x])
        re = u.match(a + b*x)
        if re:
            return True
    return False

def eager_PowerOfLinearMatchQ(u, x):
    if isinstance(u, (tuple, list, Tuple)):
        for i in u:
            if not eager_PowerOfLinearMatchQ(i, x):
                return False
        return True
    else:
        a = Wild('a', exclude=[x])
        b = Wild('b', exclude=[x, 0])
        m = Wild('m', exclude=[x, 0])
        Match = u.match((a + b*x)**m)
        if Match:
            return True
        else:
            return False

def eager_QuadraticMatchQ(u, x):
    if ListQ(u):
        return all(eager_QuadraticMatchQ(i, x) for i in u)
    pattern1 = Pattern(UtilityOperator(x_**2*WildSymbol('c', optional_value=1) + x_*WildSymbol('b', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, b, c, x: eager_FreeQ([a, b, c], x)))
    pattern2 = Pattern(UtilityOperator(x_**2*WildSymbol('c', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, c, x: eager_FreeQ([a, c], x)))
    u1 = UtilityOperator(u, x)
    return is_match(u1, pattern1) or is_match(u1, pattern2)

def CubicMatchQ(u, x):
    if isinstance(u, (tuple, list, Tuple)):
        return all(CubicMatchQ(i, x) for i in u)
    else:
        pattern1 = Pattern(UtilityOperator(x_**3*WildSymbol('d', optional_value=1) + x_**2*WildSymbol('c', optional_value=1) + x_*WildSymbol('b', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, b, c, d, x: eager_FreeQ([a, b, c, d], x)))
        pattern2 = Pattern(UtilityOperator(x_**3*WildSymbol('d', optional_value=1) + x_*WildSymbol('b', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, b, d, x: eager_FreeQ([a, b, d], x)))
        pattern3 = Pattern(UtilityOperator(x_**3*WildSymbol('d', optional_value=1) + x_**2*WildSymbol('c', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, c, d, x: eager_FreeQ([a, c, d], x)))
        pattern4 = Pattern(UtilityOperator(x_**3*WildSymbol('d', optional_value=1) + WildSymbol('a', optional_value=0), x_), _patched_custom_constraint_call(lambda a, d, x: eager_FreeQ([a, d], x)))
        u1 = UtilityOperator(u, x)
        if is_match(u1, pattern1) or is_match(u1, pattern2) or is_match(u1, pattern3) or is_match(u1, pattern4):
            return True
        else:
            return False

def eager_BinomialMatchQ(u, x):
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_BinomialMatchQ(i, x) for i in u)
    else:
        pattern = Pattern(UtilityOperator(x_**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)), x_) , _patched_custom_constraint_call(lambda a, b, n, x: eager_FreeQ([a,b,n],x)))
        u = UtilityOperator(u, x)
        return is_match(u, pattern)

def eager_TrinomialMatchQ(u, x):
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_TrinomialMatchQ(i, x) for i in u)
    else:
        pattern = Pattern(UtilityOperator(x_**WildSymbol('j', optional_value=S(1))*WildSymbol('c', optional_value=S(1)) + x_**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)), x_) , _patched_custom_constraint_call(lambda a, b, c, n, x: eager_FreeQ([a, b, c, n], x)),  _patched_custom_constraint_call(lambda j, n: ZeroQ(j-2*n) ))
        u = UtilityOperator(u, x)
        return is_match(u, pattern)

def _monomial_exponent(term, x):
    """Exponent e if ``term == coef*x**e`` with ``coef`` free of x and e free of x, else None.

    ``e`` may be symbolic; a term entirely free of x has e == 0.
    """
    coef, xpart = term.as_independent(x)
    if xpart == S.One:
        return S.Zero
    if xpart == x:
        return S.One
    if xpart.is_Pow and xpart.base == x and eager_FreeQ(xpart.exp, x):
        return xpart.exp
    return None

def eager_GeneralizedBinomialMatchQ(u, x):
    # Rubi: MatchQ[u, a_.*x^q_. + b_.*x^n_. /; FreeQ[{a,b,n,q},x]]  (verified against
    # DownValues[GeneralizedBinomialMatchQ] in Rubi 4.17.3.0). On Mathematica's
    # canonical Plus each pattern addend binds exactly one subject addend, so this is
    # purely structural: exactly two monomial addends in x. (The previous sympy Wild
    # ``.match`` implementation was both unfaithful -- numeric splits let single
    # monomials through, e.g. -3*x/2 as -x/2 + -x -- and combinatorial on sums whose
    # coefficients are large multi-symbol polynomials.)
    #
    # The exponents need NOT differ: Rubi's pattern has no q != n side condition, and
    # `a*x^2 + b*x^2` really does return True there. SymPy keeps that as a two-term Add
    # (it only collects addends differing by a numeric factor), so the case is reachable
    # and an added distinctness test made us answer False where Rubi answers True.
    # A term free of x is still rejected: `x^q_.` requires a literal x, so a bare `a`
    # cannot bind it -- which is what the exponent-0 test below expresses.
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_GeneralizedBinomialMatchQ(i, x) for i in u)
    if not u.is_Add or len(u.args) != 2:
        return False
    exps = [_monomial_exponent(t, x) for t in u.args]
    return not any(e is None or e == 0 for e in exps)

def eager_GeneralizedTrinomialMatchQ(u, x):
    # Mathematica: MatchQ[u, a_.*x^q_. + b_.*x^n_. + c_.*x^r_.] with all wilds
    # free of x and nonzero, and r == 2*n - q. Structural (see the binomial
    # variant above): exactly three monomial addends whose nonzero exponents
    # admit a labeling (q, n, r) with r == 2*n - q, i.e. an arithmetic
    # progression when the exponents are distinct.
    if isinstance(u, (tuple, list, Tuple)):
        return all(eager_GeneralizedTrinomialMatchQ(i, x) for i in u)
    if not u.is_Add or len(u.args) != 3:
        return False
    exps = [_monomial_exponent(t, x) for t in u.args]
    if any(e is None or e == 0 for e in exps):
        return False
    from itertools import permutations as _permutations
    for q, n, r in _permutations(exps):
        if (r - (2*n - q)).is_zero and n != 0 and 2*n - q != 0:
            return True
    return False

def QuotientOfLinearsMatchQ(u, x):
    if isinstance(u, (tuple, list, Tuple)):
        return all(QuotientOfLinearsMatchQ(i, x) for i in u)
    else:
        a = Wild('a', exclude=[x])
        b = Wild('b', exclude=[x])
        d = Wild('d', exclude=[x])
        c = Wild('c', exclude=[x])
        # Rubi: MatchQ[u, e_.*((a_. + b_. x)/(c_. + d_. x)) /; FreeQ[{a,b,c,d,e}, x]]
        # -- `e` is in the FreeQ list, so the outer factor must be FREE OF x. Without
        # exclude=[x] the Wild absorbed x-dependent factors and the predicate answered
        # True for things that are not a quotient of linears at all:
        #   x*(3 + 4x)/(2 + 4x)        -> matched with e = x        (Rubi: False)
        #   (1 + x)(3 + 4x^2)/(2 + 4x) -> matched with e = 1 + x    (Rubi: False)
        # A wrongly-True match here lets the quotient-of-linears rules fire on
        # integrands they do not apply to.
        e = Wild('e', exclude=[x])
        Match = u.match(e*(a + b*x)/(c + d*x))
        # `b` and `d` may not be 0. In `a_. + b_. x` the `b_. x` addend must be
        # structurally PRESENT -- Mathematica's Optional supplies a default coefficient,
        # never a missing term -- whereas a SymPy Wild happily binds b -> 0 and matches
        # a CONSTANT numerator. Without this, `1/(2+4x)` and `1/x` reported True where
        # Rubi reports False. (`a` and `c` MAY be 0: Rubi matches x/(3+4x) with a = 0
        # and (1+2x)/x with c = 0.)
        if Match and len(Match) == 5 and Match[b] != 0 and Match[d] != 0:
            return True
        else:
            return False

def PolynomialTermQ(u, x):
    # Rubi: FreeQ[u,x] || MatchQ[u, a_.*x^n_. /; FreeQ[a,x] && IntegerQ[n] && n>0].
    # A constant (free of x) IS a polynomial term; the missing FreeQ clause used to
    # push it into NonpolynomialTerms.
    if eager_FreeQ(u, x):
        return True
    a = Wild('a', exclude=[x])
    n = Wild('n', exclude=[x])
    Match = u.match(a*x**n)
    if Match and eager_IntegerQ(Match[n]) and Greater(Match[n], S(0)):
        return True
    else:
        return False

def PolynomialTerms(u, x):
    s = 0
    for i in u.args:
        if PolynomialTermQ(i, x):
            s = s + i
    return s

def NonpolynomialTerms(u, x):
    s = 0
    for i in u.args:
        if not PolynomialTermQ(i, x):
            s = s + i
    return s

def PseudoBinomialParts(u, x):
    if eager_PolynomialQ(u, x) and Greater(eager_Expon(u, x), S(2)):
        n = eager_Expon(u, x)
        d = eager_Rt(eager_Coefficient(u, x, n), n)
        c =  d**(-n + S(1))*eager_Coefficient(u, x, n + S(-1))/n
        a = eager_Simplify(u - (c + d*x)**n)
        if NonzeroQ(a) and eager_FreeQ(a, x):
            return [a, S(1), c, d, n]
        else:
            return False
    else:
        return False

def eager_NormalizePseudoBinomial(u, x):
    lst = PseudoBinomialParts(u, x)
    if lst:
        return (lst[0] + lst[1]*(lst[2] + lst[3]*x)**lst[4])

def eager_PseudoBinomialPairQ(u, v, x):
    lst1 = PseudoBinomialParts(u, x)
    if eager_AtomQ(lst1):
        return False
    else:
        lst2 = PseudoBinomialParts(v, x)
        if eager_AtomQ(lst2):
            return False
        else:
            return Drop(lst1, 2) == Drop(lst2, 2)

def PseudoBinomialQ(u, x):
    lst = PseudoBinomialParts(u, x)
    if lst:
        return True
    else:
        return False

def PolynomialGCD(f, g):
    return gcd(f, g)

def eager_PolyGCD(u, v, x):
    # (* u and v are polynomials in x. *)
    # (* PolyGCD[u,v,x] returns the factors of the gcd of u and v dependent on x. *)
    return eager_NonfreeFactors(PolynomialGCD(u, v), x)

def AlgebraicFunctionFactors(u, x, flag=False):
    # (* AlgebraicFunctionFactors[u,x] returns the product of the factors of u that are algebraic functions of x. *)
    if eager_ProductQ(u):
        result = 1
        for i in u.args:
            if eager_AlgebraicFunctionQ(i, x, flag):
                result *= i
        return result
    if eager_AlgebraicFunctionQ(u, x, flag):
        return u
    return 1

def NonalgebraicFunctionFactors(u, x):
    """
    NonalgebraicFunctionFactors[u,x] returns the product of the factors of u that are not algebraic functions of x.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import NonalgebraicFunctionFactors
    >>> from sympy.abc import x
    >>> from sympy import sin
    >>> NonalgebraicFunctionFactors(sin(x), x)
    sin(x)
    >>> NonalgebraicFunctionFactors(x, x)
    1

    """
    if eager_ProductQ(u):
        result = 1
        for i in u.args:
            if not eager_AlgebraicFunctionQ(i, x):
                result *= i
        return result
    if eager_AlgebraicFunctionQ(u, x):
        return 1
    return u

def QuotientOfLinearsP(u, x):
    if eager_LinearQ(u, x):
        return True
    elif eager_SumQ(u):
        if eager_FreeQ(u.args[0], x):
            return QuotientOfLinearsP(eager_Rest(u), x)
    elif eager_LinearQ(eager_Numerator(u), x) and eager_LinearQ(eager_Denominator(u), x):
        return True
    elif eager_ProductQ(u):
        if eager_FreeQ(eager_First(u), x):
            return QuotientOfLinearsP(eager_Rest(u), x)
    elif eager_Numerator(u) == 1 and eager_PowerQ(u):
        return QuotientOfLinearsP(eager_Denominator(u), x)
    return u == x or eager_FreeQ(u, x)

def eager_QuotientOfLinearsParts(u, x):
    # If u is equivalent to an expression of the form (a+b*x)/(c+d*x), QuotientOfLinearsParts[u,x]
    #   returns the list {a, b, c, d}.
    if eager_LinearQ(u, x):
        return [eager_Coefficient(u, x, 0), eager_Coefficient(u, x, 1), 1, 0]
    elif eager_PowerQ(u):
        if eager_Numerator(u) == 1:
            u = eager_Denominator(u)
            r = eager_QuotientOfLinearsParts(u, x)
            return [r[2], r[3], r[0], r[1]]
    elif eager_SumQ(u):
        a = eager_First(u)
        if eager_FreeQ(a, x):
            u = eager_Rest(u)
            r = eager_QuotientOfLinearsParts(u, x)
            return [r[0] + a*r[2], r[1] + a*r[3], r[2], r[3]]
    elif eager_ProductQ(u):
        a = eager_First(u)
        if eager_FreeQ(a, x):
            r = eager_QuotientOfLinearsParts(eager_Rest(u), x)
            return [a*r[0], a*r[1], r[2], r[3]]
        a = eager_Numerator(u)
        d = eager_Denominator(u)
        if eager_LinearQ(a, x) and eager_LinearQ(d, x):
            return [eager_Coefficient(a, x, 0), eager_Coefficient(a, x, 1), eager_Coefficient(d, x, 0), eager_Coefficient(d, x, 1)]
    elif u == x:
        return [0, 1, 1, 0]
    elif eager_FreeQ(u, x):
        return [u, 0, 1, 0]
    return [u, 0, 1, 0]

def eager_QuotientOfLinearsQ(u, x):
    # (*QuotientOfLinearsQ[u,x] returns True iff u is equivalent to an expression of the form (a+b x)/(c+d x) where b!=0 and d!=0.*)
    if ListQ(u):
        for i in u:
            if not eager_QuotientOfLinearsQ(i, x):
                return False
        return True
    q = eager_QuotientOfLinearsParts(u, x)
    return QuotientOfLinearsP(u, x) and NonzeroQ(q[1]) and NonzeroQ(q[3])

def Flatten(l):
    return flatten(l)

def Sort(u, r=False):
    return sorted(u, key=lambda x: x.sort_key(), reverse=r)

# (*Definition: A number is absurd if it is a rational number, a positive rational number raised to a fractional power, or a product of absurd numbers.*)
def AbsurdNumberQ(u):
    # (* AbsurdNumberQ[u] returns True if u is an absurd number, else it returns False. *)
    if eager_PowerQ(u):
        v = u.exp
        u = u.base
        return eager_RationalQ(u) and u > 0 and eager_FractionQ(v)
    elif eager_ProductQ(u):
        return all(AbsurdNumberQ(i) for i in u.args)
    return eager_RationalQ(u)

def AbsurdNumberFactors(u):
    # (* AbsurdNumberFactors[u] returns the product of the factors of u that are absurd numbers. *)
    if AbsurdNumberQ(u):
        return u
    elif eager_ProductQ(u):
        result = S(1)
        for i in u.args:
            if AbsurdNumberQ(i):
                result *= i
        return result
    return NumericFactor(u)

def NonabsurdNumberFactors(u):
    # (* NonabsurdNumberFactors[u] returns the product of the factors of u that are not absurd numbers. *)
    if AbsurdNumberQ(u):
        return S(1)
    elif eager_ProductQ(u):
        result = 1
        for i in u.args:
            result *= NonabsurdNumberFactors(i)
        return result
    return NonnumericFactors(u)

def SumSimplerAuxQ(u, v):
    if eager_SumQ(v):
        return (eager_RationalQ(eager_First(v)) or SumSimplerAuxQ(u,eager_First(v))) and (eager_RationalQ(eager_Rest(v)) or SumSimplerAuxQ(u,eager_Rest(v)))
    elif eager_SumQ(u):
        return SumSimplerAuxQ(eager_First(u), v) or SumSimplerAuxQ(eager_Rest(u), v)
    else:
        return v!=0 and NonnumericFactors(u)==NonnumericFactors(v) and (NumericFactor(u)/NumericFactor(v)<-1/2 or NumericFactor(u)/NumericFactor(v)==-1/2 and NumericFactor(u)<0)

def Prepend(l1, l2):
    """Mathematica's ``Prepend[list, elem]`` NESTS the new element, whatever it is:
    ``Prepend[{1,2,3}, {4,5}]`` is ``{{4,5},1,2,3}``, not ``{4,5,1,2,3}``.

    This used to CONCATENATE when ``l2`` was a list, which silently spliced a
    ``[base, exponent]`` pair into its container -- the defect behind the old
    ``CombineExponents`` breakage. The two in-port callers had been written around the
    splicing behaviour (passing ``[scalar]`` instead of ``scalar``) and are un-wrapped
    to match. Rubi's only list-passing call site is CombineExponents, which this port
    implements with plain list operations, so nothing else depends on the old shape.
    """
    return [l2] + list(l1)

def Drop(lst, n):
    if isinstance(lst, (tuple, list)):
        if isinstance(n, (tuple, list)):
            lst = lst[:(n[0]-1)] + lst[n[1]:]
        elif n > 0:
            lst = lst[n:]
        elif n < 0:
            lst = lst[:-n]
        else:
            return lst
        return lst
    return lst.func(*[i for i in Drop(list(lst.args), n)])

def CombineExponents(lst):
    """Rubi ``CombineExponents``: merge adjacent equal bases in a base-sorted
    (base, exponent) list by summing their exponents.

    Uses plain list operations rather than the Rubi ``Prepend``/``Rest`` helpers.
    ``Prepend(l1, l2)`` CONCATENATES when l2 is itself a list, so prepending a
    ``[base, exp]`` pair spliced its two elements into the result --
    ``Prepend([[3, 1/2]], [2, 1])`` gave ``[2, 1, [3, 1/2]]`` instead of
    ``[[2, 1], [3, 1/2]]`` -- and the next recursion then subscripted an int.
    The only caller (FactorAbsurdNumber) never reached this path before, and
    ``test_CombineExponents`` was a bare ``assert True``, so it went unnoticed.
    """
    lst = list(lst)
    if len(lst) < 2:
        return lst
    if lst[0][0] == lst[1][0]:
        merged = [lst[0][0], lst[0][1] + lst[1][1]]
        return CombineExponents([merged] + lst[2:])
    return [lst[0]] + CombineExponents(lst[1:])

def FactorInteger(n, l=None):
    """Mathematica ``FactorInteger`` — prime factorisation as (prime, exponent) pairs.

    Pairs are SymPy Integers, not Python ints. ``factorint``/``factorrat`` hand back
    plain ints, and a Python ``int ** negative int`` evaluates to a FLOAT: the
    reciprocal exponents that a rational produces (FactorInteger[3/4] is
    {{2,-2},{3,1}}) then turned ``2**-2`` into ``0.25``. That float propagated out
    through AbsurdNumberGCD into CommonFactors and ContentFactor, so an exact
    rational content came back as ``0.25*(2.0*x + 3.0)``. Mathematica's arithmetic
    here is exact.
    """
    if isinstance(n, (int, Integer)):
        pairs = factorint(n, limit=l).items()
    else:
        pairs = factorrat(n, limit=l).items()
    return sorted((Integer(base), Integer(exponent)) for base, exponent in pairs)

def FactorAbsurdNumber(m):
    # (* m must be an absurd number.  FactorAbsurdNumber[m] returns the prime factorization of m *)
    # (* as list of base-degree pairs where the bases are prime numbers and the degrees are rational. *)
    if eager_RationalQ(m):
        return FactorInteger(m)
    elif eager_PowerQ(m):
        # Rubi: Map[Function[{#[[1]], #[[2]]*m[[2]]}], FactorInteger[m[[1]]]]
        # -- MAP over the factor list, scaling each prime's exponent. This used to read
        # `r = FactorInteger(m.base); [r[0], r[1]*m.exp]`, treating that list of
        # (prime, exponent) pairs as ONE pair: wrong shape in general, and an
        # IndexError whenever the base had a single prime factor (Sqrt[3] crashed).
        return [(b, e*m.exp) for b, e in FactorInteger(m.base)]

    # Rubi: CombineExponents[Sort[Flatten[Map[FactorAbsurdNumber, Apply[List, m]], 1],
    #                             Function[i1[[1]] < i2[[1]]]]]
    # The product branch was never implemented -- it returned [(m, 1)], leaving the whole
    # product as an opaque "base". AbsurdNumberGCD compares bases, so 2*Sqrt[3] and
    # 4*Sqrt[3] looked coprime and their gcd came out 1 instead of 2*Sqrt[3].
    # Pairs are normalised to LISTS here: CombineExponents/Prepend build and concatenate
    # lists (Mathematica {base, exp}), and mixing in FactorInteger's tuples makes
    # `Prepend` raise "can only concatenate tuple (not list) to tuple".
    factors = []
    for factor in m.args:
        factors.extend([list(pair) for pair in FactorAbsurdNumber(factor)])
    return CombineExponents(sorted(factors, key=lambda pair: pair[0]))

def eager_SubstForInverseFunction(*args):
    """
    SubstForInverseFunction(u, v, w, x) returns u with subexpressions equal to v replaced by x and x replaced by w.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import eager_SubstForInverseFunction as SubstForInverseFunction
    >>> from sympy.abc import x, a, b
    >>> SubstForInverseFunction(a, a, b, x)
    a
    >>> SubstForInverseFunction(x**a, x**a, b, x)
    x
    >>> SubstForInverseFunction(a*x**a, a, b, x)
    a*b**a

    """
    if len(args) == 3:
        u, v, x = args[0], args[1], args[2]
        # Rubi: SubstForInverseFunction[u,v,x] :=
        #   SubstForInverseFunction[u, v,
        #     (-Coefficient[v[[1]],x,0] + InverseFunction[Head[v]][x]) / Coefficient[v[[1]],x,1], x]
        # i.e. v is g[a+b*x]; solve y == g[a+b*x] for x, giving (g^-1[y] - a)/b.
        inverse = eager_InverseFunction(eager_Head(v))
        if inverse is None:
            return False
        a = eager_Coefficient(v.args[0], x, 0)
        b = eager_Coefficient(v.args[0], x, 1)
        return eager_SubstForInverseFunction(u, v, (-a + inverse(x))/b, x)
    elif len(args) == 4:
        u, v, w, x = args[0], args[1], args[2], args[3]
        if eager_AtomQ(u):
            if u == x:
                return w
            return u
        elif eager_Head(u) == eager_Head(v) and ZeroQ(u.args[0] - v.args[0]):
            return x
        res = [eager_SubstForInverseFunction(i, v, w, x) for i in u.args]
        return u.func(*res)

_INVERSE_FUNCTION_PAIRS = [
    (sin, asin), (cos, acos), (tan, atan), (cot, acot), (sec, asec), (csc, acsc),
    (sinh, asinh), (cosh, acosh), (tanh, atanh), (coth, acoth), (sech, asech), (csch, acsch),
]

_INVERSE_FUNCTION_MAP = {}
for _f, _g in _INVERSE_FUNCTION_PAIRS:
    _INVERSE_FUNCTION_MAP[_f] = _g
    _INVERSE_FUNCTION_MAP[_g] = _f
_INVERSE_FUNCTION_MAP[log] = exp
_INVERSE_FUNCTION_MAP[exp] = log


def eager_InverseFunction(head):
    """Mathematica ``InverseFunction[head]`` for the heads Rubi inverts.

    Returns the inverse function CLASS (so it can be applied), or None when there is
    no entry -- Mathematica would return an ``InverseFunction[...]`` object, but every
    Rubi caller only ever reaches this with an elementary invertible head.
    """
    from sympy_wolfram.functions_eager import head_to_class
    cls = head_to_class(head)
    if cls is None:
        cls = head
    return _INVERSE_FUNCTION_MAP.get(cls)


def eager_SubstPower(Fx, x, n):
    """Rubi ``SubstPower[Fx, x, n]`` (IntegrationUtilityFunctions.m) -- replace every
    ``x`` in *Fx* by ``x^n``.

    Rubi::

        SubstPower[Fx_,x_Symbol,n_Integer] :=
          If[AtomQ[Fx], If[Fx===x, x^n, Fx],
          If[PowerQ[Fx] && Fx[[1]]===x && FreeQ[Fx[[2]],x], x^(n*Fx[[2]]),
          Map[Function[SubstPower[#,x,n]], Fx]]]

    So ``x -> x^n``, ``x^p -> x^(n*p)`` for an x-free ``p``, and anything else is
    rebuilt from its mapped parts (``Sin[x] + x^2 -> Sin[x^2] + x^4`` for n=2).
    """
    Fx = S(Fx)
    if eager_AtomQ(Fx):
        return x**n if Fx == x else Fx
    if eager_PowerQ(Fx) and Fx.base == x and eager_FreeQ(Fx.exp, x):
        return x**(n*Fx.exp)
    return Fx.func(*[eager_SubstPower(arg, x, n) for arg in Fx.args])


def SubstForFractionalPower(u, v, n, w, x):
    # (* SubstForFractionalPower[u,v,n,w,x] returns u with subexpressions equal to v^(m/n) replaced
    # by x^m and x replaced by w. *)
    if eager_AtomQ(u):
        if u == x:
            return w
        return u
    elif eager_FractionalPowerQ(u):
        if ZeroQ(u.base - v):
            return x**(n*u.exp)
    res = [SubstForFractionalPower(i, v, n, w, x) for i in u.args]
    return u.func(*res)

def eager_SubstForFractionalPowerOfQuotientOfLinears(u, x):
    # (* If u has a subexpression of the form ((a+b*x)/(c+d*x))^(m/n) where m and n>1 are integers,
    # SubstForFractionalPowerOfQuotientOfLinears[u,x] returns the list {v,n,(a+b*x)/(c+d*x),b*c-a*d} where v is u
    # with subexpressions of the form ((a+b*x)/(c+d*x))^(m/n) replaced by x^m and x replaced
    lst = FractionalPowerOfQuotientOfLinears(u, 1, False, x)
    if eager_AtomQ(lst) or eager_AtomQ(lst[1]):
        return False
    n = lst[0]
    tmp = lst[1]
    lst = eager_QuotientOfLinearsParts(tmp, x)
    a, b, c, d = lst[0], lst[1], lst[2], lst[3]
    if ZeroQ(d):
        return False
    lst = eager_Simplify(x**(n - 1)*SubstForFractionalPower(u, tmp, n, (-a + c*x**n)/(b - d*x**n), x)/(b - d*x**n)**2)
    return [eager_NonfreeFactors(lst, x), n, tmp, eager_FreeFactors(lst, x)*(b*c - a*d)]

def FractionalPowerOfQuotientOfLinears(u, n, v, x):
    # (* If u has a subexpression of the form ((a+b*x)/(c+d*x))^(m/n),
    # FractionalPowerOfQuotientOfLinears[u,1,False,x] returns {n,(a+b*x)/(c+d*x)}; else it returns False. *)
    if eager_AtomQ(u) or eager_FreeQ(u, x):
        return [n, v]
    elif CalculusQ(u):
        return False
    elif eager_FractionalPowerQ(u):
        if eager_QuotientOfLinearsQ(u.base, x) and eager_Not(eager_LinearQ(u.base, x)) and (eager_FalseQ(v) or ZeroQ(u.base - v)):
            return [LCM(eager_Denominator(u.exp), n), u.base]
    lst = [n, v]
    for i in u.args:
        lst = FractionalPowerOfQuotientOfLinears(i, lst[0], lst[1],x)
        if eager_AtomQ(lst):
            return False
    return lst

def eager_SubstForFractionalPowerQ(u, v, x):
    # (* If the substitution x=v^(1/n) will not complicate algebraic subexpressions of u,
    # SubstForFractionalPowerQ[u,v,x] returns True; else it returns False. *)
    if eager_AtomQ(u) or eager_FreeQ(u, x):
        return True
    elif eager_FractionalPowerQ(u):
        return SubstForFractionalPowerAuxQ(u, v, x)
    return all(eager_SubstForFractionalPowerQ(i, v, x) for i in u.args)

def SubstForFractionalPowerAuxQ(u, v, x):
    if eager_AtomQ(u):
        return False
    elif eager_FractionalPowerQ(u):
        if ZeroQ(u.base - v):
            return True
    return any(SubstForFractionalPowerAuxQ(i, v, x) for i in u.args)

def FractionalPowerOfSquareQ(u):
    # (* If a subexpression of u is of the form ((v+w)^2)^n where n is a fraction, *)
    # (* FractionalPowerOfSquareQ[u] returns (v+w)^2; else it returns False. *)
    if eager_AtomQ(u):
        return False
    elif eager_FractionalPowerQ(u):
        a_ = Wild('a', exclude=[0])
        b_ = Wild('b', exclude=[0])
        c_ = Wild('c', exclude=[0])
        match = u.base.match(a_*(b_ + c_)**(S(2)))
        if match:
            keys = [a_, b_, c_]
            if len(keys) == len(match):
                a, b, c = tuple(match[i] for i in keys)
                if eager_NonsumQ(a):
                    return (b + c)**S(2)
    for i in u.args:
        tmp = FractionalPowerOfSquareQ(i)
        if eager_Not(eager_FalseQ(tmp)):
            return tmp
    return False

def FractionalPowerSubexpressionQ(u, v, w):
    # (* If a subexpression of u is of the form w^n where n is a fraction but not equal to v, *)
    # (* FractionalPowerSubexpressionQ[u,v,w] returns True; else it returns False. *)
    if eager_AtomQ(u):
        return False
    elif eager_FractionalPowerQ(u):
        if eager_PositiveQ(u.base/w):
            return eager_Not(u.base == v) and eager_LeafCount(w) < 3*eager_LeafCount(v)
    for i in u.args:
        if FractionalPowerSubexpressionQ(i, v, w):
            return True
    return False

def eager_Apply(f, lst):
    return f(*lst)

def FactorNumericGcd(u):
    # (* FactorNumericGcd[u] returns u with the gcd of the numeric coefficients of terms of sums factored out. *)
    if eager_PowerQ(u):
        if eager_RationalQ(u.exp):
            return FactorNumericGcd(u.base)**u.exp
    elif eager_ProductQ(u):
        res = [FactorNumericGcd(i) for i in u.args]
        return Mul(*res)
    elif eager_SumQ(u):
        # star-unpack: passing the LIST as one argument hit eager_GCD's len==1
        # branch and always returned 1, so numeric content was never factored out.
        g = eager_GCD(*[NumericFactor(i) for i in u.args])
        r = Add(*[i/g for i in u.args])
        # `g*r` would let SymPy distribute the number straight back over the sum,
        # undoing the very factorisation this function exists to perform:
        # FactorNumericGcd[2 x + 4] came back as 4 + 2*x instead of Rubi's 2*(2 + x).
        return _content_times(g, r)
    return u

def MergeableFactorQ(bas, deg, v):
    # (* MergeableFactorQ[bas,deg,v] returns True iff bas equals the base of a factor of v or bas is a factor of every term of v. *)
    if bas == v:
        return eager_RationalQ(deg + S(1)) and (deg + 1>=0 or eager_RationalQ(deg) and deg>0)
    elif eager_PowerQ(v):
        if bas == v.base:
            return eager_RationalQ(deg+v.exp) and (deg+v.exp>=0 or eager_RationalQ(deg) and deg>0)
        return eager_SumQ(v.base) and eager_IntegerQ(v.exp) and (eager_Not(eager_IntegerQ(deg) or eager_IntegerQ(deg/v.exp))) and MergeableFactorQ(bas, deg/v.exp, v.base)
    elif eager_ProductQ(v):
        return MergeableFactorQ(bas, deg, eager_First(v)) or MergeableFactorQ(bas, deg, eager_Rest(v))
    return eager_SumQ(v) and MergeableFactorQ(bas, deg, eager_First(v)) and MergeableFactorQ(bas, deg, eager_Rest(v))

def MergeFactor(bas, deg, v):
    # (* If MergeableFactorQ[bas,deg,v], MergeFactor[bas,deg,v] return the product of bas^deg and v,
    # but with bas^deg merged into the factor of v whose base equals bas. *)
    if bas == v:
        return bas**(deg + 1)
    elif eager_PowerQ(v):
        if bas == v.base:
            return bas**(deg + v.exp)
        return MergeFactor(bas, deg/v.exp, v.base**v.exp)
    elif eager_ProductQ(v):
        if MergeableFactorQ(bas, deg, eager_First(v)):
            return MergeFactor(bas, deg, eager_First(v))*eager_Rest(v)
        return eager_First(v)*MergeFactor(bas, deg, eager_Rest(v))
    return MergeFactor(bas, deg, eager_First(v)) + MergeFactor(bas, deg, eager_Rest(v))

def MergeFactors(u, v):
    # (* MergeFactors[u,v] returns the product of u and v, but with the mergeable factors of u merged into v. *)
    if eager_ProductQ(u):
        return MergeFactors(eager_Rest(u), MergeFactors(eager_First(u), v))
    elif eager_PowerQ(u):
        if MergeableFactorQ(u.base, u.exp, v):
            return MergeFactor(u.base, u.exp, v)
        elif eager_RationalQ(u.exp) and u.exp < -1 and MergeableFactorQ(u.base, -S(1), v):
            return MergeFactors(u.base**(u.exp + 1), MergeFactor(u.base, -S(1), v))
        return u*v
    elif MergeableFactorQ(u, S(1), v):
        return MergeFactor(u, S(1), v)
    return u*v

def eager_TrigSimplifyQ(u):
    # (* TrigSimplifyQ[u] returns True if TrigSimplify[u] actually simplifies u; else False. *)
    return eager_ActivateTrig(u) != eager_TrigSimplify(u)

def eager_TrigSimplify(u):
    # (* TrigSimplify[u] returns a bottom-up trig simplification of u. *)
    return eager_ActivateTrig(TrigSimplifyRecur(u))

def TrigSimplifyRecur(u):
    if eager_AtomQ(u):
        return u
    return TrigSimplifyAux(u.func(*[TrigSimplifyRecur(i) for i in u.args]))

def Order(expr1, expr2):
    if expr1 == expr2:
        return 0
    elif expr1.sort_key() > expr2.sort_key():
        return -1
    return 1

def FactorOrder(u, v):
    if u == 1:
        if v == 1:
            return 0
        return -1
    elif v == 1:
        return 1
    return Order(u, v)

def Smallest(num1, num2=None):
    """Rubi ``Smallest`` — the value CLOSEST TO ZERO, not the minimum::

        Smallest[num1_, num2_] :=
          If[num1 > 0, If[num2 > 0, Min[num1, num2], 0],
                       If[num2 > 0, 0, Max[num1, num2]]]

    So opposite signs give 0, and two negatives give the MAXIMUM (`Smallest[-1,-2]`
    is -1, not -2). This was a plain ``Min``.

    It matters: ``CommonFactors`` uses it to choose the common exponent to extract
    (``num = Smallest[lst4]; common = common*base^num``). Picking -2 where Rubi picks
    -1 extracts the WRONG common power, so the residuals do not shrink -- expressions
    keep growing instead of being factored down.
    """
    if num2 is None:
        lst = num1
        num = lst[0]
        for i in eager_Rest(lst):
            num = Smallest(num, i)
        return num
    try:
        if num1 > 0:
            return Min(num1, num2) if num2 > 0 else S(0)
        return S(0) if num2 > 0 else Max(num1, num2)
    except TypeError:          # non-comparable (symbolic) -> keep the old behaviour
        return Min(num1, num2)

def OrderedQ(l):
    return l == Sort(l)

def MinimumDegree(deg1, deg2):
    if eager_RationalQ(deg1):
        if eager_RationalQ(deg2):
            return Min(deg1, deg2)
        return deg1
    elif eager_RationalQ(deg2):
        return deg2

    deg = eager_Simplify(deg1- deg2)

    if eager_RationalQ(deg):
        if deg > 0:
            return deg2
        return deg1
    elif OrderedQ([deg1, deg2]):
        return deg1
    return deg2

def PositiveFactors(u):
    # (* PositiveFactors[u] returns the positive factors of u *)
    if ZeroQ(u):
        return S(1)
    elif eager_RationalQ(u):
        return Abs(u)
    elif eager_PositiveQ(u):
        return u
    elif eager_ProductQ(u):
        res = 1
        for i in u.args:
            res *= PositiveFactors(i)
        return res
    return 1

def eager_Sign(u):
    return sign(u)

def NonpositiveFactors(u):
    # (* NonpositiveFactors[u] returns the nonpositive factors of u *)
    if ZeroQ(u):
        return u
    elif eager_RationalQ(u):
        return eager_Sign(u)
    elif eager_PositiveQ(u):
        return S(1)
    elif eager_ProductQ(u):
        res = S(1)
        for i in u.args:
            res *= NonpositiveFactors(i)
        return res
    return u

def PolynomialInAuxQ(u, v, x):
    if u == v:
        return True
    elif eager_AtomQ(u):
        return u != x
    elif eager_PowerQ(u):
        if eager_PowerQ(v):
            if u.base == v.base:
                return PositiveIntegerQ(u.exp/v.exp)
        return PositiveIntegerQ(u.exp) and PolynomialInAuxQ(u.base, v, x)
    elif eager_SumQ(u) or eager_ProductQ(u):
        for i in u.args:
            if eager_Not(PolynomialInAuxQ(i, v, x)):
                return False
        return True
    return False

def eager_PolynomialInQ(u, v, x):
    """
    If u is a polynomial in v(x), PolynomialInQ(u, v, x) returns True, else it returns False.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import PolynomialInQ
    >>> from sympy.abc import x
    >>> from sympy import log, S
    >>> PolynomialInQ(S(1), log(x), x)
    True
    >>> PolynomialInQ(log(x), log(x), x)
    True
    >>> PolynomialInQ(1 + log(x)**2, log(x), x)
    True

    """
    return PolynomialInAuxQ(u, eager_NonfreeFactors(NonfreeTerms(v, x), x), x)

def ExponentInAux(u, v, x):
    if u == v:
        return S(1)
    elif eager_AtomQ(u):
        return S(0)
    elif eager_PowerQ(u):
        if eager_PowerQ(v):
            if u.base == v.base:
                return u.exp/v.exp
        return u.exp*ExponentInAux(u.base, v, x)
    elif eager_ProductQ(u):
        return Add(*[ExponentInAux(i, v, x) for i in u.args])
    return Max(*[ExponentInAux(i, v, x) for i in u.args])

def ExponentIn(u, v, x):
    return ExponentInAux(u, eager_NonfreeFactors(NonfreeTerms(v, x), x), x)

def PolynomialInSubstAux(u, v, x):
    if u == v:
        return x
    elif eager_AtomQ(u):
        return u
    elif eager_PowerQ(u):
        if eager_PowerQ(v):
            if u.base == v.base:
                return x**(u.exp/v.exp)
        return PolynomialInSubstAux(u.base, v, x)**u.exp
    return u.func(*[PolynomialInSubstAux(i, v, x) for i in u.args])

def eager_PolynomialInSubst(u, v, x):
    # If u is a polynomial in v[x], PolynomialInSubst[u,v,x] returns the polynomial u in x.
    w = NonfreeTerms(v, x)
    return eager_ReplaceAll(PolynomialInSubstAux(u, eager_NonfreeFactors(w, x), x), {x: x - FreeTerms(v, x)/eager_FreeFactors(w, x)})

def eager_Distrib(u, v):
    # Distrib[u,v] returns the sum of u times each term of v.
    if eager_SumQ(v):
        return Add(*[u*i for i in v.args])
    return u*v

def DistributeDegree(u, m):
    # DistributeDegree[u,m] returns the product of the factors of u each raised to the mth degree.
    if eager_AtomQ(u):
        return u**m
    elif eager_PowerQ(u):
        return u.base**(u.exp*m)
    elif eager_ProductQ(u):
        return Mul(*[DistributeDegree(i, m) for i in u.args])
    return u**m

def FunctionOfPower(*args):
    """
    FunctionOfPower[u,x] returns the gcd of the integer degrees of x in u.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import FunctionOfPower
    >>> from sympy.abc import x
    >>> FunctionOfPower(x, x)
    1
    >>> FunctionOfPower(x**3, x)
    3

    """
    if len(args) == 2:
        return FunctionOfPower(args[0], None, args[1])

    u, n, x = args

    if eager_FreeQ(u, x):
        return n
    elif u == x:
        return S(1)
    elif eager_PowerQ(u):
        if u.base == x and eager_IntegerQ(u.exp):
            if n is None:
                return u.exp
            return eager_GCD(n, u.exp)
    tmp = n
    for i in u.args:
        tmp = FunctionOfPower(i, tmp, x)
    return tmp

def DivideDegreesOfFactors(u, n):
    """
    DivideDegreesOfFactors[u,n] returns the product of the base of the factors of u raised to the degree of the factors divided by n.

    Examples
    ========

    >>> from sympy import S
    >>> from rubi_rules.utils.utility_functions import DivideDegreesOfFactors
    >>> from sympy.abc import a, b
    >>> DivideDegreesOfFactors(a**b, S(3))
    a**(b/3)

    """
    if eager_ProductQ(u):
        return Mul(*[LeadBase(i)**(LeadDegree(i)/n) for i in u.args])
    return LeadBase(u)**(LeadDegree(u)/n)

def MonomialFactor(u, x):
    # MonomialFactor[u,x] returns the list {n,v} where x^n*v==u and n is free of x.
    if eager_AtomQ(u):
        if u == x:
            return [S(1), S(1)]
        return [S(0), u]
    elif eager_PowerQ(u):
        if eager_IntegerQ(u.exp):
            lst = MonomialFactor(u.base, x)
            return [lst[0]*u.exp, lst[1]**u.exp]
        elif u.base == x and eager_FreeQ(u.exp, x):
            return [u.exp, S(1)]
        return [S(0), u]
    elif eager_ProductQ(u):
        lst1 = MonomialFactor(eager_First(u), x)
        lst2 = MonomialFactor(eager_Rest(u), x)
        return [lst1[0] + lst2[0], lst1[1]*lst2[1]]
    elif eager_SumQ(u):
        lst = [MonomialFactor(i, x) for i in u.args]
        deg = lst[0][0]
        for i in eager_Rest(lst):
            deg = MinimumDegree(deg, i[0])
        if ZeroQ(deg) or eager_RationalQ(deg) and deg < 0:
            return [S(0), u]
        return [deg, Add(*[x**(i[0] - deg)*i[1] for i in lst])]
    return [S(0), u]

def eager_FullSimplify(expr):
    return eager_Simplify(expr)

def FunctionOfLinearSubst(u, a, b, x):
    if eager_FreeQ(u, x):
        return u
    elif eager_LinearQ(u, x):
        tmp = eager_Coefficient(u, x, 1)
        if tmp == b:
            tmp = S(1)
        else:
            tmp = tmp/b
        return eager_Coefficient(u, x, S(0)) - a*tmp + tmp*x
    elif eager_PowerQ(u):
        if eager_FreeQ(u.base, x):
            return E**(eager_FullSimplify(FunctionOfLinearSubst(Log(u.base)*u.exp, a, b, x)))
    lst = MonomialFactor(u, x)
    if eager_ProductQ(u) and NonzeroQ(lst[0]):
        if eager_RationalQ(LeadFactor(lst[1])) and LeadFactor(lst[1]) < 0:
            return  -FunctionOfLinearSubst(DivideDegreesOfFactors(-lst[1], lst[0])*x, a, b, x)**lst[0]
        return FunctionOfLinearSubst(DivideDegreesOfFactors(lst[1], lst[0])*x, a, b, x)**lst[0]
    return u.func(*[FunctionOfLinearSubst(i, a, b, x) for i in u.args])


def eager_FunctionOfLinear(*args):
    # (* If u (x) is equivalent to an expression of the form f (a+b*x) and not the case that a==0 and
    # b==1, FunctionOfLinear[u,x] returns the list {f (x),a,b}; else it returns False. *)
    if len(args) == 2:
        u, x = args
        lst = eager_FunctionOfLinear(u, False, False, x, False)
        if eager_AtomQ(lst) or eager_FalseQ(lst[0]) or (lst[0] == 0 and lst[1] == 1):
            return False
        return [FunctionOfLinearSubst(u, lst[0], lst[1], x), lst[0], lst[1]]
    u, a, b, x, flag = args
    if eager_FreeQ(u, x):
        return [a, b]
    elif CalculusQ(u):
        return False
    elif eager_LinearQ(u, x):
        if eager_FalseQ(a):
            return [eager_Coefficient(u, x, 0), eager_Coefficient(u, x, 1)]
        lst = CommonFactors([b, eager_Coefficient(u, x, 1)])
        if ZeroQ(eager_Coefficient(u, x, 0)) and eager_Not(flag):
            return [0, lst[0]]
        elif ZeroQ(b*eager_Coefficient(u, x, 0) - a*eager_Coefficient(u, x, 1)):
            return [a/lst[1], lst[0]]
        return [0, 1]
    elif eager_PowerQ(u):
        if eager_FreeQ(u.base, x):
            return eager_FunctionOfLinear(Log(u.base)*u.exp, a, b, x, False)
    lst = MonomialFactor(u, x)
    if eager_ProductQ(u) and NonzeroQ(lst[0]):
        if False and eager_IntegerQ(lst[0]) and lst[0] != -1 and eager_FreeQ(lst[1], x):
            if eager_RationalQ(LeadFactor(lst[1])) and LeadFactor(lst[1]) < 0:
                return eager_FunctionOfLinear(DivideDegreesOfFactors(-lst[1], lst[0])*x, a, b, x, False)
            return eager_FunctionOfLinear(DivideDegreesOfFactors(lst[1], lst[0])*x, a, b, x, False)
        return False
    lst = [a, b]
    for i in u.args:
        lst = eager_FunctionOfLinear(i, lst[0], lst[1], x, eager_SumQ(u))
        if eager_AtomQ(lst):
            return False
    return lst

def eager_NormalizeIntegrand(u, x):
    v = NormalizeLeadTermSigns(NormalizeIntegrandAux(u, x))
    if v == NormalizeLeadTermSigns(u):
        return u
    else:
        return v

def NormalizeIntegrandAux(u, x):
    if eager_SumQ(u):
        l = 0
        for i in u.args:
            l += NormalizeIntegrandAux(i, x)
        return l
    if eager_ProductQ(MergeMonomials(u, x)):
        l = 1
        for i in MergeMonomials(u, x).args:
            l *= NormalizeIntegrandFactor(i, x)
        return l
    else:
        return NormalizeIntegrandFactor(MergeMonomials(u, x), x)

def NormalizeIntegrandFactor(u, x):
    if eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            bas = NormalizeIntegrandFactorBase(u.base, x)
            deg = u.exp
            if eager_IntegerQ(deg) and eager_SumQ(bas):
                if all(eager_MonomialQ(i, x) for i in bas.args):
                    mi = eager_MinimumMonomialExponent(bas, x)
                    q = 0
                    for i in bas.args:
                        q += eager_Simplify(i/x**mi)
                    return x**(mi*deg)*q**deg
                else:
                    return bas**deg
            else:
                return bas**deg
    if eager_PowerQ(u):
        if eager_FreeQ(u.base, x):
            return u.base**NormalizeIntegrandFactorBase(u.exp, x)
    bas = NormalizeIntegrandFactorBase(u, x)
    if eager_SumQ(bas):
        if all(eager_MonomialQ(i, x) for i in bas.args):
            mi = eager_MinimumMonomialExponent(bas, x)
            z = 0
            for j in bas.args:
                z += j/x**mi
            return x**mi*z
        else:
            return bas
    else:
        return bas

def NormalizeIntegrandFactorBase(expr, x):
    m = Wild('m', exclude=[x])
    u = Wild('u')
    match = expr.match(x**m*u)
    if match and eager_SumQ(u):
        l = 0
        for i in u.args:
            l += NormalizeIntegrandFactorBase((x**m*i), x)
        return l
    if eager_BinomialQ(expr, x):
        if eager_BinomialMatchQ(expr, x):
            return expr
        else:
            return eager_ExpandToSum(expr, x)
    elif eager_TrinomialQ(expr, x):
        if eager_TrinomialMatchQ(expr, x):
            return expr
        else:
            return eager_ExpandToSum(expr, x)
    elif eager_ProductQ(expr):
        l = 1
        for i in expr.args:
            l *= NormalizeIntegrandFactor(i, x)
        return l
    elif eager_PolynomialQ(expr, x) and eager_Exponent(expr, x) <= 4:
        return eager_ExpandToSum(expr, x)
    elif eager_SumQ(expr):
        w = Wild('w')
        m = Wild('m', exclude=[x])
        v = TogetherSimplify(expr)
        if eager_SumQ(v) or v.match(x**m*w) and eager_SumQ(w) or eager_LeafCount(v) > eager_LeafCount(expr) + 2:
            return UnifySum(expr, x)
        else:
            return NormalizeIntegrandFactorBase(v, x)
    else:
        return expr

def NormalizeTogether(u):
    return NormalizeLeadTermSigns(eager_Together(u))

def NormalizeLeadTermSigns(u):
    if eager_ProductQ(u):
        t = 1
        for i in u.args:
            lst = SignOfFactor(i)
            if lst[0] == 1:
                t *= lst[1]
            else:
                t *= AbsorbMinusSign(lst[1])
        return t
    else:
        lst = SignOfFactor(u)
    if lst[0] == 1:
        return lst[1]
    else:
        return AbsorbMinusSign(lst[1])

def AbsorbMinusSign(expr, *x):
    m = Wild('m', exclude=[x])
    u = Wild('u')
    v = Wild('v')
    match = expr.match(u*v**m)
    if match:
        if len(match) == 3:
            if eager_SumQ(match[v]) and eager_OddQ(match[m]):
                return match[u]*(-match[v])**match[m]

    return -expr

def NormalizeSumFactors(u):
    if eager_AtomQ(u):
        return u
    elif eager_ProductQ(u):
        k = 1
        for i in u.args:
            k *= NormalizeSumFactors(i)
        return SignOfFactor(k)[0]*SignOfFactor(k)[1]
    elif eager_SumQ(u):
        k = 0
        for i in u.args:
            k += NormalizeSumFactors(i)
        return k
    else:
        return u

def SignOfFactor(u):
    # ``Less(x, 0)`` rather than bare ``x < 0``: Mathematica's Less on a non-real
    # stays unevaluated -> falsy, so the branch is simply not taken. SymPy's ``<``
    # instead returns a Relational whose bool() raises. NumericFactor can hand back a
    # value SymPy has not simplified to an obvious real (e.g. -(-1)^(3/4)+(-1)^(1/4),
    # which is Sqrt[2]); Less treats "not provably negative" as False, matching Rubi.
    if eager_RationalQ(u) and Less(u, 0) or eager_SumQ(u) and Less(NumericFactor(eager_First(u)), 0):
        return [-1, -u]
    elif eager_IntegerPowerQ(u):
        if eager_SumQ(u.base) and Less(NumericFactor(eager_First(u.base)), 0):
            return [(-1)**u.exp, (-u.base)**u.exp]
    elif eager_ProductQ(u):
        k = 1
        h = 1
        for i in u.args:
            k *= SignOfFactor(i)[0]
            h *= SignOfFactor(i)[1]
        return [k, h]
    return [1, u]

def eager_NormalizePowerOfLinear(u, x):
    v = FactorSquareFree(u)
    if eager_PowerQ(v):
        if eager_LinearQ(v.base, x) and eager_FreeQ(v.exp, x):
            return eager_ExpandToSum(v.base, x)**v.exp

    return eager_ExpandToSum(v, x)

def eager_SimplifyIntegrand(u, x):
    v = NormalizeLeadTermSigns(NormalizeIntegrandAux(eager_Simplify(u), x))
    if 5*eager_LeafCount(v) < 4*eager_LeafCount(u):
        return v
    if v != NormalizeLeadTermSigns(u):
        return v
    else:
        return u

def SimplifyTerm(u, x):
    v = eager_Simplify(u)
    w = eager_Together(v)
    if eager_LeafCount(v) < eager_LeafCount(w):
        return eager_NormalizeIntegrand(v, x)
    else:
        return eager_NormalizeIntegrand(w, x)

def TogetherSimplify(u):
    v = eager_Together(eager_Simplify(eager_Together(u)))
    return FixSimplify(v)

def SmartSimplify(u):
    v = eager_Simplify(u)
    w = factor(v)
    if eager_LeafCount(w) < eager_LeafCount(v):
        v = w
    if eager_Not(eager_FalseQ(w == FractionalPowerOfSquareQ(v))) and FractionalPowerSubexpressionQ(u, w, Expand(w)):
        v = SubstForExpn(v, w, Expand(w))
    else:
        v = FactorNumericGcd(v)
    return FixSimplify(v)

def SubstForExpn(u, v, w):
    if u == v:
        return w
    if eager_AtomQ(u):
        return u
    else:
        # Rubi: Map[SubstForExpn[#,v,w], u] -- recurse into args and rebuild with u's
        # head (was incorrectly SUMMING the results, so SubstForExpn[x^2,x,a] gave
        # a+2 instead of a^2).
        return u.func(*[SubstForExpn(i, v, w) for i in u.args])

def eager_ExpandToSum(u, *x):
    if len(x) == 1:
        x = x[0]
        expr = 0
        if eager_PolyQ(S(u), x):
            for t in ExponentList(u, x):
                expr += eager_Coeff(u, x, t)*x**t
            return expr
        if eager_BinomialQ(u, x):
            i = BinomialParts(u, x)
            expr += i[0] + i[1]*x**i[2]
            return expr
        if eager_TrinomialQ(u, x):
            i = TrinomialParts(u, x)
            expr += i[0] + i[1]*x**i[3] + i[2]*x**(2*i[3])
            return expr
        if eager_GeneralizedBinomialMatchQ(u, x):
            i = GeneralizedBinomialParts(u, x)
            expr += i[0]*x**i[3] + i[1]*x**i[2]
            return expr
        if eager_GeneralizedTrinomialMatchQ(u, x):
            i = GeneralizedTrinomialParts(u, x)
            expr += i[0]*x**i[4] + i[1]*x**i[3] + i[2]*x**(2*i[3]-i[4])
            return expr
        else:
            return Expand(u)
    else:
        v = x[0]
        x = x[1]
        w = eager_ExpandToSum(v, x)
        r = NonfreeTerms(w, x)
        if eager_SumQ(r):
            k = u*FreeTerms(w, x)
            for i in r.args:
                k += MergeMonomials(u*i, x)
            return k
        else:
            return u*FreeTerms(w, x) + MergeMonomials(u*r, x)

def UnifySum(u, x):
    if eager_SumQ(u):
        t = 0
        lst = []
        for i in u.args:
            lst += [i]
        for j in UnifyTerms(lst, x):
            t += j
        return t
    else:
        return SimplifyTerm(u, x)

def UnifyTerms(lst, x):
    if lst==[]:
        return lst
    else:
        return UnifyTerm(eager_First(lst), UnifyTerms(eager_Rest(lst), x), x)

def UnifyTerm(term, lst, x):
    if lst==[]:
        return [term]
    tmp = eager_Simplify(eager_First(lst)/term)
    if eager_FreeQ(tmp, x):
        return Prepend(eager_Rest(lst), (1+tmp)*term)
    else:
        return Prepend(UnifyTerm(term, eager_Rest(lst), x), eager_First(lst))

def CalculusQ(u):
    return False

def FunctionOfInverseLinear(*args):
    # (* If u is a function of an inverse linear binomial of the form 1/(a+b*x),
    # FunctionOfInverseLinear[u,x] returns the list {a,b}; else it returns False. *)
    if len(args) == 2:
        u, x = args
        return FunctionOfInverseLinear(u, None, x)
    u, lst, x = args

    if eager_FreeQ(u, x):
        return lst
    elif u == x:
        return False
    elif eager_QuotientOfLinearsQ(u, x):
        tmp = Drop(eager_QuotientOfLinearsParts(u, x), 2)
        if tmp[1] == 0:
            return False
        elif lst is None:
            return tmp
        elif ZeroQ(lst[0]*tmp[1] - lst[1]*tmp[0]):
            return lst
        return False
    elif CalculusQ(u):
        return False
    tmp = lst
    for i in u.args:
        tmp = FunctionOfInverseLinear(i, tmp, x)
        if eager_AtomQ(tmp):
            return False
    return tmp

def PureFunctionOfSinhQ(u, v, x):
    # (* If u is a pure function of Sinh[v] and/or Csch[v], PureFunctionOfSinhQ[u,v,x] returns True;
    # else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and ZeroQ(u.args[0] - v):
        return SinhQ(u) or CschQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfSinhQ(i, v, x)):
            return False
    return True

def PureFunctionOfTanhQ(u, v , x):
    # (* If u is a pure function of Tanh[v] and/or Coth[v], PureFunctionOfTanhQ[u,v,x] returns True;
    # else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and ZeroQ(u.args[0] - v):
        return TanhQ(u) or CothQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfTanhQ(i, v, x)):
            return False
    return True

def PureFunctionOfCoshQ(u, v, x):
    # (* If u is a pure function of Cosh[v] and/or Sech[v], PureFunctionOfCoshQ[u,v,x] returns True;
    # else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and ZeroQ(u.args[0] - v):
        return CoshQ(u) or SechQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfCoshQ(i, v, x)):
            return False
    return True

def IntegerQuotientQ(u, v):
    # (* If u/v is an integer, IntegerQuotientQ[u,v] returns True; else it returns False. *)
    return eager_IntegerQ(eager_Simplify(u/v))

def OddQuotientQ(u, v):
    # (* If u/v is odd, OddQuotientQ[u,v] returns True; else it returns False. *)
    return eager_OddQ(eager_Simplify(u/v))

def EvenQuotientQ(u, v):
    # (* If u/v is even, EvenQuotientQ[u,v] returns True; else it returns False. *)
    return eager_EvenQ(eager_Simplify(u/v))

def FindTrigFactor(func1, func2, u, v, flag):
    # (* If func[w]^m is a factor of u where m is odd and w is an integer multiple of v,
    # FindTrigFactor[func1,func2,u,v,True] returns the list {w,u/func[w]^n}; else it returns False. *)
    # (* If func[w]^m is a factor of u where m is odd and w is an integer multiple of v not equal to v,
    # FindTrigFactor[func1,func2,u,v,False] returns the list {w,u/func[w]^n}; else it returns False. *)
    if u == 1:
        return False
    elif (eager_Head(LeadBase(u)) == func1 or eager_Head(LeadBase(u)) == func2) and eager_OddQ(LeadDegree(u)) and IntegerQuotientQ(LeadBase(u).args[0], v) and (flag or NonzeroQ(LeadBase(u).args[0] - v)):
        # was `LeadBase[u]` -- Mathematica bracket-call transcribed literally; in Python
        # that subscripts the FUNCTION object (TypeError: 'function' object is not
        # subscriptable). Only fired when an odd trig factor with an integer-multiple
        # argument was found, which is why it survived so long (crashed acsc(a+b x)^2/x).
        return [LeadBase(u).args[0], RemainingFactors(u)]
    lst = FindTrigFactor(func1, func2, RemainingFactors(u), v, flag)
    if eager_AtomQ(lst):
        return False
    return [lst[0], LeadFactor(u)*lst[1]]

def FunctionOfSinhQ(u, v, x):
    # (* If u is a function of Sinh[v], FunctionOfSinhQ[u,v,x] returns True; else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        if OddQuotientQ(u.args[0], v):
            # (* Basis: If m odd, Sinh[m*v]^n is a function of Sinh[v]. *)
            return SinhQ(u) or CschQ(u)
        # (* Basis: If m even, Cos[m*v]^n is a function of Sinh[v]. *)
        return CoshQ(u) or SechQ(u)
    elif eager_IntegerPowerQ(u):
        if eager_HyperbolicQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if eager_EvenQ(u.exp):
                # (* Basis: If m integer and n even, Hyper[m*v]^n is a function of Sinh[v]. *)
                return True
            return FunctionOfSinhQ(u.base, v, x)
    elif eager_ProductQ(u):
        if CoshQ(u.args[0]) and SinhQ(u.args[1]) and ZeroQ(u.args[0].args[0] - v/2) and ZeroQ(u.args[1].args[0] - v/2):
            return FunctionOfSinhQ(Drop(u, 2), v, x)
        lst = FindTrigFactor(Sinh, Csch, u, v, False)
        if ListQ(lst) and EvenQuotientQ(lst[0], v):
            # (* Basis: If m even and n odd, Sinh[m*v]^n == Cosh[v]*u where u is a function of Sinh[v]. *)
            return FunctionOfSinhQ(Cosh(v)*lst[1], v, x)
        lst = FindTrigFactor(Cosh, Sech, u, v, False)
        if ListQ(lst) and OddQuotientQ(lst[0], v):
            # (* Basis: If m odd and n odd, Cosh[m*v]^n == Cosh[v]*u where u is a function of Sinh[v]. *)
            return FunctionOfSinhQ(Cosh(v)*lst[1], v, x)
        lst = FindTrigFactor(Tanh, Coth, u, v, True)
        if ListQ(lst):
            # (* Basis: If m integer and n odd, Tanh[m*v]^n == Cosh[v]*u where u is a function of Sinh[v]. *)
            return FunctionOfSinhQ(Cosh(v)*lst[1], v, x)
        return all(FunctionOfSinhQ(i, v, x) for i in u.args)
    return all(FunctionOfSinhQ(i, v, x) for i in u.args)

def FunctionOfCoshQ(u, v, x):
    #(* If u is a function of Cosh[v], FunctionOfCoshQ[u,v,x] returns True; else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        # (* Basis: If m integer, Cosh[m*v]^n is a function of Cosh[v]. *)
        return CoshQ(u) or SechQ(u)
    elif eager_IntegerPowerQ(u):
        if eager_HyperbolicQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if eager_EvenQ(u.exp):
                # (* Basis: If m integer and n even, Hyper[m*v]^n is a function of Cosh[v]. *)
                return True
            return FunctionOfCoshQ(u.base, v, x)
    elif eager_ProductQ(u):
        lst = FindTrigFactor(Sinh, Csch, u, v, False)
        if ListQ(lst):
            # (* Basis: If m integer and n odd, Sinh[m*v]^n == Sinh[v]*u where u is a function of Cosh[v]. *)
            return FunctionOfCoshQ(Sinh(v)*lst[1], v, x)
        lst = FindTrigFactor(Tanh, Coth, u, v, True)
        if ListQ(lst):
            # (* Basis: If m integer and n odd, Tanh[m*v]^n == Sinh[v]*u where u is a function of Cosh[v]. *)
            return FunctionOfCoshQ(Sinh(v)*lst[1], v, x)
        return all(FunctionOfCoshQ(i, v, x) for i in u.args)
    return all(FunctionOfCoshQ(i, v, x) for i in u.args)

def OddHyperbolicPowerQ(u, v, x):
    if SinhQ(u) or CoshQ(u) or SechQ(u) or CschQ(u):
        return OddQuotientQ(u.args[0], v)
    if eager_PowerQ(u):
        return eager_OddQ(u.exp) and OddHyperbolicPowerQ(u.base, v, x)
    if eager_ProductQ(u):
        if eager_Not(eager_EqQ(eager_FreeFactors(u, x), 1)):
            return OddHyperbolicPowerQ(eager_NonfreeFactors(u, x), v, x)
        lst = []
        for i in u.args:
            if eager_Not(FunctionOfTanhQ(i, v, x)):
                lst.append(i)
        if lst == []:
            return True
        return eager_Length(lst)==1 and OddHyperbolicPowerQ(lst[0], v, x)
    if eager_SumQ(u):
        return all(OddHyperbolicPowerQ(i, v, x) for i in u.args)
    return False

def FunctionOfTanhQ(u, v, x):
    #(* If u is a function of the form f[Tanh[v],Coth[v]] where f is independent of x,
    # FunctionOfTanhQ[u,v,x] returns True; else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        return TanhQ(u) or CothQ(u) or EvenQuotientQ(u.args[0], v)
    elif eager_PowerQ(u):
        if eager_EvenQ(u.exp) and eager_HyperbolicQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            return True
        elif eager_EvenQ(u.args[1]) and eager_SumQ(u.args[0]):
            # Rubi: FunctionOfTanhQ[Expand[u[[1]]^2], v, x] -- the v, x belong to the
            # OUTER call. A misplaced paren passed them to Expand, which takes one
            # argument, so this raised
            #   TypeError: Expand() takes 1 positional argument but 3 were given
            # instead of answering the predicate (e.g. x*sqrt(a*sec(x)^4)*csc(x)*sec(x)).
            return FunctionOfTanhQ(Expand(u.args[0]**2), v, x)
    if eager_ProductQ(u):
        lst = []
        for i in u.args:
            if eager_Not(FunctionOfTanhQ(i, v, x)):
                lst.append(i)
        if lst == []:
            return True
        return eager_Length(lst)==2 and OddHyperbolicPowerQ(lst[0], v, x) and OddHyperbolicPowerQ(lst[1], v, x)
    return all(FunctionOfTanhQ(i, v, x) for i in u.args)

def FunctionOfTanhWeight(u, v, x):
    """
    u is a function of the form f(tanh(v), coth(v)) where f is independent of x.
    FunctionOfTanhWeight(u, v, x) returns a nonnegative number if u is best considered a function of tanh(v), else it returns a negative number.

    Examples
    ========

    >>> from sympy import sinh, log, tanh
    >>> from sympy.abc import x
    >>> from rubi_rules.utils.utility_functions import FunctionOfTanhWeight
    >>> FunctionOfTanhWeight(x, log(x), x)
    0
    >>> FunctionOfTanhWeight(sinh(log(x)), log(x), x)
    0
    >>> FunctionOfTanhWeight(tanh(log(x)), log(x), x)
    1

    """
    if eager_AtomQ(u):
        return S(0)
    elif CalculusQ(u):
        return S(0)
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        if TanhQ(u) and ZeroQ(u.args[0] - v):
            return S(1)
        elif CothQ(u) and ZeroQ(u.args[0] - v):
            return S(-1)
        return S(0)
    elif eager_PowerQ(u):
        if eager_EvenQ(u.exp) and eager_HyperbolicQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if TanhQ(u.base) or CoshQ(u.base) or SechQ(u.base):
                return S(1)
            return S(-1)
    if eager_ProductQ(u):
        if all(FunctionOfTanhQ(i, v, x) for i in u.args):
            return Add(*[FunctionOfTanhWeight(i, v, x) for i in u.args])
        return S(0)
    return Add(*[FunctionOfTanhWeight(i, v, x) for i in u.args])

def FunctionOfHyperbolicQ(u, v, x):
    # (* If u (x) is equivalent to a function of the form f (Sinh[v],Cosh[v],Tanh[v],Coth[v],Sech[v],Csch[v])
    # where f is independent of x, FunctionOfHyperbolicQ[u,v,x] returns True; else it returns False. *)
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        return True
    return all(FunctionOfHyperbolicQ(i, v, x) for i in u.args)

def SmartNumerator(expr):
    if eager_PowerQ(expr):
        n = expr.exp
        u = expr.base
        if eager_RationalQ(n) and n < 0:
            return SmartDenominator(u**(-n))
    elif eager_ProductQ(expr):
        return Mul(*[SmartNumerator(i) for i in expr.args])
    return eager_Numerator(expr)

def SmartDenominator(expr):
    if eager_PowerQ(expr):
        u = expr.base
        n = expr.exp
        if eager_RationalQ(n) and n < 0:
            return SmartNumerator(u**(-n))
    elif eager_ProductQ(expr):
        return Mul(*[SmartDenominator(i) for i in expr.args])
    return eager_Denominator(expr)

# =============================================================================
# Inert (deactivated) trigonometric / hyperbolic functions
# =============================================================================
# Inert trig-function markers live in their own module (rubi_rules.utils.
# inert_functions); they are re-exported here so existing callers that do
# ``from rubi_rules.utils.utility_functions import InertSin`` keep working.
# ActivateTrig / DeactivateTrig and the inert-trig predicates below use them.
from rubi_rules.utils.inert_functions import (  # noqa: E402
    InertSin, InertCos, InertTan, InertCot, InertSec, InertCsc,
    _INERT_TO_ACTIVE, _INERT_TRIG_HEADS)


def eager_ActivateTrig(u):
    """Replace inert trig functions (``Function('sin')(...)``, ...) with the
    active SymPy trig functions (``sin(...)``, ...).

    A no-op on expressions that contain no inert markers (e.g. ordinary
    integrands), so it is safe to call unconditionally.
    """
    if not isinstance(u, Basic):
        return u
    for inert, active in _INERT_TO_ACTIVE.items():
        u = u.replace(inert, active)
    return u

def eager_ExpandTrig(*args):
    if len(args) == 2:
        u, x = args
        return eager_ActivateTrig(eager_ExpandIntegrand(u, x))
    u, v, x = args
    w = eager_ExpandTrig(v, x)
    z = eager_ActivateTrig(u)
    if eager_SumQ(w):
        return w.func(*[z*i for i in w.args])
    return z*w

def TrigExpand(u):
    return expand_trig(u)

# SubstForTrig[u_,sin_,cos_,v_,x_] :=
#   If[AtomQ[u],
#     u,
#   If[TrigQ[u] && IntegerQuotientQ[u[[1]],v],
#     If[u[[1]]===v || ZeroQ[u[[1]]-v],
#       If[SinQ[u],
#         sin,
#       If[CosQ[u],
#         cos,
#       If[TanQ[u],
#         sin/cos,
#       If[CotQ[u],
#         cos/sin,
#       If[SecQ[u],
#         1/cos,
#       1/sin]]]]],
#     Map[Function[SubstForTrig[#,sin,cos,v,x]],
#             ReplaceAll[TrigExpand[Head[u][Simplify[u[[1]]/v]*x]],x->v]]],
#   If[ProductQ[u] && CosQ[u[[1]]] && SinQ[u[[2]]] && ZeroQ[u[[1,1]]-v/2] && ZeroQ[u[[2,1]]-v/2],
#     sin/2*SubstForTrig[Drop[u,2],sin,cos,v,x],
#   Map[Function[SubstForTrig[#,sin,cos,v,x]],u]]]]


def SubstForTrig(u, sin_ , cos_, v, x):
    # (* u (v) is an expression of the form f (Sin[v],Cos[v],Tan[v],Cot[v],Sec[v],Csc[v]). *)
    # (* SubstForTrig[u,sin,cos,v,x] returns the expression f (sin,cos,sin/cos,cos/sin,1/cos,1/sin). *)
    if eager_AtomQ(u):
        return u
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        if u.args[0] == v or ZeroQ(u.args[0] - v):
            if SinQ(u):
                return sin_
            elif CosQ(u):
                return cos_
            elif TanQ(u):
                return sin_/cos_
            elif CotQ(u):
                return cos_/sin_
            elif SecQ(u):
                return 1/cos_
            return 1/sin_
        r = eager_ReplaceAll(TrigExpand(eager_Head(u)(eager_Simplify(u.args[0]/v*x))), {x: v})
        return r.func(*[SubstForTrig(i, sin_, cos_, v, x) for i in r.args])
    if eager_ProductQ(u) and CosQ(u.args[0]) and SinQ(u.args[1]) and ZeroQ(u.args[0].args[0] - v/2) and ZeroQ(u.args[1].args[0] - v/2):
        return sin(x)/2*SubstForTrig(Drop(u, 2), sin_, cos_, v, x)
    return u.func(*[SubstForTrig(i, sin_, cos_, v, x) for i in u.args])

def SubstForHyperbolic(u, sinh_, cosh_, v, x):
    # (* u (v) is an expression of the form f (Sinh[v],Cosh[v],Tanh[v],Coth[v],Sech[v],Csch[v]). *)
    # (* SubstForHyperbolic[u,sinh,cosh,v,x] returns the expression
    # f (sinh,cosh,sinh/cosh,cosh/sinh,1/cosh,1/sinh). *)
    if eager_AtomQ(u):
        return u
    elif eager_HyperbolicQ(u) and IntegerQuotientQ(u.args[0], v):
        if u.args[0] == v or ZeroQ(u.args[0] - v):
            if SinhQ(u):
                return sinh_
            elif CoshQ(u):
                return cosh_
            elif TanhQ(u):
                return sinh_/cosh_
            elif CothQ(u):
                return cosh_/sinh_
            if SechQ(u):
                return 1/cosh_
            return 1/sinh_
        r = eager_ReplaceAll(TrigExpand(eager_Head(u)(eager_Simplify(u.args[0]/v)*x)), {x: v})
        return r.func(*[SubstForHyperbolic(i, sinh_, cosh_, v, x) for i in r.args])
    elif eager_ProductQ(u) and CoshQ(u.args[0]) and SinhQ(u.args[1]) and ZeroQ(u.args[0].args[0] - v/2) and ZeroQ(u.args[1].args[0] - v/2):
        return sinh(x)/2*SubstForHyperbolic(Drop(u, 2), sinh_, cosh_, v, x)
    return u.func(*[SubstForHyperbolic(i, sinh_, cosh_, v, x) for i in u.args])

def eager_InertTrigFreeQ(u):
    # True when u contains no *inert* trig functions.  Active SymPy sin/cos/...
    # are not inert, so an ordinary trig integrand is inert-trig-free — which is
    # why the inert-trig fallback rules (guarded by Not(InertTrigFreeQ)) must NOT
    # fire on it.  (Checking active sin/cos here was a bug: it made every trig
    # integrand look inert and let the CannotIntegrate catch-all steal them.)
    return all(eager_FreeQ(u, h) for h in _INERT_TRIG_HEADS)

def LCM(a, b):
    return lcm(a, b)

def eager_SubstForFractionalPowerOfLinear(u, x):
    # (* If u has a subexpression of the form (a+b*x)^(m/n) where m and n>1 are integers,
    # SubstForFractionalPowerOfLinear[u,x] returns the list {v,n,a+b*x,1/b} where v is u
    # with subexpressions of the form (a+b*x)^(m/n) replaced by x^m and x replaced
    # by -a/b+x^n/b, and all times x^(n-1); else it returns False. *)
    lst = FractionalPowerOfLinear(u, S(1), False, x)
    if eager_AtomQ(lst) or eager_FalseQ(lst[1]):
        return False
    n = lst[0]
    a = eager_Coefficient(lst[1], x, 0)
    b = eager_Coefficient(lst[1], x, 1)
    tmp = eager_Simplify(x**(n-1)*SubstForFractionalPower(u, lst[1], n, -a/b + x**n/b, x))
    return [eager_NonfreeFactors(tmp, x), n, lst[1], eager_FreeFactors(tmp, x)/b]

def FractionalPowerOfLinear(u, n, v, x):
    # If u has a subexpression of the form (a + b*x)**(m/n), FractionalPowerOfLinear(u, 1, False, x) returns [n, a + b*x], else it returns False.
    if eager_AtomQ(u) or eager_FreeQ(u, x):
        return [n, v]
    elif CalculusQ(u):
        return False
    elif eager_FractionalPowerQ(u):
        if eager_LinearQ(u.base, x) and (eager_FalseQ(v) or ZeroQ(u.base - v)):
            return [LCM(eager_Denominator(u.exp), n), u.base]
    lst = [n, v]
    for i in u.args:
        lst = FractionalPowerOfLinear(i, lst[0], lst[1], x)
        if eager_AtomQ(lst):
            return False
    return lst

def eager_InverseFunctionOfLinear(u, x):
    # (* If u has a subexpression of the form g[a+b*x] where g is an inverse function,
    # InverseFunctionOfLinear[u,x] returns g[a+b*x]; else it returns False. *)
    if eager_AtomQ(u) or CalculusQ(u) or eager_FreeQ(u, x):
        return False
    elif eager_InverseFunctionQ(u) and eager_LinearQ(u.args[0], x):
        return u
    for i in u.args:
        tmp = eager_InverseFunctionOfLinear(i, x)
        if eager_Not(eager_AtomQ(tmp)):
            return tmp
    return False

def eager_InertTrigQ(*args):
    if len(args) == 1:
        f = args[0]
        return eager_Head(f) in _INERT_TRIG_HEADS
    elif len(args) == 2:
        f, g = args
        if f == g:
            return eager_InertTrigQ(f)
        return InertReciprocalQ(f, g) or InertReciprocalQ(g, f)
    else:
        f, g, h = args
        return eager_InertTrigQ(g, f) and eager_InertTrigQ(g, h)

def InertReciprocalQ(f, g):
    return ((f.func is InertSin and g.func is InertCsc) or
            (f.func is InertCos and g.func is InertSec) or
            (f.func is InertTan and g.func is InertCot))

_ACTIVE_TRIG_HEADS = [sin, cos, tan, cot, sec, csc,
                      sinh, cosh, tanh, coth, sech, csch]


def eager_DeactivateTrig(u, x):
    # (* u is a function of trig functions of a linear function of x. *)
    # (* DeactivateTrig[u,x] returns u with the trig functions replaced with inert trig functions. *)
    # DeactivateTrig[(c+d x)^m (a+b trig[e+f x])^n, x] := (c+d x)^m (a+b DeactivateTrig[trig[e+f x],x])^n
    if u.is_Mul:
        c_ = Wild('c', exclude=[x]); d_ = Wild('d', exclude=[x])
        a_ = Wild('a', exclude=[x]); b_ = Wild('b', exclude=[x])
        e_ = Wild('e', exclude=[x]); f_ = Wild('f', exclude=[x])
        m_ = Wild('m', exclude=[x]); n_ = Wild('n', exclude=[x])
        for TR in _ACTIVE_TRIG_HEADS:
            M = u.match((c_ + d_*x)**m_ * (a_ + b_*TR(e_ + f_*x))**n_)
            if M is not None and M.get(d_) is not None and not eager_EqQ(M[d_], 0):
                inner = eager_DeactivateTrig(TR(M[e_] + M[f_]*x), x)
                return (M[c_] + M[d_]*x)**M[m_] * (M[a_] + M[b_]*inner)**M[n_]
    return UnifyInertTrigFunction(FixInertTrigFunction(DeactivateTrigAux(u, x), x), x)


def FixInertTrigFunction(u, x):
    # Port of Rubi's FixInertTrigFunction (61 clauses).  Operates on INERT trig
    # expressions produced by DeactivateTrigAux -- every lowercase trig head in
    # the source maps to the Inert* markers.  Clauses are in Rubi source order
    # (most-specific first); the ``return u`` catch-all is last.
    sin_, cos_, tan_ = InertSin, InertCos, InertTan
    cot_, sec_, csc_ = InertCot, InertSec, InertCsc
    a_ = Wild('a', exclude=[x]); b_ = Wild('b', exclude=[x])
    c_ = Wild('c', exclude=[x]); n_ = Wild('n', exclude=[x])
    m_ = Wild('m', exclude=[x]); p_ = Wild('p', exclude=[x])
    A_ = Wild('A', exclude=[x]); B_ = Wild('B', exclude=[x])
    C_ = Wild('C', exclude=[x])
    v_ = Wild('v'); w_ = Wild('w'); u_ = Wild('u')
    has = u.has

    # a*u /; FreeQ[a,x]  -- pull out x-free multiplicative factors
    if u.is_Mul:
        coeff, rest = u.as_independent(x, as_Add=False)
        if coeff != 1:
            return coeff*FixInertTrigFunction(rest, x)

    # u*(a*(b+v))^n /; FreeQ[{a,b,n},x] && Not[FreeQ[v,x]]  -- distribute
    #
    # `M[b_] != 0` is REQUIRED for termination, and it is what Mathematica's matcher
    # enforces for free. `b_` is a plain Blank there, so `b_+v_` only matches a real
    # Plus with two terms. SymPy's Wild is looser: it happily binds b_ -> 0 and
    # v_ -> the whole thing, so `(a*(b+v))^n` matched `(d*InertTan[w])^n` -- a Times,
    # not a sum. The rewrite u*(a*b+a*v)^n then rebuilt the IDENTICAL expression and
    # recursed on it forever: this single clause is the RecursionError behind the whole
    # (trig)^(n/2) family (11 corpus cases) and the uninterruptible hang alongside it.
    M = _umatch(u, u_*(a_*(b_ + v_))**n_, plain=('b',))
    if M is not None and not eager_FreeQ(M[v_], x) and M[a_] != 1:
        return FixInertTrigFunction(M[u_]*(M[a_]*M[b_] + M[a_]*M[v_])**M[n_], x)

    # ---- (co)function of one power times power of another: TRIGa[v]^m*(c TRIGb[w])^n ----
    # (fa, fb, fa_result)  with  fa[v]^m*(c*fb[w])^n -> fa_result[v]^(-m)*(c*fb[w])^n
    _pairs = [
        (csc_, sin_, sin_), (sec_, cos_, cos_), (cot_, tan_, tan_),
        (tan_, cot_, cot_), (cos_, sec_, sec_), (sin_, csc_, csc_),
        (sec_, sin_, cos_), (csc_, cos_, sin_), (cos_, tan_, sec_),
        (sin_, cot_, csc_), (sin_, sec_, csc_), (cos_, csc_, sec_),
        (cot_, sin_, tan_), (tan_, cos_, cot_), (csc_, tan_, sin_),
        (sec_, cot_, cos_), (cot_, sec_, tan_), (tan_, csc_, cot_),
    ]
    for fa, fb, fr in _pairs:
        if has(fa) and has(fb):
            M = _umatch(u, fa(v_)**m_ * (c_*fb(w_))**n_)
            if M is not None and eager_IntegerQ(M[m_]):
                return fr(M[v_])**(-M[m_]) * (M[c_]*fb(M[w_]))**M[n_]

    # sec[v]^m*sec[w]^n -> cos[v]^-m cos[w]^-n ;  csc[v]^m*csc[w]^n -> sin[v]^-m sin[w]^-n
    for fa, fr in [(sec_, cos_), (csc_, sin_)]:
        if has(fa):
            M = _umatch(u, fa(v_)**m_ * fa(w_)**n_)
            if M is not None and M[v_] != M[w_] and eager_IntegersQ(M[m_], M[n_]):
                return fr(M[v_])**(-M[m_]) * fr(M[w_])**(-M[n_])

    # u*TRIG[v]^m*(a+b*TRIG2[w])^n -> (ratio)^m * Fix(u*(a+b*TRIG2[w])^n)
    for fa, fnum, fden, ftrig in [(tan_, sin_, cos_, sin_), (cot_, cos_, sin_, sin_),
                                  (tan_, sin_, cos_, cos_), (cot_, cos_, sin_, cos_)]:
        if has(fa) and has(ftrig):
            # `M[a_] != 0`: Rubi writes this as `(a_) + (b_.)*sin[w_]` -- a PLAIN Blank
            # for the constant term, so it only matches a genuine SUM. SymPy's Wild
            # binds a_ -> 0 and matches a bare `(b*sin(w))^n` too, firing a clause Rubi
            # would skip. (Same over-match as the `(b_+v_)` clause above, which is what
            # made this function recurse forever -- see that comment.)
            # Rubi's clause here is `(u_)` -- a PLAIN Blank -- so a spare factor is
            # REQUIRED; see the nonunit note in _umatch.
            M = _umatch(u, u_*fa(v_)**m_*(a_ + b_*ftrig(w_))**n_,
                        plain=('a',), nonunit=('u',))
            if M is not None and eager_IntegerQ(M[m_]):
                return (fnum(M[v_])**M[m_]/fden(M[v_])**M[m_]) * \
                    FixInertTrigFunction(M[u_]*(M[a_] + M[b_]*ftrig(M[w_]))**M[n_], x)

    # cot[v]^m*(a+b*(c*sin[w])^p)^n -> tan[v]^-m*(...)  ;  tan[v]^m*(a+b*(c*cos[w])^p)^n -> cot[v]^-m*(...)
    for fa, fr, ftrig in [(cot_, tan_, sin_), (tan_, cot_, cos_)]:
        if has(fa) and has(ftrig):
            # `M[a_] != 0` -- plain Blank in Rubi, so a genuine sum is required.
            M = _umatch(u, fa(v_)**m_*(a_ + b_*(c_*ftrig(w_))**p_)**n_, plain=('a',))
            if M is not None and eager_IntegerQ(M[m_]):
                return fr(M[v_])**(-M[m_])*(M[a_] + M[b_]*(M[c_]*ftrig(M[w_]))**M[p_])**M[n_]

    # u*(c*TRIG[v]^n)^p*w /; FreeQ[{c,p},x] && PowerOfInertTrigSumQ[w,TRIG,x]
    for ftrig in [sin_, cos_, tan_, cot_, sec_, csc_]:
        if has(ftrig) and u.is_Mul:
            facs = list(u.args)
            for i, fac in enumerate(facs):
                Mf = fac.match((c_*ftrig(v_)**n_)**p_)
                if Mf is None:
                    continue
                rest = Mul(*[facs[j] for j in range(len(facs)) if j != i])
                if any(PowerOfInertTrigSumQ(w, ftrig, x) for w in _fix_factors(rest)):
                    return (Mf[c_]*ftrig(Mf[v_])**Mf[n_])**Mf[p_]*FixInertTrigFunction(rest, x)

    # u*TRIGa[v]^n*w /; PowerOfInertTrigSumQ[w,TRIGc,x] && IntegerQ[n] -> TRIGb[v]^-n*Fix(u*w)
    _single = [
        (sec_, cos_, cos_), (csc_, sin_, sin_), (sec_, cos_, sin_), (csc_, sin_, cos_),
        (cot_, tan_, tan_), (cos_, sec_, tan_), (csc_, sin_, tan_),
        (tan_, cot_, cot_), (sin_, csc_, cot_), (sec_, cos_, cot_),
        (cos_, sec_, sec_), (cot_, tan_, sec_), (csc_, sin_, sec_),
        (sin_, csc_, csc_), (tan_, cot_, csc_), (sec_, cos_, csc_),
    ]
    for fa, fr, fw in _single:
        if has(fa) and u.is_Mul:
            facs = list(u.args)
            for i, fac in enumerate(facs):
                Mf = fac.match(fa(v_)**n_)
                if Mf is None or not eager_IntegerQ(Mf[n_]):
                    continue
                rest = Mul(*[facs[j] for j in range(len(facs)) if j != i])
                if any(PowerOfInertTrigSumQ(w, fw, x) for w in _fix_factors(rest)):
                    return fr(Mf[v_])**(-Mf[n_])*FixInertTrigFunction(rest, x)

    # u*TRIG[v]^m*(a*sin[v]+b*cos[v])^n -> (ratio)^m * Fix(u*(a sin[v]+b cos[v])^n)
    for fa, fnum, fden in [(tan_, sin_, cos_), (cot_, cos_, sin_),
                           (sec_, S(1), cos_), (csc_, S(1), sin_)]:
        if has(fa) and has(sin_) and has(cos_):
            M = _umatch(u, u_*fa(v_)**m_*(a_*sin_(v_) + b_*cos_(v_))**n_)
            if M is not None and eager_IntegerQ(M[m_]):
                num = (fnum(M[v_])**M[m_] if fnum is not S(1) else S(1))
                return num*fden(M[v_])**(-M[m_]) * \
                    FixInertTrigFunction(M[u_]*(M[a_]*sin_(M[v_]) + M[b_]*cos_(M[v_]))**M[n_], x)

    # f[v]^m*(A+B*g[v]+C*g[v]^2)   and   f[v]^m*(A+C*g[v]^2)   with InertReciprocal(f,g)
    for f1 in _INERT_TRIG_HEADS:
        for f2 in _INERT_TRIG_HEADS:
            if not (InertReciprocalQ(f1(x), f2(x)) or InertReciprocalQ(f2(x), f1(x))):
                continue
            if not (has(f1) and has(f2)):
                continue
            M = _umatch(u, f1(v_)**m_*(A_ + B_*f2(v_) + C_*f2(v_)**2)*(a_ + b_*f2(v_))**n_)
            if M is not None and eager_IntegerQ(M[m_]) and M[C_] != 0 and M[B_] != 0:
                return f2(M[v_])**(-M[m_])*(M[A_] + M[B_]*f2(M[v_]) + M[C_]*f2(M[v_])**2)*(M[a_] + M[b_]*f2(M[v_]))**M[n_]
            M = _umatch(u, f1(v_)**m_*(A_ + C_*f2(v_)**2)*(a_ + b_*f2(v_))**n_)
            if M is not None and eager_IntegerQ(M[m_]) and M[C_] != 0:
                return f2(M[v_])**(-M[m_])*(M[A_] + M[C_]*f2(M[v_])**2)*(M[a_] + M[b_]*f2(M[v_]))**M[n_]
            M = _umatch(u, f1(v_)**m_*(A_ + B_*f2(v_) + C_*f2(v_)**2))
            if M is not None and eager_IntegerQ(M[m_]) and M[C_] != 0 and M[B_] != 0:
                return f2(M[v_])**(-M[m_])*(M[A_] + M[B_]*f2(M[v_]) + M[C_]*f2(M[v_])**2)
            M = _umatch(u, f1(v_)**m_*(A_ + C_*f2(v_)**2))
            if M is not None and eager_IntegerQ(M[m_]) and M[C_] != 0:
                return f2(M[v_])**(-M[m_])*(M[A_] + M[C_]*f2(M[v_])**2)

    return u


def _fix_factors(expr):
    return list(expr.args) if expr.is_Mul else [expr]


def _umatch(u, pat, plain=(), nonunit=()):
    """Like ``u.match(pat)`` but with Mathematica's blank semantics.

    Two degenerate matches are rejected:

    1. **Incomplete matches.** SymPy will match a multi-factor pattern against a
       smaller product by dropping factors (and their wilds). A genuine match binds
       EVERY wild in the pattern, so completeness is required. The "rest" wild ``u_``
       is optional (default 1).

    2. **Zero-bound PLAIN blanks** (``plain``). Rubi distinguishes ``a_`` (a plain
       Blank, which must bind a real operand) from ``a_.`` (Optional, which defaults
       to 0 in a Plus / 1 in a Times). SymPy's ``Wild`` has no such distinction and
       happily binds ``a_ -> 0``, so a pattern like ``(a_ + b_*sin(w))**n_`` matches
       a bare ``(b*sin(w))**n`` -- firing a clause Mathematica would skip. Pass the
       names Rubi declares as plain blanks and they may not bind the additive
       identity.

       This is the bug class behind ``FixInertTrigFunction``'s infinite recursion
       (``(b_+v_)`` matched a Times, so the rewrite rebuilt its own input) and behind
       ``GeneralizedBinomialMatchQ`` answering False where Rubi answers True.

    matchpy models this natively -- ``Wildcard.dot()`` is ``a_`` and
    ``Wildcard.optional(name, default)`` is ``a_.`` -- and moving these clauses onto
    matchpy would enforce it structurally rather than by convention. That is the right
    long-term shape; it is not done here because ``FixInertTrigFunction`` alone is 61
    clauses on a hot path (~20-30 ms/call already), and matchpy's commutative matcher
    is what blows up exponentially in ``FixSimplify``. Until then this choke point
    gives the same guarantee at no runtime cost: to fix one of the remaining sites,
    add ``plain=(...)`` to its ``_umatch`` call.

    To find which names Rubi declares plain, query the real thing::

        Cases[DownValues[f][[All, 1]],
              Verbatim[Plus][___, Verbatim[Pattern][_, Verbatim[Blank][]], ___],
              Infinity]
    """
    M = u.match(pat)
    if M is None:
        return None
    for w in pat.atoms(Wild):
        if w not in M:
            if w.name == 'u':
                M[w] = S.One
            else:
                return None
    for name in plain:
        for w, val in M.items():
            if getattr(w, 'name', None) == name and val == 0:
                return None
    # `nonunit` is the MULTIPLICATIVE counterpart of `plain`: names Rubi writes as a
    # plain Blank in a product position, which therefore must bind a real factor and
    # cannot be the implicit 1. The `u` default below treats `u_` as optional for every
    # clause, but Rubi uses BOTH forms -- e.g. of its two tan+sin clauses,
    #   FixInertTrigFunction[(u_)*((a_)+(b_.)sin[w_])^(n_.)*tan[v_]^(m_.), x]   <- plain
    #   FixInertTrigFunction[(u_.)*(cos[v_](b_.)+(a_.)sin[v_])^(n_.)*tan[v_]^(m_.), x]
    # only the second permits the default. Without this, `tan^2 (2+3 sin)^(5/2)` (no
    # spare factor) matched the first clause with u -> 1 and was rewritten to
    # sin^2/cos^2 (2+3 sin)^(5/2), where Mathematica leaves it ALONE.
    for name in nonunit:
        for w, val in M.items():
            if getattr(w, 'name', None) == name and val == S.One:
                return None
    return M


def UnifyInertTrigFunction(u, x):
    # Port of Rubi's UnifyInertTrigFunction (75 clauses).  Canonicalizes the
    # co-functions in an inert-trig expression (cos->sin, sec->csc, cot->tan)
    # via a Pi/2 argument shift.  Clauses are in Rubi source order; the
    # ``return u`` catch-all -- which appears mid-file in the source -- is placed
    # LAST here so every specific clause is tried first.
    sin_, cos_, tan_ = InertSin, InertCos, InertTan
    cot_, sec_, csc_ = InertCot, InertSec, InertCsc
    a_ = Wild('a', exclude=[x]); b_ = Wild('b', exclude=[x])
    c_ = Wild('c', exclude=[x]); d_ = Wild('d', exclude=[x])
    e_ = Wild('e', exclude=[x]); f_ = Wild('f', exclude=[x])
    g_ = Wild('g', exclude=[x]); m_ = Wild('m', exclude=[x])
    n_ = Wild('n', exclude=[x]); p_ = Wild('p', exclude=[x])
    A_ = Wild('A', exclude=[x]); B_ = Wild('B', exclude=[x])
    C_ = Wild('C', exclude=[x])
    has = u.has

    # a*u /; FreeQ[a,x]  -- pull out x-free multiplicative factors (head clause)
    if u.is_Mul:
        coeff, rest = u.as_independent(x, as_Add=False)
        if coeff != 1:
            return coeff*UnifyInertTrigFunction(rest, x)

    def ap(M):
        return M[e_] + pi/2 + M[f_]*x

    def am(M):
        return M[e_] - pi/2 + M[f_]*x

    not_mul = not u.is_Mul

    # ================= Cosine to sine =================
    # 1.0 (a cos)^m (b csc)^n
    if has(cos_) and has(csc_):
        M = _umatch(u, (a_*cos_(e_ + f_*x))**m_ * (b_*csc_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*sin_(ap(M)))**M[m_] * (-M[b_]*sec_(ap(M)))**M[n_]
    # 1.0 (a cos)^m (b sec)^n
    if has(cos_) and has(sec_):
        M = _umatch(u, (a_*cos_(e_ + f_*x))**m_ * (b_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*sin_(ap(M)))**M[m_] * (M[b_]*csc_(ap(M)))**M[n_]
    # 1.1.1 (a+b cos)^n
    if has(cos_) and not_mul:
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[n_]
    # 1.1.2 (g sin)^p (a+b cos)^m   [a required]
    if has(sin_) and has(cos_):
        M = _umatch(u, (g_*sin_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[g_]*cos_(am(M)))**M[p_] * (M[a_] - M[b_]*sin_(am(M)))**M[m_]
    # 1.1.2 (g csc)^p (a+b cos)^m   [a required]
    if has(csc_) and has(cos_):
        M = _umatch(u, (g_*csc_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[g_]*sec_(am(M)))**M[p_] * (M[a_] - M[b_]*sin_(am(M)))**M[m_]
    # 1.1.3 (g cot)^p (a+b cos)^m   [a required]  (If[True] -> first branch)
    if has(cot_) and has(cos_):
        M = _umatch(u, (g_*cot_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (-M[g_]*tan_(am(M)))**M[p_] * (M[a_] - M[b_]*sin_(am(M)))**M[m_]
    # 1.1.3 (g tan)^p (a+b cos)^m   [a required]
    if has(tan_) and has(cos_):
        M = _umatch(u, (g_*tan_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (-M[g_]*cot_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_]
    # 1.2.1 (a+b cos)^m (c+d cos)^n
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_]
    # 1.2.1 (a+b cos)^m (c+d sec)^n
    if has(cos_) and has(sec_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 1.2.2 (g sin)^p (a+b cos)^m (c+d cos)^n
    if has(sin_) and has(cos_):
        M = _umatch(u, (g_*sin_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_)
        if M is not None:
            if eager_IntegerQ(2*M[p_]) and M[p_].is_negative and eager_IntegerQ(2*M[n_]):
                return (M[g_]*cos_(am(M)))**M[p_] * (M[a_] - M[b_]*sin_(am(M)))**M[m_] * (M[c_] - M[d_]*sin_(am(M)))**M[n_]
            return (-M[g_]*cos_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_]
    # 1.2.2 (g csc)^p (a+b cos)^m (c+d cos)^n
    if has(csc_) and has(cos_):
        M = _umatch(u, (g_*csc_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*sec_(am(M)))**M[p_] * (M[a_] - M[b_]*sin_(am(M)))**M[m_] * (M[c_] - M[d_]*sin_(am(M)))**M[n_]
    # 1.2.3 (g cos)^p (a+b cos)^m (c+d cos)^n
    if has(cos_):
        M = _umatch(u, (g_*cos_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*sin_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_]
    # 1.2.3 (g cos)^p (a+b cos)^m (c+d sec)^n
    if has(cos_) and has(sec_):
        M = _umatch(u, (g_*cos_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*sin_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 1.2.3 (g sec)^p (a+b cos)^m (c+d cos)^n
    if has(sec_) and has(cos_):
        M = _umatch(u, (g_*sec_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*csc_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_]
    # 1.2.3 (g sec)^p (a+b cos)^m (c+d sec)^n
    if has(sec_) and has(cos_):
        M = _umatch(u, (g_*sec_(e_ + f_*x))**p_ * (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*csc_(ap(M)))**M[p_] * (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 1.3.1 (a+b cos)^m (c+d cos)^n (A+B cos)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_ * (A_ + B_*cos_(e_ + f_*x)))
        if M is not None and M[B_] != 0:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_] * (M[A_] + M[B_]*sin_(ap(M)))
    # 1.4.1 (a+b cos)^m (A+B cos+C cos^2)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (A_ + B_*cos_(e_ + f_*x) + C_*cos_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[A_] + M[B_]*sin_(ap(M)) + M[C_]*sin_(ap(M))**2)
    # 1.4.1 (a+b cos)^m (A+C cos^2)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (A_ + C_*cos_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[A_] + M[C_]*sin_(ap(M))**2)
    # 1.4.2 (a+b cos)^m (c+d cos)^n (A+B cos+C cos^2)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_ * (A_ + B_*cos_(e_ + f_*x) + C_*cos_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_] * (M[A_] + M[B_]*sin_(ap(M)) + M[C_]*sin_(ap(M))**2)
    # 1.4.2 (a+b cos)^m (c+d cos)^n (A+C cos^2)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x))**m_ * (c_ + d_*cos_(e_ + f_*x))**n_ * (A_ + C_*cos_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] + M[b_]*sin_(ap(M)))**M[m_] * (M[c_] + M[d_]*sin_(ap(M)))**M[n_] * (M[A_] + M[C_]*sin_(ap(M))**2)
    # 1.7 (a+b (c cos)^n)^p   [single]
    if has(cos_) and not_mul:
        M = _umatch(u, (a_ + b_*(c_*cos_(e_ + f_*x))**n_)**p_)
        if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
            return (M[a_] + M[b_]*(M[c_]*sin_(ap(M)))**M[n_])**M[p_]
    # 1.7 (d TRIG)^m (a+b (c cos)^n)^p
    for ftrig, fres, sgn in [(cos_, sin_, 1), (sin_, cos_, -1), (cot_, tan_, -1),
                             (tan_, cot_, -1), (csc_, sec_, -1), (sec_, csc_, 1)]:
        if has(ftrig) and has(cos_):
            M = _umatch(u, (d_*ftrig(e_ + f_*x))**m_ * (a_ + b_*(c_*cos_(e_ + f_*x))**n_)**p_)
            if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
                return (sgn*M[d_]*fres(ap(M)))**M[m_] * (M[a_] + M[b_]*(M[c_]*sin_(ap(M)))**M[n_])**M[p_]
    # 1.7 (a+b cos^n)^m (A+B cos^n)
    if has(cos_):
        M = _umatch(u, (a_ + b_*cos_(e_ + f_*x)**n_)**m_ * (A_ + B_*cos_(e_ + f_*x)**n_))
        if M is not None and M[B_] != 0 and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[m_])):
            return (M[a_] + M[b_]*sin_(ap(M))**M[n_])**M[m_] * (M[A_] + M[B_]*sin_(ap(M))**M[n_])

    # ================= Cotangent to tangent =================
    # 2.0 (a cos)^m (b cot)^n
    if has(cos_) and has(cot_):
        M = _umatch(u, (a_*cos_(e_ + f_*x))**m_ * (b_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*sin_(ap(M)))**M[m_] * (-M[b_]*tan_(ap(M)))**M[n_]
    # 2.0 (a sin)^m (b cot)^n
    if has(sin_) and has(cot_):
        M = _umatch(u, (a_*sin_(e_ + f_*x))**m_ * (b_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*cos_(am(M)))**M[m_] * (-M[b_]*tan_(am(M)))**M[n_]
    # 2.0 (a csc)^m (b cot)^n
    if has(csc_) and has(cot_):
        M = _umatch(u, (a_*csc_(e_ + f_*x))**m_ * (b_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*sec_(am(M)))**M[m_] * (-M[b_]*tan_(am(M)))**M[n_]
    # 2.0 (a sec)^m (b cot)^n
    if has(sec_) and has(cot_):
        M = _umatch(u, (a_*sec_(e_ + f_*x))**m_ * (b_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_]*csc_(ap(M)))**M[m_] * (-M[b_]*tan_(ap(M)))**M[n_]
    # 2.1.1 (a+b cot)^n
    if has(cot_) and not_mul:
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[n_]
    # 2.1.2 (d csc)^m (a+b cot)^n   [a required]
    if has(csc_) and has(cot_):
        M = _umatch(u, (d_*csc_(e_ + f_*x))**m_ * (a_ + b_*cot_(e_ + f_*x))**n_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[d_]*sec_(am(M)))**M[m_] * (M[a_] - M[b_]*tan_(am(M)))**M[n_]
    # 2.1.2 (d sin)^m (a+b cot)^n   [a required]
    if has(sin_) and has(cot_):
        M = _umatch(u, (d_*sin_(e_ + f_*x))**m_ * (a_ + b_*cot_(e_ + f_*x))**n_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[d_]*cos_(am(M)))**M[m_] * (M[a_] - M[b_]*tan_(am(M)))**M[n_]
    # 2.1.3 (d cos)^m (a+b cot)^n   [a required]
    if has(cos_) and has(cot_):
        M = _umatch(u, (d_*cos_(e_ + f_*x))**m_ * (a_ + b_*cot_(e_ + f_*x))**n_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[d_]*sin_(ap(M)))**M[m_] * (M[a_] - M[b_]*tan_(ap(M)))**M[n_]
    # 2.1.3 (d sec)^m (a+b cot)^n   [a required]
    if has(sec_) and has(cot_):
        M = _umatch(u, (d_*sec_(e_ + f_*x))**m_ * (a_ + b_*cot_(e_ + f_*x))**n_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[d_]*csc_(ap(M)))**M[m_] * (M[a_] - M[b_]*tan_(ap(M)))**M[n_]
    # 2.2.1 (a+b cot)^m (c+d cot)^n
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*tan_(ap(M)))**M[n_]
    # 2.2.3 (g cot)^p (a+b cot)^m (c+d cot)^n
    if has(cot_):
        M = _umatch(u, (g_*cot_(e_ + f_*x))**p_ * (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*cot_(e_ + f_*x))**n_)
        if M is not None:
            return (-M[g_]*tan_(ap(M)))**M[p_] * (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*tan_(ap(M)))**M[n_]
    # 2.2.3 (g cot)^p (a+b cot)^m (c+d tan)^n
    if has(cot_) and has(tan_):
        M = _umatch(u, (g_*cot_(e_ + f_*x))**p_ * (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*tan_(e_ + f_*x))**n_)
        if M is not None:
            return (-M[g_]*tan_(ap(M)))**M[p_] * (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*cot_(ap(M)))**M[n_]
    # 2.3.1 (a+b cot)^m (c+d cot)^n (A+B cot)
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*cot_(e_ + f_*x))**n_ * (A_ + B_*cot_(e_ + f_*x)))
        if M is not None and M[B_] != 0:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*tan_(ap(M)))**M[n_] * (M[A_] - M[B_]*tan_(ap(M)))
    # 2.4.1 (a+b cot)^m (A+B cot+C cot^2)
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (A_ + B_*cot_(e_ + f_*x) + C_*cot_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[A_] - M[B_]*tan_(ap(M)) + M[C_]*tan_(ap(M))**2)
    # 2.4.1 (a+b cot)^m (A+C cot^2)
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (A_ + C_*cot_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[A_] + M[C_]*tan_(ap(M))**2)
    # 2.4.2 (a+b cot)^m (c+d cot)^n (A+B cot+C cot^2)
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*cot_(e_ + f_*x))**n_ * (A_ + B_*cot_(e_ + f_*x) + C_*cot_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*tan_(ap(M)))**M[n_] * (M[A_] - M[B_]*tan_(ap(M)) + M[C_]*tan_(ap(M))**2)
    # 2.4.2 (a+b cot)^m (c+d cot)^n (A+C cot^2)
    if has(cot_):
        M = _umatch(u, (a_ + b_*cot_(e_ + f_*x))**m_ * (c_ + d_*cot_(e_ + f_*x))**n_ * (A_ + C_*cot_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] - M[b_]*tan_(ap(M)))**M[m_] * (M[c_] - M[d_]*tan_(ap(M)))**M[n_] * (M[A_] + M[C_]*tan_(ap(M))**2)
    # 2.7 (a+b (c cot)^n)^p   [single]
    if has(cot_) and not_mul:
        M = _umatch(u, (a_ + b_*(c_*cot_(e_ + f_*x))**n_)**p_)
        if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
            return (M[a_] + M[b_]*(-M[c_]*tan_(ap(M)))**M[n_])**M[p_]
    # 2.7 (d TRIG)^m (a+b (c cot)^n)^p
    for ftrig, fres, sgn in [(cos_, sin_, 1), (sin_, cos_, -1), (cot_, tan_, -1),
                             (tan_, cot_, -1), (csc_, sec_, -1), (sec_, csc_, 1)]:
        if has(ftrig) and has(cot_):
            M = _umatch(u, (d_*ftrig(e_ + f_*x))**m_ * (a_ + b_*(c_*cot_(e_ + f_*x))**n_)**p_)
            if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
                return (sgn*M[d_]*fres(ap(M)))**M[m_] * (M[a_] + M[b_]*(-M[c_]*tan_(ap(M)))**M[n_])**M[p_]

    # ================= Cosecant to secant =================
    # 3.1.1 (a+b sec)^n
    if has(sec_) and not_mul:
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[n_]
    # 3.1.2 (g sec)^p (a+b sec)^m   [a required]
    if has(sec_):
        M = _umatch(u, (g_*sec_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[g_]*csc_(ap(M)))**M[p_] * (M[a_] + M[b_]*csc_(ap(M)))**M[m_]
    # 3.1.3 (g sin)^p (a+b sec)^m   [a required]
    if has(sin_) and has(sec_):
        M = _umatch(u, (g_*sin_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[g_]*cos_(am(M)))**M[p_] * (M[a_] - M[b_]*csc_(am(M)))**M[m_]
    # 3.1.3 (g csc)^p (a+b sec)^m   [a required]
    if has(csc_) and has(sec_):
        M = _umatch(u, (g_*csc_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (M[g_]*sec_(am(M)))**M[p_] * (M[a_] - M[b_]*csc_(am(M)))**M[m_]
    # 3.1.4 (g tan)^p (a+b sec)^m   [a required]
    if has(tan_) and has(sec_):
        M = _umatch(u, (g_*tan_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_)
        if M is not None and not eager_EqQ(M[a_], 0):
            return (-M[g_]*cot_(ap(M)))**M[p_] * (M[a_] + M[b_]*csc_(ap(M)))**M[m_]
    # 3.2.1 (a+b sec)^m (c+d sec)^n
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 3.2.2 (g sec)^p (a+b sec)^m (c+d sec)^n
    if has(sec_):
        M = _umatch(u, (g_*sec_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*csc_(ap(M)))**M[p_] * (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 3.2.2 (g cos)^p (a+b sec)^m (c+d sec)^n
    if has(cos_) and has(sec_):
        M = _umatch(u, (g_*cos_(e_ + f_*x))**p_ * (a_ + b_*sec_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_)
        if M is not None:
            return (M[g_]*sin_(ap(M)))**M[p_] * (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_]
    # 3.3.1 (a+b sec)^m (d sec)^n (A+B sec)
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (d_*sec_(e_ + f_*x))**n_ * (A_ + B_*sec_(e_ + f_*x)))
        if M is not None and M[B_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[d_]*csc_(ap(M)))**M[n_] * (M[A_] + M[B_]*csc_(ap(M)))
    # 3.3.1 (a+b sec)^m (c+d sec)^n (A+B sec)^p
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (c_ + d_*sec_(e_ + f_*x))**n_ * (A_ + B_*sec_(e_ + f_*x))**p_)
        if M is not None and M[B_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[c_] + M[d_]*csc_(ap(M)))**M[n_] * (M[A_] + M[B_]*csc_(ap(M)))**M[p_]
    # 3.4.1 (a+b sec)^m (A+B sec+C sec^2)
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (A_ + B_*sec_(e_ + f_*x) + C_*sec_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[A_] + M[B_]*csc_(ap(M)) + M[C_]*csc_(ap(M))**2)
    # 3.4.1 (a+b sec)^m (A+C sec^2)
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (A_ + C_*sec_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[A_] + M[C_]*csc_(ap(M))**2)
    # 3.4.2 (a+b sec)^m (d sec)^n (A+B sec+C sec^2)
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (d_*sec_(e_ + f_*x))**n_ * (A_ + B_*sec_(e_ + f_*x) + C_*sec_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0 and M[B_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[d_]*csc_(ap(M)))**M[n_] * (M[A_] + M[B_]*csc_(ap(M)) + M[C_]*csc_(ap(M))**2)
    # 3.4.2 (a+b sec)^m (d sec)^n (A+C sec^2)
    if has(sec_):
        M = _umatch(u, (a_ + b_*sec_(e_ + f_*x))**m_ * (d_*sec_(e_ + f_*x))**n_ * (A_ + C_*sec_(e_ + f_*x)**2))
        if M is not None and M[C_] != 0:
            return (M[a_] + M[b_]*csc_(ap(M)))**M[m_] * (M[d_]*csc_(ap(M)))**M[n_] * (M[A_] + M[C_]*csc_(ap(M))**2)
    # 3.7 (a+b (c csc)^n)^p   [single]
    if has(csc_) and not_mul:
        M = _umatch(u, (a_ + b_*(c_*csc_(e_ + f_*x))**n_)**p_)
        if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
            return (M[a_] + M[b_]*(-M[c_]*sec_(ap(M)))**M[n_])**M[p_]
    # 3.7 (d TRIG)^m (a+b (c csc)^n)^p
    for ftrig, fres, sgn in [(cos_, sin_, 1), (sin_, cos_, -1), (cot_, tan_, -1),
                             (tan_, cot_, -1), (csc_, sec_, -1), (sec_, csc_, 1)]:
        if has(ftrig) and has(csc_):
            M = _umatch(u, (d_*ftrig(e_ + f_*x))**m_ * (a_ + b_*(c_*csc_(e_ + f_*x))**n_)**p_)
            if M is not None and not (eager_EqQ(M[a_], 0) and eager_IntegerQ(M[p_])):
                if ftrig is csc_ and (eager_EqQ(M[n_], 2) and eager_EqQ(M[p_], 1)):
                    continue
                return (sgn*M[d_]*fres(ap(M)))**M[m_] * (M[a_] + M[b_]*(-M[c_]*sec_(ap(M)))**M[n_])**M[p_]

    # catch-all
    return u

def DeactivateTrigAux(u, x):
    # Replaces active trig/hyperbolic functions of a linear argument with the
    # corresponding *inert* trig markers (see ActivateTrig / InertSin ...).
    if eager_AtomQ(u):
        return u
    elif eager_TrigQ(u) and eager_LinearQ(u.args[0], x):
        v = eager_ExpandToSum(u.args[0], x)
        if SinQ(u):
            return InertSin(v)
        elif CosQ(u):
            return InertCos(v)
        elif TanQ(u):
            return InertTan(v)
        elif CotQ(u):
            return InertCot(v)
        elif SecQ(u):
            return InertSec(v)
        return InertCsc(v)
    elif eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
        v = eager_ExpandToSum(I*u.args[0], x)
        if SinhQ(u):
            return -I*InertSin(v)
        elif CoshQ(u):
            return InertCos(v)
        elif TanhQ(u):
            return -I*InertTan(v)
        elif CothQ(u):
            return I*InertCot(v)
        elif SechQ(u):
            return InertSec(v)
        return I*InertCsc(v)
    return u.func(*[DeactivateTrigAux(i, x) for i in u.args])

def PowerOfInertTrigSumQ(u, func, x):
    p_ = Wild('p', exclude=[x])
    q_ = Wild('q', exclude=[x])
    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x])
    c_ = Wild('c', exclude=[x])
    d_ = Wild('d', exclude=[x])
    n_ = Wild('n', exclude=[x])
    w_ = Wild('w')

    pattern = (a_ + b_*(c_*func(w_))**p_)**n_
    match = u.match(pattern)
    if match:
        keys = [a_, b_, c_, n_, p_, w_]
        if len(keys) == len(match):
            return True

    pattern = (a_ + b_*(d_*func(w_))**p_ + c_*(d_*func(w_))**q_)**n_
    match = u.match(pattern)
    if match:
        keys = [a_, b_, c_, d_, n_, p_, q_, w_]
        if len(keys) == len(match):
            return True
    return False

def eager_PiecewiseLinearQ(*args):
    # (* If the derivative of u wrt x is a constant wrt x, PiecewiseLinearQ[u,x] returns True;
    # else it returns False. *)
    if len(args) == 3:
        u, v, x = args
        return eager_PiecewiseLinearQ(u, x) and eager_PiecewiseLinearQ(v, x)

    u, x = args
    if eager_LinearQ(u, x):
        return True

    c_ = Wild('c', exclude=[x])
    F_ = Wild('F', exclude=[x])
    v_ = Wild('v')
    match = u.match(Log(c_*F_**v_))
    if match:
        if len(match) == 3:
            if eager_LinearQ(match[v_], x):
                return True
    try:
        F = type(u)
        G = type(u.args[0])
        v = u.args[0].args[0]
        if eager_LinearQ(v, x):
            if eager_MemberQ([[atanh, tanh], [atanh, coth], [acoth, coth], [acoth, tanh], [atan, tan], [atan, cot], [acot, cot], [acot, tan]], [F, G]):
                return True
    except:
        pass
    return False

def KnownTrigIntegrandQ(lst, u, x):
    if u == 1:
        return True
    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x, 0])
    func_ = WildFunction('func')
    m_ = Wild('m', exclude=[x])
    A_ = Wild('A', exclude=[x])
    B_ = Wild('B', exclude=[x, 0])
    C_ = Wild('C', exclude=[x, 0])

    match = u.match((a_ + b_*func_)**m_)
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    match = u.match((a_ + b_*func_)**m_*(A_ + B_*func_))
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    match = u.match(A_ + C_*func_**2)
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    match = u.match(A_ + B_*func_ + C_*func_**2)
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    match = u.match((a_ + b_*func_)**m_*(A_ + C_*func_**2))
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    match = u.match((a_ + b_*func_)**m_*(A_ + B_*func_ + C_*func_**2))
    if match:
        func = match[func_]
        if eager_LinearQ(func.args[0], x) and eager_MemberQ(lst, func.func):
            return True

    return False

# Rubi passes LOWERCASE heads here -- `KnownTrigIntegrandQ[{sin,cos},u,x]` -- and in
# Rubi lowercase sin/cos/tan/... are the INERT trig markers (`Rubi`sin`), not the
# active Sin/Cos. Passing SymPy's ACTIVE sin/cos made these predicates answer False
# for every integrand the rules actually hand them: the guarded rules match on
# `InertSin(...)`/`InertTan(...)` patterns, so `u_` always binds inert trig. That
# silently disabled all 64 rules guarded by these four predicates.
def eager_KnownSineIntegrandQ(u, x):
    return KnownTrigIntegrandQ([InertSin, InertCos], u, x)

def eager_KnownTangentIntegrandQ(u, x):
    return KnownTrigIntegrandQ([InertTan], u, x)

def eager_KnownCotangentIntegrandQ(u, x):
    return KnownTrigIntegrandQ([InertCot], u, x)

def eager_KnownSecantIntegrandQ(u, x):
    return KnownTrigIntegrandQ([InertSec, InertCsc], u, x)

def eager_TryPureTanSubst(u, x):
    a_ = Wild('a', exclude=[x])
    b_ = Wild('b', exclude=[x])
    c_ = Wild('c', exclude=[x])
    G_ = Wild('G')

    F = u.func
    try:
        if eager_MemberQ([atan, acot, atanh, acoth], F):
            match = u.args[0].match(c_*(a_ + b_*G_))
            if match:
                if len(match) == 4:
                    G = match[G_]
                    if eager_MemberQ([tan, cot, tanh, coth], G.func):
                        if eager_LinearQ(G.args[0], x):
                            # Rubi returns Not[MatchQ[...]]: a MATCH means the pure-tan
                            # substitution must NOT be tried. This was returning True on
                            # a match -- the predicate was inverted end to end, so Rubi
                            # tried the substitution in exactly the cases it must skip.
                            return False
    except:
        pass

    return True

def TryTanhSubst(u, x):
    if eager_LogQ(u):
        return False
    elif not eager_FalseQ(eager_FunctionOfLinear(u, x)):
        return False

    a_ = Wild('a', exclude=[x])
    m_ = Wild('m', exclude=[x])
    p_ = Wild('p', exclude=[x])
    r_, s_, t_, n_, b_, f_, g_ = map(Wild, 'rstnbfg')

    match = u.match(r_*(s_ + t_)**n_)
    if match:
        if len(match) == 4:
            r, s, t, n = [match[i] for i in [r_, s_, t_, n_]]
            if eager_IntegerQ(n) and eager_PositiveQ(n):
                return False

    match = u.match(1/(a_ + b_*f_**n_))
    if match:
        if len(match) == 4:
            a, b, f, n = [match[i] for i in [a_, b_, f_, n_]]
            if SinhCoshQ(f) and eager_IntegerQ(n) and n > 2:
                return False

    match = u.match(f_*g_)
    if match:
        if len(match) == 2:
            f, g = match[f_], match[g_]
            if SinhCoshQ(f) and SinhCoshQ(g):
                if eager_IntegersQ(f.args[0]/x, g.args[0]/x):
                    return False

    match = u.match(r_*(a_*s_**m_)**p_)
    if match:
        if len(match) == 5:
            r, a, s, m, p = [match[i] for i in [r_, a_, s_, m_, p_]]
            if eager_Not(m==2 and (s == Sech(x) or s == Csch(x))):
                return False

    if u != eager_ExpandIntegrand(u, x):
        return False

    return True

def TryPureTanhSubst(u, x):
    F = u.func
    a_ = Wild('a', exclude=[x])
    G_ = Wild('G')

    if F == sym_log:
        return False

    match = u.args[0].match(a_*G_)
    if match and len(match) == 2:
        G = match[G_].func
        if eager_MemberQ([atanh, acoth], F) and eager_MemberQ([tanh, coth], G):
            return False

    if eager_PolynomialQ(u, x):
        return False

    try:
        if u != eager_ExpandIntegrand(u, x):
            return False
    except (ValueError, TypeError, AttributeError):
        pass

    return True

def AbsurdNumberGCD(*seq):
    # (* m, n, ... must be absurd numbers.  AbsurdNumberGCD[m,n,...] returns the gcd of m, n, ... *)
    lst = list(seq)
    if eager_Length(lst) == 1:
        return eager_First(lst)
    return AbsurdNumberGCDList(FactorAbsurdNumber(eager_First(lst)), FactorAbsurdNumber(AbsurdNumberGCD(*eager_Rest(lst))))

def AbsurdNumberGCDList(lst1, lst2):
    # (* lst1 and lst2 must be absurd number prime factorization lists. *)
    # (* AbsurdNumberGCDList[lst1,lst2] returns the gcd of the absurd numbers represented by lst1 and lst2. *)
    if lst1 == []:
        return Mul(*[i[0]**Min(i[1],0) for i in lst2])
    elif lst2 == []:
        return Mul(*[i[0]**Min(i[1],0) for i in lst1])
    elif lst1[0][0] == lst2[0][0]:
        if lst1[0][1] <= lst2[0][1]:
            return lst1[0][0]**lst1[0][1]*AbsurdNumberGCDList(eager_Rest(lst1), eager_Rest(lst2))
        return lst1[0][0]**lst2[0][1]*AbsurdNumberGCDList(eager_Rest(lst1), eager_Rest(lst2))
    elif lst1[0][0] < lst2[0][0]:
        if lst1[0][1] < 0:
            return lst1[0][0]**lst1[0][1]*AbsurdNumberGCDList(eager_Rest(lst1), lst2)
        return AbsurdNumberGCDList(eager_Rest(lst1), lst2)
    elif lst2[0][1] < 0:
        return lst2[0][0]**lst2[0][1]*AbsurdNumberGCDList(lst1, eager_Rest(lst2))
    return AbsurdNumberGCDList(lst1, eager_Rest(lst2))

def eager_ExpandTrigExpand(u, F, v, m, n, x):
    """Rubi ``ExpandTrigExpand[u, F, v, m, n, x]``::

        With[{w = ReplaceAll[Expand[TrigExpand[F[n*x]]^m, x], x -> v]},
          If[SumQ[w], Map[Function[u*#], w], u*w]]

    ``F`` is a function HEAD (Sin, Cos, ...) that Mathematica APPLIES to ``n*x``. In
    our rules it arrives as the binding of a function-head wildcard, i.e. a HeadRef,
    so it has to be resolved to the SymPy class and called -- substituting into it
    (the previous behaviour) is only correct when F happens to be an expression in x.
    """
    from sympy_wolfram.functions_eager import head_to_class
    cls = head_to_class(F)
    if cls is not None:
        inner = cls(n*x)
    elif callable(F) and not isinstance(F, Basic):
        inner = F(n*x)
    else:
        inner = F.xreplace({x: n*x})
    w = Expand(TrigExpand(inner)**m).xreplace({x: v})
    if eager_SumQ(w):
        t = 0
        for i in w.args:
            t += u*i
        return t
    else:
        return u*w

def eager_ExpandTrigReduce(*args):
    if len(args) == 3:
        u = args[0]
        v = args[1]
        x = args[2]
        w = eager_ExpandTrigReduce(v, x)
        if eager_SumQ(w):
            t = 0
            for i in w.args:
                t += u*i
            return t
        else:
            return u*w
    else:
        u = args[0]
        x = args[1]
        return ExpandTrigReduceAux(u, x)

def ExpandTrigReduceAux(u, x):
    v = TrigReduce(u).expand()
    if eager_SumQ(v):
        t = 0
        for i in v.args:
            t += NormalizeTrig(i, x)
        return t
    return NormalizeTrig(v, x)

def NormalizeTrig(v, x):
    a = Wild('a', exclude=[x])
    n = Wild('n', exclude=[x, 0])
    F = Wild('F')
    expr = a*F**n
    M = v.match(expr)
    if M and len(M[F].args) == 1 and eager_PolynomialQ(M[F].args[0], x) and eager_Exponent(M[F].args[0], x) > 0:
        u = M[F].args[0]
        return M[a]*M[F].xreplace({u: eager_ExpandToSum(u, x)})**M[n]
    else:
        return v
#=================================
def TrigToExp(expr):
    ex = expr.rewrite(sin, sym_exp).rewrite(cos, sym_exp).rewrite(tan, sym_exp).rewrite(sec, sym_exp).rewrite(csc, sym_exp).rewrite(cot, sym_exp)
    return ex

def eager_ExpandTrigToExp(u, *args):
    if len(args) == 1:
        x = args[0]
        return eager_ExpandTrigToExp(1, u, x)
    else:
        v = args[0]
        x = args[1]
        w = TrigToExp(v)
        k = 0
        if eager_SumQ(w):
            for i in w.args:
                k += eager_SimplifyIntegrand(u*i, x)
            w = k
        else:
            w = eager_SimplifyIntegrand(u*w, x)
        return eager_ExpandIntegrand(eager_FreeFactors(w, x), eager_NonfreeFactors(w, x),x)
#======================================
def TrigReduce(i):
    """
    TrigReduce(expr) rewrites products and powers of trigonometric functions in expr in terms of trigonometric functions with combined arguments.

    Examples
    ========

    >>> from sympy import sin, cos
    >>> from rubi_rules.utils.utility_functions import TrigReduce
    >>> from sympy.abc import x
    >>> TrigReduce(cos(x)**2)
    cos(2*x)/2 + 1/2
    >>> TrigReduce(cos(x)**2*sin(x))
    sin(x)/4 + sin(3*x)/4
    >>> TrigReduce(cos(x)**2+sin(x))
    sin(x) + cos(2*x)/2 + 1/2

    """
    if eager_SumQ(i):
        t = 0
        for k in i.args:
            t += TrigReduce(k)
        return t
    if eager_ProductQ(i):
        if any(eager_PowerQ(k) for k in i.args):
            if (i.rewrite((sin, sinh), sym_exp).rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, sin)).has(I, cosh, sinh):
                return i.rewrite((sin, sinh), sym_exp).rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, sin).simplify()
            else:
                return i.rewrite((sin, sinh), sym_exp).rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, sin)
        else:
            a = Wild('a')
            b = Wild('b')
            v = Wild('v')
            Match = i.match(v*sin(a)*cos(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*sin(a)*cos(b), v*S(1)/2*(sin(a + b) + sin(a - b)))
            Match = i.match(v*sin(a)*sin(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*sin(a)*sin(b), v*S(1)/2*(cos(a - b) - cos(a + b)))
            Match = i.match(v*cos(a)*cos(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*cos(a)*cos(b), v*S(1)/2*(cos(a + b) + cos(a - b)))
            Match = i.match(v*sinh(a)*cosh(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*sinh(a)*cosh(b), v*S(1)/2*(sinh(a + b) + sinh(a - b)))
            Match = i.match(v*sinh(a)*sinh(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*sinh(a)*sinh(b), v*S(1)/2*(cosh(a + b) - cosh(a - b)))
            Match = i.match(v*cosh(a)*cosh(b))
            if Match:
                a = Match[a]
                b = Match[b]
                v = Match[v]
                return i.subs(v*cosh(a)*cosh(b), v*S(1)/2*(cosh(a + b) + cosh(a - b)))

    if eager_PowerQ(i):
        if i.has(sin, sinh):
            if (i.rewrite((sin, sinh), sym_exp).expand().rewrite(sym_exp, sin)).has(I, cosh, sinh):
                return i.rewrite((sin, sinh), sym_exp).expand().rewrite(sym_exp, sin).simplify()
            else:
                return i.rewrite((sin, sinh), sym_exp).expand().rewrite(sym_exp, sin)
        if i.has(cos, cosh):
            if (i.rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, cos)).has(I, cosh, sinh):
                return i.rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, cos).simplify()
            else:
                return i.rewrite((cos, cosh), sym_exp).expand().rewrite(sym_exp, cos)
    return i

def eager_FunctionOfTrig(u, *args):
    # If u is a function of trig functions of v where v is a linear function of x,
    # FunctionOfTrig[u,x] returns v; else it returns False.
    if len(args) == 1:
        x = args[0]
        v = eager_FunctionOfTrig(u, None, x)
        if v:
            return v
        else:
            return False
    else:
        v, x = args
        if eager_AtomQ(u):
            if u == x:
                return False
            else:
                return v
        if eager_TrigQ(u) and eager_LinearQ(u.args[0], x):
            if v is None:
                return u.args[0]
            else:
                a = eager_Coefficient(v, x, 0)
                b = eager_Coefficient(v, x, 1)
                c = eager_Coefficient(u.args[0], x, 0)
                d = eager_Coefficient(u.args[0], x, 1)
                if ZeroQ(a*d - b*c) and eager_RationalQ(b/d):
                    return a/eager_Numerator(b/d) + b*x/eager_Numerator(b/d)
                else:
                    return False
        if eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
            if v is None:
                return I*u.args[0]
            a = eager_Coefficient(v, x, 0)
            b = eager_Coefficient(v, x, 1)
            c = I*eager_Coefficient(u.args[0], x, 0)
            d = I*eager_Coefficient(u.args[0], x, 1)
            if ZeroQ(a*d - b*c) and eager_RationalQ(b/d):
                return a/eager_Numerator(b/d) + b*x/eager_Numerator(b/d)
            else:
                return False
        if CalculusQ(u):
            return False
        else:
            w = v
            for i in u.args:
                w = eager_FunctionOfTrig(i, w, x)
                if eager_FalseQ(w):
                    return False
            return w

def AlgebraicTrigFunctionQ(u, x):
    # If u is algebraic function of trig functions, AlgebraicTrigFunctionQ(u,x) returns True; else it returns False.
    if eager_AtomQ(u):
        return True
    elif eager_TrigQ(u) and eager_LinearQ(u.args[0], x):
        return True
    elif eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
        return True
    elif eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            return AlgebraicTrigFunctionQ(u.base, x)
    elif eager_ProductQ(u) or eager_SumQ(u):
        for i in u.args:
            if not AlgebraicTrigFunctionQ(i, x):
                return False
        return True

    return False

def FunctionOfHyperbolic(u, *x):
    # If u is a function of hyperbolic trig functions of v where v is linear in x,
    # FunctionOfHyperbolic(u,x) returns v; else it returns False.
    if len(x) == 1:
        x = x[0]
        v = FunctionOfHyperbolic(u, None, x)
        if v is None:
            return False
        else:
            return v
    else:
        v = x[0]
        x = x[1]
        if eager_AtomQ(u):
            if u == x:
                return False
            return v
        if eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
            if v is None:
                return u.args[0]
            a = eager_Coefficient(v, x, 0)
            b = eager_Coefficient(v, x, 1)
            c = eager_Coefficient(u.args[0], x, 0)
            d = eager_Coefficient(u.args[0], x, 1)
            if ZeroQ(a*d - b*c) and eager_RationalQ(b/d):
                return a/eager_Numerator(b/d) + b*x/eager_Numerator(b/d)
            else:
                return False
        if CalculusQ(u):
            return False
        w = v
        for i in u.args:
            if w == FunctionOfHyperbolic(i, w, x):
                return False
        return w

def eager_FunctionOfQ(v, u, x, PureFlag=False):
    # v is a function of x. If u is a function of v,  FunctionOfQ(v, u, x) returns True; else it returns False. *)
    if eager_FreeQ(u, x):
        return False
    elif eager_AtomQ(v):
        return True
    elif eager_ProductQ(v) and eager_Not(eager_EqQ(eager_FreeFactors(v, x), 1)):
        return eager_FunctionOfQ(eager_NonfreeFactors(v, x), u, x, PureFlag)
    elif PureFlag:
        if SinQ(v) or CscQ(v):
            return PureFunctionOfSinQ(u, v.args[0], x)
        elif CosQ(v) or SecQ(v):
            return PureFunctionOfCosQ(u, v.args[0], x)
        elif TanQ(v):
            return PureFunctionOfTanQ(u, v.args[0], x)
        elif CotQ(v):
            return PureFunctionOfCotQ(u, v.args[0], x)
        elif SinhQ(v) or CschQ(v):
            return PureFunctionOfSinhQ(u, v.args[0], x)
        elif CoshQ(v) or SechQ(v):
            return PureFunctionOfCoshQ(u, v.args[0], x)
        elif TanhQ(v):
            return PureFunctionOfTanhQ(u, v.args[0], x)
        elif CothQ(v):
            return PureFunctionOfCothQ(u, v.args[0], x)
        else:
            return FunctionOfExpnQ(u, v, x) != False
    elif SinQ(v) or CscQ(v):
        return FunctionOfSinQ(u, v.args[0], x)
    elif CosQ(v) or SecQ(v):
        return FunctionOfCosQ(u, v.args[0], x)
    elif TanQ(v) or CotQ(v):
        FunctionOfTanQ(u, v.args[0], x)
    elif SinhQ(v) or CschQ(v):
        return FunctionOfSinhQ(u, v.args[0], x)
    elif CoshQ(v) or SechQ(v):
        return FunctionOfCoshQ(u, v.args[0], x)
    elif TanhQ(v) or CothQ(v):
        return FunctionOfTanhQ(u, v.args[0], x)
    return FunctionOfExpnQ(u, v, x) != False



def FunctionOfExpnQ(u, v, x):
    if u == v:
        return 1
    if eager_AtomQ(u):
        if u == x:
            return False
        else:
            return 0
    if CalculusQ(u):
        return False
    if eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            if ZeroQ(u.base - v):
                if eager_IntegerQ(u.exp):
                    return u.exp
                else:
                    return 1
            if eager_PowerQ(v):
                if eager_FreeQ(v.exp, x) and ZeroQ(u.base-v.base):
                    if eager_RationalQ(v.exp):
                        if eager_RationalQ(u.exp) and eager_IntegerQ(u.exp/v.exp) and (v.exp>0 or u.exp<0):
                            return u.exp/v.exp
                        else:
                            return False
                    if eager_IntegerQ(eager_Simplify(u.exp/v.exp)):
                        return eager_Simplify(u.exp/v.exp)
                    else:
                        return False
            return FunctionOfExpnQ(u.base, v, x)
    if eager_ProductQ(u) and eager_Not(eager_EqQ(eager_FreeFactors(u, x), 1)):
        return FunctionOfExpnQ(eager_NonfreeFactors(u, x), v, x)
    if eager_ProductQ(u) and eager_ProductQ(v):
        deg1 = FunctionOfExpnQ(eager_First(u), eager_First(v), x)
        if deg1==False:
            return False
        deg2 = FunctionOfExpnQ(eager_Rest(u), eager_Rest(v), x);
        if deg1==deg2 and eager_FreeQ(eager_Simplify(u/v^deg1), x):
            return deg1
        else:
            return False
    lst = []
    for i in u.args:
        if FunctionOfExpnQ(i, v, x) is False:
            return False
        lst.append(FunctionOfExpnQ(i, v, x))
    return eager_Apply(eager_GCD, lst)

def PureFunctionOfSinQ(u, v, x):
    # If u is a pure function of Sin(v) and/or Csc(v), PureFunctionOfSinQ(u, v, x) returns True; else it returns False.
    if eager_AtomQ(u):
        return u!=x
    if CalculusQ(u):
        return False
    if eager_TrigQ(u) and ZeroQ(u.args[0]-v):
        return SinQ(u) or CscQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfSinQ(i, v, x)):
            return False
    return True

def PureFunctionOfCosQ(u, v, x):
    # If u is a pure function of Cos(v) and/or Sec(v), PureFunctionOfCosQ(u, v, x) returns True; else it returns False.
    if eager_AtomQ(u):
        return u!=x
    if CalculusQ(u):
        return False
    if eager_TrigQ(u) and ZeroQ(u.args[0]-v):
        return CosQ(u) or SecQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfCosQ(i, v, x)):
            return False
    return True

def PureFunctionOfTanQ(u, v, x):
    # If u is a pure function of Tan(v) and/or Cot(v), PureFunctionOfTanQ(u, v, x) returns True; else it returns False.
    if eager_AtomQ(u):
        return u!=x
    if CalculusQ(u):
        return False
    if eager_TrigQ(u) and ZeroQ(u.args[0]-v):
        return TanQ(u) or CotQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfTanQ(i, v, x)):
            return False
    return True

def PureFunctionOfCotQ(u, v, x):
    # If u is a pure function of Cot(v), PureFunctionOfCotQ(u, v, x) returns True; else it returns False.
    if eager_AtomQ(u):
        return u!=x
    if CalculusQ(u):
        return False
    if eager_TrigQ(u) and ZeroQ(u.args[0]-v):
        return CotQ(u)
    for i in u.args:
        if eager_Not(PureFunctionOfCotQ(i, v, x)):
            return False
    return True

def FunctionOfCosQ(u, v, x):
    # If u is a function of Cos[v], FunctionOfCosQ[u,v,x] returns True; else it returns False.
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        # Basis: If m integer, Cos[m*v]^n is a function of Cos[v]. *)
        return CosQ(u) or SecQ(u)
    elif eager_IntegerPowerQ(u):
        if eager_TrigQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if eager_EvenQ(u.exp):
                # Basis: If m integer and n even, Trig[m*v]^n is a function of Cos[v]. *)
                return True
            return FunctionOfCosQ(u.base, v, x)
    elif eager_ProductQ(u):
        lst = FindTrigFactor(sin, csc, u, v, False)
        if ListQ(lst):
            # (* Basis: If m integer and n odd, Sin[m*v]^n == Sin[v]*u where u is a function of Cos[v]. *)
            return FunctionOfCosQ(Sin(v)*lst[1], v, x)
        lst = FindTrigFactor(tan, cot, u, v, True)
        if ListQ(lst):
            # (* Basis: If m integer and n odd, Tan[m*v]^n == Sin[v]*u where u is a function of Cos[v]. *)
            return FunctionOfCosQ(Sin(v)*lst[1], v, x)
        return all(FunctionOfCosQ(i, v, x) for i in u.args)
    return all(FunctionOfCosQ(i, v, x) for i in u.args)

def FunctionOfSinQ(u, v, x):
    # If u is a function of Sin[v], FunctionOfSinQ[u,v,x] returns True; else it returns False.
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        if OddQuotientQ(u.args[0], v):
            # Basis: If m odd, Sin[m*v]^n is a function of Sin[v].
            return SinQ(u) or CscQ(u)
        # Basis: If m even, Cos[m*v]^n is a function of Sin[v].
        return CosQ(u) or SecQ(u)
    elif eager_IntegerPowerQ(u):
        if eager_TrigQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if eager_EvenQ(u.exp):
                # Basis: If m integer and n even, Hyper[m*v]^n is a function of Sin[v].
                return True
            return FunctionOfSinQ(u.base, v, x)
    elif eager_ProductQ(u):
        if CosQ(u.args[0]) and SinQ(u.args[1]) and ZeroQ(u.args[0].args[0] - v/2) and ZeroQ(u.args[1].args[0] - v/2):
            return FunctionOfSinQ(Drop(u, 2), v, x)
        lst = FindTrigFactor(sin, csch, u, v, False)
        if ListQ(lst) and EvenQuotientQ(lst[0], v):
            # Basis: If m even and n odd, Sin[m*v]^n == Cos[v]*u where u is a function of Sin[v].
            return FunctionOfSinQ(Cos(v)*lst[1], v, x)
        lst = FindTrigFactor(cos, sec, u, v, False)
        if ListQ(lst) and OddQuotientQ(lst[0], v):
            # Basis: If m odd and n odd, Cos[m*v]^n == Cos[v]*u where u is a function of Sin[v].
            return FunctionOfSinQ(Cos(v)*lst[1], v, x)
        lst = FindTrigFactor(tan, cot, u, v, True)
        if ListQ(lst):
            # Basis: If m integer and n odd, Tan[m*v]^n == Cos[v]*u where u is a function of Sin[v].
            return FunctionOfSinQ(Cos(v)*lst[1], v, x)
        return all(FunctionOfSinQ(i, v, x) for i in u.args)
    return all(FunctionOfSinQ(i, v, x) for i in u.args)

def OddTrigPowerQ(u, v, x):
    if SinQ(u) or CosQ(u) or SecQ(u) or CscQ(u):
        return OddQuotientQ(u.args[0], v)
    if eager_PowerQ(u):
        return eager_OddQ(u.exp) and OddTrigPowerQ(u.base, v, x)
    if eager_ProductQ(u):
        if not eager_FreeFactors(u, x) == 1:
            return OddTrigPowerQ(eager_NonfreeFactors(u, x), v, x)
        lst = []
        for i in u.args:
            if eager_Not(FunctionOfTanQ(i, v, x)):
                lst.append(i)
        if lst == []:
            return True
        return eager_Length(lst)==1 and OddTrigPowerQ(lst[0], v, x)
    if eager_SumQ(u):
        return all(OddTrigPowerQ(i, v, x) for i in u.args)
    return False

def FunctionOfTanQ(u, v, x):
    # If u is a function of the form f[Tan[v],Cot[v]] where f is independent of x,
    # FunctionOfTanQ[u,v,x] returns True; else it returns False.
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        return TanQ(u) or CotQ(u) or EvenQuotientQ(u.args[0], v)
    elif eager_PowerQ(u):
        if eager_EvenQ(u.exp) and eager_TrigQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            return True
        elif eager_EvenQ(u.exp) and eager_SumQ(u.base):
            # Rubi: FunctionOfTanQ[Expand[u[[1]]^2], v, x] -- same misplaced paren as in
            # FunctionOfTanhQ; Expand takes one argument.
            return FunctionOfTanQ(Expand(u.base**2), v, x)
    if eager_ProductQ(u):
        lst = []
        for i in u.args:
            if eager_Not(FunctionOfTanQ(i, v, x)):
                lst.append(i)
        if lst == []:
            return True
        return eager_Length(lst)==2 and OddTrigPowerQ(lst[0], v, x) and OddTrigPowerQ(lst[1], v, x)
    return all(FunctionOfTanQ(i, v, x) for i in u.args)

def FunctionOfTanWeight(u, v, x):
    # (* u is a function of the form f[Tan[v],Cot[v]] where f is independent of x.
    # FunctionOfTanWeight[u,v,x] returns a nonnegative number if u is best considered a function
    # of Tan[v]; else it returns a negative number. *)
    if eager_AtomQ(u):
        return S(0)
    elif CalculusQ(u):
        return S(0)
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        if TanQ(u) and ZeroQ(u.args[0] - v):
            return S(1)
        elif CotQ(u) and ZeroQ(u.args[0] - v):
            return S(-1)
        return S(0)
    elif eager_PowerQ(u):
        if eager_EvenQ(u.exp) and eager_TrigQ(u.base) and IntegerQuotientQ(u.base.args[0], v):
            if TanQ(u.base) or CosQ(u.base) or SecQ(u.base):
                return S(1)
            return S(-1)
    if eager_ProductQ(u):
        if all(FunctionOfTanQ(i, v, x) for i in u.args):
            return Add(*[FunctionOfTanWeight(i, v, x) for i in u.args])
        return S(0)
    return Add(*[FunctionOfTanWeight(i, v, x) for i in u.args])

def FunctionOfTrigQ(u, v, x):
    # If u (x) is equivalent to a function of the form f (Sin[v],Cos[v],Tan[v],Cot[v],Sec[v],Csc[v]) where f is independent of x, FunctionOfTrigQ[u,v,x] returns True; else it returns False.
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_TrigQ(u) and IntegerQuotientQ(u.args[0], v):
        return True
    return all(FunctionOfTrigQ(i, v, x) for i in u.args)

def FunctionOfDensePolynomialsQ(u, x):
    # If all occurrences of x in u (x) are in dense polynomials, FunctionOfDensePolynomialsQ[u,x] returns True; else it returns False.
    if eager_FreeQ(u, x):
        return True
    if eager_PolynomialQ(u, x):
        return eager_Length(ExponentList(u, x)) > 1
    return all(FunctionOfDensePolynomialsQ(i, x) for i in u.args)

def eager_FunctionOfLog(u, *args):
    # If u (x) is equivalent to an expression of the form f (Log[a*x^n]), FunctionOfLog[u,x] returns
    # the list {f (x),a*x^n,n}; else it returns False.
    if len(args) == 1:
        x = args[0]
        lst = eager_FunctionOfLog(u, False, False, x)
        if eager_AtomQ(lst) or eager_FalseQ(lst[1]) or not isinstance(x, Symbol):
            return False
        else:
            return lst
    else:
        v = args[0]
        n = args[1]
        x = args[2]
        if eager_AtomQ(u):
            if u==x:
                return False
            else:
                return [u, v, n]
        if CalculusQ(u):
            return False
        lst = BinomialParts(u.args[0], x)
        if eager_LogQ(u) and ListQ(lst) and ZeroQ(lst[0]):
            if eager_FalseQ(v) or u.args[0] == v:
                return [x, u.args[0], lst[2]]
            else:
                return False
        lst = [0, v, n]
        l = []
        for i in u.args:
                lst = eager_FunctionOfLog(i, lst[1], lst[2], x)
                if eager_AtomQ(lst):
                    return False
                else:
                    l.append(lst[0])

        return [u.func(*l), lst[1], lst[2]]

def eager_PowerVariableExpn(u, m, x):
    # If m is an integer, u is an expression of the form f((c*x)**n) and g=GCD(m,n)>1,
    # PowerVariableExpn(u,m,x) returns the list {x**(m/g)*f((c*x)**(n/g)),g,c}; else it returns False.
    #
    # Exact arithmetic: ``m/lst[0]`` was Python division, so Int[x^3 f(x^2)] built
    # ``x**1.0`` -- a float exponent poisoning everything downstream. S(m) keeps it exact.
    if eager_IntegerQ(m):
        lst = PowerVariableDegree(u, m, S(1), x)
        if lst is False:
            return False
        return [x**(S(m)/lst[0])*PowerVariableSubst(u, lst[0], x), lst[0], lst[1]]
    return False

def PowerVariableDegree(u, m, c, x):
    """Rubi ``PowerVariableDegree[u,m,c,x]`` -- the running GCD of the powers of x in u.

    Rubi's recursion THREADS the accumulator through the scan::

        Catch[Module[{lst={m,c}},
          Scan[Function[lst=PowerVariableDegree[#,lst[[1]],lst[[2]],x];
                        If[AtomQ[lst],Throw[False]]], u];
          lst]]

    each argument refines ``lst`` and the NEXT argument starts from the refined value.
    The port called every child with the ORIGINAL [m, c] and returned the LAST child's
    result, so any x-free trailing argument (e.g. the exponent -1 of ``(1+W)**-1``)
    reset the answer to the untouched [m, c]. Concretely,
    ``PowerVariableDegree[1/(1+W(a x^2)), 4, 1, x]`` returned g=4 instead of
    GCD(4,2)=2, the rule guard ``NeQ[lst[[2]], m+1]`` then saw 4==4 and rejected, and
    the 9.3/9.4 "Int[x^m F(x^n)] -> 1/g Subst[...]" reduction NEVER fired -- which is
    the root cause of the Int[x^3 W(a x^2)^2] wrong answer (RUBI_PORT_DEFECTS.md §27).
    """
    if eager_FreeQ(u, x):
        return [m, c]
    if eager_AtomQ(u) or CalculusQ(u):
        return False
    if eager_PowerQ(u) and eager_FreeQ(u.base/x, x):
        if ZeroQ(m) or (m == u.exp and c == u.base/x):
            return [u.exp, u.base/x]
        if eager_IntegerQ(u.exp) and eager_IntegerQ(m) and eager_GCD(m, u.exp) > 1 and c == u.base/x:
            return [eager_GCD(m, u.exp), c]
        return False
    lst = [m, c]
    for arg in u.args:
        lst = PowerVariableDegree(arg, lst[0], lst[1], x)
        if lst is False:
            return False
    return lst

def PowerVariableSubst(u, m, x):
    """Rubi ``PowerVariableSubst[u,m,x]`` -- rewrite every ``(c x)^k`` in u as ``x^(k/m)``.

    Rubi's general case is ``Map[Function[PowerVariableSubst[#,m,x]], u]`` -- over ANY
    head. The port mapped only over Mul and Add and returned everything else unchanged,
    so ``W(a x^2)`` (head LambertW) and any Power with a non-``c*x`` base survived
    untouched and the substitution silently produced the wrong integrand.
    """
    if eager_FreeQ(u, x) or eager_AtomQ(u) or CalculusQ(u):
        return u
    if eager_PowerQ(u) and eager_FreeQ(u.base/x, x):
        return x**(u.exp/m)
    return u.func(*[PowerVariableSubst(arg, m, x) for arg in u.args])

def eager_EulerIntegrandQ(expr, x):
    a = Wild('a', exclude=[x])
    b = Wild('b', exclude=[x])
    n = Wild('n', exclude=[x, 0])
    m = Wild('m', exclude=[x, 0])
    p = Wild('p', exclude=[x, 0])
    u = Wild('u')
    v = Wild('v')
    # Rubi parenthesises the LAST conjunct:
    #   ... && QuadraticQ[u,x] && (Not[RationalQ[p]] || ILtQ[p,0] && Not[BinomialQ[u,x]])
    # Python's `and` binds tighter than `or`, so dropping those parentheses turned the
    # guard into `(everything && Not[RationalQ[p]]) || (ILtQ[p,0] && Not[BinomialQ[u,x]])`
    # -- the right-hand disjunct then returned True on its own, bypassing FreeQ,
    # IntegerQ and QuadraticQ entirely. Also `1/2` was Python float division; Rubi's
    # `n+1/2` is an EXACT rational and IntegerQ[2.] is False in Mathematica.
    # Pattern 1
    M = expr.match((a*x + b*u**n)**p)
    if M:
        if (len(M) == 5 and eager_FreeQ([M[a], M[b]], x) and eager_IntegerQ(M[n] + S(1)/2)
                and eager_QuadraticQ(M[u], x)
                and (eager_Not(eager_RationalQ(M[p]))
                     or (NegativeIntegerQ(M[p]) and eager_Not(eager_BinomialQ(M[u], x))))):
            return True
    # Pattern 2
    M = expr.match(v**m*(a*x + b*u**n)**p)
    if M:
        if (len(M) == 6 and eager_FreeQ([M[a], M[b]], x) and ZeroQ(M[u] - M[v])
                and eager_IntegersQ(2*M[m], M[n] + S(1)/2) and eager_QuadraticQ(M[u], x)
                and (eager_Not(eager_RationalQ(M[p]))
                     or (NegativeIntegerQ(M[p]) and eager_Not(eager_BinomialQ(M[u], x))))):
            return True
    # Pattern 3
    M = expr.match(u**n*v**p)
    if M:
        if (len(M) == 3 and NegativeIntegerQ(M[p]) and eager_IntegerQ(M[n] + S(1)/2)
                and eager_QuadraticQ(M[u], x) and eager_QuadraticQ(M[v], x)
                and eager_Not(eager_BinomialQ(M[v], x))):
            return True
    # Rubi's final catch-all definition is `EulerIntegrandQ[u_,x_Symbol] := False`.
    # This used to fall off the end (returning None) whenever a pattern matched but
    # its guard failed.
    return False

def eager_FunctionOfSquareRootOfQuadratic(u, *args):
    if len(args) == 1:
        x = args[0]
        pattern = Pattern(UtilityOperator(x_**WildSymbol('m', optional_value=1)*(a_ + x**WildSymbol('n', optional_value=1)*WildSymbol('b', optional_value=1))**p_, x), _patched_custom_constraint_call(lambda a, b, m, n, p, x: eager_FreeQ([a, b, m, n, p], x)))
        M = is_match(UtilityOperator(u, args[0]), pattern)
        if M:
            return False
        tmp = eager_FunctionOfSquareRootOfQuadratic(u, False, x)
        if eager_AtomQ(tmp) or eager_FalseQ(tmp[0]):
            return False
        tmp = tmp[0]
        a = eager_Coefficient(tmp, x, 0)
        b = eager_Coefficient(tmp, x, 1)
        c = eager_Coefficient(tmp, x, 2)
        if ZeroQ(a) and ZeroQ(b) or ZeroQ(b**2-4*a*c):
            return False
        if eager_PosQ(c):
            sqrt = eager_Rt(c, S(2));
            q = a*sqrt + b*x + sqrt*x**2
            r = b + 2*sqrt*x
            return [eager_Simplify(SquareRootOfQuadraticSubst(u, q/r, (-a+x**2)/r, x)*q/r**2), eager_Simplify(sqrt*x + Sqrt(tmp)), 2]
        if eager_PosQ(a):
            sqrt = eager_Rt(a, S(2))
            q = c*sqrt - b*x + sqrt*x**2
            r = c - x**2
            return [eager_Simplify(SquareRootOfQuadraticSubst(u, q/r, (-b+2*sqrt*x)/r, x)*q/r**2), eager_Simplify((-sqrt+Sqrt(tmp))/x), 1]
        sqrt = eager_Rt(b**2 - 4*a*c, S(2))
        r = c - x**2
        return[eager_Simplify(-sqrt*SquareRootOfQuadraticSubst(u, -sqrt*x/r, -(b*c+c*sqrt+(-b+sqrt)*x**2)/(2*c*r), x)*x/r**2), eager_FullSimplify(2*c*Sqrt(tmp)/(b-sqrt+2*c*x)), 3]
    else:
        v = args[0]
        x = args[1]
        if eager_AtomQ(u) or eager_FreeQ(u, x):
            return [v]
        if eager_PowerQ(u):
            if eager_FreeQ(u.exp, x):
                if eager_FractionQ(u.exp) and eager_Denominator(u.exp) == 2 and eager_PolynomialQ(u.base, x) and eager_Exponent(u.base, x) == 2:
                    if eager_FalseQ(v) or u.base == v:
                        return [u.base]
                    else:
                        return False
                return eager_FunctionOfSquareRootOfQuadratic(u.base, v, x)
        if eager_ProductQ(u) or eager_SumQ(u):
            lst = [v]
            lst1 = []
            for i in u.args:
                if eager_FunctionOfSquareRootOfQuadratic(i, lst[0], x) == False:
                    return False
                lst1 = eager_FunctionOfSquareRootOfQuadratic(i, lst[0], x)
            return lst1
        else:
            return False

def SquareRootOfQuadraticSubst(u, vv, xx, x):
    # SquareRootOfQuadraticSubst(u, vv, xx, x) returns u with fractional powers replaced by vv raised to the power and x replaced by xx.
    if eager_AtomQ(u) or eager_FreeQ(u, x):
        if u==x:
            return xx
        return u
    if eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            if eager_FractionQ(u.exp) and eager_Denominator(u.exp)==2 and eager_PolynomialQ(u.base, x) and eager_Exponent(u.base, x)==2:
                return vv**eager_Numerator(u.exp)
            return SquareRootOfQuadraticSubst(u.base, vv, xx, x)**u.exp
    elif eager_SumQ(u):
        t = 0
        for i in u.args:
            t += SquareRootOfQuadraticSubst(i, vv, xx, x)
        return t
    elif eager_ProductQ(u):
        t = 1
        for i in u.args:
            t *= SquareRootOfQuadraticSubst(i, vv, xx, x)
        return t

def eager_Divides(y, u, x):
    # If u divided by y is free of x, Divides[y,u,x] returns the quotient; else it returns False.
    v = eager_Simplify(u/y)
    if eager_FreeQ(v, x):
        return v
    else:
        return False

@_pure_expr_cache(maxsize=20000)
def eager_DerivativeDivides(y, u, x):
    """
    If y not equal to x, y is easy to differentiate wrt x, and u divided by the derivative of y
    is free of x, DerivativeDivides[y,u,x] returns the quotient; else it returns False.

    Memoised (pure function of its SymPy args): the Not[FalseQ[DerivativeDivides[...]]]
    guards re-evaluate it on identical (y, u, x) triples throughout the DFS -- profiling
    showed ~15ms per call, a third of a slow integral's runtime.
    """
    from matchpy import is_match
    pattern0 = Pattern(to_matchpy_expression(_a_*x), _patched_custom_constraint_call(lambda a : eager_FreeQ(a, x)))

    def f1(y, u, x):
        if eager_PolynomialQ(y, x):
            return eager_PolynomialQ(u, x) and eager_Exponent(u, x) == eager_Exponent(y, x) - 1
        else:
            return EasyDQ(y, x)

    if is_match(y, pattern0):
        return False
    # Check if y is a product of free factors (would mean derivative is trivial)
    #if FreeQ(y, x):
        #return False

    elif f1(y, u, x):
        v = eager_D(y ,x)
        if eager_EqQ(v, 0):
            return False
        else:
            v = eager_Simplify(u/v)
            if eager_FreeQ(v, x):
                return v
            else:
                return False
    else:
        return False


def EasyDQ(expr, x):
    # If u is easy to differentiate wrt x,  EasyDQ(u, x) returns True; else it returns False *)
    u = Wild('u',exclude=[1])
    m = Wild('m',exclude=[x, 0])
    M = expr.match(u*x**m)
    if M:
        return EasyDQ(M[u], x)
    if eager_AtomQ(expr) or eager_FreeQ(expr, x) or eager_Length(expr)==0:
        return True
    elif CalculusQ(expr):
        return False
    elif eager_Length(expr)==1:
        return EasyDQ(expr.args[0], x)
    elif eager_BinomialQ(expr, x) or ProductOfLinearPowersQ(expr, x):
        return True
    elif eager_RationalFunctionQ(expr, x) and eager_RationalFunctionExponents(expr, x)==[1, 1]:
        return True
    elif eager_ProductQ(expr):
        if eager_FreeQ(eager_First(expr), x):
            return EasyDQ(eager_Rest(expr), x)
        elif eager_FreeQ(eager_Rest(expr), x):
            return EasyDQ(eager_First(expr), x)
        else:
            return False
    elif eager_SumQ(expr):
        return EasyDQ(eager_First(expr), x) and EasyDQ(eager_Rest(expr), x)
    elif eager_Length(expr)==2:
        if eager_FreeQ(expr.args[0], x):
            EasyDQ(expr.args[1], x)
        elif eager_FreeQ(expr.args[1], x):
            return EasyDQ(expr.args[0], x)
        else:
            return False
    return False

def ProductOfLinearPowersQ(u, x):
    # ProductOfLinearPowersQ(u, x) returns True iff u is a product of factors of the form v^n where v is linear in x
    v = Wild('v')
    n = Wild('n', exclude=[x])
    M = u.match(v**n)
    return eager_FreeQ(u, x) or M and eager_LinearQ(M[v], x) or eager_ProductQ(u) and ProductOfLinearPowersQ(eager_First(u), x) and ProductOfLinearPowersQ(eager_Rest(u), x)

def eager_Rt(u, n):
    return RtAux(TogetherSimplify(u), n)

def NthRoot(u, n):
    # Mathematica: NthRoot[u_,n_] := u^(1/n) -- the principal nth root.
    #
    # Matching Mathematica's *form* needs one adaptation. On a rational radicand
    # Mathematica factors it into primes and distributes 1/n across them, e.g.
    # 14580^(1/3) -> 9*2^(2/3)*5^(1/3) and (-4)^(1/2) -> 2*I; SymPy's ** only pulls
    # out the single perfect nth power (14580^(1/3) -> 9*20^(1/3)). So for a rational
    # u we factor numerator and denominator and rebuild the product ourselves.
    #
    # For everything else (symbolic, irrational, or COMPLEX u) we return the plain
    # principal power -- which is exactly Mathematica's Sqrt[2+3*I] etc. (An earlier
    # nsimplify here got the rational case right but mangled complex radicands into
    # rectangular a+b*I form, so it is not usable.)
    u = sympify(u)
    if u.is_Rational:
        p, q = u.as_numer_denom()          # p signed, q > 0
        result = S.One
        if p < 0:
            result *= S.NegativeOne ** Rational(1, n)   # (-1)^(1/n), as Mathematica
            p = -p
        for base, exp in factorint(p).items():
            result *= Integer(base) ** Rational(exp, n)
        for base, exp in factorint(q).items():
            result /= Integer(base) ** Rational(exp, n)
        return result
    return u ** (S(1) / n)

def AtomBaseQ(u):
    # If u is an atom or an atom raised to an odd degree,  AtomBaseQ(u) returns True; else it returns False
    return eager_AtomQ(u) or eager_PowerQ(u) and eager_OddQ(u.args[1]) and AtomBaseQ(u.args[0])

def eager_SumBaseQ(u):
    # If u is a sum or a sum raised to an odd degree,  SumBaseQ(u) returns True; else it returns False
    return eager_SumQ(u) or eager_PowerQ(u) and eager_OddQ(u.args[1]) and eager_SumBaseQ(u.args[0])

def NegSumBaseQ(u):
    # If u is a sum or a sum raised to an odd degree whose lead term has a negative form,  NegSumBaseQ(u) returns True; else it returns False
    return eager_SumQ(u) and eager_NegQ(eager_First(u)) or eager_PowerQ(u) and eager_OddQ(u.args[1]) and NegSumBaseQ(u.args[0])

def AllNegTermQ(u):
    # If all terms of u have a negative form, AllNegTermQ(u) returns True; else it returns False
    if eager_PowerQ(u):
        if eager_OddQ(u.exp):
            return AllNegTermQ(u.base)
    if eager_SumQ(u):
        return eager_NegQ(eager_First(u)) and AllNegTermQ(eager_Rest(u))
    return eager_NegQ(u)

def SomeNegTermQ(u):
    # If some term of u has a negative form,  SomeNegTermQ(u) returns True; else it returns False
    if eager_PowerQ(u):
        if eager_OddQ(u.exp):
            return SomeNegTermQ(u.base)
    if eager_SumQ(u):
        return eager_NegQ(eager_First(u)) or SomeNegTermQ(eager_Rest(u))
    return eager_NegQ(u)

def TrigSquareQ(u):
    # If u is an expression of the form Sin(z)^2 or Cos(z)^2,  TrigSquareQ(u) returns True,  else it returns False
    return eager_PowerQ(u) and eager_EqQ(u.args[1], 2) and eager_MemberQ([sin, cos], eager_Head(u.args[0]))

def RtAux(u, n):
    if eager_PowerQ(u):
        return u.base**(u.exp/n)
    if eager_ComplexNumberQ(u):
        a = Re(u)
        b = Im(u)
        if eager_Not(eager_IntegerQ(a) and eager_IntegerQ(b)) and eager_IntegerQ(a/(a**2 + b**2)) and eager_IntegerQ(b/(a**2 + b**2)):
            # Basis: a+b*I==1/(a/(a^2+b^2)-b/(a^2+b^2)*I)
            return S(1)/RtAux(a/(a**2 + b**2) - b/(a**2 + b**2)*I, n)
        else:
            return NthRoot(u, n)
    if eager_ProductQ(u):
        lst = eager_SplitProduct(eager_PositiveQ, u)
        if ListQ(lst):
            return RtAux(lst[0], n)*RtAux(lst[1], n)
        lst = eager_SplitProduct(eager_NegativeQ, u)
        if ListQ(lst):
            if eager_EqQ(lst[0], -1):
                v = lst[1]
                if eager_PowerQ(v):
                    if eager_NegativeQ(v.exp):
                        return 1/RtAux(-v.base**(-v.exp), n)
                if eager_ProductQ(v):
                    if ListQ(eager_SplitProduct(eager_SumBaseQ, v)):
                        lst = eager_SplitProduct(AllNegTermQ, v)
                        if ListQ(lst):
                            return RtAux(-lst[0], n)*RtAux(lst[1], n)
                        lst = eager_SplitProduct(NegSumBaseQ, v)
                        if ListQ(lst):
                            return RtAux(-lst[0], n)*RtAux(lst[1], n)
                        lst = eager_SplitProduct(SomeNegTermQ, v)
                        if ListQ(lst):
                            return RtAux(-lst[0], n)*RtAux(lst[1], n)
                        lst = eager_SplitProduct(eager_SumBaseQ, v)
                        return RtAux(-lst[0], n)*RtAux(lst[1], n)
                    lst = eager_SplitProduct(AtomBaseQ, v)
                    if ListQ(lst):
                        return RtAux(-lst[0], n)*RtAux(lst[1], n)
                    else:
                        return RtAux(-eager_First(v), n)*RtAux(eager_Rest(v), n)
                if eager_OddQ(n):
                    return -RtAux(v, n)
                else:
                    return NthRoot(u, n)
            else:
                return RtAux(-lst[0], n)*RtAux(-lst[1], n)
        lst = eager_SplitProduct(AllNegTermQ, u)
        if ListQ(lst) and ListQ(eager_SplitProduct(eager_SumBaseQ, lst[1])):
            return RtAux(-lst[0], n)*RtAux(-lst[1], n)
        lst = eager_SplitProduct(NegSumBaseQ, u)
        if ListQ(lst) and ListQ(eager_SplitProduct(NegSumBaseQ, lst[1])):
            return RtAux(-lst[0], n)*RtAux(-lst[1], n)
        return u.func(*[RtAux(i, n) for i in u.args])
    v = TrigSquare(u)
    if eager_Not(eager_AtomQ(v)):
        return RtAux(v, n)
    if eager_OddQ(n) and eager_NegativeQ(u):
        return -RtAux(-u, n)
    if eager_OddQ(n) and eager_NegQ(u) and eager_PosQ(-u):
        return -RtAux(-u, n)
    else:
        return NthRoot(u, n)

def TrigSquare(u):
    # If u is an expression of the form a-a*Sin(z)^2 or a-a*Cos(z)^2, TrigSquare(u) returns Cos(z)^2 or Sin(z)^2 respectively,
    # else it returns False.
    if eager_SumQ(u):
        for i in u.args:
            v = eager_SplitProduct(TrigSquareQ, i)
            if v == False or SplitSum(v, u) == False:
                return False
            lst = SplitSum(eager_SplitProduct(TrigSquareQ, i))
        if lst and ZeroQ(lst[1][2] + lst[1]):
            if eager_Head(lst[0][0].args[0]) == sin:
                return lst[1]*cos(lst[1][1][1][1])**2
            return lst[1]*sin(lst[1][1][1][1])**2
        else:
            return False
    else:
        return False

def eager_IntSum(u, x):
    """Rubi ``IntSum[u,x] := Map[Function[Int[#,x]], u]`` -- distribute Int over a sum.

    Emits OUR deferred ``Int`` nodes, not ``sympy.Integral``: the DFS has to be able to
    reduce each term further. Returning sympy.Integral instead left an inert node in the
    answer (it surfaced as an undifferentiable ``Derivative(IntSum(...))``).
    """
    from rubi_rules.base_objects import Int as _Int   # local: base_objects imports this module
    return Add(*[_Int(term, x) for term in u.args])

def IntTerm(expr, x):
    # If u is of the form c*(a+b*x)**m, IntTerm(u,x) returns the antiderivative of u wrt x;
    # else it returns d*Int(v,x) where d*v=u and d is free of x.
    c = Wild('c', exclude=[x])
    m = Wild('m', exclude=[x, 0])
    v = Wild('v')
    M = expr.match(c/v)
    if M and len(M) == 2 and eager_FreeQ(M[c], x) and eager_LinearQ(M[v], x):
        return eager_Simp(M[c]*Log(RemoveContent(M[v], x))/eager_Coefficient(M[v], x, 1), x)
    M = expr.match(c*v**m)
    if M and len(M) == 3 and NonzeroQ(M[m] + 1) and eager_LinearQ(M[v], x):
        return eager_Simp(M[c]*M[v]**(M[m] + 1)/(eager_Coefficient(M[v], x, 1)*(M[m] + 1)), x)
    if eager_SumQ(expr):
        t = 0
        for i in expr.args:
            t += IntTerm(i, x)
        return t
    else:
        u = expr
        return eager_Dist(eager_FreeFactors(u,x), Integral(eager_NonfreeFactors(u, x), x), x)

def Map2(f, lst1, lst2):
    result = []
    for i in range(0, len(lst1)):
        result.append(f(lst1[i], lst2[i]))
    return result

def ConstantFactor(u, x):
    # (* ConstantFactor[u,x] returns a 2-element list of the factors of u[x] free of x and the
    # factors not free of u[x].  Common constant factors of the terms of sums are also collected. *)
    if eager_FreeQ(u, x):
        return [u, S(1)]
    elif eager_AtomQ(u):
        return [S(1), u]
    elif eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            lst = ConstantFactor(u.base, x)
            if eager_IntegerQ(u.exp):
                return [lst[0]**u.exp, lst[1]**u.exp]
            tmp = PositiveFactors(lst[0])
            if tmp == 1:
                return [S(1), u]
            return [tmp**u.exp, (NonpositiveFactors(lst[0])*lst[1])**u.exp]
    elif eager_ProductQ(u):
        lst = [ConstantFactor(i, x) for i in u.args]
        return [Mul(*[eager_First(i) for i in lst]), Mul(*[i[1] for i in lst])]
    elif eager_SumQ(u):
        lst1 = [ConstantFactor(i, x) for i in u.args]
        if SameQ(*[i[1] for i in lst1]):
            return [Add(*[i[0] for i in lst1]), lst1[0][1]]
        lst2 = CommonFactors([eager_First(i) for i in lst1])
        return [eager_First(lst2), Add(*Map2(Mul, eager_Rest(lst2), [i[1] for i in lst1]))]
    return [S(1), u]

def SameQ(*args):
    for i in range(0, len(args) - 1):
        if args[i] != args[i+1]:
            return False
    return True

def ReplacePart(lst, a, b):
    lst[b] = a
    return lst

def CommonFactors(lst):
    # (* If lst is a list of n terms, CommonFactors[lst] returns a n+1-element list whose first
    # element is the product of the factors common to all terms of lst, and whose remaining
    # elements are quotients of each term divided by the common factor. *)
    lst1 = [NonabsurdNumberFactors(i) for i in lst]
    lst2 = [AbsurdNumberFactors(i) for i in lst]
    num = AbsurdNumberGCD(*lst2)
    common = num
    lst2 = [i/num for i in lst2]
    while (True):
        lst3 = [LeadFactor(i) for i in lst1]

        # Rubi is ONE nested If: exactly one branch runs per iteration. This used to be
        # two independent if-chains, so after the SameQ branch fired control fell
        # through into the second chain and ran a SECOND branch on a now-stale lst3 --
        # usually MostMainFactorPosition, which pushed the already-extracted factor
        # into the residual and dropped the real one. That broke the function's defining
        # invariant (common * residual[i] == lst[i]): CommonFactors[{2 a b, 4 a c}]
        # returned {2a, a, 2c} (2a*a = 2a^2) where Rubi returns {2a, b, 2c}.
        if SameQ(*lst3):
            common = common*lst3[0]
            lst1 = [RemainingFactors(i) for i in lst1]
        elif (all((eager_LogQ(i) and eager_IntegerQ(eager_First(i)) and eager_First(i) > 0) for i in lst3) and
              all(eager_RationalQ(i) for i in [eager_FullSimplify(j/eager_First(lst3)) for j in lst3])):
            lst4 = [eager_FullSimplify(j/eager_First(lst3)) for j in lst3]
            num = eager_GCD(*lst4)
            # .args[0] of the log node (Mathematica Log[First[lst3][[1]]^num]);
            # a sympy log is not subscriptable, so [0] raised TypeError here.
            common = common*Log((eager_First(lst3).args[0])**num)
            lst2 = [lst2[i]*lst4[i]/num for i in range(0, len(lst2))]
            lst1 = [RemainingFactors(i) for i in lst1]
        else:
            # Rubi assigns lst4 only once the two branches above have been ruled out.
            lst4 = [LeadDegree(i) for i in lst1]
            if SameQ(*[LeadBase(i) for i in lst1]) and eager_RationalQ(*lst4):
                num = Smallest(lst4)
                base = LeadBase(lst1[0])
                if num != 0:
                    common = common*base**num
                lst2 = [lst2[i]*base**(lst4[i] - num) for i in range(0, len(lst2))]
                lst1 = [RemainingFactors(i) for i in lst1]
            elif (eager_Length(lst1) == 2 and ZeroQ(LeadBase(lst1[0]) + LeadBase(lst1[1])) and
                  NonzeroQ(lst1[0] - 1) and eager_IntegerQ(lst4[0]) and eager_FractionQ(lst4[1])):
                num = Min(*lst4)
                base = LeadBase(lst1[1])
                if num != 0:
                    common = common*base**num
                lst2 = [lst2[0]*(-1)**lst4[0], lst2[1]]
                lst2 = [lst2[i]*base**(lst4[i] - num) for i in range(0, len(lst2))]
                lst1 = [RemainingFactors(i) for i in lst1]
            # Rubi: EqQ[LeadBase[lst1[[1]]] + LeadBase[lst1[[2]]], 0] && NeQ[lst1[[2]], 1]
            #       && IntegerQ[lst4[[2]]] && FractionQ[lst4[[1]]].
            # This tested lst1[0] instead of LeadBase(lst1[0]) and IntegerQ on lst1[1]
            # instead of lst4[1] -- transcription slips against the Rubi DownValues.
            elif (eager_Length(lst1) == 2 and ZeroQ(LeadBase(lst1[0]) + LeadBase(lst1[1])) and
                  NonzeroQ(lst1[1] - 1) and eager_IntegerQ(lst4[1]) and eager_FractionQ(lst4[0])):
                num = Min(*lst4)
                base = LeadBase(lst1[0])
                if num != 0:
                    common = common*base**num
                lst2 = [lst2[0], lst2[1]*(-1)**lst4[1]]
                lst2 = [lst2[i]*base**(lst4[i] - num) for i in range(0, len(lst2))]
                lst1 = [RemainingFactors(i) for i in lst1]
            else:
                num = MostMainFactorPosition(lst3)
                lst2 = ReplacePart(lst2, lst3[num]*lst2[num], num)
                lst1 = ReplacePart(lst1, RemainingFactors(lst1[num]), num)
        if all(i==1 for i in lst1):
            return Prepend(lst2, common)

def MostMainFactorPosition(lst):
    factor = S(1)
    num = 0
    for i in range(0, eager_Length(lst)):
        if FactorOrder(lst[i], factor) > 0:
            factor = lst[i]
            num = i
    return num

SbaseS, SexponS = None, None
SexponFlagS = False
def eager_FunctionOfExponentialQ(u, x):
    # (* FunctionOfExponentialQ[u,x] returns True iff u is a function of F^v where F is a constant and v is linear in x, *)
    # (* and such an exponential explicitly occurs in u (i.e. not just implicitly in hyperbolic functions). *)
    global SbaseS, SexponS, SexponFlagS
    SbaseS, SexponS = None, None
    SexponFlagS = False
    res = FunctionOfExponentialTest(u, x)
    return res and SexponFlagS

def eager_FunctionOfExponential(u, x):
    global SbaseS, SexponS, SexponFlagS
    # (* u is a function of F^v where v is linear in x.  FunctionOfExponential[u,x] returns F^v. *)
    SbaseS, SexponS = None, None
    SexponFlagS = False
    FunctionOfExponentialTest(u, x)
    return SbaseS**SexponS

def eager_FunctionOfExponentialFunction(u, x):
    global SbaseS, SexponS, SexponFlagS
    # (* u is a function of F^v where v is linear in x.  FunctionOfExponentialFunction[u,x] returns u with F^v replaced by x. *)
    SbaseS, SexponS = None, None
    SexponFlagS = False
    FunctionOfExponentialTest(u, x)
    return eager_SimplifyIntegrand(FunctionOfExponentialFunctionAux(u, x), x)

def FunctionOfExponentialFunctionAux(u, x):
    # (* u is a function of F^v where v is linear in x, and the fluid variables $base$=F and $expon$=v. *)
    # (* FunctionOfExponentialFunctionAux[u,x] returns u with F^v replaced by x. *)
    global SbaseS, SexponS, SexponFlagS
    if eager_AtomQ(u):
        return u
    elif eager_PowerQ(u):
        if eager_FreeQ(u.base, x) and eager_LinearQ(u.exp, x):
            if ZeroQ(eager_Coefficient(SexponS, x, 0)):
                return u.base**eager_Coefficient(u.exp, x, 0)*x**eager_FullSimplify(Log(u.base)*eager_Coefficient(u.exp, x, 1)/(Log(SbaseS)*eager_Coefficient(SexponS, x, 1)))
            return x**eager_FullSimplify(Log(u.base)*eager_Coefficient(u.exp, x, 1)/(Log(SbaseS)*eager_Coefficient(SexponS, x, 1)))
    elif eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
        tmp = x**eager_FullSimplify(eager_Coefficient(u.args[0], x, 1)/(Log(SbaseS)*eager_Coefficient(SexponS, x, 1)))
        if SinhQ(u):
            return tmp/2 - 1/(2*tmp)
        elif CoshQ(u):
            return tmp/2 + 1/(2*tmp)
        elif TanhQ(u):
            return (tmp - 1/tmp)/(tmp + 1/tmp)
        elif CothQ(u):
            return (tmp + 1/tmp)/(tmp - 1/tmp)
        elif SechQ(u):
            return 2/(tmp + 1/tmp)
        return 2/(tmp - 1/tmp)
    if eager_PowerQ(u):
        if eager_FreeQ(u.base, x) and eager_SumQ(u.exp):
            return FunctionOfExponentialFunctionAux(u.base**eager_First(u.exp), x)*FunctionOfExponentialFunctionAux(u.base**eager_Rest(u.exp), x)
    return u.func(*[FunctionOfExponentialFunctionAux(i, x) for i in u.args])

def FunctionOfExponentialTest(u, x):
    # (* FunctionOfExponentialTest[u,x] returns True iff u is a function of F^v where F is a constant and v is linear in x. *)
    # (* Before it is called, the fluid variables $base$ and $expon$ should be set to Null and $exponFlag$ to False. *)
    # (* If u is a function of F^v, $base$ and $expon$ are set to F and v, respectively. *)
    # (* If an explicit exponential occurs in u, $exponFlag$ is set to True. *)
    global SbaseS, SexponS, SexponFlagS
    if eager_FreeQ(u, x):
        return True
    elif u == x or CalculusQ(u):
        return False
    elif eager_PowerQ(u):
        if eager_FreeQ(u.base, x) and eager_LinearQ(u.exp, x):
            SexponFlagS = True
            return FunctionOfExponentialTestAux(u.base, u.exp, x)
    elif eager_HyperbolicQ(u) and eager_LinearQ(u.args[0], x):
        return FunctionOfExponentialTestAux(E, u.args[0], x)
    if eager_PowerQ(u):
        if eager_FreeQ(u.base, x) and eager_SumQ(u.exp):
            return FunctionOfExponentialTest(u.base**eager_First(u.exp), x) and FunctionOfExponentialTest(u.base**eager_Rest(u.exp), x)
    return all(FunctionOfExponentialTest(i, x) for i in u.args)

def FunctionOfExponentialTestAux(base, expon, x):
    global SbaseS, SexponS, SexponFlagS
    if SbaseS is None:
        SbaseS = base
        SexponS = expon
        return True
    tmp = eager_FullSimplify(Log(base)*eager_Coefficient(expon, x, 1)/(Log(SbaseS)*eager_Coefficient(SexponS, x, 1)))
    if eager_Not(eager_RationalQ(tmp)):
        return False
    elif ZeroQ(eager_Coefficient(SexponS, x, 0)) or NonzeroQ(tmp - eager_FullSimplify(Log(base)*eager_Coefficient(expon, x, 0)/(Log(SbaseS)*eager_Coefficient(SexponS, x, 0)))):
        if PositiveIntegerQ(base, SbaseS) and base < SbaseS:
            SbaseS = base
            SexponS = expon
            tmp = 1/tmp
        SexponS = eager_Coefficient(SexponS, x, 1)*x/eager_Denominator(tmp)
        if tmp < 0 and eager_NegQ(eager_Coefficient(SexponS, x, 1)):
            SexponS = -SexponS
        return True
    SexponS = SexponS/eager_Denominator(tmp)
    if tmp < 0 and eager_NegQ(eager_Coefficient(SexponS, x, 1)):
        SexponS = -SexponS
    return True

def stdev(lst):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd / num_items
    sd = sqrt(variance)

    return sd


def eager_If(cond, t, f):
    # returns t if condition is true else f
    if cond:
        return t
    return f

def eager_IntQuadraticQ(a, b, c, d, e, m, p, x):
    # (* IntQuadraticQ[a,b,c,d,e,m,p,x] returns True iff (d+e*x)^m*(a+b*x+c*x^2)^p is integrable wrt x in terms of non-Appell functions. *)
    return eager_IntegerQ(p) or PositiveIntegerQ(m) or eager_IntegersQ(2*m, 2*p) or eager_IntegersQ(m, 4*p) or eager_IntegersQ(m, p + S(1)/3) and (ZeroQ(c**2*d**2 - b*c*d*e + b**2*e**2 - 3*a*c*e**2) or ZeroQ(c**2*d**2 - b*c*d*e - 2*b**2*e**2 + 9*a*c*e**2))

def eager_IntBinomialQ(*args):
    #(* IntBinomialQ(a,b,c,n,m,p,x) returns True iff (c*x)^m*(a+b*x^n)^p is integrable wrt x in terms of non-hypergeometric functions. *)
    if len(args) == 8:
        a, b, c, d, n, p, q, x = args
        return eager_IntegersQ(p,q) or PositiveIntegerQ(p) or PositiveIntegerQ(q) or (ZeroQ(n-2) or ZeroQ(n-4)) and (eager_IntegersQ(p,4*q) or eager_IntegersQ(4*p,q)) or ZeroQ(n-2) and (eager_IntegersQ(2*p,2*q) or eager_IntegersQ(3*p,q) and ZeroQ(b*c+3*a*d) or eager_IntegersQ(p,3*q) and ZeroQ(3*b*c+a*d))
    elif len(args) == 7:
        a, b, c, n, m, p, x = args
        return eager_IntegerQ(2*p) or eager_IntegerQ((m+1)/n + p) or (ZeroQ(n - 2) or ZeroQ(n - 4)) and eager_IntegersQ(2*m, 4*p) or ZeroQ(n - 2) and eager_IntegerQ(6*p) and (eager_IntegerQ(m) or eager_IntegerQ(m - p))
    elif len(args) == 10:
        a, b, c, d, e, m, n, p, q, x = args
        return eager_IntegersQ(p,q) or PositiveIntegerQ(p) or PositiveIntegerQ(q) or ZeroQ(n-2) and eager_IntegerQ(m) and eager_IntegersQ(2*p,2*q) or ZeroQ(n-4) and (eager_IntegersQ(m,p,2*q) or eager_IntegersQ(m,2*p,q))

def RectifyTangent(*args):
    # (* RectifyTangent(u,a,b,r,x) returns an expression whose derivative equals the derivative of r*ArcTan(a+b*Tan(u)) wrt x. *)
    if len(args) == 5:
        u, a, b, r, x = args
        t1 = eager_Together(a)
        t2 = eager_Together(b)
        if (PureComplexNumberQ(t1) or (eager_ProductQ(t1) and any(PureComplexNumberQ(i) for i in t1.args))) and (PureComplexNumberQ(t2) or eager_ProductQ(t2) and any(PureComplexNumberQ(i) for i in t2.args)):
            c = a/I
            d = b/I
            if eager_NegativeQ(d):
                return RectifyTangent(u, -a, -b, -r, x)
            e = SmartDenominator(eager_Together(c + d*x))
            c = c*e
            d = d*e
            if eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
                return I*r*Log(RemoveContent(eager_Simplify((c+e)**2+d**2)+eager_Simplify((c+e)**2-d**2)*Cos(2*u)+eager_Simplify(2*(c+e)*d)*Sin(2*u),x))/4 - I*r*Log(RemoveContent(eager_Simplify((c-e)**2+d**2)+eager_Simplify((c-e)**2-d**2)*Cos(2*u)+eager_Simplify(2*(c-e)*d)*Sin(2*u),x))/4
            return I*r*Log(RemoveContent(eager_Simplify((c+e)**2)+eager_Simplify(2*(c+e)*d)*Cos(u)*Sin(u)-eager_Simplify((c+e)**2-d**2)*Sin(u)**2,x))/4 - I*r*Log(RemoveContent(eager_Simplify((c-e)**2)+eager_Simplify(2*(c-e)*d)*Cos(u)*Sin(u)-eager_Simplify((c-e)**2-d**2)*Sin(u)**2,x))/4
        elif eager_NegativeQ(b):
            return RectifyTangent(u, -a, -b, -r, x)
        elif eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
            return r*SimplifyAntiderivative(u,x) + r*ArcTan(eager_Simplify((2*a*b*Cos(2*u)-(1+a**2-b**2)*Sin(2*u))/(a**2+(1+b)**2+(1+a**2-b**2)*Cos(2*u)+2*a*b*Sin(2*u))))
        return r*SimplifyAntiderivative(u,x) - r*ArcTan(eager_ActivateTrig(eager_Simplify((a*b-2*a*b*cos(u)**2+(1+a**2-b**2)*cos(u)*sin(u))/(b*(1+b)+(1+a**2-b**2)*cos(u)**2+2*a*b*cos(u)*sin(u)))))

    u, a, b, x = args
    t = eager_Together(a)
    if PureComplexNumberQ(t) or (eager_ProductQ(t) and any(PureComplexNumberQ(i) for i in t.args)):
        c = a/I
        if eager_NegativeQ(c):
            return RectifyTangent(u, -a, -b, x)
        if ZeroQ(c - 1):
            if eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
                return I*b*ArcTanh(Sin(2*u))/2
            return I*b*ArcTanh(2*cos(u)*sin(u))/2
        e = SmartDenominator(c)
        c = c*e
        return I*b*Log(RemoveContent(e*Cos(u)+c*Sin(u),x))/2 - I*b*Log(RemoveContent(e*Cos(u)-c*Sin(u),x))/2
    elif eager_NegativeQ(a):
        return RectifyTangent(u, -a, -b, x)
    elif ZeroQ(a - 1):
        return b*SimplifyAntiderivative(u, x)
    elif eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
        c =  eager_Simplify((1 + a)/(1 - a))
        numr = SmartNumerator(c)
        denr = SmartDenominator(c)
        return b*SimplifyAntiderivative(u,x) - b*ArcTan(NormalizeLeadTermSigns(denr*Sin(2*u)/(numr+denr*Cos(2*u)))),
    elif eager_PositiveQ(a - 1):
        c = eager_Simplify(1/(a - 1))
        numr = SmartNumerator(c)
        denr = SmartDenominator(c)
        return b*SimplifyAntiderivative(u,x) + b*ArcTan(NormalizeLeadTermSigns(denr*Cos(u)*Sin(u)/(numr+denr*Sin(u)**2))),
    c = eager_Simplify(a/(1 - a))
    numr = SmartNumerator(c)
    denr = SmartDenominator(c)
    return b*SimplifyAntiderivative(u,x) - b*ArcTan(NormalizeLeadTermSigns(denr*Cos(u)*Sin(u)/(numr+denr*Cos(u)**2)))

def RectifyCotangent(*args):
    #(* RectifyCotangent[u,a,b,r,x] returns an expression whose derivative equals the derivative of r*ArcTan[a+b*Cot[u]] wrt x. *)
    if len(args) == 5:
        u, a, b, r, x = args
        t1 = eager_Together(a)
        t2 = eager_Together(b)
        if (PureComplexNumberQ(t1) or (eager_ProductQ(t1) and any(PureComplexNumberQ(i) for i in t1.args))) and (PureComplexNumberQ(t2) or eager_ProductQ(t2) and any(PureComplexNumberQ(i) for i in t2.args)):
            c = a/I
            d = b/I
            if eager_NegativeQ(d):
                return RectifyTangent(u,-a,-b,-r,x)
            e = SmartDenominator(eager_Together(c + d*x))
            c = c*e
            d = d*e
            if eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
                return  I*r*Log(RemoveContent(eager_Simplify((c+e)**2+d**2)-eager_Simplify((c+e)**2-d**2)*Cos(2*u)+eager_Simplify(2*(c+e)*d)*Sin(2*u),x))/4 - I*r*Log(RemoveContent(eager_Simplify((c-e)**2+d**2)-eager_Simplify((c-e)**2-d**2)*Cos(2*u)+eager_Simplify(2*(c-e)*d)*Sin(2*u),x))/4
            return I*r*Log(RemoveContent(eager_Simplify((c+e)**2)-eager_Simplify((c+e)**2-d**2)*Cos(u)**2+eager_Simplify(2*(c+e)*d)*Cos(u)*Sin(u),x))/4 - I*r*Log(RemoveContent(eager_Simplify((c-e)**2)-eager_Simplify((c-e)**2-d**2)*Cos(u)**2+eager_Simplify(2*(c-e)*d)*Cos(u)*Sin(u),x))/4
        elif eager_NegativeQ(b):
            return RectifyCotangent(u,-a,-b,-r,x)
        elif eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
            return -r*SimplifyAntiderivative(u,x) - r*ArcTan(eager_Simplify((2*a*b*Cos(2*u)+(1+a**2-b**2)*Sin(2*u))/(a**2+(1+b)**2-(1+a**2-b**2)*Cos(2*u)+2*a*b*Sin(2*u))))
        return -r*SimplifyAntiderivative(u,x) - r*ArcTan(eager_ActivateTrig(eager_Simplify((a*b-2*a*b*sin(u)**2+(1+a**2-b**2)*cos(u)*sin(u))/(b*(1+b)+(1+a**2-b**2)*sin(u)**2+2*a*b*cos(u)*sin(u)))))

    u, a, b, x = args
    t = eager_Together(a)
    if PureComplexNumberQ(t) or (eager_ProductQ(t) and any(PureComplexNumberQ(i) for i in t.args)):
        c = a/I
        if eager_NegativeQ(c):
            return RectifyCotangent(u,-a,-b,x)
        elif ZeroQ(c - 1):
            if eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
                return -I*b*ArcTanh(Sin(2*u))/2
            return -I*b*ArcTanh(2*Cos(u)*Sin(u))/2
        e = SmartDenominator(c)
        c = c*e
        return -I*b*Log(RemoveContent(c*Cos(u)+e*Sin(u),x))/2 + I*b*Log(RemoveContent(c*Cos(u)-e*Sin(u),x))/2
    elif eager_NegativeQ(a):
        return RectifyCotangent(u,-a,-b,x)
    elif ZeroQ(a-1):
        return b*SimplifyAntiderivative(u,x)
    elif eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))):
        c = eager_Simplify(a - 1)
        numr = SmartNumerator(c)
        denr = SmartDenominator(c)
        return b*SimplifyAntiderivative(u,x) - b*ArcTan(NormalizeLeadTermSigns(denr*Cos(u)*Sin(u)/(numr+denr*Cos(u)**2)))
    c = eager_Simplify(a/(1-a))
    numr = SmartNumerator(c)
    denr = SmartDenominator(c)
    return b*SimplifyAntiderivative(u,x) + b*ArcTan(NormalizeLeadTermSigns(denr*Cos(u)*Sin(u)/(numr+denr*Sin(u)**2)))

def Inequality(*args):
    f = args[1::2]
    e = args[0::2]
    r = []
    for i in range(0, len(f)):
        r.append(f[i](e[i], e[i + 1]))
    return all(r)

def eager_Condition(r, c):
    # returns r if c is True
    if c:
        return r
    else:
        raise NotImplementedError('In Condition()')

def eager_Simp(u, x):
    return NormalizeSumFactors(SimpHelp(u, x))

def SimpHelp(u, x):
    if eager_AtomQ(u):
        return u
    elif eager_FreeQ(u, x):
        v = SmartSimplify(u)
        if eager_LeafCount(v) <= eager_LeafCount(u):
            return v
        return u
    elif eager_ProductQ(u):
        #m = MatchQ[Rest[u],a_.+n_*Pi+b_.*v_ /; FreeQ[{a,b},x] && Not[FreeQ[v,x]] && EqQ[n^2,1/4]]
        #if EqQ(First(u), S(1)/2) and m:
        #    if
        #If[EqQ[First[u],1/2] && MatchQ[Rest[u],a_.+n_*Pi+b_.*v_ /; FreeQ[{a,b},x] && Not[FreeQ[v,x]] && EqQ[n^2,1/4]],
        #  If[MatchQ[Rest[u],n_*Pi+b_.*v_ /; FreeQ[b,x] && Not[FreeQ[v,x]] && EqQ[n^2,1/4]],
        #    Map[Function[1/2*#],Rest[u]],
        #  If[MatchQ[Rest[u],m_*a_.+n_*Pi+p_*b_.*v_ /; FreeQ[{a,b},x] && Not[FreeQ[v,x]] && IntegersQ[m/2,p/2]],
        #    Map[Function[1/2*#],Rest[u]],
        #  u]],

        v = eager_FreeFactors(u, x)
        w = eager_NonfreeFactors(u, x)
        v = NumericFactor(v)*SmartSimplify(NonnumericFactors(v)*x**2)/x**2
        if eager_ProductQ(w):
            w = Mul(*[SimpHelp(i,x) for i in w.args])
        else:
            w = SimpHelp(w, x)
        w = FactorNumericGcd(w)
        v = MergeFactors(v, w)
        if eager_ProductQ(v):
            return Mul(*[SimpFixFactor(i, x) for i in v.args])
        return v
    elif eager_SumQ(u):
        Pi = pi
        a_ = Wild('a', exclude=[x])
        b_ = Wild('b', exclude=[x, 0])
        n_ = Wild('n', exclude=[x, 0, 0])
        pattern = a_ + n_*Pi + b_*x
        match = u.match(pattern)
        m = False
        if match:
            if eager_EqQ(match[n_]**3, S(1)/16):
                m = True
        if m:
            return u
        elif eager_PolynomialQ(u, x) and eager_Exponent(u, x) <= 0:
            return SimpHelp(eager_Coefficient(u, x, 0), x)
        elif eager_PolynomialQ(u, x) and eager_Exponent(u, x) == 1 and eager_Coefficient(u, x, 0) == 0:
            return SimpHelp(eager_Coefficient(u, x, 1), x)*x

        v = 0
        w = 0
        for i in u.args:
            if eager_FreeQ(i, x):
                v = i + v
            else:
                w = i + w
        v = SmartSimplify(v)
        if eager_SumQ(w):
            w = Add(*[SimpHelp(i, x) for i in w.args])
        else:
            w = SimpHelp(w, x)
        return v + w
    return u.func(*[SimpHelp(i, x) for i in u.args])

def eager_SplitProduct(func, u):
    #(* If func[v] is True for a factor v of u, SplitProduct[func,u] returns {v, u/v} where v is the first such factor; else it returns False. *)
    if eager_ProductQ(u):
        if func(eager_First(u)):
            return [eager_First(u), eager_Rest(u)]
        lst = eager_SplitProduct(func, eager_Rest(u))
        if eager_AtomQ(lst):
            return False
        return [lst[0], eager_First(u)*lst[1]]
    if func(u):
        return [u, 1]
    return False

def SplitSum(func, u):
    # (* If func[v] is nonatomic for a term v of u, SplitSum[func,u] returns {func[v], u-v} where v is the first such term; else it returns False. *)
    if eager_SumQ(u):
        if eager_Not(eager_AtomQ(func(eager_First(u)))):
            return [func(eager_First(u)), eager_Rest(u)]
        lst = SplitSum(func, eager_Rest(u))
        if eager_AtomQ(lst):
            return False
        return [lst[0], eager_First(u) + lst[1]]
    elif eager_Not(eager_AtomQ(func(u))):
        return [func(u), 0]
    return False

def eager_SubstFor(*args):
    if len(args) == 4:
        w, v, u, x = args
        # u is a function of v. SubstFor(w,v,u,x) returns w times u with v replaced by x.
        return eager_SimplifyIntegrand(w*eager_SubstFor(v, u, x), x)
    v, u, x = args
    # u is a function of v. SubstFor(v, u, x) returns u with v replaced by x.
    if eager_AtomQ(v):
        return eager_Subst(u, v, x)
    elif eager_Not(eager_EqQ(eager_FreeFactors(v, x), 1)):
        return eager_SubstFor(eager_NonfreeFactors(v, x), u, x/eager_FreeFactors(v, x))
    elif SinQ(v):
        return SubstForTrig(u, x, Sqrt(1 - x**2), v.args[0], x)
    elif CosQ(v):
        return SubstForTrig(u, Sqrt(1 - x**2), x, v.args[0], x)
    elif TanQ(v):
        return SubstForTrig(u, x/Sqrt(1 + x**2), 1/Sqrt(1 + x**2), v.args[0], x)
    elif CotQ(v):
        return SubstForTrig(u, 1/Sqrt(1 + x**2), x/Sqrt(1 + x**2), v.args[0], x)
    elif SecQ(v):
        return SubstForTrig(u, 1/Sqrt(1 - x**2), 1/x, v.args[0], x)
    elif CscQ(v):
        return SubstForTrig(u, 1/x, 1/Sqrt(1 - x**2), v.args[0], x)
    elif SinhQ(v):
        return SubstForHyperbolic(u, x, Sqrt(1 + x**2), v.args[0], x)
    elif CoshQ(v):
        return SubstForHyperbolic(u, Sqrt( - 1 + x**2), x, v.args[0], x)
    elif TanhQ(v):
        return SubstForHyperbolic(u, x/Sqrt(1 - x**2), 1/Sqrt(1 - x**2), v.args[0], x)
    elif CothQ(v):
        return SubstForHyperbolic(u, 1/Sqrt( - 1 + x**2), x/Sqrt( - 1 + x**2), v.args[0], x)
    elif SechQ(v):
        return SubstForHyperbolic(u, 1/Sqrt( - 1 + x**2), 1/x, v.args[0], x)
    elif CschQ(v):
        return SubstForHyperbolic(u, 1/x, 1/Sqrt(1 + x**2), v.args[0], x)
    else:
        return SubstForAux(u, v, x)

def SubstForAux(u, v, x):
    # u is a function of v. SubstForAux(u, v, x) returns u with v replaced by x.
    if u==v:
        return x
    elif eager_AtomQ(u):
        if eager_PowerQ(v):
            if eager_FreeQ(v.exp, x) and ZeroQ(u - v.base):
                return x**eager_Simplify(1/v.exp)
        return u
    elif eager_PowerQ(u):
        if eager_FreeQ(u.exp, x):
            if ZeroQ(u.base - v):
                return x**u.exp
            if eager_PowerQ(v):
                if eager_FreeQ(v.exp, x) and ZeroQ(u.base - v.base):
                    return x**eager_Simplify(u.exp/v.exp)
            return SubstForAux(u.base, v, x)**u.exp
    elif eager_ProductQ(u) and eager_Not(eager_EqQ(eager_FreeFactors(u, x), 1)):
        return eager_FreeFactors(u, x)*SubstForAux(eager_NonfreeFactors(u, x), v, x)
    elif eager_ProductQ(u) and eager_ProductQ(v):
        return SubstForAux(eager_First(u), eager_First(v), x)

    return u.func(*[SubstForAux(i, v, x) for i in u.args])

def FresnelS(x):
    return fresnels(x)

def FresnelC(x):
    return fresnelc(x)

def Erf(x):
    return erf(x)

def Erfc(x):
    return erfc(x)

def Erfi(x):
    return erfi(x)

class Gamma(Function):
    @classmethod
    def eval(cls,*args):
        a = args[0]
        if len(args) == 1:
            return gamma(a)
        else:
            b = args[1]
            if (eager_NumericQ(a) and eager_NumericQ(b)) or a == 1:
                return uppergamma(a, b)

def _TrigPowerOfLinearMatchQ(u, x):
    # Rubi's structural shortcut inside FunctionOfTrigOfLinearQ:
    #   MatchQ[u, (c_.+d_.*x)^m_.*(a_.+b_.*trig_[e_.+f_.*x])^n_. /;
    #            FreeQ[{a,b,c,d,e,f,m,n},x] && (TrigQ[trig] || HyperbolicQ[trig])]
    # It catches poly*trig forms (e.g. x*Sin[x]) that FunctionOfTrig alone rejects
    # because of the free x-power factor. The heads checked are the ACTIVE trig and
    # hyperbolic functions only, so an already-inert integrand does NOT match here --
    # that keeps the deactivation dispatch idempotent (no infinite loop).
    a = Wild('a', exclude=[x]); b = Wild('b', exclude=[x])
    c = Wild('c', exclude=[x]); d = Wild('d', exclude=[x])
    e = Wild('e', exclude=[x]); f = Wild('f', exclude=[x])
    m = Wild('m', exclude=[x]); n = Wild('n', exclude=[x])
    for trig in (sin, cos, tan, cot, sec, csc, sinh, cosh, tanh, coth, sech, csch):
        match = u.match((c + d*x)**m * (a + b*trig(e + f*x))**n)
        if match is not None and match.get(f) not in (None, S(0)) and match.get(n) not in (None, S(0)):
            return True
    return False


def eager_FunctionOfTrigOfLinearQ(u, x):
    # If u is an algebraic function of trig functions of a linear function of x,
    # FunctionOfTrigOfLinearQ[u,x] returns True; else it returns False.
    # Faithful port of Rubi's two-branch definition (see IntegrationUtilityFunctions.m):
    #   the structural MatchQ shortcut, OR (FunctionOfTrig non-False AND AlgebraicTrigFunctionQ).
    if _TrigPowerOfLinearMatchQ(u, x):
        return True
    v = eager_FunctionOfTrig(u, None, x)
    return v is not None and v is not False and bool(AlgebraicTrigFunctionQ(u, x))

def ElementaryFunctionQ(u):
    # ElementaryExpressionQ[u] returns True if u is a sum, product, or power and all the operands
    # are elementary expressions; or if u is a call on a trig, hyperbolic, or inverse function
    # and all the arguments are elementary expressions; else it returns False.
    if eager_AtomQ(u):
        return True
    elif eager_SumQ(u) or eager_ProductQ(u) or eager_PowerQ(u) or eager_TrigQ(u) or eager_HyperbolicQ(u) or eager_InverseFunctionQ(u):
        for i in u.args:
            if not ElementaryFunctionQ(i):
                return False
        return True
    return False

def eager_UnsameQ(a, b):
    return a != b


def _SimpFixFactor():
    replacer = ManyToOneReplacer()

    pattern1 = Pattern(UtilityOperator(Pow(Add(Mul(eager_Complex(S(0), c_), WildSymbol('a', optional_value=S(1))), Mul(eager_Complex(S(0), d_), WildSymbol('b', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda p: eager_IntegerQ(p)))
    rule1 = _ReplacementRuleWrapped(pattern1, lambda b, c, x, a, p, d : Mul(Pow(I, p), SimpFixFactor(Pow(Add(Mul(a, c), Mul(b, d)), p), x)))
    replacer.add(rule1)

    pattern2 = Pattern(UtilityOperator(Pow(Add(Mul(eager_Complex(S(0), d_), WildSymbol('a', optional_value=S(1))), Mul(eager_Complex(S(0), e_), WildSymbol('b', optional_value=S(1))), Mul(eager_Complex(S(0), f_), WildSymbol('c', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda p: eager_IntegerQ(p)))
    rule2 = _ReplacementRuleWrapped(pattern2, lambda b, c, x, f, a, p, e, d : Mul(Pow(I, p), SimpFixFactor(Pow(Add(Mul(a, d), Mul(b, e), Mul(c, f)), p), x)))
    replacer.add(rule2)

    pattern3 = Pattern(UtilityOperator(Pow(Add(Mul(WildSymbol('a', optional_value=S(1)), Pow(c_, r_)), Mul(WildSymbol('b', optional_value=S(1)), Pow(x_, WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)), _patched_custom_constraint_call(lambda c: eager_AtomQ(c)), _patched_custom_constraint_call(lambda r: eager_RationalQ(r)), _patched_custom_constraint_call(lambda r: Less(r, S(0))))
    rule3 = _ReplacementRuleWrapped(pattern3, lambda b, c, r, n, x, a, p : Mul(Pow(c, Mul(r, p)), SimpFixFactor(Pow(Add(a, Mul(Mul(b, Pow(Pow(c, r), S(-1))), Pow(x, n))), p), x)))
    replacer.add(rule3)

    pattern4 = Pattern(UtilityOperator(Pow(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('b', optional_value=S(1)), Pow(c_, r_), Pow(x_, WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)), _patched_custom_constraint_call(lambda c: eager_AtomQ(c)), _patched_custom_constraint_call(lambda r: eager_RationalQ(r)), _patched_custom_constraint_call(lambda r: Less(r, S(0))))
    rule4 = _ReplacementRuleWrapped(pattern4, lambda b, c, r, n, x, a, p : Mul(Pow(c, Mul(r, p)), SimpFixFactor(Pow(Add(Mul(a, Pow(Pow(c, r), S(-1))), Mul(b, Pow(x, n))), p), x)))
    replacer.add(rule4)

    pattern5 = Pattern(UtilityOperator(Pow(Add(Mul(WildSymbol('a', optional_value=S(1)), Pow(c_, WildSymbol('s', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(c_, WildSymbol('r', optional_value=S(1))), Pow(x_, WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)), _patched_custom_constraint_call(lambda r, s: eager_RationalQ(s, r)), _patched_custom_constraint_call(lambda r, s: Inequality(S(0), Less, s, LessEqual, r)), _patched_custom_constraint_call(lambda p, c, s: eager_UnsameQ(Pow(c, Mul(s, p)), S(-1))))
    rule5 = _ReplacementRuleWrapped(pattern5, lambda b, c, r, n, x, a, p, s : Mul(Pow(c, Mul(s, p)), SimpFixFactor(Pow(Add(a, Mul(b, Pow(c, Add(r, Mul(S(-1), s))), Pow(x, n))), p), x)))
    replacer.add(rule5)

    pattern6 = Pattern(UtilityOperator(Pow(Add(Mul(WildSymbol('a', optional_value=S(1)), Pow(c_, WildSymbol('s', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(c_, WildSymbol('r', optional_value=S(1))), Pow(x_, WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)), _patched_custom_constraint_call(lambda r, s: eager_RationalQ(s, r)), _patched_custom_constraint_call(lambda s, r: Less(S(0), r, s)), _patched_custom_constraint_call(lambda p, c, r: eager_UnsameQ(Pow(c, Mul(r, p)), S(-1))))
    rule6 = _ReplacementRuleWrapped(pattern6, lambda b, c, r, n, x, a, p, s : Mul(Pow(c, Mul(r, p)), SimpFixFactor(Pow(Add(Mul(a, Pow(c, Add(s, Mul(S(-1), r)))), Mul(b, Pow(x, n))), p), x)))
    replacer.add(rule6)

    return replacer


def SimpFixFactor(expr, x):
    result = SimpFixFactor_replacer.replace(UtilityOperator(expr, x))
    if isinstance(result, Operation) and result.head == UtilityOp:
        return expr
    return matchpy_to_sympy(result)


def _FixSimplify():
    Plus = Add
    def cons_f1(n):
        return eager_OddQ(n)
    cons1 = _patched_custom_constraint_call(cons_f1)

    def cons_f2(m):
        return eager_RationalQ(m)
    cons2 = _patched_custom_constraint_call(cons_f2)

    def cons_f3(n):
        return eager_FractionQ(n)
    cons3 = _patched_custom_constraint_call(cons_f3)

    def cons_f4(u):
        return SqrtNumberSumQ(u)
    cons4 = _patched_custom_constraint_call(cons_f4)

    def cons_f5(v):
        return SqrtNumberSumQ(v)
    cons5 = _patched_custom_constraint_call(cons_f5)

    def cons_f6(u):
        return eager_PositiveQ(u)
    cons6 = _patched_custom_constraint_call(cons_f6)

    def cons_f7(v):
        return eager_PositiveQ(v)
    cons7 = _patched_custom_constraint_call(cons_f7)

    def cons_f8(v):
        return SqrtNumberSumQ(S(1)/v)
    cons8 = _patched_custom_constraint_call(cons_f8)

    def cons_f9(m):
        return eager_IntegerQ(m)
    cons9 = _patched_custom_constraint_call(cons_f9)

    def cons_f10(u):
        return eager_NegativeQ(u)
    cons10 = _patched_custom_constraint_call(cons_f10)

    def cons_f11(n, m, a, b):
        return eager_RationalQ(a, b, m, n)
    cons11 = _patched_custom_constraint_call(cons_f11)

    def cons_f12(a):
        return Greater(a, S(0))
    cons12 = _patched_custom_constraint_call(cons_f12)

    def cons_f13(b):
        return Greater(b, S(0))
    cons13 = _patched_custom_constraint_call(cons_f13)

    def cons_f14(p):
        return PositiveIntegerQ(p)
    cons14 = _patched_custom_constraint_call(cons_f14)

    def cons_f15(p):
        return eager_IntegerQ(p)
    cons15 = _patched_custom_constraint_call(cons_f15)

    def cons_f16(p, n):
        return Greater(-n + p, S(0))
    cons16 = _patched_custom_constraint_call(cons_f16)

    def cons_f17(a, b):
        return SameQ(a + b, S(0))
    cons17 = _patched_custom_constraint_call(cons_f17)

    def cons_f18(n):
        return eager_Not(eager_IntegerQ(n))
    cons18 = _patched_custom_constraint_call(cons_f18)

    def cons_f19(c, a, b, d):
        return ZeroQ(-a*d + b*c)
    cons19 = _patched_custom_constraint_call(cons_f19)

    def cons_f20(a):
        return eager_Not(eager_RationalQ(a))
    cons20 = _patched_custom_constraint_call(cons_f20)

    def cons_f21(t):
        return eager_IntegerQ(t)
    cons21 = _patched_custom_constraint_call(cons_f21)

    def cons_f22(n, m):
        return eager_RationalQ(m, n)
    cons22 = _patched_custom_constraint_call(cons_f22)

    def cons_f23(n, m):
        return Inequality(S(0), Less, m, LessEqual, n)
    cons23 = _patched_custom_constraint_call(cons_f23)

    def cons_f24(p, n, m):
        return eager_RationalQ(m, n, p)
    cons24 = _patched_custom_constraint_call(cons_f24)

    def cons_f25(p, n, m):
        return Inequality(S(0), Less, m, LessEqual, n, LessEqual, p)
    cons25 = _patched_custom_constraint_call(cons_f25)

    def cons_f26(p, n, m, q):
        return Inequality(S(0), Less, m, LessEqual, n, LessEqual, p, LessEqual, q)
    cons26 = _patched_custom_constraint_call(cons_f26)

    def cons_f27(w):
        return eager_Not(eager_RationalQ(w))
    cons27 = _patched_custom_constraint_call(cons_f27)

    def cons_f28(n):
        return Less(n, S(0))
    cons28 = _patched_custom_constraint_call(cons_f28)

    def cons_f29(n, w, v):
        return ZeroQ(v + w**(-n))
    cons29 = _patched_custom_constraint_call(cons_f29)

    def cons_f30(n):
        return eager_IntegerQ(n)
    cons30 = _patched_custom_constraint_call(cons_f30)

    def cons_f31(w, v):
        return ZeroQ(v + w)
    cons31 = _patched_custom_constraint_call(cons_f31)

    def cons_f32(p, n):
        return eager_IntegerQ(n/p)
    cons32 = _patched_custom_constraint_call(cons_f32)

    def cons_f33(w, v):
        return ZeroQ(v - w)
    cons33 = _patched_custom_constraint_call(cons_f33)

    def cons_f34(p, n):
        return eager_IntegersQ(n, n/p)
    cons34 = _patched_custom_constraint_call(cons_f34)

    def cons_f35(a):
        return eager_AtomQ(a)
    cons35 = _patched_custom_constraint_call(cons_f35)

    def cons_f36(b):
        return eager_AtomQ(b)
    cons36 = _patched_custom_constraint_call(cons_f36)

    pattern1 = Pattern(UtilityOperator((w_ + eager_Complex(S(0), b_)*WildSymbol('v', optional_value=S(1)))**WildSymbol('n', optional_value=S(1))*eager_Complex(S(0), a_)*WildSymbol('u', optional_value=S(1))), cons1)
    def replacement1(n, u, w, v, a, b):
        return (S(-1))**(n/S(2) + S(1)/2)*a*u*FixSimplify((b*v - w*eager_Complex(S(0), S(1)))**n)
    rule1 = _ReplacementRuleWrapped(pattern1, replacement1)
    def With2(m, n, u, w, v):
        z = u**(m/eager_GCD(m, n))*v**(n/eager_GCD(m, n))
        if Or(AbsurdNumberQ(z), SqrtNumberSumQ(z)):
            return True
        return False
    pattern2 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*v_**n_*WildSymbol('w', optional_value=S(1))), cons2, cons3, cons4, cons5, cons6, cons7, _patched_custom_constraint_call(With2))
    def replacement2(m, n, u, w, v):
        z = u**(m/eager_GCD(m, n))*v**(n/eager_GCD(m, n))
        return FixSimplify(w*z**eager_GCD(m, n))
    rule2 = _ReplacementRuleWrapped(pattern2, replacement2)
    def With3(m, n, u, w, v):
        z = u**(m/eager_GCD(m, -n))*v**(n/eager_GCD(m, -n))
        if Or(AbsurdNumberQ(z), SqrtNumberSumQ(z)):
            return True
        return False
    pattern3 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*v_**n_*WildSymbol('w', optional_value=S(1))), cons2, cons3, cons4, cons8, cons6, cons7, _patched_custom_constraint_call(With3))
    def replacement3(m, n, u, w, v):
        z = u**(m/eager_GCD(m, -n))*v**(n/eager_GCD(m, -n))
        return FixSimplify(w*z**eager_GCD(m, -n))
    rule3 = _ReplacementRuleWrapped(pattern3, replacement3)
    def With4(m, n, u, w, v):
        z = v**(n/eager_GCD(m, n))*(-u)**(m/eager_GCD(m, n))
        if Or(AbsurdNumberQ(z), SqrtNumberSumQ(z)):
            return True
        return False
    pattern4 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*v_**n_*WildSymbol('w', optional_value=S(1))), cons9, cons3, cons4, cons5, cons10, cons7, _patched_custom_constraint_call(With4))
    def replacement4(m, n, u, w, v):
        z = v**(n/eager_GCD(m, n))*(-u)**(m/eager_GCD(m, n))
        return FixSimplify(-w*z**eager_GCD(m, n))
    rule4 = _ReplacementRuleWrapped(pattern4, replacement4)
    def With5(m, n, u, w, v):
        z = v**(n/eager_GCD(m, -n))*(-u)**(m/eager_GCD(m, -n))
        if Or(AbsurdNumberQ(z), SqrtNumberSumQ(z)):
            return True
        return False
    pattern5 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*v_**n_*WildSymbol('w', optional_value=S(1))), cons9, cons3, cons4, cons8, cons10, cons7, _patched_custom_constraint_call(With5))
    def replacement5(m, n, u, w, v):
        z = v**(n/eager_GCD(m, -n))*(-u)**(m/eager_GCD(m, -n))
        return FixSimplify(-w*z**eager_GCD(m, -n))
    rule5 = _ReplacementRuleWrapped(pattern5, replacement5)
    def With6(p, m, n, u, w, v, a, b):
        c = a**(m/p)*b**n
        if eager_RationalQ(c):
            return True
        return False
    pattern6 = Pattern(UtilityOperator(a_**m_*(b_**n_*WildSymbol('v', optional_value=S(1)) + u_)**WildSymbol('p', optional_value=S(1))*WildSymbol('w', optional_value=S(1))), cons11, cons12, cons13, cons14, _patched_custom_constraint_call(With6))
    def replacement6(p, m, n, u, w, v, a, b):
        c = a**(m/p)*b**n
        return FixSimplify(w*(a**(m/p)*u + c*v)**p)
    rule6 = _ReplacementRuleWrapped(pattern6, replacement6)
    pattern7 = Pattern(UtilityOperator(a_**WildSymbol('m', optional_value=S(1))*(a_**n_*WildSymbol('u', optional_value=S(1)) + b_**WildSymbol('p', optional_value=S(1))*WildSymbol('v', optional_value=S(1)))*WildSymbol('w', optional_value=S(1))), cons2, cons3, cons15, cons16, cons17)
    def replacement7(p, m, n, u, w, v, a, b):
        return FixSimplify(a**(m + n)*w*((S(-1))**p*a**(-n + p)*v + u))
    rule7 = _ReplacementRuleWrapped(pattern7, replacement7)
    def With8(m, d, n, w, c, a, b):
        q = b/d
        if eager_FreeQ(q, Plus):
            return True
        return False
    pattern8 = Pattern(UtilityOperator((a_ + b_)**WildSymbol('m', optional_value=S(1))*(c_ + d_)**n_*WildSymbol('w', optional_value=S(1))), cons9, cons18, cons19, _patched_custom_constraint_call(With8))
    def replacement8(m, d, n, w, c, a, b):
        q = b/d
        return FixSimplify(q**m*w*(c + d)**(m + n))
    rule8 = _ReplacementRuleWrapped(pattern8, replacement8)
    pattern9 = Pattern(UtilityOperator((a_**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1)) + a_**WildSymbol('n', optional_value=S(1))*WildSymbol('v', optional_value=S(1)))**WildSymbol('t', optional_value=S(1))*WildSymbol('w', optional_value=S(1))), cons20, cons21, cons22, cons23)
    def replacement9(m, n, u, w, v, a, t):
        return FixSimplify(a**(m*t)*w*(a**(-m + n)*v + u)**t)
    rule9 = _ReplacementRuleWrapped(pattern9, replacement9)
    pattern10 = Pattern(UtilityOperator((a_**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1)) + a_**WildSymbol('n', optional_value=S(1))*WildSymbol('v', optional_value=S(1)) + a_**WildSymbol('p', optional_value=S(1))*WildSymbol('z', optional_value=S(1)))**WildSymbol('t', optional_value=S(1))*WildSymbol('w', optional_value=S(1))), cons20, cons21, cons24, cons25)
    def replacement10(p, m, n, u, w, v, a, z, t):
        return FixSimplify(a**(m*t)*w*(a**(-m + n)*v + a**(-m + p)*z + u)**t)
    rule10 = _ReplacementRuleWrapped(pattern10, replacement10)
    pattern11 = Pattern(UtilityOperator((a_**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1)) + a_**WildSymbol('n', optional_value=S(1))*WildSymbol('v', optional_value=S(1)) + a_**WildSymbol('p', optional_value=S(1))*WildSymbol('z', optional_value=S(1)) + a_**WildSymbol('q', optional_value=S(1))*WildSymbol('y', optional_value=S(1)))**WildSymbol('t', optional_value=S(1))*WildSymbol('w', optional_value=S(1))), cons20, cons21, cons24, cons26)
    def replacement11(p, m, n, u, q, w, v, a, z, y, t):
        return FixSimplify(a**(m*t)*w*(a**(-m + n)*v + a**(-m + p)*z + a**(-m + q)*y + u)**t)
    rule11 = _ReplacementRuleWrapped(pattern11, replacement11)
    pattern12 = Pattern(UtilityOperator((sqrt(v_)*WildSymbol('b', optional_value=S(1)) + sqrt(v_)*WildSymbol('c', optional_value=S(1)) + sqrt(v_)*WildSymbol('d', optional_value=S(1)) + sqrt(v_)*WildSymbol('a', optional_value=S(1)) + WildSymbol('u', optional_value=S(0)))*WildSymbol('w', optional_value=S(1))))
    def replacement12(d, u, w, v, c, a, b):
        return FixSimplify(w*(u + sqrt(v)*FixSimplify(a + b + c + d)))
    rule12 = _ReplacementRuleWrapped(pattern12, replacement12)
    pattern13 = Pattern(UtilityOperator((sqrt(v_)*WildSymbol('b', optional_value=S(1)) + sqrt(v_)*WildSymbol('c', optional_value=S(1)) + sqrt(v_)*WildSymbol('a', optional_value=S(1)) + WildSymbol('u', optional_value=S(0)))*WildSymbol('w', optional_value=S(1))))
    def replacement13(u, w, v, c, a, b):
        return FixSimplify(w*(u + sqrt(v)*FixSimplify(a + b + c)))
    rule13 = _ReplacementRuleWrapped(pattern13, replacement13)
    pattern14 = Pattern(UtilityOperator((sqrt(v_)*WildSymbol('b', optional_value=S(1)) + sqrt(v_)*WildSymbol('a', optional_value=S(1)) + WildSymbol('u', optional_value=S(0)))*WildSymbol('w', optional_value=S(1))))
    def replacement14(u, w, v, a, b):
        return FixSimplify(w*(u + sqrt(v)*FixSimplify(a + b)))
    rule14 = _ReplacementRuleWrapped(pattern14, replacement14)
    pattern15 = Pattern(UtilityOperator(v_**m_*w_**n_*WildSymbol('u', optional_value=S(1))), cons2, cons27, cons3, cons28, cons29)
    def replacement15(m, n, u, w, v):
        return -FixSimplify(u*v**(m + S(-1)))
    rule15 = _ReplacementRuleWrapped(pattern15, replacement15)
    pattern16 = Pattern(UtilityOperator(v_**m_*w_**WildSymbol('n', optional_value=S(1))*WildSymbol('u', optional_value=S(1))), cons2, cons27, cons30, cons31)
    def replacement16(m, n, u, w, v):
        return (S(-1))**n*FixSimplify(u*v**(m + n))
    rule16 = _ReplacementRuleWrapped(pattern16, replacement16)
    pattern17 = Pattern(UtilityOperator(w_**WildSymbol('n', optional_value=S(1))*(-v_**WildSymbol('p', optional_value=S(1)))**m_*WildSymbol('u', optional_value=S(1))), cons2, cons27, cons32, cons33)
    def replacement17(p, m, n, u, w, v):
        return (S(-1))**(n/p)*FixSimplify(u*(-v**p)**(m + n/p))
    rule17 = _ReplacementRuleWrapped(pattern17, replacement17)
    pattern18 = Pattern(UtilityOperator(w_**WildSymbol('n', optional_value=S(1))*(-v_**WildSymbol('p', optional_value=S(1)))**m_*WildSymbol('u', optional_value=S(1))), cons2, cons27, cons34, cons31)
    def replacement18(p, m, n, u, w, v):
        return (S(-1))**(n + n/p)*FixSimplify(u*(-v**p)**(m + n/p))
    rule18 = _ReplacementRuleWrapped(pattern18, replacement18)
    pattern19 = Pattern(UtilityOperator((a_ - b_)**WildSymbol('m', optional_value=S(1))*(a_ + b_)**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1))), cons9, cons35, cons36)
    def replacement19(m, u, a, b):
        return u*(a**S(2) - b**S(2))**m
    rule19 = _ReplacementRuleWrapped(pattern19, replacement19)
    pattern20 = Pattern(UtilityOperator((S(729)*c - e*(-S(20)*e + S(540)))**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1))), cons2)
    def replacement20(m, u):
        return u*(a*e**S(2) - b*d*e + c*d**S(2))**m
    rule20 = _ReplacementRuleWrapped(pattern20, replacement20)
    pattern21 = Pattern(UtilityOperator((S(729)*c + e*(S(20)*e + S(-540)))**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1))), cons2)
    def replacement21(m, u):
        return u*(a*e**S(2) - b*d*e + c*d**S(2))**m
    rule21 = _ReplacementRuleWrapped(pattern21, replacement21)
    pattern22 = Pattern(UtilityOperator(u_))
    def replacement22(u):
        return u
    rule22 = _ReplacementRuleWrapped(pattern22, replacement22)
    return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, ]


@_pure_expr_cache(maxsize=20000)
def _fixsimplify_scalar(expr):
    # ROOT-ONLY matching: every FixSimplify pattern is rooted at UtilityOp, a head
    # that cannot occur anywhere INSIDE the converted subject (UtilityOperator is
    # only ever applied here, at the top). So the previous
    # ``replace_all(UtilityOperator(expr), FixSimplify_rules)`` could only ever
    # fire at the root -- yet it scanned the whole tree, and the identity rule
    # (the final ``u_ -> u`` fall-through) unwrapped the root and forced a SECOND
    # full-tree pass of all 22 rules over every node. Trying the rules once at
    # the root is provably equivalent and skips both scans; when nothing fires we
    # return the ORIGINAL SymPy object, avoiding the matchpy->sympy reconversion.
    # (Profiled at 60% of the runtime of rational-function integrals with two
    # symbolic quadratics: PosQ -> TogetherSimplify -> FixSimplify on every large
    # coefficient the DFS produces.)
    subject = UtilityOperator(expr)
    for pattern, replacement in FixSimplify_rules[:-1]:  # last rule is the identity fall-through
        try:
            subst = next(iter(matchpy_match(subject, pattern)))
        except StopIteration:
            continue
        return matchpy_to_sympy(replacement(**subst))
    return expr


def FixSimplify(expr):
    if isinstance(expr, (list, tuple, TupleArg)):
        return [FixSimplify(i) for i in expr]
    return _fixsimplify_scalar(expr)


def _SimplifyAntiderivativeSum():
    replacer = ManyToOneReplacer()

    pattern1 = Pattern(UtilityOperator(Add(Mul(Log(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('A', optional_value=S(1))), Mul(Log(Cos(u_)), WildSymbol('B', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A, n: ZeroQ(Add(Mul(n, A), Mul(S(1), B)))))
    rule1 = _ReplacementRuleWrapped(pattern1, lambda n, x, v, b, B, A, u, a : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(a, Pow(Cos(u), n)), Mul(b, Pow(Sin(u), n))), x)))))
    replacer.add(rule1)

    pattern2 = Pattern(UtilityOperator(Add(Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_)), WildSymbol('A', optional_value=S(1))), Mul(Log(Sin(u_)), WildSymbol('B', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A, n: ZeroQ(Add(Mul(n, A), Mul(S(1), B)))))
    rule2 = _ReplacementRuleWrapped(pattern2, lambda n, x, v, b, B, A, a, u : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(a, Pow(Sin(u), n)), Mul(b, Pow(Cos(u), n))), x)))))
    replacer.add(rule2)

    pattern3 = Pattern(UtilityOperator(Add(Mul(Log(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('A', optional_value=S(1))), Mul(Log(Add(c_, Mul(WildSymbol('d', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('B', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda d, x: eager_FreeQ(d, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A: ZeroQ(Add(A, B))))
    rule3 = _ReplacementRuleWrapped(pattern3, lambda n, x, v, b, A, B, u, c, d, a : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(a, Pow(Cos(u), n)), Mul(b, Pow(Sin(u), n))), x))), Mul(B, Log(RemoveContent(Add(Mul(c, Pow(Cos(u), n)), Mul(d, Pow(Sin(u), n))), x)))))
    replacer.add(rule3)

    pattern4 = Pattern(UtilityOperator(Add(Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_)), WildSymbol('A', optional_value=S(1))), Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('d', optional_value=S(1))), c_)), WildSymbol('B', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda d, x: eager_FreeQ(d, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A: ZeroQ(Add(A, B))))
    rule4 = _ReplacementRuleWrapped(pattern4, lambda n, x, v, b, A, B, c, a, d, u : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(b, Pow(Cos(u), n)), Mul(a, Pow(Sin(u), n))), x))), Mul(B, Log(RemoveContent(Add(Mul(d, Pow(Cos(u), n)), Mul(c, Pow(Sin(u), n))), x)))))
    replacer.add(rule4)

    pattern5 = Pattern(UtilityOperator(Add(Mul(Log(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('A', optional_value=S(1))), Mul(Log(Add(c_, Mul(WildSymbol('d', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('B', optional_value=S(1))), Mul(Log(Add(e_, Mul(WildSymbol('f', optional_value=S(1)), Pow(Tan(u_), WildSymbol('n', optional_value=S(1)))))), WildSymbol('C', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda d, x: eager_FreeQ(d, x)), _patched_custom_constraint_call(lambda e, x: eager_FreeQ(e, x)), _patched_custom_constraint_call(lambda f, x: eager_FreeQ(f, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda C, x: eager_FreeQ(C, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A, C: ZeroQ(Add(A, B, C))))
    rule5 = _ReplacementRuleWrapped(pattern5, lambda n, e, x, v, b, A, B, u, c, f, d, a, C : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(a, Pow(Cos(u), n)), Mul(b, Pow(Sin(u), n))), x))), Mul(B, Log(RemoveContent(Add(Mul(c, Pow(Cos(u), n)), Mul(d, Pow(Sin(u), n))), x))), Mul(C, Log(RemoveContent(Add(Mul(e, Pow(Cos(u), n)), Mul(f, Pow(Sin(u), n))), x)))))
    replacer.add(rule5)

    pattern6 = Pattern(UtilityOperator(Add(Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_)), WildSymbol('A', optional_value=S(1))), Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('d', optional_value=S(1))), c_)), WildSymbol('B', optional_value=S(1))), Mul(Log(Add(Mul(Pow(Cot(u_), WildSymbol('n', optional_value=S(1))), WildSymbol('f', optional_value=S(1))), e_)), WildSymbol('C', optional_value=S(1))), WildSymbol('v', optional_value=S(0))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda d, x: eager_FreeQ(d, x)), _patched_custom_constraint_call(lambda e, x: eager_FreeQ(e, x)), _patched_custom_constraint_call(lambda f, x: eager_FreeQ(f, x)), _patched_custom_constraint_call(lambda A, x: eager_FreeQ(A, x)), _patched_custom_constraint_call(lambda B, x: eager_FreeQ(B, x)), _patched_custom_constraint_call(lambda C, x: eager_FreeQ(C, x)), _patched_custom_constraint_call(lambda n: eager_IntegerQ(n)), _patched_custom_constraint_call(lambda B, A, C: ZeroQ(Add(A, B, C))))
    rule6 = _ReplacementRuleWrapped(pattern6, lambda n, e, x, v, b, A, B, c, a, f, d, u, C : Add(SimplifyAntiderivativeSum(v, x), Mul(A, Log(RemoveContent(Add(Mul(b, Pow(Cos(u), n)), Mul(a, Pow(Sin(u), n))), x))), Mul(B, Log(RemoveContent(Add(Mul(d, Pow(Cos(u), n)), Mul(c, Pow(Sin(u), n))), x))), Mul(C, Log(RemoveContent(Add(Mul(f, Pow(Cos(u), n)), Mul(e, Pow(Sin(u), n))), x)))))
    replacer.add(rule6)

    return replacer


def SimplifyAntiderivativeSum(expr, x):
    result = SimplifyAntiderivativeSum_replacer.replace(UtilityOperator(expr, x))
    if isinstance(result, Operation) and result.head == UtilityOp:
        return expr
    return matchpy_to_sympy(result)


def _SimplifyAntiderivative():
    replacer = ManyToOneReplacer()

    pattern2 = Pattern(UtilityOperator(Log(Mul(c_, u_)), x_), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)))
    rule2 = _ReplacementRuleWrapped(pattern2, lambda x, c, u : SimplifyAntiderivative(Log(u), x))
    replacer.add(rule2)

    pattern3 = Pattern(UtilityOperator(Log(Pow(u_, n_)), x_), _patched_custom_constraint_call(lambda n, x: eager_FreeQ(n, x)))
    rule3 = _ReplacementRuleWrapped(pattern3, lambda x, n, u : Mul(n, SimplifyAntiderivative(Log(u), x)))
    replacer.add(rule3)

    pattern7 = Pattern(UtilityOperator(Log(Pow(f_, u_)), x_), _patched_custom_constraint_call(lambda f, x: eager_FreeQ(f, x)))
    rule7 = _ReplacementRuleWrapped(pattern7, lambda x, f, u : Mul(Log(f), SimplifyAntiderivative(u, x)))
    replacer.add(rule7)

    pattern8 = Pattern(UtilityOperator(Log(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Tan(u_)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda b, a: ZeroQ(Add(Pow(a, S(2)), Pow(b, S(2))))))
    rule8 = _ReplacementRuleWrapped(pattern8, lambda x, b, u, a : Add(Mul(Mul(b, Pow(a, S(1))), SimplifyAntiderivative(u, x)), Mul(S(1), SimplifyAntiderivative(Log(Cos(u)), x))))
    replacer.add(rule8)

    pattern9 = Pattern(UtilityOperator(Log(Add(Mul(Cot(u_), WildSymbol('b', optional_value=S(1))), a_)), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda b, a: ZeroQ(Add(Pow(a, S(2)), Pow(b, S(2))))))
    rule9 = _ReplacementRuleWrapped(pattern9, lambda x, b, u, a : Add(Mul(Mul(Mul(S(1), b), Pow(a, S(1))), SimplifyAntiderivative(u, x)), Mul(S(1), SimplifyAntiderivative(Log(Sin(u)), x))))
    replacer.add(rule9)

    pattern10 = Pattern(UtilityOperator(ArcTan(Mul(WildSymbol('a', optional_value=S(1)), Tan(u_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule10 = _ReplacementRuleWrapped(pattern10, lambda x, u, a : RectifyTangent(u, a, S(1), x))
    replacer.add(rule10)

    pattern11 = Pattern(UtilityOperator(ArcCot(Mul(WildSymbol('a', optional_value=S(1)), Tan(u_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule11 = _ReplacementRuleWrapped(pattern11, lambda x, u, a : RectifyTangent(u, a, S(1), x))
    replacer.add(rule11)

    pattern12 = Pattern(UtilityOperator(ArcCot(Mul(WildSymbol('a', optional_value=S(1)), Tanh(u_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule12 = _ReplacementRuleWrapped(pattern12, lambda x, u, a : Mul(S(1), SimplifyAntiderivative(ArcTan(Mul(a, Tanh(u))), x)))
    replacer.add(rule12)

    pattern13 = Pattern(UtilityOperator(ArcTanh(Mul(WildSymbol('a', optional_value=S(1)), Tan(u_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule13 = _ReplacementRuleWrapped(pattern13, lambda x, u, a : RectifyTangent(u, Mul(I, a), Mul(S(1), I), x))
    replacer.add(rule13)

    pattern14 = Pattern(UtilityOperator(ArcCoth(Mul(WildSymbol('a', optional_value=S(1)), Tan(u_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule14 = _ReplacementRuleWrapped(pattern14, lambda x, u, a : RectifyTangent(u, Mul(I, a), Mul(S(1), I), x))
    replacer.add(rule14)

    pattern15 = Pattern(UtilityOperator(ArcTanh(Tanh(u_)), x_))
    rule15 = _ReplacementRuleWrapped(pattern15, lambda x, u : SimplifyAntiderivative(u, x))
    replacer.add(rule15)

    pattern16 = Pattern(UtilityOperator(ArcCoth(Tanh(u_)), x_))
    rule16 = _ReplacementRuleWrapped(pattern16, lambda x, u : SimplifyAntiderivative(u, x))
    replacer.add(rule16)

    pattern17 = Pattern(UtilityOperator(ArcCot(Mul(Cot(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule17 = _ReplacementRuleWrapped(pattern17, lambda x, u, a : RectifyCotangent(u, a, S(1), x))
    replacer.add(rule17)

    pattern18 = Pattern(UtilityOperator(ArcTan(Mul(Cot(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule18 = _ReplacementRuleWrapped(pattern18, lambda x, u, a : RectifyCotangent(u, a, S(1), x))
    replacer.add(rule18)

    pattern19 = Pattern(UtilityOperator(ArcTan(Mul(Coth(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule19 = _ReplacementRuleWrapped(pattern19, lambda x, u, a : Mul(S(1), SimplifyAntiderivative(ArcTan(Mul(Tanh(u), Pow(a, S(1)))), x)))
    replacer.add(rule19)

    pattern20 = Pattern(UtilityOperator(ArcCoth(Mul(Cot(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule20 = _ReplacementRuleWrapped(pattern20, lambda x, u, a : RectifyCotangent(u, Mul(I, a), I, x))
    replacer.add(rule20)

    pattern21 = Pattern(UtilityOperator(ArcTanh(Mul(Cot(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda a: eager_PositiveQ(Pow(a, S(2)))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule21 = _ReplacementRuleWrapped(pattern21, lambda x, u, a : RectifyCotangent(u, Mul(I, a), I, x))
    replacer.add(rule21)

    pattern22 = Pattern(UtilityOperator(ArcCoth(Coth(u_)), x_))
    rule22 = _ReplacementRuleWrapped(pattern22, lambda x, u : SimplifyAntiderivative(u, x))
    replacer.add(rule22)

    pattern23 = Pattern(UtilityOperator(ArcTanh(Mul(Coth(u_), WildSymbol('a', optional_value=S(1)))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule23 = _ReplacementRuleWrapped(pattern23, lambda x, u, a : SimplifyAntiderivative(ArcTanh(Mul(Tanh(u), Pow(a, S(1)))), x))
    replacer.add(rule23)

    pattern24 = Pattern(UtilityOperator(ArcTanh(Coth(u_)), x_))
    rule24 = _ReplacementRuleWrapped(pattern24, lambda x, u : SimplifyAntiderivative(u, x))
    replacer.add(rule24)

    pattern25 = Pattern(UtilityOperator(ArcTan(Mul(WildSymbol('c', optional_value=S(1)), Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Tan(u_))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda c, a: eager_PositiveQ(Mul(Pow(a, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda c, b: eager_PositiveQ(Mul(Pow(b, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule25 = _ReplacementRuleWrapped(pattern25, lambda x, a, b, u, c : RectifyTangent(u, Mul(a, c), Mul(b, c), S(1), x))
    replacer.add(rule25)

    pattern26 = Pattern(UtilityOperator(ArcTanh(Mul(WildSymbol('c', optional_value=S(1)), Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Tan(u_))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda c, a: eager_PositiveQ(Mul(Pow(a, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda c, b: eager_PositiveQ(Mul(Pow(b, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule26 = _ReplacementRuleWrapped(pattern26, lambda x, a, b, u, c : RectifyTangent(u, Mul(I, a, c), Mul(I, b, c), Mul(S(1), I), x))
    replacer.add(rule26)

    pattern27 = Pattern(UtilityOperator(ArcTan(Mul(WildSymbol('c', optional_value=S(1)), Add(Mul(Cot(u_), WildSymbol('b', optional_value=S(1))), a_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda c, a: eager_PositiveQ(Mul(Pow(a, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda c, b: eager_PositiveQ(Mul(Pow(b, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule27 = _ReplacementRuleWrapped(pattern27, lambda x, a, b, u, c : RectifyCotangent(u, Mul(a, c), Mul(b, c), S(1), x))
    replacer.add(rule27)

    pattern28 = Pattern(UtilityOperator(ArcTanh(Mul(WildSymbol('c', optional_value=S(1)), Add(Mul(Cot(u_), WildSymbol('b', optional_value=S(1))), a_))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda c, a: eager_PositiveQ(Mul(Pow(a, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda c, b: eager_PositiveQ(Mul(Pow(b, S(2)), Pow(c, S(2))))), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule28 = _ReplacementRuleWrapped(pattern28, lambda x, a, b, u, c : RectifyCotangent(u, Mul(I, a, c), Mul(I, b, c), Mul(S(1), I), x))
    replacer.add(rule28)

    pattern29 = Pattern(UtilityOperator(ArcTan(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('b', optional_value=S(1)), Tan(u_)), Mul(WildSymbol('c', optional_value=S(1)), Pow(Tan(u_), S(2))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule29 = _ReplacementRuleWrapped(pattern29, lambda x, a, b, u, c : eager_If(eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))), ArcTan(NormalizeTogether(Mul(Add(a, c, S(1), Mul(Add(a, Mul(S(1), c), S(1)), Cos(Mul(S(2), u))), Mul(b, Sin(Mul(S(2), u)))), Pow(Add(a, c, S(1), Mul(Add(a, Mul(S(1), c), S(1)), Cos(Mul(S(2), u))), Mul(b, Sin(Mul(S(2), u)))), S(1))))), ArcTan(NormalizeTogether(Mul(Add(c, Mul(Add(a, Mul(S(1), c), S(1)), Pow(Cos(u), S(2))), Mul(b, Cos(u), Sin(u))), Pow(Add(c, Mul(Add(a, Mul(S(1), c), S(1)), Pow(Cos(u), S(2))), Mul(b, Cos(u), Sin(u))), S(1)))))))
    replacer.add(rule29)

    pattern30 = Pattern(UtilityOperator(ArcTan(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('b', optional_value=S(1)), Add(WildSymbol('d', optional_value=S(0)), Mul(WildSymbol('e', optional_value=S(1)), Tan(u_)))), Mul(WildSymbol('c', optional_value=S(1)), Pow(Add(WildSymbol('f', optional_value=S(0)), Mul(WildSymbol('g', optional_value=S(1)), Tan(u_))), S(2))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda b, x: eager_FreeQ(b, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule30 = _ReplacementRuleWrapped(pattern30, lambda x, d, a, e, f, b, u, c, g : SimplifyAntiderivative(ArcTan(Add(a, Mul(b, d), Mul(c, Pow(f, S(2))), Mul(Add(Mul(b, e), Mul(S(2), c, f, g)), Tan(u)), Mul(c, Pow(g, S(2)), Pow(Tan(u), S(2))))), x))
    replacer.add(rule30)

    pattern31 = Pattern(UtilityOperator(ArcTan(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('c', optional_value=S(1)), Pow(Tan(u_), S(2))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule31 = _ReplacementRuleWrapped(pattern31, lambda x, c, u, a : eager_If(eager_EvenQ(eager_Denominator(NumericFactor(eager_Together(u)))), ArcTan(NormalizeTogether(Mul(Add(a, c, S(1), Mul(Add(a, Mul(S(1), c), S(1)), Cos(Mul(S(2), u)))), Pow(Add(a, c, S(1), Mul(Add(a, Mul(S(1), c), S(1)), Cos(Mul(S(2), u)))), S(1))))), ArcTan(NormalizeTogether(Mul(Add(c, Mul(Add(a, Mul(S(1), c), S(1)), Pow(Cos(u), S(2)))), Pow(Add(c, Mul(Add(a, Mul(S(1), c), S(1)), Pow(Cos(u), S(2)))), S(1)))))))
    replacer.add(rule31)

    pattern32 = Pattern(UtilityOperator(ArcTan(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('c', optional_value=S(1)), Pow(Add(WildSymbol('f', optional_value=S(0)), Mul(WildSymbol('g', optional_value=S(1)), Tan(u_))), S(2))))), x_), _patched_custom_constraint_call(lambda a, x: eager_FreeQ(a, x)), _patched_custom_constraint_call(lambda c, x: eager_FreeQ(c, x)), _patched_custom_constraint_call(lambda u: eager_ComplexFreeQ(u)))
    rule32 = _ReplacementRuleWrapped(pattern32, lambda x, a, f, u, c, g : SimplifyAntiderivative(ArcTan(Add(a, Mul(c, Pow(f, S(2))), Mul(Mul(S(2), c, f, g), Tan(u)), Mul(c, Pow(g, S(2)), Pow(Tan(u), S(2))))), x))
    replacer.add(rule32)

    return replacer


def SimplifyAntiderivative(expr, x):
    result = SimplifyAntiderivative_replacer.replace(UtilityOperator(expr, x))
    if isinstance(result, Operation) and result.head == UtilityOp:
        if eager_ProductQ(expr):
            u, c = S(1), S(1)
            for i in expr.args:
                if eager_FreeQ(i, x):
                    c *= i
                else:
                    u *= i
            if eager_FreeQ(c, x) and c != S(1):
                v = SimplifyAntiderivative(u, x)
                if eager_SumQ(v) and eager_NonsumQ(u):
                    return Add(*[c*i for i in v.args])
                return c*v
        elif eager_LogQ(expr):
            F = expr.args[0]
            if eager_MemberQ([cot, sec, csc, coth, sech, csch], eager_Head(F)):
                return -SimplifyAntiderivative(Log(1/F), x)
        if eager_MemberQ([Log, atan, acot], eager_Head(expr)):
            F = eager_Head(expr)
            G = expr.args[0]
            if eager_MemberQ([cot, sec, csc, coth, sech, csch], eager_Head(G)):
                return -SimplifyAntiderivative(F(1/G), x)
        if eager_MemberQ([atanh, acoth], eager_Head(expr)):
            F = eager_Head(expr)
            G = expr.args[0]
            if eager_MemberQ([cot, sec, csc, coth, sech, csch], eager_Head(G)):
                return SimplifyAntiderivative(F(1/G), x)
        u = expr
        if eager_FreeQ(u, x):
            return S(0)
        elif eager_LogQ(u):
            return Log(RemoveContent(u.args[0], x))
        elif eager_SumQ(u):
            return SimplifyAntiderivativeSum(Add(*[SimplifyAntiderivative(i, x) for i in u.args]), x)
        return u
    else:
        return matchpy_to_sympy(result)


def _TrigSimplifyAux():
    replacer = ManyToOneReplacer()

    pattern1 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(WildSymbol('a', optional_value=S(1)), Pow(v_, WildSymbol('m', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(v_, WildSymbol('n', optional_value=S(1))))), p_))), _patched_custom_constraint_call(lambda v: eager_InertTrigQ(v)), _patched_custom_constraint_call(lambda p: eager_IntegerQ(p)), _patched_custom_constraint_call(lambda n, m: eager_RationalQ(m, n)), _patched_custom_constraint_call(lambda n, m: Less(m, n)))
    rule1 = _ReplacementRuleWrapped(pattern1, lambda n, a, p, m, u, v, b : Mul(u, Pow(v, Mul(m, p)), Pow(TrigSimplifyAux(Add(a, Mul(b, Pow(v, Add(n, Mul(S(-1), m)))))), p)))
    replacer.add(rule1)

    pattern2 = Pattern(UtilityOperator(Add(Mul(Pow(cos(u_), S('2')), WildSymbol('a', optional_value=S(1))), WildSymbol('v', optional_value=S(0)), Mul(WildSymbol('b', optional_value=S(1)), Pow(sin(u_), S('2'))))), _patched_custom_constraint_call(lambda b, a: SameQ(a, b)))
    rule2 = _ReplacementRuleWrapped(pattern2, lambda u, v, b, a : Add(a, v))
    replacer.add(rule2)

    pattern3 = Pattern(UtilityOperator(Add(WildSymbol('v', optional_value=S(0)), Mul(WildSymbol('a', optional_value=S(1)), Pow(sec(u_), S('2'))), Mul(WildSymbol('b', optional_value=S(1)), Pow(tan(u_), S('2'))))), _patched_custom_constraint_call(lambda b, a: SameQ(a, Mul(S(-1), b))))
    rule3 = _ReplacementRuleWrapped(pattern3, lambda u, v, b, a : Add(a, v))
    replacer.add(rule3)

    pattern4 = Pattern(UtilityOperator(Add(Mul(Pow(csc(u_), S('2')), WildSymbol('a', optional_value=S(1))), Mul(Pow(cot(u_), S('2')), WildSymbol('b', optional_value=S(1))), WildSymbol('v', optional_value=S(0)))), _patched_custom_constraint_call(lambda b, a: SameQ(a, Mul(S(-1), b))))
    rule4 = _ReplacementRuleWrapped(pattern4, lambda u, v, b, a : Add(a, v))
    replacer.add(rule4)

    pattern5 = Pattern(UtilityOperator(Pow(Add(Mul(Pow(cos(u_), S('2')), WildSymbol('a', optional_value=S(1))), WildSymbol('v', optional_value=S(0)), Mul(WildSymbol('b', optional_value=S(1)), Pow(sin(u_), S('2')))), n_)))
    rule5 = _ReplacementRuleWrapped(pattern5, lambda n, a, u, v, b : Pow(Add(Mul(Add(b, Mul(S(-1), a)), Pow(Sin(u), S('2'))), a, v), n))
    replacer.add(rule5)

    pattern6 = Pattern(UtilityOperator(Add(WildSymbol('w', optional_value=S(0)), u_, Mul(WildSymbol('v', optional_value=S(1)), Pow(sin(z_), S('2'))))), _patched_custom_constraint_call(lambda u, v: SameQ(u, Mul(S(-1), v))))
    rule6 = _ReplacementRuleWrapped(pattern6, lambda u, w, z, v : Add(Mul(u, Pow(Cos(z), S('2'))), w))
    replacer.add(rule6)

    pattern7 = Pattern(UtilityOperator(Add(Mul(Pow(cos(z_), S('2')), WildSymbol('v', optional_value=S(1))), WildSymbol('w', optional_value=S(0)), u_)), _patched_custom_constraint_call(lambda u, v: SameQ(u, Mul(S(-1), v))))
    rule7 = _ReplacementRuleWrapped(pattern7, lambda z, w, v, u : Add(Mul(u, Pow(Sin(z), S('2'))), w))
    replacer.add(rule7)

    pattern8 = Pattern(UtilityOperator(Add(WildSymbol('w', optional_value=S(0)), u_, Mul(WildSymbol('v', optional_value=S(1)), Pow(tan(z_), S('2'))))), _patched_custom_constraint_call(lambda u, v: SameQ(u, v)))
    rule8 = _ReplacementRuleWrapped(pattern8, lambda u, w, z, v : Add(Mul(u, Pow(Sec(z), S('2'))), w))
    replacer.add(rule8)

    pattern9 = Pattern(UtilityOperator(Add(Mul(Pow(cot(z_), S('2')), WildSymbol('v', optional_value=S(1))), WildSymbol('w', optional_value=S(0)), u_)), _patched_custom_constraint_call(lambda u, v: SameQ(u, v)))
    rule9 = _ReplacementRuleWrapped(pattern9, lambda z, w, v, u : Add(Mul(u, Pow(Csc(z), S('2'))), w))
    replacer.add(rule9)

    pattern10 = Pattern(UtilityOperator(Add(WildSymbol('w', optional_value=S(0)), u_, Mul(WildSymbol('v', optional_value=S(1)), Pow(sec(z_), S('2'))))), _patched_custom_constraint_call(lambda u, v: SameQ(u, Mul(S(-1), v))))
    rule10 = _ReplacementRuleWrapped(pattern10, lambda u, w, z, v : Add(Mul(v, Pow(Tan(z), S('2'))), w))
    replacer.add(rule10)

    pattern11 = Pattern(UtilityOperator(Add(Mul(Pow(csc(z_), S('2')), WildSymbol('v', optional_value=S(1))), WildSymbol('w', optional_value=S(0)), u_)), _patched_custom_constraint_call(lambda u, v: SameQ(u, Mul(S(-1), v))))
    rule11 = _ReplacementRuleWrapped(pattern11, lambda z, w, v, u : Add(Mul(v, Pow(Cot(z), S('2'))), w))
    replacer.add(rule11)

    pattern12 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(cos(v_), WildSymbol('b', optional_value=S(1))), a_), S(-1)), Pow(sin(v_), S('2')))), _patched_custom_constraint_call(lambda b, a: ZeroQ(Add(Pow(a, S('2')), Mul(S(-1), Pow(b, S('2')))))))
    rule12 = _ReplacementRuleWrapped(pattern12, lambda u, v, b, a : Mul(u, Add(Mul(S(1), Pow(a, S(-1))), Mul(S(-1), Mul(Cos(v), Pow(b, S(-1)))))))
    replacer.add(rule12)

    pattern13 = Pattern(UtilityOperator(Mul(Pow(cos(v_), S('2')), WildSymbol('u', optional_value=S(1)), Pow(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), sin(v_))), S(-1)))), _patched_custom_constraint_call(lambda b, a: ZeroQ(Add(Pow(a, S('2')), Mul(S(-1), Pow(b, S('2')))))))
    rule13 = _ReplacementRuleWrapped(pattern13, lambda u, v, b, a : Mul(u, Add(Mul(S(1), Pow(a, S(-1))), Mul(S(-1), Mul(Sin(v), Pow(b, S(-1)))))))
    replacer.add(rule13)

    pattern14 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))), Pow(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), S(-1)))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule14 = _ReplacementRuleWrapped(pattern14, lambda n, a, u, v, b : Mul(u, Pow(Add(b, Mul(a, Pow(Cot(v), n))), S(-1))))
    replacer.add(rule14)

    pattern15 = Pattern(UtilityOperator(Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_), S(-1)))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule15 = _ReplacementRuleWrapped(pattern15, lambda n, a, u, v, b : Mul(u, Pow(Add(b, Mul(a, Pow(Tan(v), n))), S(-1))))
    replacer.add(rule15)

    pattern16 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1))), Pow(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1))))), S(-1)))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule16 = _ReplacementRuleWrapped(pattern16, lambda n, a, u, v, b : Mul(u, Pow(Add(b, Mul(a, Pow(Cos(v), n))), S(-1))))
    replacer.add(rule16)

    pattern17 = Pattern(UtilityOperator(Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_), S(-1)))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule17 = _ReplacementRuleWrapped(pattern17, lambda n, a, u, v, b : Mul(u, Pow(Add(b, Mul(a, Pow(Sin(v), n))), S(-1))))
    replacer.add(rule17)

    pattern18 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(a_, Mul(WildSymbol('b', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1))))), S(-1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule18 = _ReplacementRuleWrapped(pattern18, lambda n, a, u, v, b : Mul(u, Mul(Pow(Sin(v), n), Pow(Add(b, Mul(a, Pow(Cos(v), n))), S(-1)))))
    replacer.add(rule18)

    pattern19 = Pattern(UtilityOperator(Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), a_), S(-1)))), _patched_custom_constraint_call(lambda n: PositiveIntegerQ(n)), _patched_custom_constraint_call(lambda a: eager_NonsumQ(a)))
    rule19 = _ReplacementRuleWrapped(pattern19, lambda n, a, u, v, b : Mul(u, Mul(Pow(Cos(v), n), Pow(Add(b, Mul(a, Pow(Sin(v), n))), S(-1)))))
    replacer.add(rule19)

    pattern20 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(WildSymbol('a', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)))
    rule20 = _ReplacementRuleWrapped(pattern20, lambda n, a, p, u, v, b : Mul(u, Pow(Sec(v), Mul(n, p)), Pow(Add(a, Mul(b, Pow(Sin(v), n))), p)))
    replacer.add(rule20)

    pattern21 = Pattern(UtilityOperator(Mul(Pow(Add(Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('a', optional_value=S(1))), Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), WildSymbol('u', optional_value=S(1)))), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)))
    rule21 = _ReplacementRuleWrapped(pattern21, lambda n, a, p, u, v, b : Mul(u, Pow(Csc(v), Mul(n, p)), Pow(Add(a, Mul(b, Pow(Cos(v), n))), p)))
    replacer.add(rule21)

    pattern22 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(WildSymbol('b', optional_value=S(1)), Pow(sin(v_), WildSymbol('n', optional_value=S(1)))), Mul(WildSymbol('a', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)))
    rule22 = _ReplacementRuleWrapped(pattern22, lambda n, a, p, u, v, b : Mul(u, Pow(Tan(v), Mul(n, p)), Pow(Add(a, Mul(b, Pow(Cos(v), n))), p)))
    replacer.add(rule22)

    pattern23 = Pattern(UtilityOperator(Mul(Pow(Add(Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('a', optional_value=S(1))), Mul(Pow(cos(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), WildSymbol('u', optional_value=S(1)))), _patched_custom_constraint_call(lambda n, p: eager_IntegersQ(n, p)))
    rule23 = _ReplacementRuleWrapped(pattern23, lambda n, a, p, u, v, b : Mul(u, Pow(Cot(v), Mul(n, p)), Pow(Add(a, Mul(b, Pow(Sin(v), n))), p)))
    replacer.add(rule23)

    pattern24 = Pattern(UtilityOperator(Mul(Pow(cos(v_), WildSymbol('m', optional_value=S(1))), WildSymbol('u', optional_value=S(1)), Pow(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('c', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, p, m: eager_IntegersQ(m, n, p)))
    rule24 = _ReplacementRuleWrapped(pattern24, lambda n, a, c, p, m, u, v, b : Mul(u, Pow(Cos(v), Add(m, Mul(S(-1), Mul(n, p)))), Pow(Add(c, Mul(b, Pow(Sin(v), n)), Mul(a, Pow(Cos(v), n))), p)))
    replacer.add(rule24)

    pattern25 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(sec(v_), WildSymbol('m', optional_value=S(1))), Pow(Add(WildSymbol('a', optional_value=S(0)), Mul(WildSymbol('c', optional_value=S(1)), Pow(sec(v_), WildSymbol('n', optional_value=S(1)))), Mul(WildSymbol('b', optional_value=S(1)), Pow(tan(v_), WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, p, m: eager_IntegersQ(m, n, p)))
    rule25 = _ReplacementRuleWrapped(pattern25, lambda n, a, c, p, m, u, v, b : Mul(u, Pow(Sec(v), Add(m, Mul(n, p))), Pow(Add(c, Mul(b, Pow(Sin(v), n)), Mul(a, Pow(Cos(v), n))), p)))
    replacer.add(rule25)

    pattern26 = Pattern(UtilityOperator(Mul(Pow(Add(WildSymbol('a', optional_value=S(0)), Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('c', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), WildSymbol('u', optional_value=S(1)), Pow(sin(v_), WildSymbol('m', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, p, m: eager_IntegersQ(m, n, p)))
    rule26 = _ReplacementRuleWrapped(pattern26, lambda n, a, c, p, m, u, v, b : Mul(u, Pow(Sin(v), Add(m, Mul(S(-1), Mul(n, p)))), Pow(Add(c, Mul(b, Pow(Cos(v), n)), Mul(a, Pow(Sin(v), n))), p)))
    replacer.add(rule26)

    pattern27 = Pattern(UtilityOperator(Mul(Pow(csc(v_), WildSymbol('m', optional_value=S(1))), Pow(Add(WildSymbol('a', optional_value=S(0)), Mul(Pow(cot(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), Mul(Pow(csc(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('c', optional_value=S(1)))), WildSymbol('p', optional_value=S(1))), WildSymbol('u', optional_value=S(1)))), _patched_custom_constraint_call(lambda n, p, m: eager_IntegersQ(m, n, p)))
    rule27 = _ReplacementRuleWrapped(pattern27, lambda n, a, c, p, m, u, v, b : Mul(u, Pow(Csc(v), Add(m, Mul(n, p))), Pow(Add(c, Mul(b, Pow(Cos(v), n)), Mul(a, Pow(Sin(v), n))), p)))
    replacer.add(rule27)

    pattern28 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(Pow(csc(v_), WildSymbol('m', optional_value=S(1))), WildSymbol('a', optional_value=S(1))), Mul(WildSymbol('b', optional_value=S(1)), Pow(sin(v_), WildSymbol('n', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, m: eager_IntegersQ(m, n)))
    rule28 = _ReplacementRuleWrapped(pattern28, lambda n, a, p, m, u, v, b : eager_If(And(ZeroQ(Add(m, n, S(-2))), ZeroQ(Add(a, b))), Mul(u, Pow(Mul(a, Mul(Pow(Cos(v), S('2')), Pow(Pow(Sin(v), m), S(-1)))), p)), Mul(u, Pow(Mul(Add(a, Mul(b, Pow(Sin(v), Add(m, n)))), Pow(Pow(Sin(v), m), S(-1))), p))))
    replacer.add(rule28)

    pattern29 = Pattern(UtilityOperator(Mul(WildSymbol('u', optional_value=S(1)), Pow(Add(Mul(Pow(cos(v_), WildSymbol('n', optional_value=S(1))), WildSymbol('b', optional_value=S(1))), Mul(WildSymbol('a', optional_value=S(1)), Pow(sec(v_), WildSymbol('m', optional_value=S(1))))), WildSymbol('p', optional_value=S(1))))), _patched_custom_constraint_call(lambda n, m: eager_IntegersQ(m, n)))
    rule29 = _ReplacementRuleWrapped(pattern29, lambda n, a, p, m, u, v, b : eager_If(And(ZeroQ(Add(m, n, S(-2))), ZeroQ(Add(a, b))), Mul(u, Pow(Mul(a, Mul(Pow(Sin(v), S('2')), Pow(Pow(Cos(v), m), S(-1)))), p)), Mul(u, Pow(Mul(Add(a, Mul(b, Pow(Cos(v), Add(m, n)))), Pow(Pow(Cos(v), m), S(-1))), p))))
    replacer.add(rule29)

    pattern30 = Pattern(UtilityOperator(u_))
    rule30 = _ReplacementRuleWrapped(pattern30, lambda u : u)
    replacer.add(rule30)

    return replacer


def TrigSimplifyAux(expr):
    result = TrigSimplifyAux_replacer.replace(UtilityOperator(expr))
    if isinstance(result, Operation) and result.head == UtilityOp:
        return expr
    return matchpy_to_sympy(result)

def Cancel(expr):
    return cancel(expr)

# Util_Part and Part moved to sympy_wolfram.functions_eager (imported above): generic
# 1-based part extraction, no Rubi-specific logic.

def PolyLog(n, p, z=None):
    return polylog(n, p)

def eager_D(f, x):
    try:
        return f.diff(x)
    except ValueError:
        return Function('D')(f, x)

def eager_IntegralFreeQ(u):
    return eager_FreeQ(u, Integral)

def eager_Dist(u, v, x):
    #Dist(u,v) returns the sum of u times each term of v, provided v is free of Int
    w = eager_Simp(u*x**2, x)/x**2
    if u == 1:
        return v
    elif u == 0:
        return 0
    elif NumericFactor(u) < 0 and NumericFactor(-u) > 0:
        return -eager_Dist(-u, v, x)
    elif eager_SumQ(v):
        return Add(*[eager_Dist(u, i, x) for i in v.args])
    elif eager_IntegralFreeQ(v):
        return eager_Simp(u*v, x)
    elif w != u and eager_FreeQ(w, x) and w == eager_Simp(w, x) and w == eager_Simp(w*x**2, x)/x**2:
        return eager_Dist(w, v, x)
    else:
        return eager_Simp(u*v, x)


def eager_Star(u, v):
    # Rubi Star[u, v]: the product of u and v, with u distributed over the terms
    # of v (see IntegrationUtilityFunctions.m). Rubi co-opts Wolfram's otherwise
    # meaning-free \[Star] infix operator purely as a display-friendly product,
    # so the step-by-step output shows the natural "coefficient * integral"
    # structure. Semantically it is just multiplication with distribution.
    if isinstance(v, Add):
        return Add(*[eager_Star(u, term) for term in v.args])
    return u * v

def PureFunctionOfCothQ(u, v, x):
    # If u is a pure function of Coth[v], PureFunctionOfCothQ[u,v,x] returns True;
    if eager_AtomQ(u):
        return u != x
    elif CalculusQ(u):
        return False
    elif eager_HyperbolicQ(u) and ZeroQ(u.args[0] - v):
        return CothQ(u)
    return all(PureFunctionOfCothQ(i, v, x) for i in u.args)

def SinIntegral(z):
    return Si(z)

def CosIntegral(z):
    return Ci(z)

def SinhIntegral(z):
    return Shi(z)

def CoshIntegral(z):
    return Chi(z)

def LogGamma(z):
    return loggamma(z)

def HypergeometricPFQ(a, b, c):
    return hyper(a, b, c)

def Sum_doit(exp, args):
    """
    This function perform summation using SymPy's `Sum`.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import Sum_doit
    >>> from sympy.abc import x
    >>> Sum_doit(2*x + 2, [x, 0, 1.7])
    6

    """
    if not isinstance(args[2], (int, Integer)):
        new_args = [args[0], args[1], eager_Floor(args[2])]
        return Sum(exp, new_args).doit()

    return Sum(exp, args).doit()

# PolynomialQuotient / PolynomialRemainder are standard Wolfram functions (they handle
# the rational-p Laurent case Rubi needs); the single implementation lives in
# sympy_wolfram.functions_eager and is imported at the top of this module.


def eager_Floor(x, a = None):
    if a is None:
        return floor(x)
    return a*floor(x/a)

def Factor(var):
    return factor(var)

def eager_Rule(a, b):
    return {a: b}

def Distribute(expr, *args):
    if len(args) == 1:
        if isinstance(expr, args[0]):
            return expr
        else:
            return expr.expand()
    if len(args) == 2:
        if isinstance(expr, args[1]):
            return expr.expand()
        else:
            return expr
    return expr.expand()

def CoprimeQ(*args):
    args = S(args)
    g = gcd(*args)
    if g == 1:
        return True
    return False

def eager_Quotient(m, n):
    return eager_Floor(m/n)

def process_trig(expr):
    """
    This function processes trigonometric expressions such that all `cot` is
    rewritten in terms of `tan`, `sec` in terms of `cos`, `csc` in terms of `sin` and
    similarly for `coth`, `sech` and `csch`.

    Examples
    ========

    >>> from rubi_rules.utils.utility_functions import process_trig
    >>> from sympy.abc import x
    >>> from sympy import coth, cot, csc
    >>> process_trig(x*cot(x))
    x/tan(x)
    >>> process_trig(coth(x)*csc(x))
    1/(sin(x)*tanh(x))

    """
    expr = expr.replace(lambda x: isinstance(x, cot), lambda x: 1/tan(x.args[0]))
    expr = expr.replace(lambda x: isinstance(x, sec), lambda x: 1/cos(x.args[0]))
    expr = expr.replace(lambda x: isinstance(x, csc), lambda x: 1/sin(x.args[0]))
    expr = expr.replace(lambda x: isinstance(x, coth), lambda x: 1/tanh(x.args[0]))
    expr = expr.replace(lambda x: isinstance(x, sech), lambda x: 1/cosh(x.args[0]))
    expr = expr.replace(lambda x: isinstance(x, csch), lambda x: 1/sinh(x.args[0]))
    return expr

def _ExpandIntegrand():
    Plus = Add
    Times = Mul
    def cons_f1(m):
        return PositiveIntegerQ(m)

    cons1 = _patched_custom_constraint_call(cons_f1)
    def cons_f2(d, c, b, a):
        return ZeroQ(-a*d + b*c)

    cons2 = _patched_custom_constraint_call(cons_f2)
    def cons_f3(a, x):
        return eager_FreeQ(a, x)

    cons3 = _patched_custom_constraint_call(cons_f3)
    def cons_f4(b, x):
        return eager_FreeQ(b, x)

    cons4 = _patched_custom_constraint_call(cons_f4)
    def cons_f5(c, x):
        return eager_FreeQ(c, x)

    cons5 = _patched_custom_constraint_call(cons_f5)
    def cons_f6(d, x):
        return eager_FreeQ(d, x)

    cons6 = _patched_custom_constraint_call(cons_f6)
    def cons_f7(e, x):
        return eager_FreeQ(e, x)

    cons7 = _patched_custom_constraint_call(cons_f7)
    def cons_f8(f, x):
        return eager_FreeQ(f, x)

    cons8 = _patched_custom_constraint_call(cons_f8)
    def cons_f9(g, x):
        return eager_FreeQ(g, x)

    cons9 = _patched_custom_constraint_call(cons_f9)
    def cons_f10(h, x):
        return eager_FreeQ(h, x)

    cons10 = _patched_custom_constraint_call(cons_f10)
    def cons_f11(e, b, c, f, n, p, F, x, d, m):
        if not isinstance(x, Symbol):
            return False
        return eager_FreeQ(eager_List(F, b, c, d, e, f, m, n, p), x)

    cons11 = _patched_custom_constraint_call(cons_f11)
    def cons_f12(F, x):
        return eager_FreeQ(F, x)

    cons12 = _patched_custom_constraint_call(cons_f12)
    def cons_f13(m, x):
        return eager_FreeQ(m, x)

    cons13 = _patched_custom_constraint_call(cons_f13)
    def cons_f14(n, x):
        return eager_FreeQ(n, x)

    cons14 = _patched_custom_constraint_call(cons_f14)
    def cons_f15(p, x):
        return eager_FreeQ(p, x)

    cons15 = _patched_custom_constraint_call(cons_f15)
    def cons_f16(e, b, c, f, n, a, p, F, x, d, m):
        if not isinstance(x, Symbol):
            return False
        return eager_FreeQ(eager_List(F, a, b, c, d, e, f, m, n, p), x)

    cons16 = _patched_custom_constraint_call(cons_f16)
    def cons_f17(n, m):
        return eager_IntegersQ(m, n)

    cons17 = _patched_custom_constraint_call(cons_f17)
    def cons_f18(n):
        return Less(n, S(0))

    cons18 = _patched_custom_constraint_call(cons_f18)
    def cons_f19(x, u):
        if not isinstance(x, Symbol):
            return False
        return eager_PolynomialQ(u, x)

    cons19 = _patched_custom_constraint_call(cons_f19)
    def cons_f20(G, F, u):
        return SameQ(F(u)*G(u), S(1))

    cons20 = _patched_custom_constraint_call(cons_f20)
    def cons_f21(q, x):
        return eager_FreeQ(q, x)

    cons21 = _patched_custom_constraint_call(cons_f21)
    def cons_f22(F):
        return eager_MemberQ(eager_List(ArcSin, ArcCos, ArcSinh, ArcCosh), F)

    cons22 = _patched_custom_constraint_call(cons_f22)
    def cons_f23(j, n):
        return ZeroQ(j - S(2)*n)

    cons23 = _patched_custom_constraint_call(cons_f23)
    def cons_f24(A, x):
        return eager_FreeQ(A, x)

    cons24 = _patched_custom_constraint_call(cons_f24)
    def cons_f25(B, x):
        return eager_FreeQ(B, x)

    cons25 = _patched_custom_constraint_call(cons_f25)
    def cons_f26(m, u, x):
        if not isinstance(x, Symbol):
            return False
        def _cons_f_u(d, w, c, p, x):
            return And(eager_FreeQ(eager_List(c, d), x), eager_IntegerQ(p), Greater(p, m))
        cons_u = _patched_custom_constraint_call(_cons_f_u)
        pat = Pattern(UtilityOperator((c_ + x_*WildSymbol('d', optional_value=S(1)))**p_*WildSymbol('w', optional_value=S(1)), x_), cons_u)
        result_matchq = is_match(UtilityOperator(u, x), pat)
        return eager_Not(And(PositiveIntegerQ(m), result_matchq))

    cons26 = _patched_custom_constraint_call(cons_f26)
    def cons_f27(b, v, n, a, x, u, m):
        if not isinstance(x, Symbol):
            return False
        return And(eager_FreeQ(eager_List(a, b, m), x), NegativeIntegerQ(n), eager_Not(eager_IntegerQ(m)), eager_PolynomialQ(u, x), eager_PolynomialQ(v, x),\
            eager_RationalQ(m), Less(m, -1), GreaterEqual(eager_Exponent(u, x), (-n - IntegerPart(m))*eager_Exponent(v, x)))
    cons27 = _patched_custom_constraint_call(cons_f27)
    def cons_f28(v, n, x, u, m):
        if not isinstance(x, Symbol):
            return False
        return And(eager_FreeQ(eager_List(a, b, m), x), NegativeIntegerQ(n), eager_Not(eager_IntegerQ(m)), eager_PolynomialQ(u, x),\
            eager_PolynomialQ(v, x), GreaterEqual(eager_Exponent(u, x), -n*eager_Exponent(v, x)))
    cons28 = _patched_custom_constraint_call(cons_f28)
    def cons_f29(n):
        return PositiveIntegerQ(n/S(4))

    cons29 = _patched_custom_constraint_call(cons_f29)
    def cons_f30(n):
        return eager_IntegerQ(n)

    cons30 = _patched_custom_constraint_call(cons_f30)
    def cons_f31(n):
        return Greater(n, S(1))

    cons31 = _patched_custom_constraint_call(cons_f31)
    def cons_f32(n, m):
        return Less(S(0), m, n)

    cons32 = _patched_custom_constraint_call(cons_f32)
    def cons_f33(n, m):
        return eager_OddQ(n/eager_GCD(m, n))

    cons33 = _patched_custom_constraint_call(cons_f33)
    def cons_f34(a, b):
        return eager_PosQ(a/b)

    cons34 = _patched_custom_constraint_call(cons_f34)
    def cons_f35(n, m, p):
        return eager_IntegersQ(m, n, p)

    cons35 = _patched_custom_constraint_call(cons_f35)
    def cons_f36(n, m, p):
        return Less(S(0), m, p, n)

    cons36 = _patched_custom_constraint_call(cons_f36)
    def cons_f37(q, n, m, p):
        return eager_IntegersQ(m, n, p, q)

    cons37 = _patched_custom_constraint_call(cons_f37)
    def cons_f38(n, q, m, p):
        return Less(S(0), m, p, q, n)

    cons38 = _patched_custom_constraint_call(cons_f38)
    def cons_f39(n):
        return eager_IntegerQ(n/S(2))

    cons39 = _patched_custom_constraint_call(cons_f39)
    def cons_f40(p):
        return NegativeIntegerQ(p)

    cons40 = _patched_custom_constraint_call(cons_f40)
    def cons_f41(n, m):
        return eager_IntegersQ(m, n/S(2))

    cons41 = _patched_custom_constraint_call(cons_f41)
    def cons_f42(n, m):
        return Unequal(m, n/S(2))

    cons42 = _patched_custom_constraint_call(cons_f42)
    def cons_f43(c, b, a):
        return NonzeroQ(-S(4)*a*c + b**S(2))

    cons43 = _patched_custom_constraint_call(cons_f43)
    def cons_f44(j, n, m):
        return eager_IntegersQ(m, n, j)

    cons44 = _patched_custom_constraint_call(cons_f44)
    def cons_f45(n, m):
        return Less(S(0), m, S(2)*n)

    cons45 = _patched_custom_constraint_call(cons_f45)
    def cons_f46(n, m, p):
        return eager_Not(And(Equal(m, n), Equal(p, S(-1))))

    cons46 = _patched_custom_constraint_call(cons_f46)
    def cons_f47(v, x):
        if not isinstance(x, Symbol):
            return False
        return eager_PolynomialQ(v, x)

    cons47 = _patched_custom_constraint_call(cons_f47)
    def cons_f48(v, x):
        if not isinstance(x, Symbol):
            return False
        return eager_BinomialQ(v, x)

    cons48 = _patched_custom_constraint_call(cons_f48)
    def cons_f49(v, x, u):
        if not isinstance(x, Symbol):
            return False
        return Inequality(eager_Exponent(u, x), Equal, eager_Exponent(v, x) + S(-1), GreaterEqual, S(2))

    cons49 = _patched_custom_constraint_call(cons_f49)
    def cons_f50(v, x, u):
        if not isinstance(x, Symbol):
            return False
        return GreaterEqual(eager_Exponent(u, x), eager_Exponent(v, x))

    cons50 = _patched_custom_constraint_call(cons_f50)
    def cons_f51(p):
        return eager_Not(eager_IntegerQ(p))

    cons51 = _patched_custom_constraint_call(cons_f51)

    def With2(e, b, c, f, n, a, g, h, x, d, m):
        tmp = a*h - b*g
        k = Symbol('k')
        return f**(e*(c + d*x)**n)*SimplifyTerm(h**(-m)*tmp**m, x)/(g + h*x) + Sum_doit(f**(e*(c + d*x)**n)*(a + b*x)**(-k + m)*SimplifyTerm(b*h**(-k)*tmp**(k - 1), x), eager_List(k, 1, m))
    pattern2 = Pattern(UtilityOperator(f_**((x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))**WildSymbol('n', optional_value=S(1))*WildSymbol('e', optional_value=S(1)))*(x_*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**WildSymbol('m', optional_value=S(1))/(x_*WildSymbol('h', optional_value=S(1)) + WildSymbol('g', optional_value=S(0))), x_), cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons10, cons1, cons2)
    rule2 = _ReplacementRuleWrapped(pattern2, With2)
    pattern3 = Pattern(UtilityOperator(F_**((x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)))*x_**WildSymbol('m', optional_value=S(1))*(e_ + x_*WildSymbol('f', optional_value=S(1)))**WildSymbol('p', optional_value=S(1)), x_), cons12, cons4, cons5, cons6, cons7, cons8, cons13, cons14, cons15, cons11)
    def replacement3(e, b, c, f, n, p, F, x, d, m):
        return eager_If(And(PositiveIntegerQ(m, p), LessEqual(m, p), Or(eager_EqQ(n, S(1)), ZeroQ(-c*f + d*e))), eager_ExpandLinearProduct(F**(b*(c + d*x)**n)*(e + f*x)**p, x**m, e, f, x), eager_If(PositiveIntegerQ(p), Distribute(F**(b*(c + d*x)**n)*x**m*(e + f*x)**p, Plus, Times), eager_ExpandIntegrand(F**(b*(c + d*x)**n), x**m*(e + f*x)**p, x)))
    rule3 = _ReplacementRuleWrapped(pattern3, replacement3)
    pattern4 = Pattern(UtilityOperator(F_**((x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))*x_**WildSymbol('m', optional_value=S(1))*(e_ + x_*WildSymbol('f', optional_value=S(1)))**WildSymbol('p', optional_value=S(1)), x_), cons12, cons3, cons4, cons5, cons6, cons7, cons8, cons13, cons14, cons15, cons16)
    def replacement4(e, b, c, f, n, a, p, F, x, d, m):
        return eager_If(And(PositiveIntegerQ(m, p), LessEqual(m, p), Or(eager_EqQ(n, S(1)), ZeroQ(-c*f + d*e))), eager_ExpandLinearProduct(F**(a + b*(c + d*x)**n)*(e + f*x)**p, x**m, e, f, x), eager_If(PositiveIntegerQ(p), Distribute(F**(a + b*(c + d*x)**n)*x**m*(e + f*x)**p, Plus, Times), eager_ExpandIntegrand(F**(a + b*(c + d*x)**n), x**m*(e + f*x)**p, x)))
    rule4 = _ReplacementRuleWrapped(pattern4, replacement4)
    def With5(b, v, c, n, a, F, u, x, d, m):
        if not isinstance(x, Symbol) or not (eager_FreeQ([F, a, b, c, d], x) and eager_IntegersQ(m, n) and n < 0):
            return False
        w = eager_ExpandIntegrand((a + b*x)**m*(c + d*x)**n, x)
        w = eager_ReplaceAll(w, eager_Rule(x, F**v))
        if eager_SumQ(w):
            return True
        return False
    pattern5 = Pattern(UtilityOperator((F_**v_*WildSymbol('b', optional_value=S(1)) + a_)**WildSymbol('m', optional_value=S(1))*(F_**v_*WildSymbol('d', optional_value=S(1)) + c_)**n_*WildSymbol('u', optional_value=S(1)), x_), cons12, cons3, cons4, cons5, cons6, cons17, cons18, _patched_custom_constraint_call(With5))
    def replacement5(b, v, c, n, a, F, u, x, d, m):
        w = eager_ReplaceAll(eager_ExpandIntegrand((a + b*x)**m*(c + d*x)**n, x), eager_Rule(x, F**v))
        return w.func(*[u*i for i in w.args])
    rule5 = _ReplacementRuleWrapped(pattern5, replacement5)
    def With6(e, b, c, f, n, a, x, u, d, m):
        if not isinstance(x, Symbol) or not (eager_FreeQ([a, b, c, d, e, f, m, n], x) and eager_PolynomialQ(u,x)):
            return False
        v = eager_ExpandIntegrand(u*(a + b*x)**m, x)
        if eager_SumQ(v):
            return True
        return False
    pattern6 = Pattern(UtilityOperator(f_**((x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))**WildSymbol('n', optional_value=S(1))*WildSymbol('e', optional_value=S(1)))*u_*(x_*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**WildSymbol('m', optional_value=S(1)), x_), cons3, cons4, cons5, cons6, cons7, cons8, cons13, cons14, cons19, _patched_custom_constraint_call(With6))
    def replacement6(e, b, c, f, n, a, x, u, d, m):
        v = eager_ExpandIntegrand(u*(a + b*x)**m, x)
        return Distribute(f**(e*(c + d*x)**n)*v, Plus, Times)
    rule6 = _ReplacementRuleWrapped(pattern6, replacement6)
    pattern7 = Pattern(UtilityOperator(u_*(x_*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**WildSymbol('m', optional_value=S(1))*Log((x_**WildSymbol('n', optional_value=S(1))*WildSymbol('e', optional_value=S(1)) + WildSymbol('d', optional_value=S(0)))**WildSymbol('p', optional_value=S(1))*WildSymbol('c', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons7, cons13, cons14, cons15, cons19)
    def replacement7(e, b, c, n, a, p, x, u, d, m):
        return eager_ExpandIntegrand(Log(c*(d + e*x**n)**p), u*(a + b*x)**m, x)
    rule7 = _ReplacementRuleWrapped(pattern7, replacement7)
    pattern8 = Pattern(UtilityOperator(f_**((x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))**WildSymbol('n', optional_value=S(1))*WildSymbol('e', optional_value=S(1)))*u_, x_), cons5, cons6, cons7, cons8, cons14, cons19)
    def replacement8(e, c, f, n, x, u, d):
        return eager_If(eager_EqQ(n, S(1)), eager_ExpandIntegrand(f**(e*(c + d*x)**n), u, x), eager_ExpandLinearProduct(f**(e*(c + d*x)**n), u, c, d, x))
    rule8 = _ReplacementRuleWrapped(pattern8, replacement8)
    # pattern9 = Pattern(UtilityOperator(F_**u_*(G_*u_*WildSymbol('b', optional_value=S(1)) + a_)**WildSymbol('n', optional_value=S(1)), x_), cons3, cons4, cons17, cons20)
    # def replacement9(b, G, n, a, F, u, x, m):
    #     return ReplaceAll(ExpandIntegrand(x**(-m)*(a + b*x)**n, x), Rule(x, G(u)))
    # rule9 = _ReplacementRuleWrapped(pattern9, replacement9)
    pattern10 = Pattern(UtilityOperator(u_*(WildSymbol('a', optional_value=S(0)) + WildSymbol('b', optional_value=S(1))*Log(((x_*WildSymbol('f', optional_value=S(1)) + WildSymbol('e', optional_value=S(0)))**WildSymbol('p', optional_value=S(1))*WildSymbol('d', optional_value=S(1)))**WildSymbol('q', optional_value=S(1))*WildSymbol('c', optional_value=S(1))))**n_, x_), cons3, cons4, cons5, cons6, cons7, cons8, cons14, cons15, cons21, cons19)
    def replacement10(e, b, c, f, n, a, p, x, u, d, q):
        return eager_ExpandLinearProduct((a + b*Log(c*(d*(e + f*x)**p)**q))**n, u, e, f, x)
    rule10 = _ReplacementRuleWrapped(pattern10, replacement10)
    # pattern11 = Pattern(UtilityOperator(u_*(F_*(x_*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**n_, x_), cons3, cons4, cons5, cons6, cons14, cons19, cons22)
    # def replacement11(b, c, n, a, F, u, x, d):
    #     return ExpandLinearProduct((a + b*F(c + d*x))**n, u, c, d, x)
    # rule11 = _ReplacementRuleWrapped(pattern11, replacement11)
    pattern12 = Pattern(UtilityOperator(WildSymbol('u', optional_value=S(1))/(x_**n_*WildSymbol('a', optional_value=S(1)) + sqrt(c_ + x_**j_*WildSymbol('d', optional_value=S(1)))*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons14, cons23)
    def replacement12(b, c, n, a, x, u, d, j):
        return eager_ExpandIntegrand(u*(a*x**n - b*sqrt(c + d*x**(S(2)*n)))/(-b**S(2)*c + x**(S(2)*n)*(a**S(2) - b**S(2)*d)), x)
    rule12 = _ReplacementRuleWrapped(pattern12, replacement12)
    pattern13 = Pattern(UtilityOperator((a_ + x_*WildSymbol('b', optional_value=S(1)))**m_/(c_ + x_*WildSymbol('d', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons1)
    def replacement13(b, c, a, x, d, m):
        if eager_RationalQ(a, b, c, d):
            return eager_ExpandExpression((a + b*x)**m/(c + d*x), x)
        else:
            tmp = a*d - b*c
            k = Symbol("k")
            return Sum_doit((a + b*x)**(-k + m)*SimplifyTerm(b*d**(-k)*tmp**(k + S(-1)), x), eager_List(k, S(1), m)) + SimplifyTerm(d**(-m)*tmp**m, x)/(c + d*x)

    rule13 = _ReplacementRuleWrapped(pattern13, replacement13)
    pattern14 = Pattern(UtilityOperator((A_ + x_*WildSymbol('B', optional_value=S(1)))*(a_ + x_*WildSymbol('b', optional_value=S(1)))**WildSymbol('m', optional_value=S(1))/(c_ + x_*WildSymbol('d', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons24, cons25, cons1)
    def replacement14(b, B, A, c, a, x, d, m):
        if eager_RationalQ(a, b, c, d, A, B):
            return eager_ExpandExpression((A + B*x)*(a + b*x)**m/(c + d*x), x)
        else:
            tmp1 = (A*d - B*c)/d
            tmp2 = eager_ExpandIntegrand((a + b*x)**m/(c + d*x), x)
            tmp2 = eager_If(eager_SumQ(tmp2), tmp2.func(*[SimplifyTerm(tmp1*i, x) for i in tmp2.args]), SimplifyTerm(tmp1*tmp2, x))
            return SimplifyTerm(B/d, x)*(a + b*x)**m + tmp2
    rule14 = _ReplacementRuleWrapped(pattern14, replacement14)

    def With15(b, a, x, u, m):
        tmp1 = eager_ExpandLinearProduct((a + b*x)**m, u, a, b, x)
        if not eager_IntegerQ(m):
            return tmp1
        else:
            tmp2 = eager_ExpandExpression(u*(a + b*x)**m, x)
            if eager_SumQ(tmp2) and LessEqual(eager_LeafCount(tmp2), eager_LeafCount(tmp1) + S(2)):
                return tmp2
            else:
                return tmp1
    pattern15 = Pattern(UtilityOperator(u_*(a_ + x_*WildSymbol('b', optional_value=S(1)))**m_, x_), cons3, cons4, cons13, cons19, cons26)
    rule15 = _ReplacementRuleWrapped(pattern15, With15)
    pattern16 = Pattern(UtilityOperator(u_*v_**n_*(a_ + x_*WildSymbol('b', optional_value=S(1)))**m_, x_), cons27)
    def replacement16(b, v, n, a, x, u, m):
        s = PolynomialQuotientRemainder(u, v**(-n)*(a+b*x)**(-IntegerPart(m)), x)
        return eager_ExpandIntegrand((a + b*x)**FractionalPart(m)*s[0], x) + eager_ExpandIntegrand(v**n*(a + b*x)**m*s[1], x)
    rule16 = _ReplacementRuleWrapped(pattern16, replacement16)

    pattern17 = Pattern(UtilityOperator(u_*v_**n_*(a_ + x_*WildSymbol('b', optional_value=S(1)))**m_, x_), cons28)
    def replacement17(b, v, n, a, x, u, m):
        s = PolynomialQuotientRemainder(u, v**(-n),x)
        return eager_ExpandIntegrand((a + b*x)**(m)*s[0], x) + eager_ExpandIntegrand(v**n*(a + b*x)**m*s[1], x)
    rule17 = _ReplacementRuleWrapped(pattern17, replacement17)

    def With18(b, n, a, x, u):
        r = eager_Numerator(eager_Rt(-a/b, S(2)))
        s = eager_Denominator(eager_Rt(-a/b, S(2)))
        return r/(S(2)*a*(r + s*u**(n/S(2)))) + r/(S(2)*a*(r - s*u**(n/S(2))))
    pattern18 = Pattern(UtilityOperator(S(1)/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons29)
    rule18 = _ReplacementRuleWrapped(pattern18, With18)
    def With19(b, n, a, x, u):
        k = Symbol("k")
        r = eager_Numerator(eager_Rt(-a/b, n))
        s = eager_Denominator(eager_Rt(-a/b, n))
        return Sum_doit(r/(a*n*(-(-1)**(2*k/n)*s*u + r)), eager_List(k, 1, n))
    pattern19 = Pattern(UtilityOperator(S(1)/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons30, cons31)
    rule19 = _ReplacementRuleWrapped(pattern19, With19)
    def With20(b, n, a, x, u, m):
        k = Symbol("k")
        g = eager_GCD(m, n)
        r = eager_Numerator(eager_Rt(a/b, n/eager_GCD(m, n)))
        s = eager_Denominator(eager_Rt(a/b, n/eager_GCD(m, n)))
        return eager_If(CoprimeQ(g + m, n), Sum_doit((-1)**(-2*k*m/n)*r*(-r/s)**(m/g)/(a*n*((-1)**(2*g*k/n)*s*u**g + r)), eager_List(k, 1, n/g)), Sum_doit((-1)**(2*k*(g + m)/n)*r*(-r/s)**(m/g)/(a*n*((-1)**(2*g*k/n)*r + s*u**g)), eager_List(k, 1, n/g)))
    pattern20 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons17, cons32, cons33, cons34)
    rule20 = _ReplacementRuleWrapped(pattern20, With20)
    def With21(b, n, a, x, u, m):
        k = Symbol("k")
        g = eager_GCD(m, n)
        r = eager_Numerator(eager_Rt(-a/b, n/eager_GCD(m, n)))
        s = eager_Denominator(eager_Rt(-a/b, n/eager_GCD(m, n)))
        return eager_If(Equal(n/g, S(2)), s/(S(2)*b*(r + s*u**g)) - s/(S(2)*b*(r - s*u**g)), eager_If(CoprimeQ(g + m, n), Sum_doit((S(-1))**(-S(2)*k*m/n)*r*(r/s)**(m/g)/(a*n*(-(S(-1))**(S(2)*g*k/n)*s*u**g + r)), eager_List(k, S(1), n/g)), Sum_doit((S(-1))**(S(2)*k*(g + m)/n)*r*(r/s)**(m/g)/(a*n*((S(-1))**(S(2)*g*k/n)*r - s*u**g)), eager_List(k, S(1), n/g))))
    pattern21 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons17, cons32)
    rule21 = _ReplacementRuleWrapped(pattern21, With21)
    def With22(b, c, n, a, x, u, d, m):
        k = Symbol("k")
        r = eager_Numerator(eager_Rt(-a/b, n))
        s = eager_Denominator(eager_Rt(-a/b, n))
        return Sum_doit((c*r + (-1)**(-2*k*m/n)*d*r*(r/s)**m)/(a*n*(-(-1)**(2*k/n)*s*u + r)), eager_List(k, 1, n))
    pattern22 = Pattern(UtilityOperator((c_ + u_**WildSymbol('m', optional_value=S(1))*WildSymbol('d', optional_value=S(1)))/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons17, cons32)
    rule22 = _ReplacementRuleWrapped(pattern22, With22)
    def With23(e, b, c, n, a, p, x, u, d, m):
        k = Symbol("k")
        r = eager_Numerator(eager_Rt(-a/b, n))
        s = eager_Denominator(eager_Rt(-a/b, n))
        return Sum_doit((c*r + (-1)**(-2*k*p/n)*e*r*(r/s)**p + (-1)**(-2*k*m/n)*d*r*(r/s)**m)/(a*n*(-(-1)**(2*k/n)*s*u + r)), eager_List(k, 1, n))
    pattern23 = Pattern(UtilityOperator((u_**p_*WildSymbol('e', optional_value=S(1)) + u_**WildSymbol('m', optional_value=S(1))*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons7, cons35, cons36)
    rule23 = _ReplacementRuleWrapped(pattern23, With23)
    def With24(e, b, c, f, n, a, p, x, u, d, q, m):
        k = Symbol("k")
        r = eager_Numerator(eager_Rt(-a/b, n))
        s = eager_Denominator(eager_Rt(-a/b, n))
        return Sum_doit((c*r + (-1)**(-2*k*q/n)*f*r*(r/s)**q + (-1)**(-2*k*p/n)*e*r*(r/s)**p + (-1)**(-2*k*m/n)*d*r*(r/s)**m)/(a*n*(-(-1)**(2*k/n)*s*u + r)), eager_List(k, 1, n))
    pattern24 = Pattern(UtilityOperator((u_**p_*WildSymbol('e', optional_value=S(1)) + u_**q_*WildSymbol('f', optional_value=S(1)) + u_**WildSymbol('m', optional_value=S(1))*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))/(a_ + u_**n_*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons7, cons8, cons37, cons38)
    rule24 = _ReplacementRuleWrapped(pattern24, With24)
    def With25(c, n, a, p, x, u):
        q = Symbol('q')
        return eager_ReplaceAll(eager_ExpandIntegrand(c**(-p), (c*x - q)**p*(c*x + q)**p, x), eager_List(eager_Rule(q, eager_Rt(-a*c, S(2))), eager_Rule(x, u**(n/S(2)))))
    pattern25 = Pattern(UtilityOperator((a_ + u_**WildSymbol('n', optional_value=S(1))*WildSymbol('c', optional_value=S(1)))**p_, x_), cons3, cons5, cons39, cons40)
    rule25 = _ReplacementRuleWrapped(pattern25, With25)
    def With26(c, n, a, p, x, u, m):
        q = Symbol('q')
        return eager_ReplaceAll(eager_ExpandIntegrand(c**(-p), x**m*(c*x**(n/S(2)) - q)**p*(c*x**(n/S(2)) + q)**p, x), eager_List(eager_Rule(q, eager_Rt(-a*c, S(2))), eager_Rule(x, u)))
    pattern26 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*(u_**WildSymbol('n', optional_value=S(1))*WildSymbol('c', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**p_, x_), cons3, cons5, cons41, cons40, cons32, cons42)
    rule26 = _ReplacementRuleWrapped(pattern26, With26)
    def With27(b, c, n, a, p, x, u, j):
        q = Symbol('q')
        return eager_ReplaceAll(eager_ExpandIntegrand(S(4)**(-p)*c**(-p), (b + S(2)*c*x - q)**p*(b + S(2)*c*x + q)**p, x), eager_List(eager_Rule(q, eager_Rt(-S(4)*a*c + b**S(2), S(2))), eager_Rule(x, u**n)))
    pattern27 = Pattern(UtilityOperator((u_**WildSymbol('j', optional_value=S(1))*WildSymbol('c', optional_value=S(1)) + u_**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**p_, x_), cons3, cons4, cons5, cons30, cons23, cons40, cons43)
    rule27 = _ReplacementRuleWrapped(pattern27, With27)
    def With28(b, c, n, a, p, x, u, j, m):
        q = Symbol('q')
        return eager_ReplaceAll(eager_ExpandIntegrand(S(4)**(-p)*c**(-p), x**m*(b + S(2)*c*x**n - q)**p*(b + S(2)*c*x**n + q)**p, x), eager_List(eager_Rule(q, eager_Rt(-S(4)*a*c + b**S(2), S(2))), eager_Rule(x, u)))
    pattern28 = Pattern(UtilityOperator(u_**WildSymbol('m', optional_value=S(1))*(u_**WildSymbol('j', optional_value=S(1))*WildSymbol('c', optional_value=S(1)) + u_**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0)))**p_, x_), cons3, cons4, cons5, cons44, cons23, cons40, cons45, cons46, cons43)
    rule28 = _ReplacementRuleWrapped(pattern28, With28)
    def With29(b, c, n, a, x, u, d, j):
        q = eager_Rt(-a/b, S(2))
        return -(c - d*q)/(S(2)*b*q*(q + u**n)) - (c + d*q)/(S(2)*b*q*(q - u**n))
    pattern29 = Pattern(UtilityOperator((u_**WildSymbol('n', optional_value=S(1))*WildSymbol('d', optional_value=S(1)) + WildSymbol('c', optional_value=S(0)))/(a_ + u_**WildSymbol('j', optional_value=S(1))*WildSymbol('b', optional_value=S(1))), x_), cons3, cons4, cons5, cons6, cons14, cons23)
    rule29 = _ReplacementRuleWrapped(pattern29, With29)
    def With30(e, b, c, f, n, a, g, x, u, d, j):
        q = eager_Rt(-S(4)*a*c + b**S(2), S(2))
        r = TogetherSimplify((-b*e*g + S(2)*c*(d + e*f))/q)
        return (e*g - r)/(b + 2*c*u**n + q) + (e*g + r)/(b + 2*c*u**n - q)
    pattern30 = Pattern(UtilityOperator(((u_**WildSymbol('n', optional_value=S(1))*WildSymbol('g', optional_value=S(1)) + WildSymbol('f', optional_value=S(0)))*WildSymbol('e', optional_value=S(1)) + WildSymbol('d', optional_value=S(0)))/(u_**WildSymbol('j', optional_value=S(1))*WildSymbol('c', optional_value=S(1)) + u_**WildSymbol('n', optional_value=S(1))*WildSymbol('b', optional_value=S(1)) + WildSymbol('a', optional_value=S(0))), x_), cons3, cons4, cons5, cons6, cons7, cons8, cons9, cons14, cons23, cons43)
    rule30 = _ReplacementRuleWrapped(pattern30, With30)
    def With31(v, x, u):
        lst = CoefficientList(u, x)
        i = Symbol('i')
        return x**eager_Exponent(u, x)*lst[-1]/v + Sum_doit(x**(i - 1)*eager_Part(lst, i), eager_List(i, 1, eager_Exponent(u, x)))/v
    pattern31 = Pattern(UtilityOperator(u_/v_, x_), cons19, cons47, cons48, cons49)
    rule31 = _ReplacementRuleWrapped(pattern31, With31)
    pattern32 = Pattern(UtilityOperator(u_/v_, x_), cons19, cons47, cons50)
    def replacement32(v, x, u):
        return eager_PolynomialDivide(u, v, x)
    rule32 = _ReplacementRuleWrapped(pattern32, replacement32)
    pattern33 = Pattern(UtilityOperator(u_*(x_*WildSymbol('a', optional_value=S(1)))**p_, x_), cons51, cons19)
    def replacement33(x, a, u, p):
        return eager_ExpandToSum((a*x)**p, u, x)
    rule33 = _ReplacementRuleWrapped(pattern33, replacement33)
    pattern34 = Pattern(UtilityOperator(v_**p_*WildSymbol('u', optional_value=S(1)), x_), cons51)
    def replacement34(v, x, u, p):
        return eager_ExpandIntegrand(eager_NormalizeIntegrand(v**p, x), u, x)
    rule34 = _ReplacementRuleWrapped(pattern34, replacement34)
    pattern35 = Pattern(UtilityOperator(u_, x_))
    def replacement35(x, u):
        return eager_ExpandExpression(u, x)
    rule35 = _ReplacementRuleWrapped(pattern35, replacement35)
    return [ rule2,rule3, rule4, rule5, rule6, rule7, rule8, rule10, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35]

def _RemoveContentAux():
    def cons_f1(b, a):
        return eager_IntegersQ(a, b)

    cons1 = _patched_custom_constraint_call(cons_f1)

    def cons_f2(b, a):
        return Equal(a + b, S(0))

    cons2 = _patched_custom_constraint_call(cons_f2)

    def cons_f3(m):
        return eager_RationalQ(m)

    cons3 = _patched_custom_constraint_call(cons_f3)

    def cons_f4(m, n):
        return eager_RationalQ(m, n)

    cons4 = _patched_custom_constraint_call(cons_f4)

    def cons_f5(m, n):
        return GreaterEqual(-m + n, S(0))

    cons5 = _patched_custom_constraint_call(cons_f5)

    def cons_f6(a, x):
        return eager_FreeQ(a, x)

    cons6 = _patched_custom_constraint_call(cons_f6)

    def cons_f7(m, n, p):
        return eager_RationalQ(m, n, p)

    cons7 = _patched_custom_constraint_call(cons_f7)

    def cons_f8(m, p):
        return GreaterEqual(-m + p, S(0))

    cons8 = _patched_custom_constraint_call(cons_f8)

    pattern1 = Pattern(UtilityOperator(a_**m_*WildSymbol('u', optional_value=S(1)) + b_*WildSymbol('v', optional_value=S(1)), x_), cons1, cons2, cons3)
    def replacement1(v, x, a, u, m, b):
        return eager_If(Greater(m, S(1)), RemoveContentAux(a**(m + S(-1))*u - v, x), RemoveContentAux(-a**(-m + S(1))*v + u, x))
    rule1 = _ReplacementRuleWrapped(pattern1, replacement1)
    pattern2 = Pattern(UtilityOperator(a_**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1)) + a_**WildSymbol('n', optional_value=S(1))*WildSymbol('v', optional_value=S(1)), x_), cons6, cons4, cons5)
    def replacement2(n, v, x, u, m, a):
        return RemoveContentAux(a**(-m + n)*v + u, x)
    rule2 = _ReplacementRuleWrapped(pattern2, replacement2)
    pattern3 = Pattern(UtilityOperator(a_**WildSymbol('m', optional_value=S(1))*WildSymbol('u', optional_value=S(1)) + a_**WildSymbol('n', optional_value=S(1))*WildSymbol('v', optional_value=S(1)) + a_**WildSymbol('p', optional_value=S(1))*WildSymbol('w', optional_value=S(1)), x_), cons6, cons7, cons5, cons8)
    def replacement3(n, v, x, p, u, w, m, a):
        return RemoveContentAux(a**(-m + n)*v + a**(-m + p)*w + u, x)
    rule3 = _ReplacementRuleWrapped(pattern3, replacement3)
    pattern4 = Pattern(UtilityOperator(u_, x_))
    def replacement4(u, x):
        return eager_If(And(eager_SumQ(u), eager_NegQ(eager_First(u))), -u, u)
    rule4 = _ReplacementRuleWrapped(pattern4, replacement4)
    return [rule1, rule2, rule3, rule4, ]

Log = log
Null = None

RemoveContentAux_replacer = ManyToOneReplacer(*_RemoveContentAux())
ExpandIntegrand_rules = _ExpandIntegrand()
TrigSimplifyAux_replacer = _TrigSimplifyAux()
SimplifyAntiderivative_replacer = _SimplifyAntiderivative()
SimplifyAntiderivativeSum_replacer = _SimplifyAntiderivativeSum()
FixSimplify_rules = _FixSimplify()
SimpFixFactor_replacer = _SimpFixFactor()
