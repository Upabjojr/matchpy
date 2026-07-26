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
from sympy import exp, sin, cos, tan, log, sqrt, atan, atanh, acoth, Symbol, I, Function

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
    # 1/(x^4+1): its partial-fraction path produces terms whose numeric factor SymPy
    # leaves as an unsimplified Plus-of-Powers (really Sqrt[2]); SignOfFactor's `< 0`
    # test used to crash with TypeError on that non-real form. Guards the NumberQ /
    # SignOfFactor fix (see test_SignOfFactor_complex_numeric_factor).
    (1/(x**4 + 1), None),
    # x^3/(1-x^6): GCD(4,6)=2 -> reduce via u=x^2 to the real cubic result. Without the
    # generic-Boolean constraint fix, the GCD-reduction rule was disabled and the odd-m
    # root-sum rule produced a wrong I*ArcTan. (Symbolic-coefficient siblings x/(a+b x^6)
    # etc. are in _SYMBOLIC_COEFF_INTEGRANDS.)
    (x**3/(1 - x**6), None),
    (1/sqrt(x**2 + 1), None), (sqrt(x**2 + 1), None), (1/(x*(x + 1)), None),
    (1/(x*(6*x + 4)), None),   # Simplify nc_simplify RecursionError fix
    # hyper/TupleArg round-trip fix + DerivativeDivides/Condition bool-leak fix:
    # these raised (Counter(Tuple) TypeError / 'bool' has no is_Float) before.
    (sqrt(2 + 3*x)/x, None), (1/(x*sqrt(2 + 3*x)), None),
    (1/(x*(2 + 3*x)**sympy.Rational(3, 2)), None),
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


def _numeric_matches(result, integrand, subs0, pts):
    """True iff d/dx(result) == integrand at >=2 of the sample points `pts`.

    `subs0` binds the symbolic coefficients to concrete values first.
    """
    d = sympy.diff(result, x) - integrand
    matched = 0
    for pt in pts:
        try:
            val = complex(d.subs(subs0).subs(x, pt).evalf())
        except Exception:
            continue
        if val == val and abs(val) < 1e-8:  # not NaN and ~0
            matched += 1
    return matched >= 2


def _check_full_ruleset():
    """Each integrand -> closed form whose derivative is the integrand.

    Also guards the Subst variable-capture bug (the x*log(log(x)) family).
    Returns a list of failure descriptions (empty == all good).
    """
    failures = []
    for integrand, points in FULL_RULESET_INTEGRANDS:
        try:
            result = rubi_integrate(integrand, x)
            if result == 0:
                failures.append(f"[full] {integrand}: collapsed to 0")
            elif 'Subst' in str(result):
                failures.append(f"[full] {integrand}: unresolved Subst -> {result}")
            elif not _derivative_matches(
                    result, integrand, **({'points': points} if points else {})):
                failures.append(f"[full] {integrand}: d/dx != integrand -> {result}")
        except Exception as exc:  # noqa: BLE001 - report which integrand blew up
            failures.append(f"[full] {integrand}: {type(exc).__name__}: {exc}")
    return failures


