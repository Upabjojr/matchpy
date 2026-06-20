# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.1 Sine/4.1.4.2 (a+b sin)^m (c+d sin)^n (A+B sin+C sin^2).m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.1 Sine/4.1.4.2 (a+b sin)^m (c+d sin)^n (A+B sin+C sin^2).m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, C, a, b, c, d, e, f, m, n = symbols('A B C a b c d e f m n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2),
        variable=x,
        num_steps=5,
        integral=-4*C*(2*m + 1)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)*cos(e + f*x)/(f*(2*m + 7)*(2*m + 9)) + 2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(7)/2)*cos(e + f*x)/(c*f*(2*m + 9)) + 64*c**3*(A*(4*m**2 + 32*m + 63) + C*(4*m**2 - 16*m + 39))*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*(2*m + 9)*sqrt(-c*sin(e + f*x) + c)*(4*m**2 + 8*m + 3)) + 16*c**2*(A*(4*m**2 + 32*m + 63) + C*(4*m**2 - 16*m + 39))*(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c)*cos(e + f*x)/(f*(2*m + 7)*(2*m + 9)*(4*m**2 + 16*m + 15)) + 2*c*(A*(4*m**2 + 32*m + 63) + C*(4*m**2 - 16*m + 39))*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*(2*m + 9)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-4*C*(2*m + 1)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)) + 2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)*cos(e + f*x)/(c*f*(2*m + 7)) + 8*c**2*(A*(4*m**2 + 24*m + 35) + C*(4*m**2 - 8*m + 19))*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*sqrt(-c*sin(e + f*x) + c)*(4*m**2 + 8*m + 3)) + 2*c*(A*(4*m**2 + 24*m + 35) + C*(4*m**2 - 8*m + 19))*(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c)*cos(e + f*x)/(f*(2*m + 3)*(2*m + 5)*(2*m + 7)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c),
        variable=x,
        num_steps=4,
        integral=2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*cos(e + f*x)/(c*f*(2*m + 5)) + 4*C*c*(2*m + 1)*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(a*f*(2*m + 3)*(2*m + 5)*sqrt(-c*sin(e + f*x) + c)) + 2*c*(a*sin(e + f*x) + a)**m*(A*(2*m + 5) - 6*C*m + C)*cos(e + f*x)/(f*(2*m + 1)*(2*m + 5)*sqrt(-c*sin(e + f*x) + c)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/sqrt(-c*sin(e + f*x) + c),
        variable=x,
        num_steps=4,
        integral=-2*C*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(a*f*(2*m + 3)*sqrt(-c*sin(e + f*x) + c)) + (A + C)*(a*sin(e + f*x) + a)**m*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/(-c*sin(e + f*x) + c)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=(A*(1 - 2*m) - C*(2*m + 7))*(a*sin(e + f*x) + a)**m*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(4*c*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (a*sin(e + f*x) + a)**m*(2*A*m + A + C*(2*m + 9))*cos(e + f*x)/(4*c*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (A + C)*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(4*a*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/(-c*sin(e + f*x) + c)**(sympy.S(5)/2),
        variable=x,
        num_steps=5,
        integral=(A*(5 - 2*m) - C*(2*m + 11))*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(16*c*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)) + (A*(4*m**2 - 8*m + 3) + C*(4*m**2 + 24*m + 19))*(a*sin(e + f*x) + a)**m*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(32*c**2*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (A + C)*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(8*a*f*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)/(sqrt(a*sin(e + f*x) + a)*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
        variable=x,
        num_steps=8,
        integral=-(A - 3*C)*log(1 - sin(e + f*x))*cos(e + f*x)/(4*c*f*sqrt(a*sin(e + f*x) + a)*sqrt(-c*sin(e + f*x) + c)) + (A + C)*log(sin(e + f*x) + 1)*cos(e + f*x)/(4*c*f*sqrt(a*sin(e + f*x) + a)*sqrt(-c*sin(e + f*x) + c)) + (A + C)*sqrt(a*sin(e + f*x) + a)*cos(e + f*x)/(4*a*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**n,
        variable=x,
        num_steps=6,
        integral=2**(n + sympy.S.Half)*c*(1 - sin(e + f*x))**(sympy.S.Half - n)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(n - 1)*(C*(m - n)*(2*m + 1) + (A*(m + n + 2) + C*(-m + n + 1))*(m + n + 1))*cos(e + f*x)*hyper((m + sympy.S.Half, sympy.S.Half - n), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(f*(2*m + 1)*(m + n + 1)*(m + n + 2)) - C*(2*m + 1)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**n*cos(e + f*x)/(f*(m + n + 1)*(m + n + 2)) + C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(n + 1)*cos(e + f*x)/(c*f*(m + n + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**m,
        variable=x,
        num_steps=10,
        integral=-C*(c + d*sin(e + f*x))**(n + 1)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(m + n + 2)) + sqrt(2)*C*(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**(m + 1)*(-c*(m + 1) + d*m)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, -n, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(a*d*f*((c + d*sin(e + f*x))/(c - d))**n*sqrt(1 - sin(e + f*x))*(2*m + 3)*(m + n + 2)) + sqrt(2)*(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**m*(c*(2*C*m + C) + d*(A*(m + n + 2) + C*(-m + n + 1)))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, -n, m + sympy.S(3)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(d*f*((c + d*sin(e + f*x))/(c - d))**n*sqrt(1 - sin(e + f*x))*(2*m + 1)*(m + n + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(c + d*sin(e + f*x))**(-m - 2)*(a*sin(e + f*x) + a)**m,
        variable=x,
        num_steps=8,
        integral=-2**(m + sympy.S.Half)*a*((c + d)*(sin(e + f*x) + 1)/(c + d*sin(e + f*x)))**(sympy.S.Half - m)*(a*sin(e + f*x) + a)**(m - 1)*(-c**2*(2*C*m + C) + c*d*(A + C)*(m + 1) + d**2*(-A*m + C*m + C))*cos(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), (1 - sin(e + f*x))*(c - d)/(2*c + 2*d*sin(e + f*x)))/(d*f*(c - d)*(c + d)**2*(c + d*sin(e + f*x))**m*(m + 1)) + sqrt(2)*C*((c + d*sin(e + f*x))/(c - d))**m*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, m + 1, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(a*d*f*sqrt(1 - sin(e + f*x))*(c - d)*(c + d*sin(e + f*x))**m*(2*m + 3)) + (c + d*sin(e + f*x))**(-m - 1)*(A*d**2 + C*c**2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(c**2 - d**2)*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(c + d*sin(e + f*x))**(sympy.S(3)/2)*(a*sin(e + f*x) + a)**m,
        variable=x,
        num_steps=10,
        integral=-2*C*(c + d*sin(e + f*x))**(sympy.S(5)/2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 7)) + 2*sqrt(2)*C*(c - d)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**(m + 1)*(-c*(m + 1) + d*m)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S(-3)/2, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 3)*(2*m + 7)) + sqrt(2)*(c - d)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) + d*(A*(2*m + 7) + C*(5 - 2*m)))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S(-3)/2, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 1)*(2*m + 7)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m,
        variable=x,
        num_steps=10,
        integral=-2*C*(c + d*sin(e + f*x))**(sympy.S(3)/2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 5)) + 2*sqrt(2)*C*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**(m + 1)*(-c*(m + 1) + d*m)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S(-1)/2, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 3)*(2*m + 5)) + sqrt(2)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) + d*(A*(2*m + 5) + C*(3 - 2*m)))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S(-1)/2, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 1)*(2*m + 5)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/sqrt(c + d*sin(e + f*x)),
        variable=x,
        num_steps=10,
        integral=-2*C*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 3)) - 2*sqrt(2)*C*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**(m + 1)*(c*m + c - d*m)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(2*m + 3)**2) + sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) + d*(A*(2*m + 3) - 2*C*m + C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(2*m + 1)*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/(c + d*sin(e + f*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=10,
        integral=sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(-2*c**2*(2*C*m + C) + c*d*(A + C) - d**2*(4*A*m + A - C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)*(2*m + 1)) + (2*A*d**2 + 2*C*c**2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)) + sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**(m + 1)*(2*C*c**2*(m + 1) + d**2*(2*A*m + A - C))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sin(e + f*x)**2)*(a*sin(e + f*x) + a)**m/(c + d*sin(e + f*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=10,
        integral=sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(-2*c**2*(2*C*m + C) + 3*c*d*(A + C) + d**2*(-4*A*m + A + 3*C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S(3)/2, m + sympy.S(3)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(3*d*f*sqrt(1 - sin(e + f*x))*(c - d)**2*(c + d)*sqrt(c + d*sin(e + f*x))*(2*m + 1)) + (2*A*d**2 + 2*C*c**2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(3*d*f*(c + d*sin(e + f*x))**(sympy.S(3)/2)*(c**2 - d**2)) + sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**(m + 1)*(2*C*c**2*(m + 1) - d**2*(-2*A*m + A + 3*C))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S(3)/2, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(3*a*d*f*sqrt(1 - sin(e + f*x))*(c - d)**2*(c + d)*sqrt(c + d*sin(e + f*x))*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/(sqrt(a*sin(e + f*x) + a)*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
        variable=x,
        num_steps=8,
        integral=-(A - B - 3*C)*log(1 - sin(e + f*x))*cos(e + f*x)/(4*c*f*sqrt(a*sin(e + f*x) + a)*sqrt(-c*sin(e + f*x) + c)) + (A - B + C)*log(sin(e + f*x) + 1)*cos(e + f*x)/(4*c*f*sqrt(a*sin(e + f*x) + a)*sqrt(-c*sin(e + f*x) + c)) + sqrt(a*sin(e + f*x) + a)*(A + B + C)*cos(e + f*x)/(4*a*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**n*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=6,
        integral=2**(n + sympy.S.Half)*c*(1 - sin(e + f*x))**(sympy.S.Half - n)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(n - 1)*((m - n)*(B*(m + n + 2) + 2*C*m + C) + (A*(m + n + 2) + C*(-m + n + 1))*(m + n + 1))*cos(e + f*x)*hyper((m + sympy.S.Half, sympy.S.Half - n), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(f*(2*m + 1)*(m + n + 1)*(m + n + 2)) + C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(n + 1)*cos(e + f*x)/(c*f*(m + n + 2)) - (a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**n*(B*(m + n + 2) + 2*C*m + C)*cos(e + f*x)/(f*(m + n + 1)*(m + n + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=5,
        integral=2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(7)/2)*cos(e + f*x)/(c*f*(2*m + 9)) - 64*c**3*(a*sin(e + f*x) + a)**m*(-A*(4*m**2 + 32*m + 63) + B*(-4*m**2 - 8*m + 45) - C*(4*m**2 - 16*m + 39))*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*(2*m + 9)*sqrt(-c*sin(e + f*x) + c)*(4*m**2 + 8*m + 3)) - 16*c**2*(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c)*(-A*(4*m**2 + 32*m + 63) + B*(-4*m**2 - 8*m + 45) - C*(4*m**2 - 16*m + 39))*cos(e + f*x)/(f*(2*m + 7)*(2*m + 9)*(4*m**2 + 16*m + 15)) - 2*c*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*(-A*(4*m**2 + 32*m + 63) + B*(-4*m**2 - 8*m + 45) - C*(4*m**2 - 16*m + 39))*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*(2*m + 9)) - (a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)*(4*B*m + 18*B + 8*C*m + 4*C)*cos(e + f*x)/(f*(2*m + 7)*(2*m + 9)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=4,
        integral=2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)*cos(e + f*x)/(c*f*(2*m + 7)) - 8*c**2*(a*sin(e + f*x) + a)**m*(-A*(4*m**2 + 24*m + 35) + B*(-4*m**2 - 8*m + 21) - C*(4*m**2 - 8*m + 19))*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)*sqrt(-c*sin(e + f*x) + c)*(4*m**2 + 8*m + 3)) - 2*c*(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c)*(-A*(4*m**2 + 24*m + 35) + B*(-4*m**2 - 8*m + 21) - C*(4*m**2 - 8*m + 19))*cos(e + f*x)/(f*(2*m + 3)*(2*m + 5)*(2*m + 7)) - (a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*(4*B*m + 14*B + 8*C*m + 4*C)*cos(e + f*x)/(f*(2*m + 5)*(2*m + 7)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*sqrt(-c*sin(e + f*x) + c)*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=4,
        integral=2*C*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)*cos(e + f*x)/(c*f*(2*m + 5)) + 2*c*(a*sin(e + f*x) + a)**m*(A*(2*m + 5) - B*(2*m + 5) - 6*C*m + C)*cos(e + f*x)/(f*(2*m + 1)*(2*m + 5)*sqrt(-c*sin(e + f*x) + c)) + 2*c*(a*sin(e + f*x) + a)**(m + 1)*(2*B*m + 5*B + 4*C*m + 2*C)*cos(e + f*x)/(a*f*(2*m + 3)*(2*m + 5)*sqrt(-c*sin(e + f*x) + c)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/sqrt(-c*sin(e + f*x) + c),
        variable=x,
        num_steps=5,
        integral=-2*B*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) - 2*C*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)/(a*f*(2*m + 3)*sqrt(-c*sin(e + f*x) + c)) + (a*sin(e + f*x) + a)**m*(A + B + C)*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/(-c*sin(e + f*x) + c)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=(a*sin(e + f*x) + a)**m*(A*(1 - 2*m) - B*(2*m + 3) - C*(2*m + 7))*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(4*c*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (a*sin(e + f*x) + a)**m*(2*A*m + A + 2*B*m + B + C*(2*m + 9))*cos(e + f*x)/(4*c*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (a*sin(e + f*x) + a)**(m + 1)*(A + B + C)*cos(e + f*x)/(4*a*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/(-c*sin(e + f*x) + c)**(sympy.S(5)/2),
        variable=x,
        num_steps=5,
        integral=(a*sin(e + f*x) + a)**m*(A*(5 - 2*m) - B*(2*m + 3) - C*(2*m + 11))*cos(e + f*x)/(16*c*f*(-c*sin(e + f*x) + c)**(sympy.S(3)/2)) - (a*sin(e + f*x) + a)**m*(-A*(4*m**2 - 8*m + 3) + B*(-4*m**2 - 8*m + 5) - C*(4*m**2 + 24*m + 19))*cos(e + f*x)*hyper((1, m + sympy.S.Half), (m + sympy.S(3)/2,), sin(e + f*x)/2 + sympy.S.Half)/(32*c**2*f*(2*m + 1)*sqrt(-c*sin(e + f*x) + c)) + (a*sin(e + f*x) + a)**(m + 1)*(A + B + C)*cos(e + f*x)/(8*a*f*(-c*sin(e + f*x) + c)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(-m - 2)*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=6,
        integral=-2**(-m + sympy.S(-1)/2)*C*(1 - sin(e + f*x))**(m + sympy.S.Half)*(a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(-m - 2)*cos(e + f*x)**3*hyper((m + sympy.S(3)/2, m + sympy.S(3)/2), (m + sympy.S(5)/2,), sin(e + f*x)/2 + sympy.S.Half)/(f*(2*m + 3)) + (a*sin(e + f*x) + a)**m*(-c*sin(e + f*x) + c)**(-m - 1)*(A - B + C)*cos(e + f*x)/(2*c*f*(2*m + 1)) + (a*sin(e + f*x) + a)**(m + 1)*(-c*sin(e + f*x) + c)**(-m - 2)*(A + B + C)*cos(e + f*x)/(2*a*f*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=10,
        integral=-C*(c + d*sin(e + f*x))**(n + 1)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(m + n + 2)) + sqrt(2)*(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**m*(c*(2*C*m + C) + d*(A*(m + n + 2) - B*(m + n + 2) + C*(-m + n + 1)))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, -n, m + sympy.S(3)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(d*f*((c + d*sin(e + f*x))/(c - d))**n*sqrt(1 - sin(e + f*x))*(2*m + 1)*(m + n + 2)) - sqrt(2)*(c + d*sin(e + f*x))**n*(a*sin(e + f*x) + a)**(m + 1)*(C*c*(m + 1) - d*(B*(m + n + 2) + C*m))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, -n, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(a*d*f*((c + d*sin(e + f*x))/(c - d))**n*sqrt(1 - sin(e + f*x))*(2*m + 3)*(m + n + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sin(e + f*x))**(-m - 2)*(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=8,
        integral=-2**(m + sympy.S.Half)*a*((c + d)*(sin(e + f*x) + 1)/(c + d*sin(e + f*x)))**(sympy.S.Half - m)*(a*sin(e + f*x) + a)**(m - 1)*(-c**2*(2*C*m + C) + c*d*(A*m + A + B*m + C*m + C) - d**2*(A*m + B*(m + 1) - C*(m + 1)))*cos(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), (1 - sin(e + f*x))*(c - d)/(2*c + 2*d*sin(e + f*x)))/(d*f*(c - d)*(c + d)**2*(c + d*sin(e + f*x))**m*(m + 1)) + sqrt(2)*C*((c + d*sin(e + f*x))/(c - d))**m*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, m + 1, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(a*d*f*sqrt(1 - sin(e + f*x))*(c - d)*(c + d*sin(e + f*x))**m*(2*m + 3)) + (c + d*sin(e + f*x))**(-m - 1)*(a*sin(e + f*x) + a)**m*(A*d**2 - B*c*d + C*c**2)*cos(e + f*x)/(d*f*(c**2 - d**2)*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sin(e + f*x))**(sympy.S(3)/2)*(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=10,
        integral=-2*C*(c + d*sin(e + f*x))**(sympy.S(5)/2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 7)) + sqrt(2)*(c - d)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) - d*(-A*(2*m + 7) + 2*B*m + 7*B + 2*C*m - 5*C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S(-3)/2, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 1)*(2*m + 7)) - sqrt(2)*(c - d)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**(m + 1)*(2*C*c*(m + 1) - d*(B*(2*m + 7) + 2*C*m))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S(-3)/2, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 3)*(2*m + 7)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=10,
        integral=-2*C*(c + d*sin(e + f*x))**(sympy.S(3)/2)*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 5)) + sqrt(2)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) - d*(-A*(2*m + 5) + 2*B*m + 5*B + 2*C*m - 3*C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S(-1)/2, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 1)*(2*m + 5)) - sqrt(2)*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**(m + 1)*(2*C*c*(m + 1) - d*(B*(2*m + 5) + 2*C*m))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S(-1)/2, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt((c + d*sin(e + f*x))/(c - d))*sqrt(1 - sin(e + f*x))*(2*m + 3)*(2*m + 5)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/sqrt(c + d*sin(e + f*x)),
        variable=x,
        num_steps=10,
        integral=-2*C*sqrt(c + d*sin(e + f*x))*(a*sin(e + f*x) + a)**m*cos(e + f*x)/(d*f*(2*m + 3)) + sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(2*c*(2*C*m + C) - d*(-A*(2*m + 3) + 2*B*m + 3*B + 2*C*m - C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(2*m + 1)*(2*m + 3)) - sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**(m + 1)*(2*C*c*(m + 1) - d*(B*(2*m + 3) + 2*C*m))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(2*m + 3)**2),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/(c + d*sin(e + f*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=10,
        integral=-sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(2*c**2*(2*C*m + C) - c*d*(A + 4*B*m + B + C) + d**2*(4*A*m + A + B - C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S.Half, m + sympy.S(3)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)*(2*m + 1)) + (a*sin(e + f*x) + a)**m*(2*A*d**2 - 2*B*c*d + 2*C*c**2)*cos(e + f*x)/(d*f*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)) - sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(C*(-2*c**2*(m + 1) + d**2) + d*(2*m + 1)*(-A*d + B*c))*(a*sin(e + f*x) + a)**(m + 1)*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S.Half, m + sympy.S(5)/2, -d*(sin(e + f*x) + 1)/(c - d), sin(e + f*x)/2 + sympy.S.Half)/(a*d*f*sqrt(1 - sin(e + f*x))*sqrt(c + d*sin(e + f*x))*(c**2 - d**2)*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x) + a)**m*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/(c + d*sin(e + f*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=10,
        integral=sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**m*(-2*c**2*(2*C*m + C) + c*d*(3*A + 4*B*m - B + 3*C) + d**2*(-4*A*m + A - 3*B + 3*C))*cos(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, sympy.S(3)/2, m + sympy.S(3)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(3*d*f*sqrt(1 - sin(e + f*x))*(c - d)**2*(c + d)*sqrt(c + d*sin(e + f*x))*(2*m + 1)) + (a*sin(e + f*x) + a)**m*(2*A*d**2 - 2*B*c*d + 2*C*c**2)*cos(e + f*x)/(3*d*f*(c + d*sin(e + f*x))**(sympy.S(3)/2)*(c**2 - d**2)) + sqrt(2)*sqrt((c + d*sin(e + f*x))/(c - d))*(a*sin(e + f*x) + a)**(m + 1)*(B*c*d*(1 - 2*m) + 2*C*c**2*(m + 1) - d**2*(-2*A*m + A + 3*C))*cos(e + f*x)*appellf1(m + sympy.S(3)/2, sympy.S.Half, sympy.S(3)/2, m + sympy.S(5)/2, sin(e + f*x)/2 + sympy.S.Half, -d*(sin(e + f*x) + 1)/(c - d))/(3*a*d*f*sqrt(1 - sin(e + f*x))*(c - d)**2*(c + d)*sqrt(c + d*sin(e + f*x))*(2*m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*sin(e + f*x))*(A + B*sin(e + f*x) + C*sin(e + f*x)**2)/sin(e + f*x)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=-2*A*a*cos(e + f*x)/(f*sqrt(sin(e + f*x))) - 2*C*b*sqrt(sin(e + f*x))*cos(e + f*x)/(3*f) + (2*B*b - 2*a*(A - C))*elliptic_e(e/2 + f*x/2 - pi/4, 2)/f + (6*A*b + 6*B*a + 2*C*b)*elliptic_f(e/2 + f*x/2 - pi/4, 2)/(3*f),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*sin(e + f*x))**m*(c + d*sin(e + f*x))**n*(A + B*sin(e + f*x) + C*sin(e + f*x)**2),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((((Symbol('a') + (Symbol('b') * sympy.sin((Symbol('e') + (Symbol('f') * x))))))**(Symbol('m')) * ((Symbol('c') + (Symbol('d') * sympy.sin((Symbol('e') + (Symbol('f') * x))))))**(Symbol('n')) * (Symbol('A') + (Symbol('B') * sympy.sin((Symbol('e') + (Symbol('f') * x)))) + (Symbol('C') * (sympy.sin((Symbol('e') + (Symbol('f') * x))))**(Integer(2))))), x),
    ),
]
