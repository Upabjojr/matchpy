# Rules, constraints, and the replacer

How to turn SymPy patterns into a working rewrite system: `SymPyReplacementPattern`,
constraint guards (`FreeOf`, bare Booleans, custom `SymPyMatchingConstraint`
subclasses), and `build_replacer`. For the wildcard semantics underneath, see
[`wildcards.md`](wildcards.md).

Every example is a doctest, executed by `sympy_matching/tests/test_docs.py`, and uses
only `sympy`, `omnimatch` and `sympy_matching`.

```python
>>> from sympy import Symbol, Ne, sin, cos
>>> from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
>>> from sympy_matching.matching_rule import (
...     SymPyReplacementPattern, build_replacer, to_omnimatch_expression)
>>> from sympy_matching.conversion import omnimatch_to_sympy
>>> x = Symbol('x')

```

---

## 1. A rule is pattern + guards + replacement

```python
>>> m_ = WildSymbol('m')
>>> power_rule = SymPyReplacementPattern(
...     pattern=x**m_,
...     constraints=(Ne(m_, -1),),
...     replacement=x**(m_ + 1)/(m_ + 1),
...     module_name='docs example',
...     rule_number=1,
... )

```

* `pattern` — a SymPy expression containing `WildSymbol`s.
* `constraints` — a tuple of guards over those wildcards, checked **after** the
  structure matches (§3).
* `replacement` — a SymPy expression over the same wildcards; the matched values are
  substituted into it.
* `module_name` / `rule_number` — a label; the replacer reports it with every firing,
  so results are traceable to the rule that produced them.

## 2. `build_replacer` and applying rules

`build_replacer` compiles a list of rules into a OmniMatch `ManyToOneReplacer` — one
discrimination net that matches all patterns simultaneously, which is what makes rule
sets of thousands of patterns practical (see "One matcher, all rules at once" in
[`../README.md`](../README.md) for the algorithm and a demonstration). Build it once
per rule set and reuse it; the compilation cost is meant to be amortised over many
subjects.

```python
>>> replacer = build_replacer([power_rule])
>>> result, fired = replacer.replace(to_omnimatch_expression(x**3))
>>> omnimatch_to_sympy(result)
x**4/4
>>> fired
('docs example', 1)

```

The replacer works on OmniMatch expressions; convert on the way in with
`to_omnimatch_expression` and back with `omnimatch_to_sympy`
(see [`conversion.md`](conversion.md)).

A guard rejection means *no match* — the expression comes back untouched rather than
rewritten into something invalid. Here `m = -1` matches structurally but would divide
by zero, and `Ne(m_, -1)` blocks it:

```python
>>> omnimatch_to_sympy(replacer.replace(to_omnimatch_expression(x**-1)))
1/x

```

## 3. Guards

### Bare SymPy Booleans

Any SymPy relational over the wildcards works as a guard. After the match, the bound
values are substituted in by **wildcard name** and the Boolean is evaluated; `Not`,
`And` and `Or` compose, and the combination is evaluated lazily (`Or` stops at the
first success, `And` at the first failure — so put cheap guards before expensive
ones).

```python
>>> from sympy import Gt, And
>>> b_ = WildSymbol('b')
>>> guarded = SymPyReplacementPattern(
...     pattern=b_*x,
...     constraints=(And(Ne(b_, 0), Gt(b_, 1)),),
...     replacement=b_,
...     module_name='docs example', rule_number=2,
... )
>>> rep = build_replacer([guarded])
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(5*x))[0])
5
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(-2*x)))   # Gt fails -> no match
-2*x

```

### `FreeOf` — "must not contain the variable"

The most common guard when rules revolve around a distinguished variable. It accepts
one variable or a group (all must be free), and names may be given as strings or as
the objects carrying them — the same argument shapes as higher-layer predicates built
on it:

```python
>>> from omnimatch.expressions.constraints import FreeOf
>>> a_ = WildSymbol('a')
>>> FreeOf('a', 'x').variables
frozenset({'a'})
>>> FreeOf([a_, b_], Symbol('x')).variables == frozenset({'a', 'b'})
True

```

`FreeOf` attaches to the OmniMatch `Pattern` (it is a OmniMatch-level constraint); inside a
`SymPyReplacementPattern` the same effect is usually obtained with a predicate-style
constraint from a higher layer, or a custom one (§4).

## 4. Custom constraints: `SymPyMatchingConstraint`

Subclass and implement `check(**bindings)`; the bound wildcards arrive as keyword
arguments named after their `wildcard_name`. The values come straight from the matcher
(so, inside a replacer, in OmniMatch form) — resolve them through the base-class helpers
`_resolve_all` (convert every binding to SymPy) and `_resolve` (look an argument up in
the resolved bindings), which every shipped constraint uses. `variables` is derived
automatically from the constraint's arguments.

```python
>>> from sympy_matching.constraint import SymPyMatchingConstraint
>>> class IsEven(SymPyMatchingConstraint):
...     """The bound expression must be an even integer."""
...     def check(self, **bindings):
...         value = self._resolve(self.args[0], self._resolve_all(bindings))
...         return bool(value.is_integer and value.is_even)
>>> IsEven(m_).variables
('m',)
>>> IsEven(m_).check(m=Symbol('q', integer=True, even=True))
True
>>> IsEven(m_).check(m=Symbol('q', integer=True, odd=True))
False

```

A `SymPyMatchingConstraint` derives from `sympy.logic.boolalg.Boolean`, so instances
are first-class SymPy nodes: they can sit inside `Not`/`And`/`Or`, be stored in rule
tuples, compare by `(type, args)`, and print readably.

```python
>>> from sympy import Not
>>> from sympy.logic.boolalg import Boolean
>>> isinstance(Not(IsEven(m_)), Boolean)
True

```

Used in a rule:

```python
>>> even_rule = SymPyReplacementPattern(
...     pattern=x**m_,
...     constraints=(IsEven(m_),),
...     replacement=Symbol('sq')**(m_/2),
...     module_name='docs example', rule_number=3,
... )
>>> rep = build_replacer([even_rule])
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(x**4))[0])
sq**2
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(x**3)))   # odd -> no match
x**3

```

## 5. Several rules, one replacer

All rules are compiled into a single matcher. Which rule fires for a given subject is
decided by matching, then by the guards:

```python
>>> s_ = WildSymbol('s')
>>> rules = [
...     SymPyReplacementPattern(pattern=sin(s_)**2 + cos(s_)**2, constraints=(),
...                             replacement=Symbol('one'),
...                             module_name='docs example', rule_number=4),
...     power_rule,
... ]
>>> rep = build_replacer(rules)
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(sin(x)**2 + cos(x)**2))[0])
one
>>> omnimatch_to_sympy(rep.replace(to_omnimatch_expression(x**5))[0])
x**6/6

```

## 6. Practical guidance

* **One name, one meaning.** All occurrences of a wildcard name in `pattern`,
  `constraints` and `replacement` refer to the same variable
  (see [`wildcards.md`](wildcards.md) §3).
* **Resolve bindings through the base class.** Inside a replacer, `check` receives
  OmniMatch-form values; `self._resolve_all` / `self._resolve` convert them to SymPy
  uniformly (and also make the constraint work when called directly with SymPy
  values, as in the doctests above).
* **Rejection is silent by design.** A failed guard is "no match", not an error — a
  rule set probes many rules per subject, and most are expected not to apply.
* **Order guards cheap-first.** Guards run per candidate match; an expensive predicate
  behind a cheap one is only paid for when the cheap one passes.
