# -*- coding: utf-8 -*-
"""Common Mathematica control/scoping constructs as SymPy expressions.

These classes model a small but useful subset of Mathematica semantics while
remaining fully symbolic until ``doit()`` is called, following SymPy
conventions for deferred evaluation.

All classes inherit from ``MathematicaExpr(Expr)`` and are fully symbolic
objects — they participate in SymPy expression trees and can be pattern-matched
or substituted into.  Evaluation is always explicit and on-demand via
``.doit()``.

Quick start
-----------
Local constants (simultaneous substitution)::

    >>> x, y = Symbol('x'), Symbol('y')
    >>> With(List(Set(x, Integer(2)), Set(y, Integer(3))), x**2 + y).doit()
    7

Lexical scoping with a computed local::

    >>> n = Symbol('n')
    >>> Module(List(Set(n, Integer(4))), n*(n + Integer(1))).doit()
    20

Conditional evaluation::

    >>> If(S.true, Integer(100), Integer(0)).doit()
    100

Iteration with value collection::

    >>> i = Symbol('i')
    >>> result = Reap(Do(Sow(i**2), List(i, Integer(4)))).doit()
    >>> list(result.args[1].args[0].args)
    [1, 4, 9, 16]

Non-local exit::

    >>> Catch(CompoundExpression(Throw(Integer(42)), Integer(0))).doit()
    42

Doctest configuration
---------------------
All examples below run with ``pytest --doctest-modules``.
"""
from __future__ import annotations
from __future__ import annotations

from itertools import count
from typing import Any, Iterable, Iterator

import sympy
from sympy import Add, Expr, Integer, Mul, Pow, Rational, S, Symbol
from sympy.core.sympify import sympify
from sympy.logic.boolalg import BooleanFalse, BooleanTrue


Null = Symbol('Null')
"""Sentinel returned by procedural constructs that produce no value.

Equivalent to Mathematica's ``Null``.  Represented as ``Symbol('Null')`` so
it participates naturally in SymPy expression trees.

Examples
--------
>>> Do(Integer(0), List(Integer(0))).doit() == Null
True
>>> If(S.false, Integer(1)).doit() == Null
True
"""

_MODULE_COUNTER = count(1)
_SOW_STACK: list[list[tuple[Any, Any]]] = []


class _ReturnSignal(Exception):
    """Internal signal raised by Return.doit() to unwind the call stack."""
    def __init__(self, value):
        self.value = value
        super().__init__(repr(value))


class _ThrowSignal(Exception):
    """Internal signal raised by Throw.doit() to unwind to an enclosing Catch."""
    def __init__(self, value, tag=None):
        self.value = value
        self.tag = tag
        super().__init__(repr((value, tag)))


class MathematicaExpr(Expr):
    """Abstract base class for all Mathematica-inspired SymPy expressions.

    Subclasses are fully symbolic SymPy ``Expr`` objects.  They are created
    unevaluated and evaluated on demand by calling ``.doit()``.

    Evaluation protocol
    -------------------
    ``doit(deep=True)`` (the default) first recursively calls ``.doit()`` on
    every argument, then calls ``_evaluate(**kwargs)`` on the resulting
    instance.  With ``deep=False`` the existing args are used as-is.

    Subclasses that need to control the evaluation order (e.g. ``With``,
    which must *not* evaluate the body before substituting local bindings)
    override ``doit()`` directly.

    Examples
    --------
    >>> isinstance(With(List(), Integer(1)), MathematicaExpr)
    True
    >>> isinstance(With(List(), Integer(1)), Expr)
    True
    >>> With(List(), Integer(1)).doit()
    1
    """

    def doit(self, **kwargs):
        deep = kwargs.get('deep', True)
        if deep:
            new_args = [
                arg.doit(**kwargs) if hasattr(arg, 'doit') else arg
                for arg in self.args
            ]
            instance = Expr.__new__(self.__class__, *new_args)
        else:
            instance = self
        return instance._evaluate(**kwargs)

    def _evaluate(self, **kwargs):
        raise NotImplementedError


class Set(MathematicaExpr):
    """Mathematica ``Set[symbol, expr]`` — a name/value binding marker.

    ``Set`` is a *structural* node, not a reducible expression.  It is used
    exclusively inside ``List(...)`` passed to ``With``, ``Module``, or
    ``Block`` to associate a local name with its initial value.
    ``doit()`` returns ``self`` unchanged; the enclosing scoping construct
    is responsible for interpreting the binding.

    Parameters
    ----------
    symbol : sympy.Symbol
        The local variable name.
    expr : sympy.Expr
        The value to bind to *symbol*.

    Examples
    --------
    >>> x = Symbol('x')
    >>> b = Set(x, Integer(5))
    >>> b.args == (x, Integer(5))
    True
    >>> b.doit() == b          # structural marker, stays unevaluated
    True

    Used inside ``With``::

    >>> With(List(Set(x, Integer(5))), x + Integer(1)).doit()
    6
    """

    def __new__(cls, symbol, expr):
        return Expr.__new__(cls, sympify(symbol), sympify(expr))

    def _evaluate(self, **kwargs):
        return self


