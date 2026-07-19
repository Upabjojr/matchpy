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
| `matchpy/`        | *(stdlib + `multiset` only)* | Core pattern matching — expression trees, wildcards, one-to-one and many-to-one matching, discrimination nets. currently implemented as pydantic `BaseModel` classes (`matchpy/expressions/expressions.py`), though pydantic is a temporary stopgap slated for removal (see [Conventions](#conventions)). |
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
  Language spec must live in `sympy_wolfram/`.
- **Rubi extension components** — anything custom-defined for the Rubi codebase
  (e.g. functions from `IntegrationUtilityFunctions.m`) must live in
  `rubi_rules/utils/*` as a subclass of `MathematicaExpr`.

## Data flow & code generation

The Rubi Mathematica source is translated into Python in two stages:

```
Rubi .m rules → (precomputed) FFL JSON → codegen/generate.py
    → rubi_rules/rules/**.py  (RubiRulePattern objects)
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

## Layout

- `matchpy/expressions/` — `expressions.py` (pydantic expression types), `constraints.py`, `substitution.py`, `functions.py`
- `matchpy/matching/` — `one_to_one.py`, `many_to_one.py`, `syntactic.py` (discrimination net), `bipartite.py`, `hopcroft_karp.py`, `code_generation.py`, `json_serialization.py`
- `sympy_matching/` — `operations.py` (the `SYMPY_NODES` head table), `conversion.py` (singledispatch converters), `wild.py`, `constraints.py`, `registered_heads.py`, `json_ext.py`
- `sympy_wolfram/` — `ffl_to_sympy.py`, `mathematica_parser.py`, `mathematica_expressions.py`, `mathematica_functions.py`
- `rubi_rules/base_objects.py` — `Int`, `RubiRulePattern`, `build_tracing_replacer`, `rubi_integrate`, `load_rule_patterns`
- `rubi_rules/rules/` — **auto-generated; DO NOT EDIT** (organized `r_1_algebraic_functions/…`, mirroring the Rubi Mathematica tree)
- `rubi_rules/codegen/` — `parse_rubi_to_ffl.py` and `generate.py` (the FFL→Python rule generator)
- `rubi_rules/utils/` — constraint helpers (`FreeQ`, `NeQ`, `IGtQ`, …) and Rubi utility functions
- `tests/` — MatchPy core tests; `<package>/tests/` — per-package tests

## Environment & running

- **Python 3.10 or newer** (`setup.cfg` still advertises `>=3.6`, but the newer packages use 3.10+ syntax like `str | None`).
- Core runtime deps: `multiset`, `sympy`, `pydantic`. Install dev extras with `make init` (`pip install .[develop]`).
- **MatchPy core tests + doctests:** `make test` (`py.test tests/ --doctest-modules matchpy/ README.rst docs/example.rst`)
- **A single package's tests:** `pytest rubi_rules/tests/` (or `sympy_wolfram/tests/`, `sympy_matching/`, …)
- **One test file:** `pytest rubi_rules/tests/test_integrals_r_1_1_1_1.py -x`
- **Lint / style:** `make check` (flake8), `make lint` (pylint). Max line length **120**.
- **Regenerate Rubi rules:** see [Data flow & code generation](#data-flow--code-generation).

## Conventions

- **Every file starts with `# -*- coding: utf-8 -*-`.** Keep it.
- Respect the import stack in the [enforcement matrix](#enforcement-matrix) — never introduce an up-stack or sideways import.
- MatchPy expression types are **pydantic models** — construct/copy via pydantic semantics, not ad-hoc `__init__` mutation. Note that pydantic is a **temporary stopgap** used only to validate that field type annotations are correct; the long-term aim is to remove it, since it slows the matcher down. Don't build features that depend on pydantic-specific behavior beyond type checking.
- Prefer the existing **singledispatch** converters in `sympy_matching/conversion.py` when adding SymPy↔MatchPy support; register new heads through `register_sympy_head` / the `SYMPY_NODES` table in `sympy_matching/operations.py`.
- **Never hand-edit `rubi_rules/rules/**`.** Change `codegen/generate.py` (or the source FFL) and regenerate. Each generated file carries an `AUTO-GENERATED -- DO NOT EDIT` banner.
- The canonical integration variable in rule files is `Symbol('x')`; `rubi_integrate` substitutes when the caller passes a different variable (see the docstring in `base_objects.py`).
- Rubi `Condition` semantics: a failing condition raises `StopIteration`, which `ManyToOneReplacer.replace()` treats as "no match" and silently skips the rule — preserve this behavior.
- **Eager vs deferred utility functions (RuleDelayed).** Every Rubi utility exists twice under the same name: an eager plain function in `rubi_rules/utils/utility_functions.py`, and a deferred `MathematicaExpr` subclass in `rubi_rules/utils/rubi_utils.py`. Generated rules import the *deferred* classes, so a replacement like `Int(F**ExpandToSum(v_, x))` stays unevaluated until `_make_replacement_fn` substitutes the matched wildcards and calls `.doit()` — mirroring Mathematica's `:>`. A deferred `_evaluate` should **delegate to its eager counterpart**, not re-implement it (e.g. `sympy.expand` doesn't collect `x - I*x` → `(1-I)*x`, so it wouldn't match the `a+b*x+c*x**2` patterns).
- **Active vs inert trig.** Active trig is SymPy's `sin`/`cos`/…; *inert* trig is modelled as undefined functions `Function('sin')(...)` etc. (defined in `utility_functions.py`) which never auto-evaluate. `DeactivateTrig` converts active→inert, `ActivateTrig` inert→active, and `InertTrigFreeQ`/`InertTrigQ` test for the inert markers only — so an ordinary active-trig integrand is inert-trig-free and the `Not(InertTrigFreeQ)` fallback rules (CannotIntegrate catch-alls) do not steal it.
- **Rule match order does not matter — do not sort or reorder rules.** Correctness must not depend on which matching rule the `ManyToOneMatcher` yields first. Do not add logic to order rules by Rubi rule number, priority, or specificity, and do not try to change the match order. If integration is slow, the cause is elsewhere (e.g. an integrand that never normalizes into a matchable form, a non-terminating rewrite) — investigate that, not the ordering.
- The MatchPy core suite parametrizes the `match` fixture across `one-to-one`, `many-to-one`, `generated`, and `json-roundtrip` backends (`tests/conftest.py`). New matching features should pass under all backends.
- Doctests are part of the suite (see `Makefile` and `conftest.py`, which injects `f`, `a`, `b`, `x_`, … into the doctest namespace).

## Gotchas

- `README.rst` badges/CI (Travis, coveralls) reflect upstream MatchPy and are **not wired up for this fork**. Don't trust them as the source of truth.
- `sympy_matching/operations.py` does a `sys.path.insert` at import time — keep imports working when run both as a package and standalone.
- The rules tree is large and loaded lazily by glob (`load_rule_patterns('r_1_algebraic/**')`). Loading everything is slow; scope the glob when testing a subset.

## Before you finish

- Run the tests relevant to what you touched (at minimum the affected package's `tests/`).
- If you changed matching internals, run `make test` so doctests and all match backends are exercised.
- Run `make check` if you touched style-sensitive code.
