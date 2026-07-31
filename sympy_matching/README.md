# `sympy_matching` — SymPy expressions as MatchPy patterns

Write MatchPy patterns using ordinary SymPy syntax. A `WildSymbol` behaves like a normal
`Symbol` inside a SymPy tree, and becomes a MatchPy wildcard on conversion — so patterns
can be built, manipulated and printed with the usual SymPy machinery.

This package has no dependency on any computer-algebra dialect; for how Wolfram
`FullForm` is translated *into* these objects, see `sympy_wolfram/README.md`.

Every example below is a doctest, executed by `sympy_matching/tests/test_readme.py`.

---

## 1. Three kinds of leaf

A pattern leaf is one of three things:

| leaf | built with | meaning |
|---|---|---|
| **literal** | `Symbol('d')` | matches only itself |
| **plain wildcard** | `WildSymbol('d')` | must be present; binds whatever fills it |
| **optional wildcard** | `WildSymbol('d', optional_value=...)` | may be absent; then takes its default |

```python
>>> from sympy import Symbol
>>> from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT
>>> d_ = WildSymbol('d')                                     # plain
>>> _d_ = WildSymbol('d', optional_value=IDENTITY_ELEMENT)   # optional
>>> d_.wildcard_name, _d_.wildcard_name
('d', 'd')
>>> d_.is_optional, _d_.is_optional
(False, True)

```

Naming convention: a trailing underscore in the SymPy name is stripped when deriving the
MatchPy variable name, so `WildSymbol('d_')` and `WildSymbol('d')` are the same variable.
The codebase writes plain wildcards as `d_` and optional ones as `_d_`.

```python
>>> WildSymbol('d_').wildcard_name
'd'

```

---

## 2. The wildcard's identity is its NAME

**This is the key idea of the package.** A `WildSymbol` converts to a MatchPy wildcard
named after its `wildcard_name`. Two `WildSymbol` objects carrying the same name are
therefore *one pattern variable*, even when they are different SymPy objects — which
they must be when they differ in optionality.

```python
>>> d_ == _d_                                 # different SymPy objects...
False
>>> d_.wildcard_name == _d_.wildcard_name     # ...one matchpy variable
True

```

So a plain and an optional wildcard of the same name are held together automatically.
No explicit `Eq(d_, _d_)` constraint is needed.

The helper used below:

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

Both occurrences must bind the same value:

```python
>>> W = Symbol('W')
>>> matches(d_ + _d_*W, 5 + 5*W)      # d = 5 in both slots
True
>>> matches(d_ + _d_*W, 2 + 3*W)      # 2 vs 3 -- inconsistent
False

```

Because the unification follows the *name*, it is not tied to one expression shape. It
holds however the two occurrences are nested:

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

## 3. Optionality belongs to the SLOT

Optionality describes *the position a wildcard occupies*, not the variable. The same
variable can appear in one slot that may be empty and another that may not — which is
why the plain and optional forms have to be distinct SymPy objects while sharing a name.

`IDENTITY_ELEMENT` means "if this slot is empty, use the identity of the enclosing
operation": `0` for `Add`, `1` for `Mul`, `1` for a `Pow` exponent.

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

A plain wildcard has no default and so cannot be absent:

```python
>>> matches(a_ + W, W)
False
>>> matches(a_*W, W)
False

```

A fixed default can be given instead of the context-dependent one:

```python
>>> WildSymbol('a', optional_value=7).optional_value
7

```

### A default counts as a binding

Sections 2 and 3 combine into the case most likely to catch you out. Matching
`d_ + _d_*W` against `5 + W`:

* the plain slot binds `d = 5`;
* the optional slot is **empty** — there is no coefficient on `W` — so it supplies the
  `Mul` identity, i.e. `d = 1`;
* one variable cannot be both, so there is **no match**.

```python
>>> matches(d_ + _d_*W, 5 + W)     # 5 vs the implied 1
False
>>> matches(d_ + _d_*W, 1 + W)     # 1 and the implied 1 agree
True

```

When *both* slots are optional their two defaults must agree with each other, and `0`
from the `Add` cannot equal `1` from the `Mul`:

