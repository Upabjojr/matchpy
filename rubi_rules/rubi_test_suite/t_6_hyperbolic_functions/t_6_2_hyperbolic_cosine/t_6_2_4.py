# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.4 (d+e x)^m cosh(a+b x+c x^2)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.4 (d+e x)^m cosh(a+b x+c x^2)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e = symbols('a b c d e')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x + c*x**2),
        variable=x,
        num_steps=12,
        integral=((((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + ((x * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x + c*x**2),
        variable=x,
        num_steps=6,
        integral=((Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2),
        variable=x,
        num_steps=5,
        integral=((((sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1))) + (((sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.cosh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=-b*sinh(a + b*x + c*x**2)/x + cosh(a + b*x + c*x**2)/x**2,
        variable=x,
        num_steps=7,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1)))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('c')) * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('c')) * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x - c*x**2),
        variable=x,
        num_steps=12,
        integral=((Integer(-1) * (((Symbol('b'))**(Integer(2)) * (sympy.E)**((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(-1) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (((sympy.E)**(((Integer(-1) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2))))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((x * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2))))))) * ((Integer(2) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x - c*x**2),
        variable=x,
        num_steps=6,
        integral=((Integer(-1) * ((Symbol('b') * (sympy.E)**((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(-1) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x - c*x**2),
        variable=x,
        num_steps=5,
        integral=((Integer(-1) * (((sympy.E)**((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**(((Integer(-1) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x - c*x**2)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.cosh((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=-b*sinh(a + b*x - c*x**2)/x + cosh(a + b*x - c*x**2)/x**2,
        variable=x,
        num_steps=7,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('c')) * (sympy.E)**((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('c')) * (sympy.E)**(((Integer(-1) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=12,
        integral=(((Integer(-1) * (Integer(3) * (Integer(16))**(Integer(-1)))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Integer(2))**(Integer(-1)) * (Integer(-1) + (Integer(-1) * (Integer(2) * x)))))) + (Integer(-1) * ((Integer(16))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Integer(2))**(Integer(-1)) * (Integer(1) + (Integer(2) * x)))))) + (Integer(-1) * ((Integer(4))**(Integer(-1)) * sympy.sinh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))))) + ((Integer(2))**(Integer(-1)) * x * sympy.sinh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=6,
        integral=(((Integer(8))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Integer(2))**(Integer(-1)) * (Integer(-1) + (Integer(-1) * (Integer(2) * x)))))) + (Integer(-1) * ((Integer(8))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Integer(2))**(Integer(-1)) * (Integer(1) + (Integer(2) * x)))))) + ((Integer(2))**(Integer(-1)) * sympy.sinh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=5,
        integral=(((Integer(-1) * (Integer(4))**(Integer(-1))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Integer(2))**(Integer(-1)) * (Integer(-1) + (Integer(-1) * (Integer(2) * x)))))) + ((Integer(4))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Integer(2))**(Integer(-1)) * (Integer(1) + (Integer(2) * x)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**2 + x + sympy.S(1)/4)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.cosh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**2 + x + sympy.S(1)/4)/x**2,
        variable=x,
        num_steps=6,
        integral=((Integer(-1) * (sympy.cosh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Integer(2))**(Integer(-1)) * (Integer(-1) + (Integer(-1) * (Integer(2) * x)))))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Integer(2))**(Integer(-1)) * (Integer(1) + (Integer(2) * x))))) + sympy.Function('Unintegrable')((sympy.sinh(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1))), x)),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=14,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + ((x * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=8,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=7,
        integral=((x * (Integer(2))**(Integer(-1))) + (((sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * sympy.sqrt(Symbol('c'))))**(Integer(-1))) + (((sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(2))**(Integer(-1)) * sympy.Function('Unintegrable')((sympy.cosh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=14,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * (sympy.E)**(((Integer(-2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (((sympy.E)**(((Integer(-2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2))))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((x * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2))))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=8,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * (sympy.E)**(((Integer(-2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=7,
        integral=((x * (Integer(2))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**(((Integer(-2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x - c*x**2)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(2))**(Integer(-1)) * sympy.Function('Unintegrable')((sympy.cosh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=14,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + ((Integer(16))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(Integer(2)))**(Integer(-1))))) + (Integer(-1) * ((Integer(16))**(Integer(-1)) * sympy.sinh(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))))) + ((Integer(8))**(Integer(-1)) * x * sympy.sinh(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=8,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + (Integer(-1) * ((Integer(16))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(Integer(2)))**(Integer(-1)))))) + (Integer(-1) * ((Integer(16))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(Integer(2)))**(Integer(-1)))))) + ((Integer(8))**(Integer(-1)) * sympy.sinh(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=7,
        integral=((x * (Integer(2))**(Integer(-1))) + ((Integer(8))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(Integer(2)))**(Integer(-1))))) + ((Integer(8))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(Integer(2)))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**2 + x + sympy.S(1)/4)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(2))**(Integer(-1)) * sympy.Function('Unintegrable')((sympy.cosh(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)**2*cosh(a + b*x + c*x**2),
        variable=x,
        num_steps=12,
        integral=((((Symbol('e'))**(Integer(2)) * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((Symbol('e'))**(Integer(2)) * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('e') * ((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + ((Symbol('e') * (Symbol('d') + (Symbol('e') * x)) * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)*cosh(a + b*x + c*x**2),
        variable=x,
        num_steps=6,
        integral=(((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * (sympy.E)**(((Integer(-1) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * (sympy.E)**((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('e') * sympy.sinh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2)/(d + e*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.cosh((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * ((Symbol('d') + (Symbol('e') * x)))**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)**2*cosh(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=14,
        integral=((((Symbol('d') + (Symbol('e') * x)))**(Integer(3)) * ((Integer(6) * Symbol('e')))**(Integer(-1))) + (((Symbol('e'))**(Integer(2)) * (sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * (sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((Symbol('e'))**(Integer(2)) * (sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * (sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(32) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('e') * ((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + ((Symbol('e') * (Symbol('d') + (Symbol('e') * x)) * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)*cosh(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=8,
        integral=((((Symbol('d') + (Symbol('e') * x)))**(Integer(2)) * ((Integer(4) * Symbol('e')))**(Integer(-1))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * (sympy.E)**(((Integer(-2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * (sympy.E)**(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('e') * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x + c*x**2)**2/(d + e*x),
        variable=x,
        num_steps=2,
        integral=(((Integer(2))**(Integer(-1)) * sympy.Function('Unintegrable')((sympy.cosh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * ((Symbol('d') + (Symbol('e') * x)))**(Integer(-1))), x)) + (sympy.log((Symbol('d') + (Symbol('e') * x))) * ((Integer(2) * Symbol('e')))**(Integer(-1)))),
    ),
]
