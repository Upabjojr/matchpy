# -*- coding: utf-8 -*-
"""Tests for rubi_rules code generator.

Tests the FFL-to-Python translation pipeline:
- Syntax correctness of generated code
- Wildcard extraction (dot vs optional)
- Constraint extraction (FreeQ, NeQ)
- Integration variable handling
- End-to-end: parse .m file -> generate -> load -> integrate
"""
import sys
import os
import pytest
import py_compile
import tempfile
import importlib.util
from pathlib import Path

from rubi_rules.codegen.parse_rubi_to_ffl import parse_m_file

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rubi_rules.codegen.generate import RubiRuleTranslator

# Path to Rubi repository (for integration tests that parse .m files).
# Tests skip gracefully if this path doesn't exist.
DEFAULT_RUBI_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'rubi-wip', 'Rubi')


# =============================================================================
# Test: Expression conversion (via FFLConverter)
# =============================================================================

class TestTranslatorExpressions:
    """Test FFL -> SymPy expression code generation."""

    def setup_method(self):
        self.t = RubiRuleTranslator()
        self.c = self.t._converter  # shortcut to FFLConverter
        self.c._fixed_var = 'x'
        self.c._wildcards_non_optional = set()
        self.c._wildcards_optional = set()

    def test_integer_atom(self):
        assert self.c.convert('42') == 'Integer(42)'

    def test_negative_integer(self):
        assert self.c.convert('-1') == 'Integer(-1)'

    def test_fixed_var(self):
        assert self.c.convert('x') == 'x'

    def test_symbol(self):
        assert self.c.convert('foo') == "Symbol('foo')"

    def test_constant_pi(self):
        assert self.c.convert('Pi') == 'sympy.pi'

    def test_plus(self):
        ffl = ['Plus', 'x', '1']
        result = self.c.convert(ffl)
        assert 'x' in result and '1' in result and '+' in result

    def test_times(self):
        ffl = ['Times', '2', 'x']
        result = self.c.convert(ffl)
        assert '*' in result

    def test_power(self):
        ffl = ['Power', 'x', '2']
        result = self.c.convert(ffl)
        assert '**' in result

    def test_log(self):
        ffl = ['Log', 'x']
        result = self.c.convert(ffl)
        assert 'sympy.log' in result

    def test_sin(self):
        ffl = ['Sin', 'x']
        result = self.c.convert(ffl)
        assert 'sympy.sin' in result

    def test_pattern_creates_wildcard(self):
        ffl = ['Pattern', 'm', ['Blank']]
        result = self.c.convert(ffl, is_pattern=True)
        assert result == 'm_'
        assert 'm' in self.c._wildcards_non_optional

    def test_optional_creates_optional_wildcard(self):
        ffl = ['Optional', ['Pattern', 'a', ['Blank']]]
        result = self.c.convert(ffl, is_pattern=True)
        assert result == '_a_'
        assert 'a' in self.c._wildcards_non_optional
        assert 'a' in self.c._wildcards_optional

    def test_fixed_var_pattern_not_wildcard(self):
        """Pattern['x', Blank[Symbol]] should NOT become a wildcard."""
        ffl = ['Pattern', 'x', ['Blank', 'Symbol']]
        result = self.c.convert(ffl, is_pattern=True)
        assert result == 'x'
        assert 'x' not in self.c._wildcards_non_optional

    def test_wildcard_ref_in_replacement(self):
        """A known wildcard name should reference the WildSymbol in replacement."""
        self.c._wildcards_non_optional = {'m'}
        result = self.c._atom_to_code('m', False)
        assert result == 'm_'

    def test_unknown_symbol_not_wildcard(self):
        """An unknown symbol should produce Symbol('name')."""
        result = self.c._atom_to_code('z', False)
        assert result == "Symbol('z')"


# =============================================================================
# Test: Constraint extraction
# =============================================================================


# =============================================================================
# Test: Full rule translation
# =============================================================================

