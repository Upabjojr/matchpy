# -*- coding: utf-8 -*-
"""Tests for sympy_wolfram.mathematica_expressions.

Test cases derived from Wolfram Mathematica documentation examples.
"""
import pytest
import sympy
from sympy import Integer, Rational, S, Symbol, sqrt

from sympy_wolfram.mathematica_expressions import (
    Block,
    Catch,
    CompoundExpression,
    Do,
    Head,
    If,
    List,
    Module,
    Null,
    Reap,
    Return,
    Scan,
    Set,
    Sow,
    Throw,
    With,
)
import sympy_wolfram.mathematica_expressions as _me
from sympy_wolfram.mathematica_parser import mathematica_to_sympy

# ---------------------------------------------------------------------------
# Custom-functions mapping for round-trip tests
# ---------------------------------------------------------------------------
# Passed as custom_functions= to mathematica_to_sympy() so that the parser
# produces the same unevaluated SymPy objects as direct Python constructors.
# Each entry: WolframHead -> ('me.ClassName', module_object).  The converter
# emits 'me.ClassName(args...)' and registers the module as 'me' in the eval
# namespace.
_MATH_EXPR_FUNCS = {
    'List':               ('me.List',               _me),
    'Set':                ('me.Set',                _me),
    'If':                 ('me.If',                 _me),
    'With':               ('me.With',               _me),
    'Module':             ('me.Module',             _me),
    'Block':              ('me.Block',              _me),
    'CompoundExpression': ('me.CompoundExpression', _me),
    'Return':             ('me.Return',             _me),
    'Do':                 ('me.Do',                 _me),
    'Scan':               ('me.Scan',               _me),
    'Throw':              ('me.Throw',              _me),
    'Catch':              ('me.Catch',              _me),
    'Sow':                ('me.Sow',                _me),
    'Reap':               ('me.Reap',               _me),
    'Head':               ('me.Head',               _me),
}


class TestList:
    """Tests for List: Mathematica List container."""

    def test_list_construction(self):
        """List[1, 2, 3]"""
        lst = List(1, 2, 3)
        assert len(lst.args) == 3
        assert lst.args == (Integer(1), Integer(2), Integer(3))

    def test_list_iteration(self):
        """List items can be iterated."""
        lst = List(1, 2, 3)
        assert list(lst) == [Integer(1), Integer(2), Integer(3)]

    def test_list_doit_returns_self(self):
        """List.doit() returns the list unchanged."""
        lst = List(1, 2, 3)
        assert lst.doit() == lst


class TestSet:
    """Tests for Set: Mathematica variable binding marker."""

    def test_set_construction(self):
        """Set[x, 5]"""
        x = Symbol('x')
        binding = Set(x, Integer(5))
        assert binding.args == (x, Integer(5))

    def test_set_doit_returns_self(self):
        """Set is a structural marker, not evaluated."""
        x = Symbol('x')
        binding = Set(x, Integer(5))
        assert binding.doit() == binding


class TestIf:
    """Tests for If: Mathematica conditional expression.

    Documentation: https://reference.wolfram.com/language/ref/If.html
    """

    def test_if_true_branch(self):
        """If[True, 1, 0] -> 1"""
        result = If(S.true, Integer(1), Integer(0)).doit()
        assert result == Integer(1)

    def test_if_false_branch(self):
        """If[False, 1, 0] -> 0"""
        result = If(S.false, Integer(1), Integer(0)).doit()
        assert result == Integer(0)

    def test_if_two_args_true(self):
        """If[True, 42] -> 42"""
        result = If(S.true, Integer(42)).doit()
        assert result == Integer(42)

    def test_if_two_args_false(self):
        """If[False, 42] -> Null"""
        result = If(S.false, Integer(42)).doit()
        assert result == Null

    def test_if_unknown_returns_unevaluated(self):
        """If[x > 0, 1, -1] stays unevaluated when condition is symbolic."""
        x = Symbol('x')
        cond = sympy.Gt(x, 0)
        result = If(cond, Integer(1), Integer(-1)).doit()
        assert isinstance(result, If)

    def test_if_four_args_unknown(self):
        """If[x > 0, 1, -1, 0] -> 0 when condition is neither True nor False."""
        x = Symbol('x')
        cond = sympy.Gt(x, 0)
        result = If(cond, Integer(1), Integer(-1), Integer(0)).doit()
        assert result == Integer(0)


