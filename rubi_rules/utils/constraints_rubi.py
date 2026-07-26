# -*- coding: utf-8 -*-
"""RUBI-specific constraint predicates.

These are constraints defined by the RUBI (Rule-Based Integrator) project
that are NOT part of standard Wolfram Mathematica. They are implemented as
MathematicaConstraint subclasses for use in Rubi integration rule conditions.

All constraints operate on SymPy expressions after conversion from MatchPy.

Reference: Rubi/Rubi/IntegrationUtilityFunctions.m
"""
import sympy
from sympy import Symbol, Integer, Rational, Float, Add, Mul, Pow, Number, I, S
from sympy import sin, cos, tan, cot, sec, csc
from sympy import sinh, cosh, tanh, coth, sech, csch
from sympy import asin, acos, atan, acot, asec, acsc
from sympy import asinh, acosh, atanh, acoth, asech, acsch
from sympy import log

from sympy_wolfram.constraints import MathematicaConstraint
from .constraints_wolfram import _to_sympy


# =============================================================================
# Equality and Inequality Predicates
# =============================================================================

class EqQ(MathematicaConstraint):
    """Constraint: u - v equals 0 (possibly symbolically).

    Rubi: EqQ[u,v] — If u-v equals 0, returns True; else False.
    """
    def __init__(self, *args):
        self._u = self.args[0]
        self._v = self.args[1] if len(self.args) >= 2 else None
    def check(self, **kwargs):
        from .utility_functions import EqQ as _EqQ
        if len(self.args) != 2:
            return None
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _EqQ(u, v)
    def __repr__(self):
        return f"EqQ({self._u}, {self._v})"


class NeQ(MathematicaConstraint):
    """Constraint: u - v does NOT equal 0."""
    def __init__(self, u, v):
        self._u = self.args[0]
        self._v = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import NonzeroQ
        if len(self.args) != 2:
            return None
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return NonzeroQ(u - v)
    def __repr__(self):
        return f"NeQ({self._u}, {self._v})"


# =============================================================================
# Integer Inequality Predicates
# =============================================================================

class IGtQ(MathematicaConstraint):
    """Constraint: u is an integer AND u > n."""
    def __init__(self, u, n):
        self._u = self.args[0]
        self._n = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ, Greater
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        n = self._resolve(self._n, sk)
        return IntegerQ(u) and Greater(u, n)
    def __repr__(self):
        return f"IGtQ({self._u}, {self._n})"


class ILtQ(MathematicaConstraint):
    """Constraint: u is an integer AND u < n."""
    def __init__(self, u, n):
        self._u = self.args[0]
        self._n = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ, Less
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        n = self._resolve(self._n, sk)
        return IntegerQ(u) and Less(u, n)
    def __repr__(self):
        return f"ILtQ({self._u}, {self._n})"


class IGeQ(MathematicaConstraint):
    """Constraint: u is an integer AND u >= n."""
    def __init__(self, u, n):
        self._u = self.args[0]
        self._n = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ, GreaterEqual
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        n = self._resolve(self._n, sk)
        return IntegerQ(u) and GreaterEqual(u, n)
    def __repr__(self):
        return f"IGeQ({self._u}, {self._n})"


class ILeQ(MathematicaConstraint):
    """Constraint: u is an integer AND u <= n."""
    def __init__(self, u, n):
        self._u = self.args[0]
        self._n = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ, LessEqual
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        n = self._resolve(self._n, sk)
        return IntegerQ(u) and LessEqual(u, n)
    def __repr__(self):
        return f"ILeQ({self._u}, {self._n})"


# =============================================================================
# Numeric Inequality Predicates
# =============================================================================

class GtQ(MathematicaConstraint):
    """Constraint: u > v.  If w given, u > v and v > w."""
    def __init__(self, u, v, w=None):
        self._u = self.args[0]
        self._v = self.args[1]
        self._w = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import Greater
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        if not Greater(u, v):
            return False
        if self._w is not None:
            w = self._resolve(self._w, sk)
            return Greater(v, w)
        return True
    def __repr__(self):
        if self._w is not None:
            return f"GtQ({self._u}, {self._v}, {self._w})"
        return f"GtQ({self._u}, {self._v})"


class LtQ(MathematicaConstraint):
    """Constraint: u < v.  If w given, u < v and v < w."""
    def __init__(self, u, v, w=None):
        self._u = self.args[0]
        self._v = self.args[1]
        self._w = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import Less
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        if not Less(u, v):
            return False
        if self._w is not None:
            w = self._resolve(self._w, sk)
            return Less(v, w)
        return True
    def __repr__(self):
        if self._w is not None:
            return f"LtQ({self._u}, {self._v}, {self._w})"
        return f"LtQ({self._u}, {self._v})"


