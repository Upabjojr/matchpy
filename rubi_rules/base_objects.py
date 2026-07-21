# -*- coding: utf-8 -*-
"""Core objects for Rubi integration rules."""
import os
from pathlib import Path
import sympy
from sympy.core.parameters import _exp_is_pow
from typing import Any, List, Tuple
from pydantic import BaseModel

from matchpy.expressions.expressions import (
    Operation, SymbolWrapper, Wildcard, Pattern, OperationHead, Arity,
    to_expression,
)
from matchpy.expressions.constraints import CustomConstraint
from matchpy.matching.many_to_one import ManyToOneReplacer
from matchpy.functions import ReplacementRule

from sympy_matching.conversion import register_sympy_head, matchpy_to_sympy
from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

from sympy_matching.constraints import RubiConstraint
from sympy_wolfram.mathematica_expressions import rename_scoped_locals


class Int(sympy.Function):
    """Symbolic integration function for Rubi pattern matching."""
    nargs = 2


INT = OperationHead(name='Int', arity=Arity.binary)
register_sympy_head(Int, INT)


class RubiRulePattern(BaseModel):
    """A single Rubi integration rule in SymPy form."""
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


def _make_replacement_fn(replacement_expr, wild_names, rule):
    replacement_expr = rename_scoped_locals(replacement_expr)

    def _replacement(**match_dict):
        sympy_subs = {}
        for name, matchpy_val in match_dict.items():
            sympy_subs[name] = matchpy_to_sympy(matchpy_val)
        result = replacement_expr
        for ws in _collect_wild_symbols(replacement_expr).values():
            if ws.wildcard_name in sympy_subs:
                result = result.subs(ws, sympy_subs[ws.wildcard_name])
        # Evaluate MathematicaExpr-based helper nodes (With, Condition,
        # SimplifyIntegrand, …).
        # A Condition whose test fails raises StopIteration, which propagates
        # here and is caught by ManyToOneReplacer.replace() as "no match" —
        # the rule is silently skipped, matching Mathematica's Condition semantics.
        if hasattr(result, 'doit'):
            result = result.doit()
        return to_expression(result)

    _replacement.__qualname__ = f"{rule.module_name}:[{rule.rule_number}]"
    _replacement.__module__ = ""
    return _replacement


def _extract_wild_names(constraint_obj):
    """Extract WildSymbol/Symbol names from a constraint.

    Handles RubiConstraint (via .variables), and Boolean wrappers
    Not(...), Or(...), And(...) by recursing into their args.
    """
    # Handle Not/Or/And wrappers by recursing into args
    if isinstance(constraint_obj, sympy.logic.boolalg.Not):
        inner = constraint_obj.args[0]
        return _extract_wild_names(inner)
    if isinstance(constraint_obj, (sympy.logic.boolalg.Or, sympy.logic.boolalg.And)):
        names = set()
        for arg in constraint_obj.args:
            names.update(_extract_wild_names(arg))
        return sorted(names)

    try:
        free_syms = constraint_obj.free_symbols
        names = []
        for s in free_syms:
            if isinstance(s, WildSymbol):
                names.append(s.wildcard_name)
            elif hasattr(s, 'name') and s.name.endswith('_'):
                names.append(s.name)
        if names:
            return sorted(set(names))
    except (AttributeError, TypeError):
        pass
    if hasattr(constraint_obj, 'variables'):
        return [v for v in constraint_obj.variables if v.isidentifier()]
    return []


def _make_constraint_checker(constraint_obj, variables):
    """Build a checker function for a single constraint (possibly compound).

    Returns a callable(**kwargs) -> bool.
    """
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

    # RubiConstraint: use .check() directly
    if isinstance(constraint_obj, RubiConstraint):
        def check_rubi(**kwargs):
            return constraint_obj.check(**kwargs)
        return check_rubi

    # Generic SymPy Boolean: use .subs() approach
    def check_subs(**kwargs):
        subs_dict = {}
        for name in variables:
            if name in kwargs:
                val = kwargs[name]
                val = matchpy_to_sympy(val)
                # Try to find WildSymbol in constraint's free_symbols
                subs_dict[sympy.Symbol(name)] = val
        result = constraint_obj.subs(subs_dict)
        return result == True
    return check_subs