class TestWith:
    """Tests for With: Mathematica local constant substitution.

    Documentation: https://reference.wolfram.com/language/ref/With.html
    """

    def test_with_single_binding(self):
        """With[{x = 5}, x + 1] -> 6"""
        x = Symbol('x')
        result = With(List(Set(x, Integer(5))), x + Integer(1)).doit()
        assert result == Integer(6)

    def test_with_multiple_bindings(self):
        """With[{x = 2, y = 3}, x * y] -> 6"""
        x, y = Symbol('x'), Symbol('y')
        bindings = List(Set(x, Integer(2)), Set(y, Integer(3)))
        result = With(bindings, x * y).doit()
        assert result == Integer(6)

    def test_with_nested_expression(self):
        """With[{a = 2}, a^2 + a + 1] -> 7"""
        a = Symbol('a')
        result = With(List(Set(a, Integer(2))), a**2 + a + Integer(1)).doit()
        assert result == Integer(7)

    def test_with_return_handling(self):
        """Return within With stops evaluation and returns the value."""
        x = Symbol('x')
        result = With(List(Set(x, Integer(10))), Return(x * Integer(2))).doit()
        assert result == Integer(20)


class TestModule:
    """Tests for Module: Mathematica lexical scoping with fresh symbols.

    Documentation: https://reference.wolfram.com/language/ref/Module.html
    """

    def test_module_single_local(self):
        """Module[{x = 5}, x + 1] -> 6"""
        x = Symbol('x')
        result = Module(List(Set(x, Integer(5))), x + Integer(1)).doit()
        assert result == Integer(6)

    def test_module_local_renamed(self):
        """Module introduces fresh symbols."""
        x = Symbol('x')
        result = Module(List(x), x).doit()
        assert isinstance(result, Symbol)
        assert result.name.startswith('x')

    def test_module_multiple_locals(self):
        """Module[{a = 2, b = 3}, a + b] -> 5"""
        a, b = Symbol('a'), Symbol('b')
        bindings = List(Set(a, Integer(2)), Set(b, Integer(3)))
        result = Module(bindings, a + b).doit()
        assert result == Integer(5)


class TestBlock:
    """Tests for Block: Mathematica dynamic scoping with temporary values.

    Documentation: https://reference.wolfram.com/language/ref/Block.html
    """

    def test_block_single_binding(self):
        """Block[{x = 10}, x + 5] -> 15"""
        x = Symbol('x')
        result = Block(List(Set(x, Integer(10))), x + Integer(5)).doit()
        assert result == Integer(15)

    def test_block_multiple_bindings(self):
        """Block[{a = 3, b = 7}, a * b] -> 21"""
        a, b = Symbol('a'), Symbol('b')
        bindings = List(Set(a, Integer(3)), Set(b, Integer(7)))
        result = Block(bindings, a * b).doit()
        assert result == Integer(21)


class TestCompoundExpression:
    """Tests for CompoundExpression: sequential evaluation.

    Documentation: https://reference.wolfram.com/language/ref/CompoundExpression.html
    """

    def test_compound_returns_last(self):
        """CompoundExpression[1, 2, 3] -> 3"""
        result = CompoundExpression(Integer(1), Integer(2), Integer(3)).doit()
        assert result == Integer(3)

    def test_compound_empty(self):
        """CompoundExpression[] -> Null"""
        result = CompoundExpression().doit()
        assert result == Null

    def test_compound_single_expr(self):
        """CompoundExpression[42] -> 42"""
        result = CompoundExpression(Integer(42)).doit()
        assert result == Integer(42)


class TestReturn:
    """Tests for Return: Mathematica return from procedural constructs.

    Documentation: https://reference.wolfram.com/language/ref/Return.html
    """

    def test_return_unwrapped(self):
        """Return[5] within With[{}, Return[5]] -> 5"""
        result = With(List(), Return(Integer(5))).doit()
        assert result == Integer(5)

    def test_return_default_value(self):
        """Return[] -> Null"""
        result = With(List(), Return()).doit()
        assert result == Null


