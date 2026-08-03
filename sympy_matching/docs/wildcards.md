# Wildcards in depth: `WildSymbol`

This document covers everything about pattern leaves: the three kinds, the naming
convention, name-unification, per-slot optionality, defaults, ordering, and identity.
For the package overview see [`../README.md`](../README.md); for rules and constraints
see [`rules-and-constraints.md`](rules-and-constraints.md).

Every example is a doctest, executed by `sympy_matching/tests/test_docs.py`. Examples
use only `sympy`, `omnimatch` and `sympy_matching` — this package does not depend on any
higher layer.

```python
>>> from sympy import Symbol
>>> from omnimatch import ManyToOneMatcher, Pattern
>>> from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
>>> from sympy_matching.matching_rule import to_omnimatch_expression
>>> def matches(pattern, subject):
...     m = ManyToOneMatcher()
...     m.add(Pattern(to_omnimatch_expression(pattern)))
...     return bool(list(m.match(to_omnimatch_expression(subject))))
>>> x, W, y = Symbol('x'), Symbol('W'), Symbol('y')

```

---

## 1. The three kinds of leaf

| leaf | built with | matches |
|---|---|---|
| literal | `Symbol('d')` | only the symbol `d` itself |
| plain wildcard | `WildSymbol('d')` | any expression — must be present |
| optional wildcard | `WildSymbol('d', optional_value=...)` | any expression — or nothing, taking the default |

A `WildSymbol` **is** a `sympy.Symbol` subclass, so patterns are ordinary SymPy
expressions and can be built, printed, substituted and traversed with the usual tools:

```python
>>> d_ = WildSymbol('d')
>>> isinstance(d_, Symbol)
True
>>> expr = d_*x + 1
>>> expr.free_symbols == {d_, x}
True

```

The wildcard nature only takes effect at conversion time (`to_omnimatch_expression`),
when each `WildSymbol` becomes a OmniMatch wildcard.

## 2. Naming convention

A single trailing underscore in the SymPy name is stripped to obtain the OmniMatch
variable name, so `WildSymbol('d_')` and `WildSymbol('d')` denote the same variable.
The codebase convention is:

* `d_` — a **plain** wildcard: `WildSymbol('d_')` (or `WildSymbol('d')`)
* `_d_` — an **optional** wildcard: `WildSymbol('d_', optional_value=IDENTITY_ELEMENT)`

```python
>>> WildSymbol('d_').wildcard_name
'd'
>>> WildSymbol('d').wildcard_name
'd'
>>> WildSymbol('d_', optional_value=IDENTITY_ELEMENT).is_optional
True

```

## 3. Identity is the NAME — two objects, one variable

A `WildSymbol` converts to a OmniMatch wildcard **named after its `wildcard_name`**.
Two `WildSymbol` objects carrying the same name are one pattern variable, even though
they are distinct SymPy objects — and they *must* be distinct objects whenever they
differ in optionality (§4).

```python
>>> d_ = WildSymbol('d')
>>> _d_ = WildSymbol('d', optional_value=IDENTITY_ELEMENT)
>>> d_ == _d_          # distinct SymPy objects...
False
>>> d_.wildcard_name == _d_.wildcard_name    # ...one omnimatch variable
True

```

Consequently the two occurrences must bind consistently, with **no** explicit equality
constraint needed:

```python
>>> matches(d_ + _d_*W, 5 + 5*W)    # d = 5 in both slots
True
>>> matches(d_ + _d_*W, 2 + 3*W)    # 2 vs 3 -- inconsistent
False

```

The unification follows the name, not the expression shape — it holds at any nesting
depth:

```python
>>> from sympy import sin, sqrt
>>> matches(sin(d_) + _d_*W, sin(5) + 5*W)
True
>>> matches(sin(d_) + _d_*W, sin(2) + 3*W)
False
>>> matches(sqrt(d_) + _d_*W, sqrt(5) + 5*W)
True
>>> matches(d_*y + _d_*W, 2*y + 3*W)
False

```

Note that instances of the *same* kind are still distinct objects — identity is not
interned:

```python
>>> WildSymbol('a') == WildSymbol('a')
False

```

This instance-uniqueness is deliberate. Wildcard objects are the *carriers* of pattern
structure at rule-construction time; making same-named instances compare equal lets
SymPy collapse them while a pattern is being assembled, silently merging distinct
slots. (When that was once tried, regeneration of a large rule set lost 120 rules with
no error.) Unification happens later, in the matcher, by name.

## 4. Optionality belongs to the SLOT

Optionality describes the *position* a wildcard occupies, not the variable. One
variable may fill two slots, only one of which may be empty — which is exactly why the
plain and optional forms are distinct objects sharing a name.

`IDENTITY_ELEMENT` resolves the default from the enclosing operation at conversion
time:

| context | default |
|---|---|
| `Add` | 0 |
| `Mul` | 1 |
| `Pow` exponent | 1 |

```python
>>> a_ = WildSymbol('a')
>>> _a_ = WildSymbol('a', optional_value=IDENTITY_ELEMENT)
>>> matches(_a_ + W, W)     # a -> 0
True
>>> matches(_a_*W, W)       # a -> 1
True
>>> matches(W**_a_, W)      # a -> 1
True
>>> matches(a_ + W, W)      # plain: cannot be absent
False

```

A fixed default may be given instead of the context-dependent sentinel:

```python
>>> WildSymbol('a', optional_value=7).optional_value
7

```

### A default counts as a binding

When an optional slot is empty, its default participates in the consistency check like
any bound value:

```python
>>> d_ = WildSymbol('d')
>>> _d_ = WildSymbol('d', optional_value=IDENTITY_ELEMENT)
>>> matches(d_ + _d_*W, 5 + W)      # d=5 vs the implied 1 -- clash
False
>>> matches(d_ + _d_*W, 1 + W)      # 1 and the implied 1 agree
True
>>> matches(_d_ + _d_*W, W)         # both empty: Add default 0 vs Mul default 1
False
>>> matches(_d_ + _d_*W, 5 + 5*W)
True

```

## 5. Matching is structural

The matcher never solves equations for a wildcard. `d_**2` requires a `Pow` with
exponent 2; the integer 25 is not one:

```python
>>> matches(d_**2 + _d_*W, 25 + 5*W)
False
>>> matches(d_**2 + _d_*W, y**2 + y*W)
True

```

## 6. A literal is independent of a same-named wildcard

A literal `Symbol('d')` and a wildcard named `d` may coexist in one pattern without
interacting — the literal matches only itself, the wildcard binds its slot:

```python
>>> d = Symbol('d')
>>> matches(d + _d_*W, d + 5*W)     # literal matches d, wildcard binds 5
True
>>> matches(d + _d_*W, 5 + 5*W)     # the literal cannot match 5
False

```

## 7. Deterministic ordering

`WildSymbol.sort_key` appends an optionality tag so that a plain and an optional
wildcard of one name never tie. Without it, SymPy's stable sort falls back to
construction order, and the argument order of an `Add`/`Mul` holding both becomes an
artefact of how the expression was built — which makes any *printed* output (e.g.
generated source code) non-reproducible between runs.

```python
>>> d_ = WildSymbol('d')
>>> _d_ = WildSymbol('d', optional_value=IDENTITY_ELEMENT)
>>> d_.sort_key() == _d_.sort_key()
False
>>> (d_ + _d_*W).args == (_d_*W + d_).args      # order independent of construction
True

```
