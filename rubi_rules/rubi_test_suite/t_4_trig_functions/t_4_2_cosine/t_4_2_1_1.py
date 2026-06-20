# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.2 Cosine/4.2.1.1 (a+b cos)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.2 Cosine/4.2.1.1 (a+b cos)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, n = symbols('a b c d n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(7)/2),
        variable=x,
        num_steps=4,
        integral=256*a**4*sin(c + d*x)/(35*d*sqrt(a*cos(c + d*x) + a)) + 64*a**3*sqrt(a*cos(c + d*x) + a)*sin(c + d*x)/(35*d) + 24*a**2*(a*cos(c + d*x) + a)**(sympy.S(3)/2)*sin(c + d*x)/(35*d) + 2*a*(a*cos(c + d*x) + a)**(sympy.S(5)/2)*sin(c + d*x)/(7*d),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(5)/2),
        variable=x,
        num_steps=3,
        integral=64*a**3*sin(c + d*x)/(15*d*sqrt(a*cos(c + d*x) + a)) + 16*a**2*sqrt(a*cos(c + d*x) + a)*sin(c + d*x)/(15*d) + 2*a*(a*cos(c + d*x) + a)**(sympy.S(3)/2)*sin(c + d*x)/(5*d),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(3)/2),
        variable=x,
        num_steps=2,
        integral=8*a**2*sin(c + d*x)/(3*d*sqrt(a*cos(c + d*x) + a)) + 2*a*sqrt(a*cos(c + d*x) + a)*sin(c + d*x)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a*cos(c + d*x) + a),
        variable=x,
        num_steps=1,
        integral=2*a*sin(c + d*x)/(d*sqrt(a*cos(c + d*x) + a)),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a*cos(c + d*x) + a),
        variable=x,
        num_steps=2,
        integral=sqrt(2)*atanh(sqrt(2)*sqrt(a)*sin(c + d*x)/(2*sqrt(a*cos(c + d*x) + a)))/(sqrt(a)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(-3)/2),
        variable=x,
        num_steps=3,
        integral=sin(c + d*x)/(2*d*(a*cos(c + d*x) + a)**(sympy.S(3)/2)) + sqrt(2)*atanh(sqrt(2)*sqrt(a)*sin(c + d*x)/(2*sqrt(a*cos(c + d*x) + a)))/(4*a**(sympy.S(3)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(-5)/2),
        variable=x,
        num_steps=4,
        integral=sin(c + d*x)/(4*d*(a*cos(c + d*x) + a)**(sympy.S(5)/2)) + 3*sin(c + d*x)/(16*a*d*(a*cos(c + d*x) + a)**(sympy.S(3)/2)) + 3*sqrt(2)*atanh(sqrt(2)*sqrt(a)*sin(c + d*x)/(2*sqrt(a*cos(c + d*x) + a)))/(32*a**(sympy.S(5)/2)*d),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(4)/3),
        variable=x,
        num_steps=2,
        integral=2*2**(sympy.S(5)/6)*a*(a*cos(c + d*x) + a)**(sympy.S(1)/3)*sin(c + d*x)*hyper((sympy.S(-5)/6, sympy.S.Half), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(d*(cos(c + d*x) + 1)**(sympy.S(5)/6)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(2)/3),
        variable=x,
        num_steps=2,
        integral=2*2**(sympy.S(1)/6)*(a*cos(c + d*x) + a)**(sympy.S(2)/3)*sin(c + d*x)*hyper((sympy.S(-1)/6, sympy.S.Half), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(d*(cos(c + d*x) + 1)**(sympy.S(7)/6)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(1)/3),
        variable=x,
        num_steps=2,
        integral=2**(sympy.S(5)/6)*(a*cos(c + d*x) + a)**(sympy.S(1)/3)*sin(c + d*x)*hyper((sympy.S(1)/6, sympy.S.Half), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(d*(cos(c + d*x) + 1)**(sympy.S(5)/6)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(-1)/3),
        variable=x,
        num_steps=2,
        integral=2**(sympy.S(1)/6)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S(5)/6), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(d*(a*cos(c + d*x) + a)**(sympy.S(1)/3)*(cos(c + d*x) + 1)**(sympy.S(1)/6)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(-2)/3),
        variable=x,
        num_steps=2,
        integral=2**(sympy.S(5)/6)*(cos(c + d*x) + 1)**(sympy.S(1)/6)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S(7)/6), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(2*d*(a*cos(c + d*x) + a)**(sympy.S(2)/3)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**(sympy.S(-4)/3),
        variable=x,
        num_steps=2,
        integral=2**(sympy.S(1)/6)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S(11)/6), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(2*a*d*(a*cos(c + d*x) + a)**(sympy.S(1)/3)*(cos(c + d*x) + 1)**(sympy.S(1)/6)),
    ),
    RubiTestSuiteCase(
        integrand=(a*cos(c + d*x) + a)**n,
        variable=x,
        num_steps=2,
        integral=2**(n + sympy.S.Half)*(a*cos(c + d*x) + a)**n*(cos(c + d*x) + 1)**(-n + sympy.S(-1)/2)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S.Half - n), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/d,
    ),
    RubiTestSuiteCase(
        integrand=(-a*cos(c + d*x) + a)**n,
        variable=x,
        num_steps=2,
        integral=-2**(n + sympy.S.Half)*(1 - cos(c + d*x))**(-n + sympy.S(-1)/2)*(-a*cos(c + d*x) + a)**n*sin(c + d*x)*hyper((sympy.S.Half, sympy.S.Half - n), (sympy.S(3)/2,), cos(c + d*x)/2 + sympy.S.Half)/d,
    ),
    RubiTestSuiteCase(
        integrand=(2*cos(c + d*x) + 2)**n,
        variable=x,
        num_steps=1,
        integral=2**(2*n + sympy.S.Half)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S.Half - n), (sympy.S(3)/2,), sympy.S.Half - cos(c + d*x)/2)/(d*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(2 - 2*cos(c + d*x))**n,
        variable=x,
        num_steps=1,
        integral=-2**(2*n + sympy.S.Half)*sin(c + d*x)*hyper((sympy.S.Half, sympy.S.Half - n), (sympy.S(3)/2,), cos(c + d*x)/2 + sympy.S.Half)/(d*sqrt(1 - cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=1/(3*cos(c + d*x) + 5),
        variable=x,
        num_steps=1,
        integral=x/4 - atan(sin(c + d*x)/(cos(c + d*x) + 3))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) + 5)**(-2),
        variable=x,
        num_steps=3,
        integral=5*x/64 - 5*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(32*d) - 3*sin(c + d*x)/(16*d*(3*cos(c + d*x) + 5)),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) + 5)**(-3),
        variable=x,
        num_steps=4,
        integral=59*x/2048 - 59*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(1024*d) - 45*sin(c + d*x)/(512*d*(3*cos(c + d*x) + 5)) - 3*sin(c + d*x)/(32*d*(3*cos(c + d*x) + 5)**2),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) + 5)**(-4),
        variable=x,
        num_steps=5,
        integral=385*x/32768 - 385*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(16384*d) - 311*sin(c + d*x)/(8192*d*(3*cos(c + d*x) + 5)) - 25*sin(c + d*x)/(512*d*(3*cos(c + d*x) + 5)**2) - sin(c + d*x)/(16*d*(3*cos(c + d*x) + 5)**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(5 - 3*cos(c + d*x)),
        variable=x,
        num_steps=1,
        integral=x/4 + atan(sin(c + d*x)/(3 - cos(c + d*x)))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(5 - 3*cos(c + d*x))**(-2),
        variable=x,
        num_steps=3,
        integral=5*x/64 + 5*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(32*d) + 3*sin(c + d*x)/(16*d*(5 - 3*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(5 - 3*cos(c + d*x))**(-3),
        variable=x,
        num_steps=4,
        integral=59*x/2048 + 59*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(1024*d) + 45*sin(c + d*x)/(512*d*(5 - 3*cos(c + d*x))) + 3*sin(c + d*x)/(32*d*(5 - 3*cos(c + d*x))**2),
    ),
    RubiTestSuiteCase(
        integrand=(5 - 3*cos(c + d*x))**(-4),
        variable=x,
        num_steps=5,
        integral=385*x/32768 + 385*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(16384*d) + 311*sin(c + d*x)/(8192*d*(5 - 3*cos(c + d*x))) + 25*sin(c + d*x)/(512*d*(5 - 3*cos(c + d*x))**2) + sin(c + d*x)/(16*d*(5 - 3*cos(c + d*x))**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(3*cos(c + d*x) - 5),
        variable=x,
        num_steps=1,
        integral=-x/4 - atan(sin(c + d*x)/(3 - cos(c + d*x)))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) - 5)**(-2),
        variable=x,
        num_steps=3,
        integral=5*x/64 + 5*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(32*d) + 3*sin(c + d*x)/(16*d*(5 - 3*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) - 5)**(-3),
        variable=x,
        num_steps=4,
        integral=-59*x/2048 - 59*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(1024*d) - 45*sin(c + d*x)/(512*d*(5 - 3*cos(c + d*x))) - 3*sin(c + d*x)/(32*d*(5 - 3*cos(c + d*x))**2),
    ),
    RubiTestSuiteCase(
        integrand=(3*cos(c + d*x) - 5)**(-4),
        variable=x,
        num_steps=5,
        integral=385*x/32768 + 385*atan(sin(c + d*x)/(3 - cos(c + d*x)))/(16384*d) + 311*sin(c + d*x)/(8192*d*(5 - 3*cos(c + d*x))) + 25*sin(c + d*x)/(512*d*(5 - 3*cos(c + d*x))**2) + sin(c + d*x)/(16*d*(5 - 3*cos(c + d*x))**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(-3*cos(c + d*x) - 5),
        variable=x,
        num_steps=1,
        integral=-x/4 + atan(sin(c + d*x)/(cos(c + d*x) + 3))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(-3*cos(c + d*x) - 5)**(-2),
        variable=x,
        num_steps=3,
        integral=5*x/64 - 5*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(32*d) - 3*sin(c + d*x)/(16*d*(3*cos(c + d*x) + 5)),
    ),
    RubiTestSuiteCase(
        integrand=(-3*cos(c + d*x) - 5)**(-3),
        variable=x,
        num_steps=4,
        integral=-59*x/2048 + 59*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(1024*d) + 45*sin(c + d*x)/(512*d*(3*cos(c + d*x) + 5)) + 3*sin(c + d*x)/(32*d*(3*cos(c + d*x) + 5)**2),
    ),
    RubiTestSuiteCase(
        integrand=(-3*cos(c + d*x) - 5)**(-4),
        variable=x,
        num_steps=5,
        integral=385*x/32768 - 385*atan(sin(c + d*x)/(cos(c + d*x) + 3))/(16384*d) - 311*sin(c + d*x)/(8192*d*(3*cos(c + d*x) + 5)) - 25*sin(c + d*x)/(512*d*(3*cos(c + d*x) + 5)**2) - sin(c + d*x)/(16*d*(3*cos(c + d*x) + 5)**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(5*cos(c + d*x) + 3),
        variable=x,
        num_steps=2,
        integral=-log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(4*d) + log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) + 3)**(-2),
        variable=x,
        num_steps=4,
        integral=3*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(64*d) - 3*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(64*d) + 5*sin(c + d*x)/(16*d*(5*cos(c + d*x) + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) + 3)**(-3),
        variable=x,
        num_steps=5,
        integral=-43*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(2048*d) + 43*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(2048*d) - 45*sin(c + d*x)/(512*d*(5*cos(c + d*x) + 3)) + 5*sin(c + d*x)/(32*d*(5*cos(c + d*x) + 3)**2),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) + 3)**(-4),
        variable=x,
        num_steps=6,
        integral=279*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(32768*d) - 279*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(32768*d) + 995*sin(c + d*x)/(24576*d*(5*cos(c + d*x) + 3)) - 25*sin(c + d*x)/(512*d*(5*cos(c + d*x) + 3)**2) + 5*sin(c + d*x)/(48*d*(5*cos(c + d*x) + 3)**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(3 - 5*cos(c + d*x)),
        variable=x,
        num_steps=2,
        integral=log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(4*d) - log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(3 - 5*cos(c + d*x))**(-2),
        variable=x,
        num_steps=4,
        integral=-3*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(64*d) + 3*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(64*d) - 5*sin(c + d*x)/(16*d*(3 - 5*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(3 - 5*cos(c + d*x))**(-3),
        variable=x,
        num_steps=5,
        integral=43*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(2048*d) - 43*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(2048*d) + 45*sin(c + d*x)/(512*d*(3 - 5*cos(c + d*x))) - 5*sin(c + d*x)/(32*d*(3 - 5*cos(c + d*x))**2),
    ),
    RubiTestSuiteCase(
        integrand=(3 - 5*cos(c + d*x))**(-4),
        variable=x,
        num_steps=6,
        integral=-279*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(32768*d) + 279*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(32768*d) - 995*sin(c + d*x)/(24576*d*(3 - 5*cos(c + d*x))) + 25*sin(c + d*x)/(512*d*(3 - 5*cos(c + d*x))**2) - 5*sin(c + d*x)/(48*d*(3 - 5*cos(c + d*x))**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(5*cos(c + d*x) - 3),
        variable=x,
        num_steps=2,
        integral=-log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(4*d) + log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) - 3)**(-2),
        variable=x,
        num_steps=4,
        integral=-3*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(64*d) + 3*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(64*d) - 5*sin(c + d*x)/(16*d*(3 - 5*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) - 3)**(-3),
        variable=x,
        num_steps=5,
        integral=-43*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(2048*d) + 43*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(2048*d) - 45*sin(c + d*x)/(512*d*(3 - 5*cos(c + d*x))) + 5*sin(c + d*x)/(32*d*(3 - 5*cos(c + d*x))**2),
    ),
    RubiTestSuiteCase(
        integrand=(5*cos(c + d*x) - 3)**(-4),
        variable=x,
        num_steps=6,
        integral=-279*log(-2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(32768*d) + 279*log(2*sin(c/2 + d*x/2) + cos(c/2 + d*x/2))/(32768*d) - 995*sin(c + d*x)/(24576*d*(3 - 5*cos(c + d*x))) + 25*sin(c + d*x)/(512*d*(3 - 5*cos(c + d*x))**2) - 5*sin(c + d*x)/(48*d*(3 - 5*cos(c + d*x))**3),
    ),
    RubiTestSuiteCase(
        integrand=1/(-5*cos(c + d*x) - 3),
        variable=x,
        num_steps=2,
        integral=log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(4*d) - log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(4*d),
    ),
    RubiTestSuiteCase(
        integrand=(-5*cos(c + d*x) - 3)**(-2),
        variable=x,
        num_steps=4,
        integral=3*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(64*d) - 3*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(64*d) + 5*sin(c + d*x)/(16*d*(5*cos(c + d*x) + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(-5*cos(c + d*x) - 3)**(-3),
        variable=x,
        num_steps=5,
        integral=43*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(2048*d) - 43*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(2048*d) + 45*sin(c + d*x)/(512*d*(5*cos(c + d*x) + 3)) - 5*sin(c + d*x)/(32*d*(5*cos(c + d*x) + 3)**2),
    ),
    RubiTestSuiteCase(
        integrand=(-5*cos(c + d*x) - 3)**(-4),
        variable=x,
        num_steps=6,
        integral=279*log(-sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(32768*d) - 279*log(sin(c/2 + d*x/2) + 2*cos(c/2 + d*x/2))/(32768*d) + 995*sin(c + d*x)/(24576*d*(5*cos(c + d*x) + 3)) - 25*sin(c + d*x)/(512*d*(5*cos(c + d*x) + 3)**2) + 5*sin(c + d*x)/(48*d*(5*cos(c + d*x) + 3)**3),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=7,
        integral=16*a*b*sqrt(a + b*cos(c + d*x))*sin(c + d*x)/(15*d) - 16*a*sqrt((a + b*cos(c + d*x))/(a + b))*(a**2 - b**2)*elliptic_f(c/2 + d*x/2, 2*b/(a + b))/(15*d*sqrt(a + b*cos(c + d*x))) + 2*b*(a + b*cos(c + d*x))**(sympy.S(3)/2)*sin(c + d*x)/(5*d) + sqrt(a + b*cos(c + d*x))*(46*a**2 + 18*b**2)*elliptic_e(c/2 + d*x/2, 2*b/(a + b))/(15*d*sqrt((a + b*cos(c + d*x))/(a + b))),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=8*a*sqrt(a + b*cos(c + d*x))*elliptic_e(c/2 + d*x/2, 2*b/(a + b))/(3*d*sqrt((a + b*cos(c + d*x))/(a + b))) + 2*b*sqrt(a + b*cos(c + d*x))*sin(c + d*x)/(3*d) - sqrt((a + b*cos(c + d*x))/(a + b))*(2*a**2 - 2*b**2)*elliptic_f(c/2 + d*x/2, 2*b/(a + b))/(3*d*sqrt(a + b*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(a + b*cos(c + d*x)),
        variable=x,
        num_steps=2,
        integral=2*sqrt(a + b*cos(c + d*x))*elliptic_e(c/2 + d*x/2, 2*b/(a + b))/(d*sqrt((a + b*cos(c + d*x))/(a + b))),
    ),
    RubiTestSuiteCase(
        integrand=1/sqrt(a + b*cos(c + d*x)),
        variable=x,
        num_steps=2,
        integral=2*sqrt((a + b*cos(c + d*x))/(a + b))*elliptic_f(c/2 + d*x/2, 2*b/(a + b))/(d*sqrt(a + b*cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(-3)/2),
        variable=x,
        num_steps=4,
        integral=-2*b*sin(c + d*x)/(d*sqrt(a + b*cos(c + d*x))*(a**2 - b**2)) + 2*sqrt(a + b*cos(c + d*x))*elliptic_e(c/2 + d*x/2, 2*b/(a + b))/(d*sqrt((a + b*cos(c + d*x))/(a + b))*(a**2 - b**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(-5)/2),
        variable=x,
        num_steps=7,
        integral=-8*a*b*sin(c + d*x)/(3*d*sqrt(a + b*cos(c + d*x))*(a**2 - b**2)**2) + 8*a*sqrt(a + b*cos(c + d*x))*elliptic_e(c/2 + d*x/2, 2*b/(a + b))/(3*d*sqrt((a + b*cos(c + d*x))/(a + b))*(a**2 - b**2)**2) - 2*b*sin(c + d*x)/(d*(a + b*cos(c + d*x))**(sympy.S(3)/2)*(3*a**2 - 3*b**2)) - 2*sqrt((a + b*cos(c + d*x))/(a + b))*elliptic_f(c/2 + d*x/2, 2*b/(a + b))/(d*sqrt(a + b*cos(c + d*x))*(3*a**2 - 3*b**2)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(4)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*(a + b)*(a + b*cos(c + d*x))**(sympy.S(1)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S(-4)/3, sympy.S.Half, sympy.S(3)/2, b*(1 - cos(c + d*x))/(a + b), sympy.S.Half - cos(c + d*x)/2)/(d*((a + b*cos(c + d*x))/(a + b))**(sympy.S(1)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(2)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*(a + b*cos(c + d*x))**(sympy.S(2)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S(-2)/3, sympy.S.Half, sympy.S(3)/2, b*(1 - cos(c + d*x))/(a + b), sympy.S.Half - cos(c + d*x)/2)/(d*((a + b*cos(c + d*x))/(a + b))**(sympy.S(2)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(1)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*(a + b*cos(c + d*x))**(sympy.S(1)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S(-1)/3, sympy.S.Half, sympy.S(3)/2, b*(1 - cos(c + d*x))/(a + b), sympy.S.Half - cos(c + d*x)/2)/(d*((a + b*cos(c + d*x))/(a + b))**(sympy.S(1)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(-1)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*((a + b*cos(c + d*x))/(a + b))**(sympy.S(1)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S(1)/3, sympy.S.Half, sympy.S(3)/2, b*(1 - cos(c + d*x))/(a + b), sympy.S.Half - cos(c + d*x)/2)/(d*(a + b*cos(c + d*x))**(sympy.S(1)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(-2)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*((a + b*cos(c + d*x))/(a + b))**(sympy.S(2)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S.Half, sympy.S(2)/3, sympy.S(3)/2, sympy.S.Half - cos(c + d*x)/2, b*(1 - cos(c + d*x))/(a + b))/(d*(a + b*cos(c + d*x))**(sympy.S(2)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**(sympy.S(-4)/3),
        variable=x,
        num_steps=3,
        integral=sqrt(2)*((a + b*cos(c + d*x))/(a + b))**(sympy.S(1)/3)*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S.Half, sympy.S(4)/3, sympy.S(3)/2, sympy.S.Half - cos(c + d*x)/2, b*(1 - cos(c + d*x))/(a + b))/(d*(a + b)*(a + b*cos(c + d*x))**(sympy.S(1)/3)*sqrt(cos(c + d*x) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*cos(c + d*x))**n,
        variable=x,
        num_steps=3,
        integral=sqrt(2)*(a + b*cos(c + d*x))**n*sin(c + d*x)*appellf1(sympy.S.Half, sympy.S.Half, -n, sympy.S(3)/2, sympy.S.Half - cos(c + d*x)/2, b*(1 - cos(c + d*x))/(a + b))/(d*((a + b*cos(c + d*x))/(a + b))**n*sqrt(cos(c + d*x) + 1)),
    ),
]
