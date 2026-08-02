# -*- coding: utf-8 -*-
"""Reusable SymPy -> matchpy pattern-matching-rule machinery.

Everything needed to turn a set of rules -- each a SymPy *pattern*, a SymPy
*replacement*, and SymPy *constraints*, all written with ordinary SymPy objects
mixed with :class:`~sympy_matching.wild.WildSymbol` -- into a matchpy
:class:`~matchpy.matching.many_to_one.ManyToOneReplacer`. Depends ONLY on
``matchpy`` and ``sympy_matching`` (NOT on ``sympy_wolfram`` or ``rubi_rules``),
so any matcher (integration, equation/ODE solving, term rewriting, ...) can reuse it.

- :class:`SymPyReplacementPattern` -- one (pattern, constraints, replacement) rule.
- :func:`build_replacer` (alias ``build_tracing_replacer``) -- assemble a
  ManyToOneReplacer from rules; each
  replacement returns ``(result, (rule.module_name, rule.rule_number))`` so the
  firing rule can be traced.
- The private helpers lambdify the SymPy replacement into a matchpy replacement
  callback and translate SymPy/logic constraints into matchpy ``CustomConstraint``s.

History: lifted out of ``rubi_rules.base_objects`` (was Rubi-specific by location
only), where it was called ``RubiRulePattern``/``SympyMatchingRule``.
``rubi_rules.base_objects`` re-exports these names so Rubi imports stay unchanged.
"""
import functools
from typing import Any, List, Tuple

import sympy
from pydantic import BaseModel

from matchpy.expressions.expressions import Pattern, to_matchpy_expression
from matchpy.expressions.constraints import CustomConstraint
from matchpy.matching.many_to_one import ManyToOneReplacer
from matchpy.functions import ReplacementRule

from sympy_matching.conversion import matchpy_to_sympy
from sympy_matching.wild import WildSymbol
from sympy_matching.constraint import SymPyMatchingConstraint, _resolve_with_substitution


class SymPyReplacementPattern(BaseModel):
    """A single pattern-matching rule in SymPy form.

    - ``pattern``: a SymPy expression (with WildSymbols) to match.
    - ``constraints``: a tuple of SymPy guards (``SymPyMatchingConstraint`` subclasses
      and/or bare SymPy Booleans like ``Ne(...)``, composed with Not/And/Or).
    - ``replacement``: a SymPy expression (with the same WildSymbols) produced on match.
    - ``module_name`` / ``rule_number``: an optional label for tracing/reporting.
    """
    model_config = dict(arbitrary_types_allowed=True)

    pattern: Any
    constraints: Tuple[Any, ...] = ()
    replacement: Any
    module_name: str = ''
    rule_number: int = 0


def _collect_wild_symbols(expr) -> dict:
    wilds = {}
    if isinstance(expr, WildSymbol):
        wilds[expr.wildcard_name] = expr
    elif hasattr(expr, 'args'):
        for arg in expr.args:
            wilds.update(_collect_wild_symbols(arg))
    return wilds


def _make_replacement_fn(replacement_expr, rule):
    # No scoping pass is needed here: With/Module/Block bind their locals to Dummy
    # symbols at construction, so substituting a wildcard value below can never be
    # captured by a local that happens to share its name.
    def _replacement(**match_dict):
        sympy_subs = {}
        for name, matchpy_val in match_dict.items():
            sympy_subs[name] = matchpy_to_sympy(matchpy_val)
        result = replacement_expr
        for ws in _collect_wild_symbols(replacement_expr).values():
            if ws.wildcard_name in sympy_subs:
                result = result.subs(ws, sympy_subs[ws.wildcard_name])
        # Evaluate any deferred helper nodes (With, Condition, ...).
        # A Condition whose test fails raises StopIteration, which propagates here and
        # is caught by ManyToOneReplacer.replace() as "no match" -- the rule is silently
        # skipped, matching Mathematica's Condition semantics.
        if hasattr(result, 'doit'):
            result = result.doit()
        return to_matchpy_expression(result)

    _replacement.__qualname__ = f"{rule.module_name}:[{rule.rule_number}]"
    _replacement.__module__ = ""
    return _replacement