def _make_matchpy_constraint(constraint_obj, wild_names, pattern_wilds):
    """Convert a constraint into a MatchPy CustomConstraint.

    Handles RubiConstraint, Not/Or/And wrappers, and generic SymPy Booleans.
    """
    variables = _extract_wild_names(constraint_obj)
    if not variables:
        return CustomConstraint(lambda: True)

    checker = _make_constraint_checker(constraint_obj, variables)

    # Build lambda with proper parameter names for MatchPy introspection
    params = ', '.join(variables)
    fn_code = f"lambda {params}: __checker__({', '.join(f'{v}={v}' for v in variables)})"
    fn = eval(fn_code, {'__checker__': checker})

    return CustomConstraint(fn)


def _make_tracing_replacement_fn(replacement_expr, wild_names, rule):
    base_replacement = _make_replacement_fn(replacement_expr, wild_names, rule)

    def _replacement(**match_dict):
        result = base_replacement(**match_dict)
        return result, (rule.module_name, rule.rule_number)

    _replacement.__qualname__ = base_replacement.__qualname__
    _replacement.__module__ = base_replacement.__module__
    # Expose the SymPy replacement expression explicitly so serialization does not
    # have to guess at closure cell order (the tracing wrapper's closure[0] is the
    # inner function, not the replacement expression).
    _replacement._rubi_replacement_expr = replacement_expr
    return _replacement


def build_tracing_replacer(
    rules: List[RubiRulePattern],
) -> ManyToOneReplacer:
    replacer = ManyToOneReplacer()
    for i, rule in enumerate(rules):
        matchpy_pattern_expr = to_expression(rule.pattern)
        wilds = _collect_wild_symbols(rule.pattern)
        wild_names = list(wilds.keys())
        matchpy_constraints = []
        for constraint in rule.constraints:
            mc = _make_matchpy_constraint(constraint, wild_names, wilds)
            matchpy_constraints.append(mc)
        pattern = Pattern(matchpy_pattern_expr, *matchpy_constraints)
        replacement_fn = _make_tracing_replacement_fn(
            rule.replacement,
            wild_names,
            rule,
        )
        replacer.add(ReplacementRule(pattern, replacement_fn))
    return replacer


