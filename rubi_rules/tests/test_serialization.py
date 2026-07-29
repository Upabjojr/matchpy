# -*- coding: utf-8 -*-
"""Tests for serialization/deserialization of Rubi rules and replacers.

Tests that:
- SymPyReplacementPattern expressions (pattern + replacement) survive JSON roundtrip
- Constraint objects can be serialized and deserialized
- A full replacer can be serialized, deserialized, and still integrates correctly
"""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import sympy
from sympy import Symbol, Integer, Rational, log, sqrt, sin, cos, pi

from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
from sympy_matching.conversion import to_matchpy_expression, matchpy_to_sympy
import sympy_matching  # registers json_ext handlers

from matchpy.matching.json_serialization import serialize_wrapped_value, deserialize_wrapped_value
from sympy_matching.json_ext import deserialize_sympy_expr

from rubi_rules.base_objects import Int, SymPyReplacementPattern, _rubi_integrator, build_tracing_replacer
from rubi_rules.utils import FreeQ, NeQ, IntegerQ, PositiveQ, NegativeQ


# --- Fixtures ---

@pytest.fixture
def x():
    return Symbol('x')

@pytest.fixture
def wild_symbols():
    a_ = WildSymbol('a_', optional_value=IDENTITY_ELEMENT)
    b_ = WildSymbol('b_', optional_value=IDENTITY_ELEMENT)
    m_ = WildSymbol('m_')
    n_ = WildSymbol('n_')
    return a_, b_, m_, n_


# =============================================================================
# Test: SymPy expression serialization roundtrip
# =============================================================================

