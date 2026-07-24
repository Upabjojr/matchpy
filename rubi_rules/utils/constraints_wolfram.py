# -*- coding: utf-8 -*-
"""Standard Wolfram Mathematica constraint predicates.

These are constraints that are part of the standard Wolfram Mathematica
language (not RUBI-specific). They are implemented as MathematicaConstraint
subclasses for use in Rubi integration rule conditions.

All constraints operate on SymPy expressions after conversion from MatchPy.
"""
import sympy
from sympy import Symbol

from sympy_matching.conversion import matchpy_to_sympy
from sympy_wolfram.constraints import MathematicaConstraint


# =============================================================================
# FreeQ — expression is free of a symbol
# =============================================================================

class FreeQ(MathematicaConstraint):
    """Constraint: matched value(s) are free of a given symbol.

    Mathematica: FreeQ[expr, form] — True if no subexpression matches form.
    In Rubi context:
        FreeQ[a, x]          — checks that 'a' does not contain 'x'.
        FreeQ[{a, b, c}, x]  — checks that ALL of a, b, c are free of 'x'.
    """

    def __init__(self, expr_vars, free_of):
        self._expr_vars = self.args[0]  # tuple or single Symbol
        self._free_of = self.args[1]

    def check(self, **kwargs):
        from .utility_functions import FreeQ as _FreeQ
        sk = self._resolve_all(kwargs)
        free_of = self._free_of  # integration variable, not resolved
        if isinstance(self._expr_vars, (list, tuple, sympy.Tuple)):
            for v in self._expr_vars:
                resolved = self._resolve(v, sk)
                if not _FreeQ(resolved, free_of):
                    return False
            return True
        else:
            resolved = self._resolve(self._expr_vars, sk)
            return _FreeQ(resolved, free_of)

    def __repr__(self):
        if isinstance(self._expr_vars, (list, tuple, sympy.Tuple)):
            inner = ", ".join(str(v) for v in self._expr_vars)
            return f"FreeQ([{inner}], {self._free_of})"
        return f"FreeQ({self._expr_vars}, {self._free_of})"


# =============================================================================
# Single-argument predicates
# =============================================================================

class IntegerQ(MathematicaConstraint):
    """Constraint: matched value is an explicit integer."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import IntegerQ as _IntegerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _IntegerQ(u)
    def __repr__(self):
        return f"IntegerQ({self._u})"


class OddQ(MathematicaConstraint):
    """Constraint: matched value is an odd integer."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import OddQ as _OddQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _OddQ(u)
    def __repr__(self):
        return f"OddQ({self._u})"


class EvenQ(MathematicaConstraint):
    """Constraint: matched value is an even integer."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import EvenQ as _EvenQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _EvenQ(u)
    def __repr__(self):
        return f"EvenQ({self._u})"


class NumberQ(MathematicaConstraint):
    """Constraint: matched value is an explicit numeric quantity."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NumberQ as _NumberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NumberQ(u)
    def __repr__(self):
        return f"NumberQ({self._u})"


class NumericQ(MathematicaConstraint):
    """Constraint: matched value is numeric (including constants like pi, E)."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NumericQ as _NumericQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NumericQ(u)
    def __repr__(self):
        return f"NumericQ({self._u})"


class AtomQ(MathematicaConstraint):
    """Constraint: matched value is atomic (symbol, number, etc.)."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import AtomQ as _AtomQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _AtomQ(u)
    def __repr__(self):
        return f"AtomQ({self._u})"


class PositiveQ(MathematicaConstraint):
    """Constraint: matched value is positive."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import PositiveQ as _PositiveQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PositiveQ(u)
    def __repr__(self):
        return f"PositiveQ({self._u})"


class NegativeQ(MathematicaConstraint):
    """Constraint: matched value is negative."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import NegativeQ as _NegativeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _NegativeQ(u)
    def __repr__(self):
        return f"NegativeQ({self._u})"


class PrimeQ(MathematicaConstraint):
    """Constraint: matched value is a prime number."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return u.is_prime is True
    def __repr__(self):
        return f"PrimeQ({self._u})"


# =============================================================================
# Two-argument predicates
# =============================================================================

class MemberQ(MathematicaConstraint):
    """Constraint: matched value is a member of a given list."""
    def __init__(self, u, members):
        self._u = self.args[0]
        self._members = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import MemberQ as _MemberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        members = self._members if isinstance(self._members, (list, tuple)) else [self._members]
        return _MemberQ(list(members), u)
    def __repr__(self):
        return f"MemberQ({self._u}, {self._members})"


class PolynomialQ(MathematicaConstraint):
    """Constraint: matched value is a polynomial in the integration variable."""
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]
    def check(self, **kwargs):
        from .utility_functions import PolynomialQ as _PolynomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return _PolynomialQ(u, self._x)
    def __repr__(self):
        return f"PolynomialQ({self._u}, {self._x})"


class TrueQ(MathematicaConstraint):
    """Constraint: matched value is explicitly True."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        if hasattr(u, 'doit'):
            u = u.doit()
        return u is sympy.true or u == True
    def __repr__(self):
        return f"TrueQ({self._u})"


