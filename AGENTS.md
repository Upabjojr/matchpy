# AGENTS.md

Guidance for AI coding agents (and humans) working in this repository.

## Purpose

The project exists to provide `rubi_integrate`, defined in
`rubi_rules.base_objects`. It computes integrals using the
[Rubi](https://rulebasedintegration.org/) rule set:

```python
>>> rubi_integrate(sin(x), x)
-cos(x)
```

## What this project is

This repo started as **MatchPy** — a library for pattern matching on symbolic
expressions — and has been re-engineered into a **symbolic-integration engine**
that ports the Rubi rule set to Python on top of MatchPy + SymPy.

It is a **highly customized, strict fork of MatchPy**, deliberately stripped of
the runtime magic, dynamic class monkey-patching, and forced-inheritance
dependencies of the official version. The work is split across four Python
packages, layered bottom-up:

| Package           | May import          | Purpose |
|-------------------|---------------------|---------|
| `matchpy/`        | *(stdlib + `multiset` only)* | Core pattern matching — expression trees, wildcards, one-to-one and many-to-one matching, discrimination nets. Value classes subclass the lightweight `matchpy._typed.TypedModel` (see [Conventions](#conventions)). |
| `sympy_matching/` | `matchpy`           | Bridge between SymPy and MatchPy. Converts SymPy trees ↔ MatchPy trees (singledispatch), maps SymPy heads (`Add`, `Mul`, `Pow`, `sin`, …) to MatchPy `OperationHead`s, and adds `WildSymbol` (a SymPy symbol that becomes a MatchPy `Wildcard`). |
| `sympy_wolfram/`  | `matchpy`, `sympy_matching` | Data structures and behaviors for standard Wolfram Mathematica objects, plus a converter from Mathematica **Full-Form List (FFL)** ASTs (JSON) into SymPy code. Hosts the `MathematicaExpr` base class. |
| `rubi_rules/`     | all of the above    | The Rubi integration engine. Auto-generated rule modules, constraint helpers, the code generator, and `rubi_integrate()`. |

## Design philosophy

To keep clean boundaries between our modules and external libraries, the
matching engine enforces three rules:

- **Zero inheritance contamination** — you do not need (and are not allowed) to
  subclass external library expressions to make them matchable.
- **Decoupled translation layer** — external expression trees are converted into
  MatchPy's native tree structure by explicit translator functions *before*
  matching, rather than by modifying Python class hierarchies.
- **Pure tree-based structures** — patterns and subjects use a rigid, simple
  tree data structure. This keeps matching predictable and free of hidden side
  effects.

`sympy_matching` is the isolated adapter that enforces these rules at the SymPy
boundary: it recursively transforms SymPy AST nodes into native MatchPy trees
without touching SymPy's class hierarchy, ensuring SymPy's heavy inheritance
never bleeds into the matcher.

## Architecture

The four packages form a strict, one-directional dependency stack. Each layer
may only import from the layers below it.

**Layer 1 — Core matching engine (`matchpy/`).** The foundational matcher,
operating purely on the lightweight custom tree structure. Strictly isolated: it
cannot import from any other package here, and contains zero Python magic or
class-registration hacks. It expects clean, pre-translated native trees.

**Layer 2 — SymPy bridge (`sympy_matching/`).** The isolated translator between
SymPy and MatchPy. Imports only from `matchpy/`; has no visibility into
`sympy_wolfram/` or `rubi_rules/`.

**Layer 3 — Wolfram semantics (`sympy_wolfram/`).** Defines standard Wolfram
Mathematica objects (functions, constants, symbols) within the SymPy context and
hosts the `MathematicaExpr` abstract base class. Imports only from
`sympy_matching/` and `matchpy/`.

**Layer 4 — Rulebook (`rubi_rules/`).** Top-level application layer: the rule
engine, patterns, integration rules, and domain-specific code. May import from
any layer below.

### Enforcement matrix

| Module           | Allowed imports                          | Prohibited imports                          | State / side-effects |
|------------------|------------------------------------------|---------------------------------------------|----------------------|
| `matchpy`        | Standard Python only                     | `sympy_matching`, `sympy_wolfram`, `rubi_rules` | Purely stateless data matching |
| `sympy_matching` | `matchpy`                                | `sympy_wolfram`, `rubi_rules`               | Functional tree transformation |
| `sympy_wolfram`  | `matchpy`, `sympy_matching`              | `rubi_rules`                                | Definitions of standard Wolfram AST schemas |
| `rubi_rules`     | `matchpy`, `sympy_matching`, `sympy_wolfram` | *(none)*                                | Evaluation logic, utility extensions, rule execution |

### `MathematicaExpr` partitioning

Subclasses of `MathematicaExpr` are partitioned by whether they belong to the
standard Wolfram language or to Rubi-specific project utilities:

```
                  [ sympy_wolfram/ ]
                   MathematicaExpr   ◄─── abstract base class
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
 Standard Wolfram objects          [ rubi_rules/utils/* ]
 (e.g. Sin, Cos, List, Times)      Extended Rubi utility functions
                                   (e.g. from IntegrationUtilityFunctions.m)
```

- **Standard library components** — anything native to the official Wolfram
  Language spec must live in `sympy_wolfram/`. This covers not just the *nodes*
  (`Sin`, `List`, `Times`, `With`, `Module`, `Block`, `Set`, `Condition`, `If`, …)
  but their **generic evaluation semantics and any bug fixes to them**. Rule of
  thumb: if the behaviour would be wrong for *any* consumer of `sympy_wolfram/`
  (not just Rubi), it is a `sympy_wolfram/` concern — `sympy_wolfram/` is the
  reusable SymPy↔Wolfram connector, so fix it there and add its tests under
  `sympy_wolfram/tests/`, even if `rubi_rules/` is currently the only caller.
  E.g. `Condition[expr, test]`, and `rename_scoped_locals` (lexical scoping for
  `With`/`Module`/`Block` locals) both live in `sympy_wolfram/mathematica_expressions.py`.
- **Rubi extension components** — anything custom-defined for the Rubi codebase
  (e.g. functions from `IntegrationUtilityFunctions.m`) must live in
  `rubi_rules/utils/*` as a subclass of `MathematicaExpr`.

## Data flow & code generation

The Rubi Mathematica source is translated into Python in two stages:

```
Rubi .m rules → (precomputed) FFL JSON → codegen/generate.py
    → rubi_rules/rules/**.py  (SymPyReplacementPattern objects)
    → build_tracing_replacer() → MatchPy ManyToOneReplacer
    → rubi_integrate(expr, x)  → SymPy antiderivative
```

**Stage 1 — parse Mathematica to FFL.** With the upstream Rubi repo
([RuleBasedIntegration/Rubi](https://github.com/RuleBasedIntegration/Rubi))
checked out in a sibling folder of this project:

```sh
python rubi_rules/codegen/parse_rubi_to_ffl.py
```

This produces `../Rubi/rubi_fullformlist_results.json`, containing every Rubi
`*.m` source file parsed into **Full-Form List** form — the Python-list
equivalent of Mathematica's `FullForm`, e.g.
`Integral[Sin[x], x]` → `["Integral", ["Sin", "x"], "x"]`.

**Stage 2 — generate Python rules.**

```sh
python rubi_rules/codegen/generate.py --json ../Rubi/rubi_fullformlist_results.json
```

This writes the `rubi_rules/rules/**` Python files that encode Rubi's logic.

The same procedure applied to
[MathematicaSyntaxTestSuite](https://github.com/RuleBasedIntegration/MathematicaSyntaxTestSuite)
generates the test suite under `rubi_rules/rubi_test_suite/**`.

### Which Python object does a Wolfram head become?

This is decided **per layer**, and the two layers deliberately disagree.

**`sympy_wolfram/` — the interpreter and runtime library.** A head this project
implements becomes its **own `MathematicaExpr` node**, even when SymPy has a function
of the same name. SymPy's functions apply SymPy's eager-evaluation rules, which are
not Mathematica's, so the two are kept separate and the node evaluates only on
`doit()`. `FFLConverter.wolfram_library_names()` discovers those nodes by walking the
package, so adding a node makes it translatable with no list to update.

**`rubi_rules/` — overrides the default for heads where the two really do agree.**
Rubi's rules must match what a caller passes to `rubi_integrate`, and a caller writes
`expint(n, x)`, not `ExpIntegralE(n, x)`. `_EXTRA_SYMPY_HEADS` in
`codegen/generate.py` maps those heads to plain SymPy, and it is applied to
**patterns as well as replacements** (`_PATTERN_CUSTOM`) — a pattern holding a
deferred node could never match, so the rule would be dead. Pinned by
`TestWolframHeadTranslationLayering` in `tests/test_codegen.py`.

Two heads are *replaced* at generation time rather than translated, because neither
is really a function: `Identity[z]` → `z` and `Complex[a,b]` → `(a + sympy.I*b)`.

**`MathematicaExpr.rewrite_as_standard_sympy()`** is the general form of that
override, for heads a name table *cannot* express. It is deliberately distinct from
`doit()`:

* `doit()` **evaluates** with Mathematica semantics — `Factorial(5).doit()` is `120`;
* `rewrite_as_standard_sympy()` **translates** — it swaps the Wolfram head for the
  SymPy one and stops, so the result is still a function application
  (`factorial(5)`). That is what makes it usable on rule *patterns*, whose arguments
  are wildcards that must survive.

`Gamma` is the motivating case: Mathematica overloads it (`Gamma[a]` is the complete
gamma function, `Gamma[a,z]` the upper incomplete one) where SymPy has two separate
functions, so the *node* inspects its own arity and decides. `ProductLog` uses it to
move the branch index (`ProductLog[k,z]` → `LambertW(z,k)`), and `PolyGamma[z]` to
become `polygamma(0, z)`. The base implementation returns `self`, meaning "no standard
equivalent" — true of most nodes, which model Wolfram *language* constructs
(`With`, `Module`, `Condition`).

The codegen applies it through the `rewrite` hook of `ffl_to_sympy_short_code`, which
runs on the evaluated object *before* printing, to the pattern, the replacement **and**
the constraints. Note the ordering constraint: the round-trip verifies the printed text
against that object, so rewriting afterwards would always compare unequal and be
silently discarded.

Because the protocol keys off that evaluated **object**, the codegen target for such a
head must be the genuine node. Most heads resolve to a stand-in `sympy.Function(head)`
during shortening — deliberately, since the real deferred classes may evaluate eagerly
or reject wildcard arguments and break the round-trip — and a stand-in carries no
protocol, so the hook silently changes nothing. `_rewritable_wolfram_node()` is the
exception that hands back the real class for heads that can self-translate. Replacements
went untranslated for exactly this reason, which matters more than a stale pattern: a
pattern holding a Wolfram node merely fails to fire, whereas a replacement holding one
substitutes it into the **answer**. Pinned by
`test_no_self_translating_node_survives_in_a_replacement`.

### Generated-code hygiene

Two post-processing behaviours worth knowing, because both fail **silently**:

* **Shortening.** Emitted code is round-tripped through the printer
  (`_simplify_code`): eval → print → eval, keeping the short form only if it
  reproduces the same object. If any name in the *printed* form is missing from the
  eval namespace the verification raises `NameError`, the shortener gives up, and the
  rule is left in its verbose `(Integer(-1) * ...)` form with no error. So **verbose
  generated code is the symptom of a missing name**, not a cosmetic accident. The
  namespace must contain the rubi-level override names (`expint`, `LambertW`, …) and
  the module's declared scope locals (`k`, `r`, `s`, …). Merge only *Symbols* from the
  module namespace — merging it wholesale shadows the shortener's own placeholders
  (`Not`, `Simplify`) and defeats the round-trip for ~1200 expressions.
* **Unused imports.** After all modules are written, `strip_unused_imports()` runs
  `ruff check --select F401 --fix` over them. The header imports the union of every
  name the emitter *could* need, so generating first and pruning after is the only
  order that works. `ruff` is optional: a missing binary is reported, not fatal.

## Layout

- `matchpy/expressions/` — `expressions.py` (`TypedModel` expression types), `constraints.py`, `substitution.py`, `functions.py`; `matchpy/_typed.py` — the `TypedModel` base
- `matchpy/matching/` — `one_to_one.py`, `many_to_one.py`, `syntactic.py` (discrimination net), `bipartite.py`, `hopcroft_karp.py`, `code_generation.py`, `json_serialization.py`
- `sympy_matching/` — `operations.py` (the `SYMPY_NODES` head table), `conversion.py` (singledispatch converters), `wild.py`, `registered_heads.py`, `json_ext.py`, `constraint.py` (`SymPyMatchingConstraint`, the generic SymPy-side constraint base), `matching_rule.py` (`SymPyReplacementPattern`, `build_tracing_replacer`, `_make_matchpy_constraint`, `_make_replacement_fn` — the generic rule/replacer machinery, no Wolfram/Rubi dependency)
- `sympy_wolfram/` — `parser.py` (text→FFL), `interpreter.py` (FFL→SymPy), `objects.py` (`MathematicaExpr` + language constructs), `constraints.py` (`MathematicaConstraint`, a thin subclass of `(MathematicaExpr, SymPyMatchingConstraint)` — formerly `RubiConstraint`), `mathematica_functions.py` + `functions_eager.py` (standard Wolfram function nodes: `GCD`, `Sign`, `Floor`, `LeafCount`, …)
- `rubi_rules/base_objects.py` — `Int`, `rubi_integrate`, `load_rule_patterns`; re-exports the `sympy_matching` rule machinery (`SymPyReplacementPattern` is an alias of `SymPyReplacementPattern`, `build_tracing_replacer` comes from `sympy_matching.matching_rule`)
- `rubi_rules/rules/` — **auto-generated; DO NOT EDIT** (organized `r_1_algebraic_functions/…`, mirroring the Rubi Mathematica tree)
- `rubi_rules/codegen/` — `parse_rubi_to_ffl.py` and `generate.py` (the FFL→Python rule generator)
- `rubi_rules/utils/` — constraint helpers (`FreeQ`, `NeQ`, `IGtQ`, …) and Rubi utility functions
- `tests/` — MatchPy core tests; `<package>/tests/` — per-package tests

## Environment & running

- **Python 3.10 or newer** (`setup.cfg` sets `python_requires = >=3.10`; the newer packages use 3.10+ syntax like `str | None`).
- Core runtime deps: `multiset` (matchpy), plus `sympy` and `pydantic` for the layers above `matchpy/` (`sympy_matching.matching_rule.SymPyReplacementPattern` is a pydantic `BaseModel`; only `matchpy/` itself is pydantic-free). Install dev extras with `make init` (`pip install .[develop]`).
- **MatchPy core tests + doctests:** `make test` (`py.test tests/ --doctest-modules matchpy/ README.rst docs/example.rst`)
- **A single package's tests:** `pytest rubi_rules/tests/` (or `sympy_wolfram/tests/`, `sympy_matching/`, …)
- **One test file:** `pytest rubi_rules/tests/test_integrals_r_1_1_1_1.py -x`
- **Lint / style:** `make check` (flake8), `make lint` (pylint). Max line length **120**.
- **Regenerate Rubi rules:** see [Data flow & code generation](#data-flow--code-generation).

## Conventions

- **Every file starts with `# -*- coding: utf-8 -*-`.** Keep it.
- Respect the import stack in the [enforcement matrix](#enforcement-matrix) — never introduce an up-stack or sideways import.
- MatchPy value classes subclass **`matchpy._typed.TypedModel`** (Pydantic was removed for speed). Declare fields via class annotations; use `field(default_factory=...)` (from `matchpy._typed`) for mutable defaults (list/dict/set). `TypedModel.__init__(**kwargs)` assigns fields, applies defaults, and enforces a **shallow** `isinstance` type-check per field at construction (outer type only — `List[X]` is checked as `list`). Private attrs (`_name`) aren't fields; a subclass may turn an inherited field into a bare `ClassVar` (fixed class-level value) and it stops being an instance field. Don't reintroduce a Pydantic dependency **inside `matchpy/`** — the ban is scoped to the core package; higher layers still use pydantic (e.g. `SymPyReplacementPattern`).
- Prefer the existing **singledispatch** converters in `sympy_matching/conversion.py` when adding SymPy↔MatchPy support; register new heads through `register_sympy_head` / the `SYMPY_NODES` table in `sympy_matching/operations.py`.
- **Never hand-edit `rubi_rules/rules/**`.** Change `codegen/generate.py` (or the source FFL) and regenerate. Each generated file carries an `AUTO-GENERATED -- DO NOT EDIT` banner.
- The canonical integration variable in rule files is `Symbol('x')`; `rubi_integrate` substitutes when the caller passes a different variable (see the docstring in `base_objects.py`).
- Rubi `Condition` semantics: a failing condition raises `StopIteration`, which `ManyToOneReplacer.replace()` treats as "no match" and silently skips the rule — preserve this behavior.
- **Eager vs deferred utility functions (RuleDelayed).** Every Rubi utility exists in two forms: an eager plain function named `eager_<Name>` (e.g. `eager_Rt`, `eager_LeafCount`) in `rubi_rules/utils/utility_functions.py` (or `sympy_wolfram/functions_eager.py` for Wolfram-standard ones), and a deferred `MathematicaExpr` subclass keeping the bare name (`Rt`, `LeafCount`, …) in `rubi_rules/utils/rubi_utils.py` (or `sympy_wolfram/mathematica_functions.py`). Generated rules import the *deferred* classes, so a replacement like `Int(F**ExpandToSum(v_, x))` stays unevaluated until `_make_replacement_fn` substitutes the matched wildcards and calls `.doit()` — mirroring Mathematica's `:>`. A deferred `_evaluate` should **delegate to its eager counterpart**, not re-implement it (e.g. `sympy.expand` doesn't collect `x - I*x` → `(1-I)*x`, so it wouldn't match the `a+b*x+c*x**2` patterns).
- **Active vs inert trig.** Active trig is SymPy's `sin`/`cos`/…; *inert* trig is modelled as the dedicated heads `InertSin`/`InertCos`/… defined in `rubi_rules/utils/inert_functions.py`, which never auto-evaluate. `DeactivateTrig` converts active→inert, `ActivateTrig` inert→active, and `InertTrigFreeQ`/`InertTrigQ` test for the inert markers only — so an ordinary active-trig integrand is inert-trig-free and the `Not(InertTrigFreeQ)` fallback rules (CannotIntegrate catch-alls) do not steal it.
- **Rule match order does not matter — do not sort or reorder rules.** Correctness must not depend on which matching rule the `ManyToOneMatcher` yields first. Do not add logic to order rules by Rubi rule number, priority, or specificity, and do not try to change the match order. If integration is slow, the cause is elsewhere (e.g. an integrand that never normalizes into a matchable form, a non-terminating rewrite) — investigate that, not the ordering.
- The MatchPy core suite parametrizes the `match` fixture across `one-to-one`, `many-to-one`, `generated`, and `json-roundtrip` backends (`tests/conftest.py`). New matching features should pass under all backends.
- Doctests are part of the suite (see `Makefile` and `conftest.py`, which injects `f`, `a`, `b`, `x_`, … into the doctest namespace).

## Gotchas

- `README.rst` badges/CI (Travis, coveralls) reflect upstream MatchPy and are **not wired up for this fork**. Don't trust them as the source of truth. The README examples were stale for a while (upstream `Symbol` API); they have been updated to the renamed API (`NamedAtom`, `Arity.variadic`) and run as doctests — keep them passing.
- `sympy_matching/operations.py` does a `sys.path.insert` at import time — keep imports working when run both as a package and standalone.
- The rules tree is large and loaded lazily by glob (`load_rule_patterns('r_1_algebraic_functions/**')`). Loading everything is slow; scope the glob when testing a subset. Beware: a glob that matches nothing returns an **empty tuple silently** — no error, the integrator just has no rules.
- **SymPy auto-distributes a number over a sum**, so any function whose job is to *factor* one out cannot simply return `coeff * rest`: `Mul(Rational(1,3), 2 + 3*x)` evaluates straight back to `x + 2/3`, silently undoing the work. Use `sympy.core.mul._keep_coeff` (what SymPy's own `factor_terms` uses) — `utility_functions._content_times` wraps it. This bit `ContentFactor`, `FactorNumericGcd` and `CommonFactors`.
- A **`Simplify`-based comparison against Mathematica cannot see form**, only value, so it silently passes a function that returned its input unfactored. When the *form* is the contract (ContentFactor, FactorNumericGcd, anything feeding `NumericFactor`), compare **structurally**: render the SymPy value as `Times[...]`/`Plus[...]`/`Rational[p,q]` and judge with `SameQ`. Note `sympy.printing.mathematica.mathematica_code` re-associates on the way out (it prints that same `Mul` as `x + 2/3`), so it is useless for this — walk the tree yourself.
- Mathematica canonicalises a factor of exactly **-1** into a `Plus`: `Times[Rational[-1,q], Plus[t…]]` is stored as `Times[Rational[1,q], Plus[-t…]]`, while `-3/2`, `-2` and any case with a third factor keep the sign on the coefficient. `NumericFactor` walks those args, so the representation is observable — `NumericFactor[-2/3 - x]` is `+1/3` in Rubi.

## Before you finish

- Run the tests relevant to what you touched (at minimum the affected package's `tests/`).
- If you changed matching internals, run `make test` so doctests and all match backends are exercised.
- Run `make check` if you touched style-sensitive code.
