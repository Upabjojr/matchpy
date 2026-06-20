# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.6 Hyperbolic cosecant/6.6.7 (d hyper)^m (a+b (c csch)^n)^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.6 Hyperbolic cosecant/6.6.7 (d hyper)^m (a+b (c csch)^n)^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d = symbols('a b c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**4,
        variable=x,
        num_steps=4,
        integral=a**4*x - b**4*coth(c + d*x)**7/(7*d) - b**3*(4*a - 3*b)*coth(c + d*x)**5/(5*d) - b**2*(6*a**2 - 8*a*b + 3*b**2)*coth(c + d*x)**3/(3*d) - b*(2*a - b)*(2*a**2 - 2*a*b + b**2)*coth(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**3,
        variable=x,
        num_steps=4,
        integral=a**3*x - b**3*coth(c + d*x)**5/(5*d) - b**2*(3*a - 2*b)*coth(c + d*x)**3/(3*d) - b*(3*a**2 - 3*a*b + b**2)*coth(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**2,
        variable=x,
        num_steps=4,
        integral=a**2*x - b**2*coth(c + d*x)**3/(3*d) - b*(2*a - b)*coth(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=a + b*csch(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=a*x - b*coth(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*csch(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=-sqrt(b)*atan(sqrt(a - b)*tanh(c + d*x)/sqrt(b))/(a*d*sqrt(a - b)) + x/a,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(-2),
        variable=x,
        num_steps=5,
        integral=b*coth(c + d*x)/(2*a*d*(a - b)*(a + b*coth(c + d*x)**2 - b)) - sqrt(b)*(3*a - 2*b)*atan(sqrt(a - b)*tanh(c + d*x)/sqrt(b))/(2*a**2*d*(a - b)**(sympy.S(3)/2)) + x/a**2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(-3),
        variable=x,
        num_steps=6,
        integral=b*coth(c + d*x)/(4*a*d*(a - b)*(a + b*coth(c + d*x)**2 - b)**2) + b*(7*a - 4*b)*coth(c + d*x)/(8*a**2*d*(a - b)**2*(a + b*coth(c + d*x)**2 - b)) - sqrt(b)*(15*a**2 - 20*a*b + 8*b**2)*atan(sqrt(a - b)*tanh(c + d*x)/sqrt(b))/(8*a**3*d*(a - b)**(sympy.S(5)/2)) + x/a**3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(-4),
        variable=x,
        num_steps=7,
        integral=b*coth(c + d*x)/(6*a*d*(a - b)*(a + b*coth(c + d*x)**2 - b)**3) + b*(11*a - 6*b)*coth(c + d*x)/(24*a**2*d*(a - b)**2*(a + b*coth(c + d*x)**2 - b)**2) + b*(19*a**2 - 22*a*b + 8*b**2)*coth(c + d*x)/(16*a**3*d*(a - b)**3*(a + b*coth(c + d*x)**2 - b)) - sqrt(b)*(35*a**3 - 70*a**2*b + 56*a*b**2 - 16*b**3)*atan(sqrt(a - b)*tanh(c + d*x)/sqrt(b))/(16*a**4*d*(a - b)**(sympy.S(7)/2)) + x/a**4,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=8,
        integral=a**(sympy.S(5)/2)*atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/d - sqrt(b)*(15*a**2 - 10*a*b + 3*b**2)*atanh(sqrt(b)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/(8*d) - b*(7*a - 3*b)*sqrt(a + b*coth(c + d*x)**2 - b)*coth(c + d*x)/(8*d) - b*(a + b*coth(c + d*x)**2 - b)**(sympy.S(3)/2)*coth(c + d*x)/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=a**(sympy.S(3)/2)*atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/d - sqrt(b)*(3*a - b)*atanh(sqrt(b)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/(2*d) - b*sqrt(a + b*coth(c + d*x)**2 - b)*coth(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*csch(c + d*x)**2),
        variable=x,
        num_steps=6,
        integral=sqrt(a)*atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/d - sqrt(b)*atanh(sqrt(b)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(sympy.S(-3)/2),
        variable=x,
        num_steps=4,
        integral=b*coth(c + d*x)/(a*d*(a - b)*sqrt(a + b*coth(c + d*x)**2 - b)) + atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/(a**(sympy.S(3)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(sympy.S(-5)/2),
        variable=x,
        num_steps=6,
        integral=b*coth(c + d*x)/(3*a*d*(a - b)*(a + b*coth(c + d*x)**2 - b)**(sympy.S(3)/2)) + b*(5*a - 3*b)*coth(c + d*x)/(3*a**2*d*(a - b)**2*sqrt(a + b*coth(c + d*x)**2 - b)) + atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/(a**(sympy.S(5)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*csch(c + d*x)**2)**(sympy.S(-7)/2),
        variable=x,
        num_steps=7,
        integral=b*coth(c + d*x)/(5*a*d*(a - b)*(a + b*coth(c + d*x)**2 - b)**(sympy.S(5)/2)) + b*(9*a - 5*b)*coth(c + d*x)/(15*a**2*d*(a - b)**2*(a + b*coth(c + d*x)**2 - b)**(sympy.S(3)/2)) + b*(33*a**2 - 40*a*b + 15*b**2)*coth(c + d*x)/(15*a**3*d*(a - b)**3*sqrt(a + b*coth(c + d*x)**2 - b)) + atanh(sqrt(a)*coth(c + d*x)/sqrt(a + b*coth(c + d*x)**2 - b))/(a**(sympy.S(7)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(csch(x)**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-(coth(x)**2)**(sympy.S(3)/2)*tanh(x)/2 + sqrt(coth(x)**2)*log(sinh(x))*tanh(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(csch(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=sqrt(coth(x)**2)*log(sinh(x))*tanh(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(csch(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=log(cosh(x))*coth(x)/sqrt(coth(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=(1 - csch(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=sqrt(2 - coth(x)**2)*coth(x)/2 + 2*asin(sqrt(2)*coth(x)/2) + atanh(coth(x)/sqrt(2 - coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 - csch(x)**2),
        variable=x,
        num_steps=5,
        integral=asin(sqrt(2)*coth(x)/2) + atanh(coth(x)/sqrt(2 - coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(1 - csch(x)**2),
        variable=x,
        num_steps=3,
        integral=atanh(coth(x)/sqrt(2 - coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(csch(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-sqrt(coth(x)**2 - 2)*coth(x)/2 + atan(coth(x)/sqrt(coth(x)**2 - 2)) + 2*atanh(coth(x)/sqrt(coth(x)**2 - 2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(csch(x)**2 - 1),
        variable=x,
        num_steps=6,
        integral=-atan(coth(x)/sqrt(coth(x)**2 - 2)) - atanh(coth(x)/sqrt(coth(x)**2 - 2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(csch(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=atan(coth(x)/sqrt(coth(x)**2 - 2)),
    ),
    RubiTestSuiteCase(
        integrand=(-csch(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-sqrt(-coth(x)**2)*log(sinh(x))*tanh(x) + sqrt(-coth(x)**2)*coth(x)/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-csch(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=sqrt(-coth(x)**2)*log(sinh(x))*tanh(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(-csch(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=log(cosh(x))*coth(x)/sqrt(-coth(x)**2),
    ),
]