class List(MathematicaExpr):
    """Mathematica ``List[e1, e2, …]`` — an ordered container of expressions.

    ``List`` is the primary container passed to scoping constructs
    (``With``, ``Module``, ``Block``) and to ``Do`` / ``Scan`` as the
    expression to iterate over.

    ``doit()`` returns ``self`` unchanged; ``List`` is a container, not a
    computation.  Items are accessible via ``args`` or iteration.

    Parameters
    ----------
    *items : sympy.Basic
        Zero or more SymPy-compatible elements.

    Examples
    --------
    >>> lst = List(Integer(1), Integer(2), Integer(3))
    >>> lst.args
    (1, 2, 3)
    >>> list(lst)          # supports iteration
    [1, 2, 3]
    >>> lst.doit() == lst  # container, not evaluated
    True
    >>> List().args        # empty list is allowed
    ()
    """

    def __new__(cls, *items):
        return Expr.__new__(cls, *[sympify(item) for item in items])

    def _evaluate(self, **kwargs):
        return self

    def __iter__(self) -> Iterator[Any]:
        yield from self.args


class CompoundExpression(MathematicaExpr):
    """Mathematica ``CompoundExpression[e1, e2, …]`` (semicolon operator).

    Evaluates each argument in order and returns the value of the last one.
    Equivalent to Mathematica's ``e1; e2; …; en``.  Intermediate values are
    discarded.  An empty ``CompoundExpression`` returns ``Null``.

    Parameters
    ----------
    *exprs : sympy.Basic
        Expressions to evaluate in sequence.

    Examples
    --------
    Basic sequential evaluation::

    >>> CompoundExpression(Integer(1), Integer(2), Integer(3)).doit()
    3

    Empty form returns ``Null``::

    >>> CompoundExpression().doit() == Null
    True

    Useful for grouping side effects inside ``Reap``::

    >>> result = Reap(CompoundExpression(Sow(Integer(10)), Sow(Integer(20)))).doit()
    >>> list(result.args[1].args[0].args)
    [10, 20]
    """

    def __new__(cls, *exprs):
        return Expr.__new__(cls, *[sympify(expr) for expr in exprs])

    def doit(self, **kwargs):
        result = Null
        for expr in self.args:
            result = _eval(expr, **kwargs)
        return result

    def _evaluate(self, **kwargs):
        return self


class If(MathematicaExpr):
    """Mathematica ``If[condition, t]`` / ``If[condition, t, f]`` /
    ``If[condition, t, f, u]``.

    Evaluates *condition* and branches accordingly.

    * 2-arg form ``If[cond, t]``: returns *t* if *cond* is ``True``,
      otherwise ``Null``.
    * 3-arg form ``If[cond, t, f]``: returns *t* or *f* depending on *cond*.
    * 4-arg form ``If[cond, t, f, u]``: returns *u* when the condition
      is neither ``True`` nor ``False`` (symbolic / indeterminate).

    When the condition is symbolic and no 4-arg unknown branch is given,
    the expression remains unevaluated (returns a new ``If`` node with
    the evaluated condition).

    Parameters
    ----------
    condition : sympy.Basic
        Boolean test.  Compared against ``S.true`` / ``S.false``.
    true_value : sympy.Basic
        Result when *condition* is ``True``.
    false_value : sympy.Basic, optional
        Result when *condition* is ``False`` (default: ``Null``).
    unknown_value : sympy.Basic, optional
        Result when *condition* is neither ``True`` nor ``False``.

    Examples
    --------
    Two-argument form::

    >>> If(S.true, Integer(42)).doit()
    42
    >>> If(S.false, Integer(42)).doit() == Null
    True

    Three-argument form::

    >>> If(S.true, Integer(1), Integer(0)).doit()
    1
    >>> If(S.false, Integer(1), Integer(0)).doit()
    0

    Stays unevaluated when condition is symbolic (no unknown branch)::

    >>> x = Symbol('x')
    >>> result = If(sympy.Gt(x, Integer(0)), Integer(1), Integer(-1)).doit()
    >>> isinstance(result, If)
    True

    Four-argument form returns the unknown branch for symbolic conditions::

    >>> If(sympy.Gt(x, Integer(0)), Integer(1), Integer(-1), Integer(0)).doit()
    0

    Inside a ``With``, the condition resolves to a concrete boolean::

    >>> With(List(Set(x, Integer(5))),
    ...      If(sympy.Gt(x, Integer(3)), Integer(100), Integer(0))).doit()
    100
    """

    def __new__(cls, condition, true_value, false_value=None, unknown_value=None):
        args = [sympify(condition), sympify(true_value)]
        if false_value is not None:
            args.append(sympify(false_value))
        if unknown_value is not None:
            args.append(sympify(unknown_value))
        return Expr.__new__(cls, *args)

    def doit(self, **kwargs):
        cond = _eval(self.args[0], **kwargs)
        if _is_true(cond):
            return _eval(self.args[1], **kwargs)
        if _is_false(cond):
            if len(self.args) >= 3:
                return _eval(self.args[2], **kwargs)
            return Null
        if len(self.args) >= 4:
            return _eval(self.args[3], **kwargs)
        return Expr.__new__(self.__class__, cond, *self.args[1:])

    def _evaluate(self, **kwargs):
        return self


