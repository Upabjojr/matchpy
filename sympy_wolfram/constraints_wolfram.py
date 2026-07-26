# -*- coding: utf-8 -*-
"""Concrete standard-Wolfram constraint predicates.

These are constraints that are part of the standard Wolfram Mathematica
language (not Rubi-specific), implemented as :class:`MathematicaConstraint`
subclasses.  They live here (rather than in ``rubi_rules``) because their bodies
depend solely on ``sympy_wolfram`` — the base constraint class and the eager
Wolfram helpers they delegate to are both in this layer.  ``rubi_rules`` imports
them back (the correct layer direction: rubi_rules -> sympy_wolfram).

Only constraints whose logic is purely Wolfram-standard belong here.  The
Rubi-specific ones stay in ``rubi_rules.utils.constraints_rubi``; the remaining
standard ones in ``rubi_rules.utils.constraints_wolfram`` are being migrated
here as they are shown to be free of Rubi coupling.
"""
import sympy

from sympy_wolfram.constraints import MathematicaConstraint


class FreeQ(MathematicaConstraint):
    """Constraint: matched value(s) are free of a given symbol.

    Mathematica: FreeQ[expr, form] — True if no subexpression matches form.
    In Rubi context:
        FreeQ[a, x]          — checks that 'a' does not contain 'x'.
        FreeQ[{a, b, c}, x]  — checks that ALL of a, b, c are free of 'x'.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_FreeQ` predicate.
    """

    def __init__(self, expr_vars, free_of):
        self._expr_vars = self.args[0]  # tuple or single Symbol
        self._free_of = self.args[1]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_FreeQ
        sk = self._resolve_all(kwargs)
        free_of = self._free_of  # integration variable, not resolved
        if isinstance(self._expr_vars, (list, tuple, sympy.Tuple)):
            for v in self._expr_vars:
                resolved = self._resolve(v, sk)
                if not eager_FreeQ(resolved, free_of):
                    return False
            return True
        else:
            resolved = self._resolve(self._expr_vars, sk)
            return eager_FreeQ(resolved, free_of)

    def __repr__(self):
        if isinstance(self._expr_vars, (list, tuple, sympy.Tuple)):
            inner = ", ".join(str(v) for v in self._expr_vars)
            return f"FreeQ([{inner}], {self._free_of})"
        return f"FreeQ({self._expr_vars}, {self._free_of})"


class IntegerQ(MathematicaConstraint):
    """Constraint: matched value is an explicit integer.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_IntegerQ`.
    """
    def __init__(self, u):
        self._u = self.args[0]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_IntegerQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_IntegerQ(u)

    def __repr__(self):
        return f"IntegerQ({self._u})"


class PositiveQ(MathematicaConstraint):
    """Constraint: matched value is positive.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_PositiveQ`.
    """
    def __init__(self, u):
        self._u = self.args[0]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_PositiveQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_PositiveQ(u)

    def __repr__(self):
        return f"PositiveQ({self._u})"


class MemberQ(MathematicaConstraint):
    """Constraint: matched value is a member of a given list.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_MemberQ` (which
    reconciles function-head wildcards against class/HeadRef membership lists).
    """
    def __init__(self, u, members):
        self._u = self.args[0]
        self._members = self.args[1]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_MemberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        members = self._members if isinstance(self._members, (list, tuple)) else [self._members]
        return eager_MemberQ(list(members), u)

    def __repr__(self):
        return f"MemberQ({self._u}, {self._members})"


class NumberQ(MathematicaConstraint):
    """Constraint: matched value is an explicit numeric quantity.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_NumberQ`.
    """
    def __init__(self, u):
        self._u = self.args[0]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_NumberQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_NumberQ(u)

    def __repr__(self):
        return f"NumberQ({self._u})"


class AtomQ(MathematicaConstraint):
    """Constraint: matched value is atomic (symbol, number, etc.).

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_AtomQ`.
    """
    def __init__(self, u):
        self._u = self.args[0]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_AtomQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_AtomQ(u)

    def __repr__(self):
        return f"AtomQ({self._u})"


class PolynomialQ(MathematicaConstraint):
    """Constraint: matched value is a polynomial in the integration variable.

    Delegates to the eager :func:`sympy_wolfram.functions_eager.eager_PolynomialQ`.
    """
    def __init__(self, u, x):
        self._u = self.args[0]
        self._x = self.args[1]

    def check(self, **kwargs):
        from sympy_wolfram.functions_eager import eager_PolynomialQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_PolynomialQ(u, self._x)

    def __repr__(self):
        return f"PolynomialQ({self._u}, {self._x})"


__all__ = ['FreeQ', 'IntegerQ', 'PositiveQ', 'MemberQ', 'NumberQ', 'AtomQ', 'PolynomialQ']