class GeQ(MathematicaConstraint):
    """Constraint: u >= v.  If w given, u >= v and v >= w."""
    def __init__(self, u, v, w=None):
        self._u = self.args[0]
        self._v = self.args[1]
        self._w = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import GreaterEqual
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        if not GreaterEqual(u, v):
            return False
        if self._w is not None:
            w = self._resolve(self._w, sk)
            return GreaterEqual(v, w)
        return True
    def __repr__(self):
        if self._w is not None:
            return f"GeQ({self._u}, {self._v}, {self._w})"
        return f"GeQ({self._u}, {self._v})"


class LeQ(MathematicaConstraint):
    """Constraint: u <= v.  If w given, u <= v and v <= w."""
    def __init__(self, u, v, w=None):
        self._u = self.args[0]
        self._v = self.args[1]
        self._w = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import LessEqual
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        if not LessEqual(u, v):
            return False
        if self._w is not None:
            w = self._resolve(self._w, sk)
            return LessEqual(v, w)
        return True
    def __repr__(self):
        if self._w is not None:
            return f"LeQ({self._u}, {self._v}, {self._w})"
        return f"LeQ({self._u}, {self._v})"


# =============================================================================
# Sign Predicates and Single-arg Numeric Type Predicates
# =============================================================================

class PosQ(MathematicaConstraint):
    """Constraint: u is positive."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import PosQ as _PosQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PosQ(u)
    def __repr__(self):
        return f"PosQ({self._u})"

class NegQ(MathematicaConstraint):
    """Constraint: u is negative."""
    def __init__(self, u, v=None):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NegQ as _NegQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NegQ(u)
    def __repr__(self):
        return f"NegQ({self._u})"

class HalfIntegerQ(MathematicaConstraint):
    """Constraint: u is a half-integer."""
    def __init__(self, *u):
        self._u = sympy.Tuple(*self.args)
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import Denominator
        for i in u:
            if isinstance(i, Rational) and Denominator(i) == 2:
                continue
            return False
        return True
    def __repr__(self):
        return f"HalfIntegerQ({', '.join(self._u)})"

class FractionQ(MathematicaConstraint):
    """Constraint: all args are explicit fractions."""
    def __init__(self, *args):
        self._vars = self.args
    def check(self, **kwargs):
        from .utility_functions import FractionQ as _FractionQ
        sk = self._resolve_all(kwargs)
        for a in self._vars:
            expr = self._resolve(a, sk)
            if not _FractionQ(expr):
                return False
        return True
    def __repr__(self):
        return f"FractionQ({', '.join(str(a) for a in self._vars)})"

class ComplexNumberQ(MathematicaConstraint):
    """Constraint: u is an explicit complex number."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import ComplexNumberQ as _ComplexNumberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _ComplexNumberQ(u)
    def __repr__(self):
        return f"ComplexNumberQ({self._u})"

class RealNumberQ(MathematicaConstraint):
    """Constraint: u is an explicit real number."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import RealNumericQ as _RealNumericQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _RealNumericQ(u)
    def __repr__(self):
        return f"RealNumberQ({self._u})"

class FractionOrNegativeQ(MathematicaConstraint):
    """Constraint: u is a fraction or negative."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import FractionOrNegativeQ as _FractionOrNegativeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _FractionOrNegativeQ(u)
    def __repr__(self):
        return f"FractionOrNegativeQ({self._u})"

class SqrtNumberQ(MathematicaConstraint):
    """Constraint: u is a sqrt of a rational."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import SqrtNumberQ as _SqrtNumberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _SqrtNumberQ(u)
    def __repr__(self):
        return f"SqrtNumberQ({self._u})"

class PowerQ(MathematicaConstraint):
    """Constraint: u is a power expression."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import PowerQ as _PowerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PowerQ(u)
    def __repr__(self):
        return f"PowerQ({self._u})"

class ProductQ(MathematicaConstraint):
    """Constraint: u is a product (Times)."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import ProductQ as _ProductQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _ProductQ(u)
    def __repr__(self):
        return f"ProductQ({self._u})"

class SumQ(MathematicaConstraint):
    """Constraint: u is a sum (Plus)."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import SumQ as _SumQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _SumQ(u)
    def __repr__(self):
        return f"SumQ({self._u})"

class NonsumQ(MathematicaConstraint):
    """Constraint: u is NOT a sum."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NonsumQ as _NonsumQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NonsumQ(u)
    def __repr__(self):
        return f"NonsumQ({self._u})"

class IntegerPowerQ(MathematicaConstraint):
    """Constraint: u is a power with integer exponent."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import IntegerPowerQ as _IntegerPowerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _IntegerPowerQ(u)
    def __repr__(self):
        return f"IntegerPowerQ({self._u})"

