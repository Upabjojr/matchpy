# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.1 Sine/4.1.8 (a+b sin)^m (c+d trig)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.1 Sine/4.1.8 (a+b sin)^m (c+d trig)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, a, b, c = symbols('A B a b c')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A + B*cos(x))/(a + b*sin(x)),
        variable=x,
        num_steps=7,
        integral=2*A*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) + B*log(a + b*sin(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(x))/(sin(x) + 1),
        variable=x,
        num_steps=5,
        integral=-A*cos(x)/(sin(x) + 1) + B*log(sin(x) + 1),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(x))/(1 - sin(x)),
        variable=x,
        num_steps=5,
        integral=A*cos(x)/(1 - sin(x)) - B*log(1 - sin(x)),
    ),
    RubiTestSuiteCase(
        integrand=(b + c + cos(x))/(a + b*sin(x)),
        variable=x,
        num_steps=7,
        integral=(2*b + 2*c)*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) + log(a + b*sin(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(b + c + cos(x))/(a - b*sin(x)),
        variable=x,
        num_steps=7,
        integral=-(2*b + 2*c)*atan((-a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) - log(a - b*sin(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*tan(x))/(a + b*sin(x)),
        variable=x,
        num_steps=8,
        integral=2*A*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) + B*a*log(a + b*sin(x))/(a**2 - b**2) - B*log(1 - sin(x))/(2*a + 2*b) - B*log(sin(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cot(x))/(a + b*sin(x)),
        variable=x,
        num_steps=9,
        integral=2*A*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) - B*log(a + b*sin(x))/a + B*log(sin(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(x))/(a + b*sin(x)),
        variable=x,
        num_steps=12,
        integral=2*A*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/sqrt(a**2 - b**2) - B*b*log(a + b*sin(x))/(a**2 - b**2) - B*log(1 - sin(x))/(2*a + 2*b) + B*log(sin(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*csc(x))/(a + b*sin(x)),
        variable=x,
        num_steps=6,
        integral=-B*atanh(cos(x))/a + (2*A*a - 2*B*b)*atan((a*tan(x/2) + b)/sqrt(a**2 - b**2))/(a*sqrt(a**2 - b**2)),
    ),
]
