# -*- coding: utf-8 -*-
"""Rubi constraint objects — base class (re-exported from sympy_objects).

RubiConstraint now lives in sympy_objects.constraints so that it is
independent of rubi_rules and MatchPy.

All concrete constraints inherit from RubiConstraint and must implement:
    .variables  -> Tuple[str, ...] of wildcard names they inspect
    .check(**kwargs) -> bool  receives matched SymPy expressions, returns bool

These are used in RubiRulePattern.constraints and get converted to
MatchPy CustomConstraint objects by base_objects.build_replacer().

RubiConstraint inherits from SymPy's Boolean so that constraints can be
composed with standard logic operators:  Not(FreeQ(a, x)), And(EqQ(...), ...)

Concrete constraint subclasses live in:
    - constraints_wolfram.py  (standard Mathematica predicates: FreeQ, IntegerQ, ...)
    - constraints_rubi.py     (RUBI-specific predicates: EqQ, IGtQ, PolyQ, ...)
"""
# Re-export from sympy_objects so existing imports keep working.
from sympy_objects.constraints import RubiConstraint  # noqa: F401

__all__ = ['RubiConstraint']