class FractionalPowerQ(MathematicaConstraint):
    """Constraint: u is a power with fractional exponent."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import FractionalPowerQ as _FractionalPowerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _FractionalPowerQ(u)
    def __repr__(self):
        return f"FractionalPowerQ({self._u})"

class ComplexFreeQ(MathematicaConstraint):
    """Constraint: u is free of complex numbers."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import ComplexFreeQ as _ComplexFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _ComplexFreeQ(u)
    def __repr__(self):
        return f"ComplexFreeQ({self._u})"

class FractionalPowerFreeQ(MathematicaConstraint):
    """Constraint: u is free of fractional powers."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import FractionalPowerFreeQ as _FractionalPowerFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _FractionalPowerFreeQ(u)
    def __repr__(self):
        return f"FractionalPowerFreeQ({self._u})"

class IntegralFreeQ(MathematicaConstraint):
    """Constraint: u is free of integrals."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import IntegralFreeQ as _IntegralFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _IntegralFreeQ(u)
    def __repr__(self):
        return f"IntegralFreeQ({self._u})"

class NiceSqrtQ(MathematicaConstraint):
    """Constraint: u has a nice square root."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NiceSqrtQ as _NiceSqrtQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NiceSqrtQ(u)
    def __repr__(self):
        return f"NiceSqrtQ({self._u})"

class InverseFunctionQ(MathematicaConstraint):
    """Constraint: u is a call on an inverse function."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import InverseFunctionQ as _InverseFunctionQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InverseFunctionQ(u)
    def __repr__(self):
        return f"InverseFunctionQ({self._u})"

class InertTrigQ(MathematicaConstraint):
    """Constraint: u is an inert trig function."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import InertTrigQ as _InertTrigQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InertTrigQ(u)
    def __repr__(self):
        return f"InertTrigQ({self._u})"

class InertTrigFreeQ(MathematicaConstraint):
    """Constraint: u is free of inert trig functions."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import InertTrigFreeQ as _InertTrigFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InertTrigFreeQ(u)
    def __repr__(self):
        return f"InertTrigFreeQ({self._u})"

class PerfectSquareQ(MathematicaConstraint):
    """Constraint: u is a perfect square."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import PerfectSquareQ as _PerfectSquareQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PerfectSquareQ(u)
    def __repr__(self):
        return f"PerfectSquareQ({self._u})"

class TrigQ(MathematicaConstraint):
    """Constraint: u is a trig function call."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import TrigQ as _TrigQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _TrigQ(u)
    def __repr__(self):
        return f"TrigQ({self._u})"

class HyperbolicQ(MathematicaConstraint):
    """Constraint: u is a hyperbolic function call."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import HyperbolicQ as _HyperbolicQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _HyperbolicQ(u)
    def __repr__(self):
        return f"HyperbolicQ({self._u})"

class InverseTrigQ(MathematicaConstraint):
    """Constraint: u is an inverse trig function call."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import InverseTrigQ as _InverseTrigQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InverseTrigQ(u)
    def __repr__(self):
        return f"InverseTrigQ({self._u})"

class InverseHyperbolicQ(MathematicaConstraint):
    """Constraint: u is an inverse hyperbolic function call."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import InverseHyperbolicQ as _InverseHyperbolicQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InverseHyperbolicQ(u)
    def __repr__(self):
        return f"InverseHyperbolicQ({self._u})"

class LogQ(MathematicaConstraint):
    """Constraint: u is a Log function call."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import LogQ as _LogQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _LogQ(u)
    def __repr__(self):
        return f"LogQ({self._u})"


# =============================================================================
# Variadic predicates
# =============================================================================

class IntegersQ(MathematicaConstraint):
    """Constraint: all values are explicit integers."""
    def __init__(self, *args):
        self._vars = self.args
    def check(self, **kwargs):
        from .utility_functions import IntegersQ as _IntegersQ
        sk = self._resolve_all(kwargs)
        exprs = [self._resolve(a, sk) for a in self._vars]
        return _IntegersQ(*exprs)
    def __repr__(self):
        return f"IntegersQ({', '.join(str(a) for a in self._vars)})"


class RationalQ(MathematicaConstraint):
    """Constraint: all values are rational numbers."""
    def __init__(self, *args):
        self._vars = self.args
    def check(self, **kwargs):
        from .utility_functions import RationalQ as _RationalQ
        sk = self._resolve_all(kwargs)
        exprs = [self._resolve(a, sk) for a in self._vars]
        return _RationalQ(*exprs)
    def __repr__(self):
        return f"RationalQ({', '.join(str(a) for a in self._vars)})"


# =============================================================================
# Polynomial Predicates (u, x) pattern
# =============================================================================

