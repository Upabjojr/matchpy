# -*- coding: utf-8 -*-
"""Generic base class for SymPy pattern-matching constraints.

This is layer-independent: it depends only on ``sympy`` and (lazily) on
``sympy_matching`` itself -- NOT on ``sympy_wolfram`` or ``rubi_rules``. It is the
constraint half of the reusable "SymPy + WildSymbol -> matchpy ManyToOneReplacer"
machinery (see :mod:`sympy_matching.matching_rule`): any project can subclass
:class:`SympyMatchingConstraint`, implement :meth:`check`, and feed instances as
rule guards without pulling in Wolfram/Rubi.

History: this class used to be ``MathematicaConstraint`` in ``sympy_wolfram`` (and
before that ``RubiConstraint`` in ``sympy_matching``). It is not Wolfram-specific --
it is the generic base for any SymPy predicate over matched wildcards -- so it lives
here. ``sympy_wolfram.constraints.MathematicaConstraint`` now subclasses it and only
adds the Mathematica-node (``MathematicaExpr``) identity on top.

Design
------
``SympyMatchingConstraint`` derives from :class:`sympy.logic.boolalg.Boolean`, so a
constraint is a first-class SymPy node that composes with the logic operators::

    Not(FreeQ(a, x))             -- negation
    And(EqQ(n, 0), IntegerQ(m))  -- conjunction
    Or(EqQ(n, 1), EqQ(n, -1))    -- disjunction

The SymPy invariant ``constraint == constraint.func(*constraint.args)`` holds:
``__new__`` normalises args to hashable SymPy-safe values and stores them via
``Boolean.__new__``; ``__eq__``/``__hash__`` come from ``sympy.Basic`` (compare by
``(type, args)``). It declares NO ``__slots__`` so subclasses may set instance
state (``self._var_name`` etc.) in ``__init__``.

Subclasses MUST implement :meth:`check` (called with a ``wildcard_name -> matched
SymPy expr`` mapping as kwargs, returns a bool). :attr:`variables` is auto-computed
from ``self.args`` by collecting WildSymbol names.
"""
from abc import abstractmethod
from typing import Tuple

import sympy
from sympy.logic.boolalg import Boolean


# ---------------------------------------------------------------------------
# Argument normalisation / wildcard collection / substitution
# ---------------------------------------------------------------------------

def _normalize_constraint_arg(a):
    """Return a hashable, SymPy-safe form of a single constraint argument.

    Converts Python primitives to their SymPy equivalents so that
    ``constraint.args`` contains only objects that can be hashed (SymPy's
    ``Basic.__hash__``) and serialised (``sympy_matching.json_ext``).
    """
    # SymPy objects are already safe -- pass through first to avoid re-wrapping
    # WildSymbol or other Symbol subclasses.
    if isinstance(a, sympy.Basic):
        return a

    # bool must be checked before int (bool is a subclass of int in Python).
    if isinstance(a, bool):
        return sympy.S.true if a else sympy.S.false

    if isinstance(a, int):
        return sympy.Integer(a)

    if isinstance(a, float):
        return sympy.Float(a)

    if isinstance(a, str):
        # Strip trailing underscore -- WildSymbol naming convention.
        name = a[:-1] if a.endswith('_') else a
        return sympy.Symbol(name)

    if isinstance(a, (list, tuple)):
        return sympy.Tuple(*(_normalize_constraint_arg(x) for x in a))

    if isinstance(a, dict):
        # Dicts are unhashable; convert to a sorted tuple of (key, value) pairs so
        # the result is both hashable and deterministic. The subclass __init__ must
        # therefore also accept a tuple-of-pairs for the argument that originally
        # carried a dict (see ExpressionEqQ).
        return tuple(
            sorted(
                (
                    (_normalize_constraint_arg(k), _normalize_constraint_arg(v))
                    for k, v in a.items()
                ),
                key=lambda kv: str(kv[0]),  # sort by string repr of key
            )
        )

    # Callable, set, or other type: leave unchanged; the subclass is responsible
    # for ensuring these are hashable if needed.
    return a


