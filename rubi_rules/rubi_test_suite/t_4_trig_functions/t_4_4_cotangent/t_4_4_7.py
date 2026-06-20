# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.4 Cotangent/4.4.7 (d trig)^m (a+b (c cot)^n)^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.4 Cotangent/4.4.7 (d trig)^m (a+b (c cot)^n)^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, C, a, b, c, d = symbols('A C a b c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A + C*cot(c + d*x)**2)/sqrt(b*tan(c + d*x)),
        variable=x,
        num_steps=15,
        integral=-2*C*b/(3*d*(b*tan(c + d*x))**(sympy.S(3)/2)) - sqrt(2)*(A - C)*log(sqrt(b)*tan(c + d*x) + sqrt(b) - sqrt(2)*sqrt(b*tan(c + d*x)))/(4*sqrt(b)*d) + sqrt(2)*(A - C)*log(sqrt(b)*tan(c + d*x) + sqrt(b) + sqrt(2)*sqrt(b*tan(c + d*x)))/(4*sqrt(b)*d) - sqrt(2)*(A - C)*atan(1 - sqrt(2)*sqrt(b*tan(c + d*x))/sqrt(b))/(2*sqrt(b)*d) + sqrt(2)*(A - C)*atan(1 + sqrt(2)*sqrt(b*tan(c + d*x))/sqrt(b))/(2*sqrt(b)*d),
    ),
    RubiTestSuiteCase(
        integrand=a + b*cot(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=a*x - b*x - b*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**2,
        variable=x,
        num_steps=4,
        integral=-b**2*cot(c + d*x)**3/(3*d) - b*(2*a - b)*cot(c + d*x)/d + x*(a - b)**2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**3,
        variable=x,
        num_steps=4,
        integral=-b**3*cot(c + d*x)**5/(5*d) - b**2*(3*a - b)*cot(c + d*x)**3/(3*d) - b*(3*a**2 - 3*a*b + b**2)*cot(c + d*x)/d + x*(a - b)**3,
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cot(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=x/(a - b) + sqrt(b)*atan(sqrt(b)*cot(c + d*x)/sqrt(a))/(sqrt(a)*d*(a - b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(-2),
        variable=x,
        num_steps=5,
        integral=x/(a - b)**2 + b*cot(c + d*x)/(2*a*d*(a - b)*(a + b*cot(c + d*x)**2)) + sqrt(b)*(3*a - b)*atan(sqrt(b)*cot(c + d*x)/sqrt(a))/(2*a**(sympy.S(3)/2)*d*(a - b)**2),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(-3),
        variable=x,
        num_steps=6,
        integral=x/(a - b)**3 + b*cot(c + d*x)/(4*a*d*(a - b)*(a + b*cot(c + d*x)**2)**2) + b*(7*a - 3*b)*cot(c + d*x)/(8*a**2*d*(a - b)**2*(a + b*cot(c + d*x)**2)) + sqrt(b)*(15*a**2 - 10*a*b + 3*b**2)*atan(sqrt(b)*cot(c + d*x)/sqrt(a))/(8*a**(sympy.S(5)/2)*d*(a - b)**3),
    ),
    RubiTestSuiteCase(
        integrand=(cot(x)**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-sqrt(csc(x)**2)*cot(x)/2 - asinh(cot(x))/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(cot(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=-asinh(cot(x)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(cot(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=-cot(x)/sqrt(csc(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=(-cot(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=sqrt(-csc(x)**2)*cot(x)/2 - atan(cot(x)/sqrt(-csc(x)**2))/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-cot(x)**2 - 1),
        variable=x,
        num_steps=4,
        integral=atan(cot(x)/sqrt(-csc(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(-cot(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=-cot(x)/sqrt(-csc(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/sqrt(a*cot(x)**2 + a),
        variable=x,
        num_steps=4,
        integral=-1/sqrt(a*csc(x)**2) - sqrt(a*csc(x)**2)/a,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/sqrt(a*cot(x)**2 + a),
        variable=x,
        num_steps=5,
        integral=cot(x)/sqrt(a*csc(x)**2) - atanh(cos(x))*csc(x)/sqrt(a*csc(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/sqrt(a*cot(x)**2 + a),
        variable=x,
        num_steps=3,
        integral=1/sqrt(a*csc(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/sqrt(a*cot(x)**2 + a),
        variable=x,
        num_steps=5,
        integral=-1/sqrt(a*csc(x)**2) + atanh(sqrt(a*csc(x)**2)/sqrt(a))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/sqrt(a*cot(x)**2 + a),
        variable=x,
        num_steps=5,
        integral=cot(x)/sqrt(a*csc(x)**2) + csc(x)*sec(x)/sqrt(a*csc(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*cot(x)**3,
        variable=x,
        num_steps=6,
        integral=-sqrt(a - b)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)) + sqrt(a + b*cot(x)**2) - (a + b*cot(x)**2)**(sympy.S(3)/2)/(3*b),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*cot(x),
        variable=x,
        num_steps=5,
        integral=sqrt(a - b)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)) - sqrt(a + b*cot(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*tan(x),
        variable=x,
        num_steps=7,
        integral=sqrt(a)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a)) - sqrt(a - b)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*cot(x)**2,
        variable=x,
        num_steps=7,
        integral=sqrt(a - b)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)) - sqrt(a + b*cot(x)**2)*cot(x)/2 - (a - 2*b)*atanh(sqrt(b)*cot(x)/sqrt(a + b*cot(x)**2))/(2*sqrt(b)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=6,
        integral=-sqrt(b)*atanh(sqrt(b)*cot(x)/sqrt(a + b*cot(x)**2)) - sqrt(a - b)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*tan(x)**2,
        variable=x,
        num_steps=5,
        integral=sqrt(a - b)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)) + sqrt(a + b*cot(x)**2)*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**2)*tan(x)**4,
        variable=x,
        num_steps=6,
        integral=-sqrt(a - b)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)) + sqrt(a + b*cot(x)**2)*tan(x)**3/3 - sqrt(a + b*cot(x)**2)*(3*a - b)*tan(x)/(3*a),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**2)**(sympy.S(3)/2)*cot(x)**3,
        variable=x,
        num_steps=7,
        integral=-(a - b)**(sympy.S(3)/2)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)) + (a - b)*sqrt(a + b*cot(x)**2) + (a + b*cot(x)**2)**(sympy.S(3)/2)/3 - (a + b*cot(x)**2)**(sympy.S(5)/2)/(5*b),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**2)**(sympy.S(3)/2)*cot(x)**2,
        variable=x,
        num_steps=8,
        integral=-b*sqrt(a + b*cot(x)**2)*cot(x)**3/4 - (5*a/8 - b/2)*sqrt(a + b*cot(x)**2)*cot(x) + (a - b)**(sympy.S(3)/2)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)) - (3*a**2 - 12*a*b + 8*b**2)*atanh(sqrt(b)*cot(x)/sqrt(a + b*cot(x)**2))/(8*sqrt(b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**2)**(sympy.S(3)/2)*cot(x),
        variable=x,
        num_steps=6,
        integral=(a - b)**(sympy.S(3)/2)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)) - (a - b)*sqrt(a + b*cot(x)**2) - (a + b*cot(x)**2)**(sympy.S(3)/2)/3,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**2)**(sympy.S(3)/2)*tan(x),
        variable=x,
        num_steps=8,
        integral=a**(sympy.S(3)/2)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a)) - b*sqrt(a + b*cot(x)**2) - (a - b)**(sympy.S(3)/2)*atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**2)**(sympy.S(3)/2)*tan(x)**2,
        variable=x,
        num_steps=7,
        integral=a*sqrt(a + b*cot(x)**2)*tan(x) - b**(sympy.S(3)/2)*atanh(sqrt(b)*cot(x)/sqrt(a + b*cot(x)**2)) + (a - b)**(sympy.S(3)/2)*atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=8,
        integral=-sqrt(b)*(15*a**2 - 20*a*b + 8*b**2)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(8*d) - b*(a + b*cot(c + d*x)**2)**(sympy.S(3)/2)*cot(c + d*x)/(4*d) - b*sqrt(a + b*cot(c + d*x)**2)*(7*a - 4*b)*cot(c + d*x)/(8*d) - (a - b)**(sympy.S(5)/2)*atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-sqrt(b)*(3*a - 2*b)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(2*d) - b*sqrt(a + b*cot(c + d*x)**2)*cot(c + d*x)/(2*d) - (a - b)**(sympy.S(3)/2)*atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/d,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(c + d*x)**2),
        variable=x,
        num_steps=6,
        integral=-sqrt(b)*atanh(sqrt(b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/d - sqrt(a - b)*atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/d,
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a + b*cot(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=-atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(d*sqrt(a - b)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(sympy.S(-3)/2),
        variable=x,
        num_steps=4,
        integral=-atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(d*(a - b)**(sympy.S(3)/2)) + b*cot(c + d*x)/(a*d*(a - b)*sqrt(a + b*cot(c + d*x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(sympy.S(-5)/2),
        variable=x,
        num_steps=6,
        integral=-atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(d*(a - b)**(sympy.S(5)/2)) + b*cot(c + d*x)/(3*a*d*(a - b)*(a + b*cot(c + d*x)**2)**(sympy.S(3)/2)) + b*(5*a - 2*b)*cot(c + d*x)/(3*a**2*d*(a - b)**2*sqrt(a + b*cot(c + d*x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(c + d*x)**2)**(sympy.S(-7)/2),
        variable=x,
        num_steps=7,
        integral=-atan(sqrt(a - b)*cot(c + d*x)/sqrt(a + b*cot(c + d*x)**2))/(d*(a - b)**(sympy.S(7)/2)) + b*cot(c + d*x)/(5*a*d*(a - b)*(a + b*cot(c + d*x)**2)**(sympy.S(5)/2)) + b*(9*a - 4*b)*cot(c + d*x)/(15*a**2*d*(a - b)**2*(a + b*cot(c + d*x)**2)**(sympy.S(3)/2)) + b*(33*a**2 - 26*a*b + 8*b**2)*cot(c + d*x)/(15*a**3*d*(a - b)**3*sqrt(a + b*cot(c + d*x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(1 - cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=sqrt(1 - cot(x)**2)*cot(x)/2 + 5*asin(cot(x))/2 - 2*sqrt(2)*atan(sqrt(2)*cot(x)/sqrt(1 - cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 - cot(x)**2),
        variable=x,
        num_steps=5,
        integral=asin(cot(x)) - sqrt(2)*atan(sqrt(2)*cot(x)/sqrt(1 - cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(1 - cot(x)**2),
        variable=x,
        num_steps=3,
        integral=-sqrt(2)*atan(sqrt(2)*cot(x)/sqrt(1 - cot(x)**2))/2,
    ),
    RubiTestSuiteCase(
        integrand=(cot(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=-sqrt(cot(x)**2 - 1)*cot(x)/2 + 5*atanh(cot(x)/sqrt(cot(x)**2 - 1))/2 - 2*sqrt(2)*atanh(sqrt(2)*cot(x)/sqrt(cot(x)**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(cot(x)**2 - 1),
        variable=x,
        num_steps=6,
        integral=-atanh(cot(x)/sqrt(cot(x)**2 - 1)) + sqrt(2)*atanh(sqrt(2)*cot(x)/sqrt(cot(x)**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(cot(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=-sqrt(2)*atanh(sqrt(2)*cot(x)/sqrt(cot(x)**2 - 1))/2,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=5,
        integral=-atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/sqrt(a - b) - sqrt(a + b*cot(x)**2)/b,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=6,
        integral=atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/sqrt(a - b) - atanh(sqrt(b)*cot(x)/sqrt(a + b*cot(x)**2))/sqrt(b),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=4,
        integral=atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/sqrt(a - b),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=7,
        integral=-atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/sqrt(a - b) + atanh(sqrt(a + b*cot(x)**2)/sqrt(a))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/sqrt(a + b*cot(x)**2),
        variable=x,
        num_steps=5,
        integral=atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/sqrt(a - b) + sqrt(a + b*cot(x)**2)*tan(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/(a + b*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=a/(b*(a - b)*sqrt(a + b*cot(x)**2)) - atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/(a + b*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=-cot(x)/((a - b)*sqrt(a + b*cot(x)**2)) + atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/(a - b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a + b*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=-1/((a - b)*sqrt(a + b*cot(x)**2)) + atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/(a + b*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=8,
        integral=-atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(3)/2) + b/(a*(a - b)*sqrt(a + b*cot(x)**2)) + atanh(sqrt(a + b*cot(x)**2)/sqrt(a))/a**(sympy.S(3)/2),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/(a + b*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/(a - b)**(sympy.S(3)/2) + b*tan(x)/(a*(a - b)*sqrt(a + b*cot(x)**2)) + (a - 2*b)*sqrt(a + b*cot(x)**2)*tan(x)/(a**2*(a - b)),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**3/(a + b*cot(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=a/(b*(a + b*cot(x)**2)**(sympy.S(3)/2)*(3*a - 3*b)) + 1/((a - b)**2*sqrt(a + b*cot(x)**2)) - atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)**2/(a + b*cot(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=-cot(x)/((a + b*cot(x)**2)**(sympy.S(3)/2)*(3*a - 3*b)) + atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/(a - b)**(sympy.S(5)/2) - (2*a + b)*cot(x)/(3*a*(a - b)**2*sqrt(a + b*cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a + b*cot(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=6,
        integral=-1/((a + b*cot(x)**2)**(sympy.S(3)/2)*(3*a - 3*b)) - 1/((a - b)**2*sqrt(a + b*cot(x)**2)) + atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)/(a + b*cot(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=9,
        integral=-atanh(sqrt(a + b*cot(x)**2)/sqrt(a - b))/(a - b)**(sympy.S(5)/2) + b/(3*a*(a - b)*(a + b*cot(x)**2)**(sympy.S(3)/2)) + b*(2*a - b)/(a**2*(a - b)**2*sqrt(a + b*cot(x)**2)) + atanh(sqrt(a + b*cot(x)**2)/sqrt(a))/a**(sympy.S(5)/2),
    ),
    RubiTestSuiteCase(
        integrand=tan(x)**2/(a + b*cot(x)**2)**(sympy.S(5)/2),
        variable=x,
        num_steps=7,
        integral=atan(sqrt(a - b)*cot(x)/sqrt(a + b*cot(x)**2))/(a - b)**(sympy.S(5)/2) + b*tan(x)/(3*a*(a - b)*(a + b*cot(x)**2)**(sympy.S(3)/2)) + b*(7*a - 4*b)*tan(x)/(3*a**2*(a - b)**2*sqrt(a + b*cot(x)**2)) + (a - 4*b)*sqrt(a + b*cot(x)**2)*(3*a - 2*b)*tan(x)/(3*a**3*(a - b)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/(cot(x)**3 + 1),
        variable=x,
        num_steps=7,
        integral=x/2 - log(cot(x) + 1)/6 + log(cot(x)**2 - cot(x) + 1)/3 + log(sin(x))/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cot(x)**4)*cot(x),
        variable=x,
        num_steps=8,
        integral=sqrt(b)*atanh(sqrt(b)*cot(x)**2/sqrt(a + b*cot(x)**4))/2 + sqrt(a + b)*atanh((a - b*cot(x)**2)/(sqrt(a + b)*sqrt(a + b*cot(x)**4)))/2 - sqrt(a + b*cot(x)**4)/2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cot(x)**4)**(sympy.S(3)/2)*cot(x),
        variable=x,
        num_steps=9,
        integral=sqrt(b)*(3*a + 2*b)*atanh(sqrt(b)*cot(x)**2/sqrt(a + b*cot(x)**4))/4 + (a + b)**(sympy.S(3)/2)*atanh((a - b*cot(x)**2)/(sqrt(a + b)*sqrt(a + b*cot(x)**4)))/2 - (a + b*cot(x)**4)**(sympy.S(3)/2)/6 - sqrt(a + b*cot(x)**4)*(a/2 - b*cot(x)**2/4 + b/2),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/sqrt(a + b*cot(x)**4),
        variable=x,
        num_steps=4,
        integral=atanh((a - b*cot(x)**2)/(sqrt(a + b)*sqrt(a + b*cot(x)**4)))/(2*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a + b*cot(x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=atanh((a - b*cot(x)**2)/(sqrt(a + b)*sqrt(a + b*cot(x)**4)))/(2*(a + b)**(sympy.S(3)/2)) - (a + b*cot(x)**2)/(2*a*(a + b)*sqrt(a + b*cot(x)**4)),
    ),
    RubiTestSuiteCase(
        integrand=cot(x)/(a + b*cot(x)**4)**(sympy.S(5)/2),
        variable=x,
        num_steps=7,
        integral=atanh((a - b*cot(x)**2)/(sqrt(a + b)*sqrt(a + b*cot(x)**4)))/(2*(a + b)**(sympy.S(5)/2)) - (a + b*cot(x)**2)/(6*a*(a + b)*(a + b*cot(x)**4)**(sympy.S(3)/2)) - (3*a**2 + b*(5*a + 2*b)*cot(x)**2)/(6*a**2*(a + b)**2*sqrt(a + b*cot(x)**4)),
    ),
]