class _RubiIntegrator:
    """Caller-owned Rubi integrator with explicit caches and tracing support."""

    def __init__(self, rules_dir: str | os.PathLike | None = None):
        self.rules_dir = Path(rules_dir) if rules_dir is not None else Path(os.path.dirname(__file__)) / 'rules'
        self._replacer_cache: dict[str, ManyToOneReplacer] = {}

    def _normalize_rule_glob(self, pattern: str) -> str:
        normalized = pattern.replace('\\', '/')
        if normalized.endswith('.py'):
            return normalized
        if normalized.endswith('**'):
            return normalized + '/*.py'
        if normalized.endswith('*'):
            return normalized if normalized.endswith('*.py') else normalized + '.py'

        direct_file = normalized.rstrip('/') + '.py'
        if (self.rules_dir / direct_file).exists():
            return direct_file
        return normalized.rstrip('/') + '/**/*.py'

    def load_rule_patterns(self, pattern: str = '**') -> tuple[RubiRulePattern, ...]:
        import importlib.util

        glob_pattern = self._normalize_rule_glob(pattern)

        all_rules = []
        for py_file in sorted(self.rules_dir.glob(glob_pattern)):
            if py_file.name.startswith('_'):
                continue
            module_name = (
                f"rubi_rules.rules."
                f"{py_file.relative_to(self.rules_dir).with_suffix('').as_posix().replace('/', '.')}"
            )
            try:
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'RULES'):
                    all_rules.extend(mod.RULES)
            except Exception as e:
                import warnings, traceback
                warnings.warn(
                    f"Failed to load rules from {py_file.name}: {e}\n"
                    + traceback.format_exc()
                )

        rules = tuple(all_rules)
        return rules

    def reset_cache(self):
        self._replacer_cache.clear()

    def integrate(
        self,
        expr: sympy.Expr,
        x: sympy.Symbol,
        pattern: str = '**',
        trace: list | None = None,
    ) -> tuple[sympy.Expr, list[tuple[sympy.Expr, list[tuple[str, int]]]]]:
        # Depth-first reduction with path-aware cycle detection. Some Rubi rule
        # pairs are mutually inverse (e.g. complete-the-square [42] vs ExpandToSum
        # [43]), so without rule ordering the matcher can bounce an integrand
        # between two forms forever. The DFS records the integrand forms on the
        # current reduction path; a rule whose result re-enters a path form is a
        # cycle and is skipped in favour of the next matching rule (see
        # `_dfs_match_int`). Match order stays irrelevant: a fully-integrated
        # result is always preferred over a `CannotIntegrate`/residual-`Int`
        # terminal, whichever rule happens to be yielded first.
        replacer = self._load_replacer(pattern)
        applied: list = []
        budget = [50000]  # backstop against a rule set that never converges
        result, _ = _dfs_reduce_int(
            sympy.sympify(expr), sympy.sympify(x), frozenset(), replacer, applied, budget, trace
        )
        matched_rules = [(result, applied)] if applied else []
        return result, matched_rules

    def _integration_step(
            self,
            expr: sympy.Expr,
            x: sympy.Symbol,
            pattern: str = '**',
            seen: set | None = None,
        ) -> tuple[sympy.Expr, list[tuple[str, int]]]:
        expr = sympy.sympify(expr)
        x = sympy.sympify(x)
        x_canonical = sympy.Symbol('x')

        matched_rules = []
        replacer = self._load_replacer(pattern)

        if x == x_canonical:
            result, matched_rule = _preprocess_integrate(expr, x_canonical, replacer, seen)
        else:
            dummy = sympy.Dummy('_x_var')
            x_sub = x.subs(x_canonical, dummy)  # x could be function containing x_canonical
            expr_sub = expr.subs(x_canonical, dummy).subs(x_sub, x_canonical)
            result, matched_rule = _preprocess_integrate(expr_sub, x_canonical, replacer, seen)
            result = result.subs(x_canonical, x).subs(dummy, x_canonical)

        matched_rules.append(matched_rule)
        return result, matched_rules

    def _load_replacer(self, pattern: str) -> ManyToOneReplacer:
        pattern = self._normalize_rule_glob(pattern)
        if pattern not in self._replacer_cache:
            rules = list(self.load_rule_patterns(pattern))
            replacer = build_tracing_replacer(rules)
            self._replacer_cache[pattern] = replacer
        return self._replacer_cache[pattern]


_rubi_integrator = _RubiIntegrator()


def load_rule_patterns(
    pattern: str = '**',
    integrator: _RubiIntegrator | None = None,
) -> tuple[RubiRulePattern, ...]:
    integrator = integrator or _RubiIntegrator()
    return integrator.load_rule_patterns(pattern)


def _has_cannot_integrate(expr) -> bool:
    """True if `expr` carries a `CannotIntegrate` marker.

    Matched by head *name* for the same reason as in `_dfs_is_clean`: round-tripping
    a replacement through MatchPy can turn the `rubi_utils.CannotIntegrate` node into
    a plain undefined `Function('CannotIntegrate')`, which an isinstance check misses.
    """
    return any(type(a).__name__ == 'CannotIntegrate' for a in expr.atoms(sympy.Function))


def _matchpy_integrate(expr: sympy.Expr, x: sympy.Symbol, replacer: ManyToOneReplacer, seen: set | None = None):
    mp_expr = to_expression(Int(expr, x))
    if seen is not None:
        seen.add(Int(expr, x))
    # Try the matching rules in the order the matcher yields them and apply the
    # first one that makes progress. A rule whose result only reproduces
    # integrands we have already visited (`seen`) is a cycle — skip it and try the
    # next matching rule. A rule whose Condition fails raises StopIteration; skip
    # it too. If nothing applies, return the integral unchanged.
    for replacement, subst in replacer.matcher.match(mp_expr):
        try:
            result_mp, matched_rule = replacement(**subst)
        except StopIteration:
            continue
        result = matchpy_to_sympy(result_mp)
        if seen is not None:
            produced = [f for f in result.atoms(Int)]
            if produced and all(f in seen for f in produced):
                continue  # cycle: only revisits already-integrated forms
        return result, matched_rule
    return matchpy_to_sympy(mp_expr), []