class PolyQ(MathematicaConstraint):
    """Constraint: u is polynomial in x, optionally of degree n."""
    def __init__(self, u, x, n=None):
        self._u = self.args[0]
        self._x = self.args[1]
        self._n = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import PolyQ as _PolyQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        if self._n is not None:
            n = self._resolve(self._n, sk)
            return _PolyQ(u, self._x, n)
        return _PolyQ(u, self._x)
    def __repr__(self):
        if self._n is not None:
            return f"PolyQ({self._u}, {self._x}, {self._n})"
        return f"PolyQ({self._u}, {self._x})"

class LinearQ(MathematicaConstraint):
    """Constraint: u is linear in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import LinearQ as _LinearQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _LinearQ(u, self._x)
    def __repr__(self):
        return f"LinearQ({self._u}, {self._x})"

class QuadraticQ(MathematicaConstraint):
    """Constraint: u is quadratic in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import QuadraticQ as _QuadraticQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _QuadraticQ(u, self._x)
    def __repr__(self):
        return f"QuadraticQ({self._u}, {self._x})"

class BinomialQ(MathematicaConstraint):
    """Constraint: u is binomial in x.  If n given, checks degree n."""
    def __init__(self, u, x, n=None):
        self._u = self.args[0]
        self._x = self.args[1]
        self._n = self.args[2] if len(self.args) > 2 else None
    def check(self, **kwargs):
        from .utility_functions import BinomialQ as _BinomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        if self._n is not None:
            n = self._resolve(self._n, sk)
            return _BinomialQ(u, self._x, n)
        return _BinomialQ(u, self._x)
    def __repr__(self):
        if self._n is not None:
            return f"BinomialQ({self._u}, {self._x}, {self._n})"
        return f"BinomialQ({self._u}, {self._x})"

class TrinomialQ(MathematicaConstraint):
    """Constraint: u is trinomial in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import TrinomialQ as _TrinomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _TrinomialQ(u, self._x)
    def __repr__(self):
        return f"TrinomialQ({self._u}, {self._x})"

class LinearMatchQ(MathematicaConstraint):
    """Pattern matching version of LinearQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import LinearMatchQ as _LinearMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _LinearMatchQ(u, self._x)
    def __repr__(self):
        return f"LinearMatchQ({self._u}, {self._x})"

class QuadraticMatchQ(MathematicaConstraint):
    """Pattern matching version of QuadraticQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import QuadraticMatchQ as _QuadraticMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _QuadraticMatchQ(u, self._x)
    def __repr__(self):
        return f"QuadraticMatchQ({self._u}, {self._x})"

class BinomialMatchQ(MathematicaConstraint):
    """Pattern matching version of BinomialQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import BinomialMatchQ as _BinomialMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _BinomialMatchQ(u, self._x)
    def __repr__(self):
        return f"BinomialMatchQ({self._u}, {self._x})"

class TrinomialMatchQ(MathematicaConstraint):
    """Pattern matching version of TrinomialQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import TrinomialMatchQ as _TrinomialMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _TrinomialMatchQ(u, self._x)
    def __repr__(self):
        return f"TrinomialMatchQ({self._u}, {self._x})"

class MonomialQ(MathematicaConstraint):
    """Constraint: u is a monomial in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import MonomialQ as _MonomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _MonomialQ(u, self._x)
    def __repr__(self):
        return f"MonomialQ({self._u}, {self._x})"

class GeneralizedBinomialQ(MathematicaConstraint):
    """Constraint: u is a generalized binomial."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import GeneralizedBinomialQ as _GeneralizedBinomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _GeneralizedBinomialQ(u, self._x)
    def __repr__(self):
        return f"GeneralizedBinomialQ({self._u}, {self._x})"

class GeneralizedBinomialMatchQ(MathematicaConstraint):
    """Pattern matching version of GeneralizedBinomialQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import GeneralizedBinomialMatchQ as _GeneralizedBinomialMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _GeneralizedBinomialMatchQ(u, self._x)
    def __repr__(self):
        return f"GeneralizedBinomialMatchQ({self._u}, {self._x})"

class GeneralizedTrinomialQ(MathematicaConstraint):
    """Constraint: u is a generalized trinomial."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import GeneralizedTrinomialQ as _GeneralizedTrinomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _GeneralizedTrinomialQ(u, self._x)
    def __repr__(self):
        return f"GeneralizedTrinomialQ({self._u}, {self._x})"

class GeneralizedTrinomialMatchQ(MathematicaConstraint):
    """Pattern matching version of GeneralizedTrinomialQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import GeneralizedTrinomialMatchQ as _GeneralizedTrinomialMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _GeneralizedTrinomialMatchQ(u, self._x)
    def __repr__(self):
        return f"GeneralizedTrinomialMatchQ({self._u}, {self._x})"

