# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Bronstein Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Bronstein Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sqrt(x**8 + 1)*(2*x**8 + 1)/(x**17 + 2*x**9 + x),
        variable=x,
        num_steps=6,
        integral=-atanh(sqrt(x**8 + 1))/4 - 1/(4*sqrt(x**8 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=1/(x**2 + 1),
        variable=x,
        num_steps=1,
        integral=atan(x),
    ),
    RubiTestSuiteCase(
        integrand=1/(x*sqrt(x**8 + 1)),
        variable=x,
        num_steps=3,
        integral=-atanh(sqrt(x**8 + 1))/4,
    ),
    RubiTestSuiteCase(
        integrand=x/sqrt(1 - x**3),
        variable=x,
        num_steps=3,
        integral=2*sqrt(1 - x**3)/(-x + 1 + sqrt(3)) - 3**(sympy.S(1)/4)*sqrt((x**2 + x + 1)/(-x + 1 + sqrt(3))**2)*(1 - x)*sqrt(2 - sqrt(3))*elliptic_e(asin((-x - sqrt(3) + 1)/(-x + 1 + sqrt(3))), -7 - 4*sqrt(3))/(sqrt((1 - x)/(-x + 1 + sqrt(3))**2)*sqrt(1 - x**3)) + 2*sqrt(2)*3**(sympy.S(3)/4)*sqrt((x**2 + x + 1)/(-x + 1 + sqrt(3))**2)*(1 - x)*elliptic_f(asin((-x - sqrt(3) + 1)/(-x + 1 + sqrt(3))), -7 - 4*sqrt(3))/(3*sqrt((1 - x)/(-x + 1 + sqrt(3))**2)*sqrt(1 - x**3)),
    ),
    RubiTestSuiteCase(
        integrand=1/(x*sqrt(1 - x**3)),
        variable=x,
        num_steps=3,
        integral=-2*atanh(sqrt(1 - x**3))/3,
    ),
    RubiTestSuiteCase(
        integrand=x/sqrt(x**4 + 10*x**2 - 96*x - 71),
        variable=x,
        num_steps=1,
        integral=log(x**8 + 20*x**6 - 128*x**5 + 54*x**4 - 1408*x**3 + 3124*x**2 + sqrt(x**4 + 10*x**2 - 96*x - 71)*(x**6 + 15*x**4 - 80*x**3 + 27*x**2 - 528*x + 781) + 10001)/8,
    ),
    RubiTestSuiteCase(
        integrand=(x - tan(x))/tan(x)**2,
        variable=x,
        num_steps=6,
        integral=-x**2/2 - x*cot(x),
    ),
    RubiTestSuiteCase(
        integrand=x*tan(x) + tan(x)**2 + 1,
        variable=x,
        num_steps=7,
        integral=(((sympy.I * (x)**(Integer(2))) * (Integer(2))**(Integer(-1))) + (Integer(-1) * (x * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.I * x)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.I * x))))) + sympy.tan(x)),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/x,
        variable=x,
        num_steps=1,
        integral=sympy.Function('SinIntegral')(x),
    ),
    RubiTestSuiteCase(
        integrand=(5*x**2 + 3*(x + exp(x))**(sympy.S(1)/3) + (2*x**2 + 3*x)*exp(x))/(x*(x + exp(x))**(sympy.S(1)/3)),
        variable=x,
        num_steps=8,
        integral=3*x*(x + exp(x))**(sympy.S(2)/3) + 3*log(x),
    ),
    RubiTestSuiteCase(
        integrand=(1 + 1/x)/(x + log(x))**(sympy.S(3)/2) + 1/x,
        variable=x,
        num_steps=2,
        integral=log(x) - 2/sqrt(x + log(x)),
    ),
    RubiTestSuiteCase(
        integrand=(x**2 + 2*x*log(x) + (x + 1)*sqrt(x + log(x)) + log(x)**2)/(x**3 + 2*x**2*log(x) + x*log(x)**2),
        variable=x,
        num_steps=-3,
        integral=log(x) - 2/sqrt(x + log(x)),
    ),
    RubiTestSuiteCase(
        integrand=(-x**2 + 2*log(x)**2 - log(x))/(-x**2*log(x) + log(x)**3),
        variable=x,
        num_steps=6,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.log((x + (Integer(-1) * sympy.log(x))))) + ((Integer(2))**(Integer(-1)) * sympy.log((x + sympy.log(x)))) + sympy.Function('LogIntegral')(x)),
    ),
    RubiTestSuiteCase(
        integrand=(x**4 - 3*x**2 + 6)/(x**6 - 5*x**4 + 5*x**2 + 4),
        variable=x,
        num_steps=1,
        integral=atan(x*(x**4 - 3*x**2 + 1)/2) + atan(2*x - sqrt(3)) + atan(2*x + sqrt(3)),
    ),
]
