# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.6 Cosecant/4.6.7 (d trig)^m (a+b (c csc)^n)^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.6 Cosecant/4.6.7 (d trig)^m (a+b (c csc)^n)^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d = symbols('a b c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**4,
        variable=x,
        num_steps=4,
        integral=a**4*x - b**4*cot(c + d*x)**7/(7*d) - b**3*(4*a + 3*b)*cot(c + d*x)**5/(5*d) - b**2*(6*a**2 + 8*a*b + 3*b**2)*cot(c + d*x)**3/(3*d) - b*(2*a + b)*(2*a**2 + 2*a*b + b**2)*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**3,
        variable=x,
        num_steps=4,
        integral=a**3*x - b**3*cot(c + d*x)**5/(5*d) - b**2*(3*a + 2*b)*cot(c + d*x)**3/(3*d) - b*(3*a**2 + 3*a*b + b**2)*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**2,
        variable=x,
        num_steps=4,
        integral=a**2*x - b**2*cot(c + d*x)**3/(3*d) - b*(2*a + b)*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=a + b*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=a*x - b*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*csc(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=-sqrt(b)*atan(sqrt(a + b)*tan(c + d*x)/sqrt(b))/(a*d*sqrt(a + b)) + x/a,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(-2),
        variable=x,
        num_steps=5,
        integral=b*cot(c + d*x)/(2*a*d*(a + b)*(a + b*cot(c + d*x)**2 + b)) + sqrt(b)*(3*a + 2*b)*atan(sqrt(b)*cot(c + d*x)/sqrt(a + b))/(2*a**2*d*(a + b)**(sympy.S(3)/2)) + x/a**2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(-3),
        variable=x,
        num_steps=6,
        integral=b*cot(c + d*x)/(4*a*d*(a + b)*(a + b*cot(c + d*x)**2 + b)**2) + b*(7*a + 4*b)*cot(c + d*x)/(8*a**2*d*(a + b)**2*(a + b*cot(c + d*x)**2 + b)) + sqrt(b)*(15*a**2 + 20*a*b + 8*b**2)*atan(sqrt(b)*cot(c + d*x)/sqrt(a + b))/(8*a**3*d*(a + b)**(sympy.S(5)/2)) + x/a**3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(-4),
        variable=x,
        num_steps=7,
        integral=b*cot(c + d*x)/(6*a*d*(a + b)*(a + b*cot(c + d*x)**2 + b)**3) + b*(11*a + 6*b)*cot(c + d*x)/(24*a**2*d*(a + b)**2*(a + b*cot(c + d*x)**2 + b)**2) + b*(19*a**2 + 22*a*b + 8*b**2)*cot(c + d*x)/(16*a**3*d*(a + b)**3*(a + b*cot(c + d*x)**2 + b)) + sqrt(b)*(35*a**3 + 70*a**2*b + 56*a*b**2 + 16*b**3)*atan(sqrt(b)*cot(c + d*x)/sqrt(a + b))/(16*a**4*d*(a + b)**(sympy.S(7)/2)) + x/a**4,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=8,
        integral=-a**(sympy.S(5)/2)*atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/d - sqrt(b)*(15*a**2 + 10*a*b + 3*b**2)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/(8*d) - b*(7*a + 3*b)*sqrt(a + b*cot(c + d*x)**2 + b)*cot(c + d*x)/(8*d) - b*(a + b*cot(c + d*x)**2 + b)**(sympy.S(3)/2)*cot(c + d*x)/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-a**(sympy.S(3)/2)*atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/d - sqrt(b)*(3*a + b)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/(2*d) - b*sqrt(a + b*cot(c + d*x)**2 + b)*cot(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*csc(c + d*x)**2),
        variable=x,
        num_steps=6,
        integral=-sqrt(a)*atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/d - sqrt(b)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(sympy.S(-3)/2),
        variable=x,
        num_steps=4,
        integral=b*cot(c + d*x)/(a*d*(a + b)*sqrt(a + b*cot(c + d*x)**2 + b)) - atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/(a**(sympy.S(3)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(sympy.S(-5)/2),
        variable=x,
        num_steps=6,
        integral=b*cot(c + d*x)/(3*a*d*(a + b)*(a + b*cot(c + d*x)**2 + b)**(sympy.S(3)/2)) + b*(5*a + 3*b)*cot(c + d*x)/(3*a**2*d*(a + b)**2*sqrt(a + b*cot(c + d*x)**2 + b)) - atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/(a**(sympy.S(5)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csc(c + d*x)**2)**(sympy.S(-7)/2),
        variable=x,
        num_steps=7,
        integral=b*cot(c + d*x)/(5*a*d*(a + b)*(a + b*cot(c + d*x)**2 + b)**(sympy.S(5)/2)) + b*(9*a + 5*b)*cot(c + d*x)/(15*a**2*d*(a + b)**2*(a + b*cot(c + d*x)**2 + b)**(sympy.S(3)/2)) + b*(33*a**2 + 40*a*b + 15*b**2)*cot(c + d*x)/(15*a**3*d*(a + b)**3*sqrt(a + b*cot(c + d*x)**2 + b)) - atan(sqrt(a)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2 + b))/(a**(sympy.S(7)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(csc(x)**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=-sqrt(cot(x)**2 + 2)*cot(x)/2 - 2*asinh(sqrt(2)*cot(x)/2) - atan(cot(x)/sqrt(cot(x)**2 + 2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(csc(x)**2 + 1),
        variable=x,
        num_steps=5,
        integral=-asinh(sqrt(2)*cot(x)/2) - atan(cot(x)/sqrt(cot(x)**2 + 2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(csc(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=-atan(cot(x)/sqrt(cot(x)**2 + 2)),
    ),
    RubiTestSuiteCase(
        integrand=(1 - csc(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=sqrt(-cot(x)**2)*log(sin(x))*tan(x) + sqrt(-cot(x)**2)*cot(x)/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 - csc(x)**2),
        variable=x,
        num_steps=3,
        integral=sqrt(-cot(x)**2)*log(sin(x))*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(1 - csc(x)**2),
        variable=x,
        num_steps=3,
        integral=-log(cos(x))*cot(x)/sqrt(-cot(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=(csc(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-(cot(x)**2)**(sympy.S(3)/2)*tan(x)/2 - sqrt(cot(x)**2)*log(sin(x))*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(csc(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=sqrt(cot(x)**2)*log(sin(x))*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(csc(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=-log(cos(x))*cot(x)/sqrt(cot(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=(-csc(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=sqrt(-cot(x)**2 - 2)*cot(x)/2 - 2*atan(cot(x)/sqrt(-cot(x)**2 - 2)) - atanh(cot(x)/sqrt(-cot(x)**2 - 2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-csc(x)**2 - 1),
        variable=x,
        num_steps=6,
        integral=atan(cot(x)/sqrt(-cot(x)**2 - 2)) + atanh(cot(x)/sqrt(-cot(x)**2 - 2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(-csc(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=-atanh(cot(x)/sqrt(-cot(x)**2 - 2)),
    ),
]
