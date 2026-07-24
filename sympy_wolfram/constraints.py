# -*- coding: utf-8 -*-
"""Abstract base class for Wolfram-language pattern constraints.

This module is part of sympy_wolfram and has NO dependency on rubi_rules.
Concrete constraint subclasses (FreeQ, EqQ, IntegerQ, …) live in
rubi_rules.utils.constraints_wolfram / constraints_rubi and import
``MathematicaConstraint`` from here.

``MathematicaConstraint`` used to be called ``RubiConstraint`` and lived in
``sympy_matching.constraints``.  It is not Rubi-specific — it is the generic
base for any Wolfram-language predicate — so it was renamed and moved up into
sympy_wolfram, where it can inherit from :class:`~sympy_wolfram.objects.MathematicaExpr`.

Design
------
``MathematicaConstraint`` inherits from BOTH
:class:`~sympy_wolfram.objects.MathematicaExpr` (so a constraint is a first-class
Mathematica-inspired SymPy node like every other object in this package) AND
:class:`sympy.logic.boolalg.Boolean` (so constraints compose naturally with
SymPy logic operators)::

    Not(FreeQ(a, x))             — negation
    And(EqQ(n, 0), IntegerQ(m))  — conjunction
    Or(EqQ(n, 1), EqQ(n, -1))    — disjunction

The MRO is ``MathematicaConstraint → MathematicaExpr → Expr → Boolean → Basic``:
both mixins ultimately derive from ``sympy.Basic``, so there is no metaclass or
layout conflict.

The SymPy invariant
    constraint == constraint.func(*constraint.args)
is satisfied by construction:

* ``__new__`` normalises every argument to a hashable, SymPy-safe value and
  delegates to ``Boolean.__new__``, which stores them in ``obj._args``.
* ``__eq__`` and ``__hash__`` are inherited from ``sympy.core.basic.Basic``
  and compare by ``(type, args)``, so any two constraint objects built from
  the same class and the same normalised arguments are equal.

Argument normalisation rules applied in ``__new__``
    * ``list``  →  ``tuple`` (recursive, for multi-variable constraints like
      ``FreeQ(['a', 'b'], x)``)
    * ``str``   →  ``sympy.Symbol`` (trailing ``_`` is stripped — WildSymbol
      naming convention; ``'a_'`` → ``Symbol('a')``)
    * ``int`` / ``float`` (non-bool) → ``sympy.Integer`` / ``sympy.Float``
    * ``sympy.Basic`` and everything else → passed through unchanged

Subclasses MUST implement
    ``check``  — predicate called with substitution dict as kwargs

The ``variables`` property is auto-computed from ``self.args`` by finding
all WildSymbol instances and extracting their wildcard names.
"""
from abc import abstractmethod
from typing import Tuple

import sympy
from sympy.logic.boolalg import Boolean

from sympy_wolfram.objects import MathematicaExpr


# ---------------------------------------------------------------------------
# Argument normalisation
# ---------------------------------------------------------------------------

def _normalize_constraint_arg(a):
    """Return a hashable, SymPy-safe form of a single constraint argument.

    Converts Python primitives to their SymPy equivalents so that
    ``constraint.args`` contains only objects that can be:
      * hashed (required for SymPy's Basic.__hash__)
      * serialised by sympy_matching.json_ext
    """
    # SymPy objects are already safe — pass through first to avoid
    # accidentally re-wrapping WildSymbol or other Symbol subclasses.
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
        # Strip trailing underscore — WildSymbol naming convention.
        name = a[:-1] if a.endswith('_') else a
        return sympy.Symbol(name)

    if isinstance(a, (list, tuple)):
        return sympy.Tuple(*(_normalize_constraint_arg(x) for x in a))

    if isinstance(a, dict):
        # Dicts are unhashable; convert to a sorted tuple of (key, value) pairs
        # so the result is both hashable and deterministic.  The subclass
        # __init__ must therefore also accept a tuple-of-pairs for the argument
        # that originally carried a dict (see ExpressionEqQ).
        return tuple(
            sorted(
                (
                    (_normalize_constraint_arg(k), _normalize_constraint_arg(v))
                    for k, v in a.items()
                ),
                key=lambda kv: str(kv[0]),  # sort by string repr of key
            )
        )

    # Callable, set, or other type: leave unchanged; the subclass is
    # responsible for ensuring these are hashable if needed.
    return a


