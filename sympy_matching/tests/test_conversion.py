# -*- coding: utf-8 -*-
"""Tests for SymPy ↔ OmniMatch expression conversion."""
import sys
import os
import importlib
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sympy
from sympy import symbols, sin, cos, tan, exp, log, Eq, Integer, Rational, S

from omnimatch.expressions.expressions import Operation, NamedAtom, SymbolWrapper, to_omnimatch_expression
from sympy_matching import to_omnimatch_expression, omnimatch_to_sympy
from sympy_matching.operations import (
    ADD, MUL, POW, SIN, COS, TAN, EXP, LOG, EQUALITY,
    SYMPY_NODES, SYMPY_FUNC_TO_HEAD,
)

from sympy.functions.special.bessel import besselj, bessely, besseli, besselk
from sympy.functions.special.bessel import hankel1, hankel2, airyai, airybi
from sympy.functions.special.hyper import hyper, meijerg, appellf1
from sympy.functions.special.gamma_functions import gamma, lowergamma, uppergamma, polygamma
from sympy.functions.special.beta_functions import beta
from sympy.functions.special.error_functions import erf, erfc, Ei, Si, Ci, fresnels, fresnelc
from sympy.functions.special.elliptic_integrals import elliptic_f, elliptic_k
from sympy.functions.special.delta_functions import DiracDelta, Heaviside
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.functions.special.polynomials import legendre, chebyshevt, hermite
from sympy.functions.special.zeta_functions import zeta, polylog, lerchphi
from sympy.functions.combinatorial.factorials import factorial, binomial, RisingFactorial
from sympy.functions.elementary.complexes import Abs, conjugate, arg as sympy_arg
from sympy.functions.elementary.integers import floor, ceiling
from sympy.functions.elementary.trigonometric import atan, sec, csc, asin
from sympy.functions.elementary.hyperbolic import sinh, cosh, tanh, asinh


x, y, z = symbols('x y z')


# ─── Argument recipes for multi-arg functions ─────────────────────────────────

_ARG_OVERRIDES = {
    'atan2': (x, y),
    'appellf1': (S(1), S(2), S(3), S(4), x, y),
    'elliptic_pi': (x, y, S(1)/2),
    'expint': (S(1), x),
    'polygamma': (S(1), x),
    'zeta': (S(2), x),
    'lerchphi': (x, S(2), y),
    'RisingFactorial': (x, S(3)),
    'FallingFactorial': (x, S(3)),
    'legendre': (S(3), x),
    'chebyshevt': (S(3), x),
    'chebyshevu': (S(3), x),
    'hermite': (S(3), x),
    'laguerre': (S(3), x),
    'besselj': (S(1), x),
    'bessely': (S(0), x),
    'besseli': (S(2), x),
    'besselk': (S(1), x),
    'hankel1': (S(1), x),
    'hankel2': (S(1), x),
    'jn': (S(1), x),
    'yn': (S(1), x),
}

_XFAIL_NAMES = {'hyper', 'meijerg', 'Piecewise'}


def _resolve(module_path, class_name):
    mod = importlib.import_module(module_path)
    return getattr(mod, class_name)


def _build_roundtrip_cases():
    """Build one test expression per SYMPY_NODES entry."""
    cases = []
    for module_path, class_name, arity_code in SYMPY_NODES:
        try:
            func = _resolve(module_path, class_name)
        except (ImportError, AttributeError):
            continue
        if not isinstance(func, type):
            continue
        if class_name in _XFAIL_NAMES:
            continue

        try:
            if class_name in _ARG_OVERRIDES:
                expr = func(*_ARG_OVERRIDES[class_name])
            elif arity_code == 'u':
                expr = func(x)
            elif arity_code == 'b':
                expr = func(x, y)
            else:
                expr = func(x, y)
        except Exception:
            continue

        if expr.is_Atom:
            continue

        cases.append(pytest.param(expr, id=class_name))
    return cases


# ─── Test cases ───────────────────────────────────────────────────────────────