# Symbolic-coefficient integrals: Rubi rules use With[{a=D[u,x], b=D[v,x]}, ...]
# with locals literally named a, b, ... Naive substitution let those locals
# clobber the integrand's symbolic a, b (a+b*x -> D[u,x]+b*x), silently corrupting
# the result. Guards the With/Module/Block lexical-scoping fix (base_objects
# _rename_scoped_locals) plus the hyper TupleArg round-trip fix. Checked
# numerically (d/dx == integrand) at concrete parameter values.
_a, _b, _c, _d = sympy.symbols('a b c d')
_SYMBOLIC_COEFF_INTEGRANDS = [
    (_a + _b*x)**3,
    x*(_a + _b*x)**2,
    x**2*(_a + _b*x)**3,
    sqrt(_a + _b*x),
    1/sqrt(_a + _b*x),
    (_a + _b*x)**(-2),
    1/((_a + _b*x)*(_c + _d*x)),
    x*exp(_a + _b*x),
    exp(_a + _b*x)/x,
    sin(_a + _b*x),
    sqrt(_a + _b*x)/x,          # hyper round-trip fix
    1/(x*sqrt(_a + _b*x)),      # hyper round-trip fix
    x/(_a + _b*x),              # SubstFor deferred-delegation fix (was b x too big)
    (_a + _b*x)/(_c + _d*x),    # SubstFor fix
    log(_a + _b*x),             # SubstFor fix
    log(_a + _b*x)/x,           # PolynomialRemainder transcendental fix (-> polylog)
    x**2/(_a + _b*x)**sympy.Rational(3, 2),   # SubstFor fix
    # deferred-ExpandIntegrand fix: these fed an infinite descent (coeffs squaring
    # each level) -- x/(a+b*x)^2 TIMED OUT, x^2/(a+b*x)^2 "solved" to a junk form
    # carrying 1073741824*b**30. See _check_no_giant_coefficients below.
    x/(_a + _b*x)**2,
    x**2/(_a + _b*x)**2,
    x**3/(_a + _b*x)**2,
    # x^m/(a+b x^n) with GCD(m+1,n) > 1: the GCD-reduction rule (substitute u=x^GCD)
    # must fire ahead of the odd-m root-sum rule. Its guard is a bare relational
    # `Ne(GCD(m+1,n), 1)` whose WildSymbols never substituted (Symbol('m') !=
    # WildSymbol('m')) and whose GCD stayed unevaluated -> the rule was silently
    # disabled and these returned a WRONG I*ArcTan answer. See test_constraint_checker_*.
    x/(_a + _b*x**6),
    x**3/(_a + _b*x**6),
    x/(_a + _b*x**10),
    # x^2 (c+d x)/Sqrt[c^2-d^2 x^2]: used to CRASH with IndexError in
    # FractionalPowerFactorQ -- its `if ProductQ(u)` resolved to the ProductQ constraint
    # CLASS (always truthy) and its `u.args[1:]` handed a bare tuple that the recursion
    # peeled to empty args. See TestFractionalPowerFactorQ.
    x**2*(_c + _d*x)/sqrt(_c**2 - _d**2*x**2),
]


# log(c*x^n) times a polynomial in x. Rubi integrates these by parts through
# IntHide[u,x] := Block[{$ShowSteps=False}, Int[u,x]] (which recursively integrates
# the polynomial factor) and a 2-arg Dist[u,v] that distributes u over v's terms.
# IntHide used to be a no-op stub (returned itself) and 2-arg Dist raised a
# missing-argument TypeError, so these came back Unintegrable. Verified numerically.
_e, _n = sympy.symbols('e n')
_LOG_POLY_INTEGRANDS = [
    x**3*(_a + _b*log(_c*x**_n))*(_d + _e*x),
    x**2*(_a + _b*log(_c*x**_n)),
    x*(_a + _b*log(_c*x**_n)),
]


def _check_symbolic_group(label, integrands, subs0, pts, unsolved_markers):
    """Shared body for the symbolic-coefficient integrand groups.

    Returns a list of failure descriptions (empty == all good). `unsolved_markers`
    are substrings that mark an unsolved result (e.g. 'CannotIntegrate').
    """
    failures = []
    for integrand in integrands:
        try:
            result = rubi_integrate(integrand, x)
            if result.has(Function('Int')) or any(m in str(result) for m in unsolved_markers):
                failures.append(f"[{label}] {integrand}: unsolved -> {result}")
            elif not _numeric_matches(result, integrand, subs0, pts):
                failures.append(f"[{label}] {integrand}: d/dx != integrand -> {result}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[{label}] {integrand}: {type(exc).__name__}: {exc}")
    return failures


def _check_log_times_polynomial():
    """log(c*x^n)*poly(x) integrals resolve via IntHide + 2-arg Dist (by parts).

    Regression guard for the IntHide no-op-stub bug and the 2-arg Dist[u,v]
    missing-argument bug; both made these come back Unintegrable.
    """
    return _check_symbolic_group(
        'log*poly', _LOG_POLY_INTEGRANDS,
        {_a: 2, _b: 3, _c: 5, _d: 7, _e: 11, _n: 2}, (0.35, 0.6, 1.1, 1.7),
        ('Unintegrable', 'CannotIntegrate'))


