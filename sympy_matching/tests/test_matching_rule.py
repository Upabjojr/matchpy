# -*- coding: utf-8 -*-
"""The reusable SymPy -> matchpy rule machinery works with ONLY matchpy + sympy_matching.

This is the acceptance test for the refactor that lifted ``SympyMatchingRule`` /
``SympyMatchingConstraint`` / ``build_tracing_replacer`` out of rubi_rules/sympy_wolfram:
a caller can define pattern-matching rules over ordinary SymPy expressions mixed with
``WildSymbol`` -- with custom constraints -- and build a working matchpy
``ManyToOneReplacer``, importing NOTHING from ``sympy_wolfram`` or ``rubi_rules``.
"""
import ast
import importlib

import sympy
from sympy import Symbol, Integer, sin, cos

# Only matchpy + sympy_matching -- no sympy_wolfram, no rubi_rules.
from sympy_matching import (
    WildSymbol,
    SympyMatchingRule,
    SympyMatchingConstraint,
    build_tracing_replacer,
    to_matchpy_expression,
    matchpy_to_sympy,
)


class _IsInteger(SympyMatchingConstraint):
    """Custom constraint: the matched value must be an explicit SymPy Integer."""
    def __init__(self, u):
        self._u = self.args[0]

    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return bool(getattr(u, 'is_Integer', False))


def _apply_first(replacer, subject_expr):
    """Mirror how a matcher uses the tracing replacer: take the first match, run its
    replacement callback (which returns ``(result, trace_label)``), return the SymPy
    result and the trace label -- or ``(None, None)`` if nothing matched."""
    mp = to_matchpy_expression(subject_expr)
    for replacement, subst in replacer.matcher.match(mp):
        result_mp, label = replacement(**subst)
        return matchpy_to_sympy(result_mp), label
    return None, None


def test_layer_purity_no_wolfram_or_rubi():
    """sympy_matching's rule machinery must not import sympy_wolfram or rubi_rules."""
    for modname in ('sympy_matching.matching_rule', 'sympy_matching.constraint'):
        m = importlib.import_module(modname)
        tree = ast.parse(open(m.__file__).read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                blob = (getattr(node, 'module', '') or '') + ' ' + ' '.join(a.name for a in node.names)
                assert 'sympy_wolfram' not in blob and 'rubi_rules' not in blob, \
                    f"{modname} imports upward: {blob}"


def test_build_replacer_and_match_with_constraint():
    a_ = WildSymbol('a')
    # Rule: sin(a_) -> a_ + 1, but only when a_ is an integer.
    rule = SympyMatchingRule(
        pattern=sin(a_),
        constraints=(_IsInteger(a_),),
        replacement=a_ + 1,
        module_name='demo',
        rule_number=1,
    )
    replacer = build_tracing_replacer([rule])

    # Constraint satisfied: sin(3) -> 3 + 1 = 4, traced to ('demo', 1).
    res, label = _apply_first(replacer, sin(Integer(3)))
    assert res == Integer(4)
    assert label == ('demo', 1)

    # Constraint fails (x is not an integer): no match, expression untouched.
    res2, label2 = _apply_first(replacer, sin(Symbol('x')))
    assert res2 is None and label2 is None


def test_bare_sympy_boolean_constraint():
    """A plain SymPy relational (no SympyMatchingConstraint subclass) also works as a guard."""
    a_ = WildSymbol('a')
    rule = SympyMatchingRule(
        pattern=cos(a_),
        constraints=(sympy.Ne(a_, 0),),           # fire only when a_ != 0
        replacement=a_ ** 2,
        module_name='demo',
        rule_number=2,
    )
    replacer = build_tracing_replacer([rule])
    res, _ = _apply_first(replacer, cos(Integer(5)))
    assert res == Integer(25)
    res0, _ = _apply_first(replacer, cos(Integer(0)))
    assert res0 is None                            # Ne(0, 0) is False -> refused


def test_constraint_is_sympy_boolean_and_composes():
    """A SympyMatchingConstraint is a SymPy Boolean, so Not/And/Or compose."""
    a_ = WildSymbol('a')
    c = _IsInteger(a_)
    assert isinstance(c, sympy.logic.boolalg.Boolean)
    assert isinstance(sympy.Not(c), sympy.logic.boolalg.Boolean)
    assert c.variables == ('a',)
    assert c.check(a=Integer(7)) is True
    assert c.check(a=Symbol('y')) is False


def test_matchpy_to_sympy_is_extensible_via_singledispatch():
    """matchpy_to_sympy is a singledispatch function: an external library can
    register a converter for its own MatchPy node type without touching this one."""
    import functools
    assert hasattr(matchpy_to_sympy, 'register')     # singledispatch API
    assert hasattr(matchpy_to_sympy, 'dispatch')

    class _FakeNode:                                  # not a matchpy Expression at all
        pass

    @matchpy_to_sympy.register(_FakeNode)
    def _convert_fake(node):
        return sympy.Symbol('converted_fake')

    try:
        assert matchpy_to_sympy(_FakeNode()) == sympy.Symbol('converted_fake')
    finally:
        # singledispatch has no unregister; point the type at the fallback instead
        matchpy_to_sympy.register(_FakeNode)(lambda n: n)


def test_register_head_converter_extension_point():
    """Operations with unregistered heads dispatch through the public head-name
    registry -- an external library can claim a head name."""
    from matchpy.expressions.expressions import Operation, OperationHead
    from sympy_matching import register_head_converter
    from sympy_matching.conversion import _HEAD_NAME_CONVERTERS

    @register_head_converter('MyExternalHead')
    def _convert(args):
        return sympy.Symbol('external') + sum(args)

    try:
        head = OperationHead(name='MyExternalHead')
        mp = Operation(head, to_matchpy_expression(sympy.Integer(2)), to_matchpy_expression(sympy.Integer(3)))
        assert matchpy_to_sympy(mp) == sympy.Symbol('external') + 5
    finally:
        del _HEAD_NAME_CONVERTERS['MyExternalHead']


def test_json_deserializer_registration_is_public():
    """JSON wrapped-value round-trip for a custom tag via the public register API."""
    from matchpy.matching.json_serialization import (
        serialize_wrapped_value, deserialize_wrapped_value, register_wrapped_value_deserializer,
    )

    class _Marker:
        def __init__(self, payload):
            self.payload = payload

    @serialize_wrapped_value.register(_Marker)
    def _ser(val):
        return {'_val_type': 'marker', 'payload': val.payload}

    @register_wrapped_value_deserializer('marker')
    def _deser(data):
        return _Marker(data['payload'])

    blob = serialize_wrapped_value(_Marker(42))
    restored = deserialize_wrapped_value(blob)
    assert isinstance(restored, _Marker) and restored.payload == 42


def test_conversion_round_trip():
    """to_matchpy_expression / matchpy_to_sympy round-trip a SymPy expression."""
    x = sympy.Symbol('x')
    expr = sympy.sin(x) + sympy.Integer(2)
    assert matchpy_to_sympy(to_matchpy_expression(expr)) == expr


def test_from_expression_is_generic_not_sympy():
    """matchpy's from_matchpy_expression stays domain-agnostic: NamedAtom -> its NAME (str),
    while matchpy_to_sympy maps the same node to a sympy.Symbol. The two reverse
    functions are deliberately distinct dispatches."""
    from matchpy.expressions.expressions import from_matchpy_expression, NamedAtom
    atom = NamedAtom('q')
    assert from_matchpy_expression(atom) == 'q'
    assert matchpy_to_sympy(atom) == sympy.Symbol('q')
    assert from_matchpy_expression is not matchpy_to_sympy