class FalseQ(MathematicaConstraint):
    """Constraint: matched value is explicitly False."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import FalseQ as _FalseQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        if hasattr(u, 'doit'):
            u = u.doit()
        return _FalseQ(u)
    def __repr__(self):
        return f"FalseQ({self._u})"


class UnsameQ(MathematicaConstraint):
    """Constraint: two matched values are not identical (structurally different).

    Mathematica: UnsameQ[expr1, expr2] — True if expr1 and expr2 are not identical.
    This is structural inequality (not mathematical inequality).
    """
    def __init__(self, a, b):
        self._a = self.args[0]
        self._b = self.args[1]
    def check(self, **kwargs):
        sk = self._resolve_all(kwargs)
        a = self._resolve(self._a, sk)
        b = self._resolve(self._b, sk)
        return a != b
    def __repr__(self):
        return f"UnsameQ({self._a}, {self._b})"

class MatchQ(MathematicaConstraint):
    """Mathematica ``MatchQ[expr, pattern]`` -- does *expr* match *pattern*?

    The pattern may carry its own guard, ``pattern /; test``, which arrives here as
    a ``Condition(pattern, test)`` node; the match counts only if the test holds
    under that match's bindings.

    Variable scoping is the subtle part. A ``MatchQ`` pattern mixes two kinds of
    name:

    * names the ENCLOSING rule already bound (``a``, ``b`` in
      ``MatchQ[u, (a+b*x)^m_]``) -- these arrive in *kwargs* and are substituted in,
      so they match only their actual values;
    * names LOCAL to the MatchQ (``m_`` above) -- these are not part of the outer
      match, stay free here, and are what the matching actually solves for.

    The distinction is simply whether the name was bound by the outer pattern, which
    is what `_make_matchpy_constraint` uses to decide which variables to declare.
    """

    def __init__(self, u, pattern):
        self._u = self.args[0]
        self._pattern = self.args[1]

    def check(self, **kwargs):
        resolved = self._resolve_all(kwargs)
        subject = self._resolve(self._u, resolved)
        pattern = self._resolve(self._pattern, resolved)
        return _pattern_matches(subject, pattern)

    def __repr__(self):
        return f"MatchQ({self._u}, {self._pattern})"


def _pattern_matches(subject, pattern) -> bool:
    """True iff *subject* matches *pattern*, honouring a ``pattern /; test`` guard.

    Any wildcard still free in *pattern* is a MatchQ-local pattern variable (see
    :class:`MatchQ`); MatchPy solves for those. A guard is evaluated once per
    candidate match, with that match's bindings substituted in, so
    ``MatchQ[u, (c+d*x)^m /; FreeQ[{c,d,m},x]]`` accepts only matches whose c, d, m
    are actually free of x.
    """
    from matchpy import match as _match
    from matchpy.expressions.expressions import Pattern
    from sympy_matching.conversion import to_expression, matchpy_to_sympy

    test = None
    if type(pattern).__name__ == 'Condition' and len(getattr(pattern, 'args', ())) == 2:
        pattern, test = pattern.args

    try:
        subject_expr = to_expression(subject)
        pattern_expr = Pattern(to_expression(pattern))
    except Exception:
        return False

    try:
        for substitution in _match(subject_expr, pattern_expr):
            if test is None:
                return True
            bindings = {name: matchpy_to_sympy(value)
                        for name, value in substitution.items()}
            if _guard_holds(test, bindings):
                return True
    except Exception:
        # An un-convertible subject or an unmatchable pattern is simply "no match";
        # it must never abort the surrounding rule search.
        return False
    return False


def _guard_holds(test, bindings) -> bool:
    """Evaluate a MatchQ pattern's ``/;`` guard under one match's bindings."""
    from sympy_wolfram.constraints import MathematicaConstraint as _RC

    if isinstance(test, sympy.logic.boolalg.Not):
        return not _guard_holds(test.args[0], bindings)
    if isinstance(test, sympy.logic.boolalg.And):
        return all(_guard_holds(a, bindings) for a in test.args)
    if isinstance(test, sympy.logic.boolalg.Or):
        return any(_guard_holds(a, bindings) for a in test.args)
    if isinstance(test, _RC):
        try:
            return bool(test.check(**bindings))
        except Exception:
            return False
    try:
        value = test.xreplace({sympy.Symbol(k): v for k, v in bindings.items()})
        if hasattr(value, 'doit'):
            value = value.doit()
        return value is True or value == sympy.true
    except Exception:
        return False


# =============================================================================
# Legacy helpers (kept for backwards compat with tests)
# =============================================================================

def _to_sympy(val):
    """Convert a value to SymPy expression."""
    if isinstance(val, sympy.Basic):
        return val
    try:
        return matchpy_to_sympy(val)
    except (TypeError, AttributeError):
        return sympy.sympify(val)


def _get_var_name(var) -> str:
    """Extract variable name from various input types (DEPRECATED)."""
    if isinstance(var, str):
        return var[:-1] if var.endswith('_') else var
    if hasattr(var, 'wildcard_name'):
        return var.wildcard_name
    return str(var)


__all__ = [
    'FreeQ', 'IntegerQ', 'OddQ', 'EvenQ', 'NumberQ', 'NumericQ',
    'AtomQ', 'MemberQ', 'PositiveQ', 'NegativeQ', 'PolynomialQ',
    'TrueQ', 'FalseQ', 'MatchQ', 'PrimeQ', 'UnsameQ', '_to_sympy', '_get_var_name',
]
