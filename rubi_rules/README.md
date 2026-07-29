# rubi_rules

Symbolic integration for SymPy using the [Rubi](https://rulebasedintegration.org/)
rule set (Rule-Based Integration), matched with MatchPy.

The public entry point is **`rubi_integrate`**.

```python
from sympy import Symbol, sin, exp
from rubi_rules.base_objects import rubi_integrate

x = Symbol('x')

rubi_integrate(1/x, x)            # log(x)
rubi_integrate(x**2, x)           # x**3/3
rubi_integrate(sin(x)*x, x)       # -x*cos(x) + sin(x)
rubi_integrate(exp(x**2), x)      # sqrt(pi)*erfi(x)/2
```

Results are ordinary SymPy expressions. Note that exponentials are returned in
`E**(...)` (i.e. `Pow(E, ...)`) form rather than `exp(...)` — the two are equal
(`E**u == exp(u)`); the port carries exponentials as `Pow(E, ·)` internally so
they match Rubi's `F^(...)` rule patterns.

## `rubi_integrate(expr, x, ...)`

| argument | default | meaning |
|----------|---------|---------|
| `expr` | — | the integrand (a SymPy expression) |
| `x` | — | the integration variable |
| `pattern` | `'**'` | glob selecting which generated rule files to load (see below) |
| `return_matched_rules` | `False` | also return the list of rules that were **accepted** |
| `return_trace` | `False` | also return a full DFS trace of rules **accepted and rejected** |

If the integrand cannot be integrated with the available rules it is returned
unevaluated as `Int(expr, x)`, or wrapped in `CannotIntegrate(expr, x)` when a
Rubi rule explicitly gives up.

### Which rules ran: `return_matched_rules=True`

Returns `(result, matched_rules)`. `matched_rules` is a list of `(result, applied)`
pairs (one per top-level integrand handled), where `applied` is a flat list of the
rules **accepted** on the winning path, each as `(module_name, rule_number)`:

```python
result, matched = rubi_integrate(exp(x)*sin(x**2 + x), x, return_matched_rules=True)
# matched == [(result, [
#     ('4.7.7 F^(c (a+b x)) trig(d+e x)^n', 44),
#     ('2.3 Miscellaneous exponentials', 43),
#     ('2.3 Miscellaneous exponentials', 42),
#     ('2.3 Miscellaneous exponentials', 11),
#     ... ])]
```

This shows only the rules that *stuck*. It does **not** show rules that matched
but were rejected — for that, use `return_trace`.

### Full search trace: `return_trace=True`

`rubi_integrate` reduces an integral with a depth-first search: at each
sub-integral it tries the matching rules and picks one, backing out of rules that
lead to a cycle or that fail their side conditions. `return_trace=True` returns
`(result, trace)`, where `trace` is a list of one record per rule **tried**:

```python
{'depth': int,           # reduction depth (how nested the sub-integral is)
 'integrand': Int(...),  # the sub-integral the rule was tried on
 'rule': (module, num),  # the rule, or its label string
 'status': str}          # what happened — see below
```

Statuses:

| status | meaning |
|--------|---------|
| `accepted` | produced a clean antiderivative (no `Int`, no `CannotIntegrate`); taken |
| `accepted (fallback)` | no clean rule was available, so this non-clean result was taken |
| `rejected (cycle)` | its result re-entered a sub-integral already on the current path (a loop) |
| `rejected (condition failed)` | the rule's side condition (`/;`) failed at apply time |
| `candidate (non-clean)` | matched but produced an `Int`/`CannotIntegrate`; kept only as a fallback |

`format_trace` renders it as indented text (deeper reductions are indented more):

```python
from rubi_rules.base_objects import rubi_integrate, format_trace

result, trace = rubi_integrate(exp(x)*sin(x**2 + x), x, return_trace=True)
print(format_trace(trace))
```

```
        rejected (cycle)           2.3 Miscellaneous exponentials:[42]   Int(E**(-I*x**2 + x*(1 - I) + 1/2))
        candidate (non-clean)      9.3 Miscellaneous integration rules:[67] Int(E**(-I*x**2 + x*(1 - I) + 1/2))
      candidate (non-clean)      2.3 Miscellaneous exponentials:[43]   Int(E**(I*(-2*I*x + 1 - I)**2/4))
      accepted                   2.3 Miscellaneous exponentials:[11]   Int(E**(I*(-2*I*x + 1 - I)**2/4))
    accepted                   2.3 Miscellaneous exponentials:[42]   Int(E**(-I*x**2 + x*(1 - I)))
  accepted                   2.3 Miscellaneous exponentials:[43]   Int(E**(x*(-I*x + 1 - I)))
accepted                   4.7.7 F^(c (a+b x)) trig(d+e x)^n:[44]   Int(E**x*sin(x**2 + x))
```

Records are appended in reduction order, so a sub-integral's rules appear
(indented) before the rule that produced it. `rejected`/`candidate` entries are
the branches the DFS explored and backed out of — e.g. above, rule `[43]` was
rejected in favour of `[11]` at the completed square, which is how the result
reaches `Erf`/`Erfi` instead of `CannotIntegrate`.

## Scoping the rules: the `pattern` argument

`pattern` is a glob over `rubi_rules/rules/**`. The default `'**'` loads the whole
rule set (~7700 rules; the first call builds the matcher and takes ~a minute, then
it is cached). Scope to a subsection for speed when you know which rules you need:

```python
rubi_integrate(exp(x**2), x, pattern='r_2_exponentials/**')
rubi_integrate(1/x, x,      pattern='r_1_algebraic_functions/**')
```

## How it works (short version)

Rubi's `.m` rules are translated by `codegen/generate.py` into Python
`SymPyReplacementPattern` objects under `rules/` (auto-generated — do not edit). Each rule
is a SymPy pattern + constraints + replacement. `rubi_integrate` converts the
integral to a MatchPy expression, matches rules, and applies replacements,
reducing `Int(...)` nodes depth-first until the integral is solved. Rule match
order is **not** significant — the search prefers a fully-integrated result over a
`CannotIntegrate`/residual-`Int` one regardless of which rule matches first.

See the repository-root `AGENTS.md` for the full architecture (eager vs deferred
utility functions, active vs inert trig, the exp/`Pow(E,·)` representation, and the
code-generation pipeline).
