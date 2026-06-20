# -*- coding: utf-8 -*-
"""Generated from MathematicaSyntaxTestSuite.

Source: 4 Trig functions/4.3 Tangent/4.3.1.3 (d sin)^m (a+b tan)^n.m
"""

from sympy import *
import sympy

from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase

SOURCE_FILE = '4 Trig functions/4.3 Tangent/4.3.1.3 (d sin)^m (a+b tan)^n.m'

# Free symbols used by round-trippable string expressions.
x = symbols('x')

# Free symbols used by round-trippable string expressions.
a, b, c, d, m, n = symbols('a b c d m n')

# Third tuple element: number of Rubi integration steps used.
TEST_CASES = [
    RubiTestSuiteCase(
        integrand=sin(x)**4/(tan(x) + I),
        variable=x,
        num_steps=5,
        integral=-I*x/16 - 3*I/(16*tan(x) + 16*I) - 5/(32*(tan(x) + I)**2) + I/(24*(tan(x) + I)**3) - 1/(32*(-tan(x) + I)**2) - I/(-8*tan(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**3/(tan(x) + I),
        variable=x,
        num_steps=9,
        integral=sin(x)**5/5 - I*cos(x)**5/5 + I*cos(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=sin(x)**2/(tan(x) + I),
        variable=x,
        num_steps=5,
        integral=-I*x/8 - I/(4*tan(x) + 4*I) - 1/(8*(tan(x) + I)**2) - I/(-8*tan(x) + 8*I),
    ),
    RubiTestSuiteCase(
        integrand=sin(x)/(tan(x) + I),
        variable=x,
        num_steps=8,
        integral=sin(x)**3/3 + I*cos(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(tan(x) + I),
        variable=x,
        num_steps=8,
        integral=sin(x) - I*cos(x) + I*atanh(cos(x)),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**2/(tan(x) + I),
        variable=x,
        num_steps=3,
        integral=I*x + log(cos(x)) + log(tan(x)) + I*cot(x),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**3/(tan(x) + I),
        variable=x,
        num_steps=8,
        integral=I*cot(x)*csc(x)/2 - I*atanh(cos(x))/2 - csc(x),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**4/(tan(x) + I),
        variable=x,
        num_steps=4,
        integral=I*cot(x)**3/3 - cot(x)**2/2,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**5/(tan(x) + I),
        variable=x,
        num_steps=9,
        integral=I*cot(x)*csc(x)**3/4 - I*cot(x)*csc(x)/8 - I*atanh(cos(x))/8 - csc(x)**3/3,
    ),
    RubiTestSuiteCase(
        integrand=csc(x)**6/(tan(x) + I),
        variable=x,
        num_steps=4,
        integral=I*cot(x)**5/5 - cot(x)**4/4 + I*cot(x)**3/3 - cot(x)**2/2,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x)**5,
        variable=x,
        num_steps=8,
        integral=-a*cos(c + d*x)**5/(5*d) + 2*a*cos(c + d*x)**3/(3*d) - a*cos(c + d*x)/d - b*sin(c + d*x)**5/(5*d) - b*sin(c + d*x)**3/(3*d) - b*sin(c + d*x)/d + b*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x)**4,
        variable=x,
        num_steps=6,
        integral=3*a*x/8 - b*log(cos(c + d*x))/d - (a + b*tan(c + d*x))*sin(c + d*x)**3*cos(c + d*x)/(4*d) - (3*a + 4*b*tan(c + d*x))*sin(c + d*x)*cos(c + d*x)/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x)**3,
        variable=x,
        num_steps=8,
        integral=a*cos(c + d*x)**3/(3*d) - a*cos(c + d*x)/d - b*sin(c + d*x)**3/(3*d) - b*sin(c + d*x)/d + b*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x)**2,
        variable=x,
        num_steps=5,
        integral=a*x/2 - b*log(cos(c + d*x))/d - (a + b*tan(c + d*x))*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x),
        variable=x,
        num_steps=6,
        integral=-a*cos(c + d*x)/d - b*sin(c + d*x)/d + b*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x),
        variable=x,
        num_steps=4,
        integral=-a*atanh(cos(c + d*x))/d + b*atanh(sin(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-a*cot(c + d*x)/d + b*log(tan(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x)**3,
        variable=x,
        num_steps=7,
        integral=-a*cot(c + d*x)*csc(c + d*x)/(2*d) - a*atanh(cos(c + d*x))/(2*d) + b*atanh(sin(c + d*x))/d - b*csc(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=-a*cot(c + d*x)**3/(3*d) - a*cot(c + d*x)/d + b*log(tan(c + d*x))/d - b*cot(c + d*x)**2/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x)**5,
        variable=x,
        num_steps=9,
        integral=-a*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 3*a*cot(c + d*x)*csc(c + d*x)/(8*d) - 3*a*atanh(cos(c + d*x))/(8*d) + b*atanh(sin(c + d*x))/d - b*csc(c + d*x)**3/(3*d) - b*csc(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*csc(c + d*x)**6,
        variable=x,
        num_steps=3,
        integral=-a*cot(c + d*x)**5/(5*d) - 2*a*cot(c + d*x)**3/(3*d) - a*cot(c + d*x)/d + b*log(tan(c + d*x))/d - b*cot(c + d*x)**4/(4*d) - b*cot(c + d*x)**2/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*sin(c + d*x)**4,
        variable=x,
        num_steps=8,
        integral=-2*a*b*log(cos(c + d*x))/d + b**2*tan(c + d*x)/d + x*(3*a**2/8 - 15*b**2/8) + (a + b*tan(c + d*x))**2*sin(c + d*x)*cos(c + d*x)**3/(4*d) + (a + b*tan(c + d*x))*(-5*a*tan(c + d*x) + 7*b)*cos(c + d*x)**2/(8*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*sin(c + d*x)**3,
        variable=x,
        num_steps=11,
        integral=a**2*cos(c + d*x)**3/(3*d) - a**2*cos(c + d*x)/d - 2*a*b*sin(c + d*x)**3/(3*d) - 2*a*b*sin(c + d*x)/d + 2*a*b*atanh(sin(c + d*x))/d - b**2*cos(c + d*x)**3/(3*d) + 2*b**2*cos(c + d*x)/d + b**2*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*sin(c + d*x)**2,
        variable=x,
        num_steps=6,
        integral=-2*a*b*log(cos(c + d*x))/d + 3*b**2*tan(c + d*x)/(2*d) + x*(a**2/2 - 3*b**2/2) - (a + b*tan(c + d*x))**2*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*sin(c + d*x),
        variable=x,
        num_steps=9,
        integral=-a**2*cos(c + d*x)/d - 2*a*b*sin(c + d*x)/d + 2*a*b*atanh(sin(c + d*x))/d + b**2*cos(c + d*x)/d + b**2*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x),
        variable=x,
        num_steps=6,
        integral=-a**2*atanh(cos(c + d*x))/d + 2*a*b*atanh(sin(c + d*x))/d + b**2*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-a**2*cot(c + d*x)/d + 2*a*b*log(tan(c + d*x))/d + b**2*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x)**3,
        variable=x,
        num_steps=10,
        integral=-a**2*cot(c + d*x)*csc(c + d*x)/(2*d) - a**2*atanh(cos(c + d*x))/(2*d) + 2*a*b*atanh(sin(c + d*x))/d - 2*a*b*csc(c + d*x)/d - b**2*atanh(cos(c + d*x))/d + b**2*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=-a**2*cot(c + d*x)**3/(3*d) + 2*a*b*log(tan(c + d*x))/d - a*b*cot(c + d*x)**2/d + b**2*tan(c + d*x)/d - (a**2 + b**2)*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x)**5,
        variable=x,
        num_steps=13,
        integral=-a**2*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 3*a**2*cot(c + d*x)*csc(c + d*x)/(8*d) - 3*a**2*atanh(cos(c + d*x))/(8*d) + 2*a*b*atanh(sin(c + d*x))/d - 2*a*b*csc(c + d*x)**3/(3*d) - 2*a*b*csc(c + d*x)/d - 3*b**2*atanh(cos(c + d*x))/(2*d) - b**2*csc(c + d*x)**2*sec(c + d*x)/(2*d) + 3*b**2*sec(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*csc(c + d*x)**6,
        variable=x,
        num_steps=3,
        integral=-a**2*cot(c + d*x)**5/(5*d) + 2*a*b*log(tan(c + d*x))/d - a*b*cot(c + d*x)**4/(2*d) - 2*a*b*cot(c + d*x)**2/d + b**2*tan(c + d*x)/d - (a**2 + 2*b**2)*cot(c + d*x)/d - (2*a**2 + b**2)*cot(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*sin(c + d*x)**3,
        variable=x,
        num_steps=16,
        integral=a**3*cos(c + d*x)**3/(3*d) - a**3*cos(c + d*x)/d - a**2*b*sin(c + d*x)**3/d - 3*a**2*b*sin(c + d*x)/d + 3*a**2*b*atanh(sin(c + d*x))/d - a*b**2*cos(c + d*x)**3/d + 6*a*b**2*cos(c + d*x)/d + 3*a*b**2*sec(c + d*x)/d + b**3*sin(c + d*x)**3*tan(c + d*x)**2/(2*d) + 5*b**3*sin(c + d*x)**3/(6*d) + 5*b**3*sin(c + d*x)/(2*d) - 5*b**3*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*sin(c + d*x)**2,
        variable=x,
        num_steps=7,
        integral=9*a*b**2*tan(c + d*x)/(2*d) + a*x*(a**2 - 9*b**2)/2 + b**3*tan(c + d*x)**2/d - b*(3*a**2 - 2*b**2)*log(cos(c + d*x))/d - (a + b*tan(c + d*x))**3*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*sin(c + d*x),
        variable=x,
        num_steps=13,
        integral=-a**3*cos(c + d*x)/d - 3*a**2*b*sin(c + d*x)/d + 3*a**2*b*atanh(sin(c + d*x))/d + 3*a*b**2*cos(c + d*x)/d + 3*a*b**2*sec(c + d*x)/d + b**3*sin(c + d*x)*tan(c + d*x)**2/(2*d) + 3*b**3*sin(c + d*x)/(2*d) - 3*b**3*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x),
        variable=x,
        num_steps=8,
        integral=-a**3*atanh(cos(c + d*x))/d + 3*a**2*b*atanh(sin(c + d*x))/d + 3*a*b**2*sec(c + d*x)/d + b**3*tan(c + d*x)*sec(c + d*x)/(2*d) - b**3*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-a**3*cot(c + d*x)/d + 3*a**2*b*log(tan(c + d*x))/d + 3*a*b**2*tan(c + d*x)/d + b**3*tan(c + d*x)**2/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x)**3,
        variable=x,
        num_steps=12,
        integral=-a**3*cot(c + d*x)*csc(c + d*x)/(2*d) - a**3*atanh(cos(c + d*x))/(2*d) + 3*a**2*b*atanh(sin(c + d*x))/d - 3*a**2*b*csc(c + d*x)/d - 3*a*b**2*atanh(cos(c + d*x))/d + 3*a*b**2*sec(c + d*x)/d + b**3*tan(c + d*x)*sec(c + d*x)/(2*d) + b**3*atanh(sin(c + d*x))/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=-a**3*cot(c + d*x)**3/(3*d) - 3*a**2*b*cot(c + d*x)**2/(2*d) + 3*a*b**2*tan(c + d*x)/d - a*(a**2 + 3*b**2)*cot(c + d*x)/d + b**3*tan(c + d*x)**2/(2*d) + b*(3*a**2 + b**2)*log(tan(c + d*x))/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x)**5,
        variable=x,
        num_steps=17,
        integral=-a**3*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 3*a**3*cot(c + d*x)*csc(c + d*x)/(8*d) - 3*a**3*atanh(cos(c + d*x))/(8*d) + 3*a**2*b*atanh(sin(c + d*x))/d - a**2*b*csc(c + d*x)**3/d - 3*a**2*b*csc(c + d*x)/d - 9*a*b**2*atanh(cos(c + d*x))/(2*d) - 3*a*b**2*csc(c + d*x)**2*sec(c + d*x)/(2*d) + 9*a*b**2*sec(c + d*x)/(2*d) + 3*b**3*atanh(sin(c + d*x))/(2*d) + b**3*csc(c + d*x)*sec(c + d*x)**2/(2*d) - 3*b**3*csc(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*csc(c + d*x)**6,
        variable=x,
        num_steps=3,
        integral=-a**3*cot(c + d*x)**5/(5*d) - 3*a**2*b*cot(c + d*x)**4/(4*d) + 3*a*b**2*tan(c + d*x)/d - a*(a**2 + 6*b**2)*cot(c + d*x)/d - a*(2*a**2 + 3*b**2)*cot(c + d*x)**3/(3*d) + b**3*tan(c + d*x)**2/(2*d) + b*(3*a**2 + 2*b**2)*log(tan(c + d*x))/d - b*(6*a**2 + b**2)*cot(c + d*x)**2/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*sin(c + d*x)**3,
        variable=x,
        num_steps=19,
        integral=a**4*cos(c + d*x)**3/(3*d) - a**4*cos(c + d*x)/d - 4*a**3*b*sin(c + d*x)**3/(3*d) - 4*a**3*b*sin(c + d*x)/d + 4*a**3*b*atanh(sin(c + d*x))/d - 2*a**2*b**2*cos(c + d*x)**3/d + 12*a**2*b**2*cos(c + d*x)/d + 6*a**2*b**2*sec(c + d*x)/d + 2*a*b**3*sin(c + d*x)**3*tan(c + d*x)**2/d + 10*a*b**3*sin(c + d*x)**3/(3*d) + 10*a*b**3*sin(c + d*x)/d - 10*a*b**3*atanh(sin(c + d*x))/d + b**4*cos(c + d*x)**3/(3*d) - 3*b**4*cos(c + d*x)/d + b**4*sec(c + d*x)**3/(3*d) - 3*b**4*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*sin(c + d*x)**2,
        variable=x,
        num_steps=7,
        integral=4*a*b**3*tan(c + d*x)**2/d - 4*a*b*(a**2 - 2*b**2)*log(cos(c + d*x))/d + 5*b**4*tan(c + d*x)**3/(6*d) + b**2*(18*a**2 - 5*b**2)*tan(c + d*x)/(2*d) + x*(a**4/2 - 9*a**2*b**2 + 5*b**4/2) - (a + b*tan(c + d*x))**4*sin(c + d*x)*cos(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*sin(c + d*x),
        variable=x,
        num_steps=16,
        integral=-a**4*cos(c + d*x)/d - 4*a**3*b*sin(c + d*x)/d + 4*a**3*b*atanh(sin(c + d*x))/d + 6*a**2*b**2*cos(c + d*x)/d + 6*a**2*b**2*sec(c + d*x)/d + 2*a*b**3*sin(c + d*x)*tan(c + d*x)**2/d + 6*a*b**3*sin(c + d*x)/d - 6*a*b**3*atanh(sin(c + d*x))/d - b**4*cos(c + d*x)/d + b**4*sec(c + d*x)**3/(3*d) - 2*b**4*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x),
        variable=x,
        num_steps=10,
        integral=-a**4*atanh(cos(c + d*x))/d + 4*a**3*b*atanh(sin(c + d*x))/d + 6*a**2*b**2*sec(c + d*x)/d + 2*a*b**3*tan(c + d*x)*sec(c + d*x)/d - 2*a*b**3*atanh(sin(c + d*x))/d + b**4*sec(c + d*x)**3/(3*d) - b**4*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**2,
        variable=x,
        num_steps=3,
        integral=-a**4*cot(c + d*x)/d + 4*a**3*b*log(tan(c + d*x))/d + 6*a**2*b**2*tan(c + d*x)/d + 2*a*b**3*tan(c + d*x)**2/d + b**4*tan(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**3,
        variable=x,
        num_steps=14,
        integral=-a**4*cot(c + d*x)*csc(c + d*x)/(2*d) - a**4*atanh(cos(c + d*x))/(2*d) + 4*a**3*b*atanh(sin(c + d*x))/d - 4*a**3*b*csc(c + d*x)/d - 6*a**2*b**2*atanh(cos(c + d*x))/d + 6*a**2*b**2*sec(c + d*x)/d + 2*a*b**3*tan(c + d*x)*sec(c + d*x)/d + 2*a*b**3*atanh(sin(c + d*x))/d + b**4*sec(c + d*x)**3/(3*d),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**4,
        variable=x,
        num_steps=3,
        integral=-a**4*cot(c + d*x)**3/(3*d) - 2*a**3*b*cot(c + d*x)**2/d - a**2*(a**2 + 6*b**2)*cot(c + d*x)/d + 2*a*b**3*tan(c + d*x)**2/d + 4*a*b*(a**2 + b**2)*log(tan(c + d*x))/d + b**4*tan(c + d*x)**3/(3*d) + b**2*(6*a**2 + b**2)*tan(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**5,
        variable=x,
        num_steps=21,
        integral=-a**4*cot(c + d*x)*csc(c + d*x)**3/(4*d) - 3*a**4*cot(c + d*x)*csc(c + d*x)/(8*d) - 3*a**4*atanh(cos(c + d*x))/(8*d) + 4*a**3*b*atanh(sin(c + d*x))/d - 4*a**3*b*csc(c + d*x)**3/(3*d) - 4*a**3*b*csc(c + d*x)/d - 9*a**2*b**2*atanh(cos(c + d*x))/d - 3*a**2*b**2*csc(c + d*x)**2*sec(c + d*x)/d + 9*a**2*b**2*sec(c + d*x)/d + 6*a*b**3*atanh(sin(c + d*x))/d + 2*a*b**3*csc(c + d*x)*sec(c + d*x)**2/d - 6*a*b**3*csc(c + d*x)/d - b**4*atanh(cos(c + d*x))/d + b**4*sec(c + d*x)**3/(3*d) + b**4*sec(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**6,
        variable=x,
        num_steps=3,
        integral=-a**4*cot(c + d*x)**5/(5*d) - a**3*b*cot(c + d*x)**4/d - 2*a**2*(a**2 + 3*b**2)*cot(c + d*x)**3/(3*d) + 2*a*b**3*tan(c + d*x)**2/d + 4*a*b*(a**2 + 2*b**2)*log(tan(c + d*x))/d - 2*a*b*(2*a**2 + b**2)*cot(c + d*x)**2/d + b**4*tan(c + d*x)**3/(3*d) + 2*b**2*(3*a**2 + b**2)*tan(c + d*x)/d - (a**4 + 12*a**2*b**2 + b**4)*cot(c + d*x)/d,
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**4*csc(c + d*x)**7,
        variable=x,
        num_steps=25,
        integral=-a**4*cot(c + d*x)*csc(c + d*x)**5/(6*d) - 5*a**4*cot(c + d*x)*csc(c + d*x)**3/(24*d) - 5*a**4*cot(c + d*x)*csc(c + d*x)/(16*d) - 5*a**4*atanh(cos(c + d*x))/(16*d) + 4*a**3*b*atanh(sin(c + d*x))/d - 4*a**3*b*csc(c + d*x)**5/(5*d) - 4*a**3*b*csc(c + d*x)**3/(3*d) - 4*a**3*b*csc(c + d*x)/d - 45*a**2*b**2*atanh(cos(c + d*x))/(4*d) - 3*a**2*b**2*csc(c + d*x)**4*sec(c + d*x)/(2*d) - 15*a**2*b**2*csc(c + d*x)**2*sec(c + d*x)/(4*d) + 45*a**2*b**2*sec(c + d*x)/(4*d) + 10*a*b**3*atanh(sin(c + d*x))/d + 2*a*b**3*csc(c + d*x)**3*sec(c + d*x)**2/d - 10*a*b**3*csc(c + d*x)**3/(3*d) - 10*a*b**3*csc(c + d*x)/d - 5*b**4*atanh(cos(c + d*x))/(2*d) - b**4*csc(c + d*x)**2*sec(c + d*x)**3/(2*d) + 5*b**4*sec(c + d*x)**3/(6*d) + 5*b**4*sec(c + d*x)/(2*d),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**5/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=13,
        integral=a**5*b*atanh((-a*sin(c + d*x) + b*cos(c + d*x))/sqrt(a**2 + b**2))/(d*(a**2 + b**2)**(sympy.S(7)/2)) + a**4*b*sin(c + d*x)/(d*(a**2 + b**2)**3) + a**3*b**2*cos(c + d*x)/(d*(a**2 + b**2)**3) + a**2*b*sin(c + d*x)**3/(3*d*(a**2 + b**2)**2) - a*b**2*cos(c + d*x)**3/(3*d*(a**2 + b**2)**2) + a*b**2*cos(c + d*x)/(d*(a**2 + b**2)**2) - a*cos(c + d*x)**5/(d*(5*a**2 + 5*b**2)) + 2*a*cos(c + d*x)**3/(d*(3*a**2 + 3*b**2)) - a*cos(c + d*x)/(d*(a**2 + b**2)) + b*sin(c + d*x)**5/(d*(5*a**2 + 5*b**2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**4/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=8,
        integral=a**4*b*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**3) + a*x*(3*a**4 - 6*a**2*b**2 - b**4)/(8*(a**2 + b**2)**3) + (a*tan(c + d*x) + b)*cos(c + d*x)**4/(d*(4*a**2 + 4*b**2)) - (a*(5*a**2 + b**2)*tan(c + d*x) + 4*b*(2*a**2 + b**2))*cos(c + d*x)**2/(8*d*(a**2 + b**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**3/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=10,
        integral=a**3*b*atanh((-a*sin(c + d*x) + b*cos(c + d*x))/sqrt(a**2 + b**2))/(d*(a**2 + b**2)**(sympy.S(5)/2)) + a**2*b*sin(c + d*x)/(d*(a**2 + b**2)**2) + a*b**2*cos(c + d*x)/(d*(a**2 + b**2)**2) + a*cos(c + d*x)**3/(d*(3*a**2 + 3*b**2)) - a*cos(c + d*x)/(d*(a**2 + b**2)) + b*sin(c + d*x)**3/(d*(3*a**2 + 3*b**2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**2/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=7,
        integral=a**2*b*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**2) + a*x*(a**2 - b**2)/(2*(a**2 + b**2)**2) - (a*tan(c + d*x) + b)*cos(c + d*x)**2/(d*(2*a**2 + 2*b**2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=6,
        integral=a*b*atanh((-a*sin(c + d*x) + b*cos(c + d*x))/sqrt(a**2 + b**2))/(d*(a**2 + b**2)**(sympy.S(3)/2)) - a*cos(c + d*x)/(d*(a**2 + b**2)) + b*sin(c + d*x)/(d*(a**2 + b**2)),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=6,
        integral=b*atanh((-a*sin(c + d*x) + b*cos(c + d*x))/sqrt(a**2 + b**2))/(a*d*sqrt(a**2 + b**2)) - atanh(cos(c + d*x))/(a*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**2/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)/(a*d) + b*log(a + b*tan(c + d*x))/(a**2*d) - b*log(tan(c + d*x))/(a**2*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**3/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=15,
        integral=-cot(c + d*x)*csc(c + d*x)/(2*a*d) - atanh(cos(c + d*x))/(2*a*d) + b*csc(c + d*x)/(a**2*d) - b**2*atanh(cos(c + d*x))/(a**3*d) + b*sqrt(a**2 + b**2)*atanh((-a*sin(c + d*x) + b*cos(c + d*x))/sqrt(a**2 + b**2))/(a**3*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**4/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**3/(3*a*d) + b*cot(c + d*x)**2/(2*a**2*d) - (a**2 + b**2)*cot(c + d*x)/(a**3*d) + b*(a**2 + b**2)*log(a + b*tan(c + d*x))/(a**4*d) - b*(a**2 + b**2)*log(tan(c + d*x))/(a**4*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**6/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**5/(5*a*d) + b*cot(c + d*x)**4/(4*a**2*d) - (2*a**2 + b**2)*cot(c + d*x)**3/(3*a**3*d) + b*(2*a**2 + b**2)*cot(c + d*x)**2/(2*a**4*d) - (a**2 + b**2)**2*cot(c + d*x)/(a**5*d) + b*(a**2 + b**2)**2*log(a + b*tan(c + d*x))/(a**6*d) - b*(a**2 + b**2)**2*log(tan(c + d*x))/(a**6*d),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**6/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=9,
        integral=-a**6*b/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**4) + 2*a**5*b*(a**2 - 3*b**2)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**5) + x*(5*a**8 - 80*a**6*b**2 + 50*a**4*b**4 + 8*a**2*b**6 + b**8)/(16*(a**2 + b**2)**5) - (2*a*b + (a**2 - b**2)*tan(c + d*x))*cos(c + d*x)**6/(6*d*(a**2 + b**2)**2) + (12*a*b*(3*a**2 + b**2) + (13*a**4 - 18*a**2*b**2 - 7*b**4)*tan(c + d*x))*cos(c + d*x)**4/(24*d*(a**2 + b**2)**3) - (48*a**5*b + (11*a**6 - 43*a**4*b**2 - 7*a**2*b**4 - b**6)*tan(c + d*x))*cos(c + d*x)**2/(16*d*(a**2 + b**2)**4),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**4/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=8,
        integral=-a**4*b/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**3) + 2*a**3*b*(a**2 - 2*b**2)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**4) + x*(3*a**6 - 33*a**4*b**2 + 13*a**2*b**4 + b**6)/(8*(a**2 + b**2)**4) + (2*a*b + (a**2 - b**2)*tan(c + d*x))*cos(c + d*x)**4/(4*d*(a**2 + b**2)**2) - (16*a**3*b + (5*a**4 - 12*a**2*b**2 - b**4)*tan(c + d*x))*cos(c + d*x)**2/(8*d*(a**2 + b**2)**3),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**2/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=7,
        integral=-a**2*b/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**2) + 2*a*b*(a**2 - b**2)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**3) + x*(a**4 - 6*a**2*b**2 + b**4)/(2*(a**2 + b**2)**3) - (2*a*b + (a**2 - b**2)*tan(c + d*x))*cos(c + d*x)**2/(2*d*(a**2 + b**2)**2),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**2/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=3,
        integral=-b/(a**2*d*(a + b*tan(c + d*x))) - cot(c + d*x)/(a**2*d) + 2*b*log(a + b*tan(c + d*x))/(a**3*d) - 2*b*log(tan(c + d*x))/(a**3*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**4/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**3/(3*a**2*d) + b*cot(c + d*x)**2/(a**3*d) - b*(a**2 + b**2)/(a**4*d*(a + b*tan(c + d*x))) - (a**2 + 3*b**2)*cot(c + d*x)/(a**4*d) + 2*b*(a**2 + 2*b**2)*log(a + b*tan(c + d*x))/(a**5*d) - 2*b*(a**2 + 2*b**2)*log(tan(c + d*x))/(a**5*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**6/(a + b*tan(c + d*x))**2,
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**5/(5*a**2*d) + b*cot(c + d*x)**4/(2*a**3*d) - (2*a**2 + 3*b**2)*cot(c + d*x)**3/(3*a**4*d) + 2*b*(a**2 + b**2)*cot(c + d*x)**2/(a**5*d) - b*(a**2 + b**2)**2/(a**6*d*(a + b*tan(c + d*x))) - (a**2 + b**2)*(a**2 + 5*b**2)*cot(c + d*x)/(a**6*d) + 2*b*(a**2 + b**2)*(a**2 + 3*b**2)*log(a + b*tan(c + d*x))/(a**7*d) - 2*b*(a**2 + b**2)*(a**2 + 3*b**2)*log(tan(c + d*x))/(a**7*d),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**6/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=9,
        integral=-a**6*b/(2*d*(a + b*tan(c + d*x))**2*(a**2 + b**2)**4) - 2*a**5*b*(a**2 - 3*b**2)/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**5) + a**4*b*(3*a**4 - 22*a**2*b**2 + 15*b**4)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**6) + a*x*(5*a**8 - 180*a**6*b**2 + 390*a**4*b**4 - 68*a**2*b**6 - 3*b**8)/(16*(a**2 + b**2)**6) - a*(24*a**3*b*(3*a**2 - 5*b**2) + (11*a**6 - 119*a**4*b**2 + 65*a**2*b**4 + 3*b**6)*tan(c + d*x))*cos(c + d*x)**2/(16*d*(a**2 + b**2)**5) - (a*(a**2 - 3*b**2)*tan(c + d*x) + b*(3*a**2 - b**2))*cos(c + d*x)**6/(6*d*(a**2 + b**2)**3) + (a*(13*a**4 - 62*a**2*b**2 - 3*b**4)*tan(c + d*x) + 6*b*(9*a**4 - 4*a**2*b**2 - b**4))*cos(c + d*x)**4/(24*d*(a**2 + b**2)**4),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**4/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=8,
        integral=-a**4*b/(2*d*(a + b*tan(c + d*x))**2*(a**2 + b**2)**3) - 2*a**3*b*(a**2 - 2*b**2)/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**4) + 3*a**2*b*(a**4 - 5*a**2*b**2 + 2*b**4)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**5) + 3*a*x*(a**6 - 25*a**4*b**2 + 35*a**2*b**4 - 3*b**6)/(8*(a**2 + b**2)**5) - a*(24*a*b*(a**2 - b**2) + (5*a**4 - 34*a**2*b**2 + 9*b**4)*tan(c + d*x))*cos(c + d*x)**2/(8*d*(a**2 + b**2)**4) + (a*(a**2 - 3*b**2)*tan(c + d*x) + b*(3*a**2 - b**2))*cos(c + d*x)**4/(4*d*(a**2 + b**2)**3),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**2/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=7,
        integral=-a**2*b/(2*d*(a + b*tan(c + d*x))**2*(a**2 + b**2)**2) - 2*a*b*(a**2 - b**2)/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**3) + a*x*(a**4 - 14*a**2*b**2 + 9*b**4)/(2*(a**2 + b**2)**4) + b*(3*a**4 - 8*a**2*b**2 + b**4)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**4) - (a*(a**2 - 3*b**2)*tan(c + d*x) + b*(3*a**2 - b**2))*cos(c + d*x)**2/(2*d*(a**2 + b**2)**3),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**2/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=3,
        integral=-b/(2*a**2*d*(a + b*tan(c + d*x))**2) - 2*b/(a**3*d*(a + b*tan(c + d*x))) - cot(c + d*x)/(a**3*d) + 3*b*log(a + b*tan(c + d*x))/(a**4*d) - 3*b*log(tan(c + d*x))/(a**4*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**4/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**3/(3*a**3*d) + 3*b*cot(c + d*x)**2/(2*a**4*d) - b*(a**2 + b**2)/(2*a**4*d*(a + b*tan(c + d*x))**2) - 2*b*(a**2 + 2*b**2)/(a**5*d*(a + b*tan(c + d*x))) - (a**2 + 6*b**2)*cot(c + d*x)/(a**5*d) + b*(3*a**2 + 10*b**2)*log(a + b*tan(c + d*x))/(a**6*d) - b*(3*a**2 + 10*b**2)*log(tan(c + d*x))/(a**6*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**6/(a + b*tan(c + d*x))**3,
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**5/(5*a**3*d) + 3*b*cot(c + d*x)**4/(4*a**4*d) - (2*a**2 + 6*b**2)*cot(c + d*x)**3/(3*a**5*d) + b*(3*a**2 + 5*b**2)*cot(c + d*x)**2/(a**6*d) - b*(a**2 + b**2)**2/(2*a**6*d*(a + b*tan(c + d*x))**2) - 2*b*(a**2 + b**2)*(a**2 + 3*b**2)/(a**7*d*(a + b*tan(c + d*x))) - (a**4 + 12*a**2*b**2 + 15*b**4)*cot(c + d*x)/(a**7*d) + b*(3*a**4 + 20*a**2*b**2 + 21*b**4)*log(a + b*tan(c + d*x))/(a**8*d) - b*(3*a**4 + 20*a**2*b**2 + 21*b**4)*log(tan(c + d*x))/(a**8*d),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**4/(a + b*tan(c + d*x))**4,
        variable=x,
        num_steps=8,
        integral=-a**4*b/(3*d*(a + b*tan(c + d*x))**3*(a**2 + b**2)**3) - a**3*b*(a**2 - 2*b**2)/(d*(a + b*tan(c + d*x))**2*(a**2 + b**2)**4) - 3*a**2*b*(a**4 - 5*a**2*b**2 + 2*b**4)/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**5) + 4*a*b*(a**2 - b**2)*(a**4 - 8*a**2*b**2 + b**4)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**6) + x*(3*a**8 - 132*a**6*b**2 + 370*a**4*b**4 - 132*a**2*b**6 + 3*b**8)/(8*(a**2 + b**2)**6) + (4*a*b*(a**2 - b**2) + (a**4 - 6*a**2*b**2 + b**4)*tan(c + d*x))*cos(c + d*x)**4/(4*d*(a**2 + b**2)**4) - (16*a*b*(2*a**4 - 5*a**2*b**2 + b**4) + (5*a**6 - 65*a**4*b**2 + 55*a**2*b**4 - 3*b**6)*tan(c + d*x))*cos(c + d*x)**2/(8*d*(a**2 + b**2)**5),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**2/(a + b*tan(c + d*x))**4,
        variable=x,
        num_steps=7,
        integral=-a**2*b/(3*d*(a + b*tan(c + d*x))**3*(a**2 + b**2)**2) + 4*a*b*(a**4 - 5*a**2*b**2 + 2*b**4)*log(a*cos(c + d*x) + b*sin(c + d*x))/(d*(a**2 + b**2)**5) - a*b*(a**2 - b**2)/(d*(a + b*tan(c + d*x))**2*(a**2 + b**2)**3) - b*(3*a**4 - 8*a**2*b**2 + b**4)/(d*(a + b*tan(c + d*x))*(a**2 + b**2)**4) + x*(a**6 - 25*a**4*b**2 + 35*a**2*b**4 - 3*b**6)/(2*(a**2 + b**2)**5) - (4*a*b*(a**2 - b**2) + (a**4 - 6*a**2*b**2 + b**4)*tan(c + d*x))*cos(c + d*x)**2/(2*d*(a**2 + b**2)**4),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**2/(a + b*tan(c + d*x))**4,
        variable=x,
        num_steps=3,
        integral=-b/(3*a**2*d*(a + b*tan(c + d*x))**3) - b/(a**3*d*(a + b*tan(c + d*x))**2) - 3*b/(a**4*d*(a + b*tan(c + d*x))) - cot(c + d*x)/(a**4*d) + 4*b*log(a + b*tan(c + d*x))/(a**5*d) - 4*b*log(tan(c + d*x))/(a**5*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**4/(a + b*tan(c + d*x))**4,
        variable=x,
        num_steps=3,
        integral=-b*(a**2 + b**2)/(3*a**4*d*(a + b*tan(c + d*x))**3) - cot(c + d*x)**3/(3*a**4*d) + 2*b*cot(c + d*x)**2/(a**5*d) - b*(a**2 + 2*b**2)/(a**5*d*(a + b*tan(c + d*x))**2) - b*(3*a**2 + 10*b**2)/(a**6*d*(a + b*tan(c + d*x))) - (a**2 + 10*b**2)*cot(c + d*x)/(a**6*d) + 4*b*(a**2 + 5*b**2)*log(a + b*tan(c + d*x))/(a**7*d) - 4*b*(a**2 + 5*b**2)*log(tan(c + d*x))/(a**7*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(c + d*x)**6/(a + b*tan(c + d*x))**4,
        variable=x,
        num_steps=3,
        integral=-cot(c + d*x)**5/(5*a**4*d) + b*cot(c + d*x)**4/(a**5*d) - b*(a**2 + b**2)**2/(3*a**6*d*(a + b*tan(c + d*x))**3) - (2*a**2 + 10*b**2)*cot(c + d*x)**3/(3*a**6*d) + 2*b*(2*a**2 + 5*b**2)*cot(c + d*x)**2/(a**7*d) - b*(a**2 + b**2)*(a**2 + 3*b**2)/(a**7*d*(a + b*tan(c + d*x))**2) - b*(3*a**4 + 20*a**2*b**2 + 21*b**4)/(a**8*d*(a + b*tan(c + d*x))) - (a**4 + 20*a**2*b**2 + 35*b**4)*cot(c + d*x)/(a**8*d) + 4*b*(a**4 + 10*a**2*b**2 + 14*b**4)*log(a + b*tan(c + d*x))/(a**9*d) - 4*b*(a**4 + 10*a**2*b**2 + 14*b**4)*log(tan(c + d*x))/(a**9*d),
    ),
    RubiTestSuiteCase(
        integrand=csc(x)/(tan(x) + 1),
        variable=x,
        num_steps=6,
        integral=sqrt(2)*atanh(sqrt(2)*(-sin(x) + cos(x))/2)/2 - atanh(cos(x)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**3*sin(c + d*x)**m,
        variable=x,
        num_steps=8,
        integral=a**3*sin(c + d*x)**(m + 1)*cos(c + d*x)*hyper((sympy.S.Half, m/2 + sympy.S.Half), (m/2 + sympy.S(3)/2,), sin(c + d*x)**2)/(d*(m + 1)*sqrt(cos(c + d*x)**2)) + 3*a**2*b*sin(c + d*x)**(m + 2)*hyper((1, m/2 + 1), (m/2 + 2,), sin(c + d*x)**2)/(d*(m + 2)) + 3*a*b**2*sqrt(cos(c + d*x)**2)*sin(c + d*x)**(m + 3)*hyper((sympy.S(3)/2, m/2 + sympy.S(3)/2), (m/2 + sympy.S(5)/2,), sin(c + d*x)**2)*sec(c + d*x)/(d*(m + 3)) + b**3*sin(c + d*x)**(m + 4)*hyper((2, m/2 + 2), (m/2 + 3,), sin(c + d*x)**2)/(d*(m + 4)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**2*sin(c + d*x)**m,
        variable=x,
        num_steps=6,
        integral=a**2*sin(c + d*x)**(m + 1)*cos(c + d*x)*hyper((sympy.S.Half, m/2 + sympy.S.Half), (m/2 + sympy.S(3)/2,), sin(c + d*x)**2)/(d*(m + 1)*sqrt(cos(c + d*x)**2)) + 2*a*b*sin(c + d*x)**(m + 2)*hyper((1, m/2 + 1), (m/2 + 2,), sin(c + d*x)**2)/(d*(m + 2)) + b**2*sqrt(cos(c + d*x)**2)*sin(c + d*x)**(m + 3)*hyper((sympy.S(3)/2, m/2 + sympy.S(3)/2), (m/2 + sympy.S(5)/2,), sin(c + d*x)**2)*sec(c + d*x)/(d*(m + 3)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))*sin(c + d*x)**m,
        variable=x,
        num_steps=5,
        integral=a*sin(c + d*x)**(m + 1)*cos(c + d*x)*hyper((sympy.S.Half, m/2 + sympy.S.Half), (m/2 + sympy.S(3)/2,), sin(c + d*x)**2)/(d*(m + 1)*sqrt(cos(c + d*x)**2)) + b*sin(c + d*x)**(m + 2)*hyper((1, m/2 + 1), (m/2 + 2,), sin(c + d*x)**2)/(d*(m + 2)),
    ),
    RubiTestSuiteCase(
        integrand=sin(c + d*x)**m/(a + b*tan(c + d*x)),
        variable=x,
        num_steps=14,
        integral=-2**(m + 1)*a*b*(tan(c/2 + d*x/2)/(tan(c/2 + d*x/2)**2 + 1))**m*(tan(c/2 + d*x/2)**2 + 1)**m*tan(c/2 + d*x/2)**3*appellf1(m/2 + sympy.S(3)/2, 1, m + 1, m/2 + sympy.S(5)/2, a**2*tan(c/2 + d*x/2)**2/(b + sqrt(a**2 + b**2))**2, -tan(c/2 + d*x/2)**2)/(d*sqrt(a**2 + b**2)*(b + sqrt(a**2 + b**2))**2*(m + 3)) + 2**(m + 1)*a*b*(tan(c/2 + d*x/2)/(tan(c/2 + d*x/2)**2 + 1))**m*(tan(c/2 + d*x/2)**2 + 1)**m*tan(c/2 + d*x/2)**3*appellf1(m/2 + sympy.S(3)/2, 1, m + 1, m/2 + sympy.S(5)/2, a**2*tan(c/2 + d*x/2)**2/(b - sqrt(a**2 + b**2))**2, -tan(c/2 + d*x/2)**2)/(d*sqrt(a**2 + b**2)*(b - sqrt(a**2 + b**2))**2*(m + 3)) - 2**(m + 1)*b*(tan(c/2 + d*x/2)/(tan(c/2 + d*x/2)**2 + 1))**m*(tan(c/2 + d*x/2)**2 + 1)**m*tan(c/2 + d*x/2)**2*appellf1(m/2 + 1, 1, m + 1, m/2 + 2, a**2*tan(c/2 + d*x/2)**2/(b + sqrt(a**2 + b**2))**2, -tan(c/2 + d*x/2)**2)/(d*sqrt(a**2 + b**2)*(b + sqrt(a**2 + b**2))*(m + 2)) + 2**(m + 1)*b*(tan(c/2 + d*x/2)/(tan(c/2 + d*x/2)**2 + 1))**m*(tan(c/2 + d*x/2)**2 + 1)**m*tan(c/2 + d*x/2)**2*appellf1(m/2 + 1, 1, m + 1, m/2 + 2, a**2*tan(c/2 + d*x/2)**2/(b - sqrt(a**2 + b**2))**2, -tan(c/2 + d*x/2)**2)/(d*sqrt(a**2 + b**2)*(b - sqrt(a**2 + b**2))*(m + 2)) + 2**(m + 1)*(tan(c/2 + d*x/2)/(tan(c/2 + d*x/2)**2 + 1))**m*(tan(c/2 + d*x/2)**2 + 1)**m*tan(c/2 + d*x/2)*hyper((m + 1, m/2 + sympy.S.Half), (m/2 + sympy.S(3)/2,), -tan(c/2 + d*x/2)**2)/(a*d*(m + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*sin(c + d*x)**m,
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')(((sympy.sin((Symbol('c') + (Symbol('d') * x))))**(Symbol('m')) * ((Symbol('a') + (Symbol('b') * sympy.tan((Symbol('c') + (Symbol('d') * x))))))**(Symbol('n'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*sin(c + d*x)**4,
        variable=x,
        num_steps=7,
        integral=(a + b*tan(c + d*x))**(n + 1)*(a*tan(c + d*x) + b)*cos(c + d*x)**4/(d*(4*a**2 + 4*b**2)) - (a + b*tan(c + d*x))**(n + 1)*(a*(5*a**2 + b**2*(2*n + 3))*tan(c + d*x) + b*(a**2*(7 - n) + b**2*(n + 5)))*cos(c + d*x)**2/(8*d*(a**2 + b**2)**2) - (a + b*tan(c + d*x))**(n + 1)*(a*b**2*n*(5*a**2 + b**2*(2*n + 3)) - sqrt(-b**2)*(3*a**4 + a**2*b**2*(-n**2 + 6*n + 6) + b**4*(n**2 + 4*n + 3)))*hyper((1, n + 1), (n + 2,), (a + b*tan(c + d*x))/(a + sqrt(-b**2)))/(16*b*d*(a + sqrt(-b**2))*(a**2 + b**2)**2*(n + 1)) - (a + b*tan(c + d*x))**(n + 1)*(a*b**2*n*(5*a**2 + b**2*(2*n + 3)) + sqrt(-b**2)*(3*a**4 + a**2*b**2*(-n**2 + 6*n + 6) + b**4*(n**2 + 4*n + 3)))*hyper((1, n + 1), (n + 2,), (a + b*tan(c + d*x))/(a - sqrt(-b**2)))/(16*b*d*(a - sqrt(-b**2))*(a**2 + b**2)**2*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*sin(c + d*x)**2,
        variable=x,
        num_steps=6,
        integral=-(a + b*tan(c + d*x))**(n + 1)*(a*tan(c + d*x) + b)*cos(c + d*x)**2/(d*(2*a**2 + 2*b**2)) - (a + b*tan(c + d*x))**(n + 1)*(a*b**2*n - sqrt(-b**2)*(a**2 + b**2*(n + 1)))*hyper((1, n + 1), (n + 2,), (a + b*tan(c + d*x))/(a + sqrt(-b**2)))/(4*b*d*(a + sqrt(-b**2))*(a**2 + b**2)*(n + 1)) - (a + b*tan(c + d*x))**(n + 1)*(a*b**2*n + sqrt(-b**2)*(a**2 + b**2*(n + 1)))*hyper((1, n + 1), (n + 2,), (a + b*tan(c + d*x))/(a - sqrt(-b**2)))/(4*b*d*(a - sqrt(-b**2))*(a**2 + b**2)*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*csc(c + d*x)**2,
        variable=x,
        num_steps=2,
        integral=b*(a + b*tan(c + d*x))**(n + 1)*hyper((2, n + 1), (n + 2,), 1 + b*tan(c + d*x)/a)/(a**2*d*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*csc(c + d*x)**4,
        variable=x,
        num_steps=4,
        integral=-(a + b*tan(c + d*x))**(n + 1)*cot(c + d*x)**3/(3*a*d) + b*(2 - n)*(a + b*tan(c + d*x))**(n + 1)*cot(c + d*x)**2/(6*a**2*d) + b*(a + b*tan(c + d*x))**(n + 1)*(6*a**2 + b**2*(n**2 - 3*n + 2))*hyper((2, n + 1), (n + 2,), 1 + b*tan(c + d*x)/a)/(6*a**4*d*(n + 1)),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*sin(c + d*x)**3,
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')(((sympy.sin((Symbol('c') + (Symbol('d') * x))))**(Integer(3)) * ((Symbol('a') + (Symbol('b') * sympy.tan((Symbol('c') + (Symbol('d') * x))))))**(Symbol('n'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*sin(c + d*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')((sympy.sin((Symbol('c') + (Symbol('d') * x))) * ((Symbol('a') + (Symbol('b') * sympy.tan((Symbol('c') + (Symbol('d') * x))))))**(Symbol('n'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*csc(c + d*x),
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')((sympy.csc((Symbol('c') + (Symbol('d') * x))) * ((Symbol('a') + (Symbol('b') * sympy.tan((Symbol('c') + (Symbol('d') * x))))))**(Symbol('n'))), x),
    ),
    RubiTestSuiteCase(
        integrand=(a + b*tan(c + d*x))**n*csc(c + d*x)**3,
        variable=x,
        num_steps=0,
        integral=sympy.Function('CannotIntegrate')(((sympy.csc((Symbol('c') + (Symbol('d') * x))))**(Integer(3)) * ((Symbol('a') + (Symbol('b') * sympy.tan((Symbol('c') + (Symbol('d') * x))))))**(Symbol('n'))), x),
    ),
]