# Rational functions of a single exponential f(E^(a+b x)). Rubi integrates these
# via the FunctionOfExponential substitution (rule 2.3:[96] / MMA rule 2692):
# v = FunctionOfExponential[u,x] = E^(a+b x), then Int[FunctionOfExponentialFunction[u,x]/x].
# That rule was DROPPED by codegen (its guard has an F_[v_] function-head wildcard),
# so the whole family returned CannotIntegrate. Codegen now drops only the
# untranslatable exclusionary guard and keeps the rule. Verified against Rubi on
# the Pi (e.g. 1/(a+b E^x) -> x/a - Log[a+b E^x]/a). Checked numerically.
_a2, _b2, _c2, _d2 = sympy.symbols('a b c d')
_FUNCTION_OF_EXP_INTEGRANDS = [
    1/(_a2 + _b2*exp(x)),
    1/(1 + exp(x)),
    1/(_a2 + _b2*exp(_c2 + _d2*x)),
    exp(x)/(_a2 + _b2*exp(2*x)),
    1/(exp(x) - exp(-x)),
]


def _check_function_of_exponential():
    """Rational functions of a single exponential integrate via rule 2.3:[96].

    Regression guard for the FunctionOfExponential substitution rule, recovered by
    making codegen tolerate an untranslatable exclusionary (function-head-wildcard)
    guard instead of dropping the whole rule.
    """
    return _check_symbolic_group(
        'f(e^x)', _FUNCTION_OF_EXP_INTEGRANDS,
        {_a2: 2, _b2: 3, _c2: 5, _d2: 7}, (0.35, 0.6, 1.1, 1.7),
        ('CannotIntegrate',))


def _check_symbolic_coefficients():
    """Integrals with symbolic coefficients a, b, c, d integrate correctly.

    Regression guard for the With/Module/Block local-variable capture bug and the
    hyper TupleArg round-trip bug.
    """
    return _check_symbolic_group(
        'symbolic', _SYMBOLIC_COEFF_INTEGRANDS,
        {_a: 2, _b: 3, _c: 5, _d: 7}, (0.35, 0.6, 1.1, 1.7),
        ('CannotIntegrate',))


# Integrands that used to crash the DFS via a deferred-node / utility-function bug
# (all now solved; verified numerically). Guards:
#  - Coeff[u,x,n] with symbolic n (deferred re-impl did int(n) -> TypeError)
#  - atanh(a+b*x)^2: Less/Greater on a non-real (-2*I) raised TypeError
_p3, _A3, _B3 = sympy.symbols('p A B')
_DEFERRED_CRASH_INTEGRANDS = [
    x**3*(_a + _b*atanh(_c*x)),                      # symbolic-n Coeff (atanh family)
    x**2*log(_c*(_a + _b*x**2)**_p3),                # symbolic-n Coeff (log family)
    atanh(_a + _b*x)**2,                             # Less/Greater non-real guard
    exp(acoth(_a*x)),                                # zoo-result must be rejected
    x*exp(acoth(_a*x)),                              # (finite rule preferred over zoo)
]


def _check_deferred_crash_fixes():
    """Integrands that used to abort the DFS with a TypeError in a deferred node
    or comparison utility. See bugs 10-11 in the project memory."""
    return _check_symbolic_group(
        'crash-fix', _DEFERRED_CRASH_INTEGRANDS,
        {_a: 2, _b: 3, _c: 5, _p3: sympy.Rational(3, 2), _A3: 1, _B3: 1},
        (0.35, 0.6, 1.1, 1.7), ('CannotIntegrate',))


# Integrands that used to raise inside rubi_integrate's own preprocessing (not a
# rule): a NESTED exp such as exp(x + exp(x)) is rebuilt into Pow(E, ...) mid-walk
# under exp_is_pow, so `.replace(sympy.exp, lambda u: ...)` re-matched the new Pow
# and called the 1-arg lambda with the Pow's 2 args. These must integrate or return
# CannotIntegrate -- never raise.
_NO_CRASH_INTEGRANDS = [
    (exp(x) + 1)*exp(x + exp(x))/(x + exp(x)),
    exp(x + exp(x)),
    exp(exp(x)),
    # csc(a+b x)^2/(c+d x): a DeactivateTrig rule's replacement embeds If[MatchQ[f,
    # f1*Complex(0,j)], ...] whose MatchQ-local wildcards leaked -- matchpy_to_sympy
    # raised SympifyError: Wildcard.dot('f1'). Now converts to a WildSymbol (no crash)
    # and the wildcard-laden branch is rejected by _dfs_is_clean, so the result is a
    # clean Unintegrable (Rubi returns Defer[Int] here too).
    sympy.csc(_a + _b*x)**2/(_c + _d*x),
]


