# -*- coding: utf-8 -*-
"""Singledispatch registrations for converting between SymPy and OmniMatch expressions.

Importing this module registers the converters with omnimatch's to_omnimatch_expression
and from_omnimatch_expression singledispatch functions.

The conversion is table-driven: SYMPY_NODES in operations.py defines all
supported SymPy types; a for-loop here registers singledispatch handlers
for both directions (to_omnimatch_expression and from_omnimatch_expression).

Special cases (Add, Mul, Pow) that need IDENTITY_ELEMENT resolution are
still handled by explicit handlers.

Usage:
    import sympy_matching.conversion  # registers dispatchers as side-effect

    from omnimatch import to_omnimatch_expression, from_omnimatch_expression
    import sympy

    x = sympy.Symbol('x')
    expr = sympy.sin(x) + 1
    mp_expr = to_omnimatch_expression(expr)       # OmniMatch expression tree
    sp_expr = from_omnimatch_expression(mp_expr)  # back to SymPy/Python

"""
import sys
import os
from functools import singledispatch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import sympy
from sympy import (
    Add as SympyAdd,
    Mul as SympyMul,
    Pow as SympyPow,
    Symbol as SympySymbol,
    Number as SympyNumber,
)
from sympy.core.basic import Basic as SympyBasic

from omnimatch.expressions.expressions import (
    Expression, Operation, OperationHead, NamedAtom, SymbolWrapper, Wildcard,
    WildcardOperationHead, to_omnimatch_expression, from_omnimatch_expression,
    LIST_HEAD, TUPLE_HEAD,
)
from .wild import (WildSymbol, IDENTITY_ELEMENT, HeadRef, WildHeadApp,
                   WildHeadDeriv)
from .operations import (
    ADD, MUL, POW, EQUALITY,
    SYMPY_FUNC_TO_HEAD, HEAD_TO_SYMPY_FUNC,
    register_all_heads, register_sympy_head,
)

# ─── Register all heads from the master table ────────────────────────────────

register_all_heads()


# ─── Identity element mapping ─────────────────────────────────────────────────

_SYMPY_IDENTITY = {
    SympyAdd: sympy.Integer(0),
    SympyMul: sympy.Integer(1),
    SympyPow: sympy.Integer(1),   # exponent identity: x**1 = x
}
"""Maps SymPy operation types to their identity elements.
Used to resolve IDENTITY_ELEMENT at conversion time.
For Pow, the identity (1) applies only to the exponent position."""


def _convert_operand(arg, parent_sympy_type):
    """Convert a SymPy sub-expression, resolving IDENTITY_ELEMENT for WildSymbols.

    If `arg` is a WildSymbol whose optional_value is IDENTITY_ELEMENT, it is
    converted to a OmniMatch optional wildcard whose default is the identity
    element of `parent_sympy_type` (e.g. 0 for Add, 1 for Mul).
    """
    if isinstance(arg, WildSymbol) and arg.optional_value is IDENTITY_ELEMENT:
        identity = _SYMPY_IDENTITY.get(parent_sympy_type)
        if identity is None:
            raise ValueError(
                f"IDENTITY_ELEMENT used inside {parent_sympy_type.__name__} which has "
                f"no registered identity element.  Use an explicit optional_value instead."
            )
        return Wildcard.optional(arg.wildcard_name, to_omnimatch_expression(identity))
    return to_omnimatch_expression(arg)


# ─── to_omnimatch_expression: SymPy → OmniMatch (special cases) ──────────────────────────

@to_omnimatch_expression.register(SympyNumber)
def _sympy_number_to_expression(obj: SympyNumber) -> Expression:
    """Convert SymPy numbers to OmniMatch SymbolWrappers for lossless roundtrip."""
    return SymbolWrapper(obj)


@to_omnimatch_expression.register(WildSymbol)
def _wild_symbol_to_expression(obj: WildSymbol) -> Expression:
    """Convert WildSymbol to the corresponding OmniMatch wildcard.

    If `optional_value` is set, emit a OmniMatch optional wildcard carrying the
    converted default value. Otherwise emit a standard dot wildcard.
    Plain Python numerics are coerced to SymPy types for lossless roundtrip.
    """
    if obj.is_optional:
        val = obj.optional_value
        # Coerce raw Python numerics to SymPy so they become SymbolWrapper
        # (not bare Symbol('0')) and roundtrip correctly.
        if isinstance(val, int):
            val = sympy.Integer(val)
        elif isinstance(val, float):
            val = sympy.Float(val)
        return Wildcard.optional(obj.wildcard_name, to_omnimatch_expression(val))
    return Wildcard.dot(obj.wildcard_name)


