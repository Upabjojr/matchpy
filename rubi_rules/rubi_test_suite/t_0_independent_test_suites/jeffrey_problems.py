# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Jeffrey Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Jeffrey Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
p, q, r = symbols('p q r')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=3/(5 - 4*cos(x)),
        variable=x,
        num_steps=2,
        integral=x + 2*atan(sin(x)/(2 - cos(x))),
    ),
    RubiTestSuiteCase(
        integrand=(2*sin(x) + cos(x) + 1)/(-2*sin(x)*cos(x) + 2*sin(x) + cos(x)**2 + 3),
        variable=x,
        num_steps=-43,
        integral=-atan((-sin(x) + 2*cos(x))/(sin(x) + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(5*sin(x) + cos(x) + 2)/(-2*sin(x)**2 + sin(x)*cos(x) - 2*sin(x) + 4*cos(x)),
        variable=x,
        num_steps=-25,
        integral=-log(sin(x) - 3*cos(x) + 1) + log(sin(x) + cos(x) + 3),
    ),
    RubiTestSuiteCase(
        integrand=(2*sin(x) + 7*cos(x) + 3)/(-sin(x)*cos(x) - 5*sin(x) + 3*cos(x)**2 + 4*cos(x) + 1),
        variable=x,
        num_steps=-32,
        integral=-log(-2*sin(x) + cos(x) + 1) + log(sin(x) + cos(x) + 3),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(x)**2 + 4*cos(x) - 1)/(4*cos(x)**3 - 3*cos(x)**2 - 4*cos(x) - 1),
        variable=x,
        num_steps=-2,
        integral=x - 2*atan((7*sin(x)*cos(x) + 3*sin(x))/(5*cos(x)**2 + 2*cos(x) + 1)) - 2*atan(sin(x)/(cos(x) + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(7*cos(x)**2 + 2*cos(x) - 5)/(4*cos(x)**3 - 9*cos(x)**2 + 2*cos(x) - 1),
        variable=x,
        num_steps=-2,
        integral=x - 2*atan(2*sin(x)*cos(x)/(2*cos(x)**2 - cos(x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=3/(4*sin(x) + 5),
        variable=x,
        num_steps=2,
        integral=x + 2*atan(cos(x)/(sin(x) + 2)),
    ),
    RubiTestSuiteCase(
        integrand=2/(cos(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*x - sqrt(2)*atan(sin(x)*cos(x)/(cos(x)**2 + 1 + sqrt(2))),
    ),
    RubiTestSuiteCase(
        integrand=1/(p + q*cos(x) + r*sin(x)),
        variable=x,
        num_steps=3,
        integral=2*atan((r + (p - q)*tan(x/2))/sqrt(p**2 - q**2 - r**2))/sqrt(p**2 - q**2 - r**2),
    ),
]