class TestRuleTranslation:
    def setup_method(self):
        self.t = RubiRuleTranslator()

    def test_simple_power_rule(self):
        """SetDelayed[Int[x^m_, x_], x^(m+1)/(m+1)]"""
        ffl = [
            'SetDelayed',
            ['Int', ['Power', ['Pattern', 'x', ['Blank', 'Symbol']], ['Pattern', 'm', ['Blank']]],
             ['Pattern', 'x', ['Blank', 'Symbol']]],
            ['Condition',
             ['Times', ['Power', ['Plus', ['Pattern', 'm', ['Blank']], '1'], '-1'],
              ['Power', 'x', ['Plus', ['Pattern', 'm', ['Blank']], '1']]],
             ['And', ['FreeQ', 'm', 'x'], ['NeQ', 'm', '-1']]]
        ]
        code = self.t._translate_rule(ffl, 1, "module_name")
        assert code is not None
        assert 'RubiRulePattern' in code
        assert 'FreeQ(m_, x)' in code
        assert 'NeQ(m_, -1)' in code

    def test_non_setdelayed_returns_none(self):
        code = self.t._translate_rule(['SomeOther', 'a', 'b'], 1, "module_name")
        assert code is None

    def test_non_int_lhs_returns_none(self):
        code = self.t._translate_rule(['SetDelayed', ['Foo', 'a'], 'b'], 1, "module_name")
        assert code is None

    def test_with_condition_is_lifted_into_constraints(self):
        """Condition nested inside With should become a rule constraint."""
        ffl = [
            'SetDelayed',
            ['Int',
             ['Times', ['Pattern', 'u', ['Blank']],
              ['Power', ['Pattern', 'y', ['Blank']], ['Optional', ['Pattern', 'm', ['Blank']]]]],
             ['Pattern', 'x', ['Blank', 'Symbol']]],
            ['Condition',
             ['With',
              ['List',
               ['Set', 'q', ['DerivativeDivides', ['ActivateTrig', 'y'], ['ActivateTrig', 'u'], 'x']]],
              ['Condition',
               ['Times', 'q',
                ['Power', ['Plus', 'm', '1'], '-1'],
                ['ActivateTrig', ['Power', 'y', ['Plus', 'm', '1']]]],
               ['Not', ['FalseQ', 'q']]]],
             ['And',
              ['FreeQ', 'm', 'x'],
              ['NeQ', 'm', '-1'],
              ['Not', ['InertTrigFreeQ', 'u']]]],
        ]

        code = self.t._translate_rule(ffl, 54, "4.7.5 Inert trig functions")

        assert code is not None
        assert "constraints=(FreeQ(_m_, x), NeQ(_m_, -1), Not(InertTrigFreeQ(u_)), Not(FalseQ(DerivativeDivides(ActivateTrig(y_), ActivateTrig(u_), x))),)," in code
        assert "replacement=With(List(Set(Symbol('q'), DerivativeDivides(ActivateTrig(y_), ActivateTrig(u_), x))), (Symbol('q') * ((_m_ + Integer(1)))**(Integer(-1)) * ActivateTrig((y_)**((_m_ + Integer(1))))))" in code


# =============================================================================
# Test: Module generation syntax
# =============================================================================

class TestModuleGeneration:
    """Test that generated Python modules are syntactically valid."""

    def test_simple_rules_syntax(self):
        rules = [
            ['SetDelayed',
             ['Int', ['Power', ['Pattern', 'x', ['Blank', 'Symbol']], '-1'],
              ['Pattern', 'x', ['Blank', 'Symbol']]],
             ['Log', 'x']],
        ]
        t = RubiRuleTranslator()
        code = t.translate_module(rules, 'test_module', 'test.m')
        # Check syntax by compiling the source directly (no temp file / .pyc write,
        # which avoids depending on a writable /tmp/__pycache__). Raises
        # SyntaxError if the generated code is malformed.
        compile(code, '<generated test_module>', 'exec')

    def test_module_has_rules_list(self):
        rules = [
            ['SetDelayed',
             ['Int', ['Power', ['Pattern', 'x', ['Blank', 'Symbol']], '-1'],
              ['Pattern', 'x', ['Blank', 'Symbol']]],
             ['Log', 'x']],
        ]
        t = RubiRuleTranslator()
        code = t.translate_module(rules, 'test', 'test.m')
        assert 'RULES = [' in code
        assert 'RubiRulePattern(' in code

    def test_generated_module_importable(self):
        """Generated code can be exec'd and produces RULES list."""
        rules = [
            ['SetDelayed',
             ['Int', ['Power', ['Pattern', 'x', ['Blank', 'Symbol']], '-1'],
              ['Pattern', 'x', ['Blank', 'Symbol']]],
             ['Log', 'x']],
        ]
        t = RubiRuleTranslator()
        code = t.translate_module(rules, 'test', 'test.m')
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp = f.name
        try:
            spec = importlib.util.spec_from_file_location("test_gen", tmp)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            assert hasattr(mod, 'RULES')
            assert len(mod.RULES) == 1
        finally:
            os.unlink(tmp)


