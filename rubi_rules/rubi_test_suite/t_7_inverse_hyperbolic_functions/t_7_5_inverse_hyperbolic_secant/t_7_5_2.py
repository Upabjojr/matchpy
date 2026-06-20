# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 7 Inverse hyperbolic functions/7.5 Inverse hyperbolic secant/7.5.2 Inverse hyperbolic secant functions.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '7 Inverse hyperbolic functions/7.5 Inverse hyperbolic secant/7.5.2 Inverse hyperbolic secant functions.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, m, n, p = symbols('a b c d m n p')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=x**3*asech(a + b*x),
        variable=x,
        num_steps=8,
        integral=-a**4*asech(a + b*x)/(4*b**4) + a*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x)*(a + b*x + 1)/(3*b**4) + a*(2*a**2 + 1)*atan(sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(a + b*x))/(2*b**4) + x**4*asech(a + b*x)/4 - x**2*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(12*b**2) - sqrt((-a - b*x + 1)/(a + b*x + 1))*(17*a**2 + 2)*(a + b*x + 1)/(12*b**4),
    ),
    RubiTestSuiteCase(
        integrand=x**2*asech(a + b*x),
        variable=x,
        num_steps=7,
        integral=a**3*asech(a + b*x)/(3*b**3) + 5*a*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(6*b**3) + x**3*asech(a + b*x)/3 - x*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(6*b**2) - (6*a**2 + 1)*atan(sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(a + b*x))/(6*b**3),
    ),
    RubiTestSuiteCase(
        integrand=x*asech(a + b*x),
        variable=x,
        num_steps=6,
        integral=-a**2*asech(a + b*x)/(2*b**2) + a*atan(sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(a + b*x))/b**2 + x**2*asech(a + b*x)/2 - sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x),
        variable=x,
        num_steps=4,
        integral=(a + b*x)*asech(a + b*x)/b - 2*atan(sqrt((-a - b*x + 1)/(a + b*x + 1)))/b,
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)/x,
        variable=x,
        num_steps=14,
        integral=((sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) + (sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) + (Integer(-1) * (sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))) + sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1)))) + sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)/x**2,
        variable=x,
        num_steps=5,
        integral=-asech(a + b*x)/x - b*asech(a + b*x)/a + 2*b*atanh(sqrt(a + 1)*tanh(asech(a + b*x)/2)/sqrt(1 - a))/(a*sqrt(1 - a**2)),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)/x**3,
        variable=x,
        num_steps=7,
        integral=-asech(a + b*x)/(2*x**2) + b*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(2*a*x*(1 - a**2)) - b**2*(1 - 2*a**2)*atanh(sqrt(a + 1)*tanh(asech(a + b*x)/2)/sqrt(1 - a))/(a**2*(1 - a**2)**(sympy.S(3)/2)) + b**2*asech(a + b*x)/(2*a**2),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)/x**4,
        variable=x,
        num_steps=8,
        integral=-asech(a + b*x)/(3*x**3) + b*sqrt((-a - b*x + 1)/(a + b*x + 1))*(a + b*x + 1)/(6*a*x**2*(1 - a**2)) - b**2*sqrt((-a - b*x + 1)/(a + b*x + 1))*(2 - 5*a**2)*(a + b*x + 1)/(6*a**2*x*(1 - a**2)**2) - b**3*asech(a + b*x)/(3*a**3) + b**3*(6*a**4 - 5*a**2 + 2)*atanh(sqrt(a + 1)*tanh(asech(a + b*x)/2)/sqrt(1 - a))/(3*a**3*(1 - a**2)**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=x**2*asech(a + b*x)**2,
        variable=x,
        num_steps=17,
        integral=((Integer(-1) * (x * ((Integer(3) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + ((Integer(2) * Symbol('a') * sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * sympy.asech((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * (((Symbol('a') + (Symbol('b') * x)) * sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * sympy.asech((Symbol('a') + (Symbol('b') * x)))) * ((Integer(3) * (Symbol('b'))**(Integer(3))))**(Integer(-1)))) + (((Symbol('a'))**(Integer(3)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(3) * (Symbol('b'))**(Integer(3))))**(Integer(-1))) + ((Integer(3))**(Integer(-1)) * (x)**(Integer(3)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) + (Integer(-1) * ((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * ((Integer(3) * (Symbol('b'))**(Integer(3))))**(Integer(-1)))) + (Integer(-1) * ((Integer(4) * (Symbol('a'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + ((Integer(2) * Symbol('a') * sympy.log((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + ((sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Integer(3) * (Symbol('b'))**(Integer(3))))**(Integer(-1))) + ((Integer(2) * sympy.I * (Symbol('a'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))) + (Integer(-1) * ((sympy.I * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Integer(3) * (Symbol('b'))**(Integer(3))))**(Integer(-1)))) + (Integer(-1) * ((Integer(2) * sympy.I * (Symbol('a'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x*asech(a + b*x)**2,
        variable=x,
        num_steps=11,
        integral=((Integer(-1) * ((sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * sympy.asech((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + (Integer(-1) * (((Symbol('a'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * (x)**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) + ((Integer(4) * Symbol('a') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + (Integer(-1) * (sympy.log((Symbol('a') + (Symbol('b') * x))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + (Integer(-1) * ((Integer(2) * sympy.I * Symbol('a') * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((Integer(2) * sympy.I * Symbol('a') * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**2,
        variable=x,
        num_steps=8,
        integral=((((Symbol('a') + (Symbol('b') * x)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(4) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * (Symbol('b'))**(Integer(-1)))) + ((Integer(2) * sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * sympy.I * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**2/x,
        variable=x,
        num_steps=17,
        integral=(((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) + ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))) + (Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) + (Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) + (Integer(-1) * (sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))) + (Integer(-1) * (Integer(2) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1)))))) + (Integer(-1) * (Integer(2) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(3), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**2/x**2,
        variable=x,
        num_steps=12,
        integral=((Integer(-1) * ((Symbol('b') * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * (Symbol('a'))**(Integer(-1)))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * (x)**(Integer(-1)))) + ((Integer(2) * Symbol('b') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * Symbol('b') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + ((Integer(2) * Symbol('b') * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * Symbol('b') * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**2/x**3,
        variable=x,
        num_steps=23,
        integral=((((Symbol('b'))**(Integer(2)) * sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * sympy.asech((Symbol('a') + (Symbol('b') * x)))) * ((Symbol('a') * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))) * (Symbol('a') + (Symbol('b') * x)) * (Integer(1) + (Integer(-1) * (Symbol('a') * ((Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * (Symbol('a'))**(Integer(2))))**(Integer(-1))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * ((Integer(2) * (x)**(Integer(2))))**(Integer(-1)))) + (((Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(2) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.log((x * ((Symbol('a') + (Symbol('b') * x)))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Integer(2) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(2) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*asech(a + b*x)**3,
        variable=x,
        num_steps=16,
        integral=((Integer(-1) * ((Integer(3) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * (((Symbol('a'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * (x)**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3))) + ((Integer(6) * Symbol('a') * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((Integer(3) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * sympy.I * Symbol('a') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1)))) + ((Integer(6) * sympy.I * Symbol('a') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + ((Integer(3) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1))) + ((Integer(6) * sympy.I * Symbol('a') * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * sympy.I * Symbol('a') * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Symbol('b'))**(Integer(2)))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**3,
        variable=x,
        num_steps=10,
        integral=((((Symbol('a') + (Symbol('b') * x)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.atan((sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x)))))) * (Symbol('b'))**(Integer(-1)))) + ((Integer(6) * sympy.I * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * sympy.I * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1)))) + (Integer(-1) * ((Integer(6) * sympy.I * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1)))) + ((Integer(6) * sympy.I * sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * (Symbol('b'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**3/x,
        variable=x,
        num_steps=20,
        integral=(((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) + ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))) + (Integer(3) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) + (Integer(3) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) + (Integer(-1) * ((Integer(3) * (Integer(2))**(Integer(-1))) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))))) + (Integer(-1) * (Integer(6) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1)))))) + (Integer(-1) * (Integer(6) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))))) + ((Integer(3) * (Integer(2))**(Integer(-1))) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(3), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))) + (Integer(6) * sympy.Function('PolyLog')(Integer(4), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) + (Integer(6) * sympy.Function('PolyLog')(Integer(4), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) + (Integer(-1) * ((Integer(3) * (Integer(4))**(Integer(-1))) * sympy.Function('PolyLog')(Integer(4), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**3/x**2,
        variable=x,
        num_steps=14,
        integral=((Integer(-1) * ((Symbol('b') * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3))) * (Symbol('a'))**(Integer(-1)))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * (x)**(Integer(-1)))) + ((Integer(3) * Symbol('b') * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * Symbol('b') * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + ((Integer(6) * Symbol('b') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * Symbol('b') * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + (Integer(-1) * ((Integer(6) * Symbol('b') * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + ((Integer(6) * Symbol('b') * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * ((Symbol('a') * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)**3/x**3,
        variable=x,
        num_steps=32,
        integral=((Integer(-1) * ((Integer(3) * (Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * (Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1)))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.sqrt(((Integer(1) + (Integer(-1) * Symbol('a')) + (Integer(-1) * (Symbol('b') * x))) * ((Integer(1) + Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))) * (Integer(1) + Symbol('a') + (Symbol('b') * x)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2))) * ((Integer(2) * Symbol('a') * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))) * (Symbol('a') + (Symbol('b') * x)) * (Integer(1) + (Integer(-1) * (Symbol('a') * ((Symbol('a') + (Symbol('b') * x)))**(Integer(-1)))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3))) * ((Integer(2) * (Symbol('a'))**(Integer(2))))**(Integer(-1))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(3)) * ((Integer(2) * (x)**(Integer(2))))**(Integer(-1)))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * ((Integer(2) * (Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * (Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * (Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * ((Integer(2) * (Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * (sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * sympy.log((Integer(1) + (Integer(-1) * ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1)))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * (Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(6) * (Symbol('b'))**(Integer(2)) * sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.Function('PolyLog')(Integer(2), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(6) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2))))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))) + ((Integer(3) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * ((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Integer(6) * (Symbol('b'))**(Integer(2)) * sympy.Function('PolyLog')(Integer(3), ((Symbol('a') * (sympy.E)**(sympy.asech((Symbol('a') + (Symbol('b') * x))))) * ((Integer(1) + sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))) * (((Symbol('a'))**(Integer(2)) * sympy.sqrt((Integer(1) + (Integer(-1) * (Symbol('a'))**(Integer(2)))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**3*asech(sqrt(x)),
        variable=x,
        num_steps=4,
        integral=x**4*asech(sqrt(x))/4 + (1 - x)**4/(28*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) - 3*(1 - x)**3/(20*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (1 - x)**2/(4*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) - (1 - x)/(4*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*asech(sqrt(x)),
        variable=x,
        num_steps=4,
        integral=x**3*asech(sqrt(x))/3 - (1 - x)**3/(15*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + 2*(1 - x)**2/(9*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) - (1 - x)/(3*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=x*asech(sqrt(x)),
        variable=x,
        num_steps=4,
        integral=x**2*asech(sqrt(x))/2 + (1 - x)**2/(6*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) - (1 - x)/(2*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=asech(sqrt(x)),
        variable=x,
        num_steps=3,
        integral=x*asech(sqrt(x)) - (1 - x)/(sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=asech(sqrt(x))/x,
        variable=x,
        num_steps=7,
        integral=((sympy.asech(sympy.sqrt(x)))**(Integer(2)) + (Integer(-1) * (Integer(2) * sympy.asech(sympy.sqrt(x)) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech(sympy.sqrt(x)))))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech(sympy.sqrt(x)))))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(sqrt(x))/x**2,
        variable=x,
        num_steps=5,
        integral=-asech(sqrt(x))/x + sqrt(1 - x)*atanh(sqrt(1 - x))/(2*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (1 - x)/(2*x**(sympy.S(3)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=asech(sqrt(x))/x**3,
        variable=x,
        num_steps=6,
        integral=-asech(sqrt(x))/(2*x**2) + 3*sqrt(1 - x)*atanh(sqrt(1 - x))/(16*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (3 - 3*x)/(16*x**(sympy.S(3)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (1 - x)/(8*x**(sympy.S(5)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=asech(sqrt(x))/x**4,
        variable=x,
        num_steps=7,
        integral=-asech(sqrt(x))/(3*x**3) + 5*sqrt(1 - x)*atanh(sqrt(1 - x))/(48*sqrt(x)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (5 - 5*x)/(48*x**(sympy.S(3)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (5 - 5*x)/(72*x**(sympy.S(5)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))) + (1 - x)/(18*x**(sympy.S(7)/2)*sqrt(-1 + 1/sqrt(x))*sqrt(1 + 1/sqrt(x))),
    ),
    RubiTestSuiteCase(
        integrand=asech(1/x),
        variable=x,
        num_steps=3,
        integral=x*acosh(x) - sqrt(x - 1)*sqrt(x + 1),
    ),
    RubiTestSuiteCase(
        integrand=asech(a*x**n)/x,
        variable=x,
        num_steps=7,
        integral=(((sympy.asech((Symbol('a') * (x)**(Symbol('n')))))**(Integer(2)) * ((Integer(2) * Symbol('n')))**(Integer(-1))) + (Integer(-1) * ((sympy.asech((Symbol('a') * (x)**(Symbol('n')))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') * (x)**(Symbol('n'))))))))) * (Symbol('n'))**(Integer(-1)))) + (Integer(-1) * (sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') * (x)**(Symbol('n')))))))) * ((Integer(2) * Symbol('n')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(a*x**5)/x,
        variable=x,
        num_steps=7,
        integral=(((Integer(10))**(Integer(-1)) * (sympy.asech((Symbol('a') * (x)**(Integer(5)))))**(Integer(2))) + (Integer(-1) * ((Integer(5))**(Integer(-1)) * sympy.asech((Symbol('a') * (x)**(Integer(5)))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') * (x)**(Integer(5)))))))))) + (Integer(-1) * ((Integer(10))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') * (x)**(Integer(5))))))))))),
    ),
    RubiTestSuiteCase(
        integrand=asech(c*exp(a + b*x)),
        variable=x,
        num_steps=7,
        integral=(((sympy.asech((Symbol('c') * (sympy.E)**((Symbol('a') + (Symbol('b') * x))))))**(Integer(2)) * ((Integer(2) * Symbol('b')))**(Integer(-1))) + (Integer(-1) * ((sympy.asech((Symbol('c') * (sympy.E)**((Symbol('a') + (Symbol('b') * x))))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('c') * (sympy.E)**((Symbol('a') + (Symbol('b') * x)))))))))) * (Symbol('b'))**(Integer(-1)))) + (Integer(-1) * (sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('c') * (sympy.E)**((Symbol('a') + (Symbol('b') * x))))))))) * ((Integer(2) * Symbol('b')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**3*exp(asech(a*x)),
        variable=x,
        num_steps=5,
        integral=x**4*exp(asech(a*x))/4 + x**3/(12*a) - x*sqrt(-a*x + 1)/(8*a**3*sqrt(1/(a*x + 1))) + sqrt(a*x + 1)*sqrt(1/(a*x + 1))*asin(a*x)/(8*a**4),
    ),
    RubiTestSuiteCase(
        integrand=x*exp(asech(a*x)),
        variable=x,
        num_steps=4,
        integral=x**2*exp(asech(a*x))/2 + x/(2*a) + sqrt(a*x + 1)*sqrt(1/(a*x + 1))*asin(a*x)/(2*a**2),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x))/x**4,
        variable=x,
        num_steps=8,
        integral=a**3*sqrt(a*x + 1)*sqrt(1/(a*x + 1))*atanh(sqrt(-a*x + 1)*sqrt(a*x + 1))/8 + a*sqrt(-a*x + 1)/(8*x**2*sqrt(1/(a*x + 1))) - exp(asech(a*x))/(3*x**3) + sqrt(-a*x + 1)/(12*a*x**4*sqrt(1/(a*x + 1))) + 1/(12*a*x**4),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x))/x**5,
        variable=x,
        num_steps=7,
        integral=2*a**3*sqrt(-a*x + 1)/(15*x*sqrt(1/(a*x + 1))) + a*sqrt(-a*x + 1)/(15*x**3*sqrt(1/(a*x + 1))) - exp(asech(a*x))/(4*x**4) + sqrt(-a*x + 1)/(20*a*x**5*sqrt(1/(a*x + 1))) + 1/(20*a*x**5),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x))/x**6,
        variable=x,
        num_steps=10,
        integral=a**5*sqrt(a*x + 1)*sqrt(1/(a*x + 1))*atanh(sqrt(-a*x + 1)*sqrt(a*x + 1))/16 + a**3*sqrt(-a*x + 1)/(16*x**2*sqrt(1/(a*x + 1))) + a*sqrt(-a*x + 1)/(24*x**4*sqrt(1/(a*x + 1))) - exp(asech(a*x))/(5*x**5) + sqrt(-a*x + 1)/(30*a*x**6*sqrt(1/(a*x + 1))) + 1/(30*a*x**6),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x))/x**7,
        variable=x,
        num_steps=9,
        integral=8*a**5*sqrt(-a*x + 1)/(105*x*sqrt(1/(a*x + 1))) + 4*a**3*sqrt(-a*x + 1)/(105*x**3*sqrt(1/(a*x + 1))) + a*sqrt(-a*x + 1)/(35*x**5*sqrt(1/(a*x + 1))) - exp(asech(a*x))/(6*x**6) + sqrt(-a*x + 1)/(42*a*x**7*sqrt(1/(a*x + 1))) + 1/(42*a*x**7),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x))/x**8,
        variable=x,
        num_steps=12,
        integral=5*a**7*sqrt(a*x + 1)*sqrt(1/(a*x + 1))*atanh(sqrt(-a*x + 1)*sqrt(a*x + 1))/128 + 5*a**5*sqrt(-a*x + 1)/(128*x**2*sqrt(1/(a*x + 1))) + 5*a**3*sqrt(-a*x + 1)/(192*x**4*sqrt(1/(a*x + 1))) + a*sqrt(-a*x + 1)/(48*x**6*sqrt(1/(a*x + 1))) - exp(asech(a*x))/(7*x**7) + sqrt(-a*x + 1)/(56*a*x**8*sqrt(1/(a*x + 1))) + 1/(56*a*x**8),
    ),
    RubiTestSuiteCase(
        integrand=x**7*exp(asech(a*x**2)),
        variable=x,
        num_steps=6,
        integral=x**8*exp(asech(a*x**2))/8 + x**6/(24*a) - x**2*sqrt(a*x**2 + 1)*sqrt(-a**2*x**4 + 1)*sqrt(1/(a*x**2 + 1))/(16*a**3) + sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*asin(a*x**2)/(16*a**4),
    ),
    RubiTestSuiteCase(
        integrand=x**6*exp(asech(a*x**2)),
        variable=x,
        num_steps=5,
        integral=x**7*exp(asech(a*x**2))/7 + 2*x**5/(35*a) - 2*x*sqrt(a*x**2 + 1)*sqrt(-a**2*x**4 + 1)*sqrt(1/(a*x**2 + 1))/(21*a**3) + 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_f(asin(sqrt(a)*x), -1)/(21*a**(sympy.S(7)/2)),
    ),
    RubiTestSuiteCase(
        integrand=x**4*exp(asech(a*x**2)),
        variable=x,
        num_steps=7,
        integral=x**5*exp(asech(a*x**2))/5 + 2*x**3/(15*a) + 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_e(asin(sqrt(a)*x), -1)/(5*a**(sympy.S(5)/2)) - 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_f(asin(sqrt(a)*x), -1)/(5*a**(sympy.S(5)/2)),
    ),
    RubiTestSuiteCase(
        integrand=x**3*exp(asech(a*x**2)),
        variable=x,
        num_steps=5,
        integral=x**4*exp(asech(a*x**2))/4 + x**2/(4*a) + sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*asin(a*x**2)/(4*a**2),
    ),
    RubiTestSuiteCase(
        integrand=x**2*exp(asech(a*x**2)),
        variable=x,
        num_steps=4,
        integral=x**3*exp(asech(a*x**2))/3 + 2*x/(3*a) + 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_f(asin(sqrt(a)*x), -1)/(3*a**(sympy.S(3)/2)),
    ),
    RubiTestSuiteCase(
        integrand=x*exp(asech(a*x**2)),
        variable=x,
        num_steps=6,
        integral=x**2*exp(asech(a*x**2))/2 - sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*atanh(sqrt(-a**2*x**4 + 1))/(2*a) + log(x)/a,
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x**2)),
        variable=x,
        num_steps=8,
        integral=x*exp(asech(a*x**2)) - 2*sqrt(a*x**2 + 1)*sqrt(-a**2*x**4 + 1)*sqrt(1/(a*x**2 + 1))/(a*x) - 2/(a*x) - 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_e(asin(sqrt(a)*x), -1)/sqrt(a) + 2*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_f(asin(sqrt(a)*x), -1)/sqrt(a),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x**2))/x**2,
        variable=x,
        num_steps=5,
        integral=-2*sqrt(a)*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*elliptic_f(asin(sqrt(a)*x), -1)/3 - exp(asech(a*x**2))/x + 2*sqrt(a*x**2 + 1)*sqrt(-a**2*x**4 + 1)*sqrt(1/(a*x**2 + 1))/(3*a*x**3) + 2/(3*a*x**3),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x**2))/x**3,
        variable=x,
        num_steps=7,
        integral=a*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*atanh(sqrt(-a**2*x**4 + 1))/4 - exp(asech(a*x**2))/(2*x**2) + sqrt(a*x**2 + 1)*sqrt(-a**2*x**4 + 1)*sqrt(1/(a*x**2 + 1))/(4*a*x**4) + 1/(4*a*x**4),
    ),
    RubiTestSuiteCase(
        integrand=x**m*exp(asech(a*x**3)),
        variable=x,
        num_steps=4,
        integral=x**(m + 1)*exp(asech(a*x**3))/(m + 1) - 3*x**(m - 2)*sqrt(a*x**3 + 1)*sqrt(1/(a*x**3 + 1))*hyper((sympy.S.Half, m/6 + sympy.S(-1)/3), (m/6 + sympy.S(2)/3,), a**2*x**6)/(a*(-m**2 + m + 2)) - 3*x**(m - 2)/(a*(-m**2 + m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=x**m*exp(asech(a*x**2)),
        variable=x,
        num_steps=4,
        integral=x**(m + 1)*exp(asech(a*x**2))/(m + 1) - 2*x**(m - 1)*sqrt(a*x**2 + 1)*sqrt(1/(a*x**2 + 1))*hyper((sympy.S.Half, m/4 + sympy.S(-1)/4), (m/4 + sympy.S(3)/4,), a**2*x**4)/(a*(1 - m**2)) - 2*x**(m - 1)/(a*(1 - m**2)),
    ),
    RubiTestSuiteCase(
        integrand=x**m*exp(asech(a*x)),
        variable=x,
        num_steps=4,
        integral=x**(m + 1)*exp(asech(a*x))/(m + 1) + x**m*sqrt(a*x + 1)*sqrt(1/(a*x + 1))*hyper((sympy.S.Half, m/2), (m/2 + 1,), a**2*x**2)/(a*m*(m + 1)) + x**m/(a*m*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=x**m*exp(asech(a/x)),
        variable=x,
        num_steps=5,
        integral=x**(m + 1)*exp(asech(a/x))/(m + 1) - x**(m + 2)*sqrt(a/x + 1)*sqrt(1/(a/x + 1))*hyper((sympy.S.Half, -m/2 - 1), (-m/2,), a**2/x**2)/(a*(m**2 + 3*m + 2)) - x**(m + 2)/(a*(m**2 + 3*m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=x**m*exp(asech(a*x**p)),
        variable=x,
        num_steps=4,
        integral=x**(m + 1)*exp(asech(a*x**p))/(m + 1) + p*x**(m - p + 1)*sqrt(a*x**p + 1)*sqrt(1/(a*x**p + 1))*hyper((sympy.S.Half, (m - p + 1)/(2*p)), ((m + p + 1)/(2*p),), a**2*x**(2*p))/(a*(m + 1)*(m - p + 1)) + p*x**(m - p + 1)/(a*(m + 1)*(m - p + 1)),
    ),
    RubiTestSuiteCase(
        integrand=x*exp(asech(a*x**p)),
        variable=x,
        num_steps=4,
        integral=x**2*exp(asech(a*x**p))/2 + p*x**(2 - p)*sqrt(a*x**p + 1)*sqrt(1/(a*x**p + 1))*hyper((sympy.S.Half, sympy.S(-1)/2 + 1/p), (sympy.S.Half + 1/p,), a**2*x**(2*p))/(2*a*(2 - p)) + p*x**(2 - p)/(2*a*(2 - p)),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x**p)),
        variable=x,
        num_steps=4,
        integral=x*exp(asech(a*x**p)) + p*x**(1 - p)*sqrt(a*x**p + 1)*sqrt(1/(a*x**p + 1))*hyper((sympy.S.Half, sympy.S(-1)/2 + 1/(2*p)), ((p + 1)/(2*p),), a**2*x**(2*p))/(a*(1 - p)) + p*x**(1 - p)/(a*(1 - p)),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(a*x**p))/x**2,
        variable=x,
        num_steps=4,
        integral=-exp(asech(a*x**p))/x + p*x**(-p - 1)*sqrt(a*x**p + 1)*sqrt(1/(a*x**p + 1))*hyper((sympy.S.Half, -(p + 1)/(2*p)), (-(1 - p)/(2*p),), a**2*x**(2*p))/(a*(p + 1)) + p*x**(-p - 1)/(a*(p + 1)),
    ),
    RubiTestSuiteCase(
        integrand=x**4*exp(2*asech(a*x)),
        variable=x,
        num_steps=9,
        integral=sqrt((-a*x + 1)/(a*x + 1))*(5 - 6*sqrt((-a*x + 1)/(a*x + 1)))*(a*x + 1)**4/(10*a**5) + 5*sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)**2/(4*a**5) + (4 - sqrt((-a*x + 1)/(a*x + 1)))*(a*x + 1)/(4*a**5) + (-a*x + 1)*(a*x + 1)**4/(5*a**5) - (a*x + 1)**3*(45*sqrt((-a*x + 1)/(a*x + 1)) + 4)/(30*a**5) - atan(sqrt((-a*x + 1)/(a*x + 1)))/(2*a**5),
    ),
    RubiTestSuiteCase(
        integrand=x**3*exp(2*asech(a*x)),
        variable=x,
        num_steps=8,
        integral=-x/a**3 + sqrt((-a*x + 1)/(a*x + 1))*(4 - 3*sqrt((-a*x + 1)/(a*x + 1)))*(a*x + 1)**3/(6*a**4) + (3 - 8*sqrt((-a*x + 1)/(a*x + 1)))*(a*x + 1)**2/(6*a**4) + (-a*x + 1)*(a*x + 1)**3/(4*a**4),
    ),
    RubiTestSuiteCase(
        integrand=x**2*exp(2*asech(a*x)),
        variable=x,
        num_steps=7,
        integral=-sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)**2*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3/(6*a**3) + (1 - sqrt((-a*x + 1)/(a*x + 1)))*(a*x + 1)*(sqrt((-a*x + 1)/(a*x + 1)) + 1)/(2*a**3) + (a*x + 1)**3*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**4/(12*a**3) - 2*atan(sqrt((-a*x + 1)/(a*x + 1)))/a**3,
    ),
    RubiTestSuiteCase(
        integrand=x*exp(2*asech(a*x)),
        variable=x,
        num_steps=8,
        integral=-(a*x + 1)**2/(2*a**2) + (a*x + 1)*(2*sqrt((-a*x + 1)/(a*x + 1)) + 1)/a**2 + 4*log(1 - sqrt((-a*x + 1)/(a*x + 1)))/a**2 + 2*log(a*x + 1)/a**2,
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x)),
        variable=x,
        num_steps=7,
        integral=-x + 4*atan(sqrt((-a*x + 1)/(a*x + 1)))/a - 4/(a*(1 - sqrt((-a*x + 1)/(a*x + 1)))),
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x,
        variable=x,
        num_steps=5,
        integral=-2*log(1 - sqrt((-a*x + 1)/(a*x + 1))) - log(a*x + 1) + 2/(1 - sqrt((-a*x + 1)/(a*x + 1))) - 2/(1 - sqrt((-a*x + 1)/(a*x + 1)))**2,
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x**2,
        variable=x,
        num_steps=4,
        integral=2*a/(1 - sqrt((-a*x + 1)/(a*x + 1)))**2 - 4*a/(3*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3),
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x**3,
        variable=x,
        num_steps=5,
        integral=a**2*atanh(sqrt((-a*x + 1)/(a*x + 1)))/2 + a**2/(2 - 2*sqrt((-a*x + 1)/(a*x + 1))) - 3*a**2/(2*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) + 2*a**2/(1 - sqrt((-a*x + 1)/(a*x + 1)))**3 - a**2/(1 - sqrt((-a*x + 1)/(a*x + 1)))**4,
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x**4,
        variable=x,
        num_steps=4,
        integral=-a**3/(4*sqrt((-a*x + 1)/(a*x + 1)) + 4) - a**3/(4 - 4*sqrt((-a*x + 1)/(a*x + 1))) + 3*a**3/(2*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) - 7*a**3/(3*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3) + 2*a**3/(1 - sqrt((-a*x + 1)/(a*x + 1)))**4 - 4*a**3/(5*(1 - sqrt((-a*x + 1)/(a*x + 1)))**5),
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x**5,
        variable=x,
        num_steps=5,
        integral=a**4*atanh(sqrt((-a*x + 1)/(a*x + 1)))/4 + a**4/(8*sqrt((-a*x + 1)/(a*x + 1)) + 8) - a**4/(8*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2) + 3*a**4/(8 - 8*sqrt((-a*x + 1)/(a*x + 1))) - 11*a**4/(8*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) + 8*a**4/(3*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3) - 3*a**4/(1 - sqrt((-a*x + 1)/(a*x + 1)))**4 + 2*a**4/(1 - sqrt((-a*x + 1)/(a*x + 1)))**5 - 2*a**4/(3*(1 - sqrt((-a*x + 1)/(a*x + 1)))**6),
    ),
    RubiTestSuiteCase(
        integrand=exp(2*asech(a*x))/x**6,
        variable=x,
        num_steps=4,
        integral=-a**5/(4*sqrt((-a*x + 1)/(a*x + 1)) + 4) + a**5/(8*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2) - a**5/(12*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3) - a**5/(4 - 4*sqrt((-a*x + 1)/(a*x + 1))) + 11*a**5/(8*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) - 35*a**5/(12*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3) + 4*a**5/(1 - sqrt((-a*x + 1)/(a*x + 1)))**4 - 18*a**5/(5*(1 - sqrt((-a*x + 1)/(a*x + 1)))**5) + 2*a**5/(1 - sqrt((-a*x + 1)/(a*x + 1)))**6 - 4*a**5/(7*(1 - sqrt((-a*x + 1)/(a*x + 1)))**7),
    ),
    RubiTestSuiteCase(
        integrand=x**4*exp(-asech(a*x)),
        variable=x,
        num_steps=8,
        integral=-x/a**4 - sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)**5/(5*a**5) + (a*x + 1)**4*(16*sqrt((-a*x + 1)/(a*x + 1)) + 5)/(20*a**5) - (a*x + 1)**3*(17*sqrt((-a*x + 1)/(a*x + 1)) + 15)/(15*a**5) + (a*x + 1)**2*(4*sqrt((-a*x + 1)/(a*x + 1)) + 9)/(6*a**5),
    ),
    RubiTestSuiteCase(
        integrand=x**3*exp(-asech(a*x)),
        variable=x,
        num_steps=7,
        integral=-sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)**4/(4*a**4) + (a*x + 1)**3*(9*sqrt((-a*x + 1)/(a*x + 1)) + 4)/(12*a**4) - (a*x + 1)**2*(5*sqrt((-a*x + 1)/(a*x + 1)) + 8)/(8*a**4) + (a*x + 1)*(sqrt((-a*x + 1)/(a*x + 1)) + 8)/(8*a**4) + atan(sqrt((-a*x + 1)/(a*x + 1)))/(4*a**4),
    ),
    RubiTestSuiteCase(
        integrand=x**2*exp(-asech(a*x)),
        variable=x,
        num_steps=6,
        integral=-x/a**2 - sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)**3/(3*a**3) + (a*x + 1)**2*(4*sqrt((-a*x + 1)/(a*x + 1)) + 3)/(6*a**3),
    ),
    RubiTestSuiteCase(
        integrand=x*exp(-asech(a*x)),
        variable=x,
        num_steps=5,
        integral=(1 - sqrt((-a*x + 1)/(a*x + 1)))**2*(a*x + 1)**2/(4*a**2) + (a*x + 1)*(sqrt((-a*x + 1)/(a*x + 1)) + 1)/(2*a**2) + atan(sqrt((-a*x + 1)/(a*x + 1)))/a**2,
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x)),
        variable=x,
        num_steps=6,
        integral=-sqrt((-a*x + 1)/(a*x + 1))*(a*x + 1)/a + log(a*x + 1)/a + 2*log(sqrt((-a*x + 1)/(a*x + 1)) + 1)/a,
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x,
        variable=x,
        num_steps=5,
        integral=-2*atan(sqrt((-a*x + 1)/(a*x + 1))) - 2/(sqrt((-a*x + 1)/(a*x + 1)) + 1),
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**2,
        variable=x,
        num_steps=5,
        integral=-a*atanh(sqrt((-a*x + 1)/(a*x + 1))) + a/(sqrt((-a*x + 1)/(a*x + 1)) + 1) - a/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2,
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**3,
        variable=x,
        num_steps=4,
        integral=-a**2/(2*sqrt((-a*x + 1)/(a*x + 1)) + 2) + a**2/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2 - 2*a**2/(3*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3) - a**2/(2 - 2*sqrt((-a*x + 1)/(a*x + 1))),
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**4,
        variable=x,
        num_steps=5,
        integral=-a**3*atanh(sqrt((-a*x + 1)/(a*x + 1)))/4 + a**3/(2*sqrt((-a*x + 1)/(a*x + 1)) + 2) - a**3/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2 + a**3/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3 - a**3/(2*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**4) + a**3/(4 - 4*sqrt((-a*x + 1)/(a*x + 1))) - a**3/(4*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2),
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**5,
        variable=x,
        num_steps=4,
        integral=-3*a**4/(8*sqrt((-a*x + 1)/(a*x + 1)) + 8) + a**4/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2 - 4*a**4/(3*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3) + a**4/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**4 - 2*a**4/(5*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**5) - 3*a**4/(8 - 8*sqrt((-a*x + 1)/(a*x + 1))) + a**4/(4*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) - a**4/(6*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3),
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**6,
        variable=x,
        num_steps=5,
        integral=-a**5*atanh(sqrt((-a*x + 1)/(a*x + 1)))/8 + 3*a**5/(8*sqrt((-a*x + 1)/(a*x + 1)) + 8) - a**5/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2 + 19*a**5/(12*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3) - 13*a**5/(8*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**4) + a**5/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**5 - a**5/(3*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**6) + a**5/(4 - 4*sqrt((-a*x + 1)/(a*x + 1))) - 3*a**5/(8*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) + a**5/(4*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3) - a**5/(8*(1 - sqrt((-a*x + 1)/(a*x + 1)))**4),
    ),
    RubiTestSuiteCase(
        integrand=exp(-asech(a*x))/x**7,
        variable=x,
        num_steps=4,
        integral=-5*a**6/(16*sqrt((-a*x + 1)/(a*x + 1)) + 16) + a**6/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**2 - 11*a**6/(6*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**3) + 9*a**6/(4*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**4) - 19*a**6/(10*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**5) + a**6/(sqrt((-a*x + 1)/(a*x + 1)) + 1)**6 - 2*a**6/(7*(sqrt((-a*x + 1)/(a*x + 1)) + 1)**7) - 5*a**6/(16 - 16*sqrt((-a*x + 1)/(a*x + 1))) + 3*a**6/(8*(1 - sqrt((-a*x + 1)/(a*x + 1)))**2) - 5*a**6/(12*(1 - sqrt((-a*x + 1)/(a*x + 1)))**3) + a**6/(4*(1 - sqrt((-a*x + 1)/(a*x + 1)))**4) - a**6/(10*(1 - sqrt((-a*x + 1)/(a*x + 1)))**5),
    ),
    RubiTestSuiteCase(
        integrand=(d*x)**m*exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=5,
        integral=(d*x)**m*sqrt(c*x + 1)*sqrt(1/(c*x + 1))*hyper((sympy.S.Half, m/2), (m/2 + 1,), c**2*x**2)/(c*m) + (d*x)**m*hyper((1, m/2), (m/2 + 1,), c**2*x**2)/(c*m),
    ),
    RubiTestSuiteCase(
        integrand=x**4*exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=8,
        integral=-x**2*sqrt(-c*x + 1)/(3*c**3*sqrt(1/(c*x + 1))) - x**2/(2*c**3) - 2*sqrt(-c*x + 1)/(3*c**5*sqrt(1/(c*x + 1))) - log(-c**2*x**2 + 1)/(2*c**5),
    ),
    RubiTestSuiteCase(
        integrand=x**3*exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=7,
        integral=-x*sqrt(-c*x + 1)/(2*c**3*sqrt(1/(c*x + 1))) - x/c**3 + sqrt(c*x + 1)*sqrt(1/(c*x + 1))*asin(c*x)/(2*c**4) + atanh(c*x)/c**4,
    ),
    RubiTestSuiteCase(
        integrand=x**2*exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=4,
        integral=-sqrt(-c*x + 1)/(c**3*sqrt(1/(c*x + 1))) - log(-c**2*x**2 + 1)/(2*c**3),
    ),
    RubiTestSuiteCase(
        integrand=x*exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=5,
        integral=sqrt(c*x + 1)*sqrt(1/(c*x + 1))*asin(c*x)/c**2 + atanh(c*x)/c**2,
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(c*x))/(-c**2*x**2 + 1),
        variable=x,
        num_steps=8,
        integral=-sqrt(c*x + 1)*sqrt(1/(c*x + 1))*atanh(sqrt(-c*x + 1)*sqrt(c*x + 1))/c + log(x)/c - log(-c**2*x**2 + 1)/(2*c),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(c*x))/(x*(-c**2*x**2 + 1)),
        variable=x,
        num_steps=5,
        integral=atanh(c*x) - sqrt(-c*x + 1)/(c*x*sqrt(1/(c*x + 1))) - 1/(c*x),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(c*x))/(x**2*(-c**2*x**2 + 1)),
        variable=x,
        num_steps=9,
        integral=-c*sqrt(c*x + 1)*sqrt(1/(c*x + 1))*atanh(sqrt(-c*x + 1)*sqrt(c*x + 1))/2 + c*log(x) - c*log(-c**2*x**2 + 1)/2 - sqrt(-c*x + 1)/(2*c*x**2*sqrt(1/(c*x + 1))) - 1/(2*c*x**2),
    ),
    RubiTestSuiteCase(
        integrand=exp(asech(c*x))/(x**3*(-c**2*x**2 + 1)),
        variable=x,
        num_steps=8,
        integral=c**2*atanh(c*x) - 2*c*sqrt(-c*x + 1)/(3*x*sqrt(1/(c*x + 1))) - c/x - sqrt(-c*x + 1)/(3*c*x**3*sqrt(1/(c*x + 1))) - 1/(3*c*x**3),
    ),
    RubiTestSuiteCase(
        integrand=asech(a + b*x)/(a*d/b + d*x),
        variable=x,
        num_steps=8,
        integral=(((sympy.asech((Symbol('a') + (Symbol('b') * x))))**(Integer(2)) * ((Integer(2) * Symbol('d')))**(Integer(-1))) + (Integer(-1) * ((sympy.asech((Symbol('a') + (Symbol('b') * x))) * sympy.log((Integer(1) + (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x)))))))) * (Symbol('d'))**(Integer(-1)))) + (Integer(-1) * (sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**((Integer(2) * sympy.asech((Symbol('a') + (Symbol('b') * x))))))) * ((Integer(2) * Symbol('d')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**3*asech(a + b*x**4),
        variable=x,
        num_steps=5,
        integral=(a + b*x**4)*asech(a + b*x**4)/(4*b) - atan(sqrt((-a - b*x**4 + 1)/(a + b*x**4 + 1)))/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=x**(n - 1)*asech(a + b*x**n),
        variable=x,
        num_steps=5,
        integral=(a + b*x**n)*asech(a + b*x**n)/(b*n) - 2*atan(sqrt((-a - b*x**n + 1)/(a + b*x**n + 1)))/(b*n),
    ),
]
