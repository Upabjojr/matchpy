# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Charlwood Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Charlwood Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=x*asin(x)/sqrt(1 - x**2),
        variable=x,
        num_steps=2,
        integral=x - sqrt(1 - x**2)*asin(x),
    ),
    RubiTestSuiteCase(
        integrand=-asin(sqrt(x) - sqrt(x + 1)),
        variable=x,
        num_steps=-3,
        integral=sqrt(2)*(sqrt(x) + 3*sqrt(x + 1))*sqrt(sqrt(x)*sqrt(x + 1) - x)/8 - (x + sympy.S(3)/8)*asin(sqrt(x) - sqrt(x + 1)),
    ),
    RubiTestSuiteCase(
        integrand=log(x*sqrt(x**2 + 1) + 1),
        variable=x,
        num_steps=-32,
        integral=x*log(x*sqrt(x**2 + 1) + 1) - 2*x + sqrt(2 + 2*sqrt(5))*atan(sqrt(-2 + sqrt(5))*(x + sqrt(x**2 + 1))) - sqrt(-2 + 2*sqrt(5))*atanh(sqrt(2 + sqrt(5))*(x + sqrt(x**2 + 1))),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/sqrt(cos(x)**4 + cos(x)**2 + 1),
        variable=x,
        num_steps=-5,
        integral=x/3 + atan((cos(x)**2 + 1)*sin(x)*cos(x)/(sqrt(cos(x)**4 + cos(x)**2 + 1)*cos(x)**2 + 1))/3,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(tan(x)**4 + 1)*tan(x),
        variable=x,
        num_steps=7,
        integral=sqrt(tan(x)**4 + 1)/2 - asinh(tan(x)**2)/2 - sqrt(2)*atanh(sqrt(2)*(1 - tan(x)**2)/(2*sqrt(tan(x)**4 + 1)))/2,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/sqrt(sec(x)**3 + 1),
        variable=x,
        num_steps=4,
        integral=-2*atanh(sqrt(sec(x)**3 + 1))/3,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(tan(x)**2 + 2*tan(x) + 2),
        variable=x,
        num_steps=9,
        integral=asinh(tan(x) + 1) - sqrt(sympy.S.Half + sqrt(5)/2)*atan((-(sqrt(5) + 5)*tan(x) + 2*sqrt(5))/(sqrt(10 + 10*sqrt(5))*sqrt(tan(x)**2 + 2*tan(x) + 2))) - sqrt(sympy.S(-1)/2 + sqrt(5)/2)*atanh(((5 - sqrt(5))*tan(x) + 2*sqrt(5))/(sqrt(-10 + 10*sqrt(5))*sqrt(tan(x)**2 + 2*tan(x) + 2))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)*atan(sqrt(sec(x) - 1)),
        variable=x,
        num_steps=7,
        integral=sqrt(sec(x) - 1)*cos(x)/2 - cos(x)*atan(sqrt(sec(x) - 1)) + atan(sqrt(sec(x) - 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=x*log(x + sqrt(x**2 + 1))*log(x**2 + 1)/sqrt(x**2 + 1),
        variable=x,
        num_steps=7,
        integral=-x*log(x**2 + 1) + 4*x + sqrt(x**2 + 1)*log(x + sqrt(x**2 + 1))*log(x**2 + 1) - 2*sqrt(x**2 + 1)*log(x + sqrt(x**2 + 1)) - 2*atan(x),
    ),
    RubiTestSuiteCase(
        integrand=atan(x + sqrt(1 - x**2)),
        variable=x,
        num_steps=-40,
        integral=x*atan(x + sqrt(1 - x**2)) - log(x**4 - x**2 + 1)/8 - asin(x)/2 - sqrt(3)*atan(sqrt(3)*(2*x**2 - 1)/3)/4 + sqrt(3)*atan((sqrt(3)*x - 1)/sqrt(1 - x**2))/4 + sqrt(3)*atan((sqrt(3)*x + 1)/sqrt(1 - x**2))/4 - atanh(x*sqrt(1 - x**2))/4,
    ),
    RubiTestSuiteCase(
        integrand=x*atan(x + sqrt(1 - x**2))/sqrt(1 - x**2),
        variable=x,
        num_steps=-32,
        integral=-sqrt(1 - x**2)*atan(x + sqrt(1 - x**2)) + log(x**4 - x**2 + 1)/8 - asin(x)/2 - sqrt(3)*atan(sqrt(3)*(2*x**2 - 1)/3)/4 + sqrt(3)*atan((sqrt(3)*x - 1)/sqrt(1 - x**2))/4 + sqrt(3)*atan((sqrt(3)*x + 1)/sqrt(1 - x**2))/4 + atanh(x*sqrt(1 - x**2))/4,
    ),
    RubiTestSuiteCase(
        integrand=log(x + sqrt(x**2 + 1))/(1 - x**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=3,
        integral=x*log(x + sqrt(x**2 + 1))/sqrt(1 - x**2) - asin(x**2)/2,
    ),
    RubiTestSuiteCase(
        integrand=asin(x)/(x**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=3,
        integral=x*asin(x)/sqrt(x**2 + 1) - asin(x**2)/2,
    ),
    RubiTestSuiteCase(
        integrand=log(x + sqrt(x**2 - 1))/(x**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=3,
        integral=x*log(x + sqrt(x**2 - 1))/sqrt(x**2 + 1) - acosh(x**2)/2,
    ),
    RubiTestSuiteCase(
        integrand=log(x)/(x**2*sqrt(x**2 - 1)),
        variable=x,
        num_steps=4,
        integral=-atanh(x/sqrt(x**2 - 1)) + sqrt(x**2 - 1)*log(x)/x + sqrt(x**2 - 1)/x,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x**3 + 1)/x,
        variable=x,
        num_steps=4,
        integral=2*sqrt(x**3 + 1)/3 - 2*atanh(sqrt(x**3 + 1))/3,
    ),
    RubiTestSuiteCase(
        integrand=x*log(x + sqrt(x**2 - 1))/sqrt(x**2 - 1),
        variable=x,
        num_steps=2,
        integral=-x + sqrt(x**2 - 1)*log(x + sqrt(x**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=x**3*asin(x)/sqrt(1 - x**4),
        variable=x,
        num_steps=5,
        integral=x*sqrt(x**2 + 1)/4 - sqrt(1 - x**4)*asin(x)/2 + asinh(x)/4,
    ),
    RubiTestSuiteCase(
        integrand=x*log(x + sqrt(x**2 + 1))*atan(x)/sqrt(x**2 + 1),
        variable=x,
        num_steps=4,
        integral=-x*atan(x) + sqrt(x**2 + 1)*log(x + sqrt(x**2 + 1))*atan(x) - log(x + sqrt(x**2 + 1))**2/2 + log(x**2 + 1)/2,
    ),
    RubiTestSuiteCase(
        integrand=x*log(sqrt(1 - x**2) + 1)/sqrt(1 - x**2),
        variable=x,
        num_steps=5,
        integral=-sqrt(1 - x**2)*log(sqrt(1 - x**2) + 1) + sqrt(1 - x**2) - log(sqrt(1 - x**2) + 1),
    ),
    RubiTestSuiteCase(
        integrand=x*log(x + sqrt(x**2 + 1))/sqrt(x**2 + 1),
        variable=x,
        num_steps=2,
        integral=-x + sqrt(x**2 + 1)*log(x + sqrt(x**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=x*log(x + sqrt(1 - x**2))/sqrt(1 - x**2),
        variable=x,
        num_steps=18,
        integral=-sqrt(1 - x**2)*log(x + sqrt(1 - x**2)) + sqrt(1 - x**2) + sqrt(2)*atanh(sqrt(2)*x)/2 - sqrt(2)*atanh(sqrt(2)*sqrt(1 - x**2))/2,
    ),
    RubiTestSuiteCase(
        integrand=log(x)/(x**2*sqrt(1 - x**2)),
        variable=x,
        num_steps=3,
        integral=-asin(x) - sqrt(1 - x**2)*log(x)/x - sqrt(1 - x**2)/x,
    ),
    RubiTestSuiteCase(
        integrand=x*atan(x)/sqrt(x**2 + 1),
        variable=x,
        num_steps=2,
        integral=sqrt(x**2 + 1)*atan(x) - asinh(x),
    ),
    RubiTestSuiteCase(
        integrand=atan(x)/(x**2*sqrt(1 - x**2)),
        variable=x,
        num_steps=7,
        integral=sqrt(2)*atanh(sqrt(2)*sqrt(1 - x**2)/2) - atanh(sqrt(1 - x**2)) - sqrt(1 - x**2)*atan(x)/x,
    ),
    RubiTestSuiteCase(
        integrand=x*atan(x)/sqrt(1 - x**2),
        variable=x,
        num_steps=5,
        integral=-sqrt(1 - x**2)*atan(x) - asin(x) + sqrt(2)*atan(sqrt(2)*x/sqrt(1 - x**2)),
    ),
    RubiTestSuiteCase(
        integrand=atan(x)/(x**2*sqrt(x**2 + 1)),
        variable=x,
        num_steps=4,
        integral=-atanh(sqrt(x**2 + 1)) - sqrt(x**2 + 1)*atan(x)/x,
    ),
    RubiTestSuiteCase(
        integrand=asin(x)/(x**2*sqrt(1 - x**2)),
        variable=x,
        num_steps=2,
        integral=log(x) - sqrt(1 - x**2)*asin(x)/x,
    ),
    RubiTestSuiteCase(
        integrand=x*log(x)/sqrt(x**2 - 1),
        variable=x,
        num_steps=5,
        integral=sqrt(x**2 - 1)*log(x) - sqrt(x**2 - 1) + atan(sqrt(x**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=log(x)/(x**2*sqrt(x**2 + 1)),
        variable=x,
        num_steps=3,
        integral=asinh(x) - sqrt(x**2 + 1)*log(x)/x - sqrt(x**2 + 1)/x,
    ),
    RubiTestSuiteCase(
        integrand=x*asec(x)/sqrt(x**2 - 1),
        variable=x,
        num_steps=2,
        integral=-x*log(x)/sqrt(x**2) + sqrt(x**2 - 1)*asec(x),
    ),
    RubiTestSuiteCase(
        integrand=x*log(x)/sqrt(x**2 + 1),
        variable=x,
        num_steps=5,
        integral=sqrt(x**2 + 1)*log(x) - sqrt(x**2 + 1) + atanh(sqrt(x**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(sin(x)**2 + 1),
        variable=x,
        num_steps=2,
        integral=-sqrt(2)*atanh(sqrt(2)*cos(x)/2)/2,
    ),
    RubiTestSuiteCase(
        integrand=(x**2 + 1)/((1 - x**2)*sqrt(x**4 + 1)),
        variable=x,
        num_steps=2,
        integral=sqrt(2)*atanh(sqrt(2)*x/sqrt(x**4 + 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=(1 - x**2)/((x**2 + 1)*sqrt(x**4 + 1)),
        variable=x,
        num_steps=2,
        integral=sqrt(2)*atan(sqrt(2)*x/sqrt(x**4 + 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=log(sin(x))/(sin(x) + 1),
        variable=x,
        num_steps=4,
        integral=-x - atanh(cos(x)) - log(sin(x))*cos(x)/(sin(x) + 1),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(sin(x) + 1)*log(sin(x)),
        variable=x,
        num_steps=6,
        integral=-4*atanh(cos(x)/sqrt(sin(x) + 1)) - 2*log(sin(x))*cos(x)/sqrt(sin(x) + 1) + 4*cos(x)/sqrt(sin(x) + 1),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/sqrt(sec(x)**4 - 1),
        variable=x,
        num_steps=-5,
        integral=-sqrt(2)*atanh(sqrt(2)*sqrt(sec(x)**4 - 1)*cos(x)*cot(x)/2)/2,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/sqrt(tan(x)**4 + 1),
        variable=x,
        num_steps=4,
        integral=-sqrt(2)*atanh(sqrt(2)*(1 - tan(x)**2)/(2*sqrt(tan(x)**4 + 1)))/4,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1)),
        variable=x,
        num_steps=-1,
        integral=sqrt(2)*sqrt(sec(x) - 1)*sqrt(sec(x) + 1)*(sqrt(-1 + sqrt(2))*atan(sqrt(-2 + 2*sqrt(2))*(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1) - sqrt(2))/(2*sqrt(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1)))) - sqrt(1 + sqrt(2))*atan(sqrt(2 + 2*sqrt(2))*(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1) - sqrt(2))/(2*sqrt(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1)))) - sqrt(1 + sqrt(2))*atanh(sqrt(-2 + 2*sqrt(2))*sqrt(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1))/(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1) + sqrt(2))) + sqrt(-1 + sqrt(2))*atanh(sqrt(2 + 2*sqrt(2))*sqrt(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1))/(-sqrt(sec(x) - 1) + sqrt(sec(x) + 1) + sqrt(2))))*cot(x),
    ),
    RubiTestSuiteCase(
        integrand=x*log(x**2 + 1)*atan(x)**2,
        variable=x,
        num_steps=13,
        integral=-x**2*atan(x)**2/2 - x*log(x**2 + 1)*atan(x) + 3*x*atan(x) + (x**2/2 + sympy.S.Half)*log(x**2 + 1)*atan(x)**2 + log(x**2 + 1)**2/4 - 3*log(x**2 + 1)/2 - 3*atan(x)**2/2,
    ),
    RubiTestSuiteCase(
        integrand=atan(x*sqrt(x**2 + 1)),
        variable=x,
        num_steps=12,
        integral=x*atan(x*sqrt(x**2 + 1)) - sqrt(3)*log(x**2 - sqrt(3)*sqrt(x**2 + 1) + 2)/4 + sqrt(3)*log(x**2 + sqrt(3)*sqrt(x**2 + 1) + 2)/4 - atan(2*sqrt(x**2 + 1) - sqrt(3))/2 - atan(2*sqrt(x**2 + 1) + sqrt(3))/2,
    ),
    RubiTestSuiteCase(
        integrand=asin(x/sqrt(1 - x**2)),
        variable=x,
        num_steps=4,
        integral=x*asin(x/sqrt(1 - x**2)) + atan(sqrt(1 - 2*x**2)),
    ),
]
