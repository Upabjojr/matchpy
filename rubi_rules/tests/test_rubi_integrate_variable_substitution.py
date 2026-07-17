# -*- coding: utf-8 -*-
"""Tests for rubi_integrate variable-substitution logic.

The Rubi rule files all use Symbol('x') as the canonical integration variable.
rubi_integrate() accepts any variable and performs a three-step substitution:

    1. Park the existing Symbol('x') in expr under a Dummy to avoid collision.
    2. Rename the user's integration variable -> Symbol('x').
    3. Integrate with respect to Symbol('x').
    4. Undo: Symbol('x') -> original variable, Dummy -> Symbol('x').

These tests cover the substitution logic in isolation (using the fast
r_1_1_1_1 rule set) so they run without loading the full rule library.
"""
import pytest
import sympy
from sympy import Symbol, Rational, simplify, symbols

from rubi_rules.base_objects import _preprocess_integrate, build_tracing_replacer


# ---------------------------------------------------------------------------
# Fixture — only r_1_1_1_1 rules (powers of linear expressions); fast to load
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def replacer():
    from rubi_rules.rules.r_1_algebraic_functions.r_1_1_binomial_products \
        .r_1_1_1_linear.r_1_1_1_1 import RULES
    return build_tracing_replacer(RULES)


# ---------------------------------------------------------------------------
# Helper — same substitution logic as rubi_integrate but takes a replacer
# directly (avoids the global _CACHED_REPLACER so tests are isolated)
# ---------------------------------------------------------------------------

def _integrate(expr, var, replacer):
    """Integrate expr w.r.t. var using the given replacer.

    Replicates the variable-substitution logic of rubi_integrate() so these
    tests exercise that logic without touching the global rule cache.
    """
    expr = sympy.sympify(expr)
    var = sympy.sympify(var)
    x_canonical = Symbol('x')

    if var == x_canonical:
        return _preprocess_integrate(expr, x_canonical, replacer)[0]

    dummy = sympy.Dummy('_x_var')
    expr_sub = expr.subs(x_canonical, dummy).subs(var, x_canonical)
    result, matched_rule = _preprocess_integrate(expr_sub, x_canonical, replacer)
    return result.subs(x_canonical, var).subs(dummy, x_canonical)


# ---------------------------------------------------------------------------
# Symbols shared across test classes
# ---------------------------------------------------------------------------

x, y, z, t = symbols('x y z t')
a, b, n = symbols('a b n')


# ---------------------------------------------------------------------------
# Canonical path: integration variable IS Symbol('x') — no substitution
# ---------------------------------------------------------------------------

class TestCanonicalVariable:
    """Variable is already Symbol('x') — substitution logic must be a no-op."""

    def test_x_squared(self, replacer):
        assert simplify(_integrate(x**2, x, replacer) - x**3/3) == 0

    def test_x_times_y(self, replacer):
        """y is a free parameter; x is the integration variable."""
        result = _integrate(x * y, x, replacer)
        assert simplify(result - x**2 * y / 2) == 0

    def test_x_symbolic_exponent(self, replacer):
        result = _integrate(x**n, x, replacer)
        assert simplify(result - x**(n + 1) / (n + 1)) == 0


# ---------------------------------------------------------------------------
# Non-canonical variable with NO existing x in the expression
# ---------------------------------------------------------------------------

class TestNonCanonicalVariableNoXInExpr:
    """Integration variable != x, and x does not appear in the expression."""

    def test_y_squared(self, replacer):
        result = _integrate(y**2, y, replacer)
        assert simplify(result - y**3/3) == 0

    def test_y_cubed(self, replacer):
        result = _integrate(y**3, y, replacer)
        assert simplify(result - y**4/4) == 0

    def test_t_symbolic_exponent(self, replacer):
        result = _integrate(t**n, t, replacer)
        assert simplify(result - t**(n + 1) / (n + 1)) == 0

    def test_constant_times_t(self, replacer):
        result = _integrate(5 * t, t, replacer)
        assert simplify(result - Rational(5, 2) * t**2) == 0

    def test_z_half(self, replacer):
        result = _integrate(z**Rational(1, 2), z, replacer)
        assert simplify(result - Rational(2, 3) * z**Rational(3, 2)) == 0


# ---------------------------------------------------------------------------
# Non-canonical variable WITH existing x in the expression (collision case)
# ---------------------------------------------------------------------------

class TestNonCanonicalVariableWithXInExpr:
    """Critical: x appears in expr but is NOT the integration variable.

    This is the case that requires the Dummy symbol to prevent x from being
    accidentally renamed to the user's integration variable.

    e.g. rubi_integrate(x*y, y):
        wrong (without Dummy): x*y -> x*x = x^2, Int(x^2, x) = x^3/3
        correct (with Dummy):  x -> dummy, y -> x: dummy*x, Int(dummy*x, x)
                                = dummy*x^2/2 -> x*y^2/2
    """

    def test_x_times_y_wrt_y(self, replacer):
        """The headline example: x is a constant w.r.t. y."""
        result = _integrate(x * y, y, replacer)
        assert simplify(result - x * y**2 / 2) == 0

    def test_x_times_y_collision_check(self, replacer):
        """Verify result is x*y**2/2, NOT x**2*y/2 (collision bug)."""
        result = _integrate(x * y, y, replacer)
        wrong = x**2 * y / 2
        assert simplify(result - wrong) != 0, (
            "Dummy substitution failed — x was renamed instead of y"
        )

    def test_x_squared_times_y_wrt_y(self, replacer):
        result = _integrate(x**2 * y, y, replacer)
        assert simplify(result - x**2 * y**2 / 2) == 0

    def test_x_times_y_squared_wrt_y(self, replacer):
        result = _integrate(x * y**2, y, replacer)
        assert simplify(result - x * y**3 / 3) == 0

    def test_x_times_z_wrt_z(self, replacer):
        result = _integrate(x * z, z, replacer)
        assert simplify(result - x * z**2 / 2) == 0

    def test_x_squared_times_z_cubed_wrt_z(self, replacer):
        result = _integrate(x**2 * z**3, z, replacer)
        assert simplify(result - x**2 * z**4 / 4) == 0

    def test_x_times_y_times_z_wrt_z(self, replacer):
        result = _integrate(x * y * z, z, replacer)
        assert simplify(result - x * y * z**2 / 2) == 0

    def test_x_symbolic_exponent_wrt_y(self, replacer):
        """x^n is a constant factor when integrating w.r.t. y."""
        result = _integrate(x**n * y, y, replacer)
        assert simplify(result - x**n * y**2 / 2) == 0


# ---------------------------------------------------------------------------
# Symmetry: swapping integration variable must swap the result
# ---------------------------------------------------------------------------

class TestSymmetry:
    """Int(x*y, x) and Int(x*y, y) must be symmetric in x and y."""

    def test_xy_wrt_x_vs_y(self, replacer):
        result_x = _integrate(x * y, x, replacer)   # x**2*y/2
        result_y = _integrate(x * y, y, replacer)   # x*y**2/2
        # xreplace does simultaneous substitution (subs is sequential)
        assert simplify(result_x.xreplace({x: y, y: x}) - result_y) == 0

    def test_x2_y2_wrt_x_vs_y(self, replacer):
        result_x = _integrate(x**2 * y**2, x, replacer)   # x**3*y**2/3
        result_y = _integrate(x**2 * y**2, y, replacer)   # x**2*y**3/3
        assert simplify(result_x.xreplace({x: y, y: x}) - result_y) == 0
