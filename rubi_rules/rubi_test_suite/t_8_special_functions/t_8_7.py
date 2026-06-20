# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 8 Special functions/8.7 Zeta function.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '8 Special functions/8.7 Zeta function.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, s = symbols('a b s')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=((x)**(Integer(2)) * sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=4,
        integral=((Integer(-1) * ((Integer(2) * x * sympy.Function('LogGamma')((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((Integer(2) * sympy.Function('PolyGamma')(Integer(-2), (Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (((x)**(Integer(2)) * sympy.Function('PolyGamma')(Integer(0), (Symbol('a') + (Symbol('b') * x)))) * (Symbol('b'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((x)**(Integer(1)) * sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=3,
        integral=((Integer(-1) * (sympy.Function('LogGamma')((Symbol('a') + (Symbol('b') * x))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((x * sympy.Function('PolyGamma')(Integer(0), (Symbol('a') + (Symbol('b') * x)))) * (Symbol('b'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((x)**(Integer(0)) * sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=2,
        integral=(sympy.Function('PolyGamma')(Integer(0), (Symbol('a') + (Symbol('b') * x))) * (Symbol('b'))**(Integer(-1))),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(1)))**(Integer(-1))),
        variable=x,
        num_steps=1,
        integral=sympy.Function('Unintegrable')((sympy.Function('PolyGamma')(Integer(1), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(2)))**(Integer(-1))),
        variable=x,
        num_steps=2,
        integral=((Symbol('b') * sympy.Function('Unintegrable')((sympy.Function('PolyGamma')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x)) + (Integer(-1) * (sympy.Function('PolyGamma')(Integer(1), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(3)))**(Integer(-1))),
        variable=x,
        num_steps=3,
        integral=(((Integer(2))**(Integer(-1)) * (Symbol('b'))**(Integer(2)) * sympy.Function('Unintegrable')((sympy.Function('PolyGamma')(Integer(3), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x)) + (Integer(-1) * (sympy.Function('PolyGamma')(Integer(1), (Symbol('a') + (Symbol('b') * x))) * ((Integer(2) * (x)**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * sympy.Function('PolyGamma')(Integer(2), (Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * x))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=((sympy.Function('Zeta')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(2)))**(Integer(-1))) + (Integer(-1) * (Symbol('b') * (sympy.Function('PolyGamma')(Integer(2), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1)))))),
        variable=x,
        num_steps=3,
        integral=(Integer(-1) * (sympy.Function('PolyGamma')(Integer(1), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((x)**(Integer(2)) * sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=3,
        integral=(((Integer(2) * sympy.Function('Zeta')((Integer(-3) + Symbol('s')), (Symbol('a') + (Symbol('b') * x)))) * (((Symbol('b'))**(Integer(3)) * (Integer(1) + (Integer(-1) * Symbol('s'))) * (Integer(2) + (Integer(-1) * Symbol('s'))) * (Integer(3) + (Integer(-1) * Symbol('s')))))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * x * sympy.Function('Zeta')((Integer(-2) + Symbol('s')), (Symbol('a') + (Symbol('b') * x)))) * (((Symbol('b'))**(Integer(2)) * (Integer(1) + (Integer(-1) * Symbol('s'))) * (Integer(2) + (Integer(-1) * Symbol('s')))))**(Integer(-1)))) + (((x)**(Integer(2)) * sympy.Function('Zeta')((Integer(-1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b') * (Integer(1) + (Integer(-1) * Symbol('s')))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((x)**(Integer(1)) * sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=2,
        integral=((Integer(-1) * (sympy.Function('Zeta')((Integer(-2) + Symbol('s')), (Symbol('a') + (Symbol('b') * x))) * (((Symbol('b'))**(Integer(2)) * (Integer(1) + (Integer(-1) * Symbol('s'))) * (Integer(2) + (Integer(-1) * Symbol('s')))))**(Integer(-1)))) + ((x * sympy.Function('Zeta')((Integer(-1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b') * (Integer(1) + (Integer(-1) * Symbol('s')))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((x)**(Integer(0)) * sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x)))),
        variable=x,
        num_steps=1,
        integral=(sympy.Function('Zeta')((Integer(-1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x))) * ((Symbol('b') * (Integer(1) + (Integer(-1) * Symbol('s')))))**(Integer(-1))),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(1)))**(Integer(-1))),
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')((sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(2)))**(Integer(-1))),
        variable=x,
        num_steps=1,
        integral=(((Integer(-1) * Symbol('b')) * Symbol('s') * sympy.Function('CannotIntegrate')((sympy.Function('Zeta')((Integer(1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x)) + (Integer(-1) * (sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(3)))**(Integer(-1))),
        variable=x,
        num_steps=2,
        integral=(((Integer(2))**(Integer(-1)) * (Symbol('b'))**(Integer(2)) * Symbol('s') * (Integer(1) + Symbol('s')) * sympy.Function('CannotIntegrate')((sympy.Function('Zeta')((Integer(2) + Symbol('s')), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))), x)) + (Integer(-1) * (sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * ((Integer(2) * (x)**(Integer(2))))**(Integer(-1)))) + ((Symbol('b') * Symbol('s') * sympy.Function('Zeta')((Integer(1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * x))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=((sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * ((x)**(Integer(2)))**(Integer(-1))) + (Symbol('b') * Symbol('s') * (sympy.Function('Zeta')((Integer(1) + Symbol('s')), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1))))),
        variable=x,
        num_steps=2,
        integral=(Integer(-1) * (sympy.Function('Zeta')(Symbol('s'), (Symbol('a') + (Symbol('b') * x))) * (x)**(Integer(-1)))),
    ),
]