class With(MathematicaExpr):
    """Mathematica ``With[{x=v, …}, body]`` — simultaneous local constants.

    ``With`` introduces local *constants*: all right-hand-side values are
    evaluated first (outside the body), then all variables are replaced
    simultaneously inside *body*, and finally the resulting expression is
    evaluated.  No variable can refer to another binding in the same ``With``.

    ``doit()`` is overridden to prevent *body* from being evaluated before
    substitution — the default ``MathematicaExpr.doit()`` would deep-evaluate
    all args first, which would reduce the body before local names are bound.

    If the body executes a ``Return[v]``, the value *v* is returned
    immediately and the remaining body is discarded.

    Parameters
    ----------
    bindings : List
        A ``List`` of ``Set(symbol, value)`` nodes.
    body : sympy.Expr
        The expression to evaluate after substitution.

    Examples
    --------
    Single binding::

    >>> x = Symbol('x')
    >>> With(List(Set(x, Integer(5))), x + Integer(1)).doit()
    6

    Multiple simultaneous bindings (order does not matter)::

    >>> x, y = Symbol('x'), Symbol('y')
    >>> With(List(Set(x, Integer(2)), Set(y, Integer(3))), x * y).doit()
    6

    Bindings are simultaneous — a later variable cannot reference an earlier one::

    >>> With(List(Set(x, Integer(4)), Set(y, x)), y).doit() == x
    True

    Nested ``With`` provides sequential binding::

    >>> With(List(Set(x, Integer(4))),
    ...      With(List(Set(y, x * Integer(2))), x + y)).doit()
    12

    Early exit via ``Return``::

    >>> With(List(Set(x, Integer(10))), Return(x * Integer(2))).doit()
    20
    """

    def __new__(cls, bindings, body):
        if isinstance(bindings, list):
            bindings = List(*bindings)
        if isinstance(bindings, dict):
            bindings = List(*[Set(k, v) for k, v in bindings.items()])
        return Expr.__new__(cls, sympify(bindings), sympify(body))

    def doit(self, **kwargs):
        bindings, body = self.args
        subs = _binding_substitutions(bindings, evaluate_values=True, **kwargs)
        result = _substitute_body(body, subs)
        try:
            return _eval(result, **kwargs)
        except _ReturnSignal as signal:
            return signal.value

    def _evaluate(self, **kwargs):
        return self


class Module(MathematicaExpr):
    """Mathematica ``Module[{x, y=v, …}, body]`` — lexical scoping.

    ``Module`` creates a private lexical scope by replacing each local
    variable with a fresh uniquely-named symbol (``name$N`` where *N* is a
    monotone counter).  This prevents name clashes with outer variables of
    the same name.

    * A plain ``Symbol`` entry (e.g. ``x``) introduces a fresh uninitialized
      local.  The fresh symbol appears in the evaluated body.
    * A ``Set(x, v)`` entry initialises the fresh local to the value *v*.

    Like ``With``, ``Module`` catches ``Return`` signals.

    Parameters
    ----------
    locals_list : List
        A ``List`` of ``Symbol`` or ``Set(symbol, init_value)`` entries.
    body : sympy.Expr
        The expression to evaluate in the local scope.

    Examples
    --------
    Initialized local::

    >>> n = Symbol('n')
    >>> Module(List(Set(n, Integer(4))), n * (n + Integer(1))).doit()
    20

    Uninitialized local produces a fresh symbol::

    >>> x = Symbol('x')
    >>> result = Module(List(x), x).doit()
    >>> isinstance(result, Symbol)
    True
    >>> isinstance(result, Symbol) and result != x    # Module creates a fresh symbol
    True

    Fresh symbols are independent across two ``Module`` calls::

    >>> r1 = Module(List(x), x).doit()
    >>> r2 = Module(List(x), x).doit()
    >>> r1 == r2
    False

    Fresh symbols are independent across two ``Module`` calls::

    >>> r1 = Module(List(x), x).doit()
    >>> r2 = Module(List(x), x).doit()
    >>> r1 == r2
    False

    Multiple locals with initializers::

    >>> a, b = Symbol('a'), Symbol('b')
    >>> Module(List(Set(a, Integer(3)), Set(b, Integer(4))), a**2 + b**2).doit()
    25
    """

    def __new__(cls, locals_list, body):
        if isinstance(locals_list, list):
            locals_list = List(*locals_list)
        elif isinstance(locals_list, dict):
            locals_list = List(*[Set(k, v) for k, v in locals_list.items()])
        return Expr.__new__(cls, sympify(locals_list), sympify(body))

    def doit(self, **kwargs):
        locals_list, body = self.args
        renamed = {}
        initialized = {}
        for item in _list_items(locals_list):
            if isinstance(item, Set):
                symbol, value = item.args
                fresh = _fresh_symbol(symbol)
                renamed[symbol] = fresh
                initialized[fresh] = _eval(value, **kwargs)
            elif isinstance(item, Symbol):
                renamed[item] = _fresh_symbol(item)
        result = _substitute_body(body.xreplace(renamed), initialized)
        try:
            return _eval(result, **kwargs)
        except _ReturnSignal as signal:
            return signal.value

    def _evaluate(self, **kwargs):
        return self


