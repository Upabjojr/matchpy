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

### TODO — pick one resolution (all keep order irrelevant unless noted)

- [ ] **(preferred) Make rule 43 not undo rule 42.** Prevent `[43]` from firing on
      completed-square / perfect-square forms that `[11]` already handles (e.g. a
      guard so `ExpandToSum`-normalization is not applied to `a + b*(d*x + c)^2`
      shapes). Keeps order irrelevant; needs care to stay faithful to Rubi.
- [ ] **Cycle detection in `_RubiIntegrator.integrate`.** Track visited states
      (e.g. a set of canonicalized `current` values); stop when one repeats.
      Guarantees termination but may halt on a partially-reduced form depending on
      which branch is taken — combine with (preferred) for a correct result.
- [ ] **Re-open the invariant.** If a small set of Rubi rules genuinely needs
      ordering, decide how to encode a minimal, principled precedence WITHOUT a
      global sort (the invariant currently forbids sorting).
- [ ] Add a regression test: `rubi_integrate(exp(x)*sin(x**2 + x), x)` must
      terminate and match Mathematica's `Erf`/`Erfi` result.
- [ ] Audit for other mutually-inverse rule pairs (complete-square ↔ expand,
      factor ↔ expand, together ↔ apart) that can form the same kind of cycle.

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
