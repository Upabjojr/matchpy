# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Hebisch Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Hebisch Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(x**6 - x**5 + x**4 - x**3 + 1)*exp(x),
        variable=x,
        num_steps=25,
        integral=x**6*exp(x) - 7*x**5*exp(x) + 36*x**4*exp(x) - 145*x**3*exp(x) + 435*x**2*exp(x) - 870*x*exp(x) + 871*exp(x),
    ),
    RubiTestSuiteCase(
        integrand=(2 - x**2)*exp(x/(x**2 + 2))/(x**3 + 2*x),
        variable=x,
        num_steps=-5,
        integral=sympy.Function('ExpIntegralEi')((x * ((Integer(2) + (x)**(Integer(2))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(2*x**4 - x**3 + 3*x**2 + 2*x + 2)*exp(x/(x**2 + 2))/(x**3 + 2*x),
        variable=x,
        num_steps=-5,
        integral=(((sympy.E)**((x * ((Integer(2) + (x)**(Integer(2))))**(Integer(-1)))) * (Integer(2) + (x)**(Integer(2)))) + sympy.Function('ExpIntegralEi')((x * ((Integer(2) + (x)**(Integer(2))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(exp(x) + 1)*exp(x + exp(x))/(x + exp(x)),
        variable=x,
        num_steps=2,
        integral=sympy.Function('ExpIntegralEi')(((sympy.E)**(x) + x)),
    ),
    RubiTestSuiteCase(
        integrand=(x**3 - x**2 - 3*x + 1)*exp(1/(x**2 - 1))/(x**3 - x**2 - x + 1),
        variable=x,
        num_steps=-6,
        integral=(x + 1)*exp(1/(x**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=(log(x)**2 - 1)*exp(1 + 1/log(x))/log(x)**2,
        variable=x,
        num_steps=1,
        integral=x*exp(1 + 1/log(x)),
    ),
    RubiTestSuiteCase(
        integrand=((x + 1)*log(x)**2 - 1)*exp(x + 1/log(x))/log(x)**2,
        variable=x,
        num_steps=-2,
        integral=x*exp(x + 1/log(x)),
    ),
]
