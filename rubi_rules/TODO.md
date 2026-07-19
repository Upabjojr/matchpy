# rubi_rules — Known issues & TODO

## 1. Rule-ordering dependency causes a non-terminating 42↔43 rewrite cycle

**Status:** open. Confirmed NOT a translation bug — `QuadraticMatchQ` matches the
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

### Progress

- [x] **Cycle detection (coarse) in `_RubiIntegrator` — DONE.** A `seen` set of
      visited integrands is threaded through `integrate` → `_integration_step` →
      `_preprocess_integrate` → `_matchpy_integrate`. `_matchpy_integrate` now
      enumerates the matcher's rules in order and skips any whose result only
      revisits `seen` forms (and any whose Condition raises StopIteration), taking
      the next matching rule instead. **`exp(x)*sin(x**2+x)` now TERMINATES**
      (~79s) instead of looping. No rule/codegen changes. Full suite: 1437 pass.
      LIMITATION: the `seen` set is *global*, so it over-skips — rule `[42]`
      (complete-the-square) gets skipped because its output was already seen during
      the cycle, so the result is `CannotIntegrate(...)` rather than the correct
      `Erf`/`Erfi`.

### TODO

- [ ] **Path-aware backtracking (the correct version).** Skip only the rule whose
      result returns to a state ON THE CURRENT REDUCTION PATH (not any globally
      seen form), then take the next matching rule at that choice point. This
      reaches `Erf`/`Erfi` for `exp(x)*sin(x**2+x)`. Requires restructuring
      `integrate`'s breadth-first outer loop into a DFS with a path/visited-on-path
      stack so "previous step" and "next rule" are well-defined. Integrator-only
      (no rule/codegen changes) — this is the agreed direction.
- [ ] Add a regression test: `rubi_integrate(exp(x)*sin(x**2 + x), x)` must
      terminate and match Mathematica's `Erf`/`Erfi` result.
- [ ] Audit for other mutually-inverse rule pairs (complete-square ↔ expand,
      factor ↔ expand, together ↔ apart) that can form the same kind of cycle.
- [ ] (Rejected) Making rule 43 not undo rule 42 would need editing generated
      rules / codegen — out of scope: rules are codegen-owned.

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