class TestDo:
    """Tests for Do: Mathematica iteration construct.

    Documentation: https://reference.wolfram.com/language/ref/Do.html
    """

    def test_do_single_iteration(self):
        """Do[expr, {5}] executes 5 times, returns Null."""
        result = Do(Integer(42), List(Integer(5))).doit()
        assert result == Null

    def test_do_with_iterator(self):
        """Do with i from 1 to 3."""
        i = Symbol('i')
        result = Do(Sow(i), List(i, Integer(3))).doit()
        assert result == Null

    def test_do_with_range(self):
        """Do[Sow[i], {i, 2, 4}] sows 2, 3, 4."""
        i = Symbol('i')
        reap_result = Reap(Do(Sow(i), List(i, Integer(2), Integer(4)))).doit()
        sown = reap_result.args[1]
        values = list(sown.args[0].args)
        assert values == [Integer(2), Integer(3), Integer(4)]

    def test_do_with_step(self):
        """Do[Sow[i], {i, 1, 5, 2}] sows 1, 3, 5."""
        i = Symbol('i')
        reap_result = Reap(Do(Sow(i), List(i, Integer(1), Integer(5), Integer(2)))).doit()
        values = list(reap_result.args[1].args[0].args)
        assert values == [Integer(1), Integer(3), Integer(5)]


class TestScan:
    """Tests for Scan: apply function for side effects.

    Documentation: https://reference.wolfram.com/language/ref/Scan.html
    """

    def test_scan_returns_null(self):
        """Scan[f, {1, 2, 3}] returns Null."""
        f = Symbol('f')
        result = Scan(f, List(Integer(1), Integer(2), Integer(3))).doit()
        assert result == Null

    def test_scan_with_sow(self):
        """Scan[Sow, {1, 2}] inside Reap collects values."""
        lst = List(Integer(1), Integer(2))
        reap_result = Reap(Scan(sympy.Lambda(Symbol('x'), Sow(Symbol('x'))), lst)).doit()
        values = list(reap_result.args[1].args[0].args)
        assert values == [Integer(1), Integer(2)]


class TestThrowCatch:
    """Tests for Throw and Catch: Mathematica exception mechanism.

    Documentation:
    - https://reference.wolfram.com/language/ref/Throw.html
    - https://reference.wolfram.com/language/ref/Catch.html
    """

    def test_catch_simple(self):
        """Catch[Throw[42]] -> 42"""
        result = Catch(Throw(Integer(42))).doit()
        assert result == Integer(42)

    def test_catch_nested_expression(self):
        """Catch[1 + Throw[5]] -> 5"""
        result = Catch(Integer(1) + Throw(Integer(5))).doit()
        assert result == Integer(5)

    def test_catch_with_tag(self):
        """Catch[Throw[val, tag], tag] -> val"""
        tag = Symbol('myTag')
        result = Catch(Throw(Integer(99), tag), tag).doit()
        assert result == Integer(99)

    def test_catch_mismatched_tag_propagates(self):
        """Catch with mismatched tag re-raises."""
        tag1, tag2 = Symbol('tag1'), Symbol('tag2')
        with pytest.raises(Exception):
            Catch(Throw(Integer(1), tag1), tag2).doit()

    def test_catch_no_throw(self):
        """Catch[5 + 3] -> 8 (no Throw means normal evaluation)."""
        result = Catch(Integer(5) + Integer(3)).doit()
        assert result == Integer(8)


class TestSowReap:
    """Tests for Sow and Reap: Mathematica value collection mechanism.

    Documentation:
    - https://reference.wolfram.com/language/ref/Sow.html
    - https://reference.wolfram.com/language/ref/Reap.html
    """

    def test_reap_simple(self):
        """Reap[Sow[1]; Sow[2]] -> {Null, {{1, 2}}}"""
        result = Reap(CompoundExpression(Sow(Integer(1)), Sow(Integer(2)))).doit()
        assert result.args[0] == Integer(2)
        inner = result.args[1].args[0]
        assert list(inner.args) == [Integer(1), Integer(2)]

    def test_sow_returns_value(self):
        """Sow[x] returns x."""
        x = Symbol('x')
        result = Sow(x).doit()
        assert result == x

    def test_reap_with_tag(self):
        """Reap with tag filter."""
        tag = Symbol('myTag')
        result = Reap(
            CompoundExpression(Sow(Integer(1), tag), Sow(Integer(2), tag)),
            tag
        ).doit()
        inner = result.args[1].args[0]
        assert list(inner.args) == [Integer(1), Integer(2)]

    def test_sow_outside_reap_does_nothing(self):
        """Sow outside Reap just returns the value."""
        result = Sow(Integer(42)).doit()
        assert result == Integer(42)