def _preprocess_integrate(expr: sympy.Expr, x: sympy.Symbol, replacer: ManyToOneReplacer, seen: set | None = None):
    expr = sympy.sympify(expr)
    if x not in expr.free_symbols:
        return expr * x, []
    if expr.is_Add:
        # A few Rubi rules have a SUM as their pattern -- the product rule
        # (Int[f'g + f g'] -> f g), the quotient rule, and friends. Splitting the
        # sum here unconditionally, as we used to, made those rules unreachable:
        # by the time the matcher ran, the sum was already two separate integrals.
        # So offer the whole sum to the matcher first and only fall back to
        # splitting if that does not actually get us anywhere.
        whole, whole_rules = _matchpy_integrate(expr, x, replacer, seen)
        if whole_rules and not _has_cannot_integrate(whole):
            return whole, whole_rules
        addends, matched_rules = zip(*[_preprocess_integrate(t, x, replacer, seen) for t in expr.args])
        return sympy.Add(*addends), matched_rules
    if expr.is_Mul:
        free_factors = [f for f in expr.args if x not in f.free_symbols]
        x_factors = [f for f in expr.args if x in f.free_symbols]
        if free_factors:
            const = sympy.Mul(*free_factors)
            core = x_factors[0] if len(x_factors) == 1 else sympy.Mul(*x_factors)
            integ, matched_rule = _preprocess_integrate(core, x, replacer, seen)
            return const * integ, matched_rule
    return _matchpy_integrate(expr, x, replacer, seen)


# ── DFS integrator with path-aware cycle detection ───────────────────────────

def _dfs_is_clean(expr) -> bool:
    """True if `expr` is a finished antiderivative: no unresolved `Int`, no
    `CannotIntegrate` marker, and no degenerate `zoo`/`nan` value.

    `CannotIntegrate` is matched by head *name*: round-tripping a rule's
    replacement through MatchPy can turn the `rubi_utils.CannotIntegrate` node into
    a plain undefined `Function('CannotIntegrate')`, so an isinstance/atoms check
    against the imported class misses it.

    A result containing `zoo` (ComplexInfinity) or `nan` is a degenerate
    evaluation (a coefficient divided by zero, etc.), never a valid closed form.
    Rejecting it here keeps such a result from being preferred over the correct
    finite one when several rules match and the matcher's (hash-ordered) yield
    order happens to surface the degenerate rule first -- otherwise the returned
    antiderivative varies run-to-run.
    """
    if expr.atoms(Int):
        return False
    if expr.has(sympy.zoo, sympy.nan):
        return False
    return not any(type(a).__name__ == 'CannotIntegrate' for a in expr.atoms(sympy.Function))


def _rule_id(replacement):
    """(module_name, rule_number) id parsed from a tracing replacement fn's qualname."""
    qn = getattr(replacement, '__qualname__', '')
    if ':[' in qn and qn.endswith(']'):
        mod, num = qn.rsplit(':[', 1)
        try:
            return (mod, int(num[:-1]))
        except ValueError:
            pass
    return (qn or repr(replacement), None)


def _dfs_reduce_result(result, x, path, replacer, applied, budget, trace=None):
    """Recursively reduce every `Int` atom in `result`.

    Returns (reduced_expr, blocked); blocked is True if some `Int` could only be
    reduced by re-entering a form already on the current DFS `path` (a cycle).
    """
    blocked_any = False
    for intfun in list(result.atoms(Int)):
        reduced, blocked = _dfs_reduce_int(
            intfun.args[0], intfun.args[1], path, replacer, applied, budget, trace
        )
        result = result.replace(intfun, reduced)
        blocked_any = blocked_any or blocked
    result = _collapse_resolved_substs(result)
    return result, blocked_any


