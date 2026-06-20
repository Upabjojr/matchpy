# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.4 Cotangent/4.4.1.3 (d cos)^m (a+b cot)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.4 Cotangent/4.4.1.3 (d cos)^m (a+b cot)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b = symbols('a b')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=cos(x)**4/(cot(x) + I),
        variable=x,
        num_steps=5,
        integral=-I*x/16 + 3*I/(16*cot(x) + 16*I) + 5/(32*(cot(x) + I)**2) - I/(24*(cot(x) + I)**3) + 1/(32*(-cot(x) + I)**2) + I/(-8*cot(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(cot(x) + I),
        variable=x,
        num_steps=9,
        integral=I*sin(x)**5/5 - I*sin(x)**3/3 - cos(x)**5/5,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(cot(x) + I),
        variable=x,
        num_steps=5,
        integral=-I*x/8 + I/(4*cot(x) + 4*I) + 1/(8*(cot(x) + I)**2) + I/(-8*cot(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(cot(x) + I),
        variable=x,
        num_steps=8,
        integral=-I*sin(x)**3/3 - cos(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(cot(x) + I),
        variable=x,
        num_steps=8,
        integral=I*sin(x) - cos(x) - I*atanh(sin(x)),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(cot(x) + I),
        variable=x,
        num_steps=3,
        integral=I*x - log(sin(x)) + log(tan(x)) - I*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(cot(x) + I),
        variable=x,
        num_steps=8,
        integral=-I*tan(x)*sec(x)/2 + I*atanh(sin(x))/2 + sec(x),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**4/(cot(x) + I),
        variable=x,
        num_steps=4,
        integral=-I*tan(x)**3/3 + tan(x)**2/2,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**5/(cot(x) + I),
        variable=x,
        num_steps=9,
        integral=-I*tan(x)*sec(x)**3/4 + I*tan(x)*sec(x)/8 + I*atanh(sin(x))/8 + sec(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**6/(cot(x) + I),
        variable=x,
        num_steps=4,
        integral=-I*tan(x)**5/5 + tan(x)**4/4 - I*tan(x)**3/3 + tan(x)**2/2,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**4/(a + b*cot(x)),
        variable=x,
        num_steps=8,
        integral=-a**4*b*log(a*sin(x) + b*cos(x))/(a**2 + b**2)**3 + a*x*(3*a**4 - 6*a**2*b**2 - b**4)/(8*(a**2 + b**2)**3) - (a*cot(x) + b)*sin(x)**4/(4*a**2 + 4*b**2) + (a*(5*a**2 + b**2)*cot(x) + 4*b*(2*a**2 + b**2))*sin(x)**2/(8*(a**2 + b**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(a + b*cot(x)),
        variable=x,
        num_steps=10,
        integral=a**3*b*atanh((a*cos(x) - b*sin(x))/sqrt(a**2 + b**2))/(a**2 + b**2)**(sympy.S(5)/2) - a**2*b*cos(x)/(a**2 + b**2)**2 - a*b**2*sin(x)/(a**2 + b**2)**2 - a*sin(x)**3/(3*a**2 + 3*b**2) + a*sin(x)/(a**2 + b**2) - b*cos(x)**3/(3*a**2 + 3*b**2),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(a + b*cot(x)),
        variable=x,
        num_steps=7,
        integral=-a**2*b*log(a*sin(x) + b*cos(x))/(a**2 + b**2)**2 + a*x*(a**2 - b**2)/(2*(a**2 + b**2)**2) + (a*cot(x) + b)*sin(x)**2/(2*a**2 + 2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(a + b*cot(x)),
        variable=x,
        num_steps=6,
        integral=a*b*atanh((a*cos(x) - b*sin(x))/sqrt(a**2 + b**2))/(a**2 + b**2)**(sympy.S(3)/2) + a*sin(x)/(a**2 + b**2) - b*cos(x)/(a**2 + b**2),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(a + b*cot(x)),
        variable=x,
        num_steps=6,
        integral=b*atanh((a*cos(x) - b*sin(x))/sqrt(a**2 + b**2))/(a*sqrt(a**2 + b**2)) + atanh(sin(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(a + b*cot(x)),
        variable=x,
        num_steps=3,
        integral=tan(x)/a - b*log(a + b*cot(x))/a**2 - b*log(tan(x))/a**2,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(a + b*cot(x)),
        variable=x,
        num_steps=9,
        integral=tan(x)*sec(x)/(2*a) + atanh(sin(x))/(2*a) - b*sec(x)/a**2 + b**2*atanh(sin(x))/a**3 + b*sqrt(a**2 + b**2)*atanh((a*cos(x) - b*sin(x))/sqrt(a**2 + b**2))/a**3,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**4/(a + b*cot(x)),
        variable=x,
        num_steps=3,
        integral=tan(x)**3/(3*a) - b*tan(x)**2/(2*a**2) + (a**2 + b**2)*tan(x)/a**3 - b*(a**2 + b**2)*log(a + b*cot(x))/a**4 - b*(a**2 + b**2)*log(tan(x))/a**4,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(2*cot(x) + 1),
        variable=x,
        num_steps=6,
        integral=2*sqrt(5)*atanh(sqrt(5)*(-2*sin(x) + cos(x))/5)/5 + atanh(sin(x)),
    ),
]
