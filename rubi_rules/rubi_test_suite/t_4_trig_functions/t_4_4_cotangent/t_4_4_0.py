# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.4 Cotangent/4.4.0 (a trg)^m (b cot)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.4 Cotangent/4.4.0 (a trg)^m (b cot)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e, f, m, n, p = symbols('a b c d e f m n p')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=cot(a + b*x),
        variable=x,
        num_steps=1,
        integral=log(sin(a + b*x))/b,
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**2,
        variable=x,
        num_steps=2,
        integral=-x - cot(a + b*x)/b,
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**3,
        variable=x,
        num_steps=2,
        integral=-log(sin(a + b*x))/b - cot(a + b*x)**2/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**4,
        variable=x,
        num_steps=3,
        integral=x - cot(a + b*x)**3/(3*b) + cot(a + b*x)/b,
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**5,
        variable=x,
        num_steps=3,
        integral=log(sin(a + b*x))/b - cot(a + b*x)**4/(4*b) + cot(a + b*x)**2/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**6,
        variable=x,
        num_steps=4,
        integral=-x - cot(a + b*x)**5/(5*b) + cot(a + b*x)**3/(3*b) - cot(a + b*x)/b,
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**7,
        variable=x,
        num_steps=4,
        integral=-log(sin(a + b*x))/b - cot(a + b*x)**6/(6*b) + cot(a + b*x)**4/(4*b) - cot(a + b*x)**2/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**8,
        variable=x,
        num_steps=5,
        integral=x - cot(a + b*x)**7/(7*b) + cot(a + b*x)**5/(5*b) - cot(a + b*x)**3/(3*b) + cot(a + b*x)/b,
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(7)/2),
        variable=x,
        num_steps=13,
        integral=sqrt(2)*c**(sympy.S(7)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) - sqrt(2)*c**(sympy.S(7)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) + sqrt(2)*c**(sympy.S(7)/2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) - sqrt(2)*c**(sympy.S(7)/2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) + 2*c**3*sqrt(c*cot(a + b*x))/b - 2*c*(c*cot(a + b*x))**(sympy.S(5)/2)/(5*b),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=12,
        integral=sqrt(2)*c**(sympy.S(5)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) - sqrt(2)*c**(sympy.S(5)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) - sqrt(2)*c**(sympy.S(5)/2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) + sqrt(2)*c**(sympy.S(5)/2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) - 2*c*(c*cot(a + b*x))**(sympy.S(3)/2)/(3*b),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=12,
        integral=-sqrt(2)*c**(sympy.S(3)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) + sqrt(2)*c**(sympy.S(3)/2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) - sqrt(2)*c**(sympy.S(3)/2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) + sqrt(2)*c**(sympy.S(3)/2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) - 2*c*sqrt(c*cot(a + b*x))/b,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(c*cot(a + b*x)),
        variable=x,
        num_steps=11,
        integral=-sqrt(2)*sqrt(c)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) + sqrt(2)*sqrt(c)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b) + sqrt(2)*sqrt(c)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b) - sqrt(2)*sqrt(c)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(c*cot(a + b*x)),
        variable=x,
        num_steps=11,
        integral=sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*sqrt(c)) - sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*sqrt(c)) + sqrt(2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*sqrt(c)) - sqrt(2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*sqrt(c)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-3)/2),
        variable=x,
        num_steps=12,
        integral=2/(b*c*sqrt(c*cot(a + b*x))) + sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(3)/2)) - sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(3)/2)) - sqrt(2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(3)/2)) + sqrt(2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-5)/2),
        variable=x,
        num_steps=12,
        integral=2/(3*b*c*(c*cot(a + b*x))**(sympy.S(3)/2)) - sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(5)/2)) + sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(5)/2)) - sqrt(2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(5)/2)) + sqrt(2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-7)/2),
        variable=x,
        num_steps=13,
        integral=2/(5*b*c*(c*cot(a + b*x))**(sympy.S(5)/2)) - 2/(b*c**3*sqrt(c*cot(a + b*x))) - sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) - sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(7)/2)) + sqrt(2)*log(sqrt(c)*cot(a + b*x) + sqrt(c) + sqrt(2)*sqrt(c*cot(a + b*x)))/(4*b*c**(sympy.S(7)/2)) + sqrt(2)*atan(1 - sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(7)/2)) - sqrt(2)*atan(1 + sqrt(2)*sqrt(c*cot(a + b*x))/sqrt(c))/(2*b*c**(sympy.S(7)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(4)/3),
        variable=x,
        num_steps=13,
        integral=-sqrt(3)*c**(sympy.S(4)/3)*log(c**(sympy.S(2)/3) - sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b) + sqrt(3)*c**(sympy.S(4)/3)*log(c**(sympy.S(2)/3) + sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b) + c**(sympy.S(4)/3)*atan((c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/b - c**(sympy.S(4)/3)*atan(sqrt(3) - 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b) + c**(sympy.S(4)/3)*atan(sqrt(3) + 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b) - 3*c*(c*cot(a + b*x))**(sympy.S(1)/3)/b,
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(2)/3),
        variable=x,
        num_steps=12,
        integral=-sqrt(3)*c**(sympy.S(2)/3)*log(c**(sympy.S(2)/3) - sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b) + sqrt(3)*c**(sympy.S(2)/3)*log(c**(sympy.S(2)/3) + sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b) - c**(sympy.S(2)/3)*atan((c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/b + c**(sympy.S(2)/3)*atan(sqrt(3) - 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b) - c**(sympy.S(2)/3)*atan(sqrt(3) + 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(1)/3),
        variable=x,
        num_steps=9,
        integral=c**(sympy.S(1)/3)*log(c**(sympy.S(2)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(2*b) - c**(sympy.S(1)/3)*log(c**(sympy.S(4)/3) - c**(sympy.S(2)/3)*(c*cot(a + b*x))**(sympy.S(2)/3) + (c*cot(a + b*x))**(sympy.S(4)/3))/(4*b) + sqrt(3)*c**(sympy.S(1)/3)*atan(sqrt(3)*(c**(sympy.S(2)/3) - 2*(c*cot(a + b*x))**(sympy.S(2)/3))/(3*c**(sympy.S(2)/3)))/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-1)/3),
        variable=x,
        num_steps=9,
        integral=-log(c**(sympy.S(2)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(2*b*c**(sympy.S(1)/3)) + log(c**(sympy.S(4)/3) - c**(sympy.S(2)/3)*(c*cot(a + b*x))**(sympy.S(2)/3) + (c*cot(a + b*x))**(sympy.S(4)/3))/(4*b*c**(sympy.S(1)/3)) + sqrt(3)*atan(sqrt(3)*(c**(sympy.S(2)/3) - 2*(c*cot(a + b*x))**(sympy.S(2)/3))/(3*c**(sympy.S(2)/3)))/(2*b*c**(sympy.S(1)/3)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-2)/3),
        variable=x,
        num_steps=12,
        integral=sqrt(3)*log(c**(sympy.S(2)/3) - sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b*c**(sympy.S(2)/3)) - sqrt(3)*log(c**(sympy.S(2)/3) + sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b*c**(sympy.S(2)/3)) - atan((c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(b*c**(sympy.S(2)/3)) + atan(sqrt(3) - 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b*c**(sympy.S(2)/3)) - atan(sqrt(3) + 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b*c**(sympy.S(2)/3)),
    ),
    RubiTestSuiteCase(
        integrand=(c*cot(a + b*x))**(sympy.S(-4)/3),
        variable=x,
        num_steps=13,
        integral=3/(b*c*(c*cot(a + b*x))**(sympy.S(1)/3)) + sqrt(3)*log(c**(sympy.S(2)/3) - sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b*c**(sympy.S(4)/3)) - sqrt(3)*log(c**(sympy.S(2)/3) + sqrt(3)*c**(sympy.S(1)/3)*(c*cot(a + b*x))**(sympy.S(1)/3) + (c*cot(a + b*x))**(sympy.S(2)/3))/(4*b*c**(sympy.S(4)/3)) + atan((c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(b*c**(sympy.S(4)/3)) - atan(sqrt(3) - 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b*c**(sympy.S(4)/3)) + atan(sqrt(3) + 2*(c*cot(a + b*x))**(sympy.S(1)/3)/c**(sympy.S(1)/3))/(2*b*c**(sympy.S(4)/3)),
    ),
    RubiTestSuiteCase(
        integrand=cot(a + b*x)**n,
        variable=x,
        num_steps=2,
        integral=-cot(a + b*x)**(n + 1)*hyper((1, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), -cot(a + b*x)**2)/(b*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(b*cot(c + d*x))**n,
        variable=x,
        num_steps=2,
        integral=-(b*cot(c + d*x))**(n + 1)*hyper((1, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), -cot(c + d*x)**2)/(b*d*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=3,
        integral=-a*sqrt(a*cot(x)**2)*log(sin(x))*tan(x) - a*sqrt(a*cot(x)**2)*cot(x)/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*cot(x)**2),
        variable=x,
        num_steps=2,
        integral=sqrt(a*cot(x)**2)*log(sin(x))*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a*cot(x)**2),
        variable=x,
        num_steps=2,
        integral=-log(cos(x))*cot(x)/sqrt(a*cot(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**2)**(sympy.S(-3)/2),
        variable=x,
        num_steps=3,
        integral=log(cos(x))*cot(x)/(a*sqrt(a*cot(x)**2)) + tan(x)/(2*a*sqrt(a*cot(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**3)**(sympy.S(3)/2),
        variable=x,
        num_steps=14,
        integral=-sqrt(2)*a*sqrt(a*cot(x)**3)*log(-sqrt(2)*sqrt(cot(x)) + cot(x) + 1)/(4*cot(x)**(sympy.S(3)/2)) + sqrt(2)*a*sqrt(a*cot(x)**3)*log(sqrt(2)*sqrt(cot(x)) + cot(x) + 1)/(4*cot(x)**(sympy.S(3)/2)) - 2*a*sqrt(a*cot(x)**3)*cot(x)**2/7 + 2*a*sqrt(a*cot(x)**3)/3 - sqrt(2)*a*sqrt(a*cot(x)**3)*atan(sqrt(2)*sqrt(cot(x)) - 1)/(2*cot(x)**(sympy.S(3)/2)) - sqrt(2)*a*sqrt(a*cot(x)**3)*atan(sqrt(2)*sqrt(cot(x)) + 1)/(2*cot(x)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*cot(x)**3),
        variable=x,
        num_steps=13,
        integral=-sqrt(2)*sqrt(a*cot(x)**3)*log(-sqrt(2)*sqrt(cot(x)) + cot(x) + 1)/(4*cot(x)**(sympy.S(3)/2)) + sqrt(2)*sqrt(a*cot(x)**3)*log(sqrt(2)*sqrt(cot(x)) + cot(x) + 1)/(4*cot(x)**(sympy.S(3)/2)) - 2*sqrt(a*cot(x)**3)*tan(x) + sqrt(2)*sqrt(a*cot(x)**3)*atan(sqrt(2)*sqrt(cot(x)) - 1)/(2*cot(x)**(sympy.S(3)/2)) + sqrt(2)*sqrt(a*cot(x)**3)*atan(sqrt(2)*sqrt(cot(x)) + 1)/(2*cot(x)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a*cot(x)**3),
        variable=x,
        num_steps=13,
        integral=sqrt(2)*log(-sqrt(2)*sqrt(cot(x)) + cot(x) + 1)*cot(x)**(sympy.S(3)/2)/(4*sqrt(a*cot(x)**3)) - sqrt(2)*log(sqrt(2)*sqrt(cot(x)) + cot(x) + 1)*cot(x)**(sympy.S(3)/2)/(4*sqrt(a*cot(x)**3)) + sqrt(2)*cot(x)**(sympy.S(3)/2)*atan(sqrt(2)*sqrt(cot(x)) - 1)/(2*sqrt(a*cot(x)**3)) + sqrt(2)*cot(x)**(sympy.S(3)/2)*atan(sqrt(2)*sqrt(cot(x)) + 1)/(2*sqrt(a*cot(x)**3)) + 2*cot(x)/sqrt(a*cot(x)**3),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**3)**(sympy.S(-3)/2),
        variable=x,
        num_steps=14,
        integral=sqrt(2)*log(-sqrt(2)*sqrt(cot(x)) + cot(x) + 1)*cot(x)**(sympy.S(3)/2)/(4*a*sqrt(a*cot(x)**3)) - sqrt(2)*log(sqrt(2)*sqrt(cot(x)) + cot(x) + 1)*cot(x)**(sympy.S(3)/2)/(4*a*sqrt(a*cot(x)**3)) + 2*tan(x)**2/(7*a*sqrt(a*cot(x)**3)) - sqrt(2)*cot(x)**(sympy.S(3)/2)*atan(sqrt(2)*sqrt(cot(x)) - 1)/(2*a*sqrt(a*cot(x)**3)) - sqrt(2)*cot(x)**(sympy.S(3)/2)*atan(sqrt(2)*sqrt(cot(x)) + 1)/(2*a*sqrt(a*cot(x)**3)) - 2/(3*a*sqrt(a*cot(x)**3)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**4)**(sympy.S(3)/2),
        variable=x,
        num_steps=5,
        integral=-a*x*sqrt(a*cot(x)**4)*tan(x)**2 - a*sqrt(a*cot(x)**4)*tan(x) - a*sqrt(a*cot(x)**4)*cot(x)**3/5 + a*sqrt(a*cot(x)**4)*cot(x)/3,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*cot(x)**4),
        variable=x,
        num_steps=3,
        integral=-x*sqrt(a*cot(x)**4)*tan(x)**2 - sqrt(a*cot(x)**4)*tan(x),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a*cot(x)**4),
        variable=x,
        num_steps=3,
        integral=-x*cot(x)**2/sqrt(a*cot(x)**4) + cot(x)/sqrt(a*cot(x)**4),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(x)**4)**(sympy.S(-3)/2),
        variable=x,
        num_steps=5,
        integral=-x*cot(x)**2/(a*sqrt(a*cot(x)**4)) + tan(x)**3/(5*a*sqrt(a*cot(x)**4)) - tan(x)/(3*a*sqrt(a*cot(x)**4)) + cot(x)/(a*sqrt(a*cot(x)**4)),
    ),
    RubiTestSuiteCase(
        integrand=(b*cot(c + d*x)**p)**n,
        variable=x,
        num_steps=3,
        integral=-(b*cot(c + d*x)**p)**n*cot(c + d*x)*hyper((1, n*p/2 + sympy.S.Half), (n*p/2 + sympy.S(3)/2,), -cot(c + d*x)**2)/(d*(n*p + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*(b*cot(c + d*x))**p)**n,
        variable=x,
        num_steps=3,
        integral=-(a*(b*cot(c + d*x))**p)**n*cot(c + d*x)*hyper((1, n*p/2 + sympy.S.Half), (n*p/2 + sympy.S(3)/2,), -cot(c + d*x)**2)/(d*(n*p + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sin(e + f*x))**m*(b*cot(e + f*x))**n,
        variable=x,
        num_steps=2,
        integral=-(a*sin(e + f*x))**m*(b*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(-m/2 + n/2 + sympy.S.Half)*hyper((n/2 + sympy.S.Half, -m/2 + n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(b*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(e + f*x))**m*(b*cot(e + f*x))**n,
        variable=x,
        num_steps=2,
        integral=-(a*cos(e + f*x))**m*(b*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2 + sympy.S.Half)*hyper((n/2 + sympy.S.Half, m/2 + n/2 + sympy.S.Half), (m/2 + n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(b*f*(m + n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cot(e + f*x))**m*(b*cot(e + f*x))**n,
        variable=x,
        num_steps=3,
        integral=-(a*cot(e + f*x))**(m + 1)*(b*cot(e + f*x))**n*hyper((1, m/2 + n/2 + sympy.S.Half), (m/2 + n/2 + sympy.S(3)/2,), -cot(e + f*x)**2)/(a*f*(m + n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*sec(e + f*x))**m*(b*cot(e + f*x))**n,
        variable=x,
        num_steps=3,
        integral=-(a*sec(e + f*x))**m*(b*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2 + sympy.S.Half)*hyper((n/2 + sympy.S.Half, -m/2 + n/2 + sympy.S.Half), (-m/2 + n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(b*f*(-m + n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*csc(e + f*x)**6,
        variable=x,
        num_steps=3,
        integral=-(d*cot(e + f*x))**(n + 1)/(d*f*(n + 1)) - 2*(d*cot(e + f*x))**(n + 3)/(d**3*f*(n + 3)) - (d*cot(e + f*x))**(n + 5)/(d**5*f*(n + 5)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*csc(e + f*x)**4,
        variable=x,
        num_steps=3,
        integral=-(d*cot(e + f*x))**(n + 1)/(d*f*(n + 1)) - (d*cot(e + f*x))**(n + 3)/(d**3*f*(n + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*csc(e + f*x)**2,
        variable=x,
        num_steps=2,
        integral=-(d*cot(e + f*x))**(n + 1)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*sin(e + f*x)**2,
        variable=x,
        num_steps=2,
        integral=-(d*cot(e + f*x))**(n + 1)*hyper((2, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), -cot(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*sin(e + f*x)**4,
        variable=x,
        num_steps=2,
        integral=-(d*cot(e + f*x))**(n + 1)*hyper((3, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), -cot(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*csc(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=-(d*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2 + 2)*csc(e + f*x)**3*hyper((n/2 + sympy.S.Half, n/2 + 2), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*csc(e + f*x),
        variable=x,
        num_steps=1,
        integral=-(d*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2 + 1)*csc(e + f*x)*hyper((n/2 + sympy.S.Half, n/2 + 1), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*sin(e + f*x),
        variable=x,
        num_steps=1,
        integral=-(d*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2)*sin(e + f*x)*hyper((n/2, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(d*cot(e + f*x))**n*sin(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=-(d*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(n/2 - 1)*sin(e + f*x)**3*hyper((n/2 - 1, n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(d*f*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a*csc(e + f*x))**m*(b*cot(e + f*x))**n,
        variable=x,
        num_steps=1,
        integral=-(a*csc(e + f*x))**m*(b*cot(e + f*x))**(n + 1)*(sin(e + f*x)**2)**(m/2 + n/2 + sympy.S.Half)*hyper((n/2 + sympy.S.Half, m/2 + n/2 + sympy.S.Half), (n/2 + sympy.S(3)/2,), cos(e + f*x)**2)/(b*f*(n + 1)),
    ),
]