def _collapse_resolved_substs(result):
    """Perform ``Subst[G, x, v] -> G.subs(x, v)`` once the inner integral is gone.

    ``rubi_utils.Subst`` stays deferred while it wraps an unevaluated ``Int`` (so
    the substitution cannot capture the integral's bound variable); after the
    round-trip through MatchPy it is a plain ``Function('Subst')`` node. Once the
    enclosing reduction has turned that inner ``Int`` into an antiderivative
    ``G(x)``, apply the postponed substitution here — never before, or ``v`` (often
    containing ``x``, e.g. ``log(x)``) would capture the bound variable.
    """
    def _resolved(e):
        return (type(e).__name__ == 'Subst' and len(e.args) == 3
                and not any(type(a).__name__ == 'Int' for a in e.args[0].atoms(sympy.Function)))

    return result.replace(_resolved, lambda e: e.args[0].subs(e.args[1], e.args[2]))


def _try_whole_sum_rule(f, x, replacer, trace=None, depth=0):
    """Try to integrate the SUM `f` outright with a rule whose pattern is a sum.

    Returns ``(result, rule)`` or None. Only a rule that yields a FINISHED
    antiderivative in a single step is accepted -- no recursion is performed, so
    the cost is one matcher enumeration per Add node. That is deliberate: the
    rules this exists for (Rubi's product and quotient rules) integrate a sum in
    one step, while anything that merely rewrites the sum into further integrals
    is better served by the term-by-term splitting the caller falls back to.
    """
    for replacement, subst in replacer.matcher.match(to_expression(Int(f, x))):
        try:
            result_mp, rule = replacement(**subst)
        except StopIteration:
            continue  # Condition failed -> no match
        result = matchpy_to_sympy(result_mp)
        if _dfs_is_clean(result):
            if trace is not None:
                trace.append({'depth': depth, 'integrand': Int(f, x),
                              'rule': rule, 'status': 'accepted (whole sum)'})
            return result, rule
    return None


def _dfs_reduce_int(f, x, path, replacer, applied, budget, trace=None):
    """Reduce `Int(f, x)` via DFS. Returns (result_expr, blocked).

    `path` is the frozenset of integrand forms currently on the reduction stack.
    Handles a non-canonical integration variable and the Add/Mul/constant
    preprocessing (mirrors `_preprocess_integrate`), then defers to
    `_dfs_match_int` for the rule-matching core.
    """
    x_canonical = sympy.Symbol('x')
    f = sympy.sympify(f)
    # Rules are written with Symbol('x'); rewrite a non-canonical variable.
    if x != x_canonical:
        dummy = sympy.Dummy('_x_var')
        x_sub = x.subs(x_canonical, dummy)
        f_sub = f.subs(x_canonical, dummy).subs(x_sub, x_canonical)
        r, b = _dfs_reduce_int(f_sub, x_canonical, path, replacer, applied, budget, trace)
        return r.subs(x_canonical, x).subs(dummy, x_canonical), b

    if x not in f.free_symbols:
        return f * x, False
    if f.is_Add:
        # Some Rubi rules have a SUM as their pattern -- the product rule
        # (Int[f'g + f g'] -> f g), the quotient rule, and friends. Splitting the
        # sum unconditionally made those unreachable: by the time the matcher ran,
        # the sum was already several separate integrals. So give the whole sum a
        # chance first -- but only a cheap ONE-STEP one (see _try_whole_sum_rule);
        # routing it through the full `_dfs_match_int` recursion instead made the
        # test suite ~5x slower, since that explores the entire subtree for every
        # rule that matches the sum.
        hit = _try_whole_sum_rule(f, x, replacer, trace, len(path))
        if hit is not None:
            result, rule = hit
            applied.append(rule)
            return result, False
        parts, blocked = [], False
        for t in f.args:
            r, b = _dfs_reduce_int(t, x, path, replacer, applied, budget, trace)
            parts.append(r)
            blocked = blocked or b
        return sympy.Add(*parts), blocked
    if f.is_Mul:
        free_factors = [g for g in f.args if x not in g.free_symbols]
        x_factors = [g for g in f.args if x in g.free_symbols]
        if free_factors:
            core = x_factors[0] if len(x_factors) == 1 else sympy.Mul(*x_factors)
            r, b = _dfs_reduce_int(core, x, path, replacer, applied, budget, trace)
            return sympy.Mul(*free_factors) * r, b

    return _dfs_match_int(f, x, path, replacer, applied, budget, trace)


