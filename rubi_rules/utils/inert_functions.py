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

# Reciprocal pairs: sin<->csc, cos<->sec, tan<->cot. A PURE negative-integer power
# of an inert head is definitionally a positive power of its reciprocal head, and
# the generated rule corpus (like Rubi's own) writes its patterns over the
# reciprocal head -- 4.5.10-class rules match `(c+d x)^m csc[u]^2`, never
# `(c+d x)^m sin[u]^-2`. Rubi's half-angle rules legitimately EMIT the latter
# shape ((2 a)^n (c+d x)^m Sin[...]^(2 n) with n<0), so without this
# normalisation those chains dead-ended in Unintegrable -- e.g.
# Int[(c+d x)^2/(a+a cos)] and x/Sqrt[a+a cos].
_INERT_RECIPROCAL = {InertSin: InertCsc, InertCos: InertSec, InertTan: InertCot,
                     InertCsc: InertSin, InertSec: InertCos, InertCot: InertTan}


def fix_reciprocal_inert_powers(u):
    """Rewrite every pure negative-integer power of an inert trig head as the
    positive power of its reciprocal head (``1/InertSin(v)**2 -> InertCsc(v)**2``).

    Only bare ``head(v)**(-k)`` factors are touched; composite bases like
    ``(a + b*InertSin(v))**(-k)`` are left alone (rules bind those via a
    wildcard exponent).
    """
    from sympy import Pow

    def _is_recip_power(p):
        return (p.is_Pow and p.exp.is_Integer and p.exp.is_negative
                and p.base.func in _INERT_RECIPROCAL)

    return u.replace(_is_recip_power,
                     lambda p: _INERT_RECIPROCAL[p.base.func](*p.base.args) ** (-p.exp))
