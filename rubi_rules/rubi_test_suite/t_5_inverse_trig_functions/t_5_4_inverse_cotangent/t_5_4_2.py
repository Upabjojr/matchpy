# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 5 Inverse trig functions/5.4 Inverse cotangent/5.4.2 Exponentials of inverse cotangent.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '5 Inverse trig functions/5.4 Inverse cotangent/5.4.2 Exponentials of inverse cotangent.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, c, n = symbols('a c n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=exp(acot(x)),
        variable=x,
        num_steps=2,
        integral=((x - I)/x)**(1 + I/2)*((x + I)/x)**(-1 - I/2)*(sympy.S(4)/5 + 8*I/5)*hyper((2, 1 + I/2), (2 + I/2,), (1 - I/x)/(1 + I/x)),
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a),
        variable=x,
        num_steps=1,
        integral=-exp(acot(x))/a,
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a)**2,
        variable=x,
        num_steps=2,
        integral=-(1 - 2*x)*exp(acot(x))/(5*a**2*(x**2 + 1)) - 2*exp(acot(x))/(5*a**2),
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a)**3,
        variable=x,
        num_steps=3,
        integral=-(1 - 4*x)*exp(acot(x))/(17*a**3*(x**2 + 1)**2) - 12*(1 - 2*x)*exp(acot(x))/(85*a**3*(x**2 + 1)) - 24*exp(acot(x))/(85*a**3),
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a)**(sympy.S(3)/2),
        variable=x,
        num_steps=1,
        integral=-(1 - x)*exp(acot(x))/(2*a*sqrt(a*x**2 + a)),
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a)**(sympy.S(5)/2),
        variable=x,
        num_steps=2,
        integral=-(1 - 3*x)*exp(acot(x))/(10*a*(a*x**2 + a)**(sympy.S(3)/2)) - 3*(1 - x)*exp(acot(x))/(10*a**2*sqrt(a*x**2 + a)),
    ),
    RubiTestSuiteCase(
        integrand=exp(acot(x))/(a*x**2 + a)**(sympy.S(7)/2),
        variable=x,
        num_steps=3,
        integral=-(1 - 5*x)*exp(acot(x))/(26*a*(a*x**2 + a)**(sympy.S(5)/2)) - (1 - 3*x)*exp(acot(x))/(13*a**2*(a*x**2 + a)**(sympy.S(3)/2)) - 3*(1 - x)*exp(acot(x))/(13*a**3*sqrt(a*x**2 + a)),
    ),
    RubiTestSuiteCase(
        integrand=exp(n*acot(a*x))/(a**2*c*x**2 + c)**(sympy.S(1)/3),
        variable=x,
        num_steps=3,
        integral=3*x*((a - I/x)/(a + I/x))**(-I*n/2 + sympy.S(1)/3)*(1 + 1/(a**2*x**2))**(sympy.S(1)/3)*(1 - I/(a*x))**(I*n/2 + sympy.S(-1)/3)*(1 + I/(a*x))**(-I*n/2 + sympy.S(2)/3)*hyper((sympy.S(-1)/3, -I*n/2 + sympy.S(1)/3), (sympy.S(2)/3,), 2*I/(x*(a + I/x)))/(a**2*c*x**2 + c)**(sympy.S(1)/3),
    ),
    RubiTestSuiteCase(
        integrand=exp(n*acot(a*x))/(a**2*c*x**2 + c)**(sympy.S(2)/3),
        variable=x,
        num_steps=3,
        integral=-3*x*((a - I/x)/(a + I/x))**(-I*n/2 + sympy.S(2)/3)*(1 + 1/(a**2*x**2))**(sympy.S(2)/3)*(1 - I/(a*x))**(I*n/2 + sympy.S(-2)/3)*(1 + I/(a*x))**(-I*n/2 + sympy.S(1)/3)*hyper((sympy.S(1)/3, -I*n/2 + sympy.S(2)/3), (sympy.S(4)/3,), 2*I/(x*(a + I/x)))/(a**2*c*x**2 + c)**(sympy.S(2)/3),
    ),
    RubiTestSuiteCase(
        integrand=exp(n*acot(a*x))/(a**2*c*x**2 + c)**(sympy.S(4)/3),
        variable=x,
        num_steps=4,
        integral=-6*x*((a - I/x)/(a + I/x))**(-I*n/2 + sympy.S(1)/3)*(1 + 1/(a**2*x**2))**(sympy.S(1)/3)*(1 - I/(a*x))**(I*n/2 + sympy.S(-1)/3)*(1 + I/(a*x))**(-I*n/2 + sympy.S(2)/3)*hyper((sympy.S(-1)/3, -I*n/2 + sympy.S(1)/3), (sympy.S(2)/3,), 2*I/(x*(a + I/x)))/(c*(9*n**2 + 4)*(a**2*c*x**2 + c)**(sympy.S(1)/3)) - 3*(-2*a*x + 3*n)*exp(n*acot(a*x))/(a*c*(9*n**2 + 4)*(a**2*c*x**2 + c)**(sympy.S(1)/3)),
    ),
    RubiTestSuiteCase(
        integrand=exp(n*acot(a*x))/(a**2*c*x**2 + c)**(sympy.S(5)/3),
        variable=x,
        num_steps=4,
        integral=-12*x*((a - I/x)/(a + I/x))**(-I*n/2 + sympy.S(2)/3)*(1 + 1/(a**2*x**2))**(sympy.S(2)/3)*(1 - I/(a*x))**(I*n/2 + sympy.S(-2)/3)*(1 + I/(a*x))**(-I*n/2 + sympy.S(1)/3)*hyper((sympy.S(1)/3, -I*n/2 + sympy.S(2)/3), (sympy.S(4)/3,), 2*I/(x*(a + I/x)))/(c*(9*n**2 + 16)*(a**2*c*x**2 + c)**(sympy.S(2)/3)) - 3*(-4*a*x + 3*n)*exp(n*acot(a*x))/(a*c*(9*n**2 + 16)*(a**2*c*x**2 + c)**(sympy.S(2)/3)),
    ),
    RubiTestSuiteCase(
        integrand=exp(n*acot(a*x))/(a**2*c*x**2 + c)**(sympy.S(7)/3),
        variable=x,
        num_steps=5,
        integral=-240*x*((a - I/x)/(a + I/x))**(-I*n/2 + sympy.S(1)/3)*(1 + 1/(a**2*x**2))**(sympy.S(1)/3)*(1 - I/(a*x))**(I*n/2 + sympy.S(-1)/3)*(1 + I/(a*x))**(-I*n/2 + sympy.S(2)/3)*hyper((sympy.S(-1)/3, -I*n/2 + sympy.S(1)/3), (sympy.S(2)/3,), 2*I/(x*(a + I/x)))/(c**2*(9*n**2 + 4)*(9*n**2 + 64)*(a**2*c*x**2 + c)**(sympy.S(1)/3)) - 3*(-8*a*x + 3*n)*exp(n*acot(a*x))/(a*c*(9*n**2 + 64)*(a**2*c*x**2 + c)**(sympy.S(4)/3)) - 120*(-2*a*x + 3*n)*exp(n*acot(a*x))/(a*c**2*(9*n**2 + 4)*(9*n**2 + 64)*(a**2*c*x**2 + c)**(sympy.S(1)/3)),
    ),
]