class InverseFunctionFreeQ(MathematicaConstraint):
    """Constraint: u is free of inverse functions in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import InverseFunctionFreeQ as _InverseFunctionFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _InverseFunctionFreeQ(u, self._x)
    def __repr__(self):
        return f"InverseFunctionFreeQ({self._u}, {self._x})"

class TrigHyperbolicFreeQ(MathematicaConstraint):
    """Constraint: u is free of trig/hyperbolic in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import TrigHyperbolicFreeQ as _TrigHyperbolicFreeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _TrigHyperbolicFreeQ(u, self._x)
    def __repr__(self):
        return f"TrigHyperbolicFreeQ({self._u}, {self._x})"

class RationalFunctionQ(MathematicaConstraint):
    """Constraint: u is a rational function in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import RationalFunctionQ as _RationalFunctionQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _RationalFunctionQ(u, self._x)
    def __repr__(self):
        return f"RationalFunctionQ({self._u}, {self._x})"

class AlgebraicFunctionQ(MathematicaConstraint):
    """Constraint: u is algebraic in x."""
    def __init__(self, u, x, flag_=False):
        self._u = self.args[0]
        self._x = self.args[1]
        self._flag_ = flag_
    def check(self, **kwargs):
        from .utility_functions import AlgebraicFunctionQ as _AlgebraicFunctionQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _AlgebraicFunctionQ(u, self._x, self._flag_)
    def __repr__(self):
        return f"AlgebraicFunctionQ({self._u}, {self._x})"

class IndependentQ(MathematicaConstraint):
    """Constraint: u is independent of x (alias for FreeQ)."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import IndependentQ as _IndependentQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _IndependentQ(u, self._x)
    def __repr__(self):
        return f"IndependentQ({self._u}, {self._x})"

class QuotientOfLinearsQ(MathematicaConstraint):
    """Constraint: u is a quotient of linears in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import QuotientOfLinearsQ as _QuotientOfLinearsQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _QuotientOfLinearsQ(u, self._x)
    def __repr__(self):
        return f"QuotientOfLinearsQ({self._u}, {self._x})"

class PowerOfLinearQ(MathematicaConstraint):
    """Constraint: u is a power of a linear in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import PowerOfLinearQ as _PowerOfLinearQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PowerOfLinearQ(u, self._x)
    def __repr__(self):
        return f"PowerOfLinearQ({self._u}, {self._x})"

