# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.6 Cosecant/4.6.1.3 (d cos)^n (a+b csc)^m.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.6 Cosecant/4.6.1.3 (d cos)^n (a+b csc)^m.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b = symbols('a b')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=cos(x)**4/(a*csc(x) + a),
        variable=x,
        num_steps=7,
        integral=-x/(8*a) + sin(x)*cos(x)**3/(4*a) - sin(x)*cos(x)/(8*a) - cos(x)**3/(3*a),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=-sin(x)**3/(3*a) + sin(x)**2/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(a*csc(x) + a),
        variable=x,
        num_steps=5,
        integral=-x/(2*a) + sin(x)*cos(x)/(2*a) - cos(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(a*csc(x) + a),
        variable=x,
        num_steps=5,
        integral=-log(sin(x) + 1)/a + sin(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=-tan(x)*sec(x)/(2*a) + atanh(sin(x))/(2*a) + sec(x)**2/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=-tan(x)**3/(3*a) + sec(x)**3/(3*a),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(a*csc(x) + a),
        variable=x,
        num_steps=7,
        integral=-tan(x)*sec(x)**3/(4*a) + tan(x)*sec(x)/(8*a) + atanh(sin(x))/(8*a) + sec(x)**4/(4*a),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**4/(a*csc(x) + a),
        variable=x,
        num_steps=7,
        integral=-tan(x)**5/(5*a) - tan(x)**3/(3*a) + sec(x)**5/(5*a),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**4/(a + b*csc(x)),
        variable=x,
        num_steps=7,
        integral=-(-3*a*sin(x) + 4*b)*cos(x)**3/(12*a**2) - (-a*(3*a**2 - 4*b**2)*sin(x) + 8*b*(a**2 - b**2))*cos(x)/(8*a**4) + 2*b*(a**2 - b**2)**(sympy.S(3)/2)*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/a**5 + x*(3*a**4 - 12*a**2*b**2 + 8*b**4)/(8*a**5),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(a + b*csc(x)),
        variable=x,
        num_steps=5,
        integral=-sin(x)**3/(3*a) + b*sin(x)**2/(2*a**2) + (a**2 - b**2)*sin(x)/a**3 - b*(a**2 - b**2)*log(a*sin(x) + b)/a**4,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(a + b*csc(x)),
        variable=x,
        num_steps=6,
        integral=-(-a*sin(x) + 2*b)*cos(x)/(2*a**2) + 2*b*sqrt(a**2 - b**2)*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/a**3 + x*(a**2 - 2*b**2)/(2*a**3),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(a + b*csc(x)),
        variable=x,
        num_steps=5,
        integral=sin(x)/a - b*log(a*sin(x) + b)/a**2,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(a + b*csc(x)),
        variable=x,
        num_steps=4,
        integral=-b*log(a*sin(x) + b)/(a**2 - b**2) - log(1 - sin(x))/(2*a + 2*b) + log(sin(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(a + b*csc(x)),
        variable=x,
        num_steps=6,
        integral=2*a*b*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**2 - b**2)**(sympy.S(3)/2) - (-a*sin(x) + b)*sec(x)/(a**2 - b**2),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(a + b*csc(x)),
        variable=x,
        num_steps=6,
        integral=-a**2*b*log(a*sin(x) + b)/(a**2 - b**2)**2 - a*log(1 - sin(x))/(4*(a + b)**2) + a*log(sin(x) + 1)/(4*(a - b)**2) - (-a*sin(x) + b)*sec(x)**2/(2*a**2 - 2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**4/(a + b*csc(x)),
        variable=x,
        num_steps=7,
        integral=2*a**3*b*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**2 - b**2)**(sympy.S(5)/2) - (-a*sin(x) + b)*sec(x)**3/(3*a**2 - 3*b**2) - (3*a**2*b - a*(2*a**2 + b**2)*sin(x))*sec(x)/(3*(a**2 - b**2)**2),
    ),
]
