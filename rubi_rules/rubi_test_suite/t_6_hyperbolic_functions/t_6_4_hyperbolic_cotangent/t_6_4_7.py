# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.4 Hyperbolic cotangent/6.4.7 (d hyper)^m (a+b (c coth)^n)^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.4 Hyperbolic cotangent/6.4.7 (d hyper)^m (a+b (c coth)^n)^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d = symbols('a b c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**5,
        variable=x,
        num_steps=4,
        integral=-b**5*coth(c + d*x)**9/(9*d) - b**4*(5*a + b)*coth(c + d*x)**7/(7*d) - b**3*(10*a**2 + 5*a*b + b**2)*coth(c + d*x)**5/(5*d) - b**2*(10*a**3 + 10*a**2*b + 5*a*b**2 + b**3)*coth(c + d*x)**3/(3*d) - b*(5*a**4 + 10*a**3*b + 10*a**2*b**2 + 5*a*b**3 + b**4)*coth(c + d*x)/d + x*(a + b)**5,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**4,
        variable=x,
        num_steps=4,
        integral=-b**4*coth(c + d*x)**7/(7*d) - b**3*(4*a + b)*coth(c + d*x)**5/(5*d) - b**2*(6*a**2 + 4*a*b + b**2)*coth(c + d*x)**3/(3*d) - b*(2*a + b)*(2*a**2 + 2*a*b + b**2)*coth(c + d*x)/d + x*(a + b)**4,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**3,
        variable=x,
        num_steps=4,
        integral=-b**3*coth(c + d*x)**5/(5*d) - b**2*(3*a + b)*coth(c + d*x)**3/(3*d) - b*(3*a**2 + 3*a*b + b**2)*coth(c + d*x)/d + x*(a + b)**3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**2,
        variable=x,
        num_steps=4,
        integral=-b**2*coth(c + d*x)**3/(3*d) - b*(2*a + b)*coth(c + d*x)/d + x*(a + b)**2,
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*coth(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=x/(a + b) - sqrt(b)*atan(sqrt(a)*tanh(c + d*x)/sqrt(b))/(sqrt(a)*d*(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**(-2),
        variable=x,
        num_steps=5,
        integral=x/(a + b)**2 + b*coth(c + d*x)/(2*a*d*(a + b)*(a + b*coth(c + d*x)**2)) - sqrt(b)*(3*a + b)*atan(sqrt(a)*tanh(c + d*x)/sqrt(b))/(2*a**(sympy.S(3)/2)*d*(a + b)**2),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**(-3),
        variable=x,
        num_steps=6,
        integral=x/(a + b)**3 + b*coth(c + d*x)/(4*a*d*(a + b)*(a + b*coth(c + d*x)**2)**2) + b*(7*a + 3*b)*coth(c + d*x)/(8*a**2*d*(a + b)**2*(a + b*coth(c + d*x)**2)) - sqrt(b)*(15*a**2 + 10*a*b + 3*b**2)*atan(sqrt(a)*tanh(c + d*x)/sqrt(b))/(8*a**(sympy.S(5)/2)*d*(a + b)**3),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(c + d*x)**2)**(-4),
        variable=x,
        num_steps=7,
        integral=x/(a + b)**4 + b*coth(c + d*x)/(6*a*d*(a + b)*(a + b*coth(c + d*x)**2)**3) + b*(11*a + 5*b)*coth(c + d*x)/(24*a**2*d*(a + b)**2*(a + b*coth(c + d*x)**2)**2) + b*(19*a**2 + 16*a*b + 5*b**2)*coth(c + d*x)/(16*a**3*d*(a + b)**3*(a + b*coth(c + d*x)**2)) - sqrt(b)*(35*a**3 + 35*a**2*b + 21*a*b**2 + 5*b**3)*atan(sqrt(a)*tanh(c + d*x)/sqrt(b))/(16*a**(sympy.S(7)/2)*d*(a + b)**4),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - 2*coth(x)**2),
        variable=x,
        num_steps=3,
        integral=-x + sqrt(2)*atanh(sqrt(2)*tanh(x)/2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 - coth(x)**2),
        variable=x,
        num_steps=3,
        integral=asin(coth(x)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(coth(x)**2 - 1),
        variable=x,
        num_steps=4,
        integral=-atanh(coth(x)/sqrt(csch(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(1 - coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=sqrt(-csch(x)**2)*coth(x)/2 + asin(coth(x))/2,
    ),
    RubiTestSuiteCase(
        integrand=(coth(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=-sqrt(csch(x)**2)*coth(x)/2 + atanh(coth(x)/sqrt(csch(x)**2))/2,
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(1 - coth(x)**2),
        variable=x,
        num_steps=3,
        integral=coth(x)/sqrt(-csch(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(coth(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=coth(x)/sqrt(csch(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2)*coth(x)**3,
        variable=x,
        num_steps=6,
        integral=sqrt(a + b)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)) - sqrt(a + b*coth(x)**2) - (a + b*coth(x)**2)**(sympy.S(3)/2)/(3*b),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2)*coth(x)**2,
        variable=x,
        num_steps=7,
        integral=sqrt(a + b)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)) - sqrt(a + b*coth(x)**2)*coth(x)/2 - (a + 2*b)*atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2))/(2*sqrt(b)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2)*coth(x),
        variable=x,
        num_steps=5,
        integral=sqrt(a + b)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)) - sqrt(a + b*coth(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=6,
        integral=-sqrt(b)*atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2)) + sqrt(a + b)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2)*tanh(x),
        variable=x,
        num_steps=7,
        integral=-sqrt(a)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a)) + sqrt(a + b)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**2)*tanh(x)**2,
        variable=x,
        num_steps=5,
        integral=sqrt(a + b)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)) - sqrt(a + b*coth(x)**2)*tanh(x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2)*coth(x)**3,
        variable=x,
        num_steps=7,
        integral=(a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)) - (a + b)*sqrt(a + b*coth(x)**2) - (a + b*coth(x)**2)**(sympy.S(3)/2)/3 - (a + b*coth(x)**2)**(sympy.S(5)/2)/(5*b),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2)*coth(x)**2,
        variable=x,
        num_steps=8,
        integral=-b*sqrt(a + b*coth(x)**2)*coth(x)**3/4 - (5*a/8 + b/2)*sqrt(a + b*coth(x)**2)*coth(x) + (a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)) - (3*a**2 + 12*a*b + 8*b**2)*atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2))/(8*sqrt(b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2)*coth(x),
        variable=x,
        num_steps=6,
        integral=(a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)) - (a + b)*sqrt(a + b*coth(x)**2) - (a + b*coth(x)**2)**(sympy.S(3)/2)/3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-sqrt(b)*(3*a + 2*b)*atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2))/2 - b*sqrt(a + b*coth(x)**2)*coth(x)/2 + (a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2)*tanh(x),
        variable=x,
        num_steps=8,
        integral=-a**(sympy.S(3)/2)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a)) - b*sqrt(a + b*coth(x)**2) + (a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*coth(x)**2)**(sympy.S(3)/2)*tanh(x)**2,
        variable=x,
        num_steps=7,
        integral=-a*sqrt(a + b*coth(x)**2)*tanh(x) - b**(sympy.S(3)/2)*atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2)) + (a + b)**(sympy.S(3)/2)*atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(coth(x)**2 + 1),
        variable=x,
        num_steps=5,
        integral=-asinh(coth(x)) + sqrt(2)*atanh(sqrt(2)*coth(x)/sqrt(coth(x)**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-coth(x)**2 - 1),
        variable=x,
        num_steps=6,
        integral=atan(coth(x)/sqrt(-coth(x)**2 - 1)) - sqrt(2)*atan(sqrt(2)*coth(x)/sqrt(-coth(x)**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=(coth(x)**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=-sqrt(coth(x)**2 + 1)*coth(x)/2 - 5*asinh(coth(x))/2 + 2*sqrt(2)*atanh(sqrt(2)*coth(x)/sqrt(coth(x)**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(-coth(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=sqrt(-coth(x)**2 - 1)*coth(x)/2 - 5*atan(coth(x)/sqrt(-coth(x)**2 - 1))/2 + 2*sqrt(2)*atan(sqrt(2)*coth(x)/sqrt(-coth(x)**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**3/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=5,
        integral=atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/sqrt(a + b) - sqrt(a + b*coth(x)**2)/b,
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**2/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=6,
        integral=atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/sqrt(a + b) - atanh(sqrt(b)*coth(x)/sqrt(a + b*coth(x)**2))/sqrt(b),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=4,
        integral=atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/sqrt(a + b),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=3,
        integral=atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/sqrt(a + b),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=7,
        integral=atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/sqrt(a + b) - atanh(sqrt(a + b*coth(x)**2)/sqrt(a))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)**2/sqrt(a + b*coth(x)**2),
        variable=x,
        num_steps=5,
        integral=atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/sqrt(a + b) - sqrt(a + b*coth(x)**2)*tanh(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**3/(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=a/(b*(a + b)*sqrt(a + b*coth(x)**2)) + atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**2/(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-coth(x)/((a + b)*sqrt(a + b*coth(x)**2)) + atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/(a + b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)/(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=-1/((a + b)*sqrt(a + b*coth(x)**2)) + atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=8,
        integral=atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(3)/2) + b/(a*(a + b)*sqrt(a + b*coth(x)**2)) - atanh(sqrt(a + b*coth(x)**2)/sqrt(a))/a**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)**2/(a + b*coth(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/(a + b)**(sympy.S(3)/2) + b*tanh(x)/(a*(a + b)*sqrt(a + b*coth(x)**2)) - (a + 2*b)*sqrt(a + b*coth(x)**2)*tanh(x)/(a**2*(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**3/(a + b*coth(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=a/(3*b*(a + b)*(a + b*coth(x)**2)**(sympy.S(3)/2)) - 1/((a + b)**2*sqrt(a + b*coth(x)**2)) + atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)**2/(a + b*coth(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=-coth(x)/((a + b*coth(x)**2)**(sympy.S(3)/2)*(3*a + 3*b)) + atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/(a + b)**(sympy.S(5)/2) - (2*a - b)*coth(x)/(3*a*(a + b)**2*sqrt(a + b*coth(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)/(a + b*coth(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=-1/((a + b*coth(x)**2)**(sympy.S(3)/2)*(3*a + 3*b)) - 1/((a + b)**2*sqrt(a + b*coth(x)**2)) + atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/(a + b*coth(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=9,
        integral=atanh(sqrt(a + b*coth(x)**2)/sqrt(a + b))/(a + b)**(sympy.S(5)/2) + b/(3*a*(a + b)*(a + b*coth(x)**2)**(sympy.S(3)/2)) + b*(2*a + b)/(a**2*(a + b)**2*sqrt(a + b*coth(x)**2)) - atanh(sqrt(a + b*coth(x)**2)/sqrt(a))/a**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)**2/(a + b*coth(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=7,
        integral=atanh(sqrt(a + b)*coth(x)/sqrt(a + b*coth(x)**2))/(a + b)**(sympy.S(5)/2) + b*tanh(x)/(3*a*(a + b)*(a + b*coth(x)**2)**(sympy.S(3)/2)) + b*(7*a + 4*b)*tanh(x)/(3*a**2*(a + b)**2*sqrt(a + b*coth(x)**2)) - (a + 4*b)*sqrt(a + b*coth(x)**2)*(3*a + 2*b)*tanh(x)/(3*a**3*(a + b)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(coth(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*atanh(sqrt(2)*coth(x)/sqrt(coth(x)**2 + 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(-coth(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*atan(sqrt(2)*coth(x)/sqrt(-coth(x)**2 - 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=1/(coth(x)**3 + 1),
        variable=x,
        num_steps=6,
        integral=x/2 - 2*sqrt(3)*atan(sqrt(3)*(1 - 2*coth(x))/3)/9 - 1/(6*coth(x) + 6),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*coth(x)**4)*coth(x),
        variable=x,
        num_steps=8,
        integral=-sqrt(b)*atanh(sqrt(b)*coth(x)**2/sqrt(a + b*coth(x)**4))/2 + sqrt(a + b)*atanh((a + b*coth(x)**2)/(sqrt(a + b)*sqrt(a + b*coth(x)**4)))/2 - sqrt(a + b*coth(x)**4)/2,
    ),
    RubiTestSuiteCase(
        integrand=coth(x)/sqrt(a + b*coth(x)**4),
        variable=x,
        num_steps=4,
        integral=atanh((a + b*coth(x)**2)/(sqrt(a + b)*sqrt(a + b*coth(x)**4)))/(2*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=coth(x)/(a + b*coth(x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atanh((a + b*coth(x)**2)/(sqrt(a + b)*sqrt(a + b*coth(x)**4)))/(2*(a + b)**(sympy.S(3)/2)) - (a - b*coth(x)**2)/(2*a*(a + b)*sqrt(a + b*coth(x)**4)),
    ),
]