class Block(MathematicaExpr):
    """Mathematica ``Block[{x=v, …}, body]`` — dynamic variable scope.

    ``Block`` is similar to ``With`` but models Mathematica's *dynamic*
    scoping: local variables shadow outer bindings by name during the
    body's evaluation and are restored afterwards.  In this SymPy
    implementation, dynamic restoration is not required because SymPy
    expressions are immutable; ``Block`` therefore behaves like ``With``
    — it substitutes each binding into *body* and evaluates the result.

    The practical difference from ``With`` is semantic intent: ``With``
    documents that bindings are mathematical constants, while ``Block``
    documents that they are temporary variable overrides.

    Parameters
    ----------
    locals_list : List
        A ``List`` of ``Set(symbol, value)`` bindings.
    body : sympy.Expr
        The expression to evaluate under the local bindings.

    Examples
    --------
    Single binding::

    >>> x = Symbol('x')
    >>> Block(List(Set(x, Integer(10))), x + Integer(5)).doit()
    15

    Multiple bindings::

    >>> a, b = Symbol('a'), Symbol('b')
    >>> Block(List(Set(a, Integer(3)), Set(b, Integer(7))), a * b).doit()
    21

    Nested expressions are evaluated after substitution::

    >>> Block(List(Set(x, Integer(2))), x**3 + x).doit()
    10
    """

    def __new__(cls, locals_list, body):
        return Expr.__new__(cls, sympify(locals_list), sympify(body))

    def doit(self, **kwargs):
        locals_list, body = self.args
        subs = _binding_substitutions(locals_list, evaluate_values=True, **kwargs)
        result = _substitute_body(body, subs)
        try:
            return _eval(result, **kwargs)
        except _ReturnSignal as signal:
            return signal.value

    def _evaluate(self, **kwargs):
        return self


class Return(MathematicaExpr):
    """Mathematica ``Return[value]`` — exit from a procedural construct.

    When ``doit()`` is called, ``Return`` raises an internal
    ``_ReturnSignal`` that unwinds the Python call stack until it reaches
    the nearest enclosing ``With``, ``Module``, or ``Block``
    (anything that catches ``_ReturnSignal``).  The caught value is then
    returned as the result of that construct.

    ``Return[]`` (no argument) returns ``Null``.

    Parameters
    ----------
    value : sympy.Basic, optional
        The value to return (default: ``Null``).

    Examples
    --------
    Early exit from ``With``::

    >>> x = Symbol('x')
    >>> With(List(Set(x, Integer(10))), Return(x * Integer(3))).doit()
    30

    ``Return[]`` returns ``Null``::

    >>> With(List(), Return()).doit() == Null
    True

    Exit from ``Module`` ignoring remaining body::

    >>> n = Symbol('n')
    >>> Module(
    ...     List(Set(n, Integer(5))),
    ...     CompoundExpression(Return(n**2), n + Integer(1))
    ... ).doit()
    25
    """

    def __new__(cls, value=Null):
        return Expr.__new__(cls, sympify(value))

    def doit(self, **kwargs):
        raise _ReturnSignal(_eval(self.args[0], **kwargs))

    def _evaluate(self, **kwargs):
        return self


class Throw(MathematicaExpr):
    """Mathematica ``Throw[value]`` / ``Throw[value, tag]``.

    ``Throw`` is the "raise" half of the ``Catch``/``Throw`` mechanism.
    Calling ``doit()`` raises a ``_ThrowSignal`` that propagates up the
    Python call stack until an enclosing ``Catch`` intercepts it.

    A *tag* can be attached to differentiate ``Throw`` sites; ``Catch``
    can then selectively match on the tag.

    Parameters
    ----------
    value : sympy.Basic
        The value to throw.
    tag : sympy.Basic, optional
        Tag attached to this throw for selective catching.

    Examples
    --------
    Simple throw caught by ``Catch``::

    >>> Catch(Throw(Integer(42))).doit()
    42

    Tagged throw::

    >>> tag = Symbol('myTag')
    >>> Catch(Throw(Integer(7), tag), tag).doit()
    7

    ``Throw`` inside a compound expression — remaining expressions are skipped::

    >>> Catch(CompoundExpression(Throw(Integer(1)), Integer(2))).doit()
    1
    """

    def __new__(cls, value, tag=None):
        args = [sympify(value)]
        if tag is not None:
            args.append(sympify(tag))
        return Expr.__new__(cls, *args)

    def doit(self, **kwargs):
        value = _eval(self.args[0], **kwargs)
        tag = _eval(self.args[1], **kwargs) if len(self.args) > 1 else None
        raise _ThrowSignal(value, tag)

    def _evaluate(self, **kwargs):
        return self