def _collect_wildcards_from_args(args):
    """Recursively collect WildSymbol names from constraint args.

    Returns a sorted list of unique wildcard names.
    """
    names = set()

    def _walk(obj):
        if obj is None:
            return
        # Check if it's a WildSymbol (has wildcard_name attribute)
        if hasattr(obj, 'wildcard_name'):
            names.add(obj.wildcard_name)
        elif isinstance(obj, sympy.Basic):
            # Walk free_symbols of SymPy objects
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
    """Resolve an expression using a substitution dict.

    If expr is a WildSymbol or Symbol that appears in substitution,
    return the substituted value. Otherwise return expr unchanged.
    For SymPy expressions, use xreplace.

    Args:
        expr: A WildSymbol, Symbol, or SymPy expression
        substitution: dict mapping symbol names (str) to matched values

    Returns:
        The resolved expression
    """
    if expr is None:
        return None

    # Direct lookup by wildcard_name
    if hasattr(expr, 'wildcard_name') and expr.wildcard_name in substitution:
        return substitution[expr.wildcard_name]

    # Direct lookup by symbol name
    if isinstance(expr, sympy.Symbol) and expr.name in substitution:
        return substitution[expr.name]

    # For compound expressions, build xreplace dict
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

class MathematicaConstraint(MathematicaExpr, Boolean):
    """Abstract base class for all Wolfram-language pattern constraints.

    Inherits from BOTH :class:`~sympy_wolfram.objects.MathematicaExpr` (so a
    constraint is a proper Mathematica-inspired SymPy node) and SymPy's
    :class:`~sympy.logic.boolalg.Boolean` (enabling logic composition)::

        Not(FreeQ(a, x))   — negation
        And(EqQ(...), ...)  — conjunction
        Or(EqQ(...), ...)   — disjunction

    Subclasses operate at the SymPy level: they receive matched SymPy
    expressions as keyword arguments and return a bool.  They are
    deliberately independent of MatchPy internals; conversion to a
    MatchPy CustomConstraint is handled by
    ``rubi_rules.base_objects._make_matchpy_constraint``.

    Subclasses MUST implement:
        ``check``  — predicate called with substitution dict as kwargs

    The ``variables`` property is auto-computed by scanning ``self.args``
    for WildSymbol instances.

    The invariant ``constraint == constraint.func(*constraint.args)`` is
    guaranteed because:

    * ``__new__`` normalises args and stores them in ``_args`` via
      ``Boolean.__new__``.
    * ``__eq__`` / ``__hash__`` come from ``sympy.Basic`` and compare by
      ``(type, args)``.

    A constraint is a predicate, not a reducible expression, so ``doit`` and
    ``_evaluate`` are overridden to return the node unchanged (its truth value
    is obtained through :meth:`check`, never through Mathematica-style
    evaluation).
    """

    # NOTE: MathematicaExpr already grants instance a ``__dict__`` (it declares
    # no __slots__), so subclass state set in __init__ (_var_name, _value, …)
    # works without re-declaring ``__slots__`` here -- and re-declaring
    # ``('__dict__',)`` would raise "__dict__ slot disallowed: we already got one".

    def __new__(cls, *args, **kwargs):
        # **kwargs are forwarded to __init__ by Python automatically;
        # they are NOT stored in _args because they cannot reliably round-trip
        # through func(*args).  Subclasses that need kwargs-derived state in
        # the invariant must fold that state into positional args instead.
        safe_args = tuple(_normalize_constraint_arg(a) for a in args)
        obj = Boolean.__new__(cls, *safe_args)
        return obj

    def doit(self, **kwargs):
        # A constraint is a predicate, not a reducible expression; MathematicaExpr's
        # default doit would deep-evaluate the args and call _evaluate. Keep the node
        # intact instead -- its truth value comes from check(), not doit().
        return self

    def _evaluate(self, **kwargs):
        return self

    @property
    def variables(self) -> Tuple[str, ...]:
        """Names of the wildcard variables this constraint depends on.

        Auto-computed by scanning self.args for WildSymbol instances.
        """
        return tuple(_collect_wildcards_from_args(self.args))

    @abstractmethod
    def check(self, **substitution) -> bool:
        """Return True iff the constraint is satisfied.

        Args:
            **substitution: wildcard_name -> matched SymPy expression
        """

    @staticmethod
    def _to_sympy(val):
        """Convert a value to SymPy expression (handles MatchPy objects)."""
        if isinstance(val, sympy.Basic):
            return val
        try:
            from sympy_matching.conversion import matchpy_to_sympy
            return matchpy_to_sympy(val)
        except (ImportError, TypeError, AttributeError):
            return sympy.sympify(val)

    def _resolve_all(self, kwargs):
        """Convert all kwargs values to SymPy, return dict for _resolve."""
        return {k: self._to_sympy(v) for k, v in kwargs.items()}

    def _resolve(self, expr, substitution):
        """Convenience method: resolve expr using the substitution dict."""
        return _resolve_with_substitution(expr, substitution)

    # Required by Boolean subclass — no free symbols from SymPy's perspective.
    @property
    def free_symbols(self):
        return set()
