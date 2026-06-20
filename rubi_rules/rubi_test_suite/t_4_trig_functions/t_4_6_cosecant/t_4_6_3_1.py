# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.6 Cosecant/4.6.3.1 (a+b csc)^m (d csc)^n (A+B csc).m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.6 Cosecant/4.6.3.1 (a+b csc)^m (d csc)^n (A+B csc).m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, a, c, d = symbols('A a c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=-2*A*a*cot(c + d*x)**3/(3*d) - A*a*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 7*A*a*cot(c + d*x)*csc(c + d*x)/(8*d) - 2*A*a*cot(c + d*x)/d - 7*A*a*atanh(cos(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x)**2,
        variable=x,
        num_steps=7,
        integral=-A*a*cot(c + d*x)*csc(c + d*x)**2/(3*d) - A*a*cot(c + d*x)*csc(c + d*x)/d - 5*A*a*cot(c + d*x)/(3*d) - A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x),
        variable=x,
        num_steps=6,
        integral=-A*a*cot(c + d*x)*csc(c + d*x)/(2*d) - 2*A*a*cot(c + d*x)/d - 3*A*a*atanh(cos(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*sin(c + d*x),
        variable=x,
        num_steps=5,
        integral=2*A*a*x - A*a*cos(c + d*x)/d - A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*sin(c + d*x)**2,
        variable=x,
        num_steps=5,
        integral=3*A*a*x/2 - A*a*sin(c + d*x)*cos(c + d*x)/(2*d) - 2*A*a*cos(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*sin(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=A*a*x - A*a*sin(c + d*x)*cos(c + d*x)/d + A*a*cos(c + d*x)**3/(3*d) - 2*A*a*cos(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x)**3,
        variable=x,
        num_steps=4,
        integral=A*a*cot(c + d*x)*csc(c + d*x)**3/(4*d) - A*a*cot(c + d*x)*csc(c + d*x)/(8*d) - A*a*atanh(cos(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=A*a*cot(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x),
        variable=x,
        num_steps=3,
        integral=A*a*cot(c + d*x)*csc(c + d*x)/(2*d) - A*a*atanh(cos(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*sin(c + d*x),
        variable=x,
        num_steps=4,
        integral=-A*a*cos(c + d*x)/d + A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*sin(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-A*a*x/2 - A*a*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*sin(c + d*x)**3,
        variable=x,
        num_steps=3,
        integral=A*a*cos(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x)**3,
        variable=x,
        num_steps=4,
        integral=A*a*cot(c + d*x)*csc(c + d*x)**3/(4*d) - A*a*cot(c + d*x)*csc(c + d*x)/(8*d) - A*a*atanh(cos(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=A*a*cot(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)*csc(c + d*x),
        variable=x,
        num_steps=3,
        integral=A*a*cot(c + d*x)*csc(c + d*x)/(2*d) - A*a*atanh(cos(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)/csc(c + d*x),
        variable=x,
        num_steps=4,
        integral=-A*a*cos(c + d*x)/d + A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)/csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-A*a*x/2 - A*a*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(a*csc(c + d*x) + a)/csc(c + d*x)**3,
        variable=x,
        num_steps=3,
        integral=A*a*cos(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=2*A*a*cot(c + d*x)**3/(3*d) - A*a*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 7*A*a*cot(c + d*x)*csc(c + d*x)/(8*d) + 2*A*a*cot(c + d*x)/d - 7*A*a*atanh(cos(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x)**2,
        variable=x,
        num_steps=7,
        integral=-A*a*cot(c + d*x)*csc(c + d*x)**2/(3*d) + A*a*cot(c + d*x)*csc(c + d*x)/d - 5*A*a*cot(c + d*x)/(3*d) + A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)*csc(c + d*x),
        variable=x,
        num_steps=6,
        integral=-A*a*cot(c + d*x)*csc(c + d*x)/(2*d) + 2*A*a*cot(c + d*x)/d - 3*A*a*atanh(cos(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)/csc(c + d*x),
        variable=x,
        num_steps=5,
        integral=-2*A*a*x - A*a*cos(c + d*x)/d - A*a*atanh(cos(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)/csc(c + d*x)**2,
        variable=x,
        num_steps=5,
        integral=3*A*a*x/2 - A*a*sin(c + d*x)*cos(c + d*x)/(2*d) + 2*A*a*cos(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(-A*csc(c + d*x) + A)*(-a*csc(c + d*x) + a)/csc(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=-A*a*x + A*a*sin(c + d*x)*cos(c + d*x)/d + A*a*cos(c + d*x)**3/(3*d) - 2*A*a*cos(c + d*x)/d,
    ),
]
