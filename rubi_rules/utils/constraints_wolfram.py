# -*- coding: utf-8 -*-
"""Standard Wolfram Mathematica constraint predicates.

These are constraints that are part of the standard Wolfram Mathematica
language (not RUBI-specific). They are implemented as MathematicaConstraint
subclasses for use in Rubi integration rule conditions.

All constraints operate on SymPy expressions after conversion from OmniMatch.
"""
import sympy
from sympy import Symbol

from sympy_matching.conversion import omnimatch_to_sympy
from sympy_wolfram.constraints import MathematicaConstraint

# FreeQ, IntegerQ, PositiveQ, MemberQ, NumberQ, AtomQ and PolynomialQ are standard
# Wolfram-library constraints (not Rubi-specific), so they now live in sympy_wolfram;
# re-exported here so rubi_rules.utils and the generated rules keep importing them
# from this module unchanged.
from sympy_wolfram.constraints_wolfram import (
    FreeQ, IntegerQ, PositiveQ, MemberQ, NumberQ, AtomQ, PolynomialQ,
)


# =============================================================================
# Single-argument predicates
# =============================================================================

class OddQ(MathematicaConstraint):
    """Constraint: matched value is an odd integer."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import eager_OddQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_OddQ(u)
    def __repr__(self):
        return f"OddQ({self._u})"


class EvenQ(MathematicaConstraint):
    """Constraint: matched value is an even integer."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import eager_EvenQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_EvenQ(u)
    def __repr__(self):
        return f"EvenQ({self._u})"


class NumericQ(MathematicaConstraint):
    """Constraint: matched value is numeric (including constants like pi, E)."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import eager_NumericQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_NumericQ(u)
    def __repr__(self):
        return f"NumericQ({self._u})"


class NegativeQ(MathematicaConstraint):
    """Constraint: matched value is negative."""
    def __init__(self, u):
        self._u = self.args[0]
    def check(self, **kwargs):
        from .utility_functions import eager_NegativeQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        return eager_NegativeQ(u)
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
        from .utility_functions import eager_FalseQ
        sk = self._resolve_all(kwargs)
        u = self._resolve(self._u, sk)
        if hasattr(u, 'doit'):
            u = u.doit()
        return eager_FalseQ(u)
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
        # Evaluate deferred nodes BEFORE comparing. The 9.3/9.4 catch-all rules guard
        # with UnsameQ(NormalizeIntegrand(u_, x), u_); without doit() the left side
        # stays an unevaluated node, structurally != u for EVERY integrand, so the
        # catch-all fired unconditionally, rewriting Int[u,x] -> Int[u,x] until the
        # cycle detector stopped it -- pure wasted DFS work on every slow integral.
        if hasattr(a, 'doit'):
            try:
                a = a.doit()
            except Exception:
                pass
        if hasattr(b, 'doit'):
            try:
                b = b.doit()
            except Exception:
                pass
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
    is what `_make_omnimatch_constraint` uses to decide which variables to declare.
    """

    # STRUCTURAL constraint: the pattern argument must stay an UNEVALUATED tree
    # (evaluating e.g. Complex(0, j_) to I*j would change what it matches), so opt
    # out of MathematicaConstraint._resolve's argument evaluation.
    _EVAL_RESOLVED_ARGS = False

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
    :class:`MatchQ`); OmniMatch solves for those. A guard is evaluated once per
    candidate match, with that match's bindings substituted in, so
    ``MatchQ[u, (c+d*x)^m /; FreeQ[{c,d,m},x]]`` accepts only matches whose c, d, m
    are actually free of x.
    """
    from omnimatch import match as _match
    from omnimatch.expressions.expressions import Pattern
    from sympy_matching.conversion import to_omnimatch_expression, omnimatch_to_sympy

    test = None
    if type(pattern).__name__ == 'Condition' and len(getattr(pattern, 'args', ())) == 2:
        pattern, test = pattern.args

    try:
        subject_expr = to_omnimatch_expression(subject)
        pattern_expr = Pattern(to_omnimatch_expression(pattern))
    except Exception:
        return False

    try:
        for substitution in _match(subject_expr, pattern_expr):
            if test is None:
                return True
            bindings = {name: omnimatch_to_sympy(value)
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
        return omnimatch_to_sympy(val)
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