```python
>>> matches(_d_ + _d_*W, W)        # 0 vs 1
False
>>> matches(_d_ + _d_*W, 3*W)      # 0 vs 3
False
>>> matches(_d_ + _d_*W, 5 + 5*W)  # both bind 5
True

```

---

## 4. A literal is independent of a same-named wildcard

A literal `Symbol` and a wildcard of the same name can coexist in one pattern. They do
not interact: the literal matches itself, the wildcard binds whatever is in its slot.

```python
>>> d = Symbol('d')                       # the literal
>>> matches(d + _d_*W, d + d*W)           # literal matches d, wildcard binds d
True
>>> matches(d + _d_*W, 5 + 5*W)           # the literal cannot match 5
False
>>> matches(d + _d_*W, d + 5*W)           # literal matches d, wildcard binds 5
True

```

That last line is the one to remember: `d + 5*W` **does** match `d + _d_*W`.

---

## 5. Matching is structural — it never solves for a wildcard

`d_**2` matches an expression whose head is `Pow` with exponent 2. It does not solve
`d**2 == 25`:

```python
>>> matches(d_**2 + _d_*W, 25 + 5*W)      # 25 is an Integer, not a Pow
False
>>> matches(d_**2 + _d_*W, y**2 + y*W)    # a symbolic square does match
True

```

---

## 6. Different names are independent

Nothing above crosses name boundaries:

```python
>>> c_ = WildSymbol('c')
>>> matches(c_ + _d_*W, 2 + 3*W)
True

```

---

## 7. Constraints: `FreeOf` and friends

Structure alone is often not enough. A pattern such as `a_*x + b_` matches almost
anything unless you also demand that `a` and `b` do not themselves involve `x` — the
difference between "a linear expression in x" and "any sum whatsoever". Constraints are
predicates evaluated **after** the structure matches and the wildcards are bound; if one
fails, that match is rejected and the matcher moves on.

### `FreeOf` — the bound expression must not contain a symbol

`FreeOf(variables, symbol)` succeeds when none of the expressions bound to `variables`
contains an atom of that name anywhere in its tree. It is the constraint you reach for
constantly when writing rules over a distinguished variable.

```python
>>> from matchpy import Pattern, is_match, Wildcard, Operation, Arity, NamedAtom
>>> from matchpy.expressions.constraints import FreeOf
>>> f = Operation.new('f', Arity.binary)
>>> x_, y_ = Wildcard.dot('x'), Wildcard.dot('y')
>>> pattern = Pattern(f(x_, y_), FreeOf('y', 'x'))       # y must not contain 'x'
>>> is_match(f(NamedAtom('x'), NamedAtom('a')), pattern)
True
>>> is_match(f(NamedAtom('x'), NamedAtom('x')), pattern)
False

```

### Argument shapes

A **group** of variables can be given at once; the constraint holds only if *every*
member is free of the symbol, so one grouped constraint is equivalent to several
single ones:

```python
>>> both = Pattern(f(x_, y_), FreeOf(['x', 'y'], 'z'))
>>> is_match(f(NamedAtom('a'), NamedAtom('b')), both)
True
>>> is_match(f(NamedAtom('a'), NamedAtom('z')), both)     # y contains z
False

```

Names may be given as bare strings, or as the objects that carry them — a wildcard
(via `wildcard_name`) or a symbol (via `name`) can be passed directly, so you need not
hand-write the string form:

```python
>>> a_, b_ = WildSymbol('a'), WildSymbol('b')
>>> FreeOf([a_, b_], Symbol('x'))
FreeOf(('a', 'b'), 'x')
>>> FreeOf([a_, b_], Symbol('x')).variables == frozenset({'a', 'b'})
True

```

These are the same shapes a higher-layer predicate such as `sympy_wolfram`'s `FreeQ`
accepts, so the two are interchangeable at the call site.

`FreeOf` is a dedicated constraint rather than a lambda: it traverses iteratively with
an early exit, avoids closure indirection, and has a readable `repr`, which matters when
a rule set holds thousands of them.

```python
>>> FreeOf('y', 'x').variables
frozenset({'y'})

```

### Constraints on a SymPy-side rule

