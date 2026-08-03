# -*- coding: utf-8 -*-
"""Rubi rule code generator.

Translates Rubi fullformlist JSON (produced by the Rubi FullFormList Parser notebook)
into Python source code using OmniMatch patterns and SymPy expressions.
"""
from .generate import RubiRuleTranslator