def _collect_wildcards_from_args(args):
    """Recursively collect WildSymbol names from constraint args.

    Returns a sorted list of unique wildcard names.
    """
    names = set()

    def _walk(obj):
        if obj is None:
            return
        # A WildSymbol is identified by its wildcard_name attribute.
        if hasattr(obj, 'wildcard_name'):
            names.add(obj.wildcard_name)
        elif isinstance(obj, sympy.Basic):
            for sym in obj.free_symbols:
                if hasattr(sym, 'wildcard_name'):
                    names.add(sym.wildcard_name)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                _walk(item)

    for arg in args:
        _walk(arg)

    return sorted(names)


def _resolve_with_substitution(expr, substitution):
    """Resolve an expression using a substitution dict keyed by wildcard/symbol name.

    If ``expr`` is a WildSymbol or Symbol whose name is in ``substitution``, return
    the substituted value. For compound SymPy expressions, xreplace the matching
    free symbols. For tuples/lists, resolve recursively. Otherwise return unchanged.
    """
    if expr is None:
        return None

    # Direct lookup by wildcard_name
    if hasattr(expr, 'wildcard_name') and expr.wildcard_name in substitution:
        return substitution[expr.wildcard_name]

    # Direct lookup by symbol name
    if isinstance(expr, sympy.Symbol) and expr.name in substitution:
        return substitution[expr.name]

    # For compound expressions, build an xreplace dict
    if isinstance(expr, sympy.Basic) and expr.free_symbols:
        subs_dict = {}
        for sym in expr.free_symbols:
            if hasattr(sym, 'wildcard_name') and sym.wildcard_name in substitution:
                subs_dict[sym] = substitution[sym.wildcard_name]
            elif sym.name in substitution:
                subs_dict[sym] = substitution[sym.name]
        if subs_dict:
            return expr.xreplace(subs_dict)

    # For tuples/lists, resolve recursively
    if isinstance(expr, (list, tuple)):
        resolved = [_resolve_with_substitution(item, substitution) for item in expr]
        return type(expr)(resolved) if isinstance(expr, tuple) else resolved

    return expr


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class SympyMatchingConstraint(Boolean):
    """Abstract base class for a SymPy pattern-matching constraint (rule guard).

    A constraint receives the matched wildcard values (as SymPy expressions) via
    :meth:`check` and returns a bool. It is deliberately independent of MatchPy
    internals; conversion to a MatchPy ``CustomConstraint`` is handled by
    :func:`sympy_matching.matching_rule.build_tracing_replacer`.

    Subclasses MUST implement :meth:`check`. :attr:`variables` is auto-computed by
    scanning ``self.args`` for WildSymbol instances.
    """

    # NOTE: declares no __slots__, so instances get a __dict__ and subclasses may
    # set state (_var_name, _value, ...) in __init__.

    def __new__(cls, *args, **kwargs):
        # **kwargs are forwarded to __init__ automatically; they are NOT stored in
        # _args because they cannot reliably round-trip through func(*args).
        safe_args = tuple(_normalize_constraint_arg(a) for a in args)
        return Boolean.__new__(cls, *safe_args)

    def doit(self, **kwargs):
        # A constraint is a predicate, not a reducible expression: keep the node
        # intact; its truth value comes from check(), never from doit().
        return self

    @property
    def variables(self) -> Tuple[str, ...]:
        """Names of the wildcard variables this constraint depends on."""
        return tuple(_collect_wildcards_from_args(self.args))

    @abstractmethod
    def check(self, **substitution) -> bool:
        """Return True iff the constraint is satisfied.

        Args:
            **substitution: wildcard_name -> matched SymPy expression
        """

    @staticmethod
    def _to_sympy(val):
        """Convert a value to a SymPy expression (handles MatchPy objects)."""
        if isinstance(val, sympy.Basic):
            return val
        try:
            from sympy_matching.conversion import matchpy_to_sympy
            return matchpy_to_sympy(val)
        except (ImportError, TypeError, AttributeError):
            return sympy.sympify(val)

    def _resolve_all(self, kwargs):
        """Convert all kwargs values to SymPy, return a dict for _resolve."""
        return {k: self._to_sympy(v) for k, v in kwargs.items()}

    def _resolve(self, expr, substitution):
        """Convenience: resolve expr using the substitution dict."""
        return _resolve_with_substitution(expr, substitution)

    # Required by the Boolean subclass -- no free symbols from SymPy's perspective.
    @property
    def free_symbols(self):
        return set()
