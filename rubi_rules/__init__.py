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
import sys

# Python 3.11+ caps int->str conversion at 4300 digits as a DoS guard. Rubi
# reduction chains legitimately build much larger exact integer coefficients
# (a runaway (a+b sin^4)^p chain crashed mid-DFS when matchpy's commutative
# operand sort str()-ified one), and Mathematica has no such limit -- a huge
# chain should run into the step budget or the caller's timeout, not a
# ValueError from the printer. Lift the cap for the whole process.
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
