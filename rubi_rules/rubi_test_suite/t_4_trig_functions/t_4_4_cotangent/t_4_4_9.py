# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.4 Cotangent/4.4.9 trig^m (a+b cot^n+c cot^(2 n))^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.4 Cotangent/4.4.9 trig^m (a+b cot^n+c cot^(2 n))^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e = symbols('a b c d e')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**5/sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2),
        variable=x,
        num_steps=15,
        integral=-b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*c**(sympy.S(3)/2)*e) + b*(-12*a*c + 5*b**2)*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(16*c**(sympy.S(7)/2)*e) - sqrt(2)*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c - sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) + sqrt(2)*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c + sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x)**2/(3*c*e) + sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/(c*e) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(-16*a*c + 15*b**2 - 10*b*c*cot(d + e*x))/(24*c**3*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**3/sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2),
        variable=x,
        num_steps=11,
        integral=b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*c**(sympy.S(3)/2)*e) + sqrt(2)*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c - sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) - sqrt(2)*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c + sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/(c*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)/sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2),
        variable=x,
        num_steps=6,
        integral=-sqrt(2)*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c - sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) + sqrt(2)*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c + sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)/sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2),
        variable=x,
        num_steps=10,
        integral=sqrt(2)*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c - sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) - sqrt(2)*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c + sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) + atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(sqrt(a)*e),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)**3/sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2),
        variable=x,
        num_steps=14,
        integral=-sqrt(2)*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c - sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) + sqrt(2)*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(a + b*cot(d + e*x) - c + sqrt(a**2 - 2*a*c + b**2 + c**2))/(2*sqrt(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*e*sqrt(a**2 - 2*a*c + b**2 + c**2)) + sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)**2/(2*a*e) - 3*b*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)/(4*a**2*e) - atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(sqrt(a)*e) + (-4*a*c + 3*b**2)*atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(8*a**(sympy.S(5)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x)**5,
        variable=x,
        num_steps=21,
        integral=-b*(b + 2*c*cot(d + e*x))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/(8*c**2*e) + b*(b + 2*c*cot(d + e*x))*(-12*a*c + 7*b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/(128*c**4*e) - b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*sqrt(c)*e) + b*(-4*a*c + b**2)*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(16*c**(sympy.S(5)/2)*e) - b*(-12*a*c + 7*b**2)*(-4*a*c + b**2)*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(256*c**(sympy.S(9)/2)*e) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/e + sqrt(2)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))*atanh(sqrt(2)*(b**2 + b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) - sqrt(2)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))*atan(sqrt(2)*(b**2 - b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) - (a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2)*cot(d + e*x)**2/(5*c*e) + (a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2)/(3*c*e) - (a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2)*(-32*a*c + 35*b**2 - 42*b*c*cot(d + e*x))/(240*c**3*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x)**3,
        variable=x,
        num_steps=16,
        integral=b*(b + 2*c*cot(d + e*x))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/(8*c**2*e) + b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*sqrt(c)*e) - b*(-4*a*c + b**2)*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(16*c**(sympy.S(5)/2)*e) + sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/e - sqrt(2)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))*atanh(sqrt(2)*(b**2 + b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) + sqrt(2)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))*atan(sqrt(2)*(b**2 - b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) - (a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2)/(3*c*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x),
        variable=x,
        num_steps=10,
        integral=-b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*sqrt(c)*e) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)/e + sqrt(2)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))*atanh(sqrt(2)*(b**2 + b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) - sqrt(2)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))*atan(sqrt(2)*(b**2 - b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x),
        variable=x,
        num_steps=18,
        integral=sqrt(a)*atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/e - sqrt(2)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))*atanh(sqrt(2)*(b**2 + b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) + sqrt(2)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))*atan(sqrt(2)*(b**2 - b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)**3,
        variable=x,
        num_steps=21,
        integral=-sqrt(a)*atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/e + sqrt(2)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))*atanh(sqrt(2)*(b**2 + b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c - sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c - sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) - sqrt(2)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))*atan(sqrt(2)*(b**2 - b*sqrt(a**2 - 2*a*c + b**2 + c**2)*cot(d + e*x) + (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)*sqrt(a**2 - a*(2*c + sqrt(a**2 - 2*a*c + b**2 + c**2)) + b**2 + c*(c + sqrt(a**2 - 2*a*c + b**2 + c**2)))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(1)/4)) + (2*a + b*cot(d + e*x))*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)**2/(4*a*e) - (-4*a*c + b**2)*atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(8*a**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**7/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=20,
        integral=2*b*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x)**3/(c*e*(-4*a*c + b**2)) - 3*b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*c**(sympy.S(5)/2)*e) + 5*b*(-12*a*c + 7*b**2)*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(16*c**(sympy.S(9)/2)*e) - 2*(2*a + b*cot(d + e*x))*cot(d + e*x)**4/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + 2*(2*a + b*cot(d + e*x))*cot(d + e*x)**2/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - (4*a + 2*b*cot(d + e*x))/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - (-16*a*c + 7*b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*cot(d + e*x)**2/(3*c**2*e*(-4*a*c + b**2)) + sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(-8*a*c + 3*b**2 - 2*b*c*cot(d + e*x))/(c**2*e*(-4*a*c + b**2)) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(256*a**2*c**2 - 460*a*b**2*c + 105*b**4 - 2*b*c*(-116*a*c + 35*b**2)*cot(d + e*x))/(24*c**4*e*(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**5/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=14,
        integral=3*b*atanh((b + 2*c*cot(d + e*x))/(2*sqrt(c)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(2*c**(sympy.S(5)/2)*e) - 2*(2*a + b*cot(d + e*x))*cot(d + e*x)**2/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + (4*a + 2*b*cot(d + e*x))/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*(-8*a*c + 3*b**2 - 2*b*c*cot(d + e*x))/(c**2*e*(-4*a*c + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**3/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=10,
        integral=-(4*a + 2*b*cot(d + e*x))/(e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=13,
        integral=sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - (-4*a*c + 2*b**2 + 2*b*c*cot(d + e*x))/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(a**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)**3/(a + b*cot(d + e*x) + c*cot(d + e*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=18,
        integral=-sqrt(2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c + sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c - sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 + (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) + sqrt(2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))*atanh(sqrt(2)*(b**2 - b*(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*cot(d + e*x) - (a - c)*(a - c - sqrt(a**2 - 2*a*c + b**2 + c**2)))/(2*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*sqrt(2*a - 2*c + sqrt(a**2 - 2*a*c + b**2 + c**2))*sqrt(a**2 - 2*a*c - b**2 + c**2 - (a - c)*sqrt(a**2 - 2*a*c + b**2 + c**2))))/(2*e*(a**2 - 2*a*c + b**2 + c**2)**(sympy.S(3)/2)) - (2*a*(b**2 - c*(2*a - 2*c)) + 2*b*c*(a + c)*cot(d + e*x))/(e*(b**2 + (a - c)**2)*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) - (-4*a*c + 2*b**2 + 2*b*c*cot(d + e*x))*tan(d + e*x)**2/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + (-4*a*c + 2*b**2 + 2*b*c*cot(d + e*x))/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)) + (-12*a*c + 5*b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)**2/(2*a**2*e*(-4*a*c + b**2)) - b*(-52*a*c + 15*b**2)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)*tan(d + e*x)/(4*a**3*e*(-4*a*c + b**2)) - atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(a**(sympy.S(3)/2)*e) + (-12*a*c + 15*b**2)*atanh((2*a + b*cot(d + e*x))/(2*sqrt(a)*sqrt(a + b*cot(d + e*x) + c*cot(d + e*x)**2)))/(8*a**(sympy.S(7)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**5/sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4),
        variable=x,
        num_steps=8,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*sqrt(a - b + c)) - sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)/(2*c*e) + (b + 2*c)*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*c**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**3/sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4),
        variable=x,
        num_steps=7,
        integral=-atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*sqrt(a - b + c)) - atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*sqrt(c)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)/sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4),
        variable=x,
        num_steps=4,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*sqrt(a - b + c)),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)/sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4),
        variable=x,
        num_steps=8,
        integral=-atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*sqrt(a - b + c)) + atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*sqrt(a)*e),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)**3/sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4),
        variable=x,
        num_steps=11,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*sqrt(a - b + c)) + sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*tan(d + e*x)**2/(2*a*e) - atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*sqrt(a)*e) - b*atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*a**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*cot(d + e*x)**5,
        variable=x,
        num_steps=9,
        integral=sqrt(a - b + c)*atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) - (a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2)/(6*c*e) + (2*c*(b + 2*c)*cot(d + e*x)**2 + (b - 2*c)*(b + 4*c))*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)/(16*c**2*e) - (b**3 + 2*b**2*c - 4*b*c*(a - 2*c) - 8*c**2*(a + 2*c))*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(32*c**(sympy.S(5)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*cot(d + e*x)**3,
        variable=x,
        num_steps=8,
        integral=-sqrt(a - b + c)*atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) - sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*(b + 2*c*cot(d + e*x)**2 - 4*c)/(8*c*e) + (b**2 + 4*b*c - 4*c*(a + 2*c))*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(16*c**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*cot(d + e*x),
        variable=x,
        num_steps=8,
        integral=sqrt(a - b + c)*atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) - sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)/(2*e) - (b - 2*c)*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*sqrt(c)*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*tan(d + e*x),
        variable=x,
        num_steps=10,
        integral=sqrt(a)*atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) - sqrt(c)*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) - sqrt(a - b + c)*atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*tan(d + e*x)**3,
        variable=x,
        num_steps=22,
        integral=-sqrt(a)*atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) + b*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*sqrt(c)*e) - sqrt(c)*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) + sqrt(a - b + c)*atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e) + sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*tan(d + e*x)**2/(2*e) - (b - 2*c)*atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*sqrt(c)*e) + b*atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*sqrt(a)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**7/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=8,
        integral=-atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) - (a*(-a*(b + 2*c) + b**2) + (2*a**2*c - a*b*(b + 3*c) + b**3)*cot(d + e*x)**2)/(c*e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) - atanh((b + 2*c*cot(d + e*x)**2)/(2*sqrt(c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*c**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**5/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) - (a*(2*a - b) + (2*a*c + b*(a - b))*cot(d + e*x)**2)/(e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)**3/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=-atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) + (a*(b - 2*c) + c*(2*a - b)*cot(d + e*x)**2)/(e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)),
    ),
    RubiTestSuiteCase(
        integrand=cot(d + e*x)/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) - (-2*a*c + b**2 - b*c + c*(b - 2*c)*cot(d + e*x)**2)/(e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=12,
        integral=-atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) + (-2*a*c + b**2 - b*c + c*(b - 2*c)*cot(d + e*x)**2)/(e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) - (-2*a*c + b**2 + b*c*cot(d + e*x)**2)/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) + atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*a**(sympy.S(3)/2)*e),
    ),
    RubiTestSuiteCase(
        integrand=tan(d + e*x)**3/(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=16,
        integral=atanh((2*a - b + (b - 2*c)*cot(d + e*x)**2)/(2*sqrt(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*e*(a - b + c)**(sympy.S(3)/2)) - (-2*a*c + b**2 - b*c + c*(b - 2*c)*cot(d + e*x)**2)/(e*(-4*a*c + b**2)*(a - b + c)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) - (-2*a*c + b**2 + b*c*cot(d + e*x)**2)*tan(d + e*x)**2/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) + (-2*a*c + b**2 + b*c*cot(d + e*x)**2)/(a*e*(-4*a*c + b**2)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)) + (-8*a*c + 3*b**2)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)*tan(d + e*x)**2/(2*a**2*e*(-4*a*c + b**2)) - atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(2*a**(sympy.S(3)/2)*e) - 3*b*atanh((2*a + b*cot(d + e*x)**2)/(2*sqrt(a)*sqrt(a + b*cot(d + e*x)**2 + c*cot(d + e*x)**4)))/(4*a**(sympy.S(5)/2)*e),
    ),
]