class Catch(MathematicaExpr):
    """Mathematica ``Catch[expr]`` / ``Catch[expr, tag]`` /
    ``Catch[expr, tag, handler]``.

    Evaluates *expr*; if a ``Throw`` occurs inside it, ``Catch``
    intercepts the thrown value and returns it.

    * 1-arg form: catches any ``Throw``, returns the thrown value.
    * 2-arg form: only catches ``Throw`` with a matching *tag*;
      unmatched throws propagate to the next outer ``Catch``.
    * 3-arg form: passes the thrown ``(value, tag)`` pair to a *handler*
      callable (e.g. a ``sympy.Lambda``) and returns its result.

    Parameters
    ----------
    expr : sympy.Basic
        Expression to evaluate; may contain ``Throw``.
    form : sympy.Basic, optional
        Tag pattern; only throws whose tag equals *form* are caught.
    handler : callable or sympy.Lambda, optional
        Called as ``handler(value, tag)`` when a matching throw occurs.

    Examples
    --------
    No throw — normal evaluation::

    >>> Catch(Integer(5) + Integer(3)).doit()
    8

    Simple catch::

    >>> Catch(Throw(Integer(42))).doit()
    42

    Tagged catch — matching tag::

    >>> tag = Symbol('t')
    >>> Catch(Throw(Integer(99), tag), tag).doit()
    99

    Tagged catch — mismatched tag propagates::

    >>> import pytest
    >>> t1, t2 = Symbol('t1'), Symbol('t2')
    >>> with pytest.raises(Exception):
    ...     Catch(Throw(Integer(1), t1), t2).doit()

    Handler form — transform the caught value::

    >>> v = Symbol('v')
    >>> handler = sympy.Lambda(v, v * Integer(10))
    >>> Catch(Throw(Integer(3)), None, handler).doit()
    30
    """

    def __new__(cls, expr, form=None, handler=None):
        args = [sympify(expr)]
        if handler is not None:
            # Always store form at args[1] so handler is reliably at args[2].
            # Use Null as a sentinel meaning 'match any tag' when form is None.
            args.append(Null if form is None else sympify(form))
            args.append(sympify(handler))
        elif form is not None:
            args.append(sympify(form))
        return Expr.__new__(cls, *args)

    def doit(self, **kwargs):
        expr = self.args[0]
        if len(self.args) >= 3:
            form, handler = self.args[1], self.args[2]
        elif len(self.args) == 2:
            form, handler = self.args[1], None
        else:
            form = handler = None
        # Null sentinel means 'match any tag' (set by __new__ when form=None
        # but handler was provided).
        effective_form = None if (form is None or form == Null) else form
        try:
            return _eval(expr, **kwargs)
        except _ThrowSignal as signal:
            if effective_form is not None and signal.tag != effective_form:
                raise
            if handler is None:
                return signal.value
            return _apply_function(handler, signal.value, signal.tag)

    def _evaluate(self, **kwargs):
        return self


class Sow(MathematicaExpr):
    """Mathematica ``Sow[value]`` / ``Sow[value, tag]``.

    Deposits *value* into the nearest enclosing ``Reap`` collector and
    returns *value* as its own result.  If no ``Reap`` is active, the
    value is silently dropped and *value* is still returned.

    An optional *tag* can be used to associate the sown value with a
    label so that ``Reap`` can filter by tag.

    Parameters
    ----------
    value : sympy.Basic
        The value to collect.
    tag : sympy.Basic, optional
        A label attached to this sown value (default: ``Null``).

    Examples
    --------
    Returns the sown value regardless of whether a ``Reap`` is active::

    >>> Sow(Integer(7)).doit()
    7

    Inside ``Reap``, the value is collected::

    >>> result = Reap(Sow(Integer(7))).doit()
    >>> result.args[0]          # last evaluated value
    7
    >>> list(result.args[1].args[0].args)   # collected values
    [7]

    Tagged sow; only collected when ``Reap`` matches the same tag::

    >>> tag = Symbol('t')
    >>> result = Reap(CompoundExpression(Sow(Integer(1), tag),
    ...                                  Sow(Integer(2))), tag).doit()
    >>> list(result.args[1].args[0].args)   # only tagged value collected
    [1]
    """

    def __new__(cls, value, tag=None):
        args = [sympify(value)]
        if tag is not None:
            args.append(sympify(tag))
        return Expr.__new__(cls, *args)

    def doit(self, **kwargs):
        value = _eval(self.args[0], **kwargs)
        tag = _eval(self.args[1], **kwargs) if len(self.args) > 1 else Null
        if _SOW_STACK:
            _SOW_STACK[-1].append((tag, value))
        return value

    def _evaluate(self, **kwargs):
        return self