def _dfs_match_int(f, x, path, replacer, applied, budget, trace=None):
    """Try the matching rules for `Int(f, x)`, preferring a fully-integrated result.

    Rules are tried in whatever order the matcher yields them (order must not
    matter): a rule whose result re-enters a form on `path` is a cycle and is
    skipped; a rule yielding a clean antiderivative is taken immediately; a
    non-clean terminal (`CannotIntegrate`, or a residual `Int`) is kept only as a
    fallback so a later rule can still win with a clean result.

    If `trace` is a list, one record is appended per rule *tried*
    (`{'depth', 'integrand', 'rule', 'status'}`) so accepted AND rejected rules
    (with the reason) can be inspected — see `rubi_integrate(..., return_trace=True)`.
    """
    # Combine products of exponentials (E^a * E^b -> E^(a+b)) so a single
    # Pow(E, ...) can match the exponential rule patterns; SymPy never does this.
    f = sympy.powsimp(f, combine='exp')
    if f in path:
        return Int(f, x), True
    if budget[0] <= 0:
        return Int(f, x), False
    budget[0] -= 1
    new_path = path | {f}
    mp_expr = to_expression(Int(f, x))
    depth = len(path)

    def _record(rule, status):
        if trace is not None:
            trace.append({'depth': depth, 'integrand': Int(f, x), 'rule': rule, 'status': status})

    fallback = None
    matched_any = False
    for replacement, subst in replacer.matcher.match(mp_expr):
        try:
            result_mp, rule = replacement(**subst)
        except StopIteration:
            # This rule's Condition failed; try the next matching rule.
            _record(_rule_id(replacement), 'rejected (condition failed)')
            continue
        matched_any = True
        result = matchpy_to_sympy(result_mp)
        local: list = []
        reduced, blocked = _dfs_reduce_result(result, x, new_path, replacer, local, budget, trace)
        if blocked:
            _record(rule, 'rejected (cycle)')
            continue  # rule re-enters the current path -> cycle; try the next rule
        if _dfs_is_clean(reduced):
            _record(rule, 'accepted')
            applied.append(rule)
            applied.extend(local)
            return reduced, False
        # A terminal result that still has an Int/CannotIntegrate: keep the first
        # one as a fallback, but keep looking for a clean result. A degenerate
        # zoo/nan result is never a useful partial answer -- skip it entirely so a
        # pure-degenerate integrand is left unevaluated (honest "unsolved") rather
        # than returning a wrong zoo.
        _record(rule, 'candidate (non-clean)')
        if fallback is None and not reduced.has(sympy.zoo, sympy.nan):
            fallback = (reduced, rule, local)

    if fallback is not None:
        reduced, rule, local = fallback
        _record(rule, 'accepted (fallback)')
        applied.append(rule)
        applied.extend(local)
        return reduced, False
    # Every matching rule cycled -> propagate as blocked so the caller backtracks;
    # no rule matched at all -> leave the integral unevaluated (not a cycle).
    return Int(f, x), matched_any


def format_trace(trace) -> str:
    """Render a DFS trace (from ``rubi_integrate(..., return_trace=True)``) as text.

    One indented line per rule tried, showing its status (accepted / rejected /
    candidate) and the integrand it was tried on.
    """
    lines = []
    for e in trace:
        indent = '  ' * e['depth']
        rule = e['rule']
        rule_str = (f"{rule[0]}:[{rule[1]}]"
                    if isinstance(rule, tuple) and rule[1] is not None else str(rule))
        lines.append(f"{indent}{e['status']:26s} {rule_str:40s} Int({e['integrand'].args[0]})")
    return '\n'.join(lines)


