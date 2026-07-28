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
        self.c.reserved_symbols = {'x': 'x'}
        self.c._wildcards_non_optional = set()
        self.c._wildcards_optional = set()

    def test_integer_atom(self):
        assert self.c.convert('42') == 'Integer(42)'

    def test_negative_integer(self):
        assert self.c.convert('-1') == 'Integer(-1)'

    def test_a_reserved_name_converts_to_its_identifier(self):
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

    def test_bare_function_head_becomes_headref(self):
        # A function head used as a VALUE (e.g. in MemberQ[{ArcSin, ...}, F] or EqQ[F, Sin])
        # emits HeadRef(sympy.<class>), which is what a wildcard head binds to -- NOT
        # Symbol('ArcSin'), which would never compare equal to the bound head.
        assert self.c.convert('ArcSin') == 'HeadRef(sympy.asin)'
        assert self.c.convert('ArcTan') == 'HeadRef(sympy.atan)'   # was missing from func_map
        assert self.c.convert('Sin') == 'HeadRef(sympy.sin)'
        assert self.c.convert('sin') == 'HeadRef(sympy.sin)'
        assert self.c.convert('FresnelS') == 'HeadRef(sympy.fresnels)'
        assert self.c.convert('SinIntegral') == 'HeadRef(sympy.Si)'

    def test_min_max_stay_plain_symbols(self):
        # Min/Max are NOT function-head values here -- they are the ordering sentinel of
        # Exponent[u, x, Min], which the deferred Exponent node detects by name. They must
        # stay Symbol('Min')/Symbol('Max'), not become a class/HeadRef.
        assert self.c.convert('Min') == "Symbol('Min')"
        assert self.c.convert('Max') == "Symbol('Max')"

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

    def test_reserved_name_pattern_is_not_a_wildcard(self):
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
        # `q` is a With-scope local: the binding list prints as a Python DICT and `q`
        # is emitted BARE (declared once at the module top as `q = Symbol('q')`), not
        # built inline as Symbol('q'). Because q now round-trips, the body simplifies
        # too (`q*.../(_m_ + 1)` instead of `q * (_m_ + 1)**(-1) * ...`).
        assert "replacement=With({q: DerivativeDivides(ActivateTrig(y_), ActivateTrig(u_), x)}, q*ActivateTrig(y_**(_m_ + 1))/(_m_ + 1))" in code


class TestHeaderNamespaceSync:
    """The generated-file import header and the shortening eval namespace MUST stay in
    lock-step: both are built from the single source
    ``FFLConverter.generated_code_sympy_names()``. If they drift, the shortener can emit
    a bare call that is invalid in the generated module (the load probe then silently
    skips the rule), or leave rules needlessly verbose. These tests fail if a future
    change breaks the single-source wiring."""

    def _header_namespace(self):
        import sympy  # noqa: F401 - used by exec'd header
        header = RubiRuleTranslator()._generate_header('test.module', 'test.src')
        ns = {}
        exec(header, ns)
        return ns

    def test_every_generated_sympy_name_is_importable_in_the_header(self):
        from sympy_wolfram.interpreter import FFLConverter
        ns = self._header_namespace()
        names = FFLConverter.generated_code_sympy_names()
        missing = [n for n in names if n not in ns]
        assert not missing, f"header is missing bare imports for: {missing}"
        # and they are the SAME objects the shortener evaluates against
        for name, obj in names.items():
            assert ns[name] is obj, f"header binds {name} to a different object"

    def test_eval_namespace_contains_every_generated_sympy_name(self):
        from sympy_wolfram.interpreter import FFLConverter
        eval_ns = FFLConverter().eval_ns
        names = FFLConverter.generated_code_sympy_names()
        missing = [n for n in names if eval_ns.get(n) is not names[n]]
        assert not missing, f"eval namespace out of sync with the single source: {missing}"

    def test_special_functions_are_synced(self):
        """Regression for the verbose-fresnels bug: the special functions must be BOTH
        importable in the file AND in the shortening namespace (else their rules never
        shorten)."""
        from sympy_wolfram.interpreter import FFLConverter
        import sympy
        ns = self._header_namespace()
        eval_ns = FFLConverter().eval_ns
        for name in ('fresnels', 'fresnelc', 'erf', 'erfi', 'erfc',
                     'Ei', 'li', 'Si', 'Ci', 'Shi', 'Chi'):
            assert ns.get(name) is getattr(sympy, name)
            assert eval_ns.get(name) is getattr(sympy, name)

    def test_and_or_not_stay_placeholders(self):
        """And/Or/Not are NOT part of the single source: they remain unevaluated Function
        heads in the eval namespace so shortening preserves their call-form (and arg
        order) instead of rewriting to &/|/~."""
        from sympy_wolfram.interpreter import FFLConverter
        import sympy
        eval_ns = FFLConverter().eval_ns
        for name in ('And', 'Or', 'Not'):
            assert isinstance(eval_ns[name], sympy.core.function.UndefinedFunction)
        assert 'And' not in FFLConverter.generated_code_sympy_names()

    def test_E_stays_qualified(self):
        """E is deliberately excluded from the bare set (it can be a coefficient letter
        and would collide); it must stay ``sympy.E`` and not be imported bare."""
        from sympy_wolfram.interpreter import FFLConverter
        names = FFLConverter.generated_code_sympy_names()
        assert 'E' not in names and 'EulerGamma' not in names
        ns = self._header_namespace()
        assert ns.get('E') is None or 'E' not in ns


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
# \[Star] handling. SymPy now parses Rubi's `factor \[Star] Int[...]` natively into
# a proper ['Star', u, v] node, so the generator no longer reconstructs anything --
# it just translates the head. These tests pin that end-to-end behaviour: the Int
# factor must survive into the replacement, because a Star whose Int was lost would
# emit a non-integral replacement (a silent wrong answer).
# ---------------------------------------------------------------------------
from sympy.parsing.mathematica import parse_mathematica_to_fullformlist


