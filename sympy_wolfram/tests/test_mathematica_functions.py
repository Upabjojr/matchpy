# -*- coding: utf-8 -*-
"""Tests for the standard Wolfram function nodes moved into sympy_wolfram.

These functions (GCD, Sign, Floor, Together, ProductLog, LeafCount, …) are
Mathematica standard-library, not Rubi-specific, so they live in
``sympy_wolfram.mathematica_functions`` (deferred nodes) and
``sympy_wolfram.functions_eager`` (self-contained eager helpers).

Covers:
- Module location: the nodes live in sympy_wolfram, not rubi_rules
- No wrong-direction import: neither new module imports rubi_rules
- Behaviour of a representative set (via .doit())
- Backward-compat: rubi_rules.utils.rubi_utils re-exports the SAME class objects
"""
import ast
import importlib

import pytest
import sympy
from sympy import Symbol, Integer, I, S, sin, cos

from sympy_wolfram import mathematica_functions as mf
from sympy_wolfram import functions_eager as fe
from sympy_wolfram.objects import MathematicaExpr


x = Symbol('x')


# ---------------------------------------------------------------------------
# 1. Location + no wrong-direction imports
# ---------------------------------------------------------------------------

MOVED_NODES = [
    'Coefficient', 'PolynomialQuotient', 'PolynomialRemainder', 'Rule',
    'ReplaceAll', 'SumWolfram', 'Numerator', 'Together', 'GCD', 'Sign',
    'Quotient', 'EllipticPi', 'Apply', 'FullSimplify', 'Simplify',
    'FunctionExpand', 'Binomial', 'ProductLog', 'Floor', 'Hypergeometric2F1',
    'LeafCount', 'Length', 'Not',
    # Relocated out of rubi_rules (their Rubi bodies only ever called generic
    # SymPy operations — is_Add/is_Mul/sort_key/is_rational_function/part-extract).
    'First', 'Rest', 'Part', 'Apart', 'Denominator', 'Exponent',
]


@pytest.mark.parametrize('name', MOVED_NODES)
def test_node_lives_in_sympy_wolfram(name):
    cls = getattr(mf, name)
    assert cls.__module__ == 'sympy_wolfram.mathematica_functions'
    assert issubclass(cls, MathematicaExpr)


@pytest.mark.parametrize('mod', [
    'sympy_wolfram.mathematica_functions',
    'sympy_wolfram.functions_eager',
])
def test_no_rubi_import_in_module(mod):
    m = importlib.import_module(mod)
    tree = ast.parse(open(m.__file__).read())
    rubi = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
        and any('rubi' in getattr(a, 'name', '') or 'rubi' in (getattr(n, 'module', '') or '')
                for a in getattr(n, 'names', [n]))
    ]
    assert not rubi, f"{mod} imports rubi_rules: {rubi}"


# ---------------------------------------------------------------------------
# 2. Behaviour
# ---------------------------------------------------------------------------

def test_behaviour():
    assert mf.GCD(Integer(12), Integer(18)).doit() == Integer(6)
    assert mf.Sign(Integer(-3)).doit() == Integer(-1)
    assert mf.Floor(Integer(7), Integer(2)).doit() == Integer(6)     # nearest multiple of 2
    assert mf.Quotient(Integer(7), Integer(2)).doit() == Integer(3)
    assert mf.ProductLog(Integer(0)).doit() == Integer(0)
    assert mf.Binomial(Integer(5), Integer(2)).doit() == Integer(10)
    assert mf.Coefficient(x**2 + 3 * x, x, Integer(1)).doit() == Integer(3)
    assert mf.Sum(x, mf.List(x, Integer(1), Integer(3))).doit() == Integer(6)
    assert mf.LeafCount(sin(x)).doit() == Integer(2)
    assert mf.Length(x + Integer(1)).doit() == Integer(2)
    assert mf.Not(Integer(0)).doit() is True
    assert mf.Complex(Integer(2), Integer(3)) == 2 + 3 * I           # eager __new__


def test_eager_helpers_are_self_contained():
    assert fe.LeafCount(sin(x)) == 2
    assert fe.Length(x + Integer(1)) == 2
    assert fe.Complex(Integer(0), Integer(1)) == I
    assert fe.Not(False) is True


