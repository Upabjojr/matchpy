# -*- coding: utf-8 -*-
"""Advanced polynomial equation solver using FreeOf constraints.

Demonstrates a many-to-one pattern matching approach where:
- FreeOf constraints ensure coefficients are free of the solving variable
- Optional WildSymbol defaults let a single quadratic pattern cover monic and
  missing-term cases
- Expressions like y*x² + 3*z*x + 5 = 0 correctly identify y, 3*z, 5 as
  coefficients (all free of x) and solve using the quadratic formula

This is the key use case for FreeOf: in a commutative+associative operation like
Mul(3, z, x), the pattern Mul(b_, x) matches with b_ = Mul(3, z). The FreeOf('b', 'x')
constraint then verifies that Mul(3, z) does NOT contain x — confirming it's a valid
coefficient.

Patterns use the WildSymbol type which participates in SymPy expression trees
naturally and converts to OmniMatch wildcards through to_omnimatch_expression.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sympy
from sympy import symbols, sqrt, Eq, Rational, simplify, solve, Poly, cbrt, Integer

from omnimatch.expressions.expressions import (
    Operation, Pattern, to_omnimatch_expression,
)
from omnimatch.expressions.constraints import FreeOf
from omnimatch.matching.many_to_one import ManyToOneMatcher, ManyToOneReplacer
from omnimatch import functions as omnimatch_functions

from sympy_matching.operations import SIN, EQUALITY
from sympy_matching.conversion import omnimatch_to_sympy
from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

x, y, z, w = symbols('x y z w')


# ─── Solver construction ──────────────────────────────────────────────────────

def make_polynomial_solver(var_name: str = 'x'):
    """Build a ManyToOneReplacer that solves polynomial equations for `var_name`.

    A single linear pattern and a single quadratic pattern are enough here,
    because optional WildSymbol defaults cover implicit coefficients and
    missing terms:
    * a_ defaults to 1
    * b_ defaults to 0
    * c_ defaults to 0
    """
    var = sympy.Symbol(var_name)

    # IDENTITY_ELEMENT resolves to the parent operation's identity:
    # - in Mul context: defaults to 1 (missing coefficient = 1)
    # - in Add context: defaults to 0 (missing term = 0)
    a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
    b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
    c_ = WildSymbol('c_', optional_value=IDENTITY_ELEMENT)

    a_free = FreeOf('a', var_name)
    b_free = FreeOf('b', var_name)
    c_free = FreeOf('c', var_name)

    rules = []

    linear = Pattern(
        to_omnimatch_expression(Eq(a_ * var + b_, 0)),
        a_free, b_free,
    )

    def solve_linear(a, b):
        a_s = omnimatch_to_sympy(a)
        b_s = omnimatch_to_sympy(b)
        var_s = sympy.Symbol(var_name)
        return to_omnimatch_expression(Eq(var_s, -b_s / a_s))

    rules.append(omnimatch_functions.ReplacementRule(linear, solve_linear))

    quadratic = Pattern(
        to_omnimatch_expression(Eq(a_ * var**2 + b_ * var + c_, 0)),
        a_free, b_free, c_free,
    )

    def solve_quadratic(a, b, c):
        a_s = omnimatch_to_sympy(a)
        b_s = omnimatch_to_sympy(b)
        c_s = omnimatch_to_sympy(c)
        var_s = sympy.Symbol(var_name)
        discriminant = b_s**2 - 4 * a_s * c_s
        sol1 = (-b_s + sqrt(discriminant)) / (2 * a_s)
        sol2 = (-b_s - sqrt(discriminant)) / (2 * a_s)
        return to_omnimatch_expression([Eq(var_s, sol1), Eq(var_s, sol2)])

    rules.append(omnimatch_functions.ReplacementRule(quadratic, solve_quadratic))

    # Pattern: a*x² + c = 0 (no linear term — needed because Mul(b_, var) is
    # compound and can't vanish from Add; requires a separate pattern).
    quadratic_no_linear = Pattern(
        to_omnimatch_expression(Eq(a_ * var**2 + c_, 0)),
        a_free, c_free,
    )

    def solve_quadratic_no_linear(a, c):
        a_s = omnimatch_to_sympy(a)
        c_s = omnimatch_to_sympy(c)
        var_s = sympy.Symbol(var_name)
        discriminant = -4 * a_s * c_s
        sol1 = sqrt(discriminant) / (2 * a_s)
        sol2 = -sqrt(discriminant) / (2 * a_s)
        return to_omnimatch_expression([Eq(var_s, sol1), Eq(var_s, sol2)])

    rules.append(omnimatch_functions.ReplacementRule(quadratic_no_linear, solve_quadratic_no_linear))

    # ─── Cubic: a*x³ + b*x² + c*x + d = 0 ────────────────────────────────

    d_ = WildSymbol('d_', optional_value=IDENTITY_ELEMENT)
    d_free = FreeOf('d', var_name)

    cubic = Pattern(
        to_omnimatch_expression(Eq(a_ * var**3 + b_ * var**2 + c_ * var + d_, 0)),
        a_free, b_free, c_free, d_free,
    )

    def solve_cubic(a, b, c, d):
        a_s = omnimatch_to_sympy(a)
        b_s = omnimatch_to_sympy(b)
        c_s = omnimatch_to_sympy(c)
        d_s = omnimatch_to_sympy(d)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s * var_s**3 + b_s * var_s**2 + c_s * var_s + d_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(cubic, solve_cubic))

    # Cubic without quadratic term: a*x³ + c*x + d = 0
    cubic_no_quad = Pattern(
        to_omnimatch_expression(Eq(a_ * var**3 + c_ * var + d_, 0)),
        a_free, c_free, d_free,
    )

    def solve_cubic_no_quad(a, c, d):
        a_s = omnimatch_to_sympy(a)
        c_s = omnimatch_to_sympy(c)
        d_s = omnimatch_to_sympy(d)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s * var_s**3 + c_s * var_s + d_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(cubic_no_quad, solve_cubic_no_quad))

    # Cubic without linear and quadratic terms: a*x³ + d = 0
    cubic_pure = Pattern(
        to_omnimatch_expression(Eq(a_ * var**3 + d_, 0)),
        a_free, d_free,
    )

    def solve_cubic_pure(a, d):
        a_s = omnimatch_to_sympy(a)
        d_s = omnimatch_to_sympy(d)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s * var_s**3 + d_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(cubic_pure, solve_cubic_pure))

    # ─── Quartic: a*x⁴ + b*x³ + c*x² + d*x + e = 0 ──────────────────────

    e_ = WildSymbol('e_', optional_value=IDENTITY_ELEMENT)
    e_free = FreeOf('e', var_name)

    quartic = Pattern(
        to_omnimatch_expression(Eq(a_ * var**4 + b_ * var**3 + c_ * var**2 + d_ * var + e_, 0)),
        a_free, b_free, c_free, d_free, e_free,
    )

    def solve_quartic(a, b, c, d, e):
        a_s = omnimatch_to_sympy(a)
        b_s = omnimatch_to_sympy(b)
        c_s = omnimatch_to_sympy(c)
        d_s = omnimatch_to_sympy(d)
        e_s = omnimatch_to_sympy(e)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s*var_s**4 + b_s*var_s**3 + c_s*var_s**2 + d_s*var_s + e_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(quartic, solve_quartic))

    # Quartic without odd-power terms (biquadratic): a*x⁴ + c*x² + e = 0
    biquadratic = Pattern(
        to_omnimatch_expression(Eq(a_ * var**4 + c_ * var**2 + e_, 0)),
        a_free, c_free, e_free,
    )

    def solve_biquadratic(a, c, e):
        a_s = omnimatch_to_sympy(a)
        c_s = omnimatch_to_sympy(c)
        e_s = omnimatch_to_sympy(e)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s*var_s**4 + c_s*var_s**2 + e_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(biquadratic, solve_biquadratic))

    # Pure quartic: a*x⁴ + e = 0
    quartic_pure = Pattern(
        to_omnimatch_expression(Eq(a_ * var**4 + e_, 0)),
        a_free, e_free,
    )

    def solve_quartic_pure(a, e):
        a_s = omnimatch_to_sympy(a)
        e_s = omnimatch_to_sympy(e)
        var_s = sympy.Symbol(var_name)
        sols = solve(a_s*var_s**4 + e_s, var_s)
        return to_omnimatch_expression([Eq(var_s, s) for s in sols])

    rules.append(omnimatch_functions.ReplacementRule(quartic_pure, solve_quartic_pure))

    return ManyToOneReplacer(*rules)


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestLinearEquations:
    """Test solving linear equations with FreeOf-constrained coefficients."""

    @pytest.fixture
    def solver(self):
        return make_polynomial_solver('x')

    def test_simple_linear(self, solver):
        eq = to_omnimatch_expression(Eq(2 * x + 6, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(x, -3)

    def test_linear_negative_constant(self, solver):
        eq = to_omnimatch_expression(Eq(5 * x - 15, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(x, 3)

    def test_linear_symbolic_coefficient(self, solver):
        eq = to_omnimatch_expression(Eq(y * x + z, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(x, -z / y)

    def test_linear_compound_coefficient(self, solver):
        eq = to_omnimatch_expression(Eq(3 * y * x + 5 * z, 0))
        result = solver.replace(eq)
        result_sympy = omnimatch_to_sympy(result)
        expected = Eq(x, -5 * z / (3 * y))
        assert simplify(result_sympy.lhs - expected.lhs) == 0
        assert simplify(result_sympy.rhs - expected.rhs) == 0

    def test_linear_unit_coefficient(self, solver):
        eq = to_omnimatch_expression(Eq(x + 7, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(x, -7)


class TestQuadraticEquations:
    """Test solving quadratic equations with FreeOf-constrained coefficients."""

    @pytest.fixture
    def solver(self):
        return make_polynomial_solver('x')

    def test_quadratic_integer_coefficients(self, solver):
        eq = to_omnimatch_expression(Eq(x**2 - 5 * x + 6, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {sol.rhs for sol in result_sympy}
        assert solutions == {2, 3}

    def test_quadratic_with_leading_coefficient(self, solver):
        eq = to_omnimatch_expression(Eq(2 * x**2 + 7 * x + 3, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {sol.rhs for sol in result_sympy}
        assert solutions == {Rational(-1, 2), -3}

    def test_quadratic_symbolic_coefficients(self, solver):
        eq = to_omnimatch_expression(Eq(y * x**2 + 3 * z * x + 5, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        for sol in result_sympy:
            assert sol.lhs == x
            assert simplify(y * sol.rhs**2 + 3 * z * sol.rhs + 5) == 0

    def test_quadratic_no_linear_term(self, solver):
        eq = to_omnimatch_expression(Eq(4 * x**2 - 16, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {sol.rhs for sol in result_sympy}
        assert solutions == {2, -2}

    def test_quadratic_monic_no_linear(self, solver):
        eq = to_omnimatch_expression(Eq(x**2 - 9, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {sol.rhs for sol in result_sympy}
        assert solutions == {3, -3}

    def test_quadratic_monic_with_linear(self, solver):
        eq = to_omnimatch_expression(Eq(x**2 + 2 * x - 8, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {sol.rhs for sol in result_sympy}
        assert solutions == {2, -4}


class TestFreeQFiltering:
    """Test that FreeOf correctly rejects invalid matches."""

    def test_does_not_match_when_coeff_contains_var(self):
        solver = make_polynomial_solver('x')
        eq = to_omnimatch_expression(Eq(x**2 + 3, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        assert isinstance(result_sympy, list)
        assert len(result_sympy) == 2
        for sol in result_sympy:
            assert sol.lhs == x
            assert simplify(sol.rhs**2 + 3) == 0

    def test_freeq_with_nested_variable(self):
        """sin(x)*x + 5 = 0 — sin(x) contains x, so not a valid coefficient."""
        subject = to_omnimatch_expression(Eq(sympy.sin(x) * x + 5, 0))
        solver = make_polynomial_solver('x')
        result = solver.replace(subject)
        # No pattern should match (sin(x) is not free of x)
        assert result == subject


class TestSolvingForDifferentVariables:
    """Test that the solver can be parameterized for different variables."""

    def test_solve_for_y(self):
        solver = make_polynomial_solver('y')
        eq = to_omnimatch_expression(Eq(3 * y + 9, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(y, -3)

    def test_solve_for_y_with_x_as_coefficient(self):
        solver = make_polynomial_solver('y')
        eq = to_omnimatch_expression(Eq(x * y + z, 0))
        result = solver.replace(eq)
        assert omnimatch_to_sympy(result) == Eq(y, -z / x)

    def test_solve_quadratic_for_z(self):
        solver = make_polynomial_solver('z')
        eq = to_omnimatch_expression(Eq(x * z**2 + y * z + w, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        for sol in result_sympy:
            assert sol.lhs == z
            assert simplify(x * sol.rhs**2 + y * sol.rhs + w) == 0


class TestCubicEquations:
    """Test solving cubic equations."""

    @pytest.fixture
    def solver(self):
        return make_polynomial_solver('x')

    def test_cubic_with_rational_roots(self, solver):
        """x³ - 6x² + 11x - 6 = 0 → x = 1, 2, 3"""
        eq = to_omnimatch_expression(Eq(x**3 - 6*x**2 + 11*x - 6, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {1, 2, 3}

    def test_cubic_depressed(self, solver):
        """x³ - 3x + 2 = 0 → x = 1, 1, -2"""
        eq = to_omnimatch_expression(Eq(x**3 - 3*x + 2, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {1, -2}

    def test_cubic_pure(self, solver):
        """x³ - 8 = 0 → x = 2 (real root among the three)"""
        eq = to_omnimatch_expression(Eq(x**3 - 8, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = [simplify(sol.rhs) for sol in result_sympy]
        assert 2 in solutions
        assert len(solutions) == 3

    def test_cubic_with_leading_coefficient(self, solver):
        """2x³ + 3x² - 11x - 6 = 0 → x = -3, -1/2, 2"""
        eq = to_omnimatch_expression(Eq(2*x**3 + 3*x**2 - 11*x - 6, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {-3, Rational(-1, 2), 2}

    def test_cubic_symbolic_coefficient(self, solver):
        """y*x³ + z = 0 → verify solutions satisfy the equation."""
        eq = to_omnimatch_expression(Eq(y*x**3 + z, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        for sol in result_sympy:
            assert sol.lhs == x
            assert simplify(y * sol.rhs**3 + z) == 0


class TestQuarticEquations:
    """Test solving quartic (4th degree) equations."""

    @pytest.fixture
    def solver(self):
        return make_polynomial_solver('x')

    def test_biquadratic_simple(self, solver):
        """x⁴ - 5x² + 4 = 0 → x = ±1, ±2"""
        eq = to_omnimatch_expression(Eq(x**4 - 5*x**2 + 4, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {1, -1, 2, -2}

    def test_biquadratic_with_coefficient(self, solver):
        """2x⁴ - 10x² + 8 = 0 → x = ±1, ±2"""
        eq = to_omnimatch_expression(Eq(2*x**4 - 10*x**2 + 8, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {1, -1, 2, -2}

    def test_quartic_full(self, solver):
        """x⁴ - 10x³ + 35x² - 50x + 24 = 0 → x = 1, 2, 3, 4"""
        eq = to_omnimatch_expression(Eq(x**4 - 10*x**3 + 35*x**2 - 50*x + 24, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = {simplify(sol.rhs) for sol in result_sympy}
        assert solutions == {1, 2, 3, 4}

    def test_quartic_pure(self, solver):
        """x⁴ - 16 = 0 → x = ±2, ±2i"""
        eq = to_omnimatch_expression(Eq(x**4 - 16, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        solutions = [simplify(sol.rhs) for sol in result_sympy]
        # Check real roots
        real_sols = {s for s in solutions if s.is_real}
        assert real_sols == {2, -2}
        assert len(solutions) == 4

    def test_quartic_symbolic_coefficient(self, solver):
        """y*x⁴ - z = 0 → verify solutions satisfy the equation."""
        eq = to_omnimatch_expression(Eq(y*x**4 - z, 0))
        result_sympy = omnimatch_to_sympy(solver.replace(eq))
        for sol in result_sympy:
            assert sol.lhs == x
            assert simplify(y * sol.rhs**4 - z) == 0


class TestManyToOneMatcherWithFreeQ:
    """Test using ManyToOneMatcher directly to classify equations by degree."""

    def test_classify_equation_degree(self):
        var = sympy.Symbol('x')
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
        c_ = WildSymbol('c_', optional_value=IDENTITY_ELEMENT)

        linear = Pattern(
            to_omnimatch_expression(Eq(a_ * var + b_, 0)),
            FreeOf('a', 'x'), FreeOf('b', 'x'),
        )

        quadratic = Pattern(
            to_omnimatch_expression(Eq(a_ * var**2 + b_ * var + c_, 0)),
            FreeOf('a', 'x'), FreeOf('b', 'x'), FreeOf('c', 'x'),
        )

        matcher = ManyToOneMatcher()
        matcher.add(linear, 'linear')
        matcher.add(quadratic, 'quadratic')

        eq1 = to_omnimatch_expression(Eq(2 * x + 3, 0))
        labels1 = [label for label, _ in matcher.match(eq1)]
        assert 'linear' in labels1
        assert 'quadratic' not in labels1

        eq2 = to_omnimatch_expression(Eq(3 * x**2 + 2 * x + 1, 0))
        labels2 = [label for label, _ in matcher.match(eq2)]
        assert 'quadratic' in labels2

    def test_extract_coefficients(self):
        var = sympy.Symbol('x')
        a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
        b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
        c_ = WildSymbol('c_', optional_value=IDENTITY_ELEMENT)

        quadratic = Pattern(
            to_omnimatch_expression(Eq(a_ * var**2 + b_ * var + c_, 0)),
            FreeOf('a', 'x'), FreeOf('b', 'x'), FreeOf('c', 'x'),
        )

        eq = to_omnimatch_expression(Eq(y * x**2 + 3 * z * x + 5, 0))
        matcher = ManyToOneMatcher(quadratic)
        results = list(matcher.match(eq))
        assert len(results) == 1

        _, subst = results[0]
        assert omnimatch_to_sympy(subst['a']) == y
        assert omnimatch_to_sympy(subst['b']) == 3 * z
        assert omnimatch_to_sympy(subst['c']) == 5