class Reap(MathematicaExpr):
    """Mathematica ``Reap[expr]`` / ``Reap[expr, tag]``.

    Evaluates *expr* while collecting all values deposited by ``Sow``
    calls inside it.  Returns a two-element ``List``:

    ``List(last_value, List(List(sown_1, sown_2, …)))``,

    mirroring Mathematica's ``{lastValue, {{sown1, sown2, …}}}``.  The
    inner double-wrapping is intentional: the outer ``List`` holds one
    sub-list per distinct tag when a tag pattern is used.

    An optional *tag* filters which sown values are collected;
    only values sown with a matching tag appear in the output.

    Parameters
    ----------
    expr : sympy.Basic
        Expression to evaluate; may contain ``Sow`` calls.
    pattern : sympy.Basic, optional
        If given, only collect values whose tag equals *pattern*.

    Examples
    --------
    Collect multiple values::

    >>> i = Symbol('i')
    >>> result = Reap(Do(Sow(i), List(i, Integer(4)))).doit()
    >>> result.args[0] == Null      # Do returns Null
    True
    >>> list(result.args[1].args[0].args)
    [1, 2, 3, 4]

    Combine with ``CompoundExpression``::

    >>> result = Reap(CompoundExpression(Sow(Integer(1)),
    ...                                  Sow(Integer(2)))).doit()
    >>> result.args[0]              # last evaluated value (Integer(2))
    2
    >>> list(result.args[1].args[0].args)
    [1, 2]

    Filtered by tag::

    >>> tag = Symbol('t')
    >>> result = Reap(CompoundExpression(Sow(Integer(10), tag),
    ...                                  Sow(Integer(20))), tag).doit()
    >>> list(result.args[1].args[0].args)
    [10]

    Nested ``Reap`` calls are independent::

    >>> outer = Reap(CompoundExpression(
    ...     Sow(Integer(1)),
    ...     Reap(Sow(Integer(2))))).doit()
    >>> list(outer.args[1].args[0].args)  # outer only sees value 1
    [1]
    """

    def __new__(cls, expr, pattern=None):
        args = [sympify(expr)]
        if pattern is not None:
            args.append(sympify(pattern))
        return Expr.__new__(cls, *args)

    def doit(self, **kwargs):
        expr = self.args[0]
        pattern = self.args[1] if len(self.args) > 1 else None
        bag: list[tuple[Any, Any]] = []
        _SOW_STACK.append(bag)
        try:
            result = _eval(expr, **kwargs)
        finally:
            _SOW_STACK.pop()
        values = [value for tag, value in bag if pattern is None or tag == pattern]
        return List(result, List(List(*values)))

    def _evaluate(self, **kwargs):
        return self


class Scan(MathematicaExpr):
    """Mathematica ``Scan[f, list]`` — apply *f* to each element for side effects.

    Applies *function* to every element of *expr* in order.  Return values
    are discarded.  Always returns ``Null``.

    *function* may be a ``sympy.Lambda``, a ``sympy.Function`` subclass
    instance, or any Python callable.

    If *function* triggers a ``Return`` signal during evaluation, ``Scan``
    catches it and immediately returns the signalled value (matching
    Mathematica's ``Return`` semantics inside ``Scan``).

    Parameters
    ----------
    function : callable or sympy.Lambda
        The function to apply to each element.
    expr : List
        The list of elements to scan over.

    Examples
    --------
    Returns ``Null`` after applying the function::

    >>> f = Symbol('f')
    >>> Scan(f, List(Integer(1), Integer(2), Integer(3))).doit() == Null
    True

    Collect squares via ``Sow`` inside a ``Reap``::

    >>> x = Symbol('x')
    >>> result = Reap(
    ...     Scan(sympy.Lambda(x, Sow(x**2)),
    ...          List(Integer(1), Integer(2), Integer(3)))
    ... ).doit()
    >>> list(result.args[1].args[0].args)
    [1, 4, 9]

    Early exit with ``Return``::

    >>> sentinel = Symbol('done')
    >>> Scan(
    ...     sympy.Lambda(x, If(sympy.Eq(x, Integer(2)),
    ...                        Return(sentinel), Sow(x))),
    ...     List(Integer(1), Integer(2), Integer(3))
    ... ).doit() == sentinel
    True
    """

    def __new__(cls, function, expr):
        return Expr.__new__(cls, sympify(function), sympify(expr))

    def doit(self, **kwargs):
        function, expr = self.args
        for item in _scan_items(expr):
            try:
                _eval(_apply_function(function, item), **kwargs)
            except _ReturnSignal as signal:
                return signal.value
        return Null

    def _evaluate(self, **kwargs):
        return self