class TestHead:
    """Tests for Head: Mathematica expression head.

    Documentation: https://reference.wolfram.com/language/ref/Head.html
    """

    def test_head_integer(self):
        """Head[5] -> Integer"""
        result = Head(Integer(5)).doit()
        assert result == Symbol('Integer')

    def test_head_rational(self):
        """Head[2/3] -> Rational"""
        result = Head(Rational(2, 3)).doit()
        assert result == Symbol('Rational')

    def test_head_symbol(self):
        """Head[x] -> Symbol"""
        x = Symbol('x')
        result = Head(x).doit()
        assert result == Symbol('Symbol')

    def test_head_list(self):
        """Head[{1, 2}] -> List"""
        result = Head(List(Integer(1), Integer(2))).doit()
        assert result == Symbol('List')

    def test_head_add(self):
        """Head[a + b] -> Plus"""
        a, b = Symbol('a'), Symbol('b')
        result = Head(a + b).doit()
        assert result == Symbol('Plus')

    def test_head_mul(self):
        """Head[a * b] -> Times"""
        a, b = Symbol('a'), Symbol('b')
        result = Head(a * b).doit()
        assert result == Symbol('Times')

    def test_head_pow(self):
        """Head[a^b] -> Power"""
        a, b = Symbol('a'), Symbol('b')
        result = Head(a**b).doit()
        assert result == Symbol('Power')

    def test_head_function(self):
        """Head[Sin[x]] -> sin"""
        x = Symbol('x')
        result = Head(sympy.sin(x)).doit()
        assert result == Symbol('sin')


class TestNestedConstructs:
    """Tests for combinations of constructs."""

    def test_nested_with(self):
        """With[{x = 2}, With[{y = 3}, x + y]] -> 5"""
        x, y = Symbol('x'), Symbol('y')
        inner = With(List(Set(y, Integer(3))), x + y)
        outer = With(List(Set(x, Integer(2))), inner)
        assert outer.doit() == Integer(5)

    def test_module_in_do(self):
        """Do with Module scope."""
        i, j = Symbol('i'), Symbol('j')
        body = Module(List(Set(j, i * Integer(10))), Sow(j))
        result = Reap(Do(body, List(i, Integer(1), Integer(3)))).doit()
        values = list(result.args[1].args[0].args)
        assert values == [Integer(10), Integer(20), Integer(30)]

    def test_if_in_with(self):
        """With[{x = 5}, If[x > 3, 100, 0]]"""
        x = Symbol('x')
        body = If(sympy.Gt(x, Integer(3)), Integer(100), Integer(0))
        result = With(List(Set(x, Integer(5))), body).doit()
        assert result == Integer(100)


# ---------------------------------------------------------------------------
# Round-trip tests: Mathematica string → mathematica_to_sympy → expression
# ---------------------------------------------------------------------------