def _check_no_crash():
    """Previously-crashing integrands must not raise (solved or CannotIntegrate)."""
    failures = []
    for integrand in _NO_CRASH_INTEGRANDS:
        try:
            rubi_integrate(integrand, x)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[no-crash] {integrand}: {type(exc).__name__}: {exc}")
    return failures


def test_compound_expression_set_binding_no_leaked_local():
    """Rule 1.1.3.2 #37 (x^m/(a+b x^n) partial fractions) uses
    Module[{r,s,k,u}, u = Int[f(k)]; ... Sum[u, {k, 1, N}]]. The u=... binding is a
    CompoundExpression side effect; before the fix it was dropped, so the scoping
    Dummy for u leaked into the Sum and the antiderivative was WRONG. Verify: no bare
    u/z symbol survives, and the derivative matches the integrand numerically."""
    from sympy import Symbol, sqrt, Float, I, diff
    xx, a, b, A, B = (Symbol(s) for s in 'x a b A B'.split())
    for u in (sqrt(xx)*(A + B*xx**3)/(a + b*xx**3),
              xx**2/(a + b*xx**6),
              sqrt(xx)/(a + b*xx**3)):
        r = rubi_integrate(u, xx)
        assert not any(str(s) in ('u', 'z') or str(s).startswith(('_u', '_z'))
                       for s in r.free_symbols), (u, r)
        # numeric derivative check at a generic complex point (reliable regardless of branch)
        pt = {s: Float(0.4 + 0.3 * (i + 1)) + Float(0.2 * (i + 1)) * I
              for i, s in enumerate(sorted(r.free_symbols, key=str))}
        val = complex((diff(r, xx) - u).subs(pt).evalf(30))
        assert abs(val) < 1e-8, (u, abs(val))


def test_polynomial_remainder_surd_coeffs_do_not_crash():
    """PolynomialQuotient/Remainder on surd-coefficient polynomials must not raise.

    Integrands like (a+b*x)**4/(c+d*x**3) factor c+d*x**3 into pieces with (c/d)**(1/3)
    coefficients; a Rubi EqQ constraint then runs PolynomialRemainder over the EX
    domain, where SymPy cannot detect zero and raises PolynomialDivisionFailed. That
    is a *sibling* of PolynomialError (not a subclass), so it escaped the original
    `except sympy.PolynomialError` and crashed the whole integration. The deferred
    nodes must instead fall back gracefully so the rule simply does not apply.
    """
    from sympy import Rational, Symbol
    from rubi_rules.utils.rubi_utils import PolynomialRemainder, PolynomialQuotient
    xx, a, b, c, d = (Symbol(s) for s in 'x a b c d'.split())
    r = (c/d)**Rational(1, 3)
    p = xx**2 - r*xx + r**2
    q = (-a**4*d + 4*a**3*b*d*r + 4*a*b**3*c - b**4*c*r)*xx \
        + (2*a**4*d*r + 4*a**3*b*d*r**2 - 8*a*b**3*c*r - b**4*c*r**2)
    # Guard: these exact inputs really do defeat SymPy's raw division (else the test
    # would silently stop covering the bug).
    with pytest.raises(sympy.polys.polyerrors.PolynomialDivisionFailed):
        sympy.rem(p, q, xx)
    # The Rubi deferred nodes must swallow that and return something, not raise.
    assert PolynomialRemainder(p, q, xx).doit() is not None
    assert PolynomialQuotient(p, q, xx).doit() is not None


def _check_inthide():
    """IntHide[u,x] := Block[{$ShowSteps=False}, Int[u,x]] actually integrates u.

    It used to be a no-op stub (returned itself), breaking every rule that binds a
    With/Module local to IntHide[...] (3.1.4, inverse-hyperbolic families, ...).
    Needs the full rule set because IntHide calls rubi_integrate internally.
    """
    from rubi_rules.utils.rubi_utils import IntHide as _IntHide
    d, e = sympy.Symbol('d'), sympy.Symbol('e')
    got = _IntHide(x**3*(d + e*x), x).doit()
    if sympy.simplify(got - (d*x**4/4 + e*x**5/5)) != 0:
        return [f"[IntHide] x^3*(d+e*x): {got} != d*x^4/4 + e*x^5/5"]
    return []