# ---------------------------------------------------------------------------
# 2b. Relocated First/Rest/Part/Apart/Numerator/Denominator/Exponent/Simplify
#     (behaviour moved here from rubi_rules/tests/test_utility_function.py, since
#     the functions themselves moved into this layer).
# ---------------------------------------------------------------------------

a, b, c, y = sympy.symbols('a b c y')


def test_eager_First_Rest():
    assert fe.First([2, 3, 5, 7]) == 2
    assert fe.First(y ** 2) == y
    assert fe.First(a + b + c) == a          # canonical sort_key order
    assert fe.First(a * b * c) == a
    assert fe.Rest([2, 3, 5, 7]) == [3, 5, 7]
    assert fe.Rest(a + b + c) == b + c
    assert fe.Rest(a * b * c) == b * c
    assert fe.Rest(1 / b) == -1


def test_eager_Numerator_Denominator():
    assert fe.Numerator((-a / b) ** 3) == (-a) ** 3
    assert fe.Numerator(S(3) / 2) == 3
    assert fe.Numerator(x / y) == x
    assert fe.Numerator(-S(1) / 2 + I / 3) == -3 + 2 * I
    assert fe.Denominator((-a / b) ** 3) == b ** 3
    assert fe.Denominator(S(3) / 2) == 2
    assert fe.Denominator(x / y) == y
    assert fe.Denominator(-S(1) / 2 + I / 3) == 6


def test_eager_Part():
    assert fe.Part([1, 2, 3], 1) == 1
    assert fe.Part(a * b, 1) == a
    assert fe.Util_Part(1, a + b).doit() == a
    assert fe.Util_Part(c, a + b).doit() == fe.Util_Part(c, a + b)   # symbolic index -> deferred


def test_eager_Apart():
    assert fe.Apart(1 / (x ** 2 * (a + b * x) ** 2), x) == (
        b ** 2 / (a ** 2 * (a + b * x) ** 2) + 1 / (a ** 2 * x ** 2)
        + 2 * b ** 2 / (a ** 3 * (a + b * x)) - 2 * b / (a ** 3 * x))
    # Non-rational: returned unchanged (matches Mathematica, guards SymPy's apart).
    assert fe.Apart(x ** (S(2) / 3) * (a + b * x) ** 2, x) == x ** (S(2) / 3) * (a + b * x) ** 2


def test_eager_Exponent_is_rational_function_faithful():
    assert fe.Exponent(x ** 3 + x + 1, x) == 3
    assert fe.Exponent(x ** 2 + 2 * x + 1, x) == 2
    assert fe.Exponent(S(1), x) == 0
    # Mathematica treats the argument as a rational function: Exponent[x^-3, x] == -3
    # (a polynomial-only implementation would wrongly return 0).
    assert fe.Exponent(x ** (-3), x) == -3


def test_eager_Simplify():
    assert fe.Simplify(sin(x) ** 2 + cos(x) ** 2) == 1
    assert fe.Simplify((x ** 3 + x ** 2 - x - 1) / (x ** 2 + 2 * x + 1)) == x - 1


def test_deferred_nodes_delegate_to_eager():
    assert mf.First(a + b + c).doit() == a
    assert mf.Rest(a * b * c).doit() == b * c
    assert mf.Part(sympy.Tuple(a, b, x), Integer(2)).doit() == b
    assert mf.Numerator((a + 1) / (b * x)).doit() == a + 1
    assert mf.Denominator((a + 1) / (b * x)).doit() == b * x
    assert mf.Apart(1 / (x * (x + 1)), x).doit() == 1 / x - 1 / (x + 1)
    assert mf.Exponent(a + b * x ** 3, x).doit() == 3


# ---------------------------------------------------------------------------
# 3. Backward-compat: rubi_utils re-exports the identical objects
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('name', MOVED_NODES + ['Sum'])
def test_rubi_utils_reexports_same_object(name):
    ru = importlib.import_module('rubi_rules.utils.rubi_utils')
    assert getattr(ru, name) is getattr(mf, name)


def test_gamma_deduplicated():
    """rubi_utils no longer defines its own Gamma; it uses sympy_wolfram's."""
    ru = importlib.import_module('rubi_rules.utils.rubi_utils')
    assert ru.Gamma.__module__ == 'sympy_wolfram.objects'
