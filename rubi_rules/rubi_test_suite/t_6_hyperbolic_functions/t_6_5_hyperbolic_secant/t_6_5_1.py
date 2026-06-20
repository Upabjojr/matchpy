# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.5 Hyperbolic secant/6.5.1 (c+d x)^m (a+b sech)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.5 Hyperbolic secant/6.5.1 (c+d x)^m (a+b sech)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d = symbols('a b c d')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(c + d*x)**3*sech(a + b*x),
        variable=x,
        num_steps=9,
        integral=(((Integer(2) * ((Symbol('c') + (Symbol('d') * x)))**(Integer(3)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * sympy.I * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((Integer(3) * sympy.I * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((Integer(6) * sympy.I * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * sympy.I * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + (Integer(-1) * ((Integer(6) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(4), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1)))) + ((Integer(6) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(4), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)**2*sech(a + b*x),
        variable=x,
        num_steps=7,
        integral=(((Integer(2) * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * sympy.I * Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((Integer(2) * sympy.I * Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((Integer(2) * sympy.I * (Symbol('d'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * sympy.I * (Symbol('d'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)*sech(a + b*x),
        variable=x,
        num_steps=5,
        integral=(((Integer(2) * (Symbol('c') + (Symbol('d') * x)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((sympy.I * Symbol('d') * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((sympy.I * Symbol('d') * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sech(a + b*x)/(c + d*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.sech((Symbol('a') + (Symbol('b') * x))) * ((Symbol('c') + (Symbol('d') * x)))**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)**3*sech(a + b*x)**2,
        variable=x,
        num_steps=6,
        integral=((((Symbol('c') + (Symbol('d') * x)))**(Integer(3)) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * (Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * (Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + ((Integer(3) * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(3), (Integer(-1) * (sympy.E)**((Integer(2) * (Symbol('a') + (Symbol('b') * x))))))) * ((Integer(2) * (Symbol('b'))**(Integer(4))))**(Integer(-1))) + ((((Symbol('c') + (Symbol('d') * x)))**(Integer(3)) * sympy.tanh((Symbol('a') + (Symbol('b') * x)))) * (Symbol('b'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)**2*sech(a + b*x)**2,
        variable=x,
        num_steps=5,
        integral=((((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * (Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + (Integer(-1) * (((Symbol('d'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * (Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + ((((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.tanh((Symbol('a') + (Symbol('b') * x)))) * (Symbol('b'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)*sech(a + b*x)**2,
        variable=x,
        num_steps=2,
        integral=(c + d*x)*tanh(a + b*x)/b - d*log(cosh(a + b*x))/b**2,
    ),
    RubiTestSuiteCase(
        integrand=sech(a + b*x)**2/(c + d*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')(((sympy.sech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * ((Symbol('c') + (Symbol('d') * x)))**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)**3*sech(a + b*x)**3,
        variable=x,
        num_steps=15,
        integral=((Integer(-1) * ((Integer(6) * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + ((((Symbol('c') + (Symbol('d') * x)))**(Integer(3)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * sympy.I * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1)))) + ((Integer(3) * sympy.I * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1))) + ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(2)) * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(4), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1)))) + ((Integer(3) * sympy.I * (Symbol('d'))**(Integer(3)) * sympy.Function('PolyLog')(Integer(4), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(4)))**(Integer(-1))) + ((Integer(3) * Symbol('d') * ((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.sech((Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1))) + ((((Symbol('c') + (Symbol('d') * x)))**(Integer(3)) * sympy.sech((Symbol('a') + (Symbol('b') * x))) * sympy.tanh((Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)**2*sech(a + b*x)**3,
        variable=x,
        num_steps=9,
        integral=(((((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * (((Symbol('d'))**(Integer(2)) * sympy.atan(sympy.sinh((Symbol('a') + (Symbol('b') * x))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + (Integer(-1) * ((sympy.I * Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((sympy.I * Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((sympy.I * (Symbol('d'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * ((sympy.I * (Symbol('d'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + ((Symbol('d') * (Symbol('c') + (Symbol('d') * x)) * sympy.sech((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((((Symbol('c') + (Symbol('d') * x)))**(Integer(2)) * sympy.sech((Symbol('a') + (Symbol('b') * x))) * sympy.tanh((Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(c + d*x)*sech(a + b*x)**3,
        variable=x,
        num_steps=6,
        integral=((((Symbol('c') + (Symbol('d') * x)) * sympy.atan((sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((sympy.I * Symbol('d') * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + ((sympy.I * Symbol('d') * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1))) + ((Symbol('d') * sympy.sech((Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1))) + (((Symbol('c') + (Symbol('d') * x)) * sympy.sech((Symbol('a') + (Symbol('b') * x))) * sympy.tanh((Symbol('a') + (Symbol('b') * x)))) * ((Integer(2) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sech(a + b*x)**3/(c + d*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')(((sympy.sech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * ((Symbol('c') + (Symbol('d') * x)))**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=-x*sqrt(sech(x))/3 + x/sech(x)**(sympy.S(3)/2),
        variable=x,
        num_steps=4,
        integral=2*x*sinh(x)/(3*sqrt(sech(x))) - 4/(9*sech(x)**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=-3*x/(5*sqrt(sech(x))) + x/sech(x)**(sympy.S(5)/2),
        variable=x,
        num_steps=4,
        integral=2*x*sinh(x)/(5*sech(x)**(sympy.S(3)/2)) - 4/(25*sech(x)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=-5*x*sqrt(sech(x))/21 + x/sech(x)**(sympy.S(7)/2),
        variable=x,
        num_steps=5,
        integral=10*x*sinh(x)/(21*sqrt(sech(x))) + 2*x*sinh(x)/(7*sech(x)**(sympy.S(5)/2)) - 20/(63*sech(x)**(sympy.S(3)/2)) - 4/(49*sech(x)**(sympy.S(7)/2)),
    ),
    RubiTestSuiteCase(
        integrand=-x**2*sqrt(sech(x))/3 + x**2/sech(x)**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=2*x**2*sinh(x)/(3*sqrt(sech(x))) - 8*x/(9*sech(x)**(sympy.S(3)/2)) + 16*sinh(x)/(27*sqrt(sech(x))) - 16*I*sqrt(cosh(x))*elliptic_f(I*x/2, 2)*sqrt(sech(x))/27,
    ),
]