class Do(MathematicaExpr):
    """Mathematica ``Do[body, spec]`` — imperative iteration.

    Executes *body* repeatedly according to one or more iterator
    specifications.  Always returns ``Null`` (use ``Sow``/``Reap`` or
    ``Scan`` to collect values).

    Iterator specification forms (passed as a ``List``):

    * ``List(n)``            — repeat *body* exactly *n* times.
    * ``List(i, n)``         — *i* runs from 1 to *n* (inclusive), step 1.
    * ``List(i, imin, imax)`` — *i* runs from *imin* to *imax*, step 1.
    * ``List(i, imin, imax, step)`` — *i* runs from *imin* to *imax* by
      *step* (may be negative for descending ranges).

    Multiple iterator specs produce nested loops (first spec is the
    outermost loop).

    If *body* triggers a ``Return`` signal, ``Do`` catches it and
    immediately returns the signalled value.

    Parameters
    ----------
    expr : sympy.Basic
        The body expression to evaluate on each iteration.
    *iter_specs : List
        One or more ``List`` iterator specifications (see forms above).

    Examples
    --------
    Fixed repetition::

    >>> Do(Integer(0), List(Integer(5))).doit() == Null
    True

    With iterator variable (1 to *n*, implicit)::

    >>> i = Symbol('i')
    >>> result = Reap(Do(Sow(i), List(i, Integer(4)))).doit()
    >>> list(result.args[1].args[0].args)
    [1, 2, 3, 4]

    Explicit range::

    >>> result = Reap(Do(Sow(i), List(i, Integer(3), Integer(7)))).doit()
    >>> list(result.args[1].args[0].args)
    [3, 4, 5, 6, 7]

    With step::

    >>> result = Reap(Do(Sow(i), List(i, Integer(1), Integer(9), Integer(2)))).doit()
    >>> list(result.args[1].args[0].args)
    [1, 3, 5, 7, 9]

    Descending step::

    >>> result = Reap(Do(Sow(i), List(i, Integer(5), Integer(1), Integer(-1)))).doit()
    >>> list(result.args[1].args[0].args)
    [5, 4, 3, 2, 1]

    Nested loops (matrix traversal)::

    >>> j = Symbol('j')
    >>> result = Reap(Do(Sow(i * Integer(10) + j),
    ...                  List(i, Integer(2)),
    ...                  List(j, Integer(2)))).doit()
    >>> list(result.args[1].args[0].args)
    [11, 12, 21, 22]
    """

    def __new__(cls, expr, *iter_specs):
        return Expr.__new__(cls, sympify(expr), *[sympify(spec) for spec in iter_specs])

    def doit(self, **kwargs):
        body = self.args[0]
        iter_specs = self.args[1:]
        try:
            _execute_do(body, iter_specs, kwargs)
        except _ReturnSignal as signal:
            return signal.value
        return Null

    def _evaluate(self, **kwargs):
        return self


class Head(MathematicaExpr):
    """Mathematica ``Head[expr]`` — the top-level constructor of an expression.

    Returns a ``Symbol`` whose name is the Mathematica-style head of the
    expression.  The mapping follows standard Wolfram conventions:

    ============================================ ==============
    Expression type                              Head returned
    ============================================ ==============
    ``Integer``                                  ``Integer``
    ``Rational`` (non-integer)                   ``Rational``
    ``Symbol``                                   ``Symbol``
    ``Add`` (sum)                                ``Plus``
    ``Mul`` (product)                            ``Times``
    ``Pow`` (power)                              ``Power``
    ``List``                                     ``List``
    ``sympy.Function`` subclass (e.g. ``sin``)   function name
    ``MathematicaExpr`` subclass                 class name
    ``S.true`` / ``S.false``                     ``True`` / ``False``
    ============================================ ==============

    Examples
    --------
    Numeric types::

    >>> Head(Integer(5)).doit()
    Integer
    >>> Head(Rational(2, 3)).doit()
    Rational

    Symbols and lists::

    >>> x = Symbol('x')
    >>> Head(x).doit()
    Symbol
    >>> Head(List(Integer(1), Integer(2))).doit()
    List

    Arithmetic operations::

    >>> a, b = Symbol('a'), Symbol('b')
    >>> Head(a + b).doit()
    Plus
    >>> Head(a * b).doit()
    Times
    >>> Head(a**b).doit()
    Power

    SymPy functions::

    >>> Head(sympy.sin(x)).doit()
    sin
    >>> Head(sympy.exp(x)).doit()
    exp

    Boolean constants::

    >>> Head(S.true).doit()
    True
    """

    def __new__(cls, expr):
        return Expr.__new__(cls, sympify(expr))

    def _evaluate(self, **kwargs):
        expr = self.args[0]
        return Symbol(_head_name(expr))


class D(MathematicaExpr):
    """Derivative"""
    def __new__(cls, f, x):
        obj = MathematicaExpr.__new__(cls, f, x)
        return obj

    def _evaluate(self, **kwargs):
        f, x = self.args
        return sympy.diff(f, x)


def _eval(expr, **kwargs):
    return expr.doit(**kwargs) if hasattr(expr, 'doit') else expr


def _is_true(value) -> bool:
    return value is True or value == S.true or isinstance(value, BooleanTrue)


def _is_false(value) -> bool:
    return value is False or value == S.false or isinstance(value, BooleanFalse)


def _list_items(expr) -> Iterable[Any]:
    if isinstance(expr, List):
        return expr.args
    if isinstance(expr, (tuple, list)):
        return expr
    return (expr,)


