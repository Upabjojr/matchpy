# -*- coding: utf-8 -*-
"""Rubi constraint objects — base class (re-exported from sympy_wolfram).

The base class ``MathematicaConstraint`` lives in ``sympy_wolfram.constraints``
so that it is independent of rubi_rules and MatchPy, and can inherit from
``sympy_wolfram.objects.MathematicaExpr``.  It used to be called
``RubiConstraint`` and live in ``sympy_matching.constraints``; ``RubiConstraint``
is kept below only as a deprecated backward-compatibility alias.

All concrete constraints inherit from ``MathematicaConstraint`` and must implement:
    .variables  -> Tuple[str, ...] of wildcard names they inspect
    .check(**kwargs) -> bool  receives matched SymPy expressions, returns bool

These are used in RubiRulePattern.constraints and get converted to
MatchPy CustomConstraint objects by base_objects.build_replacer().

``MathematicaConstraint`` inherits from SymPy's Boolean (and MathematicaExpr) so
that constraints compose with standard logic operators:  Not(FreeQ(a, x)),
And(EqQ(...), ...)

Concrete constraint subclasses live in:
    - constraints_wolfram.py  (standard Mathematica predicates: FreeQ, IntegerQ, ...)
    - constraints_rubi.py     (RUBI-specific predicates: EqQ, IGtQ, PolyQ, ...)
"""
# Re-export from sympy_wolfram so existing imports keep working.
from sympy_wolfram.constraints import MathematicaConstraint  # noqa: F401

# Deprecated alias: the class was renamed from RubiConstraint. Kept so any lingering
# `from rubi_rules.utils.constraints import RubiConstraint` keeps working.
RubiConstraint = MathematicaConstraint

__all__ = ['MathematicaConstraint', 'RubiConstraint']
