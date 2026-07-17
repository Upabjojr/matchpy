# -*- coding: utf-8 -*-
"""Standard Wolfram Mathematica constraint predicates.

These are constraints that are part of the standard Wolfram Mathematica
language (not RUBI-specific). They are implemented as RubiConstraint
subclasses for use in Rubi integration rule conditions.

All constraints operate on SymPy expressions after conversion from MatchPy.
"""
import sympy
from sympy import Symbol

from sympy_objects.conversion import matchpy_to_sympy
from sympy_objects.constraints import RubiConstraint


# =============================================================================
# FreeQ — expression is free of a symbol
# =============================================================================

class FreeQ(RubiConstraint):
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

class IntegerQ(RubiConstraint):
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


class OddQ(RubiConstraint):
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


class EvenQ(RubiConstraint):
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


class NumberQ(RubiConstraint):
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


class NumericQ(RubiConstraint):
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


class AtomQ(RubiConstraint):
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


class PositiveQ(RubiConstraint):
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


class NegativeQ(RubiConstraint):
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


class PrimeQ(RubiConstraint):
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

class MemberQ(RubiConstraint):
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


class PolynomialQ(RubiConstraint):
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


class TrueQ(RubiConstraint):
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


class FalseQ(RubiConstraint):
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


class UnsameQ(RubiConstraint):
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

class MatchQ(RubiConstraint):
    """Constraint: matched value matches a given pattern."""
    def __init__(self, u, pattern):
        self._u = self.args[0]
        self._pattern = self.args[1]
    def check(self, **kwargs):
        return True  # pattern matching is complex; stub
    def __repr__(self):
        return f"MatchQ({self._u}, {self._pattern})"


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
