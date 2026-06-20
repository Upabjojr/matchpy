# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.3 (e x)^m (a+b cosh(c+d x^n))^p.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '6 Hyperbolic functions/6.2 Hyperbolic cosine/6.2.3 (e x)^m (a+b cosh(c+d x^n))^p.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, e, m, n, p = symbols('a b c d e m n p')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=x**3*cosh(a + b*x**2),
        variable=x,
        num_steps=3,
        integral=x**2*sinh(a + b*x**2)/(2*b) - cosh(a + b*x**2)/(2*b**2),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x**2),
        variable=x,
        num_steps=4,
        integral=(((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**(Symbol('a')) * (Integer(8) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1)))))))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x))) * ((Integer(8) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((x * sympy.sinh((Symbol('a') + (Symbol('b') * (x)**(Integer(2)))))) * ((Integer(2) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x**2),
        variable=x,
        num_steps=2,
        integral=sinh(a + b*x**2)/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2),
        variable=x,
        num_steps=3,
        integral=(((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**(Symbol('a')) * (Integer(4) * sympy.sqrt(Symbol('b')))))**(Integer(-1))) + (((sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x))) * ((Integer(4) * sympy.sqrt(Symbol('b'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)/x,
        variable=x,
        num_steps=3,
        integral=(((Integer(2))**(Integer(-1)) * sympy.cosh(Symbol('a')) * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(2))))) + ((Integer(2))**(Integer(-1)) * sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)/x**2,
        variable=x,
        num_steps=4,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(2))))) * (x)**(Integer(-1)))) + (Integer(-1) * (((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * ((sympy.E)**(Symbol('a')))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * (sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)/x**3,
        variable=x,
        num_steps=5,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(2))))) * ((Integer(2) * (x)**(Integer(2))))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * Symbol('b') * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(2)))) * sympy.sinh(Symbol('a'))) + ((Integer(2))**(Integer(-1)) * Symbol('b') * sympy.cosh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=x**3*cosh(a + b*x**2)**2,
        variable=x,
        num_steps=3,
        integral=x**4/8 + x**2*sinh(a + b*x**2)*cosh(a + b*x**2)/(4*b) - cosh(a + b*x**2)**2/(8*b**2),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x**2)**2,
        variable=x,
        num_steps=6,
        integral=(((x)**(Integer(3)) * (Integer(6))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**((Integer(2) * Symbol('a'))) * (Integer(32) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1)))))))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**((Integer(2) * Symbol('a'))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x))) * ((Integer(32) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((x * sympy.sinh(((Integer(2) * Symbol('a')) + (Integer(2) * Symbol('b') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x**2)**2,
        variable=x,
        num_steps=3,
        integral=x**2/4 + sinh(a + b*x**2)*cosh(a + b*x**2)/(4*b),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**2,
        variable=x,
        num_steps=5,
        integral=((x * (Integer(2))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**((Integer(2) * Symbol('a'))) * (Integer(8) * sympy.sqrt(Symbol('b')))))**(Integer(-1))) + (((sympy.E)**((Integer(2) * Symbol('a'))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x))) * ((Integer(8) * sympy.sqrt(Symbol('b'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**2/x,
        variable=x,
        num_steps=5,
        integral=(((Integer(4))**(Integer(-1)) * sympy.cosh((Integer(2) * Symbol('a'))) * sympy.Function('CoshIntegral')((Integer(2) * Symbol('b') * (x)**(Integer(2))))) + (sympy.log(x) * (Integer(2))**(Integer(-1))) + ((Integer(4))**(Integer(-1)) * sympy.sinh((Integer(2) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(2) * Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**2/x**2,
        variable=x,
        num_steps=6,
        integral=((Integer(-1) * ((sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(2))))))**(Integer(2)) * (x)**(Integer(-1)))) + (Integer(-1) * (((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erf')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x))) * ((sympy.E)**((Integer(2) * Symbol('a'))))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * (sympy.E)**((Integer(2) * Symbol('a'))) * sympy.sqrt((sympy.pi * (Integer(2))**(Integer(-1)))) * sympy.Function('Erfi')((sympy.sqrt(Integer(2)) * sympy.sqrt(Symbol('b')) * x)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**2/x**3,
        variable=x,
        num_steps=7,
        integral=((Integer(-1) * ((Integer(4) * (x)**(Integer(2))))**(Integer(-1))) + (Integer(-1) * (sympy.cosh((Integer(2) * (Symbol('a') + (Symbol('b') * (x)**(Integer(2)))))) * ((Integer(4) * (x)**(Integer(2))))**(Integer(-1)))) + ((Integer(2))**(Integer(-1)) * Symbol('b') * sympy.Function('CoshIntegral')((Integer(2) * Symbol('b') * (x)**(Integer(2)))) * sympy.sinh((Integer(2) * Symbol('a')))) + ((Integer(2))**(Integer(-1)) * Symbol('b') * sympy.cosh((Integer(2) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(2) * Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=x**3*cosh(a + b*x**2)**3,
        variable=x,
        num_steps=4,
        integral=x**2*sinh(a + b*x**2)*cosh(a + b*x**2)**2/(6*b) + x**2*sinh(a + b*x**2)/(3*b) - cosh(a + b*x**2)**3/(18*b**2) - cosh(a + b*x**2)/(3*b**2),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*x**2)**3,
        variable=x,
        num_steps=10,
        integral=(((Integer(3) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**(Symbol('a')) * (Integer(32) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1)))))))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(3))**(Integer(-1)))) * sympy.Function('Erf')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**((Integer(3) * Symbol('a'))) * (Integer(96) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1)))))))**(Integer(-1))) + (Integer(-1) * ((Integer(3) * (sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x))) * ((Integer(32) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**((Integer(3) * Symbol('a'))) * sympy.sqrt((sympy.pi * (Integer(3))**(Integer(-1)))) * sympy.Function('Erfi')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x))) * ((Integer(96) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1)))) + ((Integer(3) * x * sympy.sinh((Symbol('a') + (Symbol('b') * (x)**(Integer(2)))))) * ((Integer(8) * Symbol('b')))**(Integer(-1))) + ((x * sympy.sinh(((Integer(3) * Symbol('a')) + (Integer(3) * Symbol('b') * (x)**(Integer(2)))))) * ((Integer(24) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x**2)**3,
        variable=x,
        num_steps=3,
        integral=sinh(a + b*x**2)**3/(6*b) + sinh(a + b*x**2)/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**3,
        variable=x,
        num_steps=8,
        integral=(((Integer(3) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**(Symbol('a')) * (Integer(16) * sympy.sqrt(Symbol('b')))))**(Integer(-1))) + ((sympy.sqrt((sympy.pi * (Integer(3))**(Integer(-1)))) * sympy.Function('Erf')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x))) * (((sympy.E)**((Integer(3) * Symbol('a'))) * (Integer(16) * sympy.sqrt(Symbol('b')))))**(Integer(-1))) + ((Integer(3) * (sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x))) * ((Integer(16) * sympy.sqrt(Symbol('b'))))**(Integer(-1))) + (((sympy.E)**((Integer(3) * Symbol('a'))) * sympy.sqrt((sympy.pi * (Integer(3))**(Integer(-1)))) * sympy.Function('Erfi')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x))) * ((Integer(16) * sympy.sqrt(Symbol('b'))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**3/x,
        variable=x,
        num_steps=8,
        integral=(((Integer(3) * (Integer(8))**(Integer(-1))) * sympy.cosh(Symbol('a')) * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(2))))) + ((Integer(8))**(Integer(-1)) * sympy.cosh((Integer(3) * Symbol('a'))) * sympy.Function('CoshIntegral')((Integer(3) * Symbol('b') * (x)**(Integer(2))))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(2))))) + ((Integer(8))**(Integer(-1)) * sympy.sinh((Integer(3) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(3) * Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**3/x**2,
        variable=x,
        num_steps=9,
        integral=((Integer(-1) * ((sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(2))))))**(Integer(3)) * (x)**(Integer(-1)))) + (Integer(-1) * (((Integer(3) * (Integer(8))**(Integer(-1))) * sympy.sqrt(Symbol('b')) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * x))) * ((sympy.E)**(Symbol('a')))**(Integer(-1)))) + (Integer(-1) * (((Integer(8))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * sympy.sqrt((Integer(3) * sympy.pi)) * sympy.Function('Erf')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x))) * ((sympy.E)**((Integer(3) * Symbol('a'))))**(Integer(-1)))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * sympy.sqrt(Symbol('b')) * (sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * x))) + ((Integer(8))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * (sympy.E)**((Integer(3) * Symbol('a'))) * sympy.sqrt((Integer(3) * sympy.pi)) * sympy.Function('Erfi')((sympy.sqrt(Integer(3)) * sympy.sqrt(Symbol('b')) * x)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**2)**3/x**3,
        variable=x,
        num_steps=12,
        integral=((Integer(-1) * ((Integer(3) * sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(2)))))) * ((Integer(8) * (x)**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * (sympy.cosh((Integer(3) * (Symbol('a') + (Symbol('b') * (x)**(Integer(2)))))) * ((Integer(8) * (x)**(Integer(2))))**(Integer(-1)))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * Symbol('b') * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(2)))) * sympy.sinh(Symbol('a'))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * Symbol('b') * sympy.Function('CoshIntegral')((Integer(3) * Symbol('b') * (x)**(Integer(2)))) * sympy.sinh((Integer(3) * Symbol('a')))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * Symbol('b') * sympy.cosh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(2))))) + ((Integer(3) * (Integer(8))**(Integer(-1))) * Symbol('b') * sympy.cosh((Integer(3) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(3) * Symbol('b') * (x)**(Integer(2)))))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*x**2)**7,
        variable=x,
        num_steps=3,
        integral=sinh(a + b*x**2)**7/(14*b) + 3*sinh(a + b*x**2)**5/(10*b) + sinh(a + b*x**2)**3/(2*b) + sinh(a + b*x**2)/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(x**3),
        variable=x,
        num_steps=2,
        integral=sinh(x**3)/3,
    ),
    RubiTestSuiteCase(
        integrand=cosh(x**(-5))/x**6,
        variable=x,
        num_steps=2,
        integral=-sinh(x**(-5))/5,
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x),
        variable=x,
        num_steps=5,
        integral=((x * sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Integer(-1)))))) + (Integer(-1) * (Symbol('b') * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(-1)))) * sympy.sinh(Symbol('a')))) + (Integer(-1) * (Symbol('b') * sympy.cosh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x)/x,
        variable=x,
        num_steps=3,
        integral=(((Integer(-1) * sympy.cosh(Symbol('a'))) * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Integer(-1))))) + (Integer(-1) * (sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x)/x**2,
        variable=x,
        num_steps=2,
        integral=-sinh(a + b/x)/b,
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x)/x**3,
        variable=x,
        num_steps=3,
        integral=-sinh(a + b/x)/(b*x) + cosh(a + b/x)/b**2,
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x)/x**4,
        variable=x,
        num_steps=4,
        integral=-sinh(a + b/x)/(b*x**2) + 2*cosh(a + b/x)/(b**2*x) - 2*sinh(a + b/x)/b**3,
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x**2),
        variable=x,
        num_steps=5,
        integral=((x * sympy.cosh((Symbol('a') + (Symbol('b') * ((x)**(Integer(2)))**(Integer(-1)))))) + (((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))) * ((sympy.E)**(Symbol('a')))**(Integer(-1))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.sqrt(Symbol('b')) * (sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x**2)/x,
        variable=x,
        num_steps=3,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.cosh(Symbol('a')) * sympy.Function('CoshIntegral')((Symbol('b') * ((x)**(Integer(2)))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * ((x)**(Integer(2)))**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x**2)/x**2,
        variable=x,
        num_steps=4,
        integral=((Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))) * (((sympy.E)**(Symbol('a')) * (Integer(4) * sympy.sqrt(Symbol('b')))))**(Integer(-1)))) + (Integer(-1) * (((sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))) * ((Integer(4) * sympy.sqrt(Symbol('b'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x**2)/x**3,
        variable=x,
        num_steps=2,
        integral=-sinh(a + b/x**2)/(2*b),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b/x**2)/x**4,
        variable=x,
        num_steps=5,
        integral=((Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))) * (((sympy.E)**(Symbol('a')) * (Integer(8) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1)))))))**(Integer(-1)))) + (((sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * (x)**(Integer(-1))))) * ((Integer(8) * (Symbol('b'))**((Integer(3) * (Integer(2))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (sympy.sinh((Symbol('a') + (Symbol('b') * ((x)**(Integer(2)))**(Integer(-1))))) * ((Integer(2) * Symbol('b') * x))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n),
        variable=x,
        num_steps=3,
        integral=((Integer(-1) * (((sympy.E)**(Symbol('a')) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), ((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))) * (((((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(2) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Symbol('b') * (x)**(Symbol('n'))))) * (((sympy.E)**(Symbol('a')) * ((Symbol('b') * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(2) * Symbol('n'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n)/x,
        variable=x,
        num_steps=3,
        integral=(((sympy.cosh(Symbol('a')) * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * (Symbol('n'))**(Integer(-1))) + ((sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * (Symbol('n'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n)**2,
        variable=x,
        num_steps=5,
        integral=((x * (Integer(2))**(Integer(-1))) + (Integer(-1) * (((Integer(2))**((Integer(-2) + (Integer(-1) * (Symbol('n'))**(Integer(-1))))) * (sympy.E)**((Integer(2) * Symbol('a'))) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Integer(-2) * Symbol('b') * (x)**(Symbol('n'))))) * (((((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * Symbol('n')))**(Integer(-1)))) + (Integer(-1) * (((Integer(2))**((Integer(-2) + (Integer(-1) * (Symbol('n'))**(Integer(-1))))) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Integer(2) * Symbol('b') * (x)**(Symbol('n'))))) * (((sympy.E)**((Integer(2) * Symbol('a'))) * ((Symbol('b') * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * Symbol('n')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n)**2/x,
        variable=x,
        num_steps=5,
        integral=(((sympy.cosh((Integer(2) * Symbol('a'))) * sympy.Function('CoshIntegral')((Integer(2) * Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(2) * Symbol('n')))**(Integer(-1))) + (sympy.log(x) * (Integer(2))**(Integer(-1))) + ((sympy.sinh((Integer(2) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(2) * Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(2) * Symbol('n')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n)**3,
        variable=x,
        num_steps=8,
        integral=((Integer(-1) * (((sympy.E)**((Integer(3) * Symbol('a'))) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Integer(-3) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(3))**((Symbol('n'))**(Integer(-1))) * (((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * (sympy.E)**(Symbol('a')) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), ((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))) * (((((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Symbol('b') * (x)**(Symbol('n'))))) * (((sympy.E)**(Symbol('a')) * ((Symbol('b') * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((x * sympy.Function('Gamma')((Symbol('n'))**(Integer(-1)), (Integer(3) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(3))**((Symbol('n'))**(Integer(-1))) * (sympy.E)**((Integer(3) * Symbol('a'))) * ((Symbol('b') * (x)**(Symbol('n'))))**((Symbol('n'))**(Integer(-1))) * (Integer(8) * Symbol('n'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*x**n)**3/x,
        variable=x,
        num_steps=8,
        integral=(((Integer(3) * sympy.cosh(Symbol('a')) * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((sympy.cosh((Integer(3) * Symbol('a'))) * sympy.Function('CoshIntegral')((Integer(3) * Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((Integer(3) * sympy.sinh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((sympy.sinh((Integer(3) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(3) * Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=(b*cosh(c + d*x**n))**p*(e*x)**m,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((((Symbol('e') * x))**(Symbol('m')) * ((Symbol('b') * sympy.cosh((Symbol('c') + (Symbol('d') * (x)**(Symbol('n')))))))**(Symbol('p'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(e*x)**m*(a + b*cosh(c + d*x**n))**p,
        variable=x,
        num_steps=0,
        integral=sympy.Function('Unintegrable')((((Symbol('e') * x))**(Symbol('m')) * ((Symbol('a') + (Symbol('b') * sympy.cosh((Symbol('c') + (Symbol('d') * (x)**(Symbol('n'))))))))**(Symbol('p'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(b*cosh(c + d*x**n))**p*(e*x)**(n - 1),
        variable=x,
        num_steps=3,
        integral=-(b*cosh(c + d*x**n))**(p + 1)*(e*x)**n*sinh(c + d*x**n)*hyper((sympy.S.Half, p/2 + sympy.S.Half), (p/2 + sympy.S(3)/2,), cosh(c + d*x**n)**2)/(b*d*e*n*x**n*sqrt(-sinh(c + d*x**n)**2)*(p + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(b*cosh(c + d*x**n))**p*(e*x)**(2*n - 1),
        variable=x,
        num_steps=1,
        integral=((((Symbol('e') * x))**((Integer(2) * Symbol('n'))) * sympy.Function('Unintegrable')(((x)**((Integer(-1) + (Integer(2) * Symbol('n')))) * ((Symbol('b') * sympy.cosh((Symbol('c') + (Symbol('d') * (x)**(Symbol('n')))))))**(Symbol('p'))), x)) * (((x)**((Integer(2) * Symbol('n'))) * Symbol('e')))**(Integer(-1))),
    ),
    RubiTestSuiteCase(
        integrand=(e*x)**(n - 1)*(a + b*cosh(c + d*x**n))**p,
        variable=x,
        num_steps=5,
        integral=sqrt(2)*(e*x)**n*(a + b*cosh(c + d*x**n))**p*sinh(c + d*x**n)*appellf1(sympy.S.Half, sympy.S.Half, -p, sympy.S(3)/2, sympy.S.Half - cosh(c + d*x**n)/2, b*(1 - cosh(c + d*x**n))/(a + b))/(d*e*n*x**n*((a + b*cosh(c + d*x**n))/(a + b))**p*sqrt(cosh(c + d*x**n) + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(e*x)**(2*n - 1)*(a + b*cosh(c + d*x**n))**p,
        variable=x,
        num_steps=1,
        integral=((((Symbol('e') * x))**((Integer(2) * Symbol('n'))) * sympy.Function('Unintegrable')(((x)**((Integer(-1) + (Integer(2) * Symbol('n')))) * ((Symbol('a') + (Symbol('b') * sympy.cosh((Symbol('c') + (Symbol('d') * (x)**(Symbol('n'))))))))**(Symbol('p'))), x)) * (((x)**((Integer(2) * Symbol('n'))) * Symbol('e')))**(Integer(-1))),
    ),
    RubiTestSuiteCase(
        integrand=x**m*cosh(a + b*x**n),
        variable=x,
        num_steps=3,
        integral=((Integer(-1) * (((sympy.E)**(Symbol('a')) * (x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), ((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))) * (((((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(2) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * (((x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Symbol('b') * (x)**(Symbol('n'))))) * (((sympy.E)**(Symbol('a')) * ((Symbol('b') * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(2) * Symbol('n'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**m*cosh(a + b*x**n)**2,
        variable=x,
        num_steps=5,
        integral=(((x)**((Integer(1) + Symbol('m'))) * ((Integer(2) * (Integer(1) + Symbol('m'))))**(Integer(-1))) + (Integer(-1) * (((sympy.E)**((Integer(2) * Symbol('a'))) * (x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Integer(-2) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(2))**(((Integer(1) + Symbol('m') + (Integer(2) * Symbol('n'))) * (Symbol('n'))**(Integer(-1)))) * (((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * Symbol('n')))**(Integer(-1)))) + (Integer(-1) * (((x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Integer(2) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(2))**(((Integer(1) + Symbol('m') + (Integer(2) * Symbol('n'))) * (Symbol('n'))**(Integer(-1)))) * (sympy.E)**((Integer(2) * Symbol('a'))) * ((Symbol('b') * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * Symbol('n')))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**m*cosh(a + b*x**n)**3,
        variable=x,
        num_steps=8,
        integral=((Integer(-1) * (((sympy.E)**((Integer(3) * Symbol('a'))) * (x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Integer(-3) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(3))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * (sympy.E)**(Symbol('a')) * (x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), ((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))) * (((((Integer(-1) * Symbol('b')) * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * ((Integer(3) * (x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Symbol('b') * (x)**(Symbol('n'))))) * (((sympy.E)**(Symbol('a')) * ((Symbol('b') * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(8) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * (((x)**((Integer(1) + Symbol('m'))) * sympy.Function('Gamma')(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1))), (Integer(3) * Symbol('b') * (x)**(Symbol('n'))))) * (((Integer(3))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (sympy.E)**((Integer(3) * Symbol('a'))) * ((Symbol('b') * (x)**(Symbol('n'))))**(((Integer(1) + Symbol('m')) * (Symbol('n'))**(Integer(-1)))) * (Integer(8) * Symbol('n'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**(-n - 1)*cosh(a + b*x**n),
        variable=x,
        num_steps=5,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Symbol('n'))))) * (((x)**(Symbol('n')) * Symbol('n')))**(Integer(-1)))) + ((Symbol('b') * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Symbol('n')))) * sympy.sinh(Symbol('a'))) * (Symbol('n'))**(Integer(-1))) + ((Symbol('b') * sympy.cosh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * (Symbol('n'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**(-n - 1)*cosh(a + b*x**n)**2,
        variable=x,
        num_steps=7,
        integral=((Integer(-1) * (((x)**(Symbol('n')) * (Integer(2) * Symbol('n'))))**(Integer(-1))) + (Integer(-1) * (sympy.cosh((Integer(2) * (Symbol('a') + (Symbol('b') * (x)**(Symbol('n')))))) * (((x)**(Symbol('n')) * (Integer(2) * Symbol('n'))))**(Integer(-1)))) + ((Symbol('b') * sympy.Function('CoshIntegral')((Integer(2) * Symbol('b') * (x)**(Symbol('n')))) * sympy.sinh((Integer(2) * Symbol('a')))) * (Symbol('n'))**(Integer(-1))) + ((Symbol('b') * sympy.cosh((Integer(2) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(2) * Symbol('b') * (x)**(Symbol('n'))))) * (Symbol('n'))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**(-n - 1)*cosh(a + b*x**n)**3,
        variable=x,
        num_steps=12,
        integral=((Integer(-1) * ((Integer(3) * sympy.cosh((Symbol('a') + (Symbol('b') * (x)**(Symbol('n')))))) * (((x)**(Symbol('n')) * (Integer(4) * Symbol('n'))))**(Integer(-1)))) + (Integer(-1) * (sympy.cosh((Integer(3) * (Symbol('a') + (Symbol('b') * (x)**(Symbol('n')))))) * (((x)**(Symbol('n')) * (Integer(4) * Symbol('n'))))**(Integer(-1)))) + ((Integer(3) * Symbol('b') * sympy.Function('CoshIntegral')((Symbol('b') * (x)**(Symbol('n')))) * sympy.sinh(Symbol('a'))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((Integer(3) * Symbol('b') * sympy.Function('CoshIntegral')((Integer(3) * Symbol('b') * (x)**(Symbol('n')))) * sympy.sinh((Integer(3) * Symbol('a')))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((Integer(3) * Symbol('b') * sympy.cosh(Symbol('a')) * sympy.Function('SinhIntegral')((Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1))) + ((Integer(3) * Symbol('b') * sympy.cosh((Integer(3) * Symbol('a'))) * sympy.Function('SinhIntegral')((Integer(3) * Symbol('b') * (x)**(Symbol('n'))))) * ((Integer(4) * Symbol('n')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**(n/2 - 1)*cosh(a + b*x**n),
        variable=x,
        num_steps=4,
        integral=(((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((sympy.sqrt(Symbol('b')) * (x)**((Symbol('n') * (Integer(2))**(Integer(-1))))))) * (((sympy.E)**(Symbol('a')) * (Integer(2) * sympy.sqrt(Symbol('b')) * Symbol('n'))))**(Integer(-1))) + (((sympy.E)**(Symbol('a')) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((sympy.sqrt(Symbol('b')) * (x)**((Symbol('n') * (Integer(2))**(Integer(-1))))))) * ((Integer(2) * sympy.sqrt(Symbol('b')) * Symbol('n')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh((a + b*x)**2),
        variable=x,
        num_steps=12,
        integral=(((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(8) * (Symbol('b'))**(Integer(3))))**(Integer(-1))) + (((Symbol('a'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * (Symbol('b'))**(Integer(3))))**(Integer(-1))) + (Integer(-1) * ((sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(8) * (Symbol('b'))**(Integer(3))))**(Integer(-1)))) + (((Symbol('a'))**(Integer(2)) * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * (Symbol('b'))**(Integer(3))))**(Integer(-1))) + (Integer(-1) * ((Symbol('a') * sympy.sinh(((Symbol('a') + (Symbol('b') * x)))**(Integer(2)))) * ((Symbol('b'))**(Integer(3)))**(Integer(-1)))) + (((Symbol('a') + (Symbol('b') * x)) * sympy.sinh(((Symbol('a') + (Symbol('b') * x)))**(Integer(2)))) * ((Integer(2) * (Symbol('b'))**(Integer(3))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh((a + b*x)**2),
        variable=x,
        num_steps=8,
        integral=((Integer(-1) * ((Symbol('a') * sympy.sqrt(sympy.pi) * sympy.Function('Erf')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('a') * sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))) + (sympy.sinh(((Symbol('a') + (Symbol('b') * x)))**(Integer(2))) * ((Integer(2) * (Symbol('b'))**(Integer(2))))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh((a + b*x)**2),
        variable=x,
        num_steps=4,
        integral=(((sympy.sqrt(sympy.pi) * sympy.Function('Erf')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * Symbol('b')))**(Integer(-1))) + ((sympy.sqrt(sympy.pi) * sympy.Function('Erfi')((Symbol('a') + (Symbol('b') * x)))) * ((Integer(4) * Symbol('b')))**(Integer(-1)))),
    ),
    RubiTestSuiteCase(
        integrand=cosh((a + b*x)**2)/x,
        variable=x,
        num_steps=1,
        integral=(Symbol('b') * sympy.Function('CannotIntegrate')((sympy.cosh(((Symbol('a') + (Symbol('b') * x)))**(Integer(2))) * ((Symbol('b') * x))**(Integer(-1))), x)),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*sqrt(c + d*x)),
        variable=x,
        num_steps=16,
        integral=2*c**2*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b*d**3) - 4*c*(c + d*x)**(sympy.S(3)/2)*sinh(a + b*sqrt(c + d*x))/(b*d**3) + 2*(c + d*x)**(sympy.S(5)/2)*sinh(a + b*sqrt(c + d*x))/(b*d**3) - 2*c**2*cosh(a + b*sqrt(c + d*x))/(b**2*d**3) + 12*c*(c + d*x)*cosh(a + b*sqrt(c + d*x))/(b**2*d**3) - 10*(c + d*x)**2*cosh(a + b*sqrt(c + d*x))/(b**2*d**3) - 24*c*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b**3*d**3) + 40*(c + d*x)**(sympy.S(3)/2)*sinh(a + b*sqrt(c + d*x))/(b**3*d**3) + 24*c*cosh(a + b*sqrt(c + d*x))/(b**4*d**3) - (120*c + 120*d*x)*cosh(a + b*sqrt(c + d*x))/(b**4*d**3) + 240*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b**5*d**3) - 240*cosh(a + b*sqrt(c + d*x))/(b**6*d**3),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*sqrt(c + d*x)),
        variable=x,
        num_steps=10,
        integral=-2*c*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b*d**2) + 2*(c + d*x)**(sympy.S(3)/2)*sinh(a + b*sqrt(c + d*x))/(b*d**2) + 2*c*cosh(a + b*sqrt(c + d*x))/(b**2*d**2) - (6*c + 6*d*x)*cosh(a + b*sqrt(c + d*x))/(b**2*d**2) + 12*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b**3*d**2) - 12*cosh(a + b*sqrt(c + d*x))/(b**4*d**2),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*sqrt(c + d*x)),
        variable=x,
        num_steps=4,
        integral=2*sqrt(c + d*x)*sinh(a + b*sqrt(c + d*x))/(b*d) - 2*cosh(a + b*sqrt(c + d*x))/(b**2*d),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*sqrt(c + d*x))/x,
        variable=x,
        num_steps=10,
        integral=((sympy.cosh((Symbol('a') + (Symbol('b') * sympy.sqrt(Symbol('c'))))) * sympy.Function('CoshIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + (Integer(-1) * sympy.sqrt((Symbol('c') + (Symbol('d') * x)))))))) + (sympy.cosh((Symbol('a') + (Integer(-1) * (Symbol('b') * sympy.sqrt(Symbol('c')))))) * sympy.Function('CoshIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + sympy.sqrt((Symbol('c') + (Symbol('d') * x))))))) + (Integer(-1) * (sympy.sinh((Symbol('a') + (Symbol('b') * sympy.sqrt(Symbol('c'))))) * sympy.Function('SinhIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + (Integer(-1) * sympy.sqrt((Symbol('c') + (Symbol('d') * x))))))))) + (sympy.sinh((Symbol('a') + (Integer(-1) * (Symbol('b') * sympy.sqrt(Symbol('c')))))) * sympy.Function('SinhIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + sympy.sqrt((Symbol('c') + (Symbol('d') * x)))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*sqrt(c + d*x))/x**2,
        variable=x,
        num_steps=11,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * sympy.sqrt((Symbol('c') + (Symbol('d') * x)))))) * (x)**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * Symbol('d') * sympy.Function('CoshIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + sympy.sqrt((Symbol('c') + (Symbol('d') * x)))))) * sympy.sinh((Symbol('a') + (Integer(-1) * (Symbol('b') * sympy.sqrt(Symbol('c'))))))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + ((Symbol('b') * Symbol('d') * sympy.Function('CoshIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + (Integer(-1) * sympy.sqrt((Symbol('c') + (Symbol('d') * x))))))) * sympy.sinh((Symbol('a') + (Symbol('b') * sympy.sqrt(Symbol('c')))))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * Symbol('d') * sympy.cosh((Symbol('a') + (Symbol('b') * sympy.sqrt(Symbol('c'))))) * sympy.Function('SinhIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + (Integer(-1) * sympy.sqrt((Symbol('c') + (Symbol('d') * x)))))))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1)))) + (Integer(-1) * ((Symbol('b') * Symbol('d') * sympy.cosh((Symbol('a') + (Integer(-1) * (Symbol('b') * sympy.sqrt(Symbol('c')))))) * sympy.Function('SinhIntegral')((Symbol('b') * (sympy.sqrt(Symbol('c')) + sympy.sqrt((Symbol('c') + (Symbol('d') * x))))))) * ((Integer(2) * sympy.sqrt(Symbol('c'))))**(Integer(-1))))),
    ),
    RubiTestSuiteCase(
        integrand=x**2*cosh(a + b*(c + d*x)**(sympy.S(1)/3)),
        variable=x,
        num_steps=23,
        integral=3*c**2*(c + d*x)**(sympy.S(2)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d**3) - 6*c*(c + d*x)**(sympy.S(5)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d**3) + 3*(c + d*x)**(sympy.S(8)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d**3) - 6*c**2*(c + d*x)**(sympy.S(1)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d**3) + 30*c*(c + d*x)**(sympy.S(4)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d**3) - 24*(c + d*x)**(sympy.S(7)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d**3) + 6*c**2*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d**3) - 120*c*(c + d*x)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d**3) + 168*(c + d*x)**2*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d**3) + 360*c*(c + d*x)**(sympy.S(2)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**4*d**3) - 1008*(c + d*x)**(sympy.S(5)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**4*d**3) - 720*c*(c + d*x)**(sympy.S(1)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**5*d**3) + 5040*(c + d*x)**(sympy.S(4)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**5*d**3) + 720*c*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**6*d**3) - (20160*c + 20160*d*x)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**6*d**3) + 60480*(c + d*x)**(sympy.S(2)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**7*d**3) - 120960*(c + d*x)**(sympy.S(1)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**8*d**3) + 120960*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**9*d**3),
    ),
    RubiTestSuiteCase(
        integrand=x*cosh(a + b*(c + d*x)**(sympy.S(1)/3)),
        variable=x,
        num_steps=13,
        integral=-3*c*(c + d*x)**(sympy.S(2)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d**2) + 3*(c + d*x)**(sympy.S(5)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d**2) + 6*c*(c + d*x)**(sympy.S(1)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d**2) - 15*(c + d*x)**(sympy.S(4)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d**2) - 6*c*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d**2) + (60*c + 60*d*x)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d**2) - 180*(c + d*x)**(sympy.S(2)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**4*d**2) + 360*(c + d*x)**(sympy.S(1)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**5*d**2) - 360*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**6*d**2),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*(c + d*x)**(sympy.S(1)/3)),
        variable=x,
        num_steps=5,
        integral=3*(c + d*x)**(sympy.S(2)/3)*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b*d) - 6*(c + d*x)**(sympy.S(1)/3)*cosh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**2*d) + 6*sinh(a + b*(c + d*x)**(sympy.S(1)/3))/(b**3*d),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*(c + d*x)**(sympy.S(1)/3))/x,
        variable=x,
        num_steps=13,
        integral=((sympy.cosh((Symbol('a') + (Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('CoshIntegral')((Symbol('b') * ((Symbol('c'))**((Integer(3))**(Integer(-1))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))))) + (sympy.cosh((Symbol('a') + ((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('CoshIntegral')(((Integer(-1) * Symbol('b')) * (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))))) + (sympy.cosh((Symbol('a') + (Integer(-1) * ((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1))))))) * sympy.Function('CoshIntegral')((Symbol('b') * (((Integer(-1))**((Integer(3))**(Integer(-1))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))) + (Integer(-1) * (sympy.sinh((Symbol('a') + (Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('SinhIntegral')((Symbol('b') * ((Symbol('c'))**((Integer(3))**(Integer(-1))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))))) + (Integer(-1) * (sympy.sinh((Symbol('a') + ((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('SinhIntegral')((Symbol('b') * (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))))) + (sympy.sinh((Symbol('a') + (Integer(-1) * ((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1))))))) * sympy.Function('SinhIntegral')((Symbol('b') * (((Integer(-1))**((Integer(3))**(Integer(-1))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))))),
    ),
    RubiTestSuiteCase(
        integrand=cosh(a + b*(c + d*x)**(sympy.S(1)/3))/x**2,
        variable=x,
        num_steps=14,
        integral=((Integer(-1) * (sympy.cosh((Symbol('a') + (Symbol('b') * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))) * (x)**(Integer(-1)))) + ((Symbol('b') * Symbol('d') * sympy.Function('CoshIntegral')((Symbol('b') * ((Symbol('c'))**((Integer(3))**(Integer(-1))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))) * sympy.sinh((Symbol('a') + (Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * (((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * Symbol('d') * sympy.Function('CoshIntegral')((Symbol('b') * (((Integer(-1))**((Integer(3))**(Integer(-1))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))) * sympy.sinh((Symbol('a') + (Integer(-1) * ((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1)))) + (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * Symbol('d') * sympy.Function('CoshIntegral')(((Integer(-1) * Symbol('b')) * (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))) * sympy.sinh((Symbol('a') + ((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1))) + (Integer(-1) * ((Symbol('b') * Symbol('d') * sympy.cosh((Symbol('a') + (Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('SinhIntegral')((Symbol('b') * ((Symbol('c'))**((Integer(3))**(Integer(-1))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * Symbol('d') * sympy.cosh((Symbol('a') + ((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1)))))) * sympy.Function('SinhIntegral')((Symbol('b') * (((Integer(-1))**((Integer(2) * (Integer(3))**(Integer(-1)))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + (Integer(-1) * ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1)))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1)))) + (Integer(-1) * (((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * Symbol('d') * sympy.cosh((Symbol('a') + (Integer(-1) * ((Integer(-1))**((Integer(3))**(Integer(-1))) * Symbol('b') * (Symbol('c'))**((Integer(3))**(Integer(-1))))))) * sympy.Function('SinhIntegral')((Symbol('b') * (((Integer(-1))**((Integer(3))**(Integer(-1))) * (Symbol('c'))**((Integer(3))**(Integer(-1)))) + ((Symbol('c') + (Symbol('d') * x)))**((Integer(3))**(Integer(-1))))))) * ((Integer(3) * (Symbol('c'))**((Integer(2) * (Integer(3))**(Integer(-1))))))**(Integer(-1))))),
    ),
]
