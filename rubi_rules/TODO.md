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
- [X] rubi_integrate(sin(x), sin(x)) returns correctly sin(x)**2/2, but rubi_integrate(x*sin(x), sin(x))
      probably returns an incorrect result, it should rather raise an exception and tell the user to use a solver to replace the variable u=sin(x)
      (i.e. allow complex expressions to be integration variables only if the integrand depends trivially on them, in the example before all instances of variable x get replaced with a simple u=sin(x) substitution)
- [ ] Use MatchPy codegen to generate a static decision tree for all rules. Is it correct?
      Can we reduce it to a reasonable size?
- [ ] do we even need to be able to serialize ManyToOneMatcher to JSON?
- [X] clean up `ffl_to_sympy_code_short`: it should accept
      the namespace of defined variables instead of returning it (what's the point of returning it btw?),
      furthermore, it should have an optional parameter of type StrPrinter (the class defined in SymPy).
      By default, simplify the expression if eval(str_printer.print(obj), ...namespace...) == obj,
      but str_printer could be a custom subclass of StrPrinter. Make sure the code generating the namespace
      is clear to read in rubi_rules/codegen/generate.py. Clean up the code in generate.py and make it more human readable.
      Make sure that all of these edits do not impact the way rubi_rules/rules/** are generated... the generated code has to
      remain equal to what it was.
- [ ] keep checking if Wolfram Mathematica does the same
- [ ] more tests in sympy_wolfram/ ==> make some nested Module / With / Block and check that variables with same name bind correctly (bindings in the inner scope vs outer scope). Make some calls to Wolfram Mathematica to check that the behaviour is the same.
- [ ] test looper functions in sympy_wolfram/ (check that all https://reference.wolfram.com/language/guide/LoopingConstructs.html work)
- [ ] only one slow test should be allowed to test rubi_integrate( ) full loading. Please merge all tests into a single one. Add a note in AGENTS.md to specify this feature, also comment it in the notes of that single slow test.
- [ ] code generator for rubi_rules/rules/** should avoid creating Symbol('...') objects in the code... just define them at the start of the file.
- [ ] move more stuff unrelated to rubi_rules/ to sympy_wolfram/
- [ ] restructure sympy_wolfram/ to clearly separate the parser, the interpreter and the implemented mathematica objects.
- [ ] loading Rubi rules from SymPy is very expensive... but what about writing them directly in MatchPy-like syntax? After loading the rules one could just create the same rules with `to_expression(pattern)`
- [ ] rename `to_expression` (and also get rid of `from_expression`)
- [ ] should not depend on SymPy (maybe with some exceptions)
- [X] remove "fixed_var" from sympy_wolfram/
- [X] SymPy parser has been updated to correctly handle "Derivative" nodes.
- [ ] (solved?) rubi_integrate(exp(x)*cos(x)*x, x, return_matched_rules=True)
- [ ] create sympy_to_matchpy and matchpy_to_sympy function, and _sympy_to_matchpy / _matchpy_to_sympy that are single dispatched.
- [X] rename_scoped_locals: shouldn't this act entirely inside the With, Module, Block inside sympy_wolfram/? Why is it imported in rubi_rules/? Maybe these constructs should instead replace their binding symbols with Dummy variables.

- [ ] are there memory leaks?
- [ ] generated rules contain stuff like: With(List(Set(Symbol('g'), ... ) ==> could you please avoid defining Symbol('g') in the rule? All symbols should be defined at the beginning of the file.
- [ ] remember to document IDENTITY_ELEMENT as optional matching character.
- [ ] remove not used variables from generated rules.
- [ ] RubiConstraint ==> rename and make it a subtype of MathematicaExpr?
- [ ] should MathematicaConstraint and the logic to build constraints based on SymPy expressions be moved to sympy_matching/ ? e.g. create the replacement lambda which is currently done in rubi_rules/ ? Maybe even RubiRulePattern should be renamed and moved to sympy_matching/ ?
- [ ] FreeQ in MatchPy should be removed, it's a duplicate of the other FreeQ.
- [ ] rename MatchPy classes that have a naming conflict with SymPy classes.
- [ ] use Fable for more thorough investigation of failures difficult to detect reported in this TODO file.
- [ ] name conflict of utility and eager functions: prepend eager_ to their names
- [ ] all stuff managing rules and creating replacement pattern should be moved to sympy_matching/ (maybe even constraints, MathematicaConstraint, which should then be renamed). Rule pattern matching should be generically used by SymPy, independently of Wolfram and Rubi.

Strange warning:

In [8]: rubi_integrate(exp(x)*cos(x)*x, x, return_matched_rules=True)
~/venv_global/lib/python3.12/site-packages/sympy/core/operations.py:481: SymPyDeprecationWarning: 

Using non-Expr arguments in Mul is deprecated (in this case, one of
the arguments has type 'BooleanFalse').

If you really did intend to use a multiplication or addition operation with
this object, use the * or + operator instead.

See https://docs.sympy.org/latest/explanation/active-deprecations.html#non-expr-args-deprecated
for details.

This has been deprecated since SymPy version 1.7. It
will be removed in a future version of SymPy.

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

## 2. `x^m/(a+b x^n)` partial-fraction family (1.1.3.2 #37–44) gives WRONG answers — OPEN

**Status:** OPEN. A genuine multi-bug knot; a faithful `Rt` fix was implemented and
**reverted** because it regressed without fixing the integrals (see below). Suite is
back to green (1003 passed, 1 skip).

**Symptom (numerically verified WRONG — derivative ≠ integrand):**

    x/(a + b*x**6)        -> WRONG
    x**3/(a + b*x**6)     -> WRONG
    x/(a + b*x**10)       -> WRONG
    x**3/(1 - x**6)       -> WRONG   (the only wrong answer found in a full
                                      numeric re-verification of a 81-case suite log)

These match Rubi's rules `1.1.3.2 #37/#38/#41–44` (the roots-of-unity partial-fraction
decomposition of `Int[x^m/(a+b x^n)]`), e.g. source line 43 (PosQ branch):

    Module[{r=Numerator[Rt[a/b,n]], s=Denominator[Rt[a/b,n]], k, u},
      u = Int[(r*Cos[(2k-1)m*Pi/n] - s*Cos[(2k-1)(m+1)Pi/n]*x)/(r^2 - 2 r s Cos[(2k-1)Pi/n] x + s^2 x^2), x] + Int[...+...];
      2*(-1)^(m/2)*r^(m+2)/(a n s^m)*Int[1/(r^2+s^2 x^2)] + Dist[2 r^(m+1)/(a n s^m), Sum[u,{k,1,(n-2)/4}], x]]

**This is a MULTI-bug knot — needs all of the following, coordinated:**

1. **`Rt` is NOT faithful.** Codegen maps `'Rt' -> sympy.root` (interpreter
   `SYMPY_FUNC_MAP`), which does NOT split fractions. Rubi's
   `Rt[u,n] := RtAux[TogetherSimplify[u], n]` splits: `Rt[a/b,n] = a^(1/n)/b^(1/n)`
   (Pi-verified: `Numerator[Rt[a/b,6]] = a^(1/6)`, `Denominator = b^(1/6)`).
   Because ours doesn't split, `r,s` come out `(a/b)^(1/6)` / `1` — wrong.
   NOTE: a faithful eager `Rt`/`RtAux` ALREADY EXISTS in `utility_functions.py`; it
   is simply bypassed. The intended fix is a DEFERRED `Rt` node in `rubi_utils.py`
   (stay symbolic until `n` is a concrete integer, then delegate to eager `Rt`) +
   `'Rt': 'Rt'` in `generate.py` `RUBI_UTILS_MAP` + regenerate. This was tried and
   correctly produced `r=a^(1/6)`, `s=b^(1/6)`.

2. **BUT `r,s` correct is NOT sufficient** — the integrals stay WRONG, so rule 37/38
   have a SECOND, DEEPER assembly bug. For `x^3/(1-x^6)` (rule 38, where `r=s=1`, so
   `Rt` is irrelevant) the leftover error is exactly
   `d/dx(ours) - integrand = (-2x - 1)/(3 (x+1)(x^2+x+1))`
   — an incorrectly-integrated sub-piece in the roots-of-unity decomposition. Needs a
   step-by-step diff against Rubi's `Steps[Int[x^3/(1-x^6),x]]` on the Pi to localize
   (candidates: a `Cos[(2k-1)·/n]` value, a coefficient, the `Sum`, or a downstream
   quadratic-denominator sub-integral rule).

3. **Our `RtAux` does not terminate on some input.** Wiring the faithful `Rt` in made
   rule 101 of `r_1_2_1_2` fail to load with `RecursionError` (a pre-existing
   `RtAux` non-convergence, NOT caught by a `try/except RecursionError` in the
   deferred node — so the recursion is triggered somewhere in generation, not in
   `_evaluate`). Must be fixed before `Rt` can be rewired, else it adds a skip and
   breaks `test_the_only_skipped_rule_is_the_upstream_rubi_typo`.

**Do NOT** fix this by broadening `Numerator`/`Denominator` to split `Rational`
exponents globally — TRIED, it splits `(a/b)^(1/6)` correctly but REGRESSES
`x^2/(a+b x^6)` (and others) from CORRECT to WRONG, because those two functions are
used pervasively and many rules rely on the Integer-only behavior. The split must
live in `Rt` (only `Rt` callers affected), matching Rubi.

**Recommended plan (as a unit):** (i) make `RtAux` terminate; (ii) re-add the deferred
`Rt` + `RUBI_UTILS_MAP` entry + regenerate, confirm `r,s` and no new skip; (iii)
deep-trace the assembly residual for `x^3/(1-x^6)` against Rubi on the Pi
(`ssh pi@192.168.1.119`, `<<Rubi\`; Steps[Int[...]]`) and fix the specific utility /
rule term. Verify by NUMERIC complex-point derivative check (never `simplify(diff-f)==0`,
which false-positives on these special-function results).
