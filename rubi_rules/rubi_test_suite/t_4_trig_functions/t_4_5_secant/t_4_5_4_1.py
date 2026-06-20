# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.5 Secant/4.5.4.1 (a+b sec)^m (A+B sec+C sec^2).m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.5 Secant/4.5.4.1 (a+b sec)^m (A+B sec+C sec^2).m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
A, B, C, b, c, d, e, f, m = symbols('A B C b c d e f m')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x)**6,
        variable=x,
        num_steps=3,
        integral=C*tan(c + d*x)*sec(c + d*x)**6/(7*d) + (7*A + 6*C)*tan(c + d*x)**5/(35*d) + (7*A + 6*C)*tan(c + d*x)/(7*d) + (14*A + 12*C)*tan(c + d*x)**3/(21*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x)**5,
        variable=x,
        num_steps=4,
        integral=C*tan(c + d*x)*sec(c + d*x)**5/(6*d) + (6*A + 5*C)*tan(c + d*x)*sec(c + d*x)**3/(24*d) + (6*A + 5*C)*tan(c + d*x)*sec(c + d*x)/(16*d) + (6*A + 5*C)*atanh(sin(c + d*x))/(16*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=C*tan(c + d*x)*sec(c + d*x)**4/(5*d) + (5*A + 4*C)*tan(c + d*x)**3/(15*d) + (5*A + 4*C)*tan(c + d*x)/(5*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x)**3,
        variable=x,
        num_steps=3,
        integral=C*tan(c + d*x)*sec(c + d*x)**3/(4*d) + (4*A + 3*C)*tan(c + d*x)*sec(c + d*x)/(8*d) + (4*A + 3*C)*atanh(sin(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=C*tan(c + d*x)*sec(c + d*x)**2/(3*d) + (3*A + 2*C)*tan(c + d*x)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*sec(c + d*x),
        variable=x,
        num_steps=2,
        integral=C*tan(c + d*x)*sec(c + d*x)/(2*d) + (2*A + C)*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=A + C*sec(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=A*x + C*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x),
        variable=x,
        num_steps=2,
        integral=A*sin(c + d*x)/d + C*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x)**2,
        variable=x,
        num_steps=2,
        integral=A*sin(c + d*x)*cos(c + d*x)/(2*d) + x*(A/2 + C),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x)**3,
        variable=x,
        num_steps=3,
        integral=-A*sin(c + d*x)**3/(3*d) + (A + C)*sin(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=A*sin(c + d*x)*cos(c + d*x)**3/(4*d) + x*(3*A/8 + C/2) + (3*A + 4*C)*sin(c + d*x)*cos(c + d*x)/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x)**5,
        variable=x,
        num_steps=4,
        integral=A*sin(c + d*x)**5/(5*d) + (A + C)*sin(c + d*x)/d - (2*A + C)*sin(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)*cos(c + d*x)**6,
        variable=x,
        num_steps=4,
        integral=A*sin(c + d*x)*cos(c + d*x)**5/(6*d) + x*(5*A/16 + 3*C/8) + (5*A + 6*C)*sin(c + d*x)*cos(c + d*x)**3/(24*d) + (5*A + 6*C)*sin(c + d*x)*cos(c + d*x)/(16*d),
    ),
    RubiTestSuiteCase(
        integrand=(-C*m/(m + 1) + C*sec(c + d*x)**2)*sec(c + d*x)**m,
        variable=x,
        num_steps=1,
        integral=C*sin(c + d*x)*sec(c + d*x)**(m + 1)/(d*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(A - A*(m + 1)*sec(c + d*x)**2/m)*sec(c + d*x)**m,
        variable=x,
        num_steps=1,
        integral=-A*sin(c + d*x)*sec(c + d*x)**(m + 1)/(d*m),
    ),
    RubiTestSuiteCase(
        integrand=(b*sec(c + d*x))**(sympy.S(5)/2)*(A + C*sec(c + d*x)**2),
        variable=x,
        num_steps=4,
        integral=2*C*(b*sec(c + d*x))**(sympy.S(5)/2)*tan(c + d*x)/(7*d) + 2*b**2*sqrt(b*sec(c + d*x))*(7*A + 5*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(21*d) + 2*b*(b*sec(c + d*x))**(sympy.S(3)/2)*(7*A + 5*C)*sin(c + d*x)/(21*d),
    ),
    RubiTestSuiteCase(
        integrand=(b*sec(c + d*x))**(sympy.S(3)/2)*(A + C*sec(c + d*x)**2),
        variable=x,
        num_steps=4,
        integral=2*C*(b*sec(c + d*x))**(sympy.S(3)/2)*tan(c + d*x)/(5*d) - 2*b**2*(5*A + 3*C)*elliptic_e(c/2 + d*x/2, 2)/(5*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*b*sqrt(b*sec(c + d*x))*(5*A + 3*C)*sin(c + d*x)/(5*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(b*sec(c + d*x))*(A + C*sec(c + d*x)**2),
        variable=x,
        num_steps=3,
        integral=2*C*sqrt(b*sec(c + d*x))*tan(c + d*x)/(3*d) + sqrt(b*sec(c + d*x))*(6*A + 2*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)/sqrt(b*sec(c + d*x)),
        variable=x,
        num_steps=3,
        integral=2*C*tan(c + d*x)/(d*sqrt(b*sec(c + d*x))) + (2*A - 2*C)*elliptic_e(c/2 + d*x/2, 2)/(d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=3,
        integral=2*A*tan(c + d*x)/(3*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + sqrt(b*sec(c + d*x))*(2*A + 6*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*b**2*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=3,
        integral=2*A*tan(c + d*x)/(5*d*(b*sec(c + d*x))**(sympy.S(5)/2)) + (6*A + 10*C)*elliptic_e(c/2 + d*x/2, 2)/(5*b**2*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(7)/2),
        variable=x,
        num_steps=4,
        integral=2*A*tan(c + d*x)/(7*d*(b*sec(c + d*x))**(sympy.S(7)/2)) + (10*A + 14*C)*sin(c + d*x)/(21*b**3*d*sqrt(b*sec(c + d*x))) + sqrt(b*sec(c + d*x))*(10*A + 14*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(21*b**4*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(9)/2),
        variable=x,
        num_steps=4,
        integral=2*A*tan(c + d*x)/(9*d*(b*sec(c + d*x))**(sympy.S(9)/2)) + (14*A + 18*C)*sin(c + d*x)/(45*b**3*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + (14*A + 18*C)*elliptic_e(c/2 + d*x/2, 2)/(15*b**4*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(3*sec(c + d*x)**2 + 3)/sqrt(sec(c + d*x)),
        variable=x,
        num_steps=1,
        integral=6*sin(c + d*x)*sqrt(sec(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(m - (m + 1)*sec(e + f*x)**2)*sec(e + f*x)**m,
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)*sec(e + f*x)**(m + 1)/f,
    ),
    RubiTestSuiteCase(
        integrand=(5 - 6*sec(e + f*x)**2)*sec(e + f*x)**5,
        variable=x,
        num_steps=1,
        integral=-tan(e + f*x)*sec(e + f*x)**5/f,
    ),
    RubiTestSuiteCase(
        integrand=(4 - 5*sec(e + f*x)**2)*sec(e + f*x)**4,
        variable=x,
        num_steps=1,
        integral=-tan(e + f*x)*sec(e + f*x)**4/f,
    ),
    RubiTestSuiteCase(
        integrand=(3 - 4*sec(e + f*x)**2)*sec(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=-tan(e + f*x)*sec(e + f*x)**3/f,
    ),
    RubiTestSuiteCase(
        integrand=(2 - 3*sec(e + f*x)**2)*sec(e + f*x)**2,
        variable=x,
        num_steps=1,
        integral=-tan(e + f*x)*sec(e + f*x)**2/f,
    ),
    RubiTestSuiteCase(
        integrand=(1 - 2*sec(e + f*x)**2)*sec(e + f*x),
        variable=x,
        num_steps=1,
        integral=-tan(e + f*x)*sec(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=-sec(e + f*x)**2,
        variable=x,
        num_steps=2,
        integral=-tan(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=-cos(e + f*x),
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(sec(e + f*x)**2 - 2)*cos(e + f*x)**2,
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)*cos(e + f*x)/f,
    ),
    RubiTestSuiteCase(
        integrand=(2*sec(e + f*x)**2 - 3)*cos(e + f*x)**3,
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)*cos(e + f*x)**2/f,
    ),
    RubiTestSuiteCase(
        integrand=(3*sec(e + f*x)**2 - 4)*cos(e + f*x)**4,
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)*cos(e + f*x)**3/f,
    ),
    RubiTestSuiteCase(
        integrand=(4*sec(e + f*x)**2 - 5)*cos(e + f*x)**5,
        variable=x,
        num_steps=1,
        integral=-sin(e + f*x)*cos(e + f*x)**4/f,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=B*tan(c + d*x)**3/(3*d) + B*tan(c + d*x)/d + C*tan(c + d*x)*sec(c + d*x)**3/(4*d) + 3*C*tan(c + d*x)*sec(c + d*x)/(8*d) + 3*C*atanh(sin(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x)**2,
        variable=x,
        num_steps=6,
        integral=B*tan(c + d*x)*sec(c + d*x)/(2*d) + B*atanh(sin(c + d*x))/(2*d) + C*tan(c + d*x)**3/(3*d) + C*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x),
        variable=x,
        num_steps=6,
        integral=B*tan(c + d*x)/d + C*tan(c + d*x)*sec(c + d*x)/(2*d) + C*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=B*sec(c + d*x) + C*sec(c + d*x)**2,
        variable=x,
        num_steps=4,
        integral=B*atanh(sin(c + d*x))/d + C*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x),
        variable=x,
        num_steps=4,
        integral=B*x + C*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=B*sin(c + d*x)/d + C*x,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**3,
        variable=x,
        num_steps=5,
        integral=B*x/2 + B*sin(c + d*x)*cos(c + d*x)/(2*d) + C*sin(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**4,
        variable=x,
        num_steps=6,
        integral=-B*sin(c + d*x)**3/(3*d) + B*sin(c + d*x)/d + C*x/2 + C*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**5,
        variable=x,
        num_steps=7,
        integral=3*B*x/8 + B*sin(c + d*x)*cos(c + d*x)**3/(4*d) + 3*B*sin(c + d*x)*cos(c + d*x)/(8*d) - C*sin(c + d*x)**3/(3*d) + C*sin(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**6,
        variable=x,
        num_steps=7,
        integral=B*sin(c + d*x)**5/(5*d) - 2*B*sin(c + d*x)**3/(3*d) + B*sin(c + d*x)/d + 3*C*x/8 + C*sin(c + d*x)*cos(c + d*x)**3/(4*d) + 3*C*sin(c + d*x)*cos(c + d*x)/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(b*sec(c + d*x))**(sympy.S(3)/2)*(B*sec(c + d*x) + C*sec(c + d*x)**2),
        variable=x,
        num_steps=10,
        integral=2*B*b*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*d) + 2*B*(b*sec(c + d*x))**(sympy.S(3)/2)*sin(c + d*x)/(3*d) - 6*C*b**2*elliptic_e(c/2 + d*x/2, 2)/(5*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 6*C*b*sqrt(b*sec(c + d*x))*sin(c + d*x)/(5*d) + 2*C*(b*sec(c + d*x))**(sympy.S(5)/2)*sin(c + d*x)/(5*b*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(b*sec(c + d*x))*(B*sec(c + d*x) + C*sec(c + d*x)**2),
        variable=x,
        num_steps=9,
        integral=-2*B*b*elliptic_e(c/2 + d*x/2, 2)/(d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*B*sqrt(b*sec(c + d*x))*sin(c + d*x)/d + 2*C*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*d) + 2*C*(b*sec(c + d*x))**(sympy.S(3)/2)*sin(c + d*x)/(3*b*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)/sqrt(b*sec(c + d*x)),
        variable=x,
        num_steps=8,
        integral=2*B*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(b*d) - 2*C*elliptic_e(c/2 + d*x/2, 2)/(d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*C*sqrt(b*sec(c + d*x))*sin(c + d*x)/(b*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=7,
        integral=2*B*elliptic_e(c/2 + d*x/2, 2)/(b*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*C*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(b**2*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=8,
        integral=2*B*sin(c + d*x)/(3*b**2*d*sqrt(b*sec(c + d*x))) + 2*B*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*b**3*d) + 2*C*elliptic_e(c/2 + d*x/2, 2)/(b**2*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(7)/2),
        variable=x,
        num_steps=9,
        integral=2*B*sin(c + d*x)/(5*b**2*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + 6*B*elliptic_e(c/2 + d*x/2, 2)/(5*b**3*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*C*sin(c + d*x)/(3*b**3*d*sqrt(b*sec(c + d*x))) + 2*C*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*b**4*d),
    ),
    RubiTestSuiteCase(
        integrand=(B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(9)/2),
        variable=x,
        num_steps=10,
        integral=2*B*sin(c + d*x)/(7*b**2*d*(b*sec(c + d*x))**(sympy.S(5)/2)) + 10*B*sin(c + d*x)/(21*b**4*d*sqrt(b*sec(c + d*x))) + 10*B*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(21*b**5*d) + 2*C*sin(c + d*x)/(5*b**3*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + 6*C*elliptic_e(c/2 + d*x/2, 2)/(5*b**4*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x)**4,
        variable=x,
        num_steps=7,
        integral=B*tan(c + d*x)*sec(c + d*x)**3/(4*d) + 3*B*tan(c + d*x)*sec(c + d*x)/(8*d) + 3*B*atanh(sin(c + d*x))/(8*d) + C*tan(c + d*x)*sec(c + d*x)**4/(5*d) + (5*A + 4*C)*tan(c + d*x)**3/(15*d) + (5*A + 4*C)*tan(c + d*x)/(5*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x)**3,
        variable=x,
        num_steps=6,
        integral=B*tan(c + d*x)**3/(3*d) + B*tan(c + d*x)/d + C*tan(c + d*x)*sec(c + d*x)**3/(4*d) + (4*A + 3*C)*tan(c + d*x)*sec(c + d*x)/(8*d) + (4*A + 3*C)*atanh(sin(c + d*x))/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x)**2,
        variable=x,
        num_steps=6,
        integral=B*tan(c + d*x)*sec(c + d*x)/(2*d) + B*atanh(sin(c + d*x))/(2*d) + C*tan(c + d*x)*sec(c + d*x)**2/(3*d) + (3*A + 2*C)*tan(c + d*x)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*sec(c + d*x),
        variable=x,
        num_steps=5,
        integral=B*tan(c + d*x)/d + C*tan(c + d*x)*sec(c + d*x)/(2*d) + (2*A + C)*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=A + B*sec(c + d*x) + C*sec(c + d*x)**2,
        variable=x,
        num_steps=4,
        integral=A*x + B*atanh(sin(c + d*x))/d + C*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x),
        variable=x,
        num_steps=4,
        integral=A*sin(c + d*x)/d + B*x + C*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**2,
        variable=x,
        num_steps=4,
        integral=A*sin(c + d*x)*cos(c + d*x)/(2*d) + B*sin(c + d*x)/d + x*(A/2 + C),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**3,
        variable=x,
        num_steps=6,
        integral=-A*sin(c + d*x)**3/(3*d) + B*x/2 + B*sin(c + d*x)*cos(c + d*x)/(2*d) + (A + C)*sin(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**4,
        variable=x,
        num_steps=6,
        integral=A*sin(c + d*x)*cos(c + d*x)**3/(4*d) - B*sin(c + d*x)**3/(3*d) + B*sin(c + d*x)/d + x*(3*A/8 + C/2) + (3*A + 4*C)*sin(c + d*x)*cos(c + d*x)/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**5,
        variable=x,
        num_steps=8,
        integral=A*sin(c + d*x)**5/(5*d) + 3*B*x/8 + B*sin(c + d*x)*cos(c + d*x)**3/(4*d) + 3*B*sin(c + d*x)*cos(c + d*x)/(8*d) + (A + C)*sin(c + d*x)/d - (2*A + C)*sin(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)*cos(c + d*x)**6,
        variable=x,
        num_steps=7,
        integral=A*sin(c + d*x)*cos(c + d*x)**5/(6*d) + B*sin(c + d*x)**5/(5*d) - 2*B*sin(c + d*x)**3/(3*d) + B*sin(c + d*x)/d + x*(5*A/16 + 3*C/8) + (5*A + 6*C)*sin(c + d*x)*cos(c + d*x)**3/(24*d) + (5*A + 6*C)*sin(c + d*x)*cos(c + d*x)/(16*d),
    ),
    RubiTestSuiteCase(
        integrand=(b*sec(c + d*x))**(sympy.S(3)/2)*(A + B*sec(c + d*x) + C*sec(c + d*x)**2),
        variable=x,
        num_steps=8,
        integral=2*B*b*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*d) + 2*B*(b*sec(c + d*x))**(sympy.S(3)/2)*sin(c + d*x)/(3*d) + 2*C*(b*sec(c + d*x))**(sympy.S(3)/2)*tan(c + d*x)/(5*d) - 2*b**2*(5*A + 3*C)*elliptic_e(c/2 + d*x/2, 2)/(5*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*b*sqrt(b*sec(c + d*x))*(5*A + 3*C)*sin(c + d*x)/(5*d),
    ),
    RubiTestSuiteCase(
        integrand=sqrt(b*sec(c + d*x))*(A + B*sec(c + d*x) + C*sec(c + d*x)**2),
        variable=x,
        num_steps=7,
        integral=-2*B*b*elliptic_e(c/2 + d*x/2, 2)/(d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + 2*B*sqrt(b*sec(c + d*x))*sin(c + d*x)/d + 2*C*sqrt(b*sec(c + d*x))*tan(c + d*x)/(3*d) + sqrt(b*sec(c + d*x))*(6*A + 2*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)/sqrt(b*sec(c + d*x)),
        variable=x,
        num_steps=6,
        integral=2*B*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(b*d) + 2*C*tan(c + d*x)/(d*sqrt(b*sec(c + d*x))) + (2*A - 2*C)*elliptic_e(c/2 + d*x/2, 2)/(d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(3)/2),
        variable=x,
        num_steps=6,
        integral=2*A*tan(c + d*x)/(3*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + 2*B*elliptic_e(c/2 + d*x/2, 2)/(b*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + sqrt(b*sec(c + d*x))*(2*A + 6*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*b**2*d),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(5)/2),
        variable=x,
        num_steps=7,
        integral=2*A*tan(c + d*x)/(5*d*(b*sec(c + d*x))**(sympy.S(5)/2)) + 2*B*sin(c + d*x)/(3*b**2*d*sqrt(b*sec(c + d*x))) + 2*B*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(3*b**3*d) + (6*A + 10*C)*elliptic_e(c/2 + d*x/2, 2)/(5*b**2*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))),
    ),
    RubiTestSuiteCase(
        integrand=(A + B*sec(c + d*x) + C*sec(c + d*x)**2)/(b*sec(c + d*x))**(sympy.S(7)/2),
        variable=x,
        num_steps=8,
        integral=2*A*tan(c + d*x)/(7*d*(b*sec(c + d*x))**(sympy.S(7)/2)) + 2*B*sin(c + d*x)/(5*b**2*d*(b*sec(c + d*x))**(sympy.S(3)/2)) + 6*B*elliptic_e(c/2 + d*x/2, 2)/(5*b**3*d*sqrt(b*sec(c + d*x))*sqrt(cos(c + d*x))) + (10*A + 14*C)*sin(c + d*x)/(21*b**3*d*sqrt(b*sec(c + d*x))) + sqrt(b*sec(c + d*x))*(10*A + 14*C)*sqrt(cos(c + d*x))*elliptic_f(c/2 + d*x/2, 2)/(21*b**4*d),
    ),
]
