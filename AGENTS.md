# AGENTS.md

Guidance for AI coding agents (and humans) working in this repository.

## What this project is

This repo started as **MatchPy** — a library for pattern matching on symbolic
expressions — and has been extended into a **symbolic-integration engine** that
ports the [Rubi](https://rulebasedintegration.org/) rule set to Python on top of
MatchPy + SymPy.

There are four Python packages, layered bottom-up:

| Package          | Depends on                    | Purpose |
|------------------|-------------------------------|---------|
| `matchpy/`       | `multiset` only               | Core pattern matching. Expression trees, wildcards, one-to-one and many-to-one matching, discrimination nets. **Rewritten as pydantic `BaseModel` classes** (see `matchpy/expressions/expressions.py`). |
| `sympy_matching/`| `matchpy`, `sympy`            | Bridge between SymPy and MatchPy. Converts SymPy expression trees ↔ MatchPy trees (singledispatch), maps SymPy heads (`Add`, `Mul`, `Pow`, `sin`, …) to MatchPy `OperationHead`s, and adds `WildSymbol` (a SymPy symbol that becomes a MatchPy `Wildcard`). |
| `sympy_wolfram/` | `sympy`                       | Converts Wolfram Mathematica **Full-Form List (FFL)** ASTs (JSON) into SymPy code. Standalone — no dependency on `rubi_rules`. Includes Mathematica control-flow node types (`With`, `Module`, `Condition`, …). |
| `rubi_rules/`    | all of the above              | The Rubi integration engine. Auto-generated rule modules, constraint helpers, the code generator, and `rubi_integrate()`. |


This project uses a highly customized, strict fork of MatchPy. It has been
re-engineered to eliminate runtime magic, dynamic class monkey-patching, and
forced class inheritance dependencies common in the official version.

To maintain clean boundaries between our modules and external libraries, the
matching engine enforces the following constraints:

* Zero Class Inheritance Contamination: You do not need (and are not allowed)
  to subclass external library expressions to make them matchable.
* Decoupled Translation Layer: Instead of modifying python class hierarchies,
  external expression trees must be converted into MatchPy's native tree
  structure via explicit translator functions before matching.
* Pure Tree-Based Structures: Patterns and subjects are represented using a
  rigid, simple tree-based data structure. This ensures predictability and
  prevents hidden side effects during the matching process.

`sympy_matching` serves as the isolated adapter and translation layer between
SymPy (the symbolic mathematics library) and our customized MatchPy engine. It
acts as a strict boundary keeper, ensuring SymPy's heavy class inheritance
structures never bleed into the pattern matcher.

Data flow for integration:

Rubi project implementation for Wolfram Mathematica can be found in: https://github.com/RuleBasedIntegration/Rubi

```
Rubi .m rules → (precomputed) FFL JSON → codegen/generate.py
    → rubi_rules/rules/**.py (RubiRulePattern objects)
    → build_tracing_replacer() → MatchPy ManyToOneReplacer
    → rubi_integrate(expr, x) → SymPy antiderivative
```

Running
```python
python rubi_rules/codegen/parse_rubi_to_ffl.py
```
assuming the Rubi has been checkout out in a sibling folder of this project, it will create ../Rubi/rubi_fullformlist_results.json 
that is a file that contains all Rubi `*.m` Mathematica source files parsed into full-form-list
(an equivalent of Mathematica's FullForm, but using python lists, e.g. Integral[Sin[x], x] ==> ["Integral", ["Sin", "x"], "x"])

Calling then:
```sh
python rubi_rules/codegen/generate.py --json ../Rubi/rubi_fullformlist_results.json
```
will generate `rubi_rules/rules/**` python files with the logic of Rubi translated into Python.

A similar procedure exists for https://github.com/RuleBasedIntegration/MathematicaSyntaxTestSuite to generate the test suite in rubi_rules/rubi_test_suite/**

## 2. Component Registry & Rules

### Layer 1: Core Matching Engine (matchpy/)
Role: The foundational pattern matching engine, operating purely on a lightweight, custom tree-based data structure.

Import Restrictions: Strictly Isolated. This module is completely decoupled and cannot import from any other component in this repository.

Design Philosophy: Contains zero Python magic or class inheritance registration hacks. It expects clean, pre-translated native expression trees.

### Layer 2: The SymPy Bridge (sympy_matching/)
Role: The isolated translator layer providing the connection between SymPy and MatchPy.

Import Restrictions: Can only import from matchpy/. It has zero visibility into sympy_wolfram/ or rubi_rules/.

Responsibility: Recursively transforms SymPy AST nodes into native MatchPy tree structures without altering SymPy's core class hierarchies.

### Layer 3: The Wolfram Semantics Layer (sympy_wolfram/)
Role: Defines the data structures and behaviors of standard Wolfram Mathematica objects within the SymPy context.

Import Restrictions: Can only import from sympy_matching/ and matchpy/.

Key Implementations:

Hosts the foundational MathematicaExpr abstract base class.

All standard, built-in Wolfram Mathematica objects (e.g., standard functions, constants, symbols) must be defined here.

### Layer 4: The Rule Rulebook (rubi_rules/)
Role: Top-level application layer containing the rule engines, patterns, and integration rule definitions (Rule-based Integrator).

Import Restrictions: Unrestricted down-stack. Can import from sympy_wolfram/, sympy_matching/, and matchpy/.

Key Implementations: Contains the core rule matching loops and domain-specific code.

## 3. MathematicaExpr Architecture & Inheritance Mapping

To manage Wolfram Mathematica expressions cleanly, subclasses of MathematicaExpr are strictly partitioned based on whether they belong to the standard language or domain-specific project utilities.

                  [ sympy_wolfram/ ]
                   MathematicaExpr  <─── (Abstract Base Class)
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
 Standard Wolfram Objects          [ rubi_rules/utils/* ]
(e.g., Sin, Cos, List, Times)     Extended Rubi Utility Functions
                                  (e.g., IntegrationUtilityFunctions.m)
Allocation Rules:
Standard Library Components: If an object is native to the official Wolfram Language specification, its implementation class must live in sympy_wolfram/.

Rubi Extension Components: If an object or function is custom-defined specifically for the Rubi rules codebase (e.g., functions originating from IntegrationUtilityFunctions.m), its class definition must reside in rubi_rules/utils/* as a subclass of MathematicaExpr.

## Architectural Enforcement Matrix

ModuleAllowed ImportsProhibited ImportsState/Side-Effects AllowedmatchpyNone (Standard Python only)sympy_matching, sympy_wolfram, rubi_rulesPurely stateless data matchingsympy_matchingmatchpysympy_wolfram, rubi_rulesFunctional tree transformationsympy_wolframmatchpy, sympy_matchingrubi_rulesDefinitions of standard Wolfram AST schemasrubi_rulesmatchpy, sympy_matching, sympy_wolframNoneEvaluation logic, utility extensions, rule execution

## Layout

- `matchpy/expressions/` — `expressions.py` (pydantic expression types), `constraints.py`, `substitution.py`, `functions.py`
- `matchpy/matching/` — `one_to_one.py`, `many_to_one.py`, `syntactic.py` (discrimination net), `bipartite.py`, `hopcroft_karp.py`, `code_generation.py`, `json_serialization.py`
- `sympy_matching/` — `operations.py` (the `SYMPY_NODES` head table), `conversion.py` (singledispatch converters), `wild.py`, `constraints.py`, `registered_heads.py`, `json_ext.py`
- `sympy_wolfram/` — `ffl_to_sympy.py`, `mathematica_parser.py`, `mathematica_expressions.py`, `mathematica_functions.py`
- `rubi_rules/base_objects.py` — `Int`, `RubiRulePattern`, `build_tracing_replacer`, `rubi_integrate`, `load_rule_patterns`
- `rubi_rules/rules/` — **auto-generated; DO NOT EDIT** (organized `r_1_algebraic_functions/…` mirroring the Rubi Mathematica tree)
- `rubi_rules/codegen/generate.py` — the FFL→Python rule generator
- `rubi_rules/utils/` — constraint helpers (`FreeQ`, `NeQ`, `IGtQ`, …) and Rubi utility functions
- `tests/` — MatchPy core tests; `<package>/tests/` — per-package tests

## Environment & running

- **Python 3.10 or newer** in this environment (`setup.cfg` still advertises `>=3.6`, but the newer packages use 3.10+ syntax like `str | None`). Assume 3.12.
- Core runtime deps: `multiset`, `sympy`, `pydantic`. Install dev extras with `make init` (`pip install .[develop]`).
- **Run the MatchPy core tests + doctests:** `make test`
  (`py.test tests/ --doctest-modules matchpy/ README.rst docs/example.rst`)
- **Run a single package's tests:** `pytest rubi_rules/tests/` (or `sympy_wolfram/tests/`, `sympy_matching/`, etc.)
- **Run one test file:** `pytest rubi_rules/tests/test_integrals_r_1_1_1_1.py -x`
- **Lint / style:** `make check` (flake8), `make lint` (pylint). Max line length **120**.
- **Regenerate Rubi rules:** `python -B -m rubi_rules.codegen.generate` (needs the FFL JSON; see the module docstring).

## Conventions

- **Every file starts with `# -*- coding: utf-8 -*-`.** Keep it.
- MatchPy expression types are **pydantic models** — construct/copy via pydantic semantics, not ad-hoc `__init__` mutation.
- Prefer the existing **singledispatch** converters in `sympy_matching/conversion.py` when adding SymPy↔MatchPy support; register new heads through `register_sympy_head` / the `SYMPY_NODES` table in `sympy_matching/operations.py`.
- **Never hand-edit `rubi_rules/rules/**`.** Change `codegen/generate.py` (or the source FFL) and regenerate. Each generated file carries an `AUTO-GENERATED -- DO NOT EDIT` banner.
- The canonical integration variable in rule files is `Symbol('x')`; `rubi_integrate` substitutes when the caller passes a different variable (see the docstring in `base_objects.py`).
- Rubi `Condition` semantics: a failing condition raises `StopIteration`, which `ManyToOneReplacer.replace()` treats as "no match" and silently skips the rule — preserve this behavior.
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

## Purpose of the project

The purpose is to provide `rubi_integrate` defined in `rubi_rules.basic_objects`.

This function allows users to compute integrals using Rubi rules.

Examples:

```python
>>> rubi_integrate(sin(x), x)
-cos(x)
```