class TestExpressionSerialization:
    """Test that SymPy expressions containing WildSymbol survive JSON roundtrip."""

    def test_simple_symbol(self, x):
        s = serialize_wrapped_value(x)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(x)

    def test_wild_symbol(self, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        s = serialize_wrapped_value(m_)
        d = deserialize_wrapped_value(s)
        assert d.name == m_.name
        assert isinstance(d, WildSymbol)

    def test_wild_symbol_with_optional(self, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        s = serialize_wrapped_value(a_)
        d = deserialize_wrapped_value(s)
        assert d.name == a_.name
        assert isinstance(d, WildSymbol)

    def test_integer(self):
        for n in [0, 1, -1, 42, -99]:
            s = serialize_wrapped_value(Integer(n))
            d = deserialize_wrapped_value(s)
            assert d == Integer(n)

    def test_rational(self):
        for p, q in [(1, 2), (3, 4), (-5, 7)]:
            val = Rational(p, q)
            s = serialize_wrapped_value(val)
            d = deserialize_wrapped_value(s)
            assert d == val

    def test_constants(self):
        for const in [sympy.pi, sympy.E, sympy.I, sympy.oo]:
            s = serialize_wrapped_value(const)
            d = deserialize_wrapped_value(s)
            assert d == const

    def test_power_with_wild(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = x**m_
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_add_with_wilds(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = a_ + b_*x
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_compound_expression(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = (a_ + b_*x)**(m_ + 1) / (b_*(m_ + 1))
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_log_expression(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = log(a_ + b_*x) / b_
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_int_function(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = Int(x**m_, x)
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_nested_int(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        expr = Int((a_ + b_*x)**m_, x)
        s = serialize_wrapped_value(expr)
        d = deserialize_wrapped_value(s)
        assert sympy.srepr(d) == sympy.srepr(expr)

    def test_json_string_roundtrip(self, x, wild_symbols):
        """Verify serialization goes through JSON string correctly."""
        a_, b_, m_, n_ = wild_symbols
        expr = (a_ + b_*x)**(m_ + 1) / (b_*(m_ + 1))
        s = serialize_wrapped_value(expr)
        json_str = json.dumps(s)
        loaded = json.loads(json_str)
        d = deserialize_wrapped_value(loaded)
        assert sympy.srepr(d) == sympy.srepr(expr)


# =============================================================================
# Test: Constraint serialization
# =============================================================================


# =============================================================================
# Test: Full SymPyReplacementPattern serialization
# =============================================================================

class TestSymPyReplacementPatternSerialization:
    """Test that a full SymPyReplacementPattern can be serialized and deserialized."""

    def _serialize_rule(self, rule):
        """Serialize a SymPyReplacementPattern to JSON-safe dict."""
        constraints_data = []
        for c in rule.constraints:
            # Use SymPy's func(*args) invariant: store class name + args
            constraints_data.append({
                'cls': type(c).__name__,
                'args': [serialize_wrapped_value(a) for a in c.args],
            })
        return {
            'pattern': serialize_wrapped_value(rule.pattern),
            'constraints': constraints_data,
            'replacement': serialize_wrapped_value(rule.replacement),
        }

    def _deserialize_rule(self, data):
        """Deserialize a SymPyReplacementPattern from a dict."""
        wild_cache = {}
        pattern = deserialize_sympy_expr(data['pattern'], wild_cache)
        replacement = deserialize_sympy_expr(data['replacement'], wild_cache)

        cls_map = {
            'FreeQ': FreeQ, 'NeQ': NeQ, 'IntegerQ': IntegerQ,
            'PositiveQ': PositiveQ, 'NegativeQ': NegativeQ,
        }
        constraints = []
        for cd in data['constraints']:
            cls = cls_map[cd['cls']]
            args = [deserialize_wrapped_value(a) for a in cd['args']]
            constraints.append(cls(*args))

        return SymPyReplacementPattern(
            pattern=pattern,
            constraints=tuple(constraints),
            replacement=replacement,
            module_name="TEST",
            rule_number=1,
        )

    def test_simple_rule_roundtrip(self, x):
        rule = SymPyReplacementPattern(
            pattern=Int(1/x, x),
            constraints=(),
            replacement=log(x),
            module_name="TEST",
            rule_number=1,
        )
        s = self._serialize_rule(rule)
        d = self._deserialize_rule(s)
        assert sympy.srepr(d.pattern) == sympy.srepr(rule.pattern)
        assert sympy.srepr(d.replacement) == sympy.srepr(rule.replacement)
        assert len(d.constraints) == 0

    def test_rule_with_constraints(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        rule = SymPyReplacementPattern(
            pattern=Int(x**m_, x),
            constraints=(FreeQ(m_, x), NeQ(m_, -1)),
            replacement=x**(m_ + 1)/(m_ + 1),
            module_name="TEST",
            rule_number=1,
        )
        s = self._serialize_rule(rule)
        d = self._deserialize_rule(s)
        assert sympy.srepr(d.pattern) == sympy.srepr(rule.pattern)
        assert sympy.srepr(d.replacement) == sympy.srepr(rule.replacement)
        assert len(d.constraints) == 2
        assert d.constraints[0].variables[0] == 'm'
        assert d.constraints[1].variables[0] == 'm'
        assert d.constraints[1]._v == Integer(-1)

    def test_full_json_string_roundtrip(self, x, wild_symbols):
        a_, b_, m_, n_ = wild_symbols
        rule = SymPyReplacementPattern(
            pattern=Int((a_ + b_*x)**m_, x),
            constraints=(FreeQ(a_, x), FreeQ(b_, x), FreeQ(m_, x), NeQ(m_, -1)),
            replacement=(a_ + b_*x)**(m_ + 1) / (b_*(m_ + 1)),
            module_name="TEST",
            rule_number=1,
        )
        s = self._serialize_rule(rule)
        json_str = json.dumps(s)
        loaded = json.loads(json_str)
        d = self._deserialize_rule(loaded)
        assert sympy.srepr(d.pattern) == sympy.srepr(rule.pattern)
        assert sympy.srepr(d.replacement) == sympy.srepr(rule.replacement)
        assert len(d.constraints) == 4


# =============================================================================
# Test: Functional roundtrip — serialize rules, rebuild replacer, integrate
# =============================================================================

class TestFunctionalRoundtrip:
    """Test that serialized rules rebuild a working replacer."""

    def _serialize_rules(self, rules):
        """Serialize a list of SymPyReplacementPattern."""
        result = []
        for rule in rules:
            constraints_data = []
            for c in rule.constraints:
                constraints_data.append({
                    'cls': type(c).__name__,
                    'args': [serialize_wrapped_value(a) for a in c.args],
                })
            result.append({
                'pattern': serialize_wrapped_value(rule.pattern),
                'constraints': constraints_data,
                'replacement': serialize_wrapped_value(rule.replacement),
            })
        return result

    def _deserialize_rules(self, data_list):
        """Deserialize a list of SymPyReplacementPattern using shared wild_cache."""
        cls_map = {'FreeQ': FreeQ, 'NeQ': NeQ, 'IntegerQ': IntegerQ,
                   'PositiveQ': PositiveQ, 'NegativeQ': NegativeQ}
        rules = []
        for data in data_list:
            wild_cache = {}
            pattern = deserialize_sympy_expr(data['pattern'], wild_cache)
            replacement = deserialize_sympy_expr(data['replacement'], wild_cache)
            constraints = []
            for cd in data['constraints']:
                cls = cls_map[cd['cls']]
                args = [deserialize_wrapped_value(a) for a in cd['args']]
                constraints.append(cls(*args))
            rules.append(SymPyReplacementPattern(
                pattern=pattern, constraints=tuple(constraints), replacement=replacement,
                module_name="TEST",
                rule_number=1,
            ))
        return rules

    def test_single_rule_integrate(self, x):
        """Serialize 1 rule, rebuild, integrate."""
        rules = [SymPyReplacementPattern(
                    pattern=Int(1/x, x), constraints=(), replacement=log(x),
                    module_name="TEST",
                    rule_number=1,
            )]
        data = self._serialize_rules(rules)
        json_str = json.dumps(data)
        loaded = json.loads(json_str)
        rebuilt = self._deserialize_rules(loaded)
        replacer = build_tracing_replacer(rebuilt)

        int_expr = to_matchpy_expression(Int(1/x, x))
        result = matchpy_to_sympy(replacer.replace(int_expr)[0])
        assert sympy.simplify(result - log(x)) == 0

    def test_power_rule_integrate(self, x, wild_symbols):
        """Serialize power rule with constraints, rebuild, integrate."""
        a_, b_, m_, n_ = wild_symbols
        rules = [
            SymPyReplacementPattern(
                pattern=Int(x**m_, x),
                constraints=(FreeQ(m_, x), NeQ(m_, -1)),
                replacement=x**(m_ + 1)/(m_ + 1),
                module_name="TEST",
                rule_number=1,
            ),
        ]
        data = self._serialize_rules(rules)
        json_str = json.dumps(data)
        loaded = json.loads(json_str)
        rebuilt = self._deserialize_rules(loaded)
        replacer = build_tracing_replacer(rebuilt)

        # Test x^2
        int_expr = to_matchpy_expression(Int(x**2, x))
        result = matchpy_to_sympy(replacer.replace(int_expr)[0])
        assert sympy.simplify(result - x**3/3) == 0

        # Test x^(1/2)
        int_expr = to_matchpy_expression(Int(sqrt(x), x))
        result = matchpy_to_sympy(replacer.replace(int_expr)[0])
        assert sympy.simplify(result - 2*x**Rational(3, 2)/3) == 0

    def test_multiple_rules_integrate(self, x, wild_symbols):
        """Serialize multiple rules, rebuild, integrate different expressions."""
        a_, b_, m_, n_ = wild_symbols
        rules = [
            SymPyReplacementPattern(pattern=Int(1/x, x), constraints=(), replacement=log(x)),
            SymPyReplacementPattern(
                pattern=Int(x**m_, x),
                constraints=(FreeQ(m_, x), NeQ(m_, -1)),
                replacement=x**(m_ + 1)/(m_ + 1),
                module_name="TEST",
                rule_number=1,
            ),
            SymPyReplacementPattern(
                pattern=Int(1/(a_ + b_*x), x),
                constraints=(FreeQ(a_, x), FreeQ(b_, x)),
                replacement=log(a_ + b_*x)/b_,
                module_name="TEST",
                rule_number=2,
            ),
        ]
        data = self._serialize_rules(rules)
        json_str = json.dumps(data)
        loaded = json.loads(json_str)
        rebuilt = self._deserialize_rules(loaded)
        replacer = build_tracing_replacer(rebuilt)

        a, b = sympy.symbols('a b')

        # int 1/x = log(x)
        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(1/x, x)))[0])
        assert sympy.simplify(result - log(x)) == 0

        # int x^2 = x^3/3
        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(x**2, x)))[0])
        assert sympy.simplify(result - x**3/3) == 0

        # int 1/(a+bx) = log(a+bx)/b
        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(1/(a + b*x), x)))[0])
        assert sympy.simplify(result - log(a + b*x)/b) == 0

    def test_loaded_rules_roundtrip(self, x):
        """Load actual generated rules, serialize, deserialize, integrate."""
        from pathlib import Path
        rules_dir = Path(os.path.dirname(__file__)).parent / 'rules'
        if not rules_dir.exists():
            pytest.skip("Generated rules not available")

        # Load rules from file (just 1.1.1.1 for speed)
        replacer_orig = _rubi_integrator.load_rule_patterns('r_1_algebraic/r_1_1_binomial_products/r_1_1_1_linear/r_1_1_1_1*')

        # Get the rules by loading the module
        import importlib.util
        rule_file = rules_dir / 'r_1_algebraic' / 'r_1_1_binomial_products' / 'r_1_1_1_linear' / 'r_1_1_1_1.py'
        if not rule_file.exists():
            pytest.skip("r_1_1_1_1.py not generated yet")

        spec = importlib.util.spec_from_file_location("r_1_1_1_1", rule_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rules = mod.RULES

        # Serialize all rules
        data = self._serialize_rules(rules)
        json_str = json.dumps(data)
        assert len(json_str) > 100  # sanity check

        # Deserialize
        loaded = json.loads(json_str)
        rebuilt = self._deserialize_rules(loaded)
        replacer = build_tracing_replacer(rebuilt)

        # Test integration
        a, b = sympy.symbols('a b')

        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(1/x, x)))[0])
        assert sympy.simplify(result - log(x)) == 0

        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(x**2, x)))[0])
        assert sympy.simplify(result - x**3/3) == 0

        result = matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(1/(a + b*x), x)))[0])
        assert sympy.simplify(result - log(a + b*x)/b) == 0