class TestStarIsParsedNatively:

    def test_star_parses_to_a_binary_node(self):
        assert parse_mathematica_to_fullformlist(r"Simp[a] \[Star] Int[b,x]") == \
            ['Star', ['Simp', 'a'], ['Int', 'b', 'x']]

    def test_star_survives_a_line_break(self):
        r"""The operand used to be silently DROPPED when \[Star] ended a line."""
        assert parse_mathematica_to_fullformlist("Simp[a] \\[Star]\n  Int[b,x]") == \
            ['Star', ['Simp', 'a'], ['Int', 'b', 'x']]

    def test_no_postfix_star_marker_is_produced(self):
        """The old mis-parse buried a bare 'Star' marker inside a Times."""
        ffl = parse_mathematica_to_fullformlist(r"c/(a*b) \[Star] Int[u,x]")
        def has_marker(n):
            if isinstance(n, list):
                if len(n) == 2 and n[1] == 'Star':
                    return True
                return any(has_marker(c) for c in n)
            return False
        assert not has_marker(ffl)
        assert ffl[0] == 'Star'

    def test_a_star_rule_keeps_its_Int_in_the_replacement(self):
        rule = ['SetDelayed',
                ['Int', ['Power', 'x', ['Pattern', 'm', ['Blank']]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Star', ['Simp', ['Pattern', 'm', ['Blank']]],
                 ['Int', 'x', 'x']]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'SKIPPED' not in code
        assert 'Star(' in code
        assert 'Int(' in code


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

    def test_a_predicate_definition_consumes_a_number_but_is_not_a_skip(self):
        """Rule files also carry utility PREDICATE definitions (IntLinearQ,
        IntBinomialQ, IntQuadraticQ) as SetDelayed entries whose LHS is not
        ``Int[...]``. Those are hand-implemented in rubi_rules/utils/, so they are
        not translated -- but they are NOT failures either, and reporting them as
        "skipped" overstates how much of Rubi is missing. They must still consume a
        rule_number so numbering stays aligned with the source JSON.
        """
        import re as _re
        tr = RubiRuleTranslator()
        predicate = ['SetDelayed',
                     ['IntBinomialQ', ['Pattern', 'a', ['Blank']]],
                     'True']
        rules = [self._rule('2'), predicate, self._rule('3')]
        code = tr.translate_module(rules, module_name='test')
        nums = [int(n) for n in _re.findall(r'rule_number=(\d+)', code)]
        # the predicate took number 2, so the following rule is 3 -- not renumbered
        assert nums == [1, 3], f"expected [1, 3], got {nums}"
        # ...and it is reported as a non-rule, not as a skip
        assert 'SKIPPED' not in code
        assert '2 rules translated, 0 skipped' in code
        assert '1 non-rule predicate definition not counted' in code

    def test_a_genuinely_untranslatable_rule_is_still_reported_as_skipped(self):
        """A head wildcard appearing ONLY in the replacement has nothing to bind it
        (the pattern never matched it), so it cannot be translated -- this is the
        largest remaining skip category and must stay visible as a real skip.
        """
        tr = RubiRuleTranslator()
        bad = ['SetDelayed',
               ['Int', ['Power', 'x', ['Pattern', 'm', ['Blank']]],
                ['Pattern', 'x', ['Blank', 'Symbol']]],
               [['Pattern', 'trig', ['Blank']], 'x']]
        code = tr.translate_module([self._rule('2'), bad], module_name='test')
        assert 'SKIPPED' in code
        assert '1 skipped' in code
        assert 'non-rule predicate' not in code


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


# ---------------------------------------------------------------------------
# Derivative-of-a-wildcard-function: Rubi's ``Derivative[n_][f_][x_]``.
# In FFL this is a doubly-nested application, [[['Derivative', n], f], x], which
# becomes WildHeadDeriv[f_, x_, n_] in a pattern and WFDeriv[f, x, n] in a
# replacement.
# ---------------------------------------------------------------------------
from rubi_rules.codegen.generate import _ffl_is_deriv_head

_DERIV = lambda n, f, v: [[['Derivative', n], f], v]      # noqa: E731


class TestDerivativeHeadDetection:

    def test_detects_a_derivative_of_a_wildcard_function(self):
        assert _ffl_is_deriv_head(_DERIV(_PAT('n'), _PAT('f'), 'x')) is True

    def test_detects_a_derivative_of_a_concrete_function(self):
        assert _ffl_is_deriv_head([[['Derivative', '1'], 'f'], 'x']) is True

    def test_rejects_a_plain_application(self):
        assert _ffl_is_deriv_head(['Sin', 'x']) is False

    def test_rejects_a_plain_wildcard_head_application(self):
        assert _ffl_is_deriv_head([_PAT('F'), _PAT('v')]) is False

    def test_rejects_atoms_and_empties(self):
        assert _ffl_is_deriv_head('x') is False
        assert _ffl_is_deriv_head([]) is False
        assert _ffl_is_deriv_head(['Derivative', 'n']) is False

    def test_rejects_a_wrong_arity_inner_head(self):
        # [['Derivative'], f] -- Derivative without its order
        assert _ffl_is_deriv_head([[['Derivative'], 'f'], 'x']) is False


class TestDerivativeExtractionFromPattern:

    def test_rewrites_to_wild_head_deriv_reordering_to_f_var_order(self):
        new, heads = _extract_fhw_from_pattern(_DERIV(_PAT('n'), _PAT('f'), 'x'))
        assert new == ['WildHeadDeriv', _PAT('f'), 'x', _PAT('n')]
        assert heads == {'f'}

    def test_rewrites_when_nested_inside_a_product(self):
        ffl = ['Times', 'c', _DERIV(_PAT('n'), _PAT('f'), 'x')]
        new, heads = _extract_fhw_from_pattern(ffl)
        assert new == ['Times', 'c', ['WildHeadDeriv', _PAT('f'), 'x', _PAT('n')]]
        assert heads == {'f'}

    def test_a_concrete_order_is_preserved(self):
        new, heads = _extract_fhw_from_pattern([[['Derivative', '2'], _PAT('f')], 'x'])
        assert new == ['WildHeadDeriv', _PAT('f'), 'x', '2']
        assert heads == {'f'}

    def test_a_concrete_function_contributes_no_head_name(self):
        _new, heads = _extract_fhw_from_pattern([[['Derivative', _PAT('n')], 'f'], 'x'])
        assert heads == set()

    def test_coexists_with_a_plain_wildcard_head_application(self):
        ffl = ['Times', [_PAT('F'), 'x'], _DERIV(_PAT('n'), _PAT('f'), 'x')]
        new, heads = _extract_fhw_from_pattern(ffl)
        assert heads == {'F', 'f'}
        assert new == ['Times', ['WildHeadApp', _PAT('F'), 'x'],
                       ['WildHeadDeriv', _PAT('f'), 'x', _PAT('n')]]


class TestDerivativeRewriteInReplacement:

    def test_rewrites_to_wf_deriv_reordering_to_f_var_order(self):
        out = _rewrite_fhw_in_replacement([[['Derivative', 'n'], 'f'], 'x'], {'f': 'f'})
        assert out == ['WFDeriv', 'f', 'x', 'n']

    def test_rewrites_a_computed_order(self):
        ffl = [[['Derivative', ['Plus', 'n', '-1']], 'f'], 'x']
        out = _rewrite_fhw_in_replacement(ffl, {'f': 'f'})
        assert out == ['WFDeriv', 'f', 'x', ['Plus', 'n', '-1']]

    def test_rewrites_when_nested(self):
        ffl = ['Times', 'c', [[['Derivative', 'n'], 'f'], 'x']]
        out = _rewrite_fhw_in_replacement(ffl, {'f': 'f'})
        assert out == ['Times', 'c', ['WFDeriv', 'f', 'x', 'n']]

    def test_only_rewrites_heads_bound_by_the_pattern(self):
        # 'g' is not a pattern head wildcard, so it stays a literal Derivative
        ffl = [[['Derivative', 'n'], 'g'], 'x']
        assert _rewrite_fhw_in_replacement(ffl, {'f': 'f'}) == ffl

    def test_coexists_with_a_plain_wf_apply(self):
        ffl = ['Times', ['F', 'x'], [[['Derivative', 'n'], 'f'], 'x']]
        out = _rewrite_fhw_in_replacement(ffl, {'F': 'F', 'f': 'f'})
        assert out == ['Times', ['WFApply', 'F', 'x'], ['WFDeriv', 'f', 'x', 'n']]


class TestSelectorSymbolsAreDeclared:
    """Rubi's ``Expon[Px, x, Min]`` passes Min as a bare SYMBOL. The emitter
    round-trips code through SymPy's printer, which renders ``Symbol('Min')`` as
    the bare name ``Min``, so the generated module must bind that name or the
    rule dies with NameError at import time (it previously did, in 2 rules).
    """

    def _module(self):
        return RubiRuleTranslator().translate_module([], module_name='test')

    def test_header_binds_min_and_max(self):
        code = self._module()
        assert "Min = Symbol('Min')" in code
        assert "Max = Symbol('Max')" in code

    def test_the_binding_is_a_symbol_not_sympys_min_function(self):
        # Expon dispatches on str(selector) == 'Min', so it must be a Symbol.
        import sympy as _sympy
        ns = {}
        exec(self._module().split('RULES = [')[0], ns)
        assert isinstance(ns['Min'], _sympy.Symbol)
        assert str(ns['Min']) == 'Min'

    def test_an_expon_min_rule_now_survives_load_validation(self):
        rule = ['SetDelayed',
                ['Int', ['Times', ['Power', ['Pattern', 'Px', ['Blank']],
                                   ['Pattern', 'p', ['Blank']]]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Condition', ['Expon', 'Px', 'x', 'Min'],
                 ['PolyQ', 'Px', 'x']]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'SKIPPED' not in code
        assert 'Min' in code


class TestUpstreamArityTypoIsLabelledAsFaithful:
    """Rubi's 1.2.1.4 source contains `NeQ[e^2-4*d*f]` -- one argument, where every
    sibling line writes `NeQ[...,0]`. Mathematica does not silently accept it:
    Rubi guards each predicate with `CheckArguments`, so the call stays unevaluated,
    the `&&` guard is not True, and the rule never fires there either. Skipping it
    is faithful, so the emitted comment must say so rather than read like a gap.

    Verified against real Rubi in Mathematica:
        NeQ[1-4, 0] -> True
        NeQ[1-4]    -> NeQ::argr ... ; TrueQ -> False
    """

    def test_arity_error_is_reported_as_an_upstream_typo(self):
        rule = ['SetDelayed',
                ['Int', ['Power', 'x', ['Pattern', 'm', ['Blank']]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Condition', ['Power', 'x', '2'],
                 ['NeQ', ['Plus', ['Pattern', 'm', ['Blank']], '-1']]]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'SKIPPED' in code
        assert 'upstream Rubi arity typo' in code
        assert 'inert in Mathematica too' in code

    def test_a_correct_two_arg_predicate_is_not_flagged(self):
        rule = ['SetDelayed',
                ['Int', ['Power', 'x', ['Pattern', 'm', ['Blank']]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Condition', ['Power', 'x', '2'],
                 ['NeQ', ['Pattern', 'm', ['Blank']], '-1']]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'SKIPPED' not in code
        assert 'upstream Rubi arity typo' not in code


class TestHeadWildcardsInsideMatchQ:
    """``MatchQ[u, (d_.*trig_[e+f*x])^m_. /; MemberQ[{sin,...}, trig]]`` uses a
    wildcard as a function HEAD inside a GUARD rather than in the rule's integrand.
    `_extract_fhw_from_pattern` only ever saw the integrand, so these rules were
    skipped outright -- 6 trig rules, plus one guard that was silently DROPPED
    (rule 2692), which the generator itself warns broadens a rule unsafely.
    """

    def _matchq(self, pattern):
        return ['MatchQ', 'u', pattern]

    def test_a_head_wildcard_in_the_pattern_is_rewritten(self):
        from rubi_rules.codegen.generate import _rewrite_fhw_in_matchq
        node = self._matchq([_PAT('trig'), 'x'])
        assert _rewrite_fhw_in_matchq(node) == \
            ['MatchQ', 'u', ['WildHeadApp', _PAT('trig'), 'x']]

    def test_it_reaches_inside_a_condition_guard(self):
        from rubi_rules.codegen.generate import _rewrite_fhw_in_matchq
        node = self._matchq(['Condition', [_PAT('trig'), 'x'], ['MemberQ', 'l', 'trig']])
        out = _rewrite_fhw_in_matchq(node)
        assert out[2][0] == 'Condition'
        assert out[2][1] == ['WildHeadApp', _PAT('trig'), 'x']
        assert out[2][2] == ['MemberQ', 'l', 'trig']      # the test is left alone

    def test_the_subject_is_not_treated_as_a_pattern(self):
        """Argument 1 of MatchQ is an ordinary expression, not a pattern."""
        from rubi_rules.codegen.generate import _rewrite_fhw_in_matchq
        node = ['MatchQ', ['Sin', 'x'], [_PAT('trig'), 'x']]
        out = _rewrite_fhw_in_matchq(node)
        assert out[1] == ['Sin', 'x']

    def test_a_matchq_without_head_wildcards_is_unchanged(self):
        from rubi_rules.codegen.generate import _rewrite_fhw_in_matchq
        node = ['MatchQ', 'u', ['Power', 'x', _PAT('m')]]
        assert _rewrite_fhw_in_matchq(node) == node

    def test_it_finds_a_matchq_nested_in_a_guard(self):
        from rubi_rules.codegen.generate import _rewrite_fhw_in_matchq
        node = ['And', ['FreeQ', 'a', 'x'], ['Not', self._matchq([_PAT('F'), 'v'])]]
        out = _rewrite_fhw_in_matchq(node)
        assert out[2][1][2] == ['WildHeadApp', _PAT('F'), 'v']

    def test_such_a_rule_now_translates_and_declares_its_guard_local_wildcard(self):
        rule = ['SetDelayed',
                ['Int', ['Times', ['Optional', ['Pattern', 'u', ['Blank']]],
                         ['Power', 'x', ['Pattern', 'p', ['Blank']]]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Condition', ['Power', 'x', '2'],
                 ['MatchQ', 'u', ['Condition', [_PAT('trig'), 'x'],
                                  ['FreeQ', 'u', 'x']]]]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'SKIPPED' not in code
        assert 'WildHeadApp(trig_' in code
        # the guard-local head wildcard must be DECLARED, or the module won't import
        assert "trig_ = WildSymbol('trig')" in code

    def test_no_guard_is_dropped_for_a_head_wildcard_any_more(self):
        rule = ['SetDelayed',
                ['Int', ['Times', ['Optional', ['Pattern', 'u', ['Blank']]],
                         ['Power', 'x', ['Pattern', 'p', ['Blank']]]],
                 ['Pattern', 'x', ['Blank', 'Symbol']]],
                ['Condition', ['Power', 'x', '2'],
                 ['Not', ['MatchQ', 'u', [_PAT('F'), 'x']]]]]
        code = RubiRuleTranslator().translate_module([rule], module_name='test')
        assert 'dropped guard' not in code
        assert 'Not(MatchQ(' in code


class TestGeneratedRulesetInvariants:
    """Whole-ruleset guards. These read the CHECKED-IN generated files, so they are
    fast (no rule set is loaded) and they fail loudly if a future codegen change
    silently starts skipping rules or dropping guards again."""

    RULES_DIR = Path(__file__).resolve().parents[1] / 'rules'

    def _all_text(self):
        return [(p, p.read_text(encoding='utf-8'))
                for p in self.RULES_DIR.rglob('*.py')]

    def test_no_guard_is_ever_dropped(self):
        """A dropped guard broadens a rule and can yield wrong answers, so the
        ruleset must ship with none."""
        offenders = [str(p) for p, t in self._all_text() if 'dropped guard' in t]
        assert offenders == []

    def test_only_the_two_known_rules_are_skipped(self):
        """Everything Rubi can actually run must translate; any OTHER skip is a
        regression in this port. The two known exceptions are:

        1. Rubi's own `NeQ[e^2-4*d*f]` (one argument), which Mathematica leaves
           unevaluated so the rule never fires there either -- verified against real
           Rubi.
        2. The Weierstrass half-angle substitution (4.7.5 #71). It arrived with the
           `If[TrueQ[$LoadShowSteps], ...]` unwrapping, and its nested
           `Block[{...}, Int[SubstFor[...]]]` does not survive the generator's
           load-validation yet. It was absent from this port before that unwrapping
           too, so skipping it loses nothing that used to work -- but it IS a real
           Rubi rule and wiring it up is outstanding work, not an accepted quirk.
        """
        skips = [line.strip()
                 for _p, t in self._all_text()
                 for line in t.splitlines() if 'SKIPPED' in line]
        assert len(skips) == 2, skips
        assert any('upstream Rubi arity typo' in s for s in skips), skips
        assert any('is_Float' in s for s in skips), skips

    def test_head_wildcards_inside_matchq_guards_are_emitted(self):
        """The 6 trig rules whose guard matches `trig_[e+f*x]` for any trig head."""
        n = sum(t.count('WildHeadApp(trig_') for _p, t in self._all_text())
        assert n >= 6


class TestPostfixDerivativeIsParsedNatively:
    r"""Rubi writes 6 rules with the postfix derivative ``f_'[x_]``. We used to
    normalise that to ``Derivative[1][f_][x_]`` textually because SymPy mis-parsed
    it in an INFIX context (``f'[x]*g[x]`` swallowed the operator). SymPy handles it
    now and the workaround is gone, so these pin the dependency: if the parser
    regresses, the product/quotient rules silently vanish from the ruleset again.
    """

    def test_a_bare_prime_application(self):
        assert parse_mathematica_to_fullformlist("f'[x]") == \
            [[['Derivative', '1'], 'f'], 'x']

    def test_a_prime_followed_by_an_infix_operator(self):
        """The case that used to break: the application swallowed the operator."""
        assert parse_mathematica_to_fullformlist("f'[x]*g[x]") == \
            ['Times', [[['Derivative', '1'], 'f'], 'x'], ['g', 'x']]

    def test_a_prime_on_a_pattern_inside_a_full_rule(self):
        ffl = parse_mathematica_to_fullformlist(
            "Int[f_'[x_]*g_[x_] + f_[x_]*g_'[x_], x_Symbol]")
        assert ffl[0] == 'Int'
        assert ffl[1][0] == 'Plus'          # a real sum, not a mangled application

    def test_the_second_derivative_form(self):
        assert parse_mathematica_to_fullformlist("f''[x]") == \
            [[['Derivative', '2'], 'f'], 'x']

    def test_the_product_and_quotient_rules_are_in_the_shipped_ruleset(self):
        """End-to-end: those 6 rules must actually be emitted."""
        rules_dir = Path(__file__).resolve().parents[1] / 'rules' / 'r_9_miscellaneous'
        text = '\n'.join(p.read_text(encoding='utf-8') for p in rules_dir.glob('*.py'))
        # Int[f'g + f g'] -> f g  and the quotient-rule shape
        assert text.count('WildHeadDeriv(f_, x, 1)') >= 2
        assert 'WFApply(f_, x)*WFApply(g_, x)' in text
