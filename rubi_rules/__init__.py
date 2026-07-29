# -*- coding: utf-8 -*-
"""Rubi integration rules for MatchPy.

This package provides:
- base_objects.py: Core objects (Int, SymPyReplacementPattern, build_tracing_replacer,
  rubi_integrate, load_rule_patterns)
- utils/: Constraint helpers (FreeQ, NeQ, IntegerQ, etc.)
- rules/: Auto-generated rule modules mirroring the Rubi Mathematica structure.
  DO NOT EDIT files in rules/ — they are produced by `codegen/generate.py`.
- codegen/: Code generator that translates Rubi Mathematica rules (from fullformlist
  JSON) into Python SymPyReplacementPattern definitions.

Usage:
    from rubi_rules.base_objects import rubi_integrate, Int
    import sympy
    x = sympy.Symbol('x')
    result = rubi_integrate(1/x, x)  # => log(x)

    # Or load a specific subset of rules (returns a tuple of SymPyReplacementPattern;
    # feed it to build_tracing_replacer to obtain a replacer):
    from rubi_rules.base_objects import load_rule_patterns, build_tracing_replacer
    rules = load_rule_patterns('r_1_algebraic_functions/r_1_1_binomial_products/**')
    replacer = build_tracing_replacer(rules)
"""
