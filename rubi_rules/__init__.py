# -*- coding: utf-8 -*-
"""Rubi integration rules for MatchPy.

This package provides:
- base_objects.py: Core objects (Int, RubiRulePattern, build_replacer, rubi_integrate)
- utils/: Constraint helpers (FreeQ, NeQ, IntegerQ, etc.)
- rules/: Auto-generated rule modules mirroring the Rubi Mathematica structure.
  DO NOT EDIT files in rules/ — they are produced by `codegen/generate.py`.
- codegen/: Code generator that translates Rubi Mathematica rules (from fullformlist
  JSON) into Python RubiRulePattern definitions.

Usage:
    from rubi_rules.base_objects import rubi_integrate, Int
    import sympy
    x = sympy.Symbol('x')
    result = rubi_integrate(1/x, x)  # => log(x)

    # Or load a specific subset of rules:
    from rubi_rules.base_objects import load_rules
    replacer = load_rules('r_1_algebraic/r_1_1_binomial_products/**')
"""
