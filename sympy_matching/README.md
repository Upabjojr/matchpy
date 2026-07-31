# `sympy_matching` — SymPy expressions as MatchPy patterns

This package lets you write MatchPy patterns using ordinary SymPy syntax, and it is
where Mathematica's pattern semantics are reproduced. Every example below is a doctest
and is executed by `sympy_matching/tests/test_readme.py`.

The single most important thing to understand is how the three Mathematica pattern
forms map onto SymPy objects, and how two *different* SymPy objects can be *one*
pattern variable. That is the subject of most of this document.

---

## 1. The three forms, and what each becomes

Mathematica has three things that all print as the letter `d`:

| Mathematica | `FullForm` | meaning | here |
|---|---|---|---|
| `d` | `d` | a **literal symbol** | `Symbol('d')` |
| `d_` | `Pattern[d, Blank[]]` | a **plain Blank** — must be present | `WildSymbol('d')` |
| `d_.` | `Optional[Pattern[d, Blank[]]]` | an **Optional Blank** — may be absent | `WildSymbol('d', optional_value=IDENTITY_ELEMENT)` |

Note what `FullForm` reveals: `Optional` *wraps* `Pattern[d, Blank[]]`. **Optionality is
a property of the slot, not of the variable.** `d_` and `d_.` are the *same* variable
`d`, used in two places with different rules about whether that place may be empty.

```python
>>> from sympy import Symbol
>>> from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
>>> d_ = WildSymbol('d')                                     # Mathematica  d_
>>> _d_ = WildSymbol('d', optional_value=IDENTITY_ELEMENT)   # Mathematica  d_.
>>> d_.wildcard_name, _d_.wildcard_name
('d', 'd')
>>> d_.is_optional, _d_.is_optional
(False, True)

```

A trailing underscore in the SymPy name is stripped when deriving the MatchPy variable
name, so `WildSymbol('d_')` and `WildSymbol('d')` describe the same variable:

```python
>>> WildSymbol('d_').wildcard_name
'd'

```

---

## 2. `d_` and `d_.` are ONE variable — unified by NAME

This is the part that surprises people. `d_` and `_d_` are **distinct SymPy objects**
(they must be — they carry different optionality), yet they are **one pattern
variable**, because a `WildSymbol` converts to a MatchPy wildcard named after its
`wildcard_name`. Both carry the name `'d'`, so MatchPy binds them together.

You do **not** need an explicit `Eq(d_, _d_)` constraint to hold the two slots
together; the shared name already does it.

```python
>>> d_ == _d_                    # different SymPy objects...
False
>>> d_.wildcard_name == _d_.wildcard_name    # ...but ONE matchpy variable
True

```

The helper used throughout this document:

```python
>>> from matchpy import ManyToOneMatcher, Pattern
>>> from sympy_matching.matching_rule import to_matchpy_expression
>>> from rubi_rules.base_objects import Int
>>> x = Symbol('x')
>>> def matches(pattern, subject):
...     m = ManyToOneMatcher()
...     m.add(Pattern(to_matchpy_expression(Int(pattern, x))))
...     return bool(list(m.match(to_matchpy_expression(Int(subject, x)))))

```

Both occurrences must agree, exactly as in Mathematica
(`MatchQ[5 + 5 W, d_ + d_.*W]` is `True`, `MatchQ[2 + 3 W, ...]` is `False`):

```python
>>> W = Symbol('W')
>>> matches(d_ + _d_*W, 5 + 5*W)      # d = 5 in both slots
True
>>> matches(d_ + _d_*W, 2 + 3*W)      # 2 vs 3 -- inconsistent
False

```

The unification is a property of the **name**, not of a particular expression shape, so
it holds however deeply the two slots are nested:

```python
>>> from sympy import sin, sqrt
>>> y = Symbol('y')
>>> matches(sin(d_) + _d_*W, sin(5) + 5*W)
True
>>> matches(sin(d_) + _d_*W, sin(2) + 3*W)
False
>>> matches(sqrt(d_) + _d_*W, sqrt(5) + 5*W)
True
>>> matches(d_*y + _d_*W, 2*y + 3*W)
False

```

---

## 3. An absent Optional slot takes the enclosing operation's identity

`IDENTITY_ELEMENT` means "when this slot is missing, use the identity of whatever
operation encloses it" — `0` for `Add`, `1` for `Mul`, `1` for a `Pow` exponent. This
mirrors Mathematica's `Default[Plus]`/`Default[Times]`/`Default[Power]`.