class TestMathematicaToSympyRoundTrip:
    """Verify mathematica_to_sympy() builds the same unevaluated SymPy objects
    as direct Python constructors when given _MATH_EXPR_FUNCS as the remapping.

    Each test mirrors a case from one of the TestXxx classes above, using an
    explicit Mathematica function-call string (e.g. ``List[1,2,3]``,
    ``Set[x,5]``, ``With[List[Set[x,5]], Plus[x,1]]``) to verify the full
    parse → FFL → eval pipeline.  No ``.doit()`` is called; only the
    unevaluated object structure is checked.
    """

    # -- List -----------------------------------------------------------------

    def test_list_from_string(self):
        """List[1, 2, 3] parses to List(Integer(1), Integer(2), Integer(3))."""
        result = mathematica_to_sympy("List[1, 2, 3]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == List(Integer(1), Integer(2), Integer(3))

    # -- Set ------------------------------------------------------------------

    def test_set_from_string(self):
        """Set[x, 5] parses to Set(Symbol('x'), Integer(5))."""
        x = Symbol('x')
        result = mathematica_to_sympy("Set[x, 5]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Set(x, Integer(5))

    # -- If -------------------------------------------------------------------

    def test_if_true_branch_from_string(self):
        """If[True, 1, 0] parses to If(S.true, Integer(1), Integer(0))."""
        result = mathematica_to_sympy("If[True, 1, 0]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == If(S.true, Integer(1), Integer(0))

    def test_if_false_branch_from_string(self):
        """If[False, 1, 0] parses to If(S.false, Integer(1), Integer(0))."""
        result = mathematica_to_sympy("If[False, 1, 0]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == If(S.false, Integer(1), Integer(0))

    def test_if_two_args_from_string(self):
        """If[True, 42] parses to the 2-arg If form."""
        result = mathematica_to_sympy("If[True, 42]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == If(S.true, Integer(42))

    def test_if_four_args_from_string(self):
        """If[Greater[x, 0], 1, 0, 99] parses to the 4-arg If form."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "If[Greater[x, 0], 1, 0, 99]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == If(sympy.Gt(x, Integer(0)), Integer(1), Integer(0), Integer(99))

    # -- With -----------------------------------------------------------------

    def test_with_single_binding_from_string(self):
        """With[List[Set[x, 5]], Plus[x, 1]] parses correctly."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "With[List[Set[x, 5]], Plus[x, 1]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == With(List(Set(x, Integer(5))), x + Integer(1))

    def test_with_multiple_bindings_from_string(self):
        """With[List[Set[x, 2], Set[y, 3]], Times[x, y]] parses correctly."""
        x, y = Symbol('x'), Symbol('y')
        result = mathematica_to_sympy(
            "With[List[Set[x, 2], Set[y, 3]], Times[x, y]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == With(List(Set(x, Integer(2)), Set(y, Integer(3))), x * y)

    def test_with_nested_expr_from_string(self):
        """With[List[Set[a, 2]], Times[a, Plus[a, 1]]] parses correctly."""
        a = Symbol('a')
        result = mathematica_to_sympy(
            "With[List[Set[a, 2]], Times[a, Plus[a, 1]]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == With(List(Set(a, Integer(2))), a * (a + Integer(1)))

    def test_with_return_from_string(self):
        """With[List[Set[x, 10]], Return[Times[x, 2]]] parses correctly."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "With[List[Set[x, 10]], Return[Times[x, 2]]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == With(List(Set(x, Integer(10))), Return(x * Integer(2)))

    # -- Module ---------------------------------------------------------------

    def test_module_with_init_from_string(self):
        """Module[List[Set[x, 5]], Plus[x, 1]] parses correctly."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "Module[List[Set[x, 5]], Plus[x, 1]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Module(List(Set(x, Integer(5))), x + Integer(1))

    def test_module_bare_local_from_string(self):
        """Module[List[x], x] parses correctly (uninitialized local)."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "Module[List[x], x]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Module(List(x), x)

    def test_module_multiple_locals_from_string(self):
        """Module[List[Set[a, 2], Set[b, 3]], Plus[a, b]] parses correctly."""
        a, b = Symbol('a'), Symbol('b')
        result = mathematica_to_sympy(
            "Module[List[Set[a, 2], Set[b, 3]], Plus[a, b]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Module(List(Set(a, Integer(2)), Set(b, Integer(3))), a + b)

    # -- Block ----------------------------------------------------------------

    def test_block_single_binding_from_string(self):
        """Block[List[Set[x, 10]], Plus[x, 5]] parses correctly."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "Block[List[Set[x, 10]], Plus[x, 5]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Block(List(Set(x, Integer(10))), x + Integer(5))

    def test_block_multiple_bindings_from_string(self):
        """Block[List[Set[a, 3], Set[b, 7]], Times[a, b]] parses correctly."""
        a, b = Symbol('a'), Symbol('b')
        result = mathematica_to_sympy(
            "Block[List[Set[a, 3], Set[b, 7]], Times[a, b]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Block(List(Set(a, Integer(3)), Set(b, Integer(7))), a * b)

    # -- CompoundExpression ---------------------------------------------------

    def test_compound_expression_from_string(self):
        """CompoundExpression[1, 2, 3] parses correctly."""
        result = mathematica_to_sympy(
            "CompoundExpression[1, 2, 3]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == CompoundExpression(Integer(1), Integer(2), Integer(3))

    def test_compound_single_expr_from_string(self):
        """CompoundExpression[42] parses correctly."""
        result = mathematica_to_sympy(
            "CompoundExpression[42]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == CompoundExpression(Integer(42))

    # -- Return ---------------------------------------------------------------

    def test_return_value_from_string(self):
        """Return[5] parses to Return(Integer(5))."""
        result = mathematica_to_sympy("Return[5]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Return(Integer(5))

    def test_return_null_from_string(self):
        """Return[Null] parses to Return(Null) (the Null sentinel)."""
        result = mathematica_to_sympy("Return[Null]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Return(Null)

    # -- Do -------------------------------------------------------------------

    def test_do_count_from_string(self):
        """Do[42, List[5]] parses to the fixed-count Do form."""
        result = mathematica_to_sympy(
            "Do[42, List[5]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Do(Integer(42), List(Integer(5)))

    def test_do_iterator_from_string(self):
        """Do[Sow[i], List[i, 3]] parses correctly (implicit start=1)."""
        i = Symbol('i')
        result = mathematica_to_sympy(
            "Do[Sow[i], List[i, 3]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Do(Sow(i), List(i, Integer(3)))

    def test_do_with_range_from_string(self):
        """Do[Sow[i], List[i, 2, 4]] parses correctly."""
        i = Symbol('i')
        result = mathematica_to_sympy(
            "Do[Sow[i], List[i, 2, 4]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Do(Sow(i), List(i, Integer(2), Integer(4)))

    def test_do_with_step_from_string(self):
        """Do[Sow[i], List[i, 1, 5, 2]] parses correctly (step form)."""
        i = Symbol('i')
        result = mathematica_to_sympy(
            "Do[Sow[i], List[i, 1, 5, 2]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Do(Sow(i), List(i, Integer(1), Integer(5), Integer(2)))

    # -- Scan -----------------------------------------------------------------

    def test_scan_from_string(self):
        """Scan[f, List[1, 2, 3]] parses to Scan(Symbol('f'), List(...))."""
        f = Symbol('f')
        result = mathematica_to_sympy(
            "Scan[f, List[1, 2, 3]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Scan(f, List(Integer(1), Integer(2), Integer(3)))

    # -- Throw / Catch --------------------------------------------------------

    def test_throw_from_string(self):
        """Throw[42] parses to Throw(Integer(42))."""
        result = mathematica_to_sympy("Throw[42]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Throw(Integer(42))

    def test_throw_with_tag_from_string(self):
        """Throw[99, myTag] parses to Throw(Integer(99), Symbol('myTag'))."""
        tag = Symbol('myTag')
        result = mathematica_to_sympy(
            "Throw[99, myTag]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Throw(Integer(99), tag)

    def test_catch_simple_from_string(self):
        """Catch[Throw[42]] parses to Catch(Throw(Integer(42)))."""
        result = mathematica_to_sympy(
            "Catch[Throw[42]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Catch(Throw(Integer(42)))

    def test_catch_with_tag_from_string(self):
        """Catch[Throw[99, myTag], myTag] parses to the tagged Catch form."""
        tag = Symbol('myTag')
        result = mathematica_to_sympy(
            "Catch[Throw[99, myTag], myTag]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Catch(Throw(Integer(99), tag), tag)

    def test_catch_no_throw_from_string(self):
        """Catch[Plus[5, 3]] parses to Catch(Integer(8)) (arithmetic evaluated)."""
        result = mathematica_to_sympy(
            "Catch[Plus[5, 3]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Catch(Integer(8))

    # -- Sow / Reap -----------------------------------------------------------

    def test_sow_from_string(self):
        """Sow[42] parses to Sow(Integer(42))."""
        result = mathematica_to_sympy("Sow[42]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Sow(Integer(42))

    def test_reap_sow_from_string(self):
        """Reap[Sow[1]] parses to Reap(Sow(Integer(1)))."""
        result = mathematica_to_sympy(
            "Reap[Sow[1]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Reap(Sow(Integer(1)))

    def test_reap_compound_from_string(self):
        """Reap[CompoundExpression[Sow[1], Sow[2]]] parses correctly."""
        result = mathematica_to_sympy(
            "Reap[CompoundExpression[Sow[1], Sow[2]]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Reap(CompoundExpression(Sow(Integer(1)), Sow(Integer(2))))

    def test_reap_with_tag_from_string(self):
        """Reap[Sow[1, myTag], myTag] parses to Reap(..., tag) with filter."""
        tag = Symbol('myTag')
        result = mathematica_to_sympy(
            "Reap[Sow[1, myTag], myTag]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Reap(Sow(Integer(1), tag), tag)

    # -- Head -----------------------------------------------------------------

    def test_head_integer_from_string(self):
        """Head[5] parses to Head(Integer(5))."""
        result = mathematica_to_sympy("Head[5]", custom_functions=_MATH_EXPR_FUNCS)
        assert result == Head(Integer(5))

    def test_head_list_from_string(self):
        """Head[List[1, 2]] parses to Head(List(Integer(1), Integer(2)))."""
        result = mathematica_to_sympy(
            "Head[List[1, 2]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Head(List(Integer(1), Integer(2)))

    def test_head_symbol_from_string(self):
        """Head[a] parses to Head(Symbol('a'))."""
        a = Symbol('a')
        result = mathematica_to_sympy(
            "Head[a]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Head(a)

    def test_head_add_from_string(self):
        """Head[Plus[a, b]] parses to Head(a + b)."""
        a, b = Symbol('a'), Symbol('b')
        result = mathematica_to_sympy(
            "Head[Plus[a, b]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        assert result == Head(a + b)

    # -- Nested constructs ----------------------------------------------------

    def test_nested_with_from_string(self):
        """With[List[Set[x, 2]], With[List[Set[y, 3]], Plus[x, y]]] parses correctly."""
        x, y = Symbol('x'), Symbol('y')
        result = mathematica_to_sympy(
            "With[List[Set[x, 2]], With[List[Set[y, 3]], Plus[x, y]]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        inner = With(List(Set(y, Integer(3))), x + y)
        outer = With(List(Set(x, Integer(2))), inner)
        assert result == outer

    def test_if_in_with_from_string(self):
        """With[List[Set[x, 5]], If[Greater[x, 3], 100, 0]] parses correctly."""
        x = Symbol('x')
        result = mathematica_to_sympy(
            "With[List[Set[x, 5]], If[Greater[x, 3], 100, 0]]",
            custom_functions=_MATH_EXPR_FUNCS,
        )
        body = If(sympy.Gt(x, Integer(3)), Integer(100), Integer(0))
        assert result == With(List(Set(x, Integer(5))), body)


# ── _condition_holds lazy / short-circuit evaluation ─────────────────────────
# Regression guard: _condition_holds used to _eval the WHOLE test up-front, so a
# combined And could build/sort a structure embedding a non-Expr sentinel (a util
# returning the symbol False, e.g. DerivativeDivides) -> sympy sort crash
# ('bool' object has no attribute 'is_Float'). It now evaluates And/Or/Not
# lazily, operand-by-operand, matching Mathematica's short-circuiting.

def test_condition_holds_short_circuits_and_or():
    from sympy_wolfram.mathematica_expressions import _condition_holds, MathematicaExpr
    from sympy.logic.boolalg import And, Or

    class _Boom(MathematicaExpr):
        def __new__(cls):
            return sympy.Expr.__new__(cls)
        def _evaluate(self, **kwargs):
            raise AssertionError("operand was evaluated despite short-circuit")

    # And(False, Boom): first operand False -> False, Boom must not be evaluated.
    assert _condition_holds(And(S.false, _Boom(), evaluate=False)) is False
    # Or(True, Boom): first operand True -> True, Boom must not be evaluated.
    assert _condition_holds(Or(S.true, _Boom(), evaluate=False)) is True


def test_doit_stays_unevaluated_when_evaluate_returns_none():
    from sympy_wolfram.mathematica_expressions import MathematicaExpr

    class _NoneNode(MathematicaExpr):
        def __new__(cls, arg):
            return sympy.Expr.__new__(cls, sympy.sympify(arg))
        def _evaluate(self, **kwargs):
            return None  # utility couldn't compute a value for this input

    node = _NoneNode(Symbol('x'))
    # doit must NOT return None (that would break an enclosing Add/Mul via
    # sympify(None)); it stays the unevaluated node instead.
    assert node.doit() is not None
    assert isinstance(node.doit(), _NoneNode)
    # and it must survive being embedded in arithmetic + doit'd
    expr = Symbol('y') * node
    assert expr.doit() is not None


def test_condition_holds_basic_connectives():
    from sympy_wolfram.mathematica_expressions import _condition_holds
    from sympy.logic.boolalg import And, Or, Not
    assert _condition_holds(And(S.true, S.true, evaluate=False)) is True
    assert _condition_holds(And(S.true, S.false, evaluate=False)) is False
    assert _condition_holds(Or(S.false, S.false, evaluate=False)) is False
    assert _condition_holds(Not(S.false)) is True
    assert _condition_holds(Not(S.true)) is False


# ── Condition (expr /; test) ─────────────────────────────────────────────────

def test_condition_holds_returns_body():
    from sympy_wolfram.mathematica_expressions import Condition
    assert Condition(Integer(5), S.true).doit() == 5


def test_condition_fails_raises_stopiteration():
    from sympy_wolfram.mathematica_expressions import Condition
    with pytest.raises(StopIteration):
        Condition(Integer(5), S.false).doit()


def test_condition_body_not_evaluated_when_test_fails():
    # The body must not be evaluated when the test fails (Mathematica semantics;
    # the default deep doit would have reduced the body first).
    from sympy_wolfram.mathematica_expressions import Condition, MathematicaExpr

    class _Boom(MathematicaExpr):
        def __new__(cls):
            return sympy.Expr.__new__(cls)
        def _evaluate(self, **kwargs):
            raise AssertionError("body evaluated despite failing test")

    with pytest.raises(StopIteration):
        Condition(_Boom(), S.false).doit()


def test_condition_set_in_test_binds_body():
    # Set[q, 7] inside the test binds q for the body (Mathematica side effect).
    from sympy_wolfram.mathematica_expressions import Condition, Set
    q = Symbol('q')
    cond = Condition(q + 1, Set(q, Integer(7)) > 0)
    assert cond.doit() == 8


# ── rename_scoped_locals (lexical scoping for With/Module/Block) ──────────────

def test_rename_scoped_locals_basic():
    from sympy_wolfram.mathematica_expressions import With, List, Set, rename_scoped_locals
    a, b, x = Symbol('a'), Symbol('b'), Symbol('x')
    renamed = rename_scoped_locals(With(List(Set(a, Integer(1))), a + b * x))
    local = renamed.args[0].args[0].args[0]      # the (renamed) local symbol
    assert local != a and local.name.startswith('a$')
    assert renamed.doit() == 1 + b * x           # value unchanged


def test_rename_scoped_locals_prevents_capture():
    # The core bug: a local named `a` must not clobber an `a` that is substituted
    # into the body later (as a rewrite system fills a pattern variable).
    from sympy_wolfram.mathematica_expressions import With, List, Set, rename_scoped_locals
    a, b, u = Symbol('a'), Symbol('b'), Symbol('u')
    tmpl = With(List(Set(a, u)), a * u)                  # local a = u; body a*u
    substituted = rename_scoped_locals(tmpl).subs(u, a + b)   # u carries a symbol named 'a'
    assert substituted.doit() == (a + b)**2             # local=(a+b); NOT (a+b)*(a+2b)


def test_rename_scoped_locals_noop_without_scopes():
    from sympy_wolfram.mathematica_expressions import rename_scoped_locals
    a, b, x = Symbol('a'), Symbol('b'), Symbol('x')
    expr = a * x + b
    assert rename_scoped_locals(expr) == expr