class PowerOfLinearMatchQ(MathematicaConstraint):
    """Pattern matching version of PowerOfLinearQ."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import PowerOfLinearMatchQ as _PowerOfLinearMatchQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PowerOfLinearMatchQ(u, self._x)
    def __repr__(self):
        return f"PowerOfLinearMatchQ({self._u}, {self._x})"


# =============================================================================
# Simplicity Comparison Predicates (u, v)
# =============================================================================

class SimplerQ(MathematicaConstraint):
    """Constraint: u is simpler than v."""
    def __init__(self, u, v):
        self._u = self.args[0]
        self._v = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import SimplerQ as _SimplerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _SimplerQ(u, v)
    def __repr__(self):
        return f"SimplerQ({self._u}, {self._v})"


class SumSimplerQ(MathematicaConstraint):
    """Constraint: u is a simpler addition operand than v."""
    def __init__(self, u, v):
        self._u = self.args[0]
        self._v = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import SumSimplerQ as _SumSimplerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _SumSimplerQ(u, v)
    def __repr__(self):
        return f"SumSimplerQ({self._u}, {self._v})"


class SimplerSqrtQ(MathematicaConstraint):
    """Constraint: sqrt(u) is simpler than sqrt(v)."""
    def __init__(self, u, v):
        self._u = self.args[0]
        self._v = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import SimplerSqrtQ as _SimplerSqrtQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _SimplerSqrtQ(u, v)
    def __repr__(self):
        return f"SimplerSqrtQ({self._u}, {self._v})"


# =============================================================================
# Three-argument predicates (u, v, x)
# =============================================================================

class FunctionOfQ(MathematicaConstraint):
    """Constraint: u is a function of v wrt x."""
    def __init__(self, v, u, x, pure_flag: bool = False):
        self._v = self.args[0]
        self._u = self.args[1]
        self._x = self.args[2]
        self._pure_flag = pure_flag
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        v = self._resolve(self._v, sk)
        u = self._resolve(self._u, sk)
        x = self._resolve(self._x, sk)
        from .utility_functions import FunctionOfQ as _FunctionOfQ
        return _FunctionOfQ(v, u, x, PureFlag=self._pure_flag)
    def __repr__(self):
        return f"FunctionOfQ({self._v}, {self._u}, {self._x})"


class LinearPairQ(MathematicaConstraint):
    """Constraint: u and v are linear, and u/v is constant wrt x."""
    def __init__(self, u, v, x):
        self._u = self.args[0]
        self._v = self.args[1]
        self._x = self.args[2]
    def check(self, **kwargs):
        from .utility_functions import LinearPairQ as _LinearPairQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _LinearPairQ(u, v, self._x)
    def __repr__(self):
        return f"LinearPairQ({self._u}, {self._v}, {self._x})"


class PolynomialInQ(MathematicaConstraint):
    """Constraint: u is polynomial in v wrt x."""
    def __init__(self, u, v, x):
        self._u = self.args[0]
        self._v = self.args[1]
        self._x = self.args[2]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        from .utility_functions import PolynomialInQ as _PolynomialInQ
        return _PolynomialInQ(u, v, self._x)
    def __repr__(self):
        return f"PolynomialInQ({self._u}, {self._v}, {self._x})"


class SimplerIntegrandQ(MathematicaConstraint):
    """Constraint: u is simpler to integrate than v."""
    def __init__(self, u, v, x):
        self._u = self.args[0]
        self._v = self.args[1]
        self._x = self.args[2]
    def check(self, **kwargs):
        # Delegate to the utility function so we use LeafCount with the correct
        # 6/10 threshold (IntegrationUtilityFunctions.m line 810), not count_ops.
        # When called from Condition._evaluate() after With.doit() substitution,
        # self._u and self._v already hold actual SymPy expressions (not WildSymbols),
        # so _resolve with an empty sk simply returns them unchanged.
        from .utility_functions import SimplerIntegrandQ as _SimplerIntegrandQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        x = self._resolve(self._x, sk)
        return _SimplerIntegrandQ(u, v, x)
    def __repr__(self):
        return f"SimplerIntegrandQ({self._u}, {self._v}, {self._x})"


class PseudoBinomialPairQ(MathematicaConstraint):
    """Constraint: u and v are pseudo-binomial pairs."""
    def __init__(self, u, v, x):
        self._u = self.args[0]
        self._v = self.args[1]
        self._x = self.args[2]
    def check(self, **kwargs):
        from .utility_functions import PseudoBinomialPairQ as _PseudoBinomialPairQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _PseudoBinomialPairQ(u, v, self._x)
    def __repr__(self):
        return f"PseudoBinomialPairQ({self._u}, {self._v}, {self._x})"


class SubstForFractionalPowerQ(MathematicaConstraint):
    """Constraint: substitution x=v^(1/n) is safe."""
    def __init__(self, u, v, x):
        self._u = self.args[0]
        self._v = self.args[1]
        self._x = self.args[2]
    def check(self, **kwargs):
        from .utility_functions import SubstForFractionalPowerQ as _SubstForFractionalPowerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        v = self._resolve(self._v, sk)
        return _SubstForFractionalPowerQ(u, v, self._x)
    def __repr__(self):
        return f"SubstForFractionalPowerQ({self._u}, {self._v}, {self._x})"


# =============================================================================
# Integrability Predicates
# =============================================================================

class IntLinearQ(MathematicaConstraint):
    """Constraint: exponents are integrable for linear binomial products."""
    def __init__(self, a, b, c, d, m, n, x):
        self._a = self.args[0]
        self._b = self.args[1]
        self._c = self.args[2]
        self._d = self.args[3]
        self._m = self.args[4]
        self._n = self.args[5]
        self._x = self.args[6]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ, IntegersQ, Less, Greater, IntLinearcQ as _IntLinearQ
        sk = self._resolve_all(kwargs)
        a = self._resolve(self._a, sk)
        b = self._resolve(self._b, sk)
        c = self._resolve(self._c, sk)
        d = self._resolve(self._d, sk)
        m = self._resolve(self._m, sk)
        n = self._resolve(self._n, sk)
        return _IntLinearQ(a, b, c, d, m, n, self._x)
    def __repr__(self):
        return f"IntLinearQ({self._a}, {self._b}, {self._c}, {self._d}, {self._m}, {self._n}, {self._x})"


class IntBinomialQ(MathematicaConstraint):
    """Constraint: exponents are integrable for binomial products.

    Supports multiple arities from Mathematica:
      7 args: IntBinomialQ[a, b, c, n, m, p, x]
      8 args: IntBinomialQ[a, b, c, d, n, p, q, x]
     10 args: IntBinomialQ[a, b, c, d, e, m, n, p, q, x]
    """
    def __init__(self, *args):
        # Store all args generically; x is always last
        self._vars = self.args
    def check(self, **kwargs):
        from .utility_functions import IntBinomialQ

        sk = self._resolve_all(kwargs)
        args = [self._resolve(arg, sk) for arg in self.args]
        return IntBinomialQ(*args)

    def __repr__(self):
        return f"IntBinomialQ({', '.join(str(a) for a in self._vars)})"


class IntQuadraticQ(MathematicaConstraint):
    """Constraint: exponents are integrable for quadratic products."""
    def __init__(self, a, b, c, d, e, m, p, x):
        self._a = self.args[0]
        self._b = self.args[1]
        self._c = self.args[2]
        self._d = self.args[3]
        self._e = self.args[4]
        self._m = self.args[5]
        self._p = self.args[6]
        self._x = self.args[7]
    def check(self, **kwargs):
        from .utility_functions import IntQuadraticQ as _IntQuadraticQ
        sk = self._resolve_all(kwargs)
        a = self._resolve(self._a, sk)
        b = self._resolve(self._b, sk)
        c = self._resolve(self._c, sk)
        d = self._resolve(self._d, sk)
        e = self._resolve(self._e, sk)
        m = self._resolve(self._m, sk)
        p = self._resolve(self._p, sk)
        return _IntQuadraticQ(a, b, c, d, e, m, p, self._x)
    def __repr__(self):
        return f"IntQuadraticQ({self._a}, {self._b}, {self._c}, {self._d}, {self._e}, {self._m}, {self._p}, {self._x})"


# =============================================================================
# Complex single-arg predicates with custom logic
# =============================================================================

class FractionalPowerFactorQ(MathematicaConstraint):
    """Constraint: a factor of u is complex constant or fractional power."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        # NB import ProductQ from utility_functions: the bare name `ProductQ` in this
        # module is the CONSTRAINT CLASS (always truthy when constructed), so `if
        # ProductQ(u)` without this import wrongly took the product branch for EVERY u.
        from .utility_functions import AtomQ, PowerQ, FractionQ, First, Rest, ProductQ
        if AtomQ(u):
            # Mathematica: Head[u] === Complex -- True only for an explicit COMPLEX NUMBER
            # (I, 2*I as Complex[0,2], ...), NOT for every atom. The old `u.is_complex`
            # was wrong: in SymPy reals are complex, so it wrongly fired on real atoms.
            return bool(u.is_number and u.is_real is False)
        if PowerQ(u):
            return FractionQ(u.exp)
        if ProductQ(u):
            # Mathematica recurses First[u] || Rest[u]. Rest[u] must stay a PRODUCT of the
            # remaining factors; the old `u.args[1:]` handed a bare TUPLE, which is neither
            # atom/power/product, so the recursion peeled it to an empty args tuple and
            # raised IndexError (Int[x^2 (d+e x)/Sqrt[d^2-e^2 x^2]] etc. crashed here).
            return (FractionalPowerFactorQ(First(u)).check(**kwargs)
                    or FractionalPowerFactorQ(Rest(u)).check(**kwargs))
        return False
    def __repr__(self):
        return f"FractionalPowerFactorQ({self._u})"