def _extract_wild_names(constraint_obj):
    """Extract the wildcard names a constraint depends on.

    A constraint reaches us as an arbitrary expression tree: a
    SymPyMatchingConstraint (which publishes its wilds via ``.variables`` --
    ``free_symbols`` is empty on those), a Boolean wrapper (Not/Or/And), a bare
    SymPy relational over WildSymbols, or a deferred ``MathematicaExpr`` such as
    ``If(RationalQ(n_), GtQ(n_, 1), SumSimplerQ(n_, -2))`` that WRAPS inner
    constraints.

    The walk must therefore be GENERIC over ``.args``. An earlier version knew
    only about Not/Or/And and ``.variables``, so it walked straight past the
    ``If`` wrapper above and reported that the guard used no wildcards at all --
    whereupon :func:`_make_matchpy_constraint` dropped it and the rule ran
    unguarded. Seven Rubi rules were affected.
    """
    names: set = set()
    stack = [constraint_obj]
    visited: set = set()
    while stack:
        node = stack.pop()
        marker = id(node)
        if marker in visited:
            continue
        visited.add(marker)

        if isinstance(node, WildSymbol):
            names.add(node.wildcard_name)
            continue

        # Every attribute below is read defensively with an explicit type check: a
        # constraint's args legitimately contain CLASSES, not just instances -- e.g.
        # MemberQ([HeadRef(sympy.Si), ...], F_) carries function heads. On a class,
        # `.args`/`.free_symbols` resolve to the unbound property object, which is
        # truthy and not iterable.
        declared = getattr(node, 'variables', None)
        if isinstance(declared, (list, tuple, set, frozenset)):
            names.update(v for v in declared if isinstance(v, str) and v.isidentifier())

        free_syms = getattr(node, 'free_symbols', None)
        if isinstance(free_syms, (set, frozenset, list, tuple)):
            for s in free_syms:
                if isinstance(s, WildSymbol):
                    names.add(s.wildcard_name)
                elif isinstance(getattr(s, 'name', None), str) and s.name.endswith('_'):
                    names.add(s.name)

        args = getattr(node, 'args', ())
        if isinstance(args, (list, tuple)):
            stack.extend(args)
    return sorted(names)


# Mathematica's MatchQ inspects the UNEVALUATED expression. By the time an expression
# reaches us SymPy has normalised it -- (2*x)**3 is already 8*x**3 and no longer matches
# `(c*x)^m` -- so structural matching here is NOT faithful to Rubi in either direction:
# it misses matches Rubi would make, and (because the emitted code no longer distinguishes
# an outer-bound name from a MatchQ-local one) it can also match more loosely than Rubi.
#
# Enforcing it therefore REFUSES rules Rubi would offer (measured on a 120-integrand
# sample: 81/120 solved as a permissive stub, 69/120 fully enforced). Both polarities lose
# antiderivatives, so enforcement is OFF by default: a guard that wrongly refuses a rule is
# worse than one that is merely permissive.
#
# The concrete MatchQ constraint's check() is fully implemented and unit-tested; only its
# USE as a rule guard is gated here (matched by class name so this stays Wolfram-agnostic).
ENFORCE_MATCHQ = False


def _mentions_matchq(constraint_obj) -> bool:
    """True if this constraint is (or wraps) a MatchQ. See :data:`ENFORCE_MATCHQ`."""
    if type(constraint_obj).__name__ == 'MatchQ':
        return True
    return any(_mentions_matchq(a) for a in getattr(constraint_obj, 'args', ()))