@to_omnimatch_expression.register(WildHeadApp)
def _wild_head_app_to_expression(obj: 'WildHeadApp') -> Expression:
    """Convert ``F_[args]`` into a OmniMatch Operation with a WILDCARD head.

    The resulting operation matches an application of ANY function: OmniMatch binds
    the subject's head to the head wildcard's name and matches the operands
    against the converted arguments in the usual way.
    """
    head = WildcardOperationHead(name='__any__',
                                 variable_name=obj.head_wild.wildcard_name)
    return Operation(head, *[to_omnimatch_expression(a) for a in obj.applied_args])


# `Derivative`/`Tuple` have no dedicated head registration, so a real
# ``Derivative(f(x), (x, n))`` converts through the generic fallback into
# ``Operation(OperationHead('Derivative'), <f(x)>, Operation(OperationHead('Tuple'), x, n))``.
# A WildHeadDeriv PATTERN must produce exactly that shape, so it is built from the
# same heads (OperationHead equality is by name/arity/flags).
# ``test_wildcard_head_bridge`` asserts these stay in sync with a real conversion.
_DERIVATIVE_HEAD = OperationHead(name='Derivative')
_TUPLE_OP_HEAD = OperationHead(name='Tuple')


@to_omnimatch_expression.register(WildHeadDeriv)
def _wild_head_deriv_to_expression(obj: 'WildHeadDeriv') -> Expression:
    """Convert ``Derivative[n_][f_][x_]`` into the OmniMatch shape of a SymPy
    ``Derivative`` whose differentiated function has a WILDCARD head."""
    var = to_omnimatch_expression(obj.var)
    inner = Operation(
        WildcardOperationHead(name='__any__',
                              variable_name=obj.head_wild.wildcard_name),
        var)
    return Operation(_DERIVATIVE_HEAD, inner,
                     Operation(_TUPLE_OP_HEAD, var, to_omnimatch_expression(obj.order)))


@to_omnimatch_expression.register(SympySymbol)
def _sympy_symbol_to_expression(obj: SympySymbol) -> Expression:
    """Convert SymPy Symbol to OmniMatch SymbolWrapper wrapping the original object."""
    return SymbolWrapper(obj)


@to_omnimatch_expression.register(SympyAdd)
def _sympy_add_to_expression(obj: SympyAdd) -> Expression:
    """Convert SymPy Add to OmniMatch Operation with ADD head."""
    operands = [_convert_operand(arg, SympyAdd) for arg in obj.args]
    return Operation(ADD, *operands)


@to_omnimatch_expression.register(SympyMul)
def _sympy_mul_to_expression(obj: SympyMul) -> Expression:
    """Convert SymPy Mul to OmniMatch Operation with MUL head."""
    operands = [_convert_operand(arg, SympyMul) for arg in obj.args]
    return Operation(MUL, *operands)


@to_omnimatch_expression.register(SympyPow)
def _sympy_pow_to_expression(obj: SympyPow) -> Expression:
    """Convert SymPy Pow to OmniMatch Operation with POW head.

    IDENTITY_ELEMENT is resolved only for the exponent (second arg),
    since x**1 = x is the relevant identity for Pow.
    """
    base, exp = obj.args
    return Operation(POW, to_omnimatch_expression(base), _convert_operand(exp, SympyPow))


# ─── to_omnimatch_expression: loop-based registration for all table-driven nodes ───────

def _make_to_expression_converter(head):
    """Factory: create a to_omnimatch_expression handler for a given OperationHead."""
    def _converter(obj) -> Expression:
        operands = [to_omnimatch_expression(arg) for arg in obj.args]
        return Operation(head, *operands)
    return _converter


# Register to_omnimatch_expression for every SymPy class in SYMPY_FUNC_TO_HEAD that
# doesn't already have a specific handler (Add, Mul, Pow, Number, Symbol).
_SPECIAL_TYPES = {SympyAdd, SympyMul, SympyPow, SympyNumber, SympySymbol, WildSymbol}

for _sympy_cls, _head in list(SYMPY_FUNC_TO_HEAD.items()):
    if _sympy_cls in _SPECIAL_TYPES:
        continue
    if not isinstance(_sympy_cls, type):
        continue  # skip helper functions (e.g. sqrt) that aren't real classes
    to_omnimatch_expression.register(_sympy_cls)(_make_to_expression_converter(_head))


