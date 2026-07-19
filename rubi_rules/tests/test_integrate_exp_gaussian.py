# -*- coding: utf-8 -*-
"""End-to-end integration tests via the DFS integrator (`rubi_integrate`).

Two fast tests scoped to the exponential rules exercise the complete-the-square /
ExpandToSum cycle and the Gaussian -> Erf/Erfi path.

`test_full_ruleset` (marked `slow`) loads the *entire* Rubi rule set once (~50s,
then cached) and checks a broad spread of integrals across the rule categories —
algebraic, exponential, trigonometric, logarithmic, inverse-trig, and
exponential*trig (including the Erf/Erfi and Fresnel special-function cases).

Antiderivatives that involve complex-argument erf/erfi/Fresnel functions cannot be
verified by `sympy.simplify`, so correctness is checked numerically:
d/dx(result) must equal the integrand at several sample points.
"""
import pytest
import sympy
from sympy import exp, sin, cos, tan, log, sqrt, atan, Symbol, I, Function

from rubi_rules.base_objects import rubi_integrate

x = Symbol('x')


def _derivative_matches(result, integrand,
                        points=(0.3, 0.5, 0.7, 1.2, 1.6, 2.1), tol=1e-7, need=3):
    """True iff d/dx(result) == integrand numerically, and result is fully solved.

    Points at which either side fails to evaluate to a finite number are skipped;
    at least `need` valid points must match within `tol`.
    """
    assert not result.has(Function('Int')), f"unevaluated Int in {result}"
    assert 'CannotIntegrate' not in str(result), f"CannotIntegrate in {result}"
    d = sympy.diff(result, x)
    matched = 0
    for p in points:
        try:
            got = complex(d.subs(x, p).evalf())
            want = complex(integrand.subs(x, p).evalf())
        except Exception:
            continue
        if got != got or want != want:  # NaN
            continue
        if abs(got - want) > tol:
            return False
        matched += 1
    return matched >= need


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


# Integrands the full rule set integrates to a verified closed form. Grouped by
# category; each is checked by differentiating the result (see _derivative_matches).
FULL_RULESET_INTEGRANDS = [
    # --- algebraic ---
    1/x, x**2, x**5, sqrt(x), 1/sqrt(x), 1/(3*x + 2), (3*x + 2)**4,
    1/(x**2 + 1), (x**2 + 1)**(-2), 1/(x**2 + 4),
    1/sqrt(x**2 + 1), sqrt(x**2 + 1), 1/(x*(x + 1)),
    # --- exponential ---
    exp(x), exp(3*x), x*exp(x), x**2*exp(x),
    exp(x**2), exp(x**2 + x), exp(-x**2),          # -> erf / erfi
    # --- trigonometric ---
    sin(x), cos(x), sin(3*x), sin(x)**2, sin(x)*cos(x), x*sin(x), x**2*sin(x), tan(x),
    sin(x**2), cos(x**2),                          # -> Fresnel
    # --- logarithmic ---
    log(x), x*log(x), log(x)/x, log(x)**2,
    # --- inverse trig ---
    atan(x),
    x*atan(x),  # this one tests "Star" nodes
    # --- exponential * trig (incl. Gaussian erf/erfi) ---
    exp(x)*sin(x), exp(x)*cos(x), exp(2*x)*sin(3*x), exp(x)*sin(x**2 + x),
]


@pytest.mark.slow
@pytest.mark.parametrize("integrand", FULL_RULESET_INTEGRANDS, ids=str)
def test_full_ruleset(integrand):
    """Each integrand integrates to a closed form whose derivative is the integrand.

    Uses the full rule set (loaded once, then cached across the parametrized cases).
    """
    result = rubi_integrate(integrand, x)
    assert _derivative_matches(result, integrand)
