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


# Integrands the full rule set integrates to a verified closed form, each paired
# with the sample points used to check d/dx(result) == integrand. `None` uses the
# default spread; log(log(x)) cases must be sampled at x > 1 to stay real. Grouped
# by category. The x*log(log(x)) family also guards the Subst variable-capture bug
# (see TestSubstNoVariableCapture note below).
_LOGLOG_POINTS = (1.2, 1.6, 2.1, 2.7, 3.3)
FULL_RULESET_INTEGRANDS = [
    # --- algebraic ---
    (1/x, None), (x**2, None), (x**5, None), (sqrt(x), None), (1/sqrt(x), None),
    (1/(3*x + 2), None), ((3*x + 2)**4, None),
    (1/(x**2 + 1), None), ((x**2 + 1)**(-2), None), (1/(x**2 + 4), None),
    (1/sqrt(x**2 + 1), None), (sqrt(x**2 + 1), None), (1/(x*(x + 1)), None),
    # --- exponential ---
    (exp(x), None), (exp(3*x), None), (x*exp(x), None), (x**2*exp(x), None),
    (exp(x**2), None), (exp(x**2 + x), None), (exp(-x**2), None),   # -> erf / erfi
    # --- trigonometric ---
    (sin(x), None), (cos(x), None), (sin(3*x), None), (sin(x)**2, None),
    (sin(x)*cos(x), None), (x*sin(x), None), (x**2*sin(x), None), (tan(x), None),
    (sin(x**2), None), (cos(x**2), None),                          # -> Fresnel
    # --- logarithmic ---
    (log(x), None), (x*log(x), None), (log(x)/x, None), (log(x)**2, None),
    # Subst[Int[g, x], x, v] with v = log(x) reintroducing x: guards the variable-
    # capture bug where the old eager `expr.subs(x, v)` substituted into the still-
    # unevaluated inner Int and silently gave a wrong answer (x*log(log(x)) -> 0).
    (x*log(log(x)), _LOGLOG_POINTS), (log(log(x)), _LOGLOG_POINTS),
    (x**2*log(log(x)), _LOGLOG_POINTS), (x/log(x), _LOGLOG_POINTS),
    # --- inverse trig ---
    (atan(x), None),
    (x*atan(x), None),  # this one tests "Star" nodes
    # --- exponential * trig (incl. Gaussian erf/erfi) ---
    (exp(x)*sin(x), None), (exp(x)*cos(x), None), (exp(2*x)*sin(3*x), None),
    (exp(x)*sin(x**2 + x), None),
]


@pytest.mark.slow
def test_full_ruleset():
    """Every integrand integrates to a closed form whose derivative is the integrand.

    A single test so the whole (slow) rule set is loaded once. All integrands are
    checked and every failure is reported together, rather than aborting on the
    first. Also guards the Subst variable-capture bug (the x*log(log(x)) family).
    """
    failures = []
    for integrand, points in FULL_RULESET_INTEGRANDS:
        try:
            result = rubi_integrate(integrand, x)
            if result == 0:
                failures.append(f"{integrand}: collapsed to 0")
            elif 'Subst' in str(result):
                failures.append(f"{integrand}: unresolved Subst -> {result}")
            elif not _derivative_matches(
                    result, integrand, **({'points': points} if points else {})):
                failures.append(f"{integrand}: d/dx != integrand -> {result}")
        except Exception as exc:  # noqa: BLE001 - report which integrand blew up
            failures.append(f"{integrand}: {type(exc).__name__}: {exc}")
    assert not failures, "integrals failed:\n" + "\n".join(failures)
