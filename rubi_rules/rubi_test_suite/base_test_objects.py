# -*- coding: utf-8 -*-
"""Core objects for generated Rubi test-suite cases."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from sympy import Expr as SymPyExpr
from sympy import Symbol as SymPySymbol


class RubiTestSuiteCase(BaseModel):
    """One MathematicaSyntaxTestSuite case translated to Python/SymPy."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    integrand: SymPyExpr
    variable: SymPySymbol
    num_steps: int
    integral: SymPyExpr
