# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.1 Sine/4.1.4.1 (a+b sin)^m (A+B sin+C sin^2).m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.1 Sine/4.1.4.1 (a+b sin)^m (A+B sin+C sin^2).m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, C, a, b, e, f, m = symbols('A B C a b e f m')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(m - (m + 2)*sin(e + f*x)**2 + 1)*sin(e + f*x)**m,
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**(m + 1)*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(6 - 7*sin(e + f*x)**2)*sin(e + f*x)**5,
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**6*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(5 - 6*sin(e + f*x)**2)*sin(e + f*x)**4,
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**5*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(4 - 5*sin(e + f*x)**2)*sin(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**4*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(3 - 4*sin(e + f*x)**2)*sin(e + f*x)**2,
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**3*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(2 - 3*sin(e + f*x)**2)*sin(e + f*x),
        variable=x,
        num_steps=1,
        integral=sin(e + f*x)**2*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=1 - 2*sin(e + f*x)**2,
        variable=x,
        num_steps=3,
        integral=sin(e + f*x)*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=-sin(e + f*x)**2*csc(e + f*x),
        variable=x,
        num_steps=1,
        integral=cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=-csc(e + f*x)**2,
        variable=x,
        num_steps=2,
        integral=cot(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(sin(e + f*x)**2 - 2)*csc(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=cot(e + f*x)*csc(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(2*sin(e + f*x)**2 - 3)*csc(e + f*x)**4,
        variable=x,
        num_steps=1,
        integral=cot(e + f*x)*csc(e + f*x)**2/f,
    ),
    RubiTestSuiteCase(
        integrand=(3*sin(e + f*x)**2 - 4)*csc(e + f*x)**5,
        variable=x,
        num_steps=1,
        integral=cot(e + f*x)*csc(e + f*x)**3/f,
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m,
        variable=x,
        num_steps=4,
        integral=-2**(m + sympy.S.Half)*(A*(m**2 + 3*m + 2) + C*(m**2 + m + 1))*(a*sin(e + f*x) + a)**m*(sin(e + f*x) + 1)**(-m + sympy.S(-1)/2)*cos(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), sympy.S.Half - sin(e + f*x)/2)/(f*(m + 1)*(m + 2)) + C*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(f*(m**2 + 3*m + 2)) - C*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(a*f*(m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*sin(e + f*x))**m*(-A*sin(e + f*x)**2 + A),
        variable=x,
        num_steps=7,
        integral=4*sqrt(2)*A*(a + b*sin(e + f*x))**m*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S(-3)/2, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(f*((a + b*sin(e + f*x))/(a + b))**m*sqrt(sin(e + f*x) + 1)) - 4*sqrt(2)*A*(a + b*sin(e + f*x))**m*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S(-1)/2, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(f*((a + b*sin(e + f*x))/(a + b))**m*sqrt(sin(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a + b*sin(e + f*x))**m,
        variable=x,
        num_steps=8,
        integral=sqrt(2)*C*a*(a + b)*(a + b*sin(e + f*x))**m*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m - 1, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(b**2*f*((a + b*sin(e + f*x))/(a + b))**m*(m + 2)*sqrt(sin(e + f*x) + 1)) - C*(a + b*sin(e + f*x))**(m + 1)*cos(e + f*x)/(b*f*(m + 2)) - sqrt(2)*(a + b*sin(e + f*x))**m*(C*a**2 + b**2*(A*(m + 2) + C*(m + 1)))*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(b**2*f*((a + b*sin(e + f*x))/(a + b))**m*(m + 2)*sqrt(sin(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*sin(e + f*x)**5,
        variable=x,
        num_steps=3,
        integral=C*cos(e + f*x)**7/(7*f) - (A + C)*cos(e + f*x)/f - (A + 3*C)*cos(e + f*x)**5/(5*f) + (2*A + 3*C)*cos(e + f*x)**3/(3*f),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=4,
        integral=-2**(m + sympy.S.Half)*(a*sin(e + f*x) + a)**m*(sin(e + f*x) + 1)**(-m + sympy.S(-1)/2)*(A*(m**2 + 3*m + 2) + B*m*(m + 2) + C*(m**2 + m + 1))*cos(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), sympy.S.Half - sin(e + f*x)/2)/(f*(m + 1)*(m + 2)) - C*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(a*f*(m + 2)) + (-B*(m + 2) + C)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(f*(m + 1)*(m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*sin(e + f*x))**m*(A + C*sin(e + f*x)**2 + (A + C)*sin(e + f*x)),
        variable=x,
        num_steps=7,
        integral=-4*sqrt(2)*C*(a + b*sin(e + f*x))**m*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S(-3)/2, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(f*((a + b*sin(e + f*x))/(a + b))**m*sqrt(sin(e + f*x) + 1)) - 2*sqrt(2)*(A - C)*(a + b*sin(e + f*x))**m*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S(-1)/2, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(f*((a + b*sin(e + f*x))/(a + b))**m*sqrt(sin(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*sin(e + f*x))**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=8,
        integral=-C*(a + b*sin(e + f*x))**(m + 1)*cos(e + f*x)/(b*f*(m + 2)) + sqrt(2)*(a + b)*(a + b*sin(e + f*x))**m*(-B*b*(m + 2) + C*a)*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m - 1, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(b**2*f*((a + b*sin(e + f*x))/(a + b))**m*(m + 2)*sqrt(sin(e + f*x) + 1)) - sqrt(2)*(a + b*sin(e + f*x))**m*(A*b**2*(m + 2) - B*a*b*(m + 2) + C*a**2 + C*b**2*(m + 1))*cos(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m, sympy.S(3)/2, sympy.S.Half - sin(e + f*x)/2, b*(1 - sin(e + f*x))/(a + b))/(b**2*f*((a + b*sin(e + f*x))/(a + b))**m*(m + 2)*sqrt(sin(e + f*x) + 1)),
    ),
]
