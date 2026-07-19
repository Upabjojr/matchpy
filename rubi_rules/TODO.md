# rubi_rules — Known issues & TODO

## 1. Rule-ordering dependency causes a non-terminating 42↔43 rewrite cycle — RESOLVED

**Status:** RESOLVED via path-aware DFS cycle detection (integrator-only, no rule
edits). `rubi_integrate(exp(x)*sin(x**2 + x), x)` now returns the correct
`Erf`/`Erfi` antiderivative (numerically verified; regression test in
`tests/test_integrate_exp_gaussian.py`). Details of the original problem and the
implemented fix below.

**Confirmed NOT a translation bug** — `QuadraticMatchQ` matches the
Mathematica original faithfully (`Rubi/Rubi/IntegrationUtilityFunctions.m:1427`;
verified `(x+1)^2` → False, `expand((x+1)^2)` → True, completed square → False).

**Symptom:** `rubi_integrate(exp(x)*sin(x**2 + x), x)` never terminates (runs many
minutes). The reduction reaches a pair of Gaussian integrals and then loops.

**Root cause:** in module `2.3 Miscellaneous exponentials`:

- Rule `[42]` completes the square:
  `Int(F^(c*x^2 + b*x + a)) → F^(a - b^2/4c) * Int(F^((2*c*x + b)^2/(4*c)))`
- The completed square `(2*c*x + b)^2/(4*c)` is matched by BOTH:
  - Rule `[11]` → `Erf`/`Erfi` (**terminates**), and
  - Rule `[43]` (`Int(F^v)` with `QuadraticQ(v) & Not(QuadraticMatchQ(v))`) →
    `ExpandToSum` **re-expands** it back to `c*x^2 + b*x + a`.
- If `[43]` fires, `[42]` re-fires → a **period-2 loop**. The integrator's
  `current == previous` convergence check cannot detect a 2-cycle.

**Why Rubi does not loop:** Mathematica tries downvalues top-down, and rule `[11]`
has a lower number than `[43]`, so `[11]` fires first on the completed square.
i.e. termination here **depends on rule order**.

**Tension:** this contradicts the project invariant "rule match order must not
matter" (documented in `AGENTS.md`). The `ManyToOneMatcher` does not preserve
Rubi's rule order, so on the full ruleset rule `[43]` can win the completed-square
form and the integration loops.

### Resolution — path-aware DFS cycle detection (DONE)

`_RubiIntegrator.integrate` is now a depth-first reducer (`_dfs_reduce_int` /
`_dfs_match_int` / `_dfs_reduce_result` in `base_objects.py`). Key properties:

- **Path-aware cycle detection.** Each recursion carries a frozenset `path` of the
  integrand forms currently on the reduction stack. A rule whose (recursively
  reduced) result re-enters a `path` form is a cycle and is skipped in favour of
  the next matching rule — so rule `[43]` is skipped at the completed square while
  rule `[42]` (which produces that square) is NOT globally banned.
- **Order-independent by preferring clean results.** Rules are tried in whatever
  order the matcher yields them; a *clean* result (no `Int`, no `CannotIntegrate`)
  wins immediately, and a non-clean terminal (`CannotIntegrate` / residual `Int`)
  is kept only as a fallback. So rule `[11]` (→ `Erf`) beats rule `[43]`'s
  `CannotIntegrate` regardless of yield order.
- **`CannotIntegrate` detected by head name** (`_dfs_is_clean`): round-tripping a
  rule's replacement through MatchPy turns `rubi_utils.CannotIntegrate` into a
  plain `Function('CannotIntegrate')`, so an isinstance/atoms check against the
  imported class misses it — this was the bug that made the first DFS still return
  `CannotIntegrate`.
- Backstop: a `budget` counter caps total match attempts.

Integrator-only; no rule/codegen changes. Full suite: 1437 pass, 7 pre-existing
failures. Regression test: `tests/test_integrate_exp_gaussian.py`.

### Remaining TODO

- [ ] Audit for other mutually-inverse rule pairs (complete-square ↔ expand,
      factor ↔ expand, together ↔ apart) that can form the same kind of cycle —
      the DFS handles them generically, but worth a sweep for correctness/perf.
- [ ] Performance: the full-ruleset build is ~50s (cached after first call); the
      DFS itself is fast (~3s once cached).
- [ ] (Rejected) Making rule 43 not undo rule 42 would need editing generated
      rules / codegen — out of scope: rules are codegen-owned.
- [ ] rubi_integrate(sin(x), sin(x)) returns correctly sin(x)**2/2, but rubi_integrate(x*sin(x), sin(x))
      probably returns an incorrect result, it should rather raise an exception and tell the user to use a solver to replace the variable u=sin(x)
      (i.e. allow complex expressions to be integration variables only if the integrand depends trivially on them, in the example before all instances of variable x get replaced with a simple u=sin(x) substitution)
- [ ] Use MatchPy codegen to generate a static decision tree for all rules. Is it correct?
      Can we reduce it to a reasonable size?
- [ ] do we even need to be able to serialize ManyToOneMatcher to JSON?

### Already fixed on the way to this (for context)

- exp represented as `Pow(E, ·)` via `_exp_is_pow` in `rubi_integrate` (SymPy `exp`
  never matched the `F^(...)` exponential rule patterns otherwise).
- Active/inert trig distinction via `Function('sin')(...)` markers;
  `InertTrigFreeQ`/`InertTrigQ`/`ActivateTrig`/`DeactivateTrig` corrected so the
  `Not(InertTrigFreeQ)` CannotIntegrate catch-alls no longer steal active-trig
  integrands.
- `ExpandToSum` deferred class now delegates to the eager `utility_functions`
  implementation (plain `sympy.expand` does not collect `x - I*x → (1-I)*x`).
- `powsimp(combine='exp')` applied before each `_integration_step` so
  `E^a * E^b → E^(a+b)`.