# =============================================================================
# Test: .m file parser
# =============================================================================

class TestMFileParser:
    """Test parsing Mathematica .m files."""

    @pytest.fixture
    def rubi_root(self):
        root = Path(DEFAULT_RUBI_ROOT)
        if not root.exists():
            pytest.skip("Rubi repository not available")
        return root

    def test_parse_1_1_1_1(self, rubi_root):
        mfile = rubi_root / 'Rubi' / 'IntegrationRules' / '1 Algebraic functions' / \
                '1.1 Binomial products' / '1.1.1 Linear' / '1.1.1.1 (a+b x)^m.m'
        ffls, err = parse_m_file(mfile)
        assert err is None
        assert len(ffls) == 5
        # All should be SetDelayed
        assert all(isinstance(r, list) and r[0] == 'SetDelayed' for r in ffls)

    def test_parse_1_1_1_2(self, rubi_root):
        mfile = rubi_root / 'Rubi' / 'IntegrationRules' / '1 Algebraic functions' / \
                '1.1 Binomial products' / '1.1.1 Linear' / '1.1.1.2 (a+b x)^m (c+d x)^n.m'
        ffls, err = parse_m_file(mfile)
        assert err is None
        assert len(ffls) >= 30  # 41 rules

    def test_parse_empty_returns_empty(self, tmp_path):
        f = tmp_path / 'empty.m'
        f.write_text('')
        ffls, err = parse_m_file(f)
        assert err is None
        assert ffls == []


# ---------------------------------------------------------------------------
# \[Star] handling: a Rubi `factor \[Star] Int[...]` must keep its Int factor;
# a rule whose Int was dropped by the parser must be skipped, not emitted as a
# non-integral replacement (which would silently give a wrong answer).
# ---------------------------------------------------------------------------
from rubi_rules.codegen.generate import _ffl_has_int_head, _ffl_has_star


class TestStarIntHandling:

    def test_ffl_has_int_head(self):
        assert _ffl_has_int_head(['Int', ['Times', 'u'], 'x']) is True
        assert _ffl_has_int_head(['Times', ['Subst', 'a'], 'b']) is True
        assert _ffl_has_int_head(['Simp', ['Times', 'a', 'b']]) is False
        # a non-string head (list) must not crash the search
        assert _ffl_has_int_head([['Simp', 'x'], 'Star']) is False

    def test_dropped_int_after_star_is_detectable(self):
        # `Simp[...] \[Star] Int[...]` where the parser lost the Int leaves a bare
        # star marker: has a Star but NO Int-like head. The translator skips such a
        # rule instead of emitting a non-integral replacement (a silent wrong
        # answer). Guards the 50 algebraic rules whose Int was dropped at parse time.
        dropped = [['Simp', ['Times', 'a', 'b']], 'Star']
        assert _ffl_has_star(dropped) is True
        assert _ffl_has_int_head(dropped) is False
        # a well-parsed factor*Int keeps its Int-like head
        assert _ffl_has_int_head(['Times', ['Simp', 'f'], ['Int', 'u', 'x']]) is True


