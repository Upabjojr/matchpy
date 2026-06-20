# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.2 Cosine/4.2.1.3 (g tan)^p (a+b cos)^m.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.2 Cosine/4.2.1.3 (g tan)^p (a+b cos)^m.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e, f, g, m, p = symbols('a b c d e f g m p')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=tan(x)**4/(a*cos(x) + a),
        variable=x,
        num_steps=5,
        integral=tan(x)**3/(3*a) - tan(x)*sec(x)/(2*a) + atanh(sin(x))/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**3/(a*cos(x) + a),
        variable=x,
        num_steps=5,
        integral=sec(x)**2/(2*a) - sec(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/(a*cos(x) + a),
        variable=x,
        num_steps=4,
        integral=tan(x)/a - atanh(sin(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/(a*cos(x) + a),
        variable=x,
        num_steps=4,
        integral=log(cos(x) + 1)/a - log(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a*cos(x) + a),
        variable=x,
        num_steps=5,
        integral=cot(x)*csc(x)/(2*a) - atanh(cos(x))/(2*a) - csc(x)**2/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/(a*cos(x) + a),
        variable=x,
        num_steps=5,
        integral=-cot(x)**3/(3*a) + csc(x)**3/(3*a) - csc(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/(a*cos(x) + a),
        variable=x,
        num_steps=6,
        integral=-cot(x)**4/(4*a) + cot(x)**3*csc(x)/(4*a) - 3*cot(x)*csc(x)/(8*a) + 3*atanh(cos(x))/(8*a),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**4/(a*cos(x) + a),
        variable=x,
        num_steps=6,
        integral=-cot(x)**5/(5*a) + csc(x)**5/(5*a) - 2*csc(x)**3/(3*a) + csc(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=tan(3*x)/(cos(3*x) + 1)**2,
        variable=x,
        num_steps=3,
        integral=log(cos(3*x) + 1)/3 - log(cos(3*x))/3 - 1/(3*cos(3*x) + 3),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**4/(a + b*cos(x)),
        variable=x,
        num_steps=6,
        integral=tan(x)*sec(x)**2/(3*a) - b*tan(x)*sec(x)/(2*a**2) - (4*a**2 - 3*b**2)*tan(x)/(3*a**3) + b*(3*a**2 - 2*b**2)*atanh(sin(x))/(2*a**4) + 2*(a - b)**(sympy.S(3)/2)*(a + b)**(sympy.S(3)/2)*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/a**4,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**3/(a + b*cos(x)),
        variable=x,
        num_steps=3,
        integral=sec(x)**2/(2*a) - b*sec(x)/a**2 - (a**2 - b**2)*log(a + b*cos(x))/a**3 + (a**2 - b**2)*log(cos(x))/a**3,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/(a + b*cos(x)),
        variable=x,
        num_steps=6,
        integral=tan(x)/a - b*atanh(sin(x))/a**2 - 2*sqrt(a - b)*sqrt(a + b)*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/a**2,
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/(a + b*cos(x)),
        variable=x,
        num_steps=4,
        integral=log(a + b*cos(x))/a - log(cos(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a + b*cos(x)),
        variable=x,
        num_steps=3,
        integral=-a*log(a + b*cos(x))/(a**2 - b**2) + log(1 - cos(x))/(2*a + 2*b) + log(cos(x) + 1)/(2*a - 2*b),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/(a + b*cos(x)),
        variable=x,
        num_steps=7,
        integral=-2*a**2*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/((a - b)**(sympy.S(3)/2)*(a + b)**(sympy.S(3)/2)) - a*cot(x)/(a**2 - b**2) + b*csc(x)/(a**2 - b**2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/(a + b*cos(x)),
        variable=x,
        num_steps=4,
        integral=a**3*log(a + b*cos(x))/(a**2 - b**2)**2 - (a - b*cos(x))*csc(x)**2/(2*a**2 - 2*b**2) - (2*a + b)*log(1 - cos(x))/(4*(a + b)**2) - (2*a - b)*log(cos(x) + 1)/(4*(a - b)**2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**4/(a + b*cos(x)),
        variable=x,
        num_steps=12,
        integral=2*a**4*atan(sqrt(a - b)*tan(x/2)/sqrt(a + b))/((a - b)**(sympy.S(5)/2)*(a + b)**(sympy.S(5)/2)) + a**3*cot(x)/(a**2 - b**2)**2 - a**2*b*csc(x)/(a**2 - b**2)**2 - a*cot(x)**3/(3*a**2 - 3*b**2) + b*csc(x)**3/(3*a**2 - 3*b**2) - b*csc(x)/(a**2 - b**2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/sqrt(3 - cos(x)),
        variable=x,
        num_steps=5,
        integral=-sqrt(2)*atanh(sqrt(2)*sqrt(3 - cos(x))/2)/2 - atanh(sqrt(3 - cos(x))/2)/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cos(x))*tan(x),
        variable=x,
        num_steps=4,
        integral=2*sqrt(a)*atanh(sqrt(a + b*cos(x))/sqrt(a)) - 2*sqrt(a + b*cos(x)),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/sqrt(a + b*cos(x)),
        variable=x,
        num_steps=3,
        integral=2*atanh(sqrt(a + b*cos(x))/sqrt(a))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(e*tan(c + d*x))/(a + b*cos(c + d*x)),
        variable=x,
        num_steps=9,
        integral=((Integer(-1) * ((Integer(2) * sympy.sqrt(Integer(2)) * sympy.sqrt(sympy.cos((Symbol('c') + (Symbol('d') * x)))) * sympy.Function('EllipticPi')((Integer(-1) * (sympy.sqrt(((Integer(-1) * Symbol('a')) + Symbol('b'))) * (sympy.sqrt((Symbol('a') + Symbol('b'))))**(Integer(-1)))), sympy.asin((sympy.sqrt(sympy.sin((Symbol('c') + (Symbol('d') * x)))) * (sympy.sqrt((Integer(1) + sympy.cos((Symbol('c') + (Symbol('d') * x))))))**(Integer(-1)))), Integer(-1)) * sympy.sqrt((Symbol('e') * sympy.tan((Symbol('c') + (Symbol('d') * x)))))) * ((sympy.sqrt(((Integer(-1) * Symbol('a')) + Symbol('b'))) * sympy.sqrt((Symbol('a') + Symbol('b'))) * Symbol('d') * sympy.sqrt(sympy.sin((Symbol('c') + (Symbol('d') * x))))))**(Integer(-1)))) + ((Integer(2) * sympy.sqrt(Integer(2)) * sympy.sqrt(sympy.cos((Symbol('c') + (Symbol('d') * x)))) * sympy.Function('EllipticPi')((sympy.sqrt(((Integer(-1) * Symbol('a')) + Symbol('b'))) * (sympy.sqrt((Symbol('a') + Symbol('b'))))**(Integer(-1))), sympy.asin((sympy.sqrt(sympy.sin((Symbol('c') + (Symbol('d') * x)))) * (sympy.sqrt((Integer(1) + sympy.cos((Symbol('c') + (Symbol('d') * x))))))**(Integer(-1)))), Integer(-1)) * sympy.sqrt((Symbol('e') * sympy.tan((Symbol('c') + (Symbol('d') * x)))))) * ((sympy.sqrt(((Integer(-1) * Symbol('a')) + Symbol('b'))) * sympy.sqrt((Symbol('a') + Symbol('b'))) * Symbol('d') * sympy.sqrt(sympy.sin((Symbol('c') + (Symbol('d') * x))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(g*tan(e + f*x))**p*(a + b*cos(e + f*x))**m,
        variable=x,
        num_steps=1,
        integral=(((Symbol('g') * sympy.cot((Symbol('e') + (Symbol('f') * x)))))**(Symbol('p')) * ((Symbol('g') * sympy.tan((Symbol('e') + (Symbol('f') * x)))))**(Symbol('p')) * sympy.Function('Unintegrable')((((Symbol('a') + (Symbol('b') * sympy.cos((Symbol('e') + (Symbol('f') * x))))))**(Symbol('m')) * (((Symbol('g') * sympy.cot((Symbol('e') + (Symbol('f') * x)))))**(Symbol('p')))**(Integer(-1))), x)),
    ),
]
