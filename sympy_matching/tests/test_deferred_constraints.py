# -*- coding: utf-8 -*-
"""`build_replacer(defer_constraint=...)`: guards deferred to attempt time.

Consumers that sort the matcher's yields by rule priority EXHAUST the match generator,
and omnimatch evaluates Pattern-attached constraints for EVERY candidate during
enumeration. A guard that is itself expensive (in a rewrite system: one that
recursively invokes the system) then runs once per candidate before the first rule is
ever attempted. `defer_constraint` moves selected guards into the replacement
callback: they run at ATTEMPT time, in whatever order the caller attempts candidates,
and a failure raises StopIteration -- the ordinary "condition failed" signal.

These tests pin the mechanism with a SPY constraint that records when it is evaluated.
"""
import pytest
from sympy import Symbol

from sympy_matching.constraint import SymPyMatchingConstraint
from sympy_matching.matching_rule import (
    SymPyReplacementPattern, build_replacer, to_omnimatch_expression)
from sympy_matching.wild import WildSymbol

x = Symbol('x')
m_ = WildSymbol('m')


class SpyConstraint(SymPyMatchingConstraint):
    """Records every evaluation; verdict is configured per instance name."""
    calls: list = []            # class-level log: (tag, bindings)

    def check(self, **bindings):
        tag = str(self.args[0])
        SpyConstraint.calls.append(tag)
        return not tag.startswith('fail')


def _rule(tag):
    return SymPyReplacementPattern(
        pattern=x**m_,
        constraints=(SpyConstraint(Symbol(tag)),),
        replacement=Symbol(tag),
        module_name='spy', rule_number=1,
    )


def test_without_deferral_the_guard_runs_during_enumeration():
    SpyConstraint.calls = []
    rep = build_replacer([_rule('pass_a')])
    list(rep.matcher.match(to_omnimatch_expression(x**3)))   # enumerate ONLY
    assert SpyConstraint.calls == ['pass_a'], \
        'a Pattern-attached guard is evaluated by match() itself'


def test_deferred_guard_does_not_run_during_enumeration():
    SpyConstraint.calls = []
    rep = build_replacer([_rule('pass_a')], defer_constraint=lambda c: True)
    matches = list(rep.matcher.match(to_omnimatch_expression(x**3)))
    assert SpyConstraint.calls == [], 'deferred guards must not run during match()'
    assert len(matches) == 1, 'the candidate is still yielded'


def test_deferred_guard_runs_at_attempt_time_and_passes():
    SpyConstraint.calls = []
    rep = build_replacer([_rule('pass_a')], defer_constraint=lambda c: True)
    [(replacement, subst)] = list(rep.matcher.match(to_omnimatch_expression(x**3)))
    result = replacement(**subst)
    assert SpyConstraint.calls == ['pass_a']
    assert result is not None


def test_failing_deferred_guard_raises_stop_iteration():
    """StopIteration is the existing condition-failed convention, so every consumer
    already treats it as 'try the next candidate'."""
    SpyConstraint.calls = []
    rep = build_replacer([_rule('fail_b')], defer_constraint=lambda c: True)
    [(replacement, subst)] = list(rep.matcher.match(to_omnimatch_expression(x**3)))
    with pytest.raises(StopIteration):
        replacement(**subst)
    assert SpyConstraint.calls == ['fail_b']


def test_predicate_selects_which_guards_defer():
    """Cheap guards stay on the Pattern; only predicate-selected ones defer."""
    SpyConstraint.calls = []
    rule = SymPyReplacementPattern(
        pattern=x**m_,
        constraints=(SpyConstraint(Symbol('pass_cheap')),
                     SpyConstraint(Symbol('pass_costly'))),
        replacement=Symbol('r'),
        module_name='spy', rule_number=2,
    )
    rep = build_replacer([rule],
                         defer_constraint=lambda c: 'costly' in str(c))
    list(rep.matcher.match(to_omnimatch_expression(x**3)))
    assert SpyConstraint.calls == ['pass_cheap'], \
        'only the non-deferred guard runs during enumeration'


class TestAdditionOrderIsStored:
    """`build_replacer` records each rule's addition index on the yielded callback.

    A many-to-one matcher enumerates matches in an internal order; a consumer wanting
    first-come-first-tried semantics (definition order IS priority, as in Mathematica's
    DownValues) sorts candidates by `_rule_index` -- one attribute read, with the
    caller controlling priority purely through the order it supplies the rules.
    """

    def _rules(self):
        return [
            SymPyReplacementPattern(pattern=x**m_, constraints=(),
                                    replacement=Symbol(f'r{i}'),
                                    module_name='ord', rule_number=i)
            for i in range(3)
        ]

    def test_indices_follow_addition_order(self):
        rep = build_replacer(self._rules())
        matches = list(rep.matcher.match(to_omnimatch_expression(x**3)))
        indices = sorted(fn._rule_index for fn, _ in matches)
        assert indices == [0, 1, 2]

    def test_sorting_by_index_recovers_supply_order(self):
        rep = build_replacer(self._rules())
        matches = sorted(rep.matcher.match(to_omnimatch_expression(x**3)),
                         key=lambda rs: rs[0]._rule_index)
        results = [fn(**subst)[0] for fn, subst in matches]
        assert [str(r) for r in results] == ['r0', 'r1', 'r2']

    def test_index_survives_the_deferred_guard_wrapper(self):
        SpyConstraint.calls = []
        rules = [SymPyReplacementPattern(
            pattern=x**m_, constraints=(SpyConstraint(Symbol('pass_z')),),
            replacement=Symbol('rz'), module_name='ord', rule_number=9)]
        rep = build_replacer(rules, defer_constraint=lambda c: True)
        [(fn, _)] = list(rep.matcher.match(to_omnimatch_expression(x**2)))
        assert fn._rule_index == 0
