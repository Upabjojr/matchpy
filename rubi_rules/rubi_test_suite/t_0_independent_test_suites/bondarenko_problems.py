# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 0 Independent test suites/Bondarenko Problems.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '0 Independent test suites/Bondarenko Problems.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
z = symbols('z')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=1/(sin(z) + cos(z) + sqrt(2)),
        variable=z,
        num_steps=1,
        integral=-(-sqrt(2)*sin(z) + 1)/(-sin(z) + cos(z)),
    ),
    RubiTestSuiteCase(
        integrand=(sqrt(1 - x) + sqrt(x + 1))**(-2),
        variable=x,
        num_steps=4,
        integral=asin(x)/2 + sqrt(1 - x**2)/(2*x) - 1/(2*x),
    ),
    RubiTestSuiteCase(
        integrand=(cos(x) + 1)**(-2),
        variable=x,
        num_steps=2,
        integral=sin(x)/(3*cos(x) + 3) + sin(x)/(3*(cos(x) + 1)**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/sqrt(x + 1),
        variable=x,
        num_steps=5,
        integral=((sympy.sqrt((Integer(2) * sympy.pi)) * sympy.cos(Integer(1)) * sympy.Function('FresnelS')((sympy.sqrt((Integer(2) * (sympy.pi)**(Integer(-1)))) * sympy.sqrt((Integer(1) + x))))) + (Integer(-1) * (sympy.sqrt((Integer(2) * sympy.pi)) * sympy.Function('FresnelC')((sympy.sqrt((Integer(2) * (sympy.pi)**(Integer(-1)))) * sympy.sqrt((Integer(1) + x)))) * sympy.sin(Integer(1))))),
    ),
    RubiTestSuiteCase(
        integrand=(sin(x) + cos(x))**(-6),
        variable=x,
        num_steps=3,
        integral=-(-sin(x) + cos(x))/(15*(sin(x) + cos(x))**3) - (-sin(x) + cos(x))/(10*(sin(x) + cos(x))**5) + 2*sin(x)/(15*sin(x) + 15*cos(x)),
    ),
    RubiTestSuiteCase(
        integrand=log(x**4 + x**(-4)),
        variable=x,
        num_steps=22,
        integral=x*log(x**4 + x**(-4)) - 4*x - sqrt(2 - sqrt(2))*log(x**2 - x*sqrt(2 - sqrt(2)) + 1)/2 + sqrt(2 - sqrt(2))*log(x**2 + x*sqrt(2 - sqrt(2)) + 1)/2 - sqrt(sqrt(2) + 2)*log(x**2 - x*sqrt(sqrt(2) + 2) + 1)/2 + sqrt(sqrt(2) + 2)*log(x**2 + x*sqrt(sqrt(2) + 2) + 1)/2 - sqrt(2 - sqrt(2))*atan((-2*x + sqrt(sqrt(2) + 2))/sqrt(2 - sqrt(2))) + sqrt(2 - sqrt(2))*atan((2*x + sqrt(sqrt(2) + 2))/sqrt(2 - sqrt(2))) - sqrt(sqrt(2) + 2)*atan((-2*x + sqrt(2 - sqrt(2)))/sqrt(sqrt(2) + 2)) + sqrt(sqrt(2) + 2)*atan((2*x + sqrt(2 - sqrt(2)))/sqrt(sqrt(2) + 2)),
    ),
    RubiTestSuiteCase(
        integrand=log(x + 1)/(x*sqrt(sqrt(x + 1) + 1)),
        variable=x,
        num_steps=-1,
        integral=((Integer(-8) * sympy.atanh(sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) + (Integer(-1) * ((Integer(2) * sympy.log((Integer(1) + x))) * (sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))**(Integer(-1)))) + (Integer(-1) * (sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))) * (sympy.sqrt(Integer(2)))**(Integer(-1)))) * sympy.log((Integer(1) + x)))) + (Integer(2) * sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt(Integer(2)))**(Integer(-1))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))))) + (Integer(-1) * (Integer(2) * sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt(Integer(2)))**(Integer(-1))) * sympy.log((Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))))) + (sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((sympy.sqrt(Integer(2)) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x))))))) * ((Integer(2) + (Integer(-1) * sympy.sqrt(Integer(2)))))**(Integer(-1)))))) + (Integer(-1) * (sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((sympy.sqrt(Integer(2)) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x))))))) * ((Integer(2) + sympy.sqrt(Integer(2))))**(Integer(-1)))))) + (Integer(-1) * (sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((sympy.sqrt(Integer(2)) * (Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) * ((Integer(2) + (Integer(-1) * sympy.sqrt(Integer(2)))))**(Integer(-1))))))) + (sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((sympy.sqrt(Integer(2)) * (Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) * ((Integer(2) + sympy.sqrt(Integer(2))))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(sqrt(x + 1) + 1)*log(x + 1)/x,
        variable=x,
        num_steps=-1,
        integral=((Integer(-16) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x))))) + (Integer(16) * sympy.atanh(sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) + (Integer(4) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))) * sympy.log((Integer(1) + x))) + (Integer(-1) * (Integer(2) * sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))) * (sympy.sqrt(Integer(2)))**(Integer(-1)))) * sympy.log((Integer(1) + x)))) + (Integer(4) * sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt(Integer(2)))**(Integer(-1))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))))) + (Integer(-1) * (Integer(4) * sympy.sqrt(Integer(2)) * sympy.atanh((sympy.sqrt(Integer(2)))**(Integer(-1))) * sympy.log((Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))))) + (Integer(2) * sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((sympy.sqrt(Integer(2)) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x))))))) * ((Integer(2) + (Integer(-1) * sympy.sqrt(Integer(2)))))**(Integer(-1)))))) + (Integer(-1) * (Integer(2) * sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((sympy.sqrt(Integer(2)) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x))))))) * ((Integer(2) + sympy.sqrt(Integer(2))))**(Integer(-1)))))) + (Integer(-1) * (Integer(2) * sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((sympy.sqrt(Integer(2)) * (Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) * ((Integer(2) + (Integer(-1) * sympy.sqrt(Integer(2)))))**(Integer(-1))))))) + (Integer(2) * sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), ((sympy.sqrt(Integer(2)) * (Integer(1) + sympy.sqrt((Integer(1) + sympy.sqrt((Integer(1) + x)))))) * ((Integer(2) + sympy.sqrt(Integer(2))))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=1/(sqrt(x + sqrt(x**2 + 1)) + 1),
        variable=x,
        num_steps=4,
        integral=sqrt(x + sqrt(x**2 + 1)) + log(x + sqrt(x**2 + 1))/2 - 2*log(sqrt(x + sqrt(x**2 + 1)) + 1) - 1/(2*x + 2*sqrt(x**2 + 1)) + 1/sqrt(x + sqrt(x**2 + 1)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x + 1)/(x + sqrt(sqrt(x + 1) + 1)),
        variable=x,
        num_steps=6,
        integral=2*sqrt(x + 1) + 8*sqrt(5)*atanh(sqrt(5)*(2*sqrt(sqrt(x + 1) + 1) + 1)/5)/5,
    ),
    RubiTestSuiteCase(
        integrand=1/(x - sqrt(sqrt(x + 1) + 1)),
        variable=x,
        num_steps=5,
        integral=(2 - 2*sqrt(5)/5)*log(-2*sqrt(sqrt(x + 1) + 1) + 1 + sqrt(5)) + (2*sqrt(5)/5 + 2)*log(-2*sqrt(sqrt(x + 1) + 1) - sqrt(5) + 1),
    ),
    RubiTestSuiteCase(
        integrand=x/(x + sqrt(1 - sqrt(x + 1))),
        variable=x,
        num_steps=6,
        integral=-4*sqrt(1 - sqrt(x + 1)) + (1 - sqrt(x + 1))**2 + 2*sqrt(x + 1) + 8*sqrt(5)*atanh(sqrt(5)*(2*sqrt(1 - sqrt(x + 1)) + 1)/5)/5,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x + sqrt(x + 1))/(sqrt(x + 1)*(x**2 + 1)),
        variable=x,
        num_steps=20,
        integral=I*atan((-(1 - 2*sqrt(1 + I))*sqrt(x + 1) + 2 + sqrt(1 + I))/(2*sqrt(-I + sqrt(1 + I))*sqrt(x + sqrt(x + 1))))/(2*sqrt(-(1 + I)/(-sqrt(1 + I) + I))) - I*atan((-(1 - 2*sqrt(1 - I))*sqrt(x + 1) + 2 + sqrt(1 - I))/(2*sqrt(x + sqrt(x + 1))*sqrt(sqrt(1 - I) + I)))/(2*sqrt((1 - I)/(sqrt(1 - I) + I))) + I*atanh((-(1 + 2*sqrt(1 - I))*sqrt(x + 1) + 2 - sqrt(1 - I))/(2*sqrt(-I + sqrt(1 - I))*sqrt(x + sqrt(x + 1))))/(2*sqrt(-(1 - I)/(-sqrt(1 - I) + I))) - I*atanh((-(1 + 2*sqrt(1 + I))*sqrt(x + 1) + 2 - sqrt(1 + I))/(2*sqrt(x + sqrt(x + 1))*sqrt(sqrt(1 + I) + I)))/(2*sqrt((1 + I)/(sqrt(1 + I) + I))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x + sqrt(x + 1))/(x**2 + 1),
        variable=x,
        num_steps=22,
        integral=-I*sqrt(-I + sqrt(1 + I))*atan((-(1 - 2*sqrt(1 + I))*sqrt(x + 1) + 2 + sqrt(1 + I))/(2*sqrt(-I + sqrt(1 + I))*sqrt(x + sqrt(x + 1))))/2 + I*sqrt(sqrt(1 - I) + I)*atan((-(1 - 2*sqrt(1 - I))*sqrt(x + 1) + 2 + sqrt(1 - I))/(2*sqrt(x + sqrt(x + 1))*sqrt(sqrt(1 - I) + I)))/2 + I*sqrt(-I + sqrt(1 - I))*atanh((-(1 + 2*sqrt(1 - I))*sqrt(x + 1) + 2 - sqrt(1 - I))/(2*sqrt(-I + sqrt(1 - I))*sqrt(x + sqrt(x + 1))))/2 - I*sqrt(sqrt(1 + I) + I)*atanh((-(1 + 2*sqrt(1 + I))*sqrt(x + 1) + 2 - sqrt(1 + I))/(2*sqrt(x + sqrt(x + 1))*sqrt(sqrt(1 + I) + I)))/2,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(sqrt(x) + sqrt(2*sqrt(x) + 2*x + 1) + 1),
        variable=x,
        num_steps=2,
        integral=2*sqrt(sqrt(x) + sqrt(2*sqrt(x) + 2*x + 1) + 1)*(6*x**(sympy.S(3)/2) + sqrt(x) - (2 - sqrt(x))*sqrt(2*sqrt(x) + 2*x + 1) + 2)/(15*sqrt(x)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(sqrt(x) + sqrt(2*sqrt(2)*sqrt(x) + 2*x + 2) + sqrt(2)),
        variable=x,
        num_steps=3,
        integral=2*sqrt(2)*sqrt(sqrt(x) + sqrt(2)*sqrt(sqrt(2)*sqrt(x) + x + 1) + sqrt(2))*(3*sqrt(2)*x**(sympy.S(3)/2) + sqrt(2)*sqrt(x) - sqrt(2)*(-sqrt(x) + 2*sqrt(2))*sqrt(sqrt(2)*sqrt(x) + x + 1) + 4)/(15*sqrt(x)),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x + sqrt(x + 1))/x**2,
        variable=x,
        num_steps=7,
        integral=-atan((sqrt(x + 1) + 3)/(2*sqrt(x + sqrt(x + 1))))/4 + 3*atanh((1 - 3*sqrt(x + 1))/(2*sqrt(x + sqrt(x + 1))))/4 - sqrt(x + sqrt(x + 1))/x,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(sqrt(1 + 1/x) + 1/x),
        variable=x,
        num_steps=7,
        integral=x*sqrt(sqrt(1 + 1/x) + 1/x) + atan((sqrt(1 + 1/x) + 3)/(2*sqrt(sqrt(1 + 1/x) + 1/x)))/4 - 3*atanh((1 - 3*sqrt(1 + 1/x))/(2*sqrt(sqrt(1 + 1/x) + 1/x)))/4,
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 + exp(-x))/(exp(x) - exp(-x)),
        variable=x,
        num_steps=6,
        integral=-sqrt(2)*atanh(sqrt(2)*sqrt(1 + exp(-x))/2),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(1 + exp(-x))/sinh(x),
        variable=x,
        num_steps=7,
        integral=-2*sqrt(2)*atanh(sqrt(2)*sqrt(1 + exp(-x))/2),
    ),
    RubiTestSuiteCase(
        integrand=(cos(x) + cos(3*x))**(-5),
        variable=x,
        num_steps=-45,
        integral=-tan(x)*sec(x)**3/128 - 43*tan(x)*sec(x)/256 + 1483*sqrt(2)*atanh(sqrt(2)*sin(x))/1024 - 523*atanh(sin(x))/256 - 437*sin(x)/(512 - 1024*sin(x)**2) + 203*sin(x)/(768*(1 - 2*sin(x)**2)**2) - 17*sin(x)/(192*(1 - 2*sin(x)**2)**3) + sin(x)/(32*(1 - 2*sin(x)**2)**4),
    ),
    RubiTestSuiteCase(
        integrand=(sin(x) + cos(x) + 1)**(-2),
        variable=x,
        num_steps=3,
        integral=-(-sin(x) + cos(x))/(sin(x) + cos(x) + 1) - log(tan(x/2) + 1),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(tanh(4*x) + 1),
        variable=x,
        num_steps=2,
        integral=sqrt(2)*atanh(sqrt(2)*sqrt(tanh(4*x) + 1)/2)/4,
    ),
    RubiTestSuiteCase(
        integrand=tanh(x)/sqrt(exp(2*x) + exp(x)),
        variable=x,
        num_steps=-11,
        integral=2*sqrt(exp(2*x) + exp(x))*exp(-x) + atan(((1 + 2*I)*exp(x) + I)/(2*sqrt(1 - I)*sqrt(exp(2*x) + exp(x))))/sqrt(1 - I) - atan((-(1 - 2*I)*exp(x) + I)/(2*sqrt(1 + I)*sqrt(exp(2*x) + exp(x))))/sqrt(1 + I),
    ),
    RubiTestSuiteCase(
        integrand=log(x**2 + sqrt(1 - x**2)),
        variable=x,
        num_steps=-31,
        integral=x*log(x**2 + sqrt(1 - x**2)) - 2*x - asin(x) + sqrt(sympy.S.Half + sqrt(5)/2)*atan(sqrt(2)*x/sqrt(1 + sqrt(5))) + sqrt(sympy.S.Half + sqrt(5)/2)*atan(x*sqrt(sympy.S.Half + sqrt(5)/2)/sqrt(1 - x**2)) + sqrt(sympy.S(-1)/2 + sqrt(5)/2)*atanh(sqrt(2)*x/sqrt(-1 + sqrt(5))) - sqrt(sympy.S(-1)/2 + sqrt(5)/2)*atanh(x*sqrt(sympy.S(-1)/2 + sqrt(5)/2)/sqrt(1 - x**2)),
    ),
    RubiTestSuiteCase(
        integrand=log(exp(x) + 1)/(exp(2*x) + 1),
        variable=x,
        num_steps=12,
        integral=(((Integer(-1) * (Integer(2))**(Integer(-1))) * sympy.log((((Integer(2))**(Integer(-1)) + (Integer(-1) * (sympy.I * (Integer(2))**(Integer(-1))))) * (sympy.I + (Integer(-1) * (sympy.E)**(x))))) * sympy.log((Integer(1) + (sympy.E)**(x)))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.log((((Integer(-1) * (Integer(2))**(Integer(-1))) + (Integer(-1) * (sympy.I * (Integer(2))**(Integer(-1))))) * (sympy.I + (sympy.E)**(x)))) * sympy.log((Integer(1) + (sympy.E)**(x))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * (sympy.E)**(x)))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), (((Integer(2))**(Integer(-1)) + (Integer(-1) * (sympy.I * (Integer(2))**(Integer(-1))))) * (Integer(1) + (sympy.E)**(x)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), (((Integer(2))**(Integer(-1)) + (sympy.I * (Integer(2))**(Integer(-1)))) * (Integer(1) + (sympy.E)**(x))))))),
    ),
    RubiTestSuiteCase(
        integrand=log(cosh(x)**2 + 1)**2*cosh(x),
        variable=x,
        num_steps=13,
        integral=((Integer(-8) * sympy.sqrt(Integer(2)) * sympy.atan((sympy.sinh(x) * (sympy.sqrt(Integer(2)))**(Integer(-1))))) + (Integer(4) * sympy.I * sympy.sqrt(Integer(2)) * (sympy.atan((sympy.sinh(x) * (sympy.sqrt(Integer(2)))**(Integer(-1)))))**(Integer(2))) + (Integer(8) * sympy.sqrt(Integer(2)) * sympy.atan((sympy.sinh(x) * (sympy.sqrt(Integer(2)))**(Integer(-1)))) * sympy.log(((Integer(2) * sympy.sqrt(Integer(2))) * ((sympy.sqrt(Integer(2)) + (sympy.I * sympy.sinh(x))))**(Integer(-1))))) + (Integer(4) * sympy.sqrt(Integer(2)) * sympy.atan((sympy.sinh(x) * (sympy.sqrt(Integer(2)))**(Integer(-1)))) * sympy.log((Integer(2) + (sympy.sinh(x))**(Integer(2))))) + (Integer(4) * sympy.I * sympy.sqrt(Integer(2)) * sympy.Function('PolyLog')(Integer(2), (Integer(1) + (Integer(-1) * ((Integer(2) * sympy.sqrt(Integer(2))) * ((sympy.sqrt(Integer(2)) + (sympy.I * sympy.sinh(x))))**(Integer(-1))))))) + (Integer(8) * sympy.sinh(x)) + (Integer(-1) * (Integer(4) * sympy.log((Integer(2) + (sympy.sinh(x))**(Integer(2)))) * sympy.sinh(x))) + ((sympy.log((Integer(2) + (sympy.sinh(x))**(Integer(2)))))**(Integer(2)) * sympy.sinh(x))),
    ),
    RubiTestSuiteCase(
        integrand=log(sinh(x) + cosh(x)**2)**2*cosh(x),
        variable=x,
        num_steps=28,
        integral=((Integer(-4) * sympy.sqrt(Integer(3)) * sympy.atan(((Integer(1) + (Integer(2) * sympy.sinh(x))) * (sympy.sqrt(Integer(3)))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * (Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3))))) * (sympy.log((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3)))) + (Integer(2) * sympy.sinh(x)))))**(Integer(2)))) + (Integer(-1) * ((Integer(1) + (sympy.I * sympy.sqrt(Integer(3)))) * sympy.log(((sympy.I * (Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3)))) + (Integer(2) * sympy.sinh(x)))) * ((Integer(2) * sympy.sqrt(Integer(3))))**(Integer(-1)))) * sympy.log((Integer(1) + (sympy.I * sympy.sqrt(Integer(3))) + (Integer(2) * sympy.sinh(x)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * (Integer(1) + (sympy.I * sympy.sqrt(Integer(3)))) * (sympy.log((Integer(1) + (sympy.I * sympy.sqrt(Integer(3))) + (Integer(2) * sympy.sinh(x)))))**(Integer(2)))) + (Integer(-1) * ((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3))))) * sympy.log((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3)))) + (Integer(2) * sympy.sinh(x)))) * sympy.log((Integer(-1) * ((sympy.I * (Integer(1) + (sympy.I * sympy.sqrt(Integer(3))) + (Integer(2) * sympy.sinh(x)))) * ((Integer(2) * sympy.sqrt(Integer(3))))**(Integer(-1))))))) + (Integer(-1) * (Integer(2) * sympy.log((Integer(1) + sympy.sinh(x) + (sympy.sinh(x))**(Integer(2)))))) + ((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3))))) * sympy.log((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3)))) + (Integer(2) * sympy.sinh(x)))) * sympy.log((Integer(1) + sympy.sinh(x) + (sympy.sinh(x))**(Integer(2))))) + ((Integer(1) + (sympy.I * sympy.sqrt(Integer(3)))) * sympy.log((Integer(1) + (sympy.I * sympy.sqrt(Integer(3))) + (Integer(2) * sympy.sinh(x)))) * sympy.log((Integer(1) + sympy.sinh(x) + (sympy.sinh(x))**(Integer(2))))) + (Integer(-1) * ((Integer(1) + (sympy.I * sympy.sqrt(Integer(3)))) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((sympy.I + (Integer(-1) * sympy.sqrt(Integer(3))) + (Integer(2) * sympy.I * sympy.sinh(x))) * ((Integer(2) * sympy.sqrt(Integer(3))))**(Integer(-1))))))) + (Integer(-1) * ((Integer(1) + (Integer(-1) * (sympy.I * sympy.sqrt(Integer(3))))) * sympy.Function('PolyLog')(Integer(2), ((sympy.I + sympy.sqrt(Integer(3)) + (Integer(2) * sympy.I * sympy.sinh(x))) * ((Integer(2) * sympy.sqrt(Integer(3))))**(Integer(-1)))))) + (Integer(8) * sympy.sinh(x)) + (Integer(-1) * (Integer(4) * sympy.log((Integer(1) + sympy.sinh(x) + (sympy.sinh(x))**(Integer(2)))) * sympy.sinh(x))) + ((sympy.log((Integer(1) + sympy.sinh(x) + (sympy.sinh(x))**(Integer(2)))))**(Integer(2)) * sympy.sinh(x))),
    ),
    RubiTestSuiteCase(
        integrand=log(x + sqrt(x + 1))/(x**2 + 1),
        variable=x,
        num_steps=44,
        integral=(((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log((x + sympy.sqrt((Integer(1) + x))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log((x + sympy.sqrt((Integer(1) + x)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + sympy.sqrt((Integer(1) + x)))) * sympy.log((x + sympy.sqrt((Integer(1) + x))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + sympy.sqrt((Integer(1) + x)))) * sympy.log((x + sympy.sqrt((Integer(1) + x)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log(((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I)))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + sympy.I)))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log(((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + sympy.I))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))))) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I)))) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + sympy.I)))) + sympy.sqrt(Integer(5))))**(Integer(-1))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log((sympy.sqrt((Integer(1) + sympy.I)) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + sympy.I))) + sympy.sqrt(Integer(5))))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I)))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I)))) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (sympy.sqrt((Integer(1) + sympy.I)) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + sympy.I))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (sympy.sqrt((Integer(1) + sympy.I)) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(1) + (Integer(2) * sympy.sqrt((Integer(1) + sympy.I))) + sympy.sqrt(Integer(5))))**(Integer(-1))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(2) * (sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(2) * (sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + (Integer(-1) * sympy.I))))) + sympy.sqrt(Integer(5))))**(Integer(-1))))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(2) * (sympy.sqrt((Integer(1) + sympy.I)) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + sympy.I)))) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(2) * (sympy.sqrt((Integer(1) + sympy.I)) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * (Integer(2) * sympy.sqrt((Integer(1) + sympy.I)))) + sympy.sqrt(Integer(5))))**(Integer(-1))))))),
    ),
    RubiTestSuiteCase(
        integrand=log(x + sqrt(x + 1))**2/(x + 1)**2,
        variable=x,
        num_steps=35,
        integral=(sympy.log((Integer(1) + x)) + ((Integer(2) * sympy.log((x + sympy.sqrt((Integer(1) + x))))) * (sympy.sqrt((Integer(1) + x)))**(Integer(-1))) + (Integer(-1) * (Integer(6) * sympy.log(sympy.sqrt((Integer(1) + x))) * sympy.log((x + sympy.sqrt((Integer(1) + x)))))) + (Integer(-1) * ((sympy.log((x + sympy.sqrt((Integer(1) + x)))))**(Integer(2)) * ((Integer(1) + x))**(Integer(-1)))) + (Integer(-1) * ((Integer(1) + sympy.sqrt(Integer(5))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x))))))) + (Integer(6) * sympy.log(((Integer(2))**(Integer(-1)) * (Integer(-1) + sympy.sqrt(Integer(5))))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))))) + ((Integer(3) + sympy.sqrt(Integer(5))) * sympy.log((x + sympy.sqrt((Integer(1) + x)))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * (Integer(3) + sympy.sqrt(Integer(5))) * (sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x))))))**(Integer(2)))) + (Integer(-1) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5)))) * sympy.log((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x))))))) + ((Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))) * sympy.log((x + sympy.sqrt((Integer(1) + x)))) * sympy.log((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))))) + (Integer(-1) * ((Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))) * sympy.log((Integer(-1) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(2) * sympy.sqrt(Integer(5))))**(Integer(-1))))) * sympy.log((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x))))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * (Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))) * (sympy.log((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x))))))**(Integer(2)))) + (Integer(-1) * ((Integer(3) + sympy.sqrt(Integer(5))) * sympy.log((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x))))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(2) * sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(6) * sympy.log(sympy.sqrt((Integer(1) + x))) * sympy.log((Integer(1) + ((Integer(2) * sympy.sqrt((Integer(1) + x))) * ((Integer(1) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(6) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(2) * sympy.sqrt((Integer(1) + x))) * ((Integer(1) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(-1) * ((Integer(3) + sympy.sqrt(Integer(5))) * sympy.Function('PolyLog')(Integer(2), (Integer(-1) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(2) * sympy.sqrt(Integer(5))))**(Integer(-1))))))) + (Integer(-1) * ((Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))) * sympy.Function('PolyLog')(Integer(2), ((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(2) * sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(-1) * (Integer(6) * sympy.Function('PolyLog')(Integer(2), (Integer(1) + ((Integer(2) * sympy.sqrt((Integer(1) + x))) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))))),
    ),
    RubiTestSuiteCase(
        integrand=log(x + sqrt(x + 1))/x,
        variable=x,
        num_steps=21,
        integral=((sympy.log((Integer(-1) + sympy.sqrt((Integer(1) + x)))) * sympy.log((x + sympy.sqrt((Integer(1) + x))))) + (sympy.log((Integer(1) + sympy.sqrt((Integer(1) + x)))) * sympy.log((x + sympy.sqrt((Integer(1) + x))))) + (Integer(-1) * (sympy.log((Integer(-1) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1)))))) + (Integer(-1) * (sympy.log((Integer(1) + sympy.sqrt((Integer(1) + x)))) * sympy.log((Integer(-1) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5))) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + sympy.sqrt(Integer(5))))**(Integer(-1))))))) + (Integer(-1) * (sympy.log((Integer(1) + sympy.sqrt((Integer(1) + x)))) * sympy.log((Integer(-1) * ((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))))) + (Integer(-1) * (sympy.log((Integer(-1) + sympy.sqrt((Integer(1) + x)))) * sympy.log(((Integer(1) + sympy.sqrt(Integer(5)) + (Integer(2) * sympy.sqrt((Integer(1) + x)))) * ((Integer(3) + sympy.sqrt(Integer(5))))**(Integer(-1)))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(3) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (Integer(1) + (Integer(-1) * sympy.sqrt((Integer(1) + x))))) * ((Integer(3) + sympy.sqrt(Integer(5))))**(Integer(-1))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (Integer(1) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + (Integer(-1) * sympy.sqrt(Integer(5)))))**(Integer(-1))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(2), ((Integer(2) * (Integer(1) + sympy.sqrt((Integer(1) + x)))) * ((Integer(1) + sympy.sqrt(Integer(5))))**(Integer(-1)))))),
    ),
    RubiTestSuiteCase(
        integrand=atan(2*tan(x)),
        variable=x,
        num_steps=7,
        integral=((x * sympy.atan((Integer(2) * sympy.tan(x)))) + ((Integer(2))**(Integer(-1)) * sympy.I * x * sympy.log((Integer(1) + (Integer(-1) * (Integer(3) * (sympy.E)**((Integer(2) * sympy.I * x))))))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * x * sympy.log((Integer(1) + (Integer(-1) * ((Integer(3))**(Integer(-1)) * (sympy.E)**((Integer(2) * sympy.I * x)))))))) + (Integer(-1) * ((Integer(4))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), ((Integer(3))**(Integer(-1)) * (sympy.E)**((Integer(2) * sympy.I * x)))))) + ((Integer(4))**(Integer(-1)) * sympy.Function('PolyLog')(Integer(2), (Integer(3) * (sympy.E)**((Integer(2) * sympy.I * x)))))),
    ),
    RubiTestSuiteCase(
        integrand=log(x)*atan(x)/x,
        variable=x,
        num_steps=5,
        integral=(((Integer(2))**(Integer(-1)) * sympy.I * sympy.log(x) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * x))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.log(x) * sympy.Function('PolyLog')(Integer(2), (sympy.I * x)))) + (Integer(-1) * ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * x)))) + ((Integer(2))**(Integer(-1)) * sympy.I * sympy.Function('PolyLog')(Integer(3), (sympy.I * x)))),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(x**2 + 1)*atan(x)**2,
        variable=x,
        num_steps=10,
        integral=(sympy.asinh(x) + (Integer(-1) * (sympy.sqrt((Integer(1) + (x)**(Integer(2)))) * sympy.atan(x))) + ((Integer(2))**(Integer(-1)) * x * sympy.sqrt((Integer(1) + (x)**(Integer(2)))) * (sympy.atan(x))**(Integer(2))) + (Integer(-1) * (sympy.I * sympy.atan((sympy.E)**((sympy.I * sympy.atan(x)))) * (sympy.atan(x))**(Integer(2)))) + (sympy.I * sympy.atan(x) * sympy.Function('PolyLog')(Integer(2), ((Integer(-1) * sympy.I) * (sympy.E)**((sympy.I * sympy.atan(x)))))) + (Integer(-1) * (sympy.I * sympy.atan(x) * sympy.Function('PolyLog')(Integer(2), (sympy.I * (sympy.E)**((sympy.I * sympy.atan(x))))))) + (Integer(-1) * sympy.Function('PolyLog')(Integer(3), ((Integer(-1) * sympy.I) * (sympy.E)**((sympy.I * sympy.atan(x)))))) + sympy.Function('PolyLog')(Integer(3), (sympy.I * (sympy.E)**((sympy.I * sympy.atan(x)))))),
    ),
]
