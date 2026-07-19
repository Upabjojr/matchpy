# -*- coding: utf-8 -*-
"""Regression tests for exponential/Gaussian integrals that reach Erf/Erfi.

These exercise, end to end via the DFS integrator with path-aware cycle
detection (`_RubiIntegrator.integrate`):

- exp represented as Pow(E, .) so the F^(...) exponential rules match,
- the complete-the-square [42] / ExpandToSum-normalize [43] pair, which are
  mutually inverse and would otherwise loop forever without cycle detection,
- rule [11] (F^(a+b(d x+c)^2) -> Erf/Erfi) winning over the CannotIntegrate
  fallback, independent of the order the matcher yields rules.

The antiderivatives involve complex-argument erf/erfi, which sympy.simplify
cannot verify symbolically, so correctness is checked numerically:
d/dx(result) must equal the integrand.
"""
import pytest
import sympy
from sympy import exp, sin, Symbol, I, diff, Function

from rubi_rules.base_objects import rubi_integrate

x = Symbol('x')


def _derivative_matches(result, integrand, points=(0.3, 0.7, 1.1, 1.7, -0.5, -1.2)):
    """True iff d/dx(result) == integrand numerically at every sample point."""
    assert not result.has(Function('Int')), f"unevaluated Int in {result}"
    assert 'CannotIntegrate' not in str(result), f"CannotIntegrate in {result}"
    d = diff(result, x)
    for val in points:
        got = complex(d.subs(x, val).evalf())
        want = complex(integrand.subs(x, val).evalf())
        if abs(got - want) > 1e-9:
            return False
    return True


class TestExponentialGaussian:

    def test_complex_gaussian_scoped(self):
        """int e^(-i x^2 + (1-i) x) dx -> erfi, via r_2 rules only.

        Exercises the 42<->43 cycle: without cycle detection this loops forever.
        """
        integrand = exp(-I * x**2 + (1 - I) * x)
        result = rubi_integrate(integrand, x, pattern='r_2_exponentials/**')
        assert _derivative_matches(result, integrand)

    def test_gaussian_real(self):
        """int e^(x^2) dx -> sqrt(pi)/2 erfi(x)."""
        integrand = exp(x**2)
        result = rubi_integrate(integrand, x, pattern='r_2_exponentials/**')
        assert _derivative_matches(result, integrand)

    @pytest.mark.slow
    def test_exp_times_sin_of_quadratic_full(self):
        """int e^x sin(x^2 + x) dx -> Erf/Erfi (matches Mathematica Rubi).

        Full ruleset: reduces via 4.7.7 (exp*trig) and 2.3 (Gaussian). Requires
        the DFS cycle detection to terminate and to prefer the Erf result over the
        CannotIntegrate fallback.
        """
        integrand = exp(x) * sin(x**2 + x)
        result = rubi_integrate(integrand, x)
        assert _derivative_matches(result, integrand)
