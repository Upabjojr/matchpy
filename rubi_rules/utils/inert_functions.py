# -*- coding: utf-8 -*-
"""Inert trig-function markers for Rubi's deactivation dispatch.

Rubi distinguishes *active* trig functions (SymPy's ``sin``, ``cos``, ...) from
*inert* ones.  While integrating it deactivates the active functions into inert
markers so their operands are never auto-simplified, applies the inert-trig
rules, then reactivates (see ``rubi_rules.base_objects`` and the project note
``rubi-trig-deactivation-dispatch``).

We model an inert trig function as a plain undefined ``Function('InertSin')`` etc.
-- an *undefined* function SymPy never evaluates or rewrites (``InertSin(0)`` stays
unevaluated, whereas ``sin(0)`` collapses to ``0``).  The head is DELIBERATELY named
``InertSin`` (not ``sin``) and is NOT a subclass of ``sympy.sin``: an inert marker
must print DISTINCTLY from the active function so an un-reactivated leaf is visible
rather than masquerading as a correct ``sin(x)``.  All inert detection keys off
object identity (``_INERT_TO_ACTIVE`` / ``_INERT_TRIG_HEADS``), never the head name.
"""
from sympy.core.function import Function
from sympy.functions.elementary.trigonometric import sin, cos, tan, cot, sec, csc

InertSin = Function('InertSin')
InertCos = Function('InertCos')
InertTan = Function('InertTan')
InertCot = Function('InertCot')
InertSec = Function('InertSec')
InertCsc = Function('InertCsc')

# Maps each inert marker to the active SymPy function it reactivates to.
_INERT_TO_ACTIVE = {InertSin: sin, InertCos: cos, InertTan: tan,
                    InertCot: cot, InertSec: sec, InertCsc: csc}
_INERT_TRIG_HEADS = tuple(_INERT_TO_ACTIVE)