CASES = [
    # Structural (SymPy expr, expected OmniMatch expr)
    (x, SymbolWrapper(x)),
    (Integer(42), SymbolWrapper(Integer(42))),
    (Integer(-3), SymbolWrapper(Integer(-3))),
    (Rational(3, 2), SymbolWrapper(Rational(3, 2))),
    (sympy.I, SymbolWrapper(sympy.I)),
    (x + y, Operation(ADD, SymbolWrapper(x), SymbolWrapper(y))),
    (x*y, Operation(MUL, SymbolWrapper(x), SymbolWrapper(y))),
    (x**2, Operation(POW, SymbolWrapper(x), SymbolWrapper(2))),
    (sin(x), Operation(SIN, SymbolWrapper(x))),
    (cos(x), Operation(COS, SymbolWrapper(x))),
    (tan(x), Operation(TAN, SymbolWrapper(x))),
    (exp(x), Operation(EXP, SymbolWrapper(x))),
    (log(x), Operation(LOG, SymbolWrapper(x))),
    (Eq(x, 0), Operation(EQUALITY, SymbolWrapper(x), SymbolWrapper(0))),
    (sin(x)**2, Operation(POW, Operation(SIN, SymbolWrapper(x)), SymbolWrapper(2))),
    (sin(x)**2 + cos(x)**2, Operation(ADD, Operation(POW, Operation(COS, SymbolWrapper(x)), SymbolWrapper(2)), Operation(POW, Operation(SIN, SymbolWrapper(x)), SymbolWrapper(2)))),
    (2*x*y, Operation(MUL, SymbolWrapper(2), SymbolWrapper(x), SymbolWrapper(y))),

    (log(sin(x)), Operation(LOG, Operation(SIN, SymbolWrapper(x)))),

    (2*x + 3*y, Operation(ADD, Operation(MUL, SymbolWrapper(2), SymbolWrapper(x)), Operation(MUL, SymbolWrapper(3), SymbolWrapper(y)))),
    (exp(x) + 1, Operation(ADD, SymbolWrapper(1), Operation(EXP, SymbolWrapper(x)))),
    (log(x * y), Operation(LOG, Operation(MUL, SymbolWrapper(x), SymbolWrapper(y)))),
    (Eq(x, 0), Operation(EQUALITY, SymbolWrapper(x), SymbolWrapper(0))),
]

CASE_IDS = [str(c[0]) for c in CASES]

ROUNDTRIP_CASES = _build_roundtrip_cases()


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestConversions:

    # ── Structural: verify exact OmniMatch tree shape ───────────────────────────

    @pytest.mark.parametrize("expr_sympy,expr_omnimatch", CASES, ids=CASE_IDS)
    def test_convert_sympy_to_omnimatch(self, expr_sympy, expr_omnimatch):
        expr_omnimatch_converted = to_omnimatch_expression(expr_sympy)
        assert expr_omnimatch_converted == expr_omnimatch
        if isinstance(expr_omnimatch, Operation):
            assert isinstance(expr_omnimatch_converted, Operation)
            assert expr_omnimatch_converted.head == expr_omnimatch.head
            assert len(expr_omnimatch_converted.operands) == len(expr_omnimatch.operands)
        if isinstance(expr_omnimatch, SymbolWrapper):
            assert isinstance(expr_omnimatch_converted, SymbolWrapper)
            assert expr_omnimatch_converted.value == expr_omnimatch.value
            assert expr_omnimatch_converted.name == expr_omnimatch.name

    @pytest.mark.parametrize("expr_sympy,expr_omnimatch", CASES, ids=CASE_IDS)
    def test_convert_omnimatch_to_sympy(self, expr_sympy, expr_omnimatch):
        expr_sympy_converted = omnimatch_to_sympy(expr_omnimatch)
        assert expr_sympy_converted == expr_sympy

    @pytest.mark.parametrize("expr_sympy,expr_omnimatch", CASES, ids=CASE_IDS)
    def test_roundtrip_structural(self, expr_sympy, expr_omnimatch):
        """SymPy → OmniMatch → SymPy preserves expressions (structural cases)."""
        mp_expr = to_omnimatch_expression(expr_sympy)
        result = omnimatch_to_sympy(mp_expr)
        if isinstance(expr_sympy, sympy.Eq):
            assert result == expr_sympy
        else:
            assert sympy.simplify(result - expr_sympy) == 0 or result == expr_sympy

    # ── Roundtrip: every registered SYMPY_NODES entry ─────────────────────────

    @pytest.mark.parametrize("expr", ROUNDTRIP_CASES)
    def test_roundtrip(self, expr):
        """SymPy → OmniMatch → SymPy roundtrip for every registered node."""
        mp_expr = to_omnimatch_expression(expr)
        result = omnimatch_to_sympy(mp_expr)
        assert result == expr

    @pytest.mark.parametrize("expr", ROUNDTRIP_CASES)
    def test_produces_operation(self, expr):
        """to_omnimatch_expression produces an Operation for non-atom function calls."""
        mp_expr = to_omnimatch_expression(expr)
        assert isinstance(mp_expr, Operation)

    @pytest.mark.parametrize("expr", ROUNDTRIP_CASES)
    def test_head_is_registered(self, expr):
        """Top-level head belongs to the registered set."""
        mp_expr = to_omnimatch_expression(expr)
        assert mp_expr.head in SYMPY_FUNC_TO_HEAD.values()

    @pytest.mark.parametrize("expr", ROUNDTRIP_CASES)
    def test_dispatch_is_direct(self, expr):
        """Singledispatch routes directly, not through the SympyBasic fallback."""
        handler = to_omnimatch_expression.dispatch(type(expr))
        assert 'basic' not in handler.__name__.lower(), (
            f"{type(expr).__name__} falls through to the generic handler"
        )

    # ── Roundtrips of heads with an internal container arg ────────────────────
    # hyper/meijerg hold their parameter lists as TupleArg; the conversion
    # unwraps them, so these roundtrip exactly. Piecewise (ExprCondPair) does not.

    def test_hyper_roundtrip(self):
        expr = hyper((S(1), S(2)), (S(3),), x)
        assert omnimatch_to_sympy(to_omnimatch_expression(expr)) == expr

    def test_meijerg_roundtrip(self):
        expr = meijerg((S(1),), (S(2),), (S(3),), (S(4),), x)
        assert omnimatch_to_sympy(to_omnimatch_expression(expr)) == expr

    @pytest.mark.xfail(reason="Piecewise uses ExprCondPair internally")
    def test_piecewise_roundtrip(self):
        from sympy.functions.elementary.piecewise import Piecewise
        expr = Piecewise((x, x > 0), (S(0), True))
        assert omnimatch_to_sympy(to_omnimatch_expression(expr)) == expr