# ─── Fallback for other SymPy Basic types ─────────────────────────────────────

@to_omnimatch_expression.register(SympyBasic)
def _sympy_basic_to_expression(obj: SympyBasic) -> Expression:
    """Fallback: convert unknown SymPy expression via its args."""
    if obj.is_Atom:
        return SymbolWrapper(obj)

    obj_type = type(obj)
    if obj_type in SYMPY_FUNC_TO_HEAD:
        head = SYMPY_FUNC_TO_HEAD[obj_type]
        operands = [to_omnimatch_expression(arg) for arg in obj.args]
        return Operation(head, *operands)

    from omnimatch.expressions.expressions import OperationHead, Arity
    head = OperationHead(name=obj_type.__name__, arity=Arity.variadic)
    operands = [to_omnimatch_expression(arg) for arg in obj.args]
    return Operation(head, *operands)


# ─── from_omnimatch_expression: OmniMatch → SymPy / Python ───────────────────────────────

def _head_to_sympy(head: OperationHead) -> HeadRef:
    """Map a matched OmniMatch ``OperationHead`` to a substitutable SymPy ``HeadRef``.

    A wildcard operation head binds to an ``OperationHead`` (matcher metadata, not
    an expression). It must NEVER reach SymPy as-is -- arithmetic on it raises
    ``TypeError: unsupported operand type(s) for -: 'OperationHead' and 'Symbol'``.
    An unregistered head degrades to an undefined SymPy function of the same name
    rather than leaking the raw object.
    """
    func = HEAD_TO_SYMPY_FUNC.get(head)
    if func is None:
        func = sympy.Function(head.name)
    return HeadRef(func)


@from_omnimatch_expression.register(SymbolWrapper)
def _symbol_wrapper_from_expression(expr: SymbolWrapper):
    """Lossless conversion: unwrap the original SymPy object directly.

    A wildcard operation head arrives wrapped in a SymbolWrapper; convert it to a
    ``HeadRef`` so it can be substituted into a replacement and re-applied.
    """
    value = expr.value
    if isinstance(value, OperationHead):
        return _head_to_sympy(value)
    return value


def _unwrap_tuplearg(v):
    """Recursively turn hyper/meijerg TupleArg containers back into plain tuples.

    hyper/meijerg/appellf1 constructors accept plain lists/tuples for their
    parameter groups but reject an already-built ``TupleArg`` (e.g. hyper does
    ``Tuple(*ap)``, which cannot unpack one).  meijerg nests them
    (``((a,), (b,))``), so the unwrap must recurse.
    """
    if type(v).__name__ == 'TupleArg':
        return tuple(_unwrap_tuplearg(e) for e in v.args)
    return v


# ─── omnimatch_to_sympy: singledispatch by OmniMatch node type ────────────────────
#
# Extensibility (mirrors the to_omnimatch_expression direction):
#   * per-NODE-TYPE:  @omnimatch_to_sympy.register(MyOmnimatchType)
#   * per-HEAD-NAME:  @register_head_converter('MyHead') for Operations whose head
#     has no registered SymPy class (see HEAD_TO_SYMPY_FUNC); the converter
#     receives the already-converted operand list.
# Both registries are usable from OUTSIDE this library.

_HEAD_NAME_CONVERTERS = {}
"""Converters for Operation heads WITHOUT a registered SymPy class, keyed by head
name. Each is called as ``fn(args)`` with the operands already converted to SymPy;
returning ``NotImplemented`` falls through to the undefined-Function fallback."""


def register_head_converter(head_name: str, fn=None):
    """Register ``fn(args) -> sympy_expr`` for Operations with the given head name.

    Usable as a decorator: ``@register_head_converter('Derivative')``.
    """
    if fn is None:
        def _decorator(f):
            _HEAD_NAME_CONVERTERS[head_name] = f
            return f
        return _decorator
    _HEAD_NAME_CONVERTERS[head_name] = fn
    return fn


@singledispatch
def omnimatch_to_sympy(expr):
    """Convert a OmniMatch expression tree back to a SymPy expression.

    Singledispatch — register handlers for new OmniMatch node types with
    ``@omnimatch_to_sympy.register(Type)``, and converters for unregistered
    operation heads with :func:`register_head_converter`. Unknown nodes fall
    back to omnimatch's generic :func:`from_omnimatch_expression`.
    """
    return from_omnimatch_expression(expr)


