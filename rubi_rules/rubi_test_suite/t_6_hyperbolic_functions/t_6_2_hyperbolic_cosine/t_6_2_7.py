# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.7 hyper^m (a+b cosh^n)^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.7 hyper^m (a+b cosh^n)^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, n = symbols('a b n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sinh(x)**4/(-a*cosh(x)**2 + a),
        variable=x,
        num_steps=3,
        integral=x/(2*a) - sinh(x)*cosh(x)/(2*a),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**3/(-a*cosh(x)**2 + a),
        variable=x,
        num_steps=2,
        integral=-cosh(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**2/(-a*cosh(x)**2 + a),
        variable=x,
        num_steps=2,
        integral=-x/a,
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**2/(-a*cosh(x)**2 + a),
        variable=x,
        num_steps=3,
        integral=coth(x)**3/(3*a) - coth(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**4/(-a*cosh(x)**2 + a),
        variable=x,
        num_steps=3,
        integral=coth(x)**5/(5*a) - 2*coth(x)**3/(3*a) + coth(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**7/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=cosh(x)**5/(5*b) - (a + 3*b)*cosh(x)**3/(3*b**2) + (a**2 + 3*a*b + 3*b**2)*cosh(x)/b**3 - (a + b)**3*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*b**(sympy.S(7)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**5/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=cosh(x)**3/(3*b) - (a + 2*b)*cosh(x)/b**2 + (a + b)**2*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*b**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**3/(a + b*cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=cosh(x)/b - (a + b)*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*b**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)/(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*sqrt(b)),
    ),
    RubiTestSuiteCase(
        integrand=csch(x)/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-atanh(cosh(x))/(a + b) - sqrt(b)*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**3/(a + b*cosh(x)**2),
        variable=x,
        num_steps=5,
        integral=-coth(x)*csch(x)/(2*a + 2*b) + (a + 3*b)*atanh(cosh(x))/(2*(a + b)**2) + b**(sympy.S(3)/2)*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*(a + b)**2),
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**5/(a + b*cosh(x)**2),
        variable=x,
        num_steps=6,
        integral=-coth(x)*csch(x)**3/(4*a + 4*b) + (3*a + 7*b)*coth(x)*csch(x)/(8*(a + b)**2) - (3*a**2 + 10*a*b + 15*b**2)*atanh(cosh(x))/(8*(a + b)**3) - b**(sympy.S(5)/2)*atan(sqrt(b)*cosh(x)/sqrt(a))/(sqrt(a)*(a + b)**3),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**6/(a + b*cosh(x)**2),
        variable=x,
        num_steps=6,
        integral=sinh(x)**3*cosh(x)/(4*b) - (4*a + 7*b)*sinh(x)*cosh(x)/(8*b**2) + x*(8*a**2 + 20*a*b + 15*b**2)/(8*b**3) - (a + b)**(sympy.S(5)/2)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*b**3),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**4/(a + b*cosh(x)**2),
        variable=x,
        num_steps=5,
        integral=sinh(x)*cosh(x)/(2*b) - x*(2*a + 3*b)/(2*b**2) + (a + b)**(sympy.S(3)/2)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*b**2),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)**2/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=x/b - sqrt(a + b)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*b),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**4/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-coth(x)**3/(3*a + 3*b) + (a + 2*b)*coth(x)/(a + b)**2 + b**2*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*(a + b)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=csch(x)**6/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-coth(x)**5/(5*a + 5*b) + (2*a + 3*b)*coth(x)**3/(3*(a + b)**2) - (a**2 + 3*a*b + 3*b**2)*coth(x)/(a + b)**3 - b**3*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*(a + b)**(sympy.S(7)/2)),
    ),
    RubiTestSuiteCase(
        integrand=sinh(x)/(4 - 3*cosh(x)**3),
        variable=x,
        num_steps=7,
        integral=-6**(sympy.S(2)/3)*log(-3**(sympy.S(1)/3)*cosh(x) + 2**(sympy.S(2)/3))/36 + 6**(sympy.S(2)/3)*log(3**(sympy.S(2)/3)*cosh(x)**2 + 2**(sympy.S(2)/3)*3**(sympy.S(1)/3)*cosh(x) + 2*2**(sympy.S(1)/3))/72 + 2**(sympy.S(2)/3)*3**(sympy.S(1)/6)*atan(sqrt(3)*(6**(sympy.S(1)/3)*cosh(x) + 1)/3)/12,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**7/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-a**3*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(b**(sympy.S(7)/2)*sqrt(a + b)) + sinh(x)**5/(5*b) - (a - 2*b)*sinh(x)**3/(3*b**2) + (a**2 - a*b + b**2)*sinh(x)/b**3,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**6/(a + b*cosh(x)**2),
        variable=x,
        num_steps=6,
        integral=-a**(sympy.S(5)/2)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(b**3*sqrt(a + b)) + sinh(x)*cosh(x)**3/(4*b) - (4*a - 3*b)*sinh(x)*cosh(x)/(8*b**2) + x*(8*a**2 - 4*a*b + 3*b**2)/(8*b**3),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**5/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=a**2*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(b**(sympy.S(5)/2)*sqrt(a + b)) + sinh(x)**3/(3*b) - (a - b)*sinh(x)/b**2,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**4/(a + b*cosh(x)**2),
        variable=x,
        num_steps=5,
        integral=a**(sympy.S(3)/2)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(b**2*sqrt(a + b)) + sinh(x)*cosh(x)/(2*b) - x*(2*a - b)/(2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**3/(a + b*cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=-a*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(b**(sympy.S(3)/2)*sqrt(a + b)) + sinh(x)/b,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)**2/(a + b*cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=-sqrt(a)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(b*sqrt(a + b)) + x/b,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x)/(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=atan(sqrt(b)*sinh(x)/sqrt(a + b))/(sqrt(b)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(sqrt(a)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=sech(x)/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-sqrt(b)*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(a*sqrt(a + b)) + atan(sinh(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=sech(x)**2/(a + b*cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=tanh(x)/a - b*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(a**(sympy.S(3)/2)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=sech(x)**3/(a + b*cosh(x)**2),
        variable=x,
        num_steps=5,
        integral=tanh(x)*sech(x)/(2*a) + b**(sympy.S(3)/2)*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(a**2*sqrt(a + b)) + (a - 2*b)*atan(sinh(x))/(2*a**2),
    ),
    RubiTestSuiteCase(
        integrand=sech(x)**4/(a + b*cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-tanh(x)**3/(3*a) + (a - b)*tanh(x)/a**2 + b**2*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(a**(sympy.S(5)/2)*sqrt(a + b)),
    ),
    RubiTestSuiteCase(
        integrand=sech(x)**5/(a + b*cosh(x)**2),
        variable=x,
        num_steps=6,
        integral=tanh(x)*sech(x)**3/(4*a) + (3*a - 4*b)*tanh(x)*sech(x)/(8*a**2) - b**(sympy.S(5)/2)*atan(sqrt(b)*sinh(x)/sqrt(a + b))/(a**3*sqrt(a + b)) + (3*a**2 - 4*a*b + 8*b**2)*atan(sinh(x))/(8*a**3),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cosh(x)**2)**(-2),
        variable=x,
        num_steps=4,
        integral=-b*sinh(x)*cosh(x)/(2*a*(a + b)*(a + b*cosh(x)**2)) + (2*a + b)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(2*a**(sympy.S(3)/2)*(a + b)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cosh(x)**2)**(-3),
        variable=x,
        num_steps=5,
        integral=-b*sinh(x)*cosh(x)/(4*a*(a + b)*(a + b*cosh(x)**2)**2) - 3*b*(2*a + b)*sinh(x)*cosh(x)/(8*a**2*(a + b)**2*(a + b*cosh(x)**2)) + (8*a**2 + 8*a*b + 3*b**2)*atanh(sqrt(a)*tanh(x)/sqrt(a + b))/(8*a**(sympy.S(5)/2)*(a + b)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**2 + 1),
        variable=x,
        num_steps=2,
        integral=sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/2,
    ),
    RubiTestSuiteCase(
        integrand=(cosh(x)**2 + 1)**(-2),
        variable=x,
        num_steps=4,
        integral=3*sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/8 - sinh(x)*cosh(x)/(4*cosh(x)**2 + 4),
    ),
    RubiTestSuiteCase(
        integrand=(cosh(x)**2 + 1)**(-3),
        variable=x,
        num_steps=5,
        integral=19*sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/64 - 9*sinh(x)*cosh(x)/(32*cosh(x)**2 + 32) - sinh(x)*cosh(x)/(8*(cosh(x)**2 + 1)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=coth(x),
    ),
    RubiTestSuiteCase(
        integrand=(1 - cosh(x)**2)**(-2),
        variable=x,
        num_steps=3,
        integral=-coth(x)**3/3 + coth(x),
    ),
    RubiTestSuiteCase(
        integrand=(1 - cosh(x)**2)**(-3),
        variable=x,
        num_steps=3,
        integral=coth(x)**5/5 - 2*coth(x)**3/3 + coth(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=-I*sqrt(a + b*cosh(x)**2)*elliptic_e(I*x + pi/2, -b/a)/sqrt(1 + b*cosh(x)**2/a),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(cosh(x)**2 + 1),
        variable=x,
        num_steps=1,
        integral=-I*elliptic_e(I*x + pi/2, -1),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 - cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=sqrt(-sinh(x)**2)*coth(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(cosh(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=sqrt(sinh(x)**2)*coth(x),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(-cosh(x)**2 - 1),
        variable=x,
        num_steps=2,
        integral=-I*sqrt(-cosh(x)**2 - 1)*elliptic_e(I*x + pi/2, -1)/sqrt(cosh(x)**2 + 1),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cosh(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=I*a*sqrt(1 + b*cosh(x)**2/a)*(a + b)*elliptic_f(I*x + pi/2, -b/a)/(3*sqrt(a + b*cosh(x)**2)) + b*sqrt(a + b*cosh(x)**2)*sinh(x)*cosh(x)/3 - 2*I*sqrt(a + b*cosh(x)**2)*(2*a + b)*elliptic_e(I*x + pi/2, -b/a)/(3*sqrt(1 + b*cosh(x)**2/a)),
    ),
    RubiTestSuiteCase(
        integrand=(cosh(x)**2 + 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=sqrt(cosh(x)**2 + 1)*sinh(x)*cosh(x)/3 - 2*I*elliptic_e(I*x + pi/2, -1) + 2*I*elliptic_f(I*x + pi/2, -1)/3,
    ),
    RubiTestSuiteCase(
        integrand=(1 - cosh(x)**2)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=(-sinh(x)**2)**(sympy.S(3)/2)*coth(x)/3 + 2*sqrt(-sinh(x)**2)*coth(x)/3,
    ),
    RubiTestSuiteCase(
        integrand=(cosh(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=(sinh(x)**2)**(sympy.S(3)/2)*coth(x)/3 - 2*sqrt(sinh(x)**2)*coth(x)/3,
    ),
    RubiTestSuiteCase(
        integrand=(-cosh(x)**2 - 1)**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=-sqrt(-cosh(x)**2 - 1)*sinh(x)*cosh(x)/3 + 2*I*sqrt(-cosh(x)**2 - 1)*elliptic_e(I*x + pi/2, -1)/sqrt(cosh(x)**2 + 1) + 2*I*sqrt(cosh(x)**2 + 1)*elliptic_f(I*x + pi/2, -1)/(3*sqrt(-cosh(x)**2 - 1)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a + b*cosh(x)**2),
        variable=x,
        num_steps=2,
        integral=-I*sqrt(1 + b*cosh(x)**2/a)*elliptic_f(I*x + pi/2, -b/a)/sqrt(a + b*cosh(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(cosh(x)**2 + 1),
        variable=x,
        num_steps=1,
        integral=-I*elliptic_f(I*x + pi/2, -1),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(1 - cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=-sinh(x)*atanh(cosh(x))/sqrt(-sinh(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(cosh(x)**2 - 1),
        variable=x,
        num_steps=3,
        integral=-sinh(x)*atanh(cosh(x))/sqrt(sinh(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(-cosh(x)**2 - 1),
        variable=x,
        num_steps=2,
        integral=-I*sqrt(cosh(x)**2 + 1)*elliptic_f(I*x + pi/2, -1)/sqrt(-cosh(x)**2 - 1),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**3),
        variable=x,
        num_steps=8,
        integral=2*atanh(sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))) + 2*atanh(sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))) + 2*atanh(sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a - b*cosh(x)**3),
        variable=x,
        num_steps=8,
        integral=2*atanh(sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))) + 2*atanh(sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))) + 2*atanh(sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3))*tanh(x/2)/sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3)))/(3*a**(sympy.S(2)/3)*sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3))*sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**3 + 1),
        variable=x,
        num_steps=7,
        integral=-2*(-3)**(sympy.S(3)/4)*atan((-3)**(sympy.S(1)/4)*tanh(x/2))/(3*(3 + 3*(-1)**(sympy.S(2)/3))) - 2*(-3)**(sympy.S(3)/4)*atanh((-3)**(sympy.S(1)/4)*tanh(x/2))/(3*(3 - 3*(-1)**(sympy.S(1)/3))) + sinh(x)/(3*cosh(x) + 3),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**3),
        variable=x,
        num_steps=7,
        integral=-2*(-3)**(sympy.S(1)/4)*atan((-3)**(sympy.S(3)/4)*tanh(x/2)/3)/(3*(1 - (-1)**(sympy.S(2)/3))) - 2*(-3)**(sympy.S(1)/4)*atanh((-3)**(sympy.S(3)/4)*tanh(x/2)/3)/(3*(1 + (-1)**(sympy.S(1)/3))) - sinh(x)/(3 - 3*cosh(x)),
    ),
    RubiTestSuiteCase(
        integrand=1/(a - b*cosh(x)**4),
        variable=x,
        num_steps=4,
        integral=atanh(a**(sympy.S(1)/4)*tanh(x)/sqrt(sqrt(a) + sqrt(b)))/(2*a**(sympy.S(3)/4)*sqrt(sqrt(a) + sqrt(b))) + atanh(a**(sympy.S(1)/4)*tanh(x)/sqrt(sqrt(a) - sqrt(b)))/(2*a**(sympy.S(3)/4)*sqrt(sqrt(a) - sqrt(b))),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**4 + 1),
        variable=x,
        num_steps=10,
        integral=sqrt(1 + sqrt(2))*log(sqrt(2)*coth(x)**2 + sqrt(2 + 2*sqrt(2))*coth(x) + 1)/8 - sqrt(1 + sqrt(2))*log(2*coth(x)**2 - 2*sqrt(1 + sqrt(2))*coth(x) + sqrt(2))/8 - atan((-2*coth(x) + sqrt(1 + sqrt(2)))/sqrt(-1 + sqrt(2)))/(4*sqrt(1 + sqrt(2))) + atan((2*coth(x) + sqrt(1 + sqrt(2)))/sqrt(-1 + sqrt(2)))/(4*sqrt(1 + sqrt(2))),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**4),
        variable=x,
        num_steps=3,
        integral=coth(x)/2 + sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/4,
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**5),
        variable=x,
        num_steps=12,
        integral=2*atanh(sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) - b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) + b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + b**(sympy.S(1)/5))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**6),
        variable=x,
        num_steps=7,
        integral=atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))) + atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))) + atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) + b**(sympy.S(1)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a + b*cosh(x)**8),
        variable=x,
        num_steps=9,
        integral=-atanh((-a)**(sympy.S(1)/8)*tanh(x)/sqrt(I*b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4)))/(4*(-a)**(sympy.S(7)/8)*sqrt(I*b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4))) - atanh((-a)**(sympy.S(1)/8)*tanh(x)/sqrt(-I*b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4)))/(4*(-a)**(sympy.S(7)/8)*sqrt(-I*b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4))) - atanh((-a)**(sympy.S(1)/8)*tanh(x)/sqrt(b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4)))/(4*(-a)**(sympy.S(7)/8)*sqrt(b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4))) - atanh((-a)**(sympy.S(1)/8)*tanh(x)/sqrt(-b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4)))/(4*(-a)**(sympy.S(7)/8)*sqrt(-b**(sympy.S(1)/4) + (-a)**(sympy.S(1)/4))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a - b*cosh(x)**5),
        variable=x,
        num_steps=12,
        integral=2*atanh(sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(4)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(3)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(2)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + (-1)**(sympy.S(1)/5)*b**(sympy.S(1)/5))) + 2*atanh(sqrt(a**(sympy.S(1)/5) + b**(sympy.S(1)/5))*tanh(x/2)/sqrt(a**(sympy.S(1)/5) - b**(sympy.S(1)/5)))/(5*a**(sympy.S(4)/5)*sqrt(a**(sympy.S(1)/5) - b**(sympy.S(1)/5))*sqrt(a**(sympy.S(1)/5) + b**(sympy.S(1)/5))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a - b*cosh(x)**6),
        variable=x,
        num_steps=7,
        integral=atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) - (-1)**(sympy.S(2)/3)*b**(sympy.S(1)/3))) + atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) + (-1)**(sympy.S(1)/3)*b**(sympy.S(1)/3))) + atanh(a**(sympy.S(1)/6)*tanh(x)/sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/6)*sqrt(a**(sympy.S(1)/3) - b**(sympy.S(1)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(a - b*cosh(x)**8),
        variable=x,
        num_steps=9,
        integral=atanh(a**(sympy.S(1)/8)*tanh(x)/sqrt(a**(sympy.S(1)/4) + I*b**(sympy.S(1)/4)))/(4*a**(sympy.S(7)/8)*sqrt(a**(sympy.S(1)/4) + I*b**(sympy.S(1)/4))) + atanh(a**(sympy.S(1)/8)*tanh(x)/sqrt(a**(sympy.S(1)/4) - I*b**(sympy.S(1)/4)))/(4*a**(sympy.S(7)/8)*sqrt(a**(sympy.S(1)/4) - I*b**(sympy.S(1)/4))) + atanh(a**(sympy.S(1)/8)*tanh(x)/sqrt(a**(sympy.S(1)/4) + b**(sympy.S(1)/4)))/(4*a**(sympy.S(7)/8)*sqrt(a**(sympy.S(1)/4) + b**(sympy.S(1)/4))) + atanh(a**(sympy.S(1)/8)*tanh(x)/sqrt(a**(sympy.S(1)/4) - b**(sympy.S(1)/4)))/(4*a**(sympy.S(7)/8)*sqrt(a**(sympy.S(1)/4) - b**(sympy.S(1)/4))),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**5 + 1),
        variable=x,
        num_steps=11,
        integral=-2*atan(tanh(x/2)/sqrt(-(1 - (-1)**(sympy.S(1)/5))/(1 + (-1)**(sympy.S(1)/5))))/(5*sqrt(-1 + (-1)**(sympy.S(2)/5))) - 2*sqrt(-(1 + (-1)**(sympy.S(3)/5))/(1 - (-1)**(sympy.S(3)/5)))*atan(sqrt(-(1 + (-1)**(sympy.S(3)/5))/(1 - (-1)**(sympy.S(3)/5)))*tanh(x/2))/(5 + 5*(-1)**(sympy.S(3)/5)) + 2*atanh(sqrt((1 - (-1)**(sympy.S(2)/5))/(1 + (-1)**(sympy.S(2)/5)))*tanh(x/2))/(5*sqrt(1 - (-1)**(sympy.S(4)/5))) + 2*atanh(sqrt((1 - (-1)**(sympy.S(4)/5))/(1 + (-1)**(sympy.S(4)/5)))*tanh(x/2))/(5*sqrt(1 + (-1)**(sympy.S(3)/5))) + sinh(x)/(5*cosh(x) + 5),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**6 + 1),
        variable=x,
        num_steps=7,
        integral=sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/6 + atanh(tanh(x)/sqrt(1 - (-1)**(sympy.S(1)/3)))/(3*sqrt(1 - (-1)**(sympy.S(1)/3))) + atanh(tanh(x)/sqrt(1 + (-1)**(sympy.S(2)/3)))/(3*sqrt(1 + (-1)**(sympy.S(2)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(cosh(x)**8 + 1),
        variable=x,
        num_steps=9,
        integral=atanh(tanh(x)/sqrt(1 - (-1)**(sympy.S(1)/4)))/(4*sqrt(1 - (-1)**(sympy.S(1)/4))) + atanh(tanh(x)/sqrt(1 + (-1)**(sympy.S(1)/4)))/(4*sqrt(1 + (-1)**(sympy.S(1)/4))) + atanh(tanh(x)/sqrt(1 - (-1)**(sympy.S(3)/4)))/(4*sqrt(1 - (-1)**(sympy.S(3)/4))) + atanh(tanh(x)/sqrt(1 + (-1)**(sympy.S(3)/4)))/(4*sqrt(1 + (-1)**(sympy.S(3)/4))),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**5),
        variable=x,
        num_steps=11,
        integral=-2*atan(tanh(x/2)/sqrt(-(1 - (-1)**(sympy.S(2)/5))/(1 + (-1)**(sympy.S(2)/5))))/(5*sqrt(-1 + (-1)**(sympy.S(4)/5))) + 2*atan(sqrt(-(1 + (-1)**(sympy.S(4)/5))/(1 - (-1)**(sympy.S(4)/5)))*tanh(x/2))/(5*sqrt(-1 - (-1)**(sympy.S(3)/5))) + 2*atanh(sqrt((1 - (-1)**(sympy.S(1)/5))/(1 + (-1)**(sympy.S(1)/5)))*tanh(x/2))/(5*sqrt(1 - (-1)**(sympy.S(2)/5))) + 2*atanh(sqrt((1 - (-1)**(sympy.S(3)/5))/(1 + (-1)**(sympy.S(3)/5)))*tanh(x/2))/(5*sqrt(1 + (-1)**(sympy.S(1)/5))) - sinh(x)/(5 - 5*cosh(x)),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**6),
        variable=x,
        num_steps=8,
        integral=coth(x)/3 + atanh(tanh(x)/sqrt(1 + (-1)**(sympy.S(1)/3)))/(3*sqrt(1 + (-1)**(sympy.S(1)/3))) + atanh(tanh(x)/sqrt(1 - (-1)**(sympy.S(2)/3)))/(3*sqrt(1 - (-1)**(sympy.S(2)/3))),
    ),
    RubiTestSuiteCase(
        integrand=1/(1 - cosh(x)**8),
        variable=x,
        num_steps=10,
        integral=coth(x)/4 + sqrt(2)*atanh(sqrt(2)*tanh(x)/2)/8 + atanh(tanh(x)/sqrt(1 - I))/(4*sqrt(1 - I)) + atanh(tanh(x)/sqrt(1 + I))/(4*sqrt(1 + I)),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/(cosh(x)**2 + 1),
        variable=x,
        num_steps=4,
        integral=-log(cosh(x)**2 + 1)/2 + log(cosh(x)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cosh(x)**2)*tanh(x),
        variable=x,
        num_steps=4,
        integral=-sqrt(a)*atanh(sqrt(a + b*cosh(x)**2)/sqrt(a)) + sqrt(a + b*cosh(x)**2),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(a + b*cosh(x)**2),
        variable=x,
        num_steps=3,
        integral=-atanh(sqrt(a + b*cosh(x)**2)/sqrt(a))/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(cosh(x)**2 + 1),
        variable=x,
        num_steps=3,
        integral=-atanh(sqrt(cosh(x)**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(1 - cosh(x)**2),
        variable=x,
        num_steps=4,
        integral=-atanh(sqrt(-sinh(x)**2)),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)**3/(a + b*cosh(x)**3),
        variable=x,
        num_steps=11,
        integral=-log(a + b*cosh(x)**3)/(3*a) + log(cosh(x))/a + sech(x)**2/(2*a) + b**(sympy.S(2)/3)*log(a**(sympy.S(1)/3) + b**(sympy.S(1)/3)*cosh(x))/(3*a**(sympy.S(5)/3)) - b**(sympy.S(2)/3)*log(a**(sympy.S(2)/3) - a**(sympy.S(1)/3)*b**(sympy.S(1)/3)*cosh(x) + b**(sympy.S(2)/3)*cosh(x)**2)/(6*a**(sympy.S(5)/3)) - sqrt(3)*b**(sympy.S(2)/3)*atan(sqrt(3)*(a**(sympy.S(1)/3) - 2*b**(sympy.S(1)/3)*cosh(x))/(3*a**(sympy.S(1)/3)))/(3*a**(sympy.S(5)/3)),
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(a + b*cosh(x)**3),
        variable=x,
        num_steps=4,
        integral=-2*atanh(sqrt(a + b*cosh(x)**3)/sqrt(a))/(3*sqrt(a)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cosh(x)**3)*tanh(x),
        variable=x,
        num_steps=5,
        integral=-2*sqrt(a)*atanh(sqrt(a + b*cosh(x)**3)/sqrt(a))/3 + 2*sqrt(a + b*cosh(x)**3)/3,
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(a + b*cosh(x)**n),
        variable=x,
        num_steps=4,
        integral=-2*atanh(sqrt(a + b*cosh(x)**n)/sqrt(a))/(sqrt(a)*n),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cosh(x)**n)*tanh(x),
        variable=x,
        num_steps=5,
        integral=-2*sqrt(a)*atanh(sqrt(a + b*cosh(x)**n)/sqrt(a))/n + 2*sqrt(a + b*cosh(x)**n)/n,
    ),
]
