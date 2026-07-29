# -*- coding: utf-8 -*-
"""Rubi constraint objects — base class (re-exported from sympy_wolfram).

The base class ``MathematicaConstraint`` lives in ``sympy_wolfram.constraints``:
it is a thin subclass of ``(MathematicaExpr, SymPyMatchingConstraint)``, where the
generic constraint base ``SymPyMatchingConstraint`` lives in
``sympy_matching/constraint.py``.  Historically the class was called
``RubiConstraint`` and lived in ``sympy_matching.constraints``; ``RubiConstraint``
is kept below only as a deprecated backward-compatibility alias.

All concrete constraints inherit from ``MathematicaConstraint`` and must implement:
    .variables  -> Tuple[str, ...] of wildcard names they inspect
    .check(**kwargs) -> bool  receives matched SymPy expressions, returns bool

These are used in SymPyReplacementPattern.constraints and get converted to MatchPy
CustomConstraint objects by ``sympy_matching.matching_rule._make_matchpy_constraint``
(called from ``build_tracing_replacer``).

``MathematicaConstraint`` inherits from SymPy's Boolean (via
``SymPyMatchingConstraint``) and from ``MathematicaExpr``, so constraints compose
with standard logic operators:  Not(FreeQ(a, x)), And(EqQ(...), ...)

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