def rubi_integrate(
    expr: sympy.Expr,
    x: sympy.Symbol,
    pattern: str = '**',
    return_matched_rules: bool = False,
    return_trace: bool = False,
):
    """Integrate expr with respect to x using the Rubi rule set.

    The rule files are written with Symbol('x') as the canonical integration
    variable.  When the caller passes a different variable (e.g. Symbol('y')),
    we perform a three-step substitution so the rules still apply:

        1. Replace the existing Symbol('x') in expr with a Dummy symbol to
           avoid a name collision when the user's variable is renamed to 'x'.
        2. Replace the user's integration variable with Symbol('x').
        3. Integrate with respect to Symbol('x').
        4. Undo the substitution: Symbol('x') → original variable,
           Dummy → Symbol('x').

    Parameters
    ----------
    pattern:
        Glob over ``rubi_rules/rules/**`` selecting which rule files to load
        (default ``'**'`` = the whole rule set). Scope it (e.g.
        ``'r_2_exponentials/**'``) for speed.
    return_matched_rules:
        If True, return ``(result, matched_rules)`` where ``matched_rules`` lists
        the rules ACCEPTED on the winning path.
    return_trace:
        If True, return ``(result, trace)`` where ``trace`` records every rule the
        DFS tried — accepted AND rejected, with the reason. Render it with
        ``format_trace(trace)``. See ``rubi_rules/README.md``.

    Examples
    --------
    >>> from sympy import symbols
    >>> x, y = symbols('x y')
    >>> rubi_integrate(x * y, x)   # x**2*y/2
    >>> rubi_integrate(x * y, y)   # x*y**2/2
    """
    # Rubi (like Mathematica) represents e^u as Power[E, u], so every exponential
    # rule pattern is a Power (F^(...)).  SymPy normally collapses E**u into the
    # distinct exp(u) function, whose head never matches those Power patterns.
    # Run the whole integration under SymPy's exp_is_pow flag so exponentials are
    # built as Pow(E, u); and rebuild any exp(...) already present in the incoming
    # expression (it was created before we entered the context) into that form.
    with _exp_is_pow(True):
        # Rebuild pre-existing exp(...) into Pow(E, ...). The lambda must accept a
        # variable arg count: for a NESTED exp (e.g. exp(x + exp(x))) sympy rebuilds
        # the outer node into Pow(E, ...) mid-walk, and `.replace(sympy.exp, ...)`
        # then re-matches that Pow and calls the replacement with its TWO args
        # (E, u) instead of one -- a 1-arg `lambda u:` crashed there. Using the last
        # arg handles both exp(u) (args=(u,)) and Pow(E,u) (args=(E,u)); rebuilding
        # exp(u) under exp_is_pow is idempotent (it is already Pow(E,u)).
        _to_pow = lambda *a: sympy.exp(a[-1])
        expr = sympy.sympify(expr).replace(sympy.exp, _to_pow)
        x = sympy.sympify(x).replace(sympy.exp, _to_pow)
        # A non-symbol integration variable (e.g. sin(x)) is only meaningful when the
        # integrand is a function of that whole expression — i.e. substituting
        # u = <var> removes every trace of the underlying symbols. Otherwise the
        # change of variables is not trivial (x*sin(x) is not a function of sin(x)
        # alone), and integrating "with respect to sin(x)" while treating the leftover
        # x as a constant silently gives a wrong answer. Refuse it and tell the caller
        # to introduce the substitution themselves.
        if not isinstance(x, sympy.Symbol):
            _u = sympy.Dummy('u')
            residual = sorted(expr.subs(x, _u).free_symbols & x.free_symbols, key=str)
            if residual:
                raise ValueError(
                    f"Cannot integrate with respect to the expression {x}: after the "
                    f"substitution u = {x}, the integrand still depends on "
                    f"{', '.join(map(str, residual))}, so it is not a function of {x} "
                    f"alone. Introduce the substitution yourself — solve u = {x} for the "
                    f"integrand, then call rubi_integrate(<integrand in u>, u)."
                )
        # When return_trace is set, collect a record of every rule the DFS tried
        # (accepted AND rejected, with the reason) — see format_trace().
        trace = [] if return_trace else None
        integ, matched_rules = _rubi_integrator.integrate(
            expr,
            x,
            pattern=pattern,
            trace=trace,
        )
    if return_trace:
        return integ, trace
    if return_matched_rules:
        return integ, matched_rules
    return integ


def reset_cache(integrator: _RubiIntegrator | None = None):
    if integrator is not None:
        integrator.reset_cache()
