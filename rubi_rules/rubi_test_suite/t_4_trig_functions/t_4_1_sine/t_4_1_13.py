# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.1 Sine/4.1.13 (d+e x)^m sin(a+b x+c x^2)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.1 Sine/4.1.13 (d+e x)^m sin(a+b x+c x^2)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e = symbols('a b c d e')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=x**2*sin(a + b*x + c*x**2),
        variable=x,
        num_steps=8,
        integral=(((Symbol('b') * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + (Integer(-1) * ((x * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(a + b*x + c*x**2),
        variable=x,
        num_steps=4,
        integral=((Integer(-1) * (sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2),
        variable=x,
        num_steps=3,
        integral=(((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.sin((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=-b*cos(a + b*x + c*x**2)/x + sin(a + b*x + c*x**2)/x**2,
        variable=x,
        num_steps=5,
        integral=((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi)) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) + (Integer(-1) * (sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi)) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))))) + (Integer(-1) * (sympy.sin((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*sin(a + b*x - c*x**2),
        variable=x,
        num_steps=8,
        integral=(((Symbol('b') * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2))))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + ((x * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2))))))) * ((Integer(2) * Symbol('c')))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(a + b*x - c*x**2),
        variable=x,
        num_steps=4,
        integral=((sympy.cos((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1))) + ((Symbol('b') * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x - c*x**2),
        variable=x,
        num_steps=3,
        integral=(((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x - c*x**2)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.sin((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=-b*cos(a + b*x - c*x**2)/x + sin(a + b*x - c*x**2)/x**2,
        variable=x,
        num_steps=5,
        integral=((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi)) * sympy.cos((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) + (sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi)) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) + (Integer(-1) * (sympy.sin((Symbol('a') + (Symbol('b') * x) + (Integer(-1) * (Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*sin(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=6,
        integral=(((Integer(4))**(Integer(-1)) * sympy.cos(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * x * sympy.cos(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt((Integer(2) * sympy.pi)))**(Integer(-1))))) + ((Integer(4))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt((Integer(2) * sympy.pi)))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=3,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.cos(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt((Integer(2) * sympy.pi)))**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4),
        variable=x,
        num_steps=2,
        integral=(sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt((Integer(2) * sympy.pi)))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4)/x,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.sin(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4)/x**2,
        variable=x,
        num_steps=3,
        integral=((sympy.sqrt((Integer(2) * sympy.pi)) * sympy.Function('FresnelC')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt((Integer(2) * sympy.pi)))**(Integer(-1))))) + sympy.Function('Unintegrable')((sympy.cos(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1))), x) + (Integer(-1) * (sympy.sin(((Integer(4))**(Integer(-1)) + x + (x)**(Integer(2)))) * (x)**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=10,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + (Integer(-1) * (((Symbol('b'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('b') * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + (Integer(-1) * ((x * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=6,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + ((Symbol('b') * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=5,
        integral=((x * (Integer(2))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + ((sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.Function('Unintegrable')((sympy.cos(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*sin(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=10,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('b'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('b') * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2))))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1))) + ((x * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2))))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=6,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + ((Symbol('b') * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((Symbol('b') * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x - c*x**2)**2,
        variable=x,
        num_steps=5,
        integral=((x * (Integer(2))**(Integer(-1))) + ((sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1))) + ((sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(-1) * (Integer(2) * Symbol('c') * x))) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x - c*x**2)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.Function('Unintegrable')((sympy.cos(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(-1) * (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*sin(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=8,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + (Integer(-1) * ((Integer(16))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(sympy.pi))**(Integer(-1)))))) + ((Integer(16))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(sympy.pi))**(Integer(-1))))) + ((Integer(16))**(Integer(-1)) * sympy.sin(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2)))))) + (Integer(-1) * ((Integer(8))**(Integer(-1)) * x * sympy.sin(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2)))))))),
    ),
    RubiTestSuiteCase(
        integrand=x*sin(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=5,
        integral=(((x)**(Integer(2)) * (Integer(4))**(Integer(-1))) + ((Integer(8))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(sympy.pi))**(Integer(-1))))) + (Integer(-1) * ((Integer(8))**(Integer(-1)) * sympy.sin(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2)))))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4)**2,
        variable=x,
        num_steps=4,
        integral=((x * (Integer(2))**(Integer(-1))) + (Integer(-1) * ((Integer(4))**(Integer(-1)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(sympy.pi))**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4)**2/x,
        variable=x,
        num_steps=2,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.Function('Unintegrable')((sympy.cos(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))) * (x)**(Integer(-1))), x)) + (sympy.log(x) * (Integer(2))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(x**2 + x + sympy.S(1)/4)**2/x**2,
        variable=x,
        num_steps=5,
        integral=((Integer(-1) * ((Integer(2) * x))**(Integer(-1))) + (sympy.cos(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))) * ((Integer(2) * x))**(Integer(-1))) + (sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Integer(1) + (Integer(2) * x)) * (sympy.sqrt(sympy.pi))**(Integer(-1))))) + sympy.Function('Unintegrable')((sympy.sin(((Integer(2))**(Integer(-1)) + (Integer(2) * x) + (Integer(2) * (x)**(Integer(2))))) * (x)**(Integer(-1))), x)),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)**2*sin(a + b*x + c*x**2),
        variable=x,
        num_steps=8,
        integral=((Integer(-1) * ((Symbol('e') * ((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(4) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('e') * (Symbol('d') + (Symbol('e') * x)) * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))) + (((Symbol('e'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(4) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((Symbol('e'))**(Integer(2)) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)*sin(a + b*x + c*x**2),
        variable=x,
        num_steps=4,
        integral=((Integer(-1) * ((Symbol('e') * sympy.cos((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('c')))**(Integer(-1)))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * ((Integer(2) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2),
        variable=x,
        num_steps=3,
        integral=(((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.cos((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt((Integer(2) * sympy.pi))))**(Integer(-1)))) * sympy.sin((Symbol('a') + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(4) * Symbol('c')))**(Integer(-1))))))) * (sympy.sqrt(Symbol('c')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)/(d + e*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((sympy.sin((Symbol('a') + (Symbol('b') * x) + (Symbol('c') * (x)**(Integer(2))))) * ((Symbol('d') + (Symbol('e') * x)))**(Integer(-1))), x),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)**2*sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=10,
        integral=((((Symbol('d') + (Symbol('e') * x)))**(Integer(3)) * ((Integer(6) * Symbol('e')))**(Integer(-1))) + (Integer(-1) * (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (((Symbol('e'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((Symbol('e'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(16) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(16) * (Symbol('c'))**((Integer(5) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('e') * ((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(16) * (Symbol('c'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('e') * (Symbol('d') + (Symbol('e') * x)) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=(d + e*x)*sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=6,
        integral=((((Symbol('d') + (Symbol('e') * x)))**(Integer(2)) * ((Integer(4) * Symbol('e')))**(Integer(-1))) + (Integer(-1) * ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((((Integer(2) * Symbol('c') * Symbol('d')) + (Integer(-1) * (Symbol('b') * Symbol('e')))) * sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(8) * (Symbol('c'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('e') * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('c')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)**2,
        variable=x,
        num_steps=5,
        integral=((x * (Integer(2))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.cos(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1)))))) * sympy.Function('FresnelC')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + ((sympy.sqrt(sympy.pi) * sympy.Function('FresnelS')(((Symbol('b') + (Integer(2) * Symbol('c') * x)) * ((sympy.sqrt(Symbol('c')) * sympy.sqrt(sympy.pi)))**(Integer(-1)))) * sympy.sin(((Integer(2) * Symbol('a')) + (Integer(-1) * ((Symbol('b'))**(Integer(2)) * ((Integer(2) * Symbol('c')))**(Integer(-1))))))) * ((Integer(4) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=sin(a + b*x + c*x**2)**2/(d + e*x),
        variable=x,
        num_steps=2,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.Function('Unintegrable')((sympy.cos(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * x) + (Integer(2) * Symbol('c') * (x)**(Integer(2))))) * ((Symbol('d') + (Symbol('e') * x)))**(Integer(-1))), x)) + (sympy.log((Symbol('d') + (Symbol('e') * x))) * ((Integer(2) * Symbol('e')))**(Integer(-1)))),
    ),
]