def _make_constraint_checker(constraint_obj, variables):
    """Build a checker function for a single constraint (possibly compound).

    Returns a callable(**kwargs) -> bool.
    """
    # MatchQ is not faithful enough to be used as a guard (see ENFORCE_MATCHQ).
    # This MUST come before the Not/Or/And handling below: applied to a MatchQ nested
    # inside a Not, the negation would turn the permissive True into False and REFUSE
    # the rule -- the exact harm the gate exists to avoid.
    if not ENFORCE_MATCHQ and _mentions_matchq(constraint_obj):
        return lambda **kwargs: True

    # Not(inner): negate inner check
    if isinstance(constraint_obj, sympy.logic.boolalg.Not):
        inner = constraint_obj.args[0]
        inner_checker = _make_constraint_checker(inner, variables)

        def check_not(**kwargs):
            return not inner_checker(**kwargs)
        return check_not

    # Or(a, b, ...): any inner check passes
    if isinstance(constraint_obj, sympy.logic.boolalg.Or):
        inner_checkers = [_make_constraint_checker(arg, variables) for arg in constraint_obj.args]

        def check_or(**kwargs):
            return any(c(**kwargs) for c in inner_checkers)
        return check_or

    # And(a, b, ...): all inner checks pass
    if isinstance(constraint_obj, sympy.logic.boolalg.And):
        inner_checkers = [_make_constraint_checker(arg, variables) for arg in constraint_obj.args]

        def check_and(**kwargs):
            return all(c(**kwargs) for c in inner_checkers)
        return check_and

    # SymPyMatchingConstraint (incl. Wolfram's MathematicaConstraint): use .check().
    if isinstance(constraint_obj, SymPyMatchingConstraint):
        def check_constraint(**kwargs):
            try:
                return constraint_obj.check(**kwargs)
            except TypeError as exc:
                # A guard whose operand is a Boolean cannot be evaluated arithmetically:
                # SymPy raises "BooleanAtom not allowed in this context" from the first
                # `-` or comparison. This happens all over Rubi because its helpers
                # signal "no result" by returning False, and a rule then feeds that
                # value straight into the next guard (ZeroQ[u.base - v], EqQ[lst[[3]],2],
                # ...). Mathematica keeps such an expression symbolic, so the guard
                # simply does not hold -- which is what we return. Only this one
                # message is swallowed; any other TypeError is a real bug and propagates.
                if 'BooleanAtom not allowed' not in str(exc):
                    raise
                return False
        return check_constraint

    # Generic SymPy Boolean guard (a bare relational like Ne(GCD(m+1,n),1), NOT a
    # SymPyMatchingConstraint). Resolve its wildcards the SAME way -- through
    # _resolve_with_substitution, keyed by wildcard_name.
    #
    # Why the dedicated path: the guard's variables are WildSymbols, which cross the
    # sympy<->matchpy boundary as Wildcards; a plain Symbol crosses as a SymbolWrapper
    # CONSTANT. So the matcher hands back values by wildcard NAME (as SymbolWrappers,
    # e.g. 'm' -> SymbolWrapper(1)), never as an object equal to a Symbol('m') or even a
    # freshly built WildSymbol('m') (a WildSymbol is instance-unique). The only sound move
    # is to xreplace the guard's OWN wildcard instances, matched by name, with the match
    # values converted back to SymPy -- exactly what _resolve_with_substitution does.
    def check_boolean_guard(**kwargs):
        substitution = {name: matchpy_to_sympy(kwargs[name])
                        for name in variables if name in kwargs}
        result = _resolve_with_substitution(constraint_obj, substitution)
        # A bare relational leaves any deferred node (GCD, Denominator, ...) unevaluated
        # -- Ne(GCD(2,6),1) stays symbolic -- so reduce it before the truth test.
        if hasattr(result, 'doit'):
            try:
                result = result.doit()
            except Exception:
                pass
        return result == True   # noqa: E712 -- sympy truth, `is True` would be wrong
    return check_boolean_guard


def _make_matchpy_constraint(constraint_obj, pattern_wilds):
    """Convert a SymPy-level constraint into a MatchPy ``CustomConstraint``.

    ``pattern_wilds`` is the mapping of wildcard names the PATTERN binds (from
    :func:`_collect_wild_symbols`); only those may be declared to MatchPy.
    Handles SymPyMatchingConstraint, Not/Or/And wrappers, and generic SymPy Booleans.
    """
    # A constraint may mention variables the PATTERN does not bind (MatchQ scopes its
    # inner pattern's variables to itself). MatchPy can only supply what it matched, and
    # CustomConstraint.__call__ silently returns True when a declared variable is missing
    # -- so declaring them made the whole guard a no-op. Declare only what the pattern
    # binds; the rest stay free variables inside the constraint.
    declared = _extract_wild_names(constraint_obj)
    variables = [v for v in declared if v in pattern_wilds]
    if not variables:
        if declared:
            # Mentions wildcards, just none the pattern binds -> its value still depends
            # on something we cannot supply, so stay permissive (see the note above).
            return CustomConstraint(lambda: True)
        # A guard over NO wildcard at all cannot depend on the match, so its value is
        # fixed for the whole run -- EVALUATE it once here rather than assume it passes.
        # Assuming True let a constant-FALSE guard run its rule unconditionally, which
        # is how Rubi's `MemberQ[{SinIntegral,CosIntegral}, x]` typo (rules 8.4#27 and
        # 8.5#27, where `x` should read `F`) turned from harmless upstream dead code
        # into a catch-all: the pattern's head wildcard matches EVERY head, so the rules
        # fired for arbitrary F and returned a wrong antiderivative. The same held for
        # `TrueQ[$UseGamma]` (2.3#2/#5), which Rubi defines as False.
        # An indeterminate result (None, or a guard that raises because it wants match
        # context after all) keeps the permissive default -- only a definite False blocks.
        try:
            value = _make_constraint_checker(constraint_obj, [])()
        except Exception:
            return CustomConstraint(lambda: True)
        if value is False or value is sympy.S.false:
            return CustomConstraint(lambda: False)
        return CustomConstraint(lambda: True)

    checker = _make_constraint_checker(constraint_obj, variables)

    # Build a lambda with proper parameter names for MatchPy introspection. The
    # SOURCE only depends on the variable-name tuple, so the compile step is cached
    # (parsing 29k+ tiny lambdas was ~1s of Rubi matcher construction); only the
    # cheap eval-of-code-object binding the concrete checker runs per rule.
    fn = eval(_trampoline_code(tuple(variables)), {'__checker__': checker})

    return CustomConstraint(fn)


