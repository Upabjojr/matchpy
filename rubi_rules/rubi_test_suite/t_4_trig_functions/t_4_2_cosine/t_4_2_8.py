# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.2 Cosine/4.2.8 (a+b cos)^m (c+d trig)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.2 Cosine/4.2.8 (a+b cos)^m (c+d trig)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, C, a, b, c, d, e, f = symbols('A B C a b c d e f')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A + B*sin(x))/(a + b*cos(x)),
        variable=x,
        num_steps=6,
        integral=2*A*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)) - B*log(a + b*cos(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sin(x))/(cos(x) + 1),
        variable=x,
        num_steps=5,
        integral=A*sin(x)/(cos(x) + 1) - B*log(cos(x) + 1),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sin(x))/(1 - cos(x)),
        variable=x,
        num_steps=5,
        integral=-A*sin(x)/(1 - cos(x)) + B*log(1 - cos(x)),
    ),
    RubiTestSuiteCase(
        integrand=(b + c + sin(x))/(a + b*cos(x)),
        variable=x,
        num_steps=6,
        integral=(2*b + 2*c)*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)) - log(a + b*cos(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(b + c + sin(x))/(a - b*cos(x)),
        variable=x,
        num_steps=6,
        integral=(2*b + 2*c)*atan(sqrt(a + b)*tan(x/2)/sqrt(a - b))/(sqrt(a - b)*sqrt(a + b)) + log(a - b*cos(x))/b,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*tan(x))/(a + b*cos(x)),
        variable=x,
        num_steps=8,
        integral=2*A*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)) + B*log(a + b*cos(x))/a - B*log(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cot(x))/(a + b*cos(x)),
        variable=x,
        num_steps=7,
        integral=2*A*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)) - B*a*log(a + b*cos(x))/(a**2 - b**2) + B*log(1 - cos(x))/(2*a + 2*b) + B*log(cos(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*csc(x))/(a + b*cos(x)),
        variable=x,
        num_steps=11,
        integral=2*A*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/(sqrt(a - b)*sqrt(a + b)) + B*b*log(a + b*cos(x))/(a**2 - b**2) + B*log(1 - cos(x))/(2*a + 2*b) - B*log(cos(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sec(e + f*x))**4/(a + b*cos(e + f*x)),
        variable=x,
        num_steps=12,
        integral=d**4*tan(e + f*x)**3/(3*a*f) + d**4*tan(e + f*x)/(a*f) + d**3*(4*a*c - b*d)*tan(e + f*x)*sec(e + f*x)/(2*a**2*f) + d**3*(4*a*c - b*d)*atanh(sin(e + f*x))/(2*a**2*f) + d**2*(6*a**2*c**2 - 4*a*b*c*d + b**2*d**2)*tan(e + f*x)/(a**3*f) + d*(2*a*c - b*d)*(2*a**2*c**2 - 2*a*b*c*d + b**2*d**2)*atanh(sin(e + f*x))/(a**4*f) + 2*(a*c - b*d)**4*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(a**4*f*sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sec(e + f*x))**3/(a + b*cos(e + f*x)),
        variable=x,
        num_steps=10,
        integral=d**3*tan(e + f*x)*sec(e + f*x)/(2*a*f) + d**3*atanh(sin(e + f*x))/(2*a*f) + d**2*(3*a*c - b*d)*tan(e + f*x)/(a**2*f) + d*(3*a**2*c**2 - 3*a*b*c*d + b**2*d**2)*atanh(sin(e + f*x))/(a**3*f) + 2*(a*c - b*d)**3*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(a**3*f*sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sec(e + f*x))**2/(a + b*cos(e + f*x)),
        variable=x,
        num_steps=8,
        integral=d**2*tan(e + f*x)/(a*f) + d*(2*a*c - b*d)*atanh(sin(e + f*x))/(a**2*f) + 2*(a*c - b*d)**2*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(a**2*f*sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*sec(e + f*x))/(a + b*cos(e + f*x)),
        variable=x,
        num_steps=5,
        integral=d*atanh(sin(e + f*x))/(a*f) + (2*a*c - 2*b*d)*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(a*f*sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=1/((a + b*cos(e + f*x))*(c + d*sec(e + f*x))),
        variable=x,
        num_steps=6,
        integral=2*a*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(f*sqrt(a - b)*sqrt(a + b)*(a*c - b*d)) - 2*d*atanh(sqrt(c - d)*tan(e/2 + f*x/2)/sqrt(c + d))/(f*sqrt(c - d)*sqrt(c + d)*(a*c - b*d)),
    ),
    RubiTestSuiteCase(
        integrand=1/((a + b*cos(e + f*x))*(c + d*sec(e + f*x))**2),
        variable=x,
        num_steps=7,
        integral=2*a**2*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(f*sqrt(a - b)*sqrt(a + b)*(a*c - b*d)**2) + d**2*sin(e + f*x)/(f*(c**2 - d**2)*(a*c - b*d)*(c*cos(e + f*x) + d)) - 2*d*(2*a*c**2 - a*d**2 - b*c*d)*atanh(sqrt(c - d)*tan(e/2 + f*x/2)/sqrt(c + d))/(f*(c - d)**(sympy.S(3)/2)*(c + d)**(sympy.S(3)/2)*(a*c - b*d)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/((a + b*cos(e + f*x))*(c + d*sec(e + f*x))**3),
        variable=x,
        num_steps=16,
        integral=2*a**3*atan(sqrt(a - b)*tan(e/2 + f*x/2)/sqrt(a + b))/(f*sqrt(a - b)*sqrt(a + b)*(a*c - b*d)**3) + 3*d**4*sin(e + f*x)/(2*c*f*(c**2 - d**2)**2*(a*c - b*d)*(c*cos(e + f*x) + d)) - d**3*sin(e + f*x)/(2*c*f*(c**2 - d**2)*(a*c - b*d)*(c*cos(e + f*x) + d)**2) + d**2*(3*a*c - 2*b*d)*sin(e + f*x)/(c*f*(c**2 - d**2)*(a*c - b*d)**2*(c*cos(e + f*x) + d)) - 2*d**3*(3*a*c - 2*b*d)*atanh(sqrt(c - d)*tan(e/2 + f*x/2)/sqrt(c + d))/(c**2*f*(c - d)**(sympy.S(3)/2)*(c + d)**(sympy.S(3)/2)*(a*c - b*d)**2) - d**3*(c**2 + 2*d**2)*atanh(sqrt(c - d)*tan(e/2 + f*x/2)/sqrt(c + d))/(c**2*f*(c - d)**(sympy.S(5)/2)*(c + d)**(sympy.S(5)/2)*(a*c - b*d)) - 2*d*(3*a**2*c**2 - 3*a*b*c*d + b**2*d**2)*atanh(sqrt(c - d)*tan(e/2 + f*x/2)/sqrt(c + d))/(c**2*f*sqrt(c - d)*sqrt(c + d)*(a*c - b*d)**3),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(c + d*sec(e + f*x))/(a + b*cos(e + f*x)),
        variable=x,
        num_steps=4,
        integral=(((Integer(2) * sympy.sqrt((Symbol('c') + Symbol('d'))) * sympy.cot((Symbol('e') + (Symbol('f') * x))) * sympy.elliptic_f(sympy.asin((sympy.sqrt((Symbol('c') + (Symbol('d') * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * (sympy.sqrt((Symbol('c') + Symbol('d'))))**(Integer(-1)))), ((Symbol('c') + Symbol('d')) * ((Symbol('c') + (Integer(-1) * Symbol('d'))))**(Integer(-1)))) * sympy.sqrt(((Symbol('d') * (Integer(1) + (Integer(-1) * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * ((Symbol('c') + Symbol('d')))**(Integer(-1)))) * sympy.sqrt((Integer(-1) * ((Symbol('d') * (Integer(1) + sympy.sec((Symbol('e') + (Symbol('f') * x))))) * ((Symbol('c') + (Integer(-1) * Symbol('d'))))**(Integer(-1)))))) * ((Symbol('a') * Symbol('f')))**(Integer(-1))) + ((Integer(2) * ((Symbol('a') * Symbol('c')) + (Integer(-1) * (Symbol('b') * Symbol('d')))) * sympy.Function('EllipticPi')(((Integer(2) * Symbol('a')) * ((Symbol('a') + Symbol('b')))**(Integer(-1))), sympy.asin((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * (sympy.sqrt(Integer(2)))**(Integer(-1)))), ((Integer(2) * Symbol('d')) * ((Symbol('c') + Symbol('d')))**(Integer(-1)))) * sympy.sqrt(((Symbol('c') + (Symbol('d') * sympy.sec((Symbol('e') + (Symbol('f') * x))))) * ((Symbol('c') + Symbol('d')))**(Integer(-1)))) * sympy.tan((Symbol('e') + (Symbol('f') * x)))) * ((Symbol('a') * (Symbol('a') + Symbol('b')) * Symbol('f') * sympy.sqrt((Symbol('c') + (Symbol('d') * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * sympy.sqrt((Integer(-1) * (sympy.tan((Symbol('e') + (Symbol('f') * x))))**(Integer(2))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=1/((a + b*cos(e + f*x))*sqrt(c + d*sec(e + f*x))),
        variable=x,
        num_steps=2,
        integral=((Integer(2) * sympy.Function('EllipticPi')(((Integer(2) * Symbol('a')) * ((Symbol('a') + Symbol('b')))**(Integer(-1))), sympy.asin((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * (sympy.sqrt(Integer(2)))**(Integer(-1)))), ((Integer(2) * Symbol('d')) * ((Symbol('c') + Symbol('d')))**(Integer(-1)))) * sympy.sqrt(((Symbol('c') + (Symbol('d') * sympy.sec((Symbol('e') + (Symbol('f') * x))))) * ((Symbol('c') + Symbol('d')))**(Integer(-1)))) * sympy.tan((Symbol('e') + (Symbol('f') * x)))) * (((Symbol('a') + Symbol('b')) * Symbol('f') * sympy.sqrt((Symbol('c') + (Symbol('d') * sympy.sec((Symbol('e') + (Symbol('f') * x)))))) * sympy.sqrt((Integer(-1) * (sympy.tan((Symbol('e') + (Symbol('f') * x))))**(Integer(2))))))**(Integer(-1))),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(d + e*x) + C*sin(d + e*x))/(a + b*cos(d + e*x)),
        variable=x,
        num_steps=6,
        integral=B*x/b - C*log(a + b*cos(d + e*x))/(b*e) + (2*A*b - 2*B*a)*atan(sqrt(a - b)*tan(d/2 + e*x/2)/sqrt(a + b))/(b*e*sqrt(a - b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(d + e*x) + C*sin(d + e*x))/(a + b*cos(d + e*x))**2,
        variable=x,
        num_steps=7,
        integral=C/(b*e*(a + b*cos(d + e*x))) - (A*b - B*a)*sin(d + e*x)/(e*(a + b*cos(d + e*x))*(a**2 - b**2)) + (2*A*a - 2*B*b)*atan(sqrt(a - b)*tan(d/2 + e*x/2)/sqrt(a + b))/(e*(a - b)**(sympy.S(3)/2)*(a + b)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(d + e*x) + C*sin(d + e*x))/(a + b*cos(d + e*x))**3,
        variable=x,
        num_steps=8,
        integral=C/(2*b*e*(a + b*cos(d + e*x))**2) - (3*A*a*b - B*a**2 - 2*B*b**2)*sin(d + e*x)/(2*e*(a + b*cos(d + e*x))*(a**2 - b**2)**2) - (A*b - B*a)*sin(d + e*x)/(e*(a + b*cos(d + e*x))**2*(2*a**2 - 2*b**2)) + (2*A*a**2 + A*b**2 - 3*B*a*b)*atan(sqrt(a - b)*tan(d/2 + e*x/2)/sqrt(a + b))/(e*(a - b)**(sympy.S(5)/2)*(a + b)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*cos(d + e*x) + C*sin(d + e*x))/(a + b*cos(d + e*x))**4,
        variable=x,
        num_steps=9,
        integral=C/(3*b*e*(a + b*cos(d + e*x))**3) - (11*A*a**2*b + 4*A*b**3 - 2*B*a**3 - 13*B*a*b**2)*sin(d + e*x)/(6*e*(a + b*cos(d + e*x))*(a**2 - b**2)**3) - (5*A*a*b - 2*B*a**2 - 3*B*b**2)*sin(d + e*x)/(6*e*(a + b*cos(d + e*x))**2*(a**2 - b**2)**2) - (A*b - B*a)*sin(d + e*x)/(e*(a + b*cos(d + e*x))**3*(3*a**2 - 3*b**2)) + (2*A*a**3 + 3*A*a*b**2 - 4*B*a**2*b - B*b**3)*atan(sqrt(a - b)*tan(d/2 + e*x/2)/sqrt(a + b))/(e*(a - b)**(sympy.S(7)/2)*(a + b)**(sympy.S(7)/2)),
    ),
]
