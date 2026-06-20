# -*- coding: utf-8 -*-
"""Singledispatch registrations for converting between SymPy and MatchPy expressions.

Importing this module registers the converters with matchpy's to_expression
and from_expression singledispatch functions.

The conversion is table-driven: SYMPY_NODES in operations.py defines all
supported SymPy types; a for-loop here registers singledispatch handlers
for both directions (to_expression and from_expression).

Special cases (Add, Mul, Pow) that need IDENTITY_ELEMENT resolution are
still handled by explicit handlers.

Usage:
    import sympy_objects.conversion  # registers dispatchers as side-effect

    from matchpy import to_expression, from_expression
    import sympy

    x = sympy.Symbol('x')
    expr = sympy.sin(x) + 1
    mp_expr = to_expression(expr)       # MatchPy expression tree
    sp_expr = from_expression(mp_expr)  # back to SymPy/Python

"""
import sys
import os

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

from matchpy.expressions.expressions import (
    Expression, Operation, Symbol, SymbolWrapper, Wildcard, to_expression, from_expression,
    LIST_HEAD, TUPLE_HEAD,
)
from .wild import WildSymbol, IDENTITY_ELEMENT
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
    converted to a MatchPy optional wildcard whose default is the identity
    element of `parent_sympy_type` (e.g. 0 for Add, 1 for Mul).
    """
    if isinstance(arg, WildSymbol) and arg.optional_value is IDENTITY_ELEMENT:
        identity = _SYMPY_IDENTITY.get(parent_sympy_type)
        if identity is None:
            raise ValueError(
                f"IDENTITY_ELEMENT used inside {parent_sympy_type.__name__} which has "
                f"no registered identity element.  Use an explicit optional_value instead."
            )
        return Wildcard.optional(arg.wildcard_name, to_expression(identity))
    return to_expression(arg)


# ─── to_expression: SymPy → MatchPy (special cases) ──────────────────────────

@to_expression.register(SympyNumber)
def _sympy_number_to_expression(obj: SympyNumber) -> Expression:
    """Convert SymPy numbers to MatchPy SymbolWrappers for lossless roundtrip."""
    return SymbolWrapper(obj)


@to_expression.register(WildSymbol)
def _wild_symbol_to_expression(obj: WildSymbol) -> Expression:
    """Convert WildSymbol to the corresponding MatchPy wildcard.

    If `optional_value` is set, emit a MatchPy optional wildcard carrying the
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
        return Wildcard.optional(obj.wildcard_name, to_expression(val))
    return Wildcard.dot(obj.wildcard_name)


@to_expression.register(SympySymbol)
def _sympy_symbol_to_expression(obj: SympySymbol) -> Expression:
    """Convert SymPy Symbol to MatchPy SymbolWrapper wrapping the original object."""
    return SymbolWrapper(obj)


@to_expression.register(SympyAdd)
def _sympy_add_to_expression(obj: SympyAdd) -> Expression:
    """Convert SymPy Add to MatchPy Operation with ADD head."""
    operands = [_convert_operand(arg, SympyAdd) for arg in obj.args]
    return Operation(ADD, *operands)


@to_expression.register(SympyMul)
def _sympy_mul_to_expression(obj: SympyMul) -> Expression:
    """Convert SymPy Mul to MatchPy Operation with MUL head."""
    operands = [_convert_operand(arg, SympyMul) for arg in obj.args]
    return Operation(MUL, *operands)


@to_expression.register(SympyPow)
def _sympy_pow_to_expression(obj: SympyPow) -> Expression:
    """Convert SymPy Pow to MatchPy Operation with POW head.

    IDENTITY_ELEMENT is resolved only for the exponent (second arg),
    since x**1 = x is the relevant identity for Pow.
    """
    base, exp = obj.args
    return Operation(POW, to_expression(base), _convert_operand(exp, SympyPow))


# ─── to_expression: loop-based registration for all table-driven nodes ───────

def _make_to_expression_converter(head):
    """Factory: create a to_expression handler for a given OperationHead."""
    def _converter(obj) -> Expression:
        operands = [to_expression(arg) for arg in obj.args]
        return Operation(head, *operands)
    return _converter


# Register to_expression for every SymPy class in SYMPY_FUNC_TO_HEAD that
# doesn't already have a specific handler (Add, Mul, Pow, Number, Symbol).
_SPECIAL_TYPES = {SympyAdd, SympyMul, SympyPow, SympyNumber, SympySymbol, WildSymbol}

for _sympy_cls, _head in list(SYMPY_FUNC_TO_HEAD.items()):
    if _sympy_cls in _SPECIAL_TYPES:
        continue
    if not isinstance(_sympy_cls, type):
        continue  # skip helper functions (e.g. sqrt) that aren't real classes
    to_expression.register(_sympy_cls)(_make_to_expression_converter(_head))


# ─── Fallback for other SymPy Basic types ─────────────────────────────────────

@to_expression.register(SympyBasic)
def _sympy_basic_to_expression(obj: SympyBasic) -> Expression:
    """Fallback: convert unknown SymPy expression via its args."""
    if obj.is_Atom:
        return SymbolWrapper(obj)

    obj_type = type(obj)
    if obj_type in SYMPY_FUNC_TO_HEAD:
        head = SYMPY_FUNC_TO_HEAD[obj_type]
        operands = [to_expression(arg) for arg in obj.args]
        return Operation(head, *operands)

    from matchpy.expressions.expressions import OperationHead, Arity
    head = OperationHead(name=obj_type.__name__, arity=Arity.variadic)
    operands = [to_expression(arg) for arg in obj.args]
    return Operation(head, *operands)


# ─── from_expression: MatchPy → SymPy / Python ───────────────────────────────

@from_expression.register(SymbolWrapper)
def _symbol_wrapper_from_expression(expr: SymbolWrapper):
    """Lossless conversion: unwrap the original SymPy object directly."""
    return expr.value


def matchpy_to_sympy(expr):
    """Convert a MatchPy expression tree back to a SymPy expression.

    Handles:
    - SymbolWrapper → unwrap original SymPy object (via from_expression dispatch)
    - Operations with registered SymPy heads → corresponding SymPy classes
    - Built-in container heads (list, tuple) → Python containers
    - Plain Symbols → sympy.Symbol

    Note on 1-arg POW: because POW has one_identity=True with variadic arity,
    MatchPy's matching algorithm may internally produce a 1-arg POW(base) to
    represent a bare symbol.  That case is normalised back to just the base
    (base**1 = base in SymPy).
    """
    if isinstance(expr, Operation):
        head = expr.head
        if head in HEAD_TO_SYMPY_FUNC:
            sympy_class = HEAD_TO_SYMPY_FUNC[head]
            args = [matchpy_to_sympy(op) for op in expr.operands]
            # POW with one_identity=True: a 1-arg Operation(POW, base) represents
            # base**1 = base.  SympyPow(base) would raise TypeError, so unwrap.
            if sympy_class is SympyPow and len(args) == 1:
                return args[0]
            return sympy_class(*args)
        if head == LIST_HEAD:
            return [matchpy_to_sympy(op) for op in expr.operands]
        if head == TUPLE_HEAD:
            return tuple(matchpy_to_sympy(op) for op in expr.operands)
        args = [matchpy_to_sympy(op) for op in expr.operands]
        return sympy.Function(head.name)(*args)

    if isinstance(expr, SymbolWrapper):
        return expr.value

    if isinstance(expr, Symbol):
        return SympySymbol(expr.name)

    return from_expression(expr)