class SumBaseQ(MathematicaConstraint):
    """Constraint: u is a sum or sum raised to an odd power."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        expr = self._resolve(self._u, sk)
        if isinstance(expr, Add):
            return True
        if isinstance(expr, Pow) and expr.exp.is_odd:
            return isinstance(expr.base, Add)
        return False
    def __repr__(self):
        return f"SumBaseQ({self._u})"


class PiecewiseLinearQ(MathematicaConstraint):
    """Constraint: u is piecewise linear in x."""
    def __init__(self, *args):
        self._u = self.args[0]
        if len(self.args) == 2:
            self._v = None
            self._x = self.args[1]
        elif len(self.args) == 3:
            self._v = self.args[1]
            self._x = self.args[2]

    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        x = self._resolve(self._x, sk)

        from .utility_functions import PiecewiseLinearQ as _PiecewiseLinearQ

        if self._v is None:
            return _PiecewiseLinearQ(u, x)
        else:
            v = self._resolve(self._v, sk)
            return _PiecewiseLinearQ(u, v, x)

    def __repr__(self):
        return f"PiecewiseLinearQ({self._u}, {self._x})"


class CalculusFreeQ(MathematicaConstraint):
    """Constraint: u is free of calculus functions in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        for sub in sympy.preorder_traversal(u):
            if isinstance(sub, (sympy.Integral, sympy.Derivative)):
                if self._x in sub.free_symbols:
                    return False
        return True
    def __repr__(self):
        return f"CalculusFreeQ({self._u}, {self._x})"


class FunctionOfExponentialQ(MathematicaConstraint):
    """Constraint: u contains an exponential F^(a+b*x)."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from sympy import exp as sym_exp
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import FunctionOfExponentialQ
        return FunctionOfExponentialQ(u, self._x)
    def __repr__(self):
        return f"FunctionOfExponentialQ({self._u}, {self._x})"


class FunctionOfTrigOfLinearQ(MathematicaConstraint):
    """Constraint: u involves trig of linear expression in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import FunctionOfTrigOfLinearQ as _FunctionOfTrigOfLinearQ
        return _FunctionOfTrigOfLinearQ(u, self._x)
    def __repr__(self):
        return f"FunctionOfTrigOfLinearQ({self._u}, {self._x})"


