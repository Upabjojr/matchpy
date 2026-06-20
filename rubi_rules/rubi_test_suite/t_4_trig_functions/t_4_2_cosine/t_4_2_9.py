# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.2 Cosine/4.2.9 trig^m (a+b cos^n+c cos^(2 n))^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.2 Cosine/4.2.9 trig^m (a+b cos^n+c cos^(2 n))^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c = symbols('a b c')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sin(x)**5/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=7,
        integral=b*cos(x)**2/(2*c**2) + b*(b**2 - 2*c*(a + c))*log(a + b*cos(x) + c*cos(x)**2)/(2*c**4) - cos(x)**3/(3*c) - (b**2 - c*(a + 2*c))*cos(x)/c**3 + (b**4 - 2*b**2*c*(2*a + c) + 2*c**2*(a + c)**2)*atanh((b + 2*c*cos(x))/sqrt(-4*a*c + b**2))/(c**4*sqrt(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=7,
        integral=-b*log(a + b*cos(x) + c*cos(x)**2)/(2*c**2) + cos(x)/c - (b**2 - 2*c*(a + c))*atanh((b + 2*c*cos(x))/sqrt(-4*a*c + b**2))/(c**2*sqrt(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=3,
        integral=2*atanh((b + 2*c*cos(x))/sqrt(-4*a*c + b**2))/sqrt(-4*a*c + b**2),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=9,
        integral=b*log(a + b*cos(x) + c*cos(x)**2)/((a + b + c)*(2*a - 2*b + 2*c)) + log(1 - cos(x))/(2*a + 2*b + 2*c) - log(cos(x) + 1)/(2*a - 2*b + 2*c) - (-2*a*c + b**2 - 2*c**2)*atanh((b + 2*c*cos(x))/sqrt(-4*a*c + b**2))/(sqrt(-4*a*c + b**2)*(a - b + c)*(a + b + c)),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=10,
        integral=-b*(b**2 - 2*c*(a + c))*log(a + b*cos(x) + c*cos(x)**2)/(2*(a**2 + 2*a*c - b**2 + c**2)**2) + (b - (a + c)*cos(x))*csc(x)**2/((a + b + c)*(2*a - 2*b + 2*c)) - (a - 2*b + 3*c)*log(cos(x) + 1)/(4*(a - b + c)**2) + (a + 2*b + 3*c)*log(1 - cos(x))/(4*(a + b + c)**2) + (b**4 - 2*b**2*c*(2*a + c) + 2*c**2*(a + c)**2)*atanh((b + 2*c*cos(x))/sqrt(-4*a*c + b**2))/(sqrt(-4*a*c + b**2)*(a**2 + 2*a*c - b**2 + c**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**4/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=10,
        integral=-b*sin(x)/c**2 + x/(2*c) + sin(x)*cos(x)/(2*c) + x*(b**2 - c*(a + 2*c))/c**3 - (2*b*(b**2 - 2*c*(a + c)) - 2*(b**4 - 2*b**2*c*(2*a + c) + 2*c**2*(a + c)**2)/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(c**3*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) - (2*b**4 + 2*b**3*sqrt(-4*a*c + b**2) - 4*b**2*c*(2*a + c) - 4*b*c*(a + c)*sqrt(-4*a*c + b**2) + 4*c**2*(a + c)**2)*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(c**3*sqrt(-4*a*c + b**2)*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=7,
        integral=-x/c + (2*b - 2*(b**2 - 2*c*(a + c))/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(c*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) + (2*b + 2*(b**2 - 2*c*(a + c))/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(c*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=9,
        integral=-2*b*c*(1 - (b**2 - 2*c*(a + c))/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/((a - b + c)*(a + b + c)*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) - 2*b*c*(1 + (b**2 - 2*c*(a + c))/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/((a - b + c)*(a + b + c)*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) + sin(x)/((cos(x) + 1)*(2*a - 2*b + 2*c)) - sin(x)/((1 - cos(x))*(2*a + 2*b + 2*c)),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(cos(x)**2 + cos(x) - 2),
        variable=x,
        num_steps=4,
        integral=-log(1 - cos(x))/3 + log(cos(x) + 2)/3,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(cos(x)**2 - 5*cos(x) + 4),
        variable=x,
        num_steps=4,
        integral=log(1 - cos(x))/3 - log(4 - cos(x))/3,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(cos(x)**2 - 2*cos(x) + 3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*atan(sqrt(2)*(1 - cos(x))/2)/2,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(cos(x)**2 - 4*cos(x) + 13)**2,
        variable=x,
        num_steps=4,
        integral=(2 - cos(x))/(18*cos(x)**2 - 72*cos(x) + 234) - atan(cos(x)/3 + sympy.S(-2)/3)/54,
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**4/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=10,
        integral=-b*sin(x)/c**2 + x/(2*c) + sin(x)*cos(x)/(2*c) + x*(-a*c + b**2)/c**3 - (-4*a*b*c + 2*b**3 + 2*(2*a**2*c**2 - 4*a*b**2*c + b**4)/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(c**3*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) - (-4*a*b*c + 2*b**3 - 2*(2*a**2*c**2 - 4*a*b**2*c + b**4)/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(c**3*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**3/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=8,
        integral=-b*x/c**2 + sin(x)/c + (-6*a*b*c/sqrt(-4*a*c + b**2) - 2*a*c + 2*b**3/sqrt(-4*a*c + b**2) + 2*b**2)*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(c**2*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) + (6*a*b*c/sqrt(-4*a*c + b**2) - 2*a*c - 2*b**3/sqrt(-4*a*c + b**2) + 2*b**2)*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(c**2*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)**2/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=7,
        integral=x/c - (2*b - 2*(-2*a*c + b**2)/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(c*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) - (2*b + 2*(-2*a*c + b**2)/sqrt(-4*a*c + b**2))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(c*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=cos(x)/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=6,
        integral=(-2*b/sqrt(-4*a*c + b**2) + 2)*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) + (2*b/sqrt(-4*a*c + b**2) + 2)*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=5,
        integral=-4*c*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(sqrt(-4*a*c + b**2)*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) + 4*c*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(sqrt(-4*a*c + b**2)*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))),
    ),
    RubiTestSuiteCase(
        integrand=sec(x)/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=8,
        integral=-2*c*(-b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(a*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) - 2*c*(b/sqrt(-4*a*c + b**2) + 1)*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(a*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) + atanh(sin(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**2/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=10,
        integral=tan(x)/a + 2*b*c*(1 - (-2*a*c + b**2)/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(a**2*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) + 2*b*c*(1 + (-2*a*c + b**2)/(b*sqrt(-4*a*c + b**2)))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(a**2*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) - b*atanh(sin(x))/a**2,
    ),
    RubiTestSuiteCase(
        integrand=sec(x)**3/(a + b*cos(x) + c*cos(x)**2),
        variable=x,
        num_steps=12,
        integral=tan(x)*sec(x)/(2*a) + atanh(sin(x))/(2*a) - b*tan(x)/a**2 + 2*c*(-3*a*b*c + b**3 - sqrt(-4*a*c + b**2)*(-a*c + b**2))*atan(sqrt(b - 2*c + sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c + sqrt(-4*a*c + b**2)))/(a**3*sqrt(-4*a*c + b**2)*sqrt(b - 2*c + sqrt(-4*a*c + b**2))*sqrt(b + 2*c + sqrt(-4*a*c + b**2))) - 2*c*(-3*a*b*c + b**3 + sqrt(-4*a*c + b**2)*(-a*c + b**2))*atan(sqrt(b - 2*c - sqrt(-4*a*c + b**2))*tan(x/2)/sqrt(b + 2*c - sqrt(-4*a*c + b**2)))/(a**3*sqrt(-4*a*c + b**2)*sqrt(b - 2*c - sqrt(-4*a*c + b**2))*sqrt(b + 2*c - sqrt(-4*a*c + b**2))) + (-a*c + b**2)*atanh(sin(x))/a**3,
    ),
]