```python
>>> a_ = WildSymbol('a')
>>> _a_ = WildSymbol('a', optional_value=IDENTITY_ELEMENT)
>>> matches(_a_ + W, W)        # a -> 0, the Add identity
True
>>> matches(_a_*W, W)          # a -> 1, the Mul identity
True
>>> matches(W**_a_, W)         # a -> 1, the Pow identity
True

```

A **plain** Blank has no default and therefore cannot be absent:

```python
>>> matches(a_ + W, W)
False
>>> matches(a_*W, W)
False

```

### The default participates in the consistency check

This is the subtle consequence of §2 and §3 together, and the case most likely to catch
you out. In `d_ + d_.*W` matched against `5 + W`:

* the `d_` slot binds `d = 5`;
* the `d_.` slot is **absent** (there is no coefficient on `W`), so it supplies the
  `Mul` identity, i.e. `d = 1`;
* `d` cannot be both 5 and 1, so there is **no match**.

```python
>>> matches(d_ + _d_*W, 5 + W)     # 5 vs the implied 1
False
>>> matches(d_ + _d_*W, 1 + W)     # 1 and the implied 1 agree
True

```

And when *both* slots are optional, their two defaults must agree with each other —
`0` from the `Add` and `1` from the `Mul` cannot, so nothing matches:

```python
>>> matches(_d_ + _d_*W, W)        # 0 vs 1
False
>>> matches(_d_ + _d_*W, 3*W)      # 0 vs 3
False
>>> matches(_d_ + _d_*W, 5 + 5*W)  # both bind 5
True

```

---

## 4. A literal symbol is independent of a same-named wildcard

Inside one pattern, the same *name* can be both a literal symbol and a pattern
variable, and Mathematica keeps them **independent**: the literal matches itself while
the variable binds whatever is in its slot.

```python
>>> d = Symbol('d')                       # the LITERAL symbol
>>> matches(d + _d_*W, d + d*W)           # literal matches d, variable binds d
True
>>> matches(d + _d_*W, 5 + 5*W)           # the literal cannot match 5
False
>>> matches(d + _d_*W, d + 5*W)           # literal matches d, variable binds 5
True

```

That last line is the one worth remembering: `d + 5*W` **does** match `d + d_.*W`.

---

## 5. Matching never solves for a wildcard

Pattern matching is structural. `d_**2` matches an expression whose head is `Pow` with
exponent 2 — it does not solve `d**2 == 25`:

```python
>>> matches(d_**2 + _d_*W, 25 + 5*W)      # 25 is an Integer, not a Pow
False
>>> matches(d_**2 + _d_*W, y**2 + y*W)    # a symbolic square does match
True

```

---

## 6. Distinct names bind independently

Nothing above applies across *different* names — `c` and `d` are unrelated:

```python
>>> c_ = WildSymbol('c')
>>> matches(c_ + _d_*W, 2 + 3*W)
True

```

---

## 7. Putting a rule together

A `SymPyReplacementPattern` bundles a pattern, its constraints and its replacement.
Constraints are ordinary SymPy Booleans (or `SymPyMatchingConstraint`s) over the
wildcards.

```python
>>> from sympy_matching.matching_rule import SymPyReplacementPattern, build_replacer
>>> from sympy_matching.matching_rule import to_matchpy_expression
>>> m_ = WildSymbol('m')
>>> rule = SymPyReplacementPattern(
...     pattern=Int(x**m_, x),
...     constraints=(),
...     replacement=x**(m_ + 1)/(m_ + 1),
...     module_name='doc example',
...     rule_number=1,
... )
>>> replacer = build_replacer([rule])
>>> expr = to_matchpy_expression(Int(x**3, x))
>>> len(list(replacer.matcher.match(expr)))
1

```

---

## Why not just add an `Eq(d_, _d_)` constraint?

It would work — and give identical results — but it is redundant: the shared
`wildcard_name` already unifies the two slots (§2), as the nesting examples show. An
explicit constraint would be evaluated on every match attempt, and constraint
evaluation dominates runtime in the Rubi rule set. It would also force the code
generator to invent distinct names (`d1`, `d2`), making generated rules harder to diff
against Rubi's Mathematica source.

## See also

* `sympy_wolfram/README.md` — how Wolfram `FullForm` is translated *into* these objects,
  including why a bare atom inside a pattern must stay a literal `Symbol`.
* `sympy_wolfram/tests/test_blank_optional_semantics.py` — the same semantics pinned
  against values read directly off Mathematica.