class QuadraticProductQ(MathematicaConstraint):
    """Constraint: u is a product of quadratics in x."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        expr = self._resolve(self._u, sk)
        if isinstance(expr, Mul):
            from sympy import Poly, degree
            for arg in expr.args:
                if self._x in arg.free_symbols:
                    try:
                        if degree(Poly(arg, self._x)) != 2:
                            return False
                    except Exception:
                        return False
            return True
        return False
    def __repr__(self):
        return f"QuadraticProductQ({self._u}, {self._x})"


# Trig integrand predicates (u, x) with custom check logic
class KnownSineIntegrandQ(MathematicaConstraint):
    """Constraint: u is a known sine/cosine integrand pattern."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import KnownSineIntegrandQ as _KnownSineIntegrandQ
        return _KnownSineIntegrandQ(u, self._x)
    def __repr__(self):
        return f"KnownSineIntegrandQ({self._u}, {self._x})"


class KnownSecantIntegrandQ(MathematicaConstraint):
    """Constraint: u is a known secant/cosecant integrand pattern."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import KnownSecantIntegrandQ as _KnownSecantIntegrandQ
        return _KnownSecantIntegrandQ(u, self._x)
    def __repr__(self):
        return f"KnownSecantIntegrandQ({self._u}, {self._x})"


class KnownTangentIntegrandQ(MathematicaConstraint):
    """Constraint: u is a known tangent integrand pattern."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import KnownTangentIntegrandQ as _KnownTangentIntegrandQ
        return _KnownTangentIntegrandQ(u, self._x)
    def __repr__(self):
        return f"KnownTangentIntegrandQ({self._u}, {self._x})"


class KnownCotangentIntegrandQ(MathematicaConstraint):
    """Constraint: u is a known cotangent integrand pattern."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        from .utility_functions import KnownCotangentIntegrandQ as _KnownCotangentIntegrandQ
        return _KnownCotangentIntegrandQ(u, self._x)
    def __repr__(self):
        return f"KnownCotangentIntegrandQ({self._u}, {self._x})"


class EulerIntegrandQ(MathematicaConstraint):
    """Constraint: u is an Euler integrand."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        expr = self._resolve(self._u, sk)
        from .utility_functions import EulerIntegrandQ as _EulerIntegrandQ
        return _EulerIntegrandQ(expr, self._x)
    def __repr__(self):
        return f"EulerIntegrandQ({self._u}, {self._x})"


# =============================================================================
# Rarely-used / stub predicates
# =============================================================================

class EqM(MathematicaConstraint):
    """Constraint: symbolic expression equality (stub)."""
    def __init__(self, *args, **kw):
        self._args_stored = args
    def check(self, **kwargs):
        return True
    def __repr__(self):
        return f"EqM({self._args_stored})"


class ExpressionEqQ(MathematicaConstraint):
    """Generic constraint for linear combination equality."""
    def __init__(self, coefficients, constant=0, target=0):
        if isinstance(coefficients, dict):
            items = list(coefficients.items())
        else:
            items = list(coefficients)
        self._coefficients = {str(k) if not isinstance(k, str) else k: sympy.sympify(v)
                              for k, v in items}
        self._constant = sympy.sympify(constant)
        self._target = sympy.sympify(target)
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        total = self._constant
        for var_name, coeff in self._coefficients.items():
            val = sk.get(var_name, sympy.Symbol(var_name))
            total += coeff * val
        from .utility_functions import ZeroQ
        return ZeroQ(total - self._target)
    def __repr__(self):
        return f"ExpressionEqQ({self._coefficients}, {self._constant}, {self._target})"


class EveryQ(MathematicaConstraint):
    """Constraint: predicate holds for all sub-expressions."""
    def __init__(self, func, u):
        self._func = self.args[0]
        self._u = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        expr = self._resolve(self._u, sk)
        if isinstance(expr, sympy.Basic) and expr.args:
            return all(self._func(a) for a in expr.args)
        return bool(self._func(expr))
    def __repr__(self):
        return f"EveryQ(<func>, {self._u})"


class TrigSimplifyQ(MathematicaConstraint):
    """Constraint: TrigSimplify[u] actually simplifies u.

    Rubi: TrigSimplifyQ[u] returns True if TrigSimplify[u] != ActivateTrig[u].
    """
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import TrigSimplifyQ as _TrigSimplifyQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _TrigSimplifyQ(u)
    def __repr__(self):
        return f"TrigSimplifyQ({self._u})"


class TryPureTanSubst(MathematicaConstraint):
    """Constraint: u admits a pure tan/cot substitution."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import TryPureTanSubst as _TryPureTanSubst
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        x = self._resolve(self._x, sk)
        return _TryPureTanSubst(u, x)
    def __repr__(self):
        return f"TryPureTanSubst({self._u}, {self._x})"
