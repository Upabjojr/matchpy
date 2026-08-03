# Conversion: SymPy ⇄ OmniMatch

How expressions cross between the two worlds: `to_omnimatch_expression` /
`omnimatch_to_sympy`, the head registry (`SYMPY_NODES`, `register_sympy_head`), and how
to add support for a new function class. See also [`wildcards.md`](wildcards.md) for
what happens to `WildSymbol`s during conversion.

Every example is a doctest, executed by `sympy_matching/tests/test_docs.py`.

```python
>>> from sympy import Symbol, Function, sin
>>> from sympy_matching.matching_rule import to_omnimatch_expression
>>> from sympy_matching.conversion import omnimatch_to_sympy
>>> x = Symbol('x')

```

---

## 1. The round trip

`to_omnimatch_expression` maps a SymPy tree onto OmniMatch `Operation`s; `omnimatch_to_sympy`
maps back. The pair is a faithful round trip for every registered head:

```python
>>> e = sin(x)**2 + 3*x
>>> mp = to_omnimatch_expression(e)
>>> print(mp)
Add(Mul(3, x), Pow(sin(x), 2))
>>> omnimatch_to_sympy(mp) == e
True

```

`Add`, `Mul` and `Pow` are special: their OmniMatch heads carry the algebraic properties
the matcher exploits — `Add`/`Mul` are commutative, associative and `one_identity`,
which is what makes commutative matching and the optional-wildcard defaults of
[`wildcards.md`](wildcards.md) §4 work.

Plain symbols convert to constants; `WildSymbol`s convert to wildcards (that is the
whole difference between a subject and a pattern — the conversion function is the
same).

## 2. The head registry

Supported function classes live in one master table, `SYMPY_NODES` in
`operations.py` — `(module_path, class_name, arity_code)` triples. At import time
`register_all_heads()` walks the table, builds an `OperationHead` per entry, and
registers the bidirectional mapping in `SYMPY_FUNC_TO_HEAD` / `HEAD_TO_SYMPY_FUNC`:

```python
>>> import sympy
>>> from sympy_matching.operations import SYMPY_FUNC_TO_HEAD, HEAD_TO_SYMPY_FUNC
>>> SYMPY_FUNC_TO_HEAD[sympy.sin].name
'sin'
>>> HEAD_TO_SYMPY_FUNC[SYMPY_FUNC_TO_HEAD[sympy.sin]] is sympy.sin
True

```

Entries whose class does not exist in the installed SymPy version are skipped, so the
table can list classes across SymPy versions.

One easy-to-miss registered head: `sympy.Tuple`. It is a container, not a function —
but `Derivative` stores its `(variable, order)` spec as one, and without a registered
head it would round-trip as an *undefined function* named `Tuple`, silently breaking
every expression containing a derivative.

## 3. Undefined functions round-trip generically

An `UndefinedFunction` (from `sympy.Function('name')`) needs no registration — a
generic path preserves it by name:

```python
>>> f = Function('myfunc')
>>> omnimatch_to_sympy(to_omnimatch_expression(f(x))) == f(x)
True

```

This is the right behaviour for opaque markers, but note the limitation: the returned
class is *reconstructed by name*, so behaviour attached to a custom `Function`
**subclass** (evaluation, assumptions, printing) does not survive the trip. For those,
register a head (§4).

## 4. Registering a new head

Adding support for a custom function class takes one `OperationHead` and one
registration call. **Do this via `register_sympy_head` / the `SYMPY_NODES` table — not
ad hoc** — so both directions of the mapping stay consistent:

```python
>>> from omnimatch.expressions.expressions import OperationHead, Arity
>>> from sympy_matching.operations import register_sympy_head
>>> class mystep(Function):
...     nargs = 1
>>> MYSTEP = OperationHead(name='mystep', arity=Arity.unary)
>>> register_sympy_head(mystep, MYSTEP)
>>> mp = to_omnimatch_expression(mystep(x**2))
>>> print(mp)
mystep(Pow(x, 2))
>>> omnimatch_to_sympy(mp).func is mystep     # the CLASS survives, not just the name
True

```

Patterns over the new head work immediately:

```python
>>> from omnimatch import ManyToOneMatcher, Pattern
>>> from sympy_matching.wild import WildSymbol
>>> u_ = WildSymbol('u')
>>> m = ManyToOneMatcher()
>>> m.add(Pattern(to_omnimatch_expression(mystep(u_))))
>>> bool(list(m.match(mp)))
True

```

For a class that ships with the package, prefer adding a `SYMPY_NODES` row over an
imperative `register_sympy_head` call — the table is the single place readers look to
see what is supported.

Arity codes in the table: `'u'` unary, `'b'` binary, and so on; the registration loop
translates them to OmniMatch `Arity` values.

## 5. Layering note

This package depends only on `sympy` and `omnimatch`. Higher layers (such as a Wolfram
translation layer) register their own heads through exactly the mechanism in §4 — the
registry is the extension point; nothing here knows about them.