@omnimatch_to_sympy.register(Operation)
def _operation_to_sympy(expr):
    head = expr.head
    if head in HEAD_TO_SYMPY_FUNC:
        sympy_class = HEAD_TO_SYMPY_FUNC[head]
        args = [omnimatch_to_sympy(op) for op in expr.operands]
        # POW with one_identity=True: a 1-arg Operation(POW, base) represents
        # base**1 = base.  SympyPow(base) would raise TypeError, so unwrap.
        if sympy_class is SympyPow and len(args) == 1:
            return args[0]
        # hyper/meijerg/appellf1 store their parameter lists in TupleArg
        # containers.  Their constructors accept plain lists/tuples and wrap
        # them, but reject an already-built TupleArg (hyper does Tuple(*ap),
        # which cannot unpack a TupleArg), so unwrap those back to tuples --
        # recursively, since meijerg nests them (((a,),(b,)), ...).
        args = [_unwrap_tuplearg(a) for a in args]
        return sympy_class(*args)
    args = [omnimatch_to_sympy(op) for op in expr.operands]
    converter = _HEAD_NAME_CONVERTERS.get(head.name)
    if converter is not None:
        result = converter(args)
        if result is not NotImplemented:
            return result
    return sympy.Function(head.name)(*args)


@register_head_converter(LIST_HEAD.name)      # 'list'
def _list_head_to_sympy(args):
    return list(args)


@register_head_converter(TUPLE_HEAD.name)     # 'tuple'
def _tuple_head_to_sympy(args):
    return tuple(args)


@register_head_converter('Derivative')
def _derivative_head_to_sympy(args):
    """Rebuild a real ``sympy.Derivative`` for the unregistered 'Derivative' head.

    Without this the generic fallback would rebuild it as an UNDEFINED function
    named "Derivative", losing all derivative semantics. The ``(var, order)``
    specs come back either as a SymPy Tuple or (also unregistered) as an
    undefined function named "Tuple"; Derivative requires plain tuples, so
    normalise both.
    """
    def _plain(t):
        if isinstance(t, sympy.Tuple):
            return tuple(t)
        if getattr(getattr(t, 'func', None), '__name__', '') == 'Tuple':
            return tuple(t.args)
        return t
    try:
        return sympy.Derivative(*[_plain(t) for t in args])
    except (ValueError, TypeError, sympy.SympifyError):
        # e.g. converting a PATTERN back, where the operands are still
        # wildcards -- fall through to the inert-function fallback.
        return NotImplemented


@omnimatch_to_sympy.register(SymbolWrapper)
def _symbol_wrapper_to_sympy(expr):
    # A wildcard operation head binds to an OperationHead; it must never reach
    # SymPy raw (arithmetic on it raises TypeError) -- see _head_to_sympy.
    value = expr.value
    if isinstance(value, OperationHead):
        return _head_to_sympy(value)
    return value


@omnimatch_to_sympy.register(Wildcard)
def _wildcard_to_sympy(expr):
    # An unbound wildcard reaching here is a pattern variable LOCAL to a MatchQ
    # embedded in a rule's REPLACEMENT, e.g. If[MatchQ[f, f1*Complex(0, j)], ...]:
    # f1/j/e1 are NOT bound by the outer rule match, only by the MatchQ's own pattern
    # matching WHEN that MatchQ runs. omnimatch_to_sympy runs BEFORE the replacement's
    # .doit(), so at this instant the wildcard is legitimately still free -- convert it
    # to a WildSymbol so the round-trip does not crash (SympifyError: Wildcard.dot).
    # `If.doit()` then evaluates the MatchQ (see sympy_wolfram.objects.If.doit), which
    # resolves f1/j/e1 exactly as Wolfram does, so NO wildcard survives into the final
    # antiderivative. NOTE FOR FUTURE AGENTS: a wildcard appearing in a *finished*
    # result is therefore always a real bug -- some predicate condition (MatchQ/EqQ/...)
    # was not evaluated at fire time. Fix that evaluation; do NOT paper over it by
    # discarding wildcard-laden results downstream.
    if getattr(expr, 'variable_name', None):
        return WildSymbol(expr.variable_name)
    return from_omnimatch_expression(expr)


@omnimatch_to_sympy.register(NamedAtom)
def _named_atom_to_sympy(expr):
    return SympySymbol(expr.name)