class TestStableRuleNumbering:
    """rule_number must count only actual rules, so an orphan expression (e.g. a
    stray Int[...] the parser split off a mangled \\[Star]) never shifts numbering.
    """

    def _rule(self, m_exp):
        # SetDelayed[Int[x^m_, x], x^(m_exp)] -- a minimal translatable rule.
        return ['SetDelayed',
                ['Int', ['Power', 'x', ['Pattern', 'm', ['Blank']]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Power', 'x', m_exp]]

    def test_orphan_expression_does_not_shift_numbering(self):
        import re as _re
        tr = RubiRuleTranslator()
        orphan = ['Int', 'x', 'x']  # non-SetDelayed: an orphaned fragment
        # rule, ORPHAN, rule -> the second rule must still be Rule 2, not Rule 3.
        rules = [self._rule('2'), orphan, self._rule('3')]
        code = tr.translate_module(rules, module_name='test')
        nums = [int(n) for n in _re.findall(r'rule_number=(\d+)', code)]
        assert nums == [1, 2], f"expected [1, 2], got {nums}"


# ---------------------------------------------------------------------------
# Function-head wildcards: F_[args] -> WildHeadApp[F_, args] (pattern) and
# F[args] -> WFApply[F, args] (replacement). MatchPy matches the wildcard head
# natively, so no constraint or post-hoc decomposition is involved.
# ---------------------------------------------------------------------------
from rubi_rules.codegen.generate import (
    _extract_fhw_from_pattern, _rewrite_fhw_in_replacement, _ffl_is_fhw_head,
)

_PAT = lambda n: ['Pattern', n, ['Blank']]          # noqa: E731
_OPT = lambda n: ['Optional', _PAT(n)]              # noqa: E731


class TestFunctionHeadWildcardDetection:

    def test_detects_a_wildcard_head_application(self):
        assert _ffl_is_fhw_head([_PAT('F'), _PAT('v')]) is True

    def test_ordinary_head_is_not_a_wildcard_head(self):
        assert _ffl_is_fhw_head(['Sin', 'x']) is False
        assert _ffl_is_fhw_head(['Times', 'a', 'b']) is False

    def test_non_list_and_empty_are_safe(self):
        assert _ffl_is_fhw_head('x') is False
        assert _ffl_is_fhw_head([]) is False

    def test_derivative_operator_head_is_not_treated_as_a_plain_head_wildcard(self):
        """Derivative[n_][f_] nests differently and is handled separately."""
        node = [[['Derivative', _PAT('n')], _PAT('f')], _PAT('x')]
        assert _ffl_is_fhw_head(node) is False


class TestExtractFhwFromPattern:

    def test_rewrites_into_wild_head_app(self):
        new, heads = _extract_fhw_from_pattern([_PAT('F'), _PAT('v')])
        assert new == ['WildHeadApp', _PAT('F'), _PAT('v')]
        assert heads == {'F'}

    def test_rewrites_nested_occurrence(self):
        ffl = ['Times', 'u', ['Power', [_PAT('F'), _PAT('v')], _PAT('m')]]
        new, heads = _extract_fhw_from_pattern(ffl)
        assert heads == {'F'}
        assert new == ['Times', 'u',
                       ['Power', ['WildHeadApp', _PAT('F'), _PAT('v')], _PAT('m')]]

    def test_collects_several_distinct_heads(self):
        ffl = ['Times', [_PAT('F'), _PAT('u')], [_PAT('G'), _PAT('v')]]
        _new, heads = _extract_fhw_from_pattern(ffl)
        assert heads == {'F', 'G'}

    def test_rewrites_doubly_nested_heads(self):
        ffl = [_PAT('F'), [_PAT('G'), _PAT('v')]]
        new, heads = _extract_fhw_from_pattern(ffl)
        assert heads == {'F', 'G'}
        assert new == ['WildHeadApp', _PAT('F'),
                       ['WildHeadApp', _PAT('G'), _PAT('v')]]

    def test_compound_argument_is_preserved(self):
        arg = ['Plus', _OPT('a'), ['Times', _OPT('b'), 'x']]
        new, _heads = _extract_fhw_from_pattern([_PAT('F'), arg])
        assert new == ['WildHeadApp', _PAT('F'), arg]

    def test_pattern_without_wildcard_head_is_unchanged(self):
        ffl = ['Times', 'a', ['Sin', 'x']]
        new, heads = _extract_fhw_from_pattern(ffl)
        assert new == ffl and heads == set()


class TestRewriteFhwInReplacement:

    def test_rewrites_applied_head_into_wfapply(self):
        out = _rewrite_fhw_in_replacement(['F', 'y'], {'F': 'F'})
        assert out == ['WFApply', 'F', 'y']

    def test_rewrites_nested_occurrences(self):
        ffl = ['Times', 'c', ['Power', ['F', ['Plus', 'a', 'x']], 'm']]
        out = _rewrite_fhw_in_replacement(ffl, {'F': 'F'})
        assert out == ['Times', 'c',
                       ['Power', ['WFApply', 'F', ['Plus', 'a', 'x']], 'm']]

    def test_only_rewrites_known_head_names(self):
        ffl = ['Times', ['F', 'y'], ['Sin', 'y']]
        out = _rewrite_fhw_in_replacement(ffl, {'F': 'F'})
        assert out == ['Times', ['WFApply', 'F', 'y'], ['Sin', 'y']]

    def test_no_head_map_leaves_everything_alone(self):
        ffl = ['Times', ['F', 'y'], ['Sin', 'y']]
        assert _rewrite_fhw_in_replacement(ffl, {}) == ffl

    def test_multi_argument_application(self):
        out = _rewrite_fhw_in_replacement(['F', 'u', 'v'], {'F': 'F'})
        assert out == ['WFApply', 'F', 'u', 'v']