# =============================================================================
# Test: ManyToOneReplacer serialization via to_json / from_json
# =============================================================================

class TestManyToOneReplacerSerialization:
    """Test that a ManyToOneReplacer's internal matcher can be serialized.

    The replacer stores replacement functions as closure labels in its matcher.
    Serialization captures the SymPy replacement expression from the closure;
    deserialization rebuilds the function so the replacer works after roundtrip.
    """

    @pytest.fixture
    def replacer_with_rules(self, x, wild_symbols):
        """Build a replacer with multiple rules."""
        a_, b_, m_, n_ = wild_symbols
        rules = [
            SymPyReplacementPattern(
                pattern=Int(1/x, x),
                constraints=(),
                replacement=log(x),
                module_name="TEST",
                rule_number=1,
            ),
            SymPyReplacementPattern(
                pattern=Int(x**m_, x),
                constraints=(FreeQ(m_, x), NeQ(m_, -1)),
                replacement=x**(m_ + 1)/(m_ + 1),
                module_name="TEST",
                rule_number=2,
            ),
            SymPyReplacementPattern(
                pattern=Int(1/(a_ + b_*x), x),
                constraints=(FreeQ(a_, x), FreeQ(b_, x)),
                replacement=log(a_ + b_*x)/b_,
                module_name="TEST",
                rule_number=3,
            ),
            SymPyReplacementPattern(
                pattern=Int((a_ + b_*x)**m_, x),
                constraints=(FreeQ(a_, x), FreeQ(b_, x), FreeQ(m_, x), NeQ(m_, -1)),
                replacement=(a_ + b_*x)**(m_ + 1)/(b_*(m_ + 1)),
                module_name="TEST",
                rule_number=4,
            ),
        ]
        return build_tracing_replacer(rules)

    def _roundtrip_replacer(self, replacer):
        """Serialize and deserialize a replacer's matcher."""
        from matchpy.matching.json_serialization import to_json, from_json
        from matchpy.matching.many_to_one import ManyToOneReplacer
        json_str = to_json(replacer.matcher)
        matcher2 = from_json(json_str)
        replacer2 = ManyToOneReplacer()
        replacer2.matcher = matcher2
        return replacer2, json_str

    def test_serialize_produces_valid_json(self, replacer_with_rules):
        """Serialization produces a valid JSON string with expected keys."""
        from matchpy.matching.json_serialization import to_json
        json_str = to_json(replacer_with_rules.matcher)
        data = json.loads(json_str)
        assert 'patterns' in data
        assert 'root' in data
        assert len(data['patterns']) == 4

    def test_replacement_labels_serialized_as_replacement_fn(self, replacer_with_rules):
        """Labels are stored with _kind='replacement_fn'."""
        from matchpy.matching.json_serialization import to_json
        data = json.loads(to_json(replacer_with_rules.matcher))
        for pat_data, label_data, ci in data['patterns']:
            assert label_data['_kind'] == 'replacement_fn'
            assert 'replacement_expr' in label_data

    def test_deserialize_restores_pattern_count(self, replacer_with_rules):
        """Deserialized matcher has the same number of patterns."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        assert len(replacer2.matcher.patterns) == 4

    def test_deserialized_labels_are_callable(self, replacer_with_rules):
        """Deserialized labels are callable replacement functions."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        for pat, label, ci in replacer2.matcher.patterns:
            assert callable(label)

    def test_roundtrip_integrate_1_over_x(self, x, replacer_with_rules):
        """After roundtrip, int 1/x dx = log(x)."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int(1/x, x))))
        assert sympy.simplify(result - log(x)) == 0

    def test_roundtrip_integrate_power(self, x, replacer_with_rules):
        """After roundtrip, int x^2 dx = x^3/3."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int(x**2, x))))
        assert sympy.simplify(result - x**3/3) == 0

    def test_roundtrip_integrate_sqrt(self, x, replacer_with_rules):
        """After roundtrip, int sqrt(x) dx = 2x^(3/2)/3."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int(sqrt(x), x))))
        assert sympy.simplify(result - 2*x**Rational(3, 2)/3) == 0

    def test_roundtrip_integrate_linear(self, x, replacer_with_rules):
        """After roundtrip, int 1/(a+bx) dx = log(a+bx)/b."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        a, b = sympy.symbols('a b')
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int(1/(a + b*x), x))))
        assert sympy.simplify(result - log(a + b*x)/b) == 0

    def test_roundtrip_integrate_binomial_power(self, x, replacer_with_rules):
        """After roundtrip, int (a+bx)^2 dx = (a+bx)^3/(3b)."""
        replacer2, _ = self._roundtrip_replacer(replacer_with_rules)
        a, b = sympy.symbols('a b')
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int((a + b*x)**2, x))))
        assert sympy.simplify(result - (a + b*x)**3/(3*b)) == 0

    def test_json_string_full_roundtrip(self, x, replacer_with_rules):
        """dumps -> loads -> deserialize produces working replacer."""
        from matchpy.matching.json_serialization import to_json, from_json
        from matchpy.matching.many_to_one import ManyToOneReplacer
        json_str = to_json(replacer_with_rules.matcher)
        data = json.loads(json_str)
        json_str2 = json.dumps(data)
        matcher2 = from_json(json_str2)
        replacer2 = ManyToOneReplacer()
        replacer2.matcher = matcher2
        result = matchpy_to_sympy(replacer2.replace(to_matchpy_expression(Int(x**2, x))))
        assert sympy.simplify(result - x**3/3) == 0