@functools.lru_cache(maxsize=None)
def _trampoline_code(variables):
    params = ', '.join(variables)
    src = f"lambda {params}: __checker__({', '.join(f'{v}={v}' for v in variables)})"
    return compile(src, '<constraint-trampoline>', 'eval')


def _make_tracing_replacement_fn(replacement_expr, rule):
    base_replacement = _make_replacement_fn(replacement_expr, rule)

    def _replacement(**match_dict):
        result = base_replacement(**match_dict)
        return result, (rule.module_name, rule.rule_number)

    _replacement.__qualname__ = base_replacement.__qualname__
    _replacement.__module__ = base_replacement.__module__
    # Expose the SymPy replacement expression explicitly so serialization does not have
    # to guess at closure cell order. Attribute name kept as `_rubi_replacement_expr`
    # because matchpy's json_serialization reads exactly that name.
    _replacement._rubi_replacement_expr = replacement_expr
    return _replacement


def _wrap_with_deferred_guards(replacement_fn, deferred_checkers):
    """Run the deferred guards at attempt time; a failure IS a failed condition.

    Raising StopIteration is the existing convention for "this rule's Condition
    failed" -- every consumer already catches it and moves to the next candidate, so
    deferring guards here changes WHEN they run, never the accept/reject outcome.
    """
    def _guarded(**match_dict):
        for checker in deferred_checkers:
            if not checker(**match_dict):
                raise StopIteration
        return replacement_fn(**match_dict)
    for attr in ('__qualname__', '__module__', '_rubi_replacement_expr'):
        try:
            setattr(_guarded, attr, getattr(replacement_fn, attr))
        except AttributeError:
            pass
    return _guarded


def build_replacer(rules: List[SymPyReplacementPattern], defer_constraint=None) -> ManyToOneReplacer:
    """Assemble a matchpy ManyToOneReplacer from SymPyReplacementPattern objects.

    Each rule's SymPy pattern/constraints/replacement are converted to matchpy form;
    the replacement callback returns ``(result, (module_name, rule_number))`` so the
    firing rule can always be traced. (Historic alias: ``build_tracing_replacer``.)

    ``defer_constraint`` is an optional predicate over a rule constraint. A constraint
    for which it returns True is NOT attached to the matchpy Pattern; it is deferred
    into the replacement callback and evaluated at ATTEMPT time, raising StopIteration
    on failure (the ordinary "condition failed" signal).

    Why a caller might want this: consumers that sort the matcher's yields by rule
    priority EXHAUST the match generator, and matchpy evaluates Pattern-attached
    constraints for EVERY candidate during enumeration. A guard whose evaluation is
    itself expensive (in a rewrite system: one that recursively invokes the system)
    then runs once per candidate before the first rule is ever attempted. Deferring
    such guards restores first-match-wins economics: they run in attempt order, only
    until the first winner. Which guards are "expensive" is DOMAIN knowledge -- this
    layer is agnostic; the caller supplies the predicate (for the Rubi rule set, see
    ``rubi_rules.base_objects``).

    Guards kept on the Pattern still prune commutative enumeration, which is what
    keeps matching a many-thousand-rule net tractable -- so a predicate should defer
    only what is genuinely expensive.
    """
    replacer = ManyToOneReplacer()
    for index, rule in enumerate(rules):
        matchpy_pattern_expr = to_matchpy_expression(rule.pattern)
        pattern_wilds = _collect_wild_symbols(rule.pattern)
        cheap, expensive = [], []
        for constraint in rule.constraints:
            target = expensive if (defer_constraint is not None
                                   and defer_constraint(constraint)) else cheap
            target.append(constraint)
        matchpy_constraints = [
            _make_matchpy_constraint(constraint, pattern_wilds)
            for constraint in cheap
        ]
        pattern = Pattern(matchpy_pattern_expr, *matchpy_constraints)
        replacement_fn = _make_tracing_replacement_fn(rule.replacement, rule)
        if expensive:
            variables = set(pattern_wilds)
            deferred_checkers = [
                _make_constraint_checker(constraint, variables)
                for constraint in expensive
            ]
            replacement_fn = _wrap_with_deferred_guards(replacement_fn, deferred_checkers)
        # The rule's ADDITION ORDER, exposed on the callback the matcher yields.
        # A many-to-one matcher enumerates matches in an internal order; a consumer
        # that wants first-come-first-tried semantics (a rule set where definition
        # order IS priority, as in Mathematica's DownValues) can sort candidates by
        # this index -- an attribute read, with no name parsing at match time. The
        # caller controls priority entirely by the order it supplies the rules.
        replacement_fn._rule_index = index
        replacer.add(ReplacementRule(pattern, replacement_fn))
    return replacer


# Historic name (every existing caller uses it); the replacer has always traced.
build_tracing_replacer = build_replacer
