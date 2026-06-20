# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.6 Cosecant/4.6.1.2 (d csc)^n (a+b csc)^m.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.6 Cosecant/4.6.1.2 (d csc)^n (a+b csc)^m.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e, f, m, n = symbols('a b c d e f m n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=csc(x)**5/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=cot(x)*csc(x)**3/(a*csc(x) + a) - 4*cot(x)**3/(3*a) + 3*cot(x)*csc(x)/(2*a) - 4*cot(x)/a + 3*atanh(cos(x))/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**4/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=cot(x)*csc(x)**2/(a*csc(x) + a) - 3*cot(x)*csc(x)/(2*a) + 2*cot(x)/a - 3*atanh(cos(x))/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(a*csc(x) + a),
        variable=x,
        num_steps=4,
        integral=-cot(x)/(a*csc(x) + a) - cot(x)/a + atanh(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a*csc(x) + a),
        variable=x,
        num_steps=3,
        integral=cot(x)/(a*csc(x) + a) - atanh(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(a*csc(x) + a),
        variable=x,
        num_steps=1,
        integral=-cot(x)/(a*csc(x) + a),
    ),
    RubiTestSuiteCase(
        integrand=1/(a*csc(c + d*x) + a),
        variable=x,
        num_steps=2,
        integral=cot(c + d*x)/(d*(a*csc(c + d*x) + a)) + x/a,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(a*csc(x) + a),
        variable=x,
        num_steps=4,
        integral=cos(x)/(a*csc(x) + a) - x/a - 2*cos(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(a*csc(x) + a),
        variable=x,
        num_steps=5,
        integral=sin(x)*cos(x)/(a*csc(x) + a) + 3*x/(2*a) - 3*sin(x)*cos(x)/(2*a) + 2*cos(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(a*csc(x) + a),
        variable=x,
        num_steps=6,
        integral=sin(x)**2*cos(x)/(a*csc(x) + a) - 3*x/(2*a) + 3*sin(x)*cos(x)/(2*a) + 4*cos(x)**3/(3*a) - 4*cos(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**4/(a*csc(x) + a),
        variable=x,
        num_steps=7,
        integral=sin(x)**3*cos(x)/(a*csc(x) + a) + 15*x/(8*a) - 5*sin(x)**3*cos(x)/(4*a) - 15*sin(x)*cos(x)/(8*a) - 4*cos(x)**3/(3*a) + 4*cos(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(c + d*x) + a)**(-2),
        variable=x,
        num_steps=3,
        integral=cot(c + d*x)/(3*d*(a*csc(c + d*x) + a)**2) + x/a**2 + 4*cot(c + d*x)/(3*a**2*d*(csc(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(c + d*x) + a)**(-3),
        variable=x,
        num_steps=4,
        integral=22*cot(c + d*x)/(15*d*(a**3*csc(c + d*x) + a**3)) + cot(c + d*x)/(5*d*(a*csc(c + d*x) + a)**3) + 7*cot(c + d*x)/(15*a*d*(a*csc(c + d*x) + a)**2) + x/a**3,
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(x) + a)**(sympy.S(5)/2),
        variable=x,
        num_steps=5,
        integral=-2*a**(sympy.S(5)/2)*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a)) - 14*a**3*cot(x)/(3*sqrt(a*csc(x) + a)) - 2*a**2*sqrt(a*csc(x) + a)*cot(x)/3,
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(x) + a)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-2*a**(sympy.S(3)/2)*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a)) - 2*a**2*cot(x)/sqrt(a*csc(x) + a),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(x) + a),
        variable=x,
        num_steps=2,
        integral=-2*sqrt(a)*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a*csc(x) + a),
        variable=x,
        num_steps=5,
        integral=-2*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a))/sqrt(a) + sqrt(2)*atan(sqrt(2)*sqrt(a)*cot(x)/(2*sqrt(a*csc(x) + a)))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(x) + a)**(sympy.S(-3)/2),
        variable=x,
        num_steps=6,
        integral=cot(x)/(2*(a*csc(x) + a)**(sympy.S(3)/2)) - 2*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a))/a**(sympy.S(3)/2) + 5*sqrt(2)*atan(sqrt(2)*sqrt(a)*cot(x)/(2*sqrt(a*csc(x) + a)))/(4*a**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(x) + a)**(sympy.S(-5)/2),
        variable=x,
        num_steps=7,
        integral=cot(x)/(4*(a*csc(x) + a)**(sympy.S(5)/2)) + 11*cot(x)/(16*a*(a*csc(x) + a)**(sympy.S(3)/2)) - 2*atan(sqrt(a)*cot(x)/sqrt(a*csc(x) + a))/a**(sympy.S(5)/2) + 43*sqrt(2)*atan(sqrt(2)*sqrt(a)*cot(x)/(2*sqrt(a*csc(x) + a)))/(32*a**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(e + f*x) + a)*sqrt(csc(e + f*x)),
        variable=x,
        num_steps=2,
        integral=-2*sqrt(a)*asinh(sqrt(a)*cot(e + f*x)/sqrt(a*csc(e + f*x) + a))/f,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-csc(e + f*x))*sqrt(-a*csc(e + f*x) + a),
        variable=x,
        num_steps=2,
        integral=-2*sqrt(a)*asinh(sqrt(a)*cot(e + f*x)/sqrt(-a*csc(e + f*x) + a))/f,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**(sympy.S(4)/3),
        variable=x,
        num_steps=4,
        integral=-4*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(sqrt(3) + 2)*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(5*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 6*a*cos(c + d*x)*csc(c + d*x)**(sympy.S(4)/3)/(5*d*sqrt(a*csc(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**(sympy.S(1)/3),
        variable=x,
        num_steps=3,
        integral=-2*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(sqrt(3) + 2)*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)/csc(c + d*x)**(sympy.S(2)/3),
        variable=x,
        num_steps=4,
        integral=-3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(sqrt(3) + 2)*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(2*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 3*a*cos(c + d*x)*csc(c + d*x)**(sympy.S(1)/3)/(2*d*sqrt(a*csc(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**(sympy.S(5)/3),
        variable=x,
        num_steps=6,
        integral=-12*3**(sympy.S(1)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(2 - sqrt(3))*cot(c + d*x)*elliptic_e(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(7*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) + 8*sqrt(2)*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(7*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 6*a*cos(c + d*x)*csc(c + d*x)**(sympy.S(5)/3)/(7*d*sqrt(a*csc(c + d*x) + a)) + 24*a*cot(c + d*x)/(7*d*sqrt(a*csc(c + d*x) + a)*(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**(sympy.S(2)/3),
        variable=x,
        num_steps=5,
        integral=-3*3**(sympy.S(1)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(2 - sqrt(3))*cot(c + d*x)*elliptic_e(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) + 2*sqrt(2)*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) + 6*a*cot(c + d*x)/(d*sqrt(a*csc(c + d*x) + a)*(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)/csc(c + d*x)**(sympy.S(1)/3),
        variable=x,
        num_steps=6,
        integral=3*3**(sympy.S(1)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(2 - sqrt(3))*cot(c + d*x)*elliptic_e(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(2*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - sqrt(2)*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 3*a*cos(c + d*x)*csc(c + d*x)**(sympy.S(2)/3)/(d*sqrt(a*csc(c + d*x) + a)) - 3*a*cot(c + d*x)/(d*sqrt(a*csc(c + d*x) + a)*(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)/csc(c + d*x)**(sympy.S(4)/3),
        variable=x,
        num_steps=7,
        integral=15*3**(sympy.S(1)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*sqrt(2 - sqrt(3))*cot(c + d*x)*elliptic_e(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(16*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 5*sqrt(2)*3**(sympy.S(3)/4)*a**2*sqrt((csc(c + d*x)**(sympy.S(2)/3) + csc(c + d*x)**(sympy.S(1)/3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(1 - csc(c + d*x)**(sympy.S(1)/3))*cot(c + d*x)*elliptic_f(asin((-csc(c + d*x)**(sympy.S(1)/3) - sqrt(3) + 1)/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))), -7 - 4*sqrt(3))/(8*d*sqrt((1 - csc(c + d*x)**(sympy.S(1)/3))/(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))**2)*(-a*csc(c + d*x) + a)*sqrt(a*csc(c + d*x) + a)) - 15*a*cos(c + d*x)*csc(c + d*x)**(sympy.S(2)/3)/(8*d*sqrt(a*csc(c + d*x) + a)) - 3*a*cos(c + d*x)/(4*d*sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**(sympy.S(1)/3)) - 15*a*cot(c + d*x)/(8*d*sqrt(a*csc(c + d*x) + a)*(-csc(c + d*x)**(sympy.S(1)/3) + 1 + sqrt(3))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*csc(c + d*x) + a)*csc(c + d*x)**n,
        variable=x,
        num_steps=2,
        integral=-2*a*cot(c + d*x)*hyper((sympy.S.Half, 1 - n), (sympy.S(3)/2,), 1 - csc(c + d*x))/(d*sqrt(a*csc(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-a*csc(c + d*x) + a)*csc(c + d*x)**n,
        variable=x,
        num_steps=3,
        integral=-2*a*cos(c + d*x)*csc(c + d*x)**(n + 1)*hyper((sympy.S.Half, 1 - n), (sympy.S(3)/2,), csc(c + d*x) + 1)/(d*(-csc(c + d*x))**n*sqrt(-a*csc(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m*csc(e + f*x)**3,
        variable=x,
        num_steps=5,
        integral=-2**(m + sympy.S.Half)*(a*csc(e + f*x) + a)**m*(csc(e + f*x) + 1)**(-m + sympy.S(-1)/2)*(m**2 + m + 1)*cot(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), sympy.S.Half - csc(e + f*x)/2)/(f*(m + 1)*(m + 2)) + (a*csc(e + f*x) + a)**m*cot(e + f*x)/(f*(m**2 + 3*m + 2)) - (a*csc(e + f*x) + a)**(m + 1)*cot(e + f*x)/(a*f*(m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m*csc(e + f*x)**2,
        variable=x,
        num_steps=4,
        integral=-2**(m + sympy.S.Half)*m*(a*csc(e + f*x) + a)**m*(csc(e + f*x) + 1)**(-m + sympy.S(-1)/2)*cot(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), sympy.S.Half - csc(e + f*x)/2)/(f*(m + 1)) - (a*csc(e + f*x) + a)**m*cot(e + f*x)/(f*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m*csc(e + f*x),
        variable=x,
        num_steps=3,
        integral=-2**(m + sympy.S.Half)*(a*csc(e + f*x) + a)**m*(csc(e + f*x) + 1)**(-m + sympy.S(-1)/2)*cot(e + f*x)*hyper((sympy.S.Half, sympy.S.Half - m), (sympy.S(3)/2,), sympy.S.Half - csc(e + f*x)/2)/f,
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m,
        variable=x,
        num_steps=3,
        integral=-sqrt(2)*(a*csc(e + f*x) + a)**m*cot(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, 1, m + sympy.S(3)/2, csc(e + f*x)/2 + sympy.S.Half, csc(e + f*x) + 1)/(f*sqrt(1 - csc(e + f*x))*(2*m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m*sin(e + f*x),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*(a*csc(e + f*x) + a)**m*cot(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, 2, m + sympy.S(3)/2, csc(e + f*x)/2 + sympy.S.Half, csc(e + f*x) + 1)/(f*sqrt(1 - csc(e + f*x))*(2*m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x) + a)**m*sin(e + f*x)**2,
        variable=x,
        num_steps=3,
        integral=-sqrt(2)*(a*csc(e + f*x) + a)**m*cot(e + f*x)*appellf1(m + sympy.S.Half, sympy.S.Half, 3, m + sympy.S(3)/2, csc(e + f*x)/2 + sympy.S.Half, csc(e + f*x) + 1)/(f*sqrt(1 - csc(e + f*x))*(2*m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**4,
        variable=x,
        num_steps=6,
        integral=a**4*x - 4*a*b**3*cot(c + d*x)*csc(c + d*x)/(3*d) - 2*a*b*(2*a**2 + b**2)*atanh(cos(c + d*x))/d - b**2*(a + b*csc(c + d*x))**2*cot(c + d*x)/(3*d) - b**2*(17*a**2 + 2*b**2)*cot(c + d*x)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**3,
        variable=x,
        num_steps=5,
        integral=a**3*x - 5*a*b**2*cot(c + d*x)/(2*d) - b**2*(a + b*csc(c + d*x))*cot(c + d*x)/(2*d) - b*(6*a**2 + b**2)*atanh(cos(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**2,
        variable=x,
        num_steps=4,
        integral=a**2*x - 2*a*b*atanh(cos(c + d*x))/d - b**2*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**5/(a + b*csc(x)),
        variable=x,
        num_steps=9,
        integral=-2*a**4*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(b**4*sqrt(a**2 - b**2)) + a*cot(x)*csc(x)/(2*b**2) + a*(2*a**2 + b**2)*atanh(cos(x))/(2*b**4) - cot(x)*csc(x)**2/(3*b) - (3*a**2 + 2*b**2)*cot(x)/(3*b**3),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**4/(a + b*csc(x)),
        variable=x,
        num_steps=8,
        integral=2*a**3*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(b**3*sqrt(a**2 - b**2)) + a*cot(x)/b**2 - cot(x)*csc(x)/(2*b) - (2*a**2 + b**2)*atanh(cos(x))/(2*b**3),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(a + b*csc(x)),
        variable=x,
        num_steps=7,
        integral=-2*a**2*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(b**2*sqrt(a**2 - b**2)) + a*atanh(cos(x))/b**2 - cot(x)/b,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(a + b*csc(x)),
        variable=x,
        num_steps=6,
        integral=2*a*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(b*sqrt(a**2 - b**2)) - atanh(cos(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(a + b*csc(x)),
        variable=x,
        num_steps=4,
        integral=-2*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/sqrt(a**2 - b**2),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*csc(c + d*x)),
        variable=x,
        num_steps=4,
        integral=2*b*atanh((a + b*tan(c/2 + d*x/2))/sqrt(a**2 - b**2))/(a*d*sqrt(a**2 - b**2)) + x/a,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(a + b*csc(x)),
        variable=x,
        num_steps=6,
        integral=-cos(x)/a - 2*b**2*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**2*sqrt(a**2 - b**2)) - b*x/a**2,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(a + b*csc(x)),
        variable=x,
        num_steps=7,
        integral=-sin(x)*cos(x)/(2*a) + b*cos(x)/a**2 + 2*b**3*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**3*sqrt(a**2 - b**2)) + x*(a**2 + 2*b**2)/(2*a**3),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(a + b*csc(x)),
        variable=x,
        num_steps=8,
        integral=-sin(x)**2*cos(x)/(3*a) + b*sin(x)*cos(x)/(2*a**2) - (2*a**2 + 3*b**2)*cos(x)/(3*a**3) - 2*b**4*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**4*sqrt(a**2 - b**2)) - b*x*(a**2 + 2*b**2)/(2*a**4),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**4/(a + b*csc(x)),
        variable=x,
        num_steps=9,
        integral=-sin(x)**3*cos(x)/(4*a) + b*sin(x)**2*cos(x)/(3*a**2) - (3*a**2 + 4*b**2)*sin(x)*cos(x)/(8*a**3) + b*(2*a**2 + 3*b**2)*cos(x)/(3*a**4) + 2*b**5*atanh((a + b*tan(x/2))/sqrt(a**2 - b**2))/(a**5*sqrt(a**2 - b**2)) + x*(3*a**4 + 4*a**2*b**2 + 8*b**4)/(8*a**5),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**(-2),
        variable=x,
        num_steps=6,
        integral=-b**2*cot(c + d*x)/(a*d*(a + b*csc(c + d*x))*(a**2 - b**2)) + 2*b*(2*a**2 - b**2)*atanh((a + b*tan(c/2 + d*x/2))/sqrt(a**2 - b**2))/(a**2*d*(a**2 - b**2)**(sympy.S(3)/2)) + x/a**2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**(-3),
        variable=x,
        num_steps=7,
        integral=-b**2*cot(c + d*x)/(2*a*d*(a + b*csc(c + d*x))**2*(a**2 - b**2)) - b**2*(5*a**2 - 2*b**2)*cot(c + d*x)/(2*a**2*d*(a + b*csc(c + d*x))*(a**2 - b**2)**2) + b*(6*a**4 - 5*a**2*b**2 + 2*b**4)*atanh((a + b*tan(c/2 + d*x/2))/sqrt(a**2 - b**2))/(a**3*d*(a**2 - b**2)**(sympy.S(5)/2)) + x/a**3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x))**(-4),
        variable=x,
        num_steps=8,
        integral=-b**2*cot(c + d*x)/(3*a*d*(a + b*csc(c + d*x))**3*(a**2 - b**2)) - b**2*(8*a**2 - 3*b**2)*cot(c + d*x)/(6*a**2*d*(a + b*csc(c + d*x))**2*(a**2 - b**2)**2) - b**2*(26*a**4 - 17*a**2*b**2 + 6*b**4)*cot(c + d*x)/(6*a**3*d*(a + b*csc(c + d*x))*(a**2 - b**2)**3) + b*(8*a**6 - 8*a**4*b**2 + 7*a**2*b**4 - 2*b**6)*atanh((a + b*tan(c/2 + d*x/2))/sqrt(a**2 - b**2))/(a**4*d*(a**2 - b**2)**(sympy.S(7)/2)) + x/a**4,
    ),
    RubiTestSuiteCase(
        integrand=1/(5*csc(c + d*x) + 3),
        variable=x,
        num_steps=2,
        integral=-x/12 - 5*atan(cos(c + d*x)/(sin(c + d*x) + 3))/(6*d),
    ),
    RubiTestSuiteCase(
        integrand=1/(3*csc(c + d*x) + 5),
        variable=x,
        num_steps=5,
        integral=x/5 + 3*log(sin(c/2 + d*x/2) + 3*cos(c/2 + d*x/2))/(20*d) - 3*log(3*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(20*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m*csc(e + f*x)**3,
        variable=x,
        num_steps=8,
        integral=sqrt(2)*a*(a + b)*(a + b*csc(e + f*x))**m*cot(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m - 1, sympy.S(3)/2, sympy.S.Half - csc(e + f*x)/2, b*(1 - csc(e + f*x))/(a + b))/(b**2*f*((a + b*csc(e + f*x))/(a + b))**m*(m + 2)*sqrt(csc(e + f*x) + 1)) - (a + b*csc(e + f*x))**(m + 1)*cot(e + f*x)/(b*f*(m + 2)) - sqrt(2)*(a + b*csc(e + f*x))**m*(a**2 + b**2*(m + 1))*cot(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m, sympy.S(3)/2, sympy.S.Half - csc(e + f*x)/2, b*(1 - csc(e + f*x))/(a + b))/(b**2*f*((a + b*csc(e + f*x))/(a + b))**m*(m + 2)*sqrt(csc(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m*csc(e + f*x)**2,
        variable=x,
        num_steps=7,
        integral=sqrt(2)*a*(a + b*csc(e + f*x))**m*cot(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m, sympy.S(3)/2, sympy.S.Half - csc(e + f*x)/2, b*(1 - csc(e + f*x))/(a + b))/(b*f*((a + b*csc(e + f*x))/(a + b))**m*sqrt(csc(e + f*x) + 1)) - sqrt(2)*(a + b)*(a + b*csc(e + f*x))**m*cot(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m - 1, sympy.S(3)/2, sympy.S.Half - csc(e + f*x)/2, b*(1 - csc(e + f*x))/(a + b))/(b*f*((a + b*csc(e + f*x))/(a + b))**m*sqrt(csc(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m*csc(e + f*x),
        variable=x,
        num_steps=3,
        integral=-sqrt(2)*(a + b*csc(e + f*x))**m*cot(e + f*x)*appellf1(sympy.S.Half, sympy.S.Half, -m, sympy.S(3)/2, sympy.S.Half - csc(e + f*x)/2, b*(1 - csc(e + f*x))/(a + b))/(f*((a + b*csc(e + f*x))/(a + b))**m*sqrt(csc(e + f*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')(((Symbol('a') + (Symbol('b') * sympy.csc((Symbol('e') + (Symbol('f') * x))))))**(Symbol('m')), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m*sin(e + f*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((((Symbol('a') + (Symbol('b') * sympy.csc((Symbol('e') + (Symbol('f') * x))))))**(Symbol('m')) * sympy.sin((Symbol('e') + (Symbol('f') * x)))), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(e + f*x))**m*sin(e + f*x)**2,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((((Symbol('a') + (Symbol('b') * sympy.csc((Symbol('e') + (Symbol('f') * x))))))**(Symbol('m')) * (sympy.sin((Symbol('e') + (Symbol('f') * x))))**(Integer(2))), x),
    ),
]
