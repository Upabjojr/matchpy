# -*- coding: utf-8 -*-
"""Tests for roundtrip conversion of all registered SymPy function heads."""
import pytest
import importlib
import sympy
from sympy import Symbol, S

from omnimatch import to_omnimatch_expression

from sympy_matching.conversion import omnimatch_to_sympy
from sympy_matching.operations import SYMPY_NODES


x = Symbol('x')
y = Symbol('y')


def _resolve(module_path, class_name):
    """Import a SymPy class by module path and name."""
    mod = importlib.import_module(module_path)
    return getattr(mod, class_name)


# ─── Build test cases from SYMPY_NODES ────────────────────────────────────────

_UNARY_CASES = []
_MULTI_ARG_CASES = []

for module_path, class_name, arity_code in SYMPY_NODES:
    try:
        func = _resolve(module_path, class_name)
    except (ImportError, AttributeError):
        continue
    if not isinstance(func, type):
        continue  # skip helper functions like sqrt

    name = class_name

    if arity_code == 'u':
        _UNARY_CASES.append(func)
    else:
        # Build appropriate test args for multi-arg functions
        if name == 'atan2':
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name == 'hyper':
            # TupleArg parameter lists are unwrapped by the conversion, so these
            # roundtrip exactly.
            _MULTI_ARG_CASES.append((func, ((S(1), S(2)), (S(3),), x)))
        elif name == 'meijerg':
            _MULTI_ARG_CASES.append((func, ((S(1),), (S(2),), (S(3),), (S(4),), x)))
        elif name == 'appellf1':
            _MULTI_ARG_CASES.append((func, (S(1), S(2), S(3), S(4), x, y)))
        elif name == 'polylog':
            _MULTI_ARG_CASES.append((func, (S(2), x)))
        elif name in ('elliptic_f', 'elliptic_e'):
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name == 'elliptic_pi':
            _MULTI_ARG_CASES.append((func, (x, y, S(1)/2)))
        elif name in ('Ei', 'li', 'Li', 'Si', 'Ci', 'Shi', 'Chi', 'fresnelc', 'fresnels'):
            _MULTI_ARG_CASES.append((func, (x,)))
        elif name == 'expint':
            _MULTI_ARG_CASES.append((func, (S(1), x)))
        elif name in ('polygamma', 'uppergamma', 'lowergamma'):
            _MULTI_ARG_CASES.append((func, (S(1), x)))
        elif name == 'LambertW':
            _MULTI_ARG_CASES.append((func, (x,)))
        elif name in ('Max', 'Min'):
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name == 'Piecewise':
            _MULTI_ARG_CASES.append(pytest.param(func, ((x, x > 0), (S(0), True)),
                                                  marks=pytest.mark.xfail(reason="Piecewise ExprCondPair roundtrip")))
        elif name in ('DiracDelta', 'Heaviside'):
            _MULTI_ARG_CASES.append((func, (x,)))
        elif name == 'KroneckerDelta':
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name == 'beta':
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name in ('zeta', 'lerchphi'):
            _MULTI_ARG_CASES.append((func, (S(2), x)))
        elif name in ('bernoulli', 'bell'):
            _MULTI_ARG_CASES.append((func, (S(3),)))
        elif name == 'erf2':
            _MULTI_ARG_CASES.append((func, (x, y)))
        elif name == 'binomial':
            _MULTI_ARG_CASES.append((func, (S(5), S(2))))
        elif name in ('RisingFactorial', 'FallingFactorial'):
            _MULTI_ARG_CASES.append((func, (x, S(3))))
        elif name in ('legendre', 'chebyshevt', 'chebyshevu', 'hermite', 'laguerre'):
            _MULTI_ARG_CASES.append((func, (S(3), x)))
        elif name in ('besselj', 'bessely', 'besseli', 'besselk',
                      'hankel1', 'hankel2', 'jn', 'yn'):
            _MULTI_ARG_CASES.append((func, (S(1), x)))
        else:
            # Default: try with (x, y)
            _MULTI_ARG_CASES.append((func, (x, y)))


@pytest.mark.parametrize("func", _UNARY_CASES, ids=lambda f: f.__name__)
def test_unary_roundtrip(func):
    """Each registered unary function should survive to_omnimatch_expression -> omnimatch_to_sympy roundtrip."""
    expr = func(x)
    mp_expr = to_omnimatch_expression(expr)
    result = omnimatch_to_sympy(mp_expr)
    assert result == expr, f"{func.__name__}: roundtrip gave {result}, expected {expr}"


@pytest.mark.parametrize("func,args", _MULTI_ARG_CASES,
                         ids=lambda f: f.__name__ if callable(f) else "")
def test_multi_arg_roundtrip(func, args):
    """Each registered multi-arg function should survive to_omnimatch_expression -> omnimatch_to_sympy roundtrip."""
    expr = func(*args)
    mp_expr = to_omnimatch_expression(expr)
    result = omnimatch_to_sympy(mp_expr)
    assert result == expr, f"{func.__name__}: roundtrip gave {result}, expected {expr}"