def _binding_substitutions(bindings, evaluate_values: bool, **kwargs):
    subs = {}
    for item in _list_items(bindings):
        if isinstance(item, Set):
            symbol, value = item.args
            subs[symbol] = _eval(value, **kwargs) if evaluate_values else value
    return subs


def _is_condition_wrapper(expr) -> bool:
    return getattr(expr.__class__, '__name__', '') == 'Condition' and len(getattr(expr, 'args', ())) == 2


def _substitute_body(body, substitutions):
    if _is_condition_wrapper(body):
        expr, test = body.args
        return body.func(expr.xreplace(substitutions), test.xreplace(substitutions))
    return body.xreplace(substitutions)


def _condition_holds(test, **kwargs) -> bool:
    test = _eval(test, **kwargs) if hasattr(test, 'doit') else test
    if _is_true(test):
        return True
    if _is_false(test):
        return False
    if isinstance(test, sympy.logic.boolalg.Not):
        return not _condition_holds(test.args[0], **kwargs)
    if isinstance(test, sympy.logic.boolalg.And):
        return all(_condition_holds(arg, **kwargs) for arg in test.args)
    if isinstance(test, sympy.logic.boolalg.Or):
        return any(_condition_holds(arg, **kwargs) for arg in test.args)
    if hasattr(test, 'check') and callable(test.check):
        return bool(test.check(**kwargs))
    return False


def _fresh_symbol(symbol: Symbol) -> Symbol:
    return Symbol(f'{symbol.name}${next(_MODULE_COUNTER)}')


def _apply_function(function, *items):
    if isinstance(function, sympy.Lambda):
        # Slice args to Lambda's declared arity: a 1-variable Lambda(v, expr)
        # still works when called as handler(value, tag).
        n = len(function.variables)
        return function(*items[:n])
    if isinstance(function, Expr) and getattr(function, 'is_Function', False):
        return function.func(*items)
    if callable(function):
        return function(*items)
    return sympy.Function(str(function))(*items)


def _scan_items(expr):
    if isinstance(expr, List):
        return expr.args
    if isinstance(expr, (tuple, list)):
        return expr
    return (expr,)


def _execute_do(body, iter_specs, kwargs):
    if not iter_specs:
        _eval(body, **kwargs)
        return
    current, *rest = iter_specs
    for subs in _iterator_substitutions(current, **kwargs):
        next_body = body.xreplace(subs)
        _execute_do(next_body, rest, kwargs)


def _iterator_substitutions(spec, **kwargs):
    if not isinstance(spec, List):
        raise TypeError('Do iterator specification must be a List expression')
    items = list(spec.args)
    if not items:
        return []

    if isinstance(items[0], Symbol):
        var = items[0]
        if len(items) == 2:
            imin = Integer(1)
            imax = _eval(items[1], **kwargs)
            step = Integer(1)
        elif len(items) == 3:
            imin = _eval(items[1], **kwargs)
            imax = _eval(items[2], **kwargs)
            step = Integer(1)
        elif len(items) == 4:
            imin = _eval(items[1], **kwargs)
            imax = _eval(items[2], **kwargs)
            step = _eval(items[3], **kwargs)
        else:
            raise ValueError('Unsupported Do iterator specification')
        return ({var: value} for value in _inclusive_range(imin, imax, step))

    if len(items) == 1:
        n = _eval(items[0], **kwargs)
        return ({} for _ in _inclusive_range(Integer(1), n, Integer(1)))

    raise ValueError('Unsupported Do iterator specification')


def _inclusive_range(imin, imax, step):
    start = int(imin)
    stop = int(imax)
    delta = int(step)
    if delta == 0:
        raise ValueError('Do step must be non-zero')
    if delta > 0:
        return [Integer(i) for i in range(start, stop + 1, delta)]
    return [Integer(i) for i in range(start, stop - 1, delta)]


def _head_name(expr) -> str:
    if expr == S.true:
        return 'True'
    if expr == S.false:
        return 'False'
    if expr == Null:
        return 'Symbol'
    if isinstance(expr, Integer):
        return 'Integer'
    if isinstance(expr, Rational) and not isinstance(expr, Integer):
        return 'Rational'
    if isinstance(expr, Symbol):
        return 'Symbol'
    if isinstance(expr, List):
        return 'List'
    if isinstance(expr, Add):
        return 'Plus'
    if isinstance(expr, Mul):
        return 'Times'
    if isinstance(expr, Pow):
        return 'Power'
    if isinstance(expr, sympy.Function):
        return expr.func.__name__
    if isinstance(expr, MathematicaExpr):
        return expr.__class__.__name__
    return expr.func.__name__


__all__ = [
    'Block',
    'Catch',
    'CompoundExpression',
    'Do',
    'Head',
    'If',
    'List',
    'MathematicaExpr',
    'Module',
    'Null',
    'Reap',
    'Return',
    'Scan',
    'Set',
    'Sow',
    'Throw',
    'With',
]
