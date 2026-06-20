# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.4 Cotangent/4.4.1.2 (d csc)^m (a+b cot)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.4 Cotangent/4.4.1.2 (d csc)^m (a+b cot)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, n = symbols('a b n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sin(x)**4/(cot(x) + I),
        variable=x,
        num_steps=4,
        integral=-5*I*x/16 + 3*I/(16*cot(x) + 16*I) - 3/(32*(cot(x) + I)**2) - I/(24*(cot(x) + I)**3) + 1/(32*(-cot(x) + I)**2) - I/(-8*cot(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(cot(x) + I),
        variable=x,
        num_steps=3,
        integral=-4*I*cos(x)**3/15 + 4*I*cos(x)/5 + I*sin(x)**3/(5*cot(x) + 5*I),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(cot(x) + I),
        variable=x,
        num_steps=4,
        integral=-3*I*x/8 + I/(4*cot(x) + 4*I) - 1/(8*(cot(x) + I)**2) - I/(-8*cot(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(cot(x) + I),
        variable=x,
        num_steps=2,
        integral=2*I*cos(x)/3 + I*sin(x)/(3*cot(x) + 3*I),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(cot(x) + I),
        variable=x,
        num_steps=1,
        integral=I*csc(x)/(cot(x) + I),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(cot(x) + I),
        variable=x,
        num_steps=2,
        integral=-I*x + log(sin(x)),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(cot(x) + I),
        variable=x,
        num_steps=2,
        integral=I*atanh(cos(x)) - csc(x),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**4/(cot(x) + I),
        variable=x,
        num_steps=2,
        integral=-cot(x)**2/2 + I*cot(x),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**5/(cot(x) + I),
        variable=x,
        num_steps=3,
        integral=I*cot(x)*csc(x)/2 + I*atanh(cos(x))/2 - csc(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**6/(cot(x) + I),
        variable=x,
        num_steps=3,
        integral=-cot(x)**4/4 + I*cot(x)**3/3 - cot(x)**2/2 + I*cot(x),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**7/(cot(x) + I),
        variable=x,
        num_steps=4,
        integral=I*cot(x)*csc(x)**3/4 + 3*I*cot(x)*csc(x)/8 + 3*I*atanh(cos(x))/8 - csc(x)**5/5,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**6/(a + b*cot(x)),
        variable=x,
        num_steps=3,
        integral=a*cot(x)**3/(3*b**2) + a*(a**2 + 2*b**2)*cot(x)/b**4 - cot(x)**4/(4*b) - (a**2 + 2*b**2)*cot(x)**2/(2*b**3) - (a**2 + b**2)**2*log(a + b*cot(x))/b**5,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**4/(a + b*cot(x)),
        variable=x,
        num_steps=3,
        integral=a*cot(x)/b**2 - cot(x)**2/(2*b) - (a**2 + b**2)*log(a + b*cot(x))/b**3,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a + b*cot(x)),
        variable=x,
        num_steps=2,
        integral=-log(a + b*cot(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(a + b*cot(x)),
        variable=x,
        num_steps=7,
        integral=a*x*(a**2 + 3*b**2)/(2*(a**2 + b**2)**2) - b**3*log(a*sin(x) + b*cos(x))/(a**2 + b**2)**2 - (a*cot(x) + b)*sin(x)**2/(2*a**2 + 2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**4/(a + b*cot(x)),
        variable=x,
        num_steps=8,
        integral=a*x*(3*a**4 + 10*a**2*b**2 + 15*b**4)/(8*(a**2 + b**2)**3) - b**5*log(a*sin(x) + b*cos(x))/(a**2 + b**2)**3 - (a*cot(x) + b)*sin(x)**4/(4*a**2 + 4*b**2) - (a*(3*a**2 + 7*b**2)*cot(x) + 4*b**3)*sin(x)**2/(8*(a**2 + b**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**5/(a + b*cot(x)),
        variable=x,
        num_steps=9,
        integral=a*cot(x)*csc(x)/(2*b**2) + a*atanh(cos(x))/(2*b**2) + a*(a**2 + b**2)*atanh(cos(x))/b**4 - csc(x)**3/(3*b) - (a**2 + b**2)*csc(x)/b**3 + (a**2 + b**2)**(sympy.S(3)/2)*atanh((-a*cot(x) + b)*sin(x)/sqrt(a**2 + b**2))/b**4,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(a + b*cot(x)),
        variable=x,
        num_steps=5,
        integral=a*atanh(cos(x))/b**2 - csc(x)/b + sqrt(a**2 + b**2)*atanh((-a*cot(x) + b)*sin(x)/sqrt(a**2 + b**2))/b**2,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(a + b*cot(x)),
        variable=x,
        num_steps=2,
        integral=-atanh((a*cot(x) - b)*sin(x)/sqrt(a**2 + b**2))/sqrt(a**2 + b**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(a + b*cot(x)),
        variable=x,
        num_steps=5,
        integral=-a*cos(x)/(a**2 + b**2) + b**2*atanh((-a*cot(x) + b)*sin(x)/sqrt(a**2 + b**2))/(a**2 + b**2)**(sympy.S(3)/2) - b*sin(x)/(a**2 + b**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(a + b*cot(x)),
        variable=x,
        num_steps=9,
        integral=-a*b**2*cos(x)/(a**2 + b**2)**2 + a*cos(x)**3/(3*a**2 + 3*b**2) - a*cos(x)/(a**2 + b**2) + b**4*atanh((-a*cot(x) + b)*sin(x)/sqrt(a**2 + b**2))/(a**2 + b**2)**(sympy.S(5)/2) - b**3*sin(x)/(a**2 + b**2)**2 - b*sin(x)**3/(3*a**2 + 3*b**2),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a + b*cot(x))**2,
        variable=x,
        num_steps=2,
        integral=1/(b*(a + b*cot(x))),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x))**n*csc(x)**2,
        variable=x,
        num_steps=2,
        integral=-(a + b*cot(x))**(n + 1)/(b*(n + 1)),
    ),
]
