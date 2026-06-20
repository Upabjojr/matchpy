# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.2 Cosine/4.2.2.3 (g cos)^p (a+b cos)^m (c+d cos)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.2 Cosine/4.2.2.3 (g cos)^p (a+b cos)^m (c+d cos)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, c, e, f = symbols('a c e f')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a*cos(e + f*x) + a)**2*sec(e + f*x)**2/(c*cos(e + f*x) - c),
        variable=x,
        num_steps=6,
        integral=-a**2*tan(e + f*x)/(c*f) - 3*a**2*atanh(sin(e + f*x))/(c*f) + 4*a**2*sin(e + f*x)/(c*f*(1 - cos(e + f*x))),
    ),
]