In a `SymPyReplacementPattern` the guards are ordinary SymPy `Boolean`s over the
wildcards. Below, the power rule must not fire for `m = -1`, where the antiderivative is
a logarithm and `x**(m+1)/(m+1)` would divide by zero:

```python
>>> from sympy import Ne
>>> from sympy_matching.matching_rule import SymPyReplacementPattern, build_replacer
>>> from sympy_matching.conversion import matchpy_to_sympy
>>> m_ = WildSymbol('m')
>>> power_rule = SymPyReplacementPattern(
...     pattern=Int(x**m_, x),
...     constraints=(Ne(m_, -1),),
...     replacement=x**(m_ + 1)/(m_ + 1),
...     module_name='doc example',
...     rule_number=1,
... )
>>> replacer = build_replacer([power_rule])
>>> rewritten, fired = replacer.replace(to_matchpy_expression(Int(x**3, x)))
>>> matchpy_to_sympy(rewritten)
x**4/4
>>> fired
('doc example', 1)

```

The guard genuinely blocks the excluded case — with `m = -1` the structure still
matches, but the constraint rejects it, so the integral comes back untouched instead of
being rewritten to a division by zero:

```python
>>> matchpy_to_sympy(replacer.replace(to_matchpy_expression(Int(x**-1, x))))
Int(1/x, x)

```

### Writing your own

Subclass `SymPyMatchingConstraint` and implement `check`, which receives the bound
wildcards as keyword arguments named after their `wildcard_name` (§2) and returns a
bool. `variables` is derived automatically from the constraint's arguments.

```python
>>> from sympy_matching.constraint import SymPyMatchingConstraint
>>> class IsEven(SymPyMatchingConstraint):
...     """The bound expression must be an even integer."""
...     def check(self, **bindings):
...         value = bindings[self.args[0].wildcard_name]
...         return value.is_integer and value.is_even
>>> IsEven(m_).variables
('m',)
>>> IsEven(m_).check(m=Symbol('q', integer=True, even=True))
True
>>> IsEven(m_).check(m=Symbol('q', integer=True, odd=True))
False

```

Because these constraints subclass SymPy's `Boolean`, they compose with the logic
operators, and the rule machinery evaluates the combination lazily — `Or` stops at the
first success, `And` at the first failure — so an expensive guard placed after a cheap
one is only reached when the cheap one passes:

```python
>>> from sympy import And, Not
>>> from sympy.logic.boolalg import Boolean
>>> isinstance(Not(IsEven(m_)), Boolean)
True
>>> isinstance(And(Ne(m_, -1), IsEven(m_)), Boolean)
True

```

Dialect-specific predicate families are built on this base rather than added here — for
example `sympy_wolfram` supplies a Wolfram-named `FreeQ` over the same idea.

---

## 8. Assembling a rule

`SymPyReplacementPattern` bundles a pattern, its constraints and its replacement;
`build_replacer` compiles a list of them into a MatchPy `ManyToOneReplacer`. Constraints
are ordinary SymPy Booleans (or `SymPyMatchingConstraint`s) over the wildcards.

```python
>>> from sympy_matching.matching_rule import SymPyReplacementPattern, build_replacer
>>> m_ = WildSymbol('m')
>>> rule = SymPyReplacementPattern(
...     pattern=Int(x**m_, x),
...     constraints=(),
...     replacement=x**(m_ + 1)/(m_ + 1),
...     module_name='doc example',
...     rule_number=1,
... )
>>> replacer = build_replacer([rule])
>>> len(list(replacer.matcher.match(to_matchpy_expression(Int(x**3, x)))))
1

```

---

## Why not an explicit `Eq(d_, _d_)` constraint?

It would work and give identical results, but it is redundant: the shared
`wildcard_name` already unifies the slots (§2), including in the nested shapes above. An
explicit constraint would be evaluated on every match attempt — constraint evaluation
dominates runtime on large rule sets — and would force generated patterns to use
distinct names such as `d1`/`d2`, which obscures the fact that they are one variable.

## See also

* `sympy_wolfram/README.md` — translating Wolfram `FullForm` into these objects, and the
  dialect-specific semantics behind the defaults used here.
