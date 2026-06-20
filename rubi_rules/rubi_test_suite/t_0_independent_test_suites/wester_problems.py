# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Wester Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Wester Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, m = symbols('a b m')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(3*x - 5)**2/(2*x - 1)**(sympy.S(7)/2),
        variable=x,
        num_steps=2,
        integral=-9/(4*sqrt(2*x - 1)) + 7/(2*(2*x - 1)**(sympy.S(3)/2)) - 49/(20*(2*x - 1)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=1/(2*exp(m*x) - 5*exp(-m*x)),
        variable=x,
        num_steps=2,
        integral=-sqrt(10)*atanh(sqrt(10)*exp(m*x)/5)/(10*m),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cos(x)),
        variable=x,
        num_steps=2,
        integral=2*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=1/(4*sin(x) + 3*cos(x) + 3),
        variable=x,
        num_steps=2,
        integral=log(4*tan(x/2) + 3)/4,
    ),
    RubiTestSuiteCase(
        integrand=1/(4*sin(x) + 3*cos(x) + 4),
        variable=x,
        num_steps=2,
        integral=-log(3*cot(x/2 + pi/4) + 4)/3,
    ),
    RubiTestSuiteCase(
        integrand=1/(4*sin(x) + 3*cos(x) + 6),
        variable=x,
        num_steps=3,
        integral=sqrt(11)*x/11 + 2*sqrt(11)*atan((-3*sin(x) + 4*cos(x))/(4*sin(x) + 3*cos(x) + sqrt(11) + 6))/11,
    ),
    RubiTestSuiteCase(
        integrand=log((-a**2 + x**2)**2)/2,
        variable=x,
        num_steps=4,
        integral=2*a*atanh(x/a) + x*log((-a**2 + x**2)**2)/2 - 2*x,
    ),
]