# Rules over an UNKNOWN function: Derivative[n_][f_][x_], plus the sum-patterned
# product/quotient rules. These cover three things that were each separately broken:
#   * WildcardOperationHead matching (a wildcard used as a function HEAD);
#   * the sympy.Tuple head registration -- Derivative stores its (var, order) spec
#     as a Tuple, and while that was unregistered a round-trip silently turned
#     Derivative into an undefined function, which made the inert-trig catch-all
#     misfire and return 0 for the product rule;
#   * offering a SUM to the matcher before splitting it term-by-term, without which
#     a rule whose pattern IS a sum can never fire.
_f, _g = Function('f'), Function('g')


def _check_derivative_of_unknown_function():
    fp = sympy.Derivative(_f(x), x)
    gp = sympy.Derivative(_g(x), x)
    cases = [
        ("f'", fp, _f(x)),
        ("f''", sympy.Derivative(_f(x), (x, 2)), sympy.Derivative(_f(x), x)),
        ("g'''", sympy.Derivative(_g(x), (x, 3)), sympy.Derivative(_g(x), (x, 2))),
        ("product rule", fp*_g(x) + _f(x)*gp, _f(x)*_g(x)),
        ("quotient rule", (fp*_g(x) - _f(x)*gp)/_g(x)**2, _f(x)/_g(x)),
    ]
    failures = []
    for name, integrand, expected in cases:
        try:
            got = rubi_integrate(integrand, x)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[deriv] {name}: {type(exc).__name__}: {exc}")
            continue
        if 'CannotIntegrate' in str(got) or 'Int(' in str(got):
            failures.append(f"[deriv] {name}: unsolved -> {got}")
            continue
        if sympy.simplify(got - expected) != 0:
            failures.append(f"[deriv] {name}: {got} != {expected}")
    return failures


def _check_plain_sums_still_split():
    """The whole-sum attempt must not disturb ordinary term-by-term integration."""
    cases = [
        (x**2 + sin(x), x**3/3 - cos(x)),
        (exp(x) + 1/x + cos(x), exp(x) + log(x) + sin(x)),
        (1/(1 + x) + 1/(1 + x**2), log(x + 1) + atan(x)),
        (sqrt(x) + x**3 - 5, 2*x**sympy.Rational(3, 2)/3 + x**4/4 - 5*x),
    ]
    failures = []
    for integrand, expected in cases:
        got = rubi_integrate(integrand, x)
        if sympy.simplify(got - expected) != 0:
            failures.append(f"[sum] {integrand}: {got} != {expected}")
    return failures


def _check_matchq_gate_is_a_noop():
    """With `ENFORCE_MATCHQ` off, MatchQ must never be consulted while integrating.

    That is the whole safety argument for the gate: if `check()` is never called,
    the gated path is logically IDENTICAL to the always-permissive behaviour this
    port has always had, so enabling the implementation cannot have changed any
    result. Asserted directly, because the obvious alternative -- comparing
    solvability counts on a corpus sample -- is dominated by per-integral timeout
    noise on a loaded machine and cannot distinguish a real change from jitter.
    """
    import rubi_rules.base_objects as bo
    from rubi_rules.utils import constraints_wolfram as cw

    if bo.ENFORCE_MATCHQ:
        return []          # enforcement deliberately switched on; nothing to assert

    calls = []
    original = cw.MatchQ.check
    cw.MatchQ.check = lambda self, **kw: (calls.append(1), original(self, **kw))[1]
    try:
        for integrand in (x*sympy.sqrt(1 + x), 1/(1 + x)**2, log(1 + x)/x,
                          sin(x)*cos(x), x**3*log(x)):
            try:
                rubi_integrate(integrand, x)
            except Exception:  # noqa: BLE001 - a failure here is another test's problem
                pass
    finally:
        cw.MatchQ.check = original

    if calls:
        return [f"[matchq-gate] MatchQ.check() called {len(calls)}x despite "
                f"ENFORCE_MATCHQ=False; the gate is not a no-op"]
    return []