# ── hyper / meijerg / appellf1 round-trip ────────────────────────────────────
# These special functions store their parameter lists in TupleArg containers.
# omnimatch_to_sympy used to rebuild them as cls(*args), passing the TupleArg back
# in, which the constructor rejects (hyper does Tuple(*ap) -> TypeError). The fix
# unwraps TupleArg operands to plain tuples. Regression guard for the crash that
# broke sqrt(a+b*x)/x, 1/(x*sqrt(a+b*x)), x^k/(a+b*x)^(3/2), ... integration.

def test_hyper_roundtrip():
    a, b, c, w = symbols('a b c w')
    h = hyper((a, b), (c,), w)
    assert omnimatch_to_sympy(to_omnimatch_expression(h)) == h


def test_meijerg_roundtrip():
    a, b, c, d, w = symbols('a b c d w')
    g = meijerg(((a,), (b,)), ((c,), (d,)), w)
    assert omnimatch_to_sympy(to_omnimatch_expression(g)) == g


def test_appellf1_roundtrip():
    a, b1, b2, c, x1, y1 = symbols('a b1 b2 c x1 y1')
    f = appellf1(a, b1, b2, c, x1, y1)
    assert omnimatch_to_sympy(to_omnimatch_expression(f)) == f


class TestSympyTupleHead:
    """``sympy.Tuple`` is a container, not a function, so it was easy to miss when
    registering heads -- but ``Derivative`` stores its ``(var, order)`` spec as one.
    While it was unregistered it fell through to the generic path and came back as
    an UNDEFINED function named "Tuple", so any generic ``expr.func(*expr.args)``
    traversal silently turned a Derivative into a non-derivative.
    """

    def test_roundtrips_as_a_real_sympy_tuple(self):
        t = sympy.Tuple(x, S(1))
        rt = omnimatch_to_sympy(to_omnimatch_expression(t))
        assert rt == t
        assert type(rt) is sympy.Tuple

    def test_a_plain_python_tuple_still_roundtrips_separately(self):
        """TUPLE_HEAD ('tuple') and the new TUPLE head ('Tuple') must not collide."""
        rt = omnimatch_to_sympy(to_omnimatch_expression((x, S(1))))
        assert rt == (x, S(1))
        assert type(rt) is tuple

    def test_the_two_heads_are_distinct(self):
        from sympy_matching.conversion import TUPLE_HEAD
        assert to_omnimatch_expression(sympy.Tuple(x)).head != TUPLE_HEAD
        assert to_omnimatch_expression((x,)).head == TUPLE_HEAD

    def test_nested_inside_a_derivative_survives(self):
        f = sympy.Function('f')
        d = sympy.Derivative(f(x), (x, 3))
        assert omnimatch_to_sympy(to_omnimatch_expression(d)) == d

    def test_rebuilding_from_args_is_identity_after_a_roundtrip(self):
        """The exact traversal (TrigSimplifyRecur) that used to corrupt Derivative."""
        f = sympy.Function('f')
        d = sympy.Derivative(f(x), (x, 2))
        rebuilt_args = [omnimatch_to_sympy(to_omnimatch_expression(a)) for a in d.args]
        assert d.func(*rebuilt_args) == d

    def test_hyper_tuplearg_is_not_captured_by_the_tuple_registration(self):
        """TupleArg subclasses Tuple; head lookup is by EXACT type, so hyper keeps
        its own handling and still roundtrips."""
        expr = hyper((S(1), S(2)), (S(3),), x)
        assert omnimatch_to_sympy(to_omnimatch_expression(expr)) == expr
