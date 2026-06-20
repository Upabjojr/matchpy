# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.1 Sine/4.1.9 trig^m (a+b sin^n+c sin^(2 n))^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.1 Sine/4.1.9 trig^m (a+b sin^n+c sin^(2 n))^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c = symbols('a b c')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sin(x)**4/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=12,
        integral=b*cos(x)/c**2 + x/(2*c) - sin(x)*cos(x)/(2*c) + x*(-a*c + b**2)/c**3 - sqrt(2)*(-2*a*b*c + b**3 + (2*a**2*c**2 - 4*a*b**2*c + b**4)/sqrt(-4*a*c + b**2))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c**3*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - sqrt(2)*(-2*a*b*c + b**3 - (2*a**2*c**2 - 4*a*b**2*c + b**4)/sqrt(-4*a*c + b**2))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c**3*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=10,
        integral=-b*x/c**2 + sqrt(2)*b*(-3*a*c/sqrt(-4*a*c + b**2) - a*c/b + b**2/sqrt(-4*a*c + b**2) + b)*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c**2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) + sqrt(2)*b*(3*a*c/sqrt(-4*a*c + b**2) - a*c/b - b**2/sqrt(-4*a*c + b**2) + b)*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c**2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - cos(x)/c,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=9,
        integral=x/c - sqrt(2)*(b - (-2*a*c + b**2)/sqrt(-4*a*c + b**2))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - sqrt(2)*(b + (-2*a*c + b**2)/sqrt(-4*a*c + b**2))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=8,
        integral=sqrt(2)*(-b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c)) + sqrt(2)*(b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c)),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=7,
        integral=-2*sqrt(2)*c*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(sqrt(-4*a*c + b**2)*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) + 2*sqrt(2)*c*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(sqrt(-4*a*c + b**2)*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=10,
        integral=-sqrt(2)*c*(-b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - sqrt(2)*c*(b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - atanh(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=12,
        integral=-cot(x)/a + sqrt(2)*b*c*(1 - (-2*a*c + b**2)/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a**2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) + sqrt(2)*b*c*(1 + (-2*a*c + b**2)/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a**2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) + b*atanh(cos(x))/a**2,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=14,
        integral=-cot(x)*csc(x)/(2*a) - atanh(cos(x))/(2*a) + b*cot(x)/a**2 + sqrt(2)*c*(-3*a*b*c + b**3 - sqrt(-4*a*c + b**2)*(-a*c + b**2))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a**3*sqrt(-4*a*c + b**2)*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - sqrt(2)*c*(-3*a*b*c + b**3 + sqrt(-4*a*c + b**2)*(-a*c + b**2))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(a**3*sqrt(-4*a*c + b**2)*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - (-a*c + b**2)*atanh(cos(x))/a**3,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=7,
        integral=b*log(a + b*sin(x) + c*sin(x)**2)/(2*c**2) - sin(x)/c + (b**2 - 2*c*(a + c))*atanh((b + 2*c*sin(x))/sqrt(-4*a*c + b**2))/(c**2*sqrt(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=9,
        integral=-x/c - sqrt(2)*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c*sqrt(-4*a*c + b**2)) + sqrt(2)*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/(c*sqrt(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=3,
        integral=-2*atanh((b + 2*c*sin(x))/sqrt(-4*a*c + b**2))/sqrt(-4*a*c + b**2),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=9,
        integral=-b*log(a + b*sin(x) + c*sin(x)**2)/((a + b + c)*(2*a - 2*b + 2*c)) - log(1 - sin(x))/(2*a + 2*b + 2*c) + log(sin(x) + 1)/(2*a - 2*b + 2*c) + (-2*a*c + b**2 - 2*c**2)*atanh((b + 2*c*sin(x))/sqrt(-4*a*c + b**2))/(sqrt(-4*a*c + b**2)*(a - b + c)*(a + b + c)),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=11,
        integral=-sqrt(2)*b*c*(1 - (b**2 - 2*c*(a + c))/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(2)*(2*c + (b + sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/((a - b + c)*(a + b + c)*sqrt(b**2 + b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - sqrt(2)*b*c*(1 + (b**2 - 2*c*(a + c))/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(2)*(2*c + (b - sqrt(-4*a*c + b**2))*tan(x/2))/(2*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))))/((a - b + c)*(a + b + c)*sqrt(b**2 - b*sqrt(-4*a*c + b**2) - 2*c*(a + c))) - cos(x)/((sin(x) + 1)*(2*a - 2*b + 2*c)) + cos(x)/((1 - sin(x))*(2*a + 2*b + 2*c)),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(a + b*sin(x) + c*sin(x)**2),
        variable=x,
        num_steps=10,
        integral=b*(b**2 - 2*c*(a + c))*log(a + b*sin(x) + c*sin(x)**2)/(2*(a**2 + 2*a*c - b**2 + c**2)**2) - (b - (a + c)*sin(x))*sec(x)**2/((a + b + c)*(2*a - 2*b + 2*c)) + (a - 2*b + 3*c)*log(sin(x) + 1)/(4*(a - b + c)**2) - (a + 2*b + 3*c)*log(1 - sin(x))/(4*(a + b + c)**2) - (b**4 - 2*b**2*c*(2*a + c) + 2*c**2*(a + c)**2)*atanh((b + 2*c*sin(x))/sqrt(-4*a*c + b**2))/(sqrt(-4*a*c + b**2)*(a**2 + 2*a*c - b**2 + c**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(sin(x)**2 + sin(x) - 6),
        variable=x,
        num_steps=4,
        integral=log(2 - sin(x))/5 - log(sin(x) + 3)/5,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(sin(x)**2 - 3*sin(x) + 2),
        variable=x,
        num_steps=4,
        integral=-log(1 - sin(x)) + log(2 - sin(x)),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(sin(x)**2 + 4*sin(x) - 5),
        variable=x,
        num_steps=4,
        integral=log(1 - sin(x))/6 - log(sin(x) + 5)/6,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(sin(x)**2 - 6*sin(x) + 10),
        variable=x,
        num_steps=3,
        integral=atan(sin(x) - 3),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(sin(x)**2 + 2*sin(x) + 2),
        variable=x,
        num_steps=3,
        integral=atan(sin(x) + 1),
    ),
]