def _check_hyperbolic_secant_via_deactivation():
    """sech^m(a+b sech^n)^p has no dedicated rules; Rubi (and now our port) solves
    it by deactivating sech(z)->inert sec(I z) and using the circular sec rules.
    Verified against real Rubi on the Pi. Answers checked by differentiation."""
    a, b = sympy.Symbol('a'), sympy.Symbol('b')
    c, d = sympy.Symbol('c'), sympy.Symbol('d')
    cases = [
        sympy.sech(c + d*x)**2/(a + b*sympy.sech(c + d*x)**2),
        1/(a + b*sympy.sech(c + d*x)**2),
        (a + b*sympy.sech(c + d*x)**2)*sympy.sinh(c + d*x),
    ]
    subs0 = {a: 2, b: 3, c: sympy.Rational(1, 2), d: sympy.Rational(7, 10)}
    failures = []
    for u in cases:
        try:
            r = rubi_integrate(u, x)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[sech] {u}: {type(exc).__name__}: {exc}")
            continue
        if 'CannotIntegrate' in str(r) or 'Int(' in str(r):
            failures.append(f"[sech] {u}: unsolved -> {r}")
            continue
        dr = sympy.diff(r, x) - u
        ok = sum(1 for pt in (0.3, 0.6, 0.9, 1.2)
                 if abs(complex(dr.subs(subs0).subs(x, pt).evalf())) < 1e-7)
        if ok < 2:
            failures.append(f"[sech] {u}: d/dx(result) != integrand -> {r}")
    return failures


def _check_no_giant_coefficients():
    """The x^n/(a+b*x)^2 family must integrate to a SMALL-coefficient closed form.

    The deferred-ExpandIntegrand bug did not always time out: x^2/(a+b*x)^2 still
    "solved", but to a mathematically-correct junk form carrying 1073741824*b**30
    from the geometric coefficient blow-up. Verifying the derivative alone would
    pass that, so this guards the coefficient magnitude directly -- a correct
    antiderivative of these has single-digit integer coefficients.
    """
    a, b = sympy.Symbol('a'), sympy.Symbol('b')
    failures = []
    for integrand in (x/(a + b*x)**2, x**2/(a + b*x)**2, x**3/(a + b*x)**2):
        try:
            result = rubi_integrate(integrand, x)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[giant-coeff] {integrand}: {type(exc).__name__}: {exc}")
            continue
        if 'CannotIntegrate' in str(result) or 'Int(' in str(result):
            failures.append(f"[giant-coeff] {integrand}: unsolved -> {result}")
            continue
        biggest = max((abs(int(n)) for n in result.atoms(sympy.Integer)), default=0)
        if biggest > 1000:
            failures.append(
                f"[giant-coeff] {integrand}: coefficient blow-up (max |int| = {biggest}), "
                f"the deferred-ExpandIntegrand loop is back")
        if sympy.simplify(sympy.diff(result, x) - integrand) != 0:
            failures.append(f"[giant-coeff] {integrand}: d/dx != integrand -> {result}")
    return failures


@pytest.mark.slow
def test_full_ruleset_integrals():
    """The one test that loads the entire Rubi rule set (~50s, then cached).

    Loading the full rule set is a costly one-time operation, so EVERY check that
    needs it lives here: each `_check_*` subfunction returns its failures and they
    are asserted together, so the rule set is loaded exactly once and every failing
    integrand across all groups is reported in a single message. Do NOT add more
    `@pytest.mark.slow` full-rule-set tests -- add a `_check_*` subfunction and call
    it from here instead.
    """
    failures = []
    failures += _check_full_ruleset()            # broad spread across categories
    failures += _check_symbolic_coefficients()   # symbolic a,b,c,d (scoping/hyper)
    failures += _check_log_times_polynomial()     # IntHide + 2-arg Dist (by parts)
    failures += _check_function_of_exponential()  # FunctionOfExponential subst (rule 96)
    failures += _check_inthide()                  # IntHide delegates to rubi_integrate
    failures += _check_deferred_crash_fixes()     # symbolic-n Coeff + non-real compare
    failures += _check_no_crash()                 # nested-exp preprocessing crash
    failures += _check_derivative_of_unknown_function()  # Derivative[n_][f_][x_] + sum rules
    failures += _check_plain_sums_still_split()         # whole-sum attempt is non-invasive
    failures += _check_matchq_gate_is_a_noop()          # ENFORCE_MATCHQ off == old behaviour
    failures += _check_no_giant_coefficients()          # deferred-ExpandIntegrand loop
    failures += _check_hyperbolic_secant_via_deactivation()  # sech via inert-sec deactivation
    assert not failures, (
        f"{len(failures)} integral(s) failed:\n" + "\n".join(failures))
