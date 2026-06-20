# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.6 Cosecant/4.6.4.2 (a+b csc)^m (d csc)^n (A+B csc+C csc^2).m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.6 Cosecant/4.6.4.2 (a+b csc)^m (d csc)^n (A+B csc+C csc^2).m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, C, a, b = symbols('A B C a b')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a + b*csc(x))*(A + B*csc(x) + C*csc(x)**2)/sqrt(csc(x)),
        variable=x,
        num_steps=7,
        integral=-2*C*b*cos(x)*csc(x)**(sympy.S(3)/2)/3 + (-2*B*b - 2*C*a)*cos(x)*sqrt(csc(x)) - (2*B*b - 2*a*(A - C))*sqrt(sin(x))*sqrt(csc(x))*elliptic_e(x/2 - pi/4, 2) + (2*A*b + 2*B*a + 2*C*b/3)*sqrt(sin(x))*sqrt(csc(x))*elliptic_f(x/2 - pi/4, 2),
    ),
]
