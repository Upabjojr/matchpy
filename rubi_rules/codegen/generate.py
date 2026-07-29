#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate MatchPy integration rules from the Rubi pre-computed JSON.

Usage (from matchpy-wip/matchpy/ directory):
    python -B -m rubi_rules.codegen.generate [--json PATH] [--output-dir DIR] [--filter REGEX]

The script reads the pre-computed fullformlist JSON produced from the Rubi
Mathematica repository and translates every entry into a Python module of
SymPyReplacementPattern definitions.

Defaults:
    --json     : rubi_fullformlist_results.json
    --output-dir: rubi_rules/  (auto-detected relative to this script)
    --filter   : no filter — generate everything
"""
import argparse
import copy
import itertools
import json
import re
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

from rubi_rules.utils import rubi_utils
from sympy_wolfram import FFLConverter
from sympy_wolfram import objects as wolfram_objects
from sympy_wolfram.interpreter import ffl_to_sympy_short_code
from sympy import Symbol as _sympy_Symbol


# =============================================================================
# Rubi-specific FFL helpers (operate on Int[integrand, x_Symbol] structure)
# =============================================================================

def _rewrite_gamma_arity(node):
    """Split Mathematica's overloaded ``Gamma`` by arity, for the rubi layer.

    ``Gamma[a]`` is the complete gamma function (SymPy ``gamma``) while
    ``Gamma[a, z]`` is the UPPER INCOMPLETE one (SymPy ``uppergamma``) -- one Wolfram
    head, two different SymPy functions, so it cannot be expressed as a name mapping
    the way the other overrides in ``_EXTRA_SYMPY_HEADS`` are. Rewriting the head to a
    private arity-tagged name lets the ordinary mapping machinery finish the job.

    Without this the rules kept the Wolfram ``Gamma`` NODE in their patterns, which no
    caller's expression can ever match (they pass ``gamma(a)`` / ``uppergamma(a, z)``),
    so all 17 of those rules were dead.
    """
    if not isinstance(node, list) or not node:
        return node
    rewritten = [_rewrite_gamma_arity(child) for child in node]
    if rewritten[0] == 'Gamma':
        if len(rewritten) == 2:
            rewritten[0] = 'Gamma$Complete'
        elif len(rewritten) == 3:
            rewritten[0] = 'Gamma$Upper'
    return rewritten


def _rubi_override_sympy_names() -> Dict[str, Any]:
    """Bare SymPy names introduced by the rubi_rules-level overrides.

    ``_EXTRA_SYMPY_HEADS`` translates Wolfram heads to SymPy functions for THIS layer
    (see :func:`_build_pattern_custom_functions`). The emitter writes them qualified
    (``sympy.expint(...)``), but the shortening printer prints them BARE
    (``expint(...)``) -- so unless the bare name is both importable in the generated
    module and present in the shortening namespace, the round-trip's verification eval
    raises NameError and the shortener SILENTLY keeps the verbose form. That is what
    left ~100 rules reading ``(Integer(-1) * sympy.expint(...)) * (_b_)**(Integer(-1))``
    instead of ``-expint(n_ + 1, ...)/_b_``.
    """
    import sympy as _sympy
    names: Dict[str, Any] = {}
    for target in _EXTRA_SYMPY_HEADS.values():
        if not target.startswith('sympy.'):
            continue
        bare = target.split('.', 1)[1]
        obj = getattr(_sympy, bare, None)
        if obj is not None:
            names[bare] = obj
    return names


def _sympy_import_line() -> str:
    """The generated-module ``from sympy import (...)`` line for every SymPy name that
    may appear UNQUALIFIED in emitted rule code.

    Built from the SAME single source as the shortening eval namespace
    (:meth:`FFLConverter.generated_code_sympy_names`), so a name is importable in the
    generated file IFF it is evaluable during shortening. This is what keeps the two in
    lock-step: adding a function to ``SYMPY_FUNC_MAP`` makes it both importable here and
    resolvable in the round-trip, with no second list to update.
    """
    import textwrap
    names = sorted(set(FFLConverter.generated_code_sympy_names())
                   | set(_rubi_override_sympy_names()))
    body = textwrap.fill(', '.join(names), width=100,
                         initial_indent='    ', subsequent_indent='    ')
    return f"from sympy import (\n{body},\n)"


def _integration_variable(lhs) -> str:
    """Name of the integration variable in an ``Int[integrand, x_Symbol]`` LHS.

    Rubi writes most rules over ``x`` but a few use another letter. Whatever it is
    called in the source, it is BOUND by the rule (it is the variable being
    integrated over), so it must never be translated into a pattern wildcard --
    it is passed to the converter as a reserved symbol mapped to the identifier
    ``x``, which is the canonical variable the emitted modules declare.
    """
    if isinstance(lhs, list) and lhs[0] == 'Int' and len(lhs) >= 3:
        var_pat = lhs[2]
        if isinstance(var_pat, list) and var_pat[0] == 'Pattern':
            return var_pat[1]
    return 'x'


# The canonical identifier every generated module declares for the integration
# variable (`x = Symbol('x')` in the header).
CANONICAL_VAR = 'x'


def _reserved_symbols(lhs) -> Dict[str, str]:
    """Reserved-symbol map for a rule: its integration variable -> ``x``."""
    return {_integration_variable(lhs): CANONICAL_VAR}


def _collect_wildcards_from_rules(converter, rules):
    """Pre-scan FFL rules to collect all wildcard AND plain-symbol names.

    Assumes rules are SetDelayed[Int[...], ...] structure.
    Returns (non_optional_set, optional_set, plain_symbol_set). The plain symbols
    (scoping locals like r/s/k/u, selector symbols, ...) are declared once at the top
    of the module so the emitted code can reference them bare (`r`) instead of
    building `Symbol('r')` inline inside every binding.
    """
    all_non_optional = set()
    all_optional = set()
    all_symbols = set()
    for rule in rules:
        if not isinstance(rule, list) or not rule or rule[0] != 'SetDelayed':
            continue
        if len(rule) < 3:
            continue
        lhs = rule[1]
        rhs = rule[2]
        if not isinstance(lhs, list) or lhs[0] != 'Int':
            continue
        converter.reset()
        converter.reserved_symbols = _reserved_symbols(lhs)
        # Rewrite function-head wildcards F_[..] into WildHeadApp[F_, ..] first, so
        # converting the pattern discovers F and the argument wildcards normally
        # (the raw form has a non-string head and would abort the scan early).
        _lhs_pattern, _ = _extract_fhw_from_pattern(lhs[1])
        try:
            converter.convert(_lhs_pattern, is_pattern=True)
        except Exception:
            pass
        try:
            # Same MatchQ rewrite as in translation, so a head wildcard local to a
            # guard (e.g. `trig`) is discovered here and gets declared in the
            # module -- otherwise the emitted constraint references an undefined name.
            converter.convert(_rewrite_fhw_in_matchq(rhs), is_pattern=True)
        except Exception:
            pass
        all_non_optional.update(converter.wildcards_non_optional)
        all_optional.update(converter.wildcards_optional)
        all_symbols.update(converter._bare_locals)
    return all_non_optional, all_optional, all_symbols


def _with_binding_substitutions(bindings_ffl) -> Dict[str, object]:
    """Extract simple ``With[{x = value, ...}, ...]`` substitutions from FFL."""
    subs: Dict[str, object] = {}
    if not isinstance(bindings_ffl, list) or not bindings_ffl or bindings_ffl[0] != 'List':
        return subs
    for item in bindings_ffl[1:]:
        if (
            isinstance(item, list)
            and len(item) >= 3
            and item[0] == 'Set'
            and isinstance(item[1], str)
        ):
            subs[item[1]] = item[2]
    return subs


def _ffl_substitute_symbols(expr, substitutions: Dict[str, object]):
    """Recursively substitute simple symbol atoms in an FFL expression."""
    if isinstance(expr, str):
        if expr in substitutions:
            return copy.deepcopy(substitutions[expr])
        return expr
    if isinstance(expr, list):
        return [_ffl_substitute_symbols(part, substitutions) for part in expr]
    return expr


def _ffl_is_fhw_head(node) -> bool:
    """True if `node` is a function-head-wildcard application ``F_[args...]``:
    a list whose head is itself a ``Pattern[F, Blank[]]`` (a wildcard as head)."""
    return bool(isinstance(node, list) and node
                and isinstance(node[0], list) and node[0]
                and node[0][0] == 'Pattern')


def _ffl_is_deriv_head(node) -> bool:
    """True for Rubi's ``Derivative[n][f][x]``.

    Its FFL head is itself an application, ``[['Derivative', n], f]`` -- i.e. the
    operator ``Derivative[n]`` applied to the function ``f``, the whole thing then
    applied to ``x``. Both ``n`` and ``f`` are usually wildcards.
    """
    return bool(isinstance(node, list) and len(node) >= 2
                and isinstance(node[0], list) and len(node[0]) == 2
                and isinstance(node[0][0], list) and len(node[0][0]) == 2
                and node[0][0][0] == 'Derivative')


def _collect_pattern_names(node, out):
    """Collect the names of all ``Pattern[name, ...]`` wildcards in `node`."""
    if isinstance(node, list) and node:
        if node[0] == 'Pattern' and len(node) >= 2 and isinstance(node[1], str):
            out.add(node[1])
        for c in node:
            _collect_pattern_names(c, out)


def _extract_fhw_from_pattern(pattern_ffl):
    """Rewrite every function-head wildcard ``F_[args...]`` in a pattern FFL into
    ``WildHeadApp[F_, args...]``.

    MatchPy supports a WILDCARD OPERATION HEAD (see
    ``matchpy.expressions.expressions.WildcardOperationHead``), so such a pattern
    matches an application of ANY function, binding the head to ``F`` and matching
    the arguments normally -- argument wildcards and their constraints therefore
    behave exactly as in an ordinary pattern.

    Returns (new_pattern_ffl, head_names).
    """
    head_names = set()

    def rec(node):
        if not isinstance(node, list) or not node:
            return node
        if _ffl_is_deriv_head(node):
            order, fpat, var = node[0][0][1], node[0][1], node[1]
            if isinstance(fpat, list) and fpat and fpat[0] == 'Pattern':
                head_names.add(fpat[1])
            return ['WildHeadDeriv', fpat, rec(var), rec(order)]
        if _ffl_is_fhw_head(node):
            head_pat = node[0]           # Pattern[F, Blank]
            head_names.add(head_pat[1])  # 'F'
            return ['WildHeadApp', head_pat] + [rec(a) for a in node[1:]]
        return [rec(c) for c in node]

    return rec(pattern_ffl), head_names


def _rewrite_fhw_in_replacement(node, head_map):
    """In a replacement FFL, rewrite each ``F[args...]`` (F a head-wildcard from the
    pattern, so the head is the bare string name) into ``WFApply[fresh, args...]``."""
    if not isinstance(node, list) or not node:
        return node
    if _ffl_is_deriv_head(node) and isinstance(node[0][1], str) and node[0][1] in head_map:
        order, fname, var = node[0][0][1], node[0][1], node[1]
        return ['WFDeriv', fname,
                _rewrite_fhw_in_replacement(var, head_map),
                _rewrite_fhw_in_replacement(order, head_map)]
    if isinstance(node[0], str) and node[0] in head_map:
        fresh = head_map[node[0]]
        return ['WFApply', fresh] + [_rewrite_fhw_in_replacement(a, head_map) for a in node[1:]]
    return [_rewrite_fhw_in_replacement(c, head_map) for c in node]


def _rewrite_fhw_in_matchq(node):
    """Rewrite function-head wildcards inside a ``MatchQ`` guard's INNER pattern.

    ``MatchQ[u, (d_.*trig_[e+f*x])^m_. /; ... MemberQ[{sin,cos,...}, trig]]`` uses a
    wildcard as a function HEAD, but inside the guard rather than in the rule's own
    integrand -- so `_extract_fhw_from_pattern`, which only sees the integrand,
    never reached it and the whole rule was skipped.

    The inner pattern is a pattern in its own right, so it gets the same treatment:
    ``trig_[args]`` becomes ``WildHeadApp[trig_, args]``, which MatchQ then matches
    with a wildcard operation head. Only argument 2 of MatchQ is rewritten (argument
    1 is the subject, an ordinary expression), and a ``Condition[pattern, test]``
    wrapper is unwrapped so the pattern inside it is the part rewritten.
    """
    if not isinstance(node, list) or not node:
        return node
    if node[0] == 'MatchQ' and len(node) >= 3:
        subject, pattern = node[1], node[2]
        if isinstance(pattern, list) and pattern and pattern[0] == 'Condition':
            inner, test = pattern[1], pattern[2]
            inner, heads = _extract_fhw_from_pattern(inner)
            pattern = ['Condition', inner, _apply_fhw_heads_in_test(test, heads)]
        else:
            pattern, _heads = _extract_fhw_from_pattern(pattern)
        return ['MatchQ', _rewrite_fhw_in_matchq(subject), pattern] + list(node[3:])
    return [_rewrite_fhw_in_matchq(c) for c in node]


def _apply_fhw_heads_in_test(test, heads):
    """Rewrite ``F[args]`` in a MatchQ condition's TEST when ``F`` is a head wildcard
    bound by the surrounding pattern.

    ``MatchQ[u, E^(c_.*(a_.+b_.*x))*F_[v_] /; ... && InverseFunctionQ[F[x]]]``: the
    pattern binds ``F`` as a function HEAD, and the test then APPLIES it to ``x``. In
    the FFL the pattern side is ``[['Pattern','F',['Blank']], v]`` (rewritten to
    WildHeadApp by :func:`_extract_fhw_from_pattern`), but the test side is a plain
    ``['F', 'x']`` -- head is the bare string, so nothing recognised it and the
    emitter produced an undefined ``sympy.Function('F')(x)``, silently losing the
    binding. Rewrite those applications to ``WildHeadApp[F_, args]`` too.
    """
    if not heads or not isinstance(test, list) or not test:
        return test
    if isinstance(test[0], str) and test[0] in heads:
        args = [_apply_fhw_heads_in_test(a, heads) for a in test[1:]]
        return ['WildHeadApp', ['Pattern', test[0], ['Blank']]] + args
    return [_apply_fhw_heads_in_test(c, heads) for c in test]


def _summarize_ffl_guard(ffl) -> str:
    """Short human-readable summary of an FFL guard, for a dropped-guard comment.

    Renders heads and atoms compactly (e.g. ``Not[MatchQ[u, ...]]``) without the
    full nested structure, purely so the emitted comment is traceable.
    """
    def render(node, depth=0):
        if isinstance(node, str):
            return node
        if not isinstance(node, list) or not node:
            return repr(node)
        head = node[0]
        head_str = render(head) if not isinstance(head, str) else head
        if depth >= 3:
            return f"{head_str}[...]"
        args = ', '.join(render(a, depth + 1) for a in node[1:])
        return f"{head_str}[{args}]"

    text = render(ffl)
    return text if len(text) <= 160 else text[:157] + '...'


def _extract_nested_with_condition(result_ffl):
    """Lift ``With[..., Condition(expr, test)]`` into an outer rule condition.

    Returns ``(new_result_ffl, extra_conditions)``.
    """
    if not isinstance(result_ffl, list) or not result_ffl:
        return result_ffl, []

    head = result_ffl[0]
    if head == 'Condition' and len(result_ffl) >= 3:
        return result_ffl[1], [result_ffl[2]]

    if head == 'With' and len(result_ffl) >= 3:
        bindings_ffl = result_ffl[1]
        body_ffl, extra_conditions = _extract_nested_with_condition(result_ffl[2])
        if not extra_conditions:
            return result_ffl, []
        substitutions = _with_binding_substitutions(bindings_ffl)
        lifted_conditions = [
            _ffl_substitute_symbols(cond, substitutions)
            for cond in extra_conditions
        ]
        return ['With', bindings_ffl, body_ffl], lifted_conditions

    return result_ffl, []


# =============================================================================
# Rubi \[Star] operator
# =============================================================================
#
# Rubi co-opts Wolfram's otherwise meaning-free ``\[Star]`` infix operator as a
# display-friendly product: ``Star[u, v]`` shows as ``u*v`` and evaluates to the
# product of ``u`` and ``v`` with ``u`` distributed over the terms of ``v``. The
# source rules write it infix, e.g. ``c/(e*(b*c-a*d)) \[Star] Int[...,x]``.
#
# SymPy now parses it NATIVELY into a proper ``['Star', u, v]`` node, so it needs no
# special handling here -- it is translated like any other head, through the
# ``'Star'`` entry in the custom-function maps below. (SymPy used to read it as a
# POSTFIX operator, producing a flat ``Times[.., [tail,'Star'], .., v]`` that this
# module had to detect and regroup. All 1060 occurrences across the Rubi sources now
# arrive as real binary Star nodes -- none n-ary, matching Star's 2-arg runtime -- so
# that reconstruction layer is gone.)



# =============================================================================
# Known constraint classes (for import resolution)
# =============================================================================

_CONSTRAINTS_WOLFRAM: Set[str] = {
    'FreeQ', 'IntegerQ', 'OddQ', 'EvenQ', 'NumberQ', 'NumericQ',
    'AtomQ', 'MemberQ', 'PositiveQ', 'NegativeQ', 'PolynomialQ',
    'TrueQ', 'FalseQ', 'MatchQ', 'PrimeQ', 'UnsameQ',
}

_CONSTRAINTS_RUBI: Set[str] = {
    'EqQ', 'NeQ', 'IGtQ', 'ILtQ', 'IGeQ', 'ILeQ',
    'GtQ', 'LtQ', 'GeQ', 'LeQ', 'PosQ', 'NegQ',
    'IntegersQ', 'HalfIntegerQ', 'FractionQ', 'RationalQ',
    'ComplexNumberQ', 'RealNumberQ', 'FractionOrNegativeQ', 'SqrtNumberQ',
    'PowerQ', 'ProductQ', 'SumQ', 'NonsumQ',
    'IntegerPowerQ', 'FractionalPowerQ',
    'PolyQ', 'LinearQ', 'QuadraticQ', 'BinomialQ', 'TrinomialQ',
    'LinearMatchQ', 'QuadraticMatchQ', 'BinomialMatchQ', 'TrinomialMatchQ',
    'TrigQ', 'HyperbolicQ', 'InverseTrigQ', 'InverseHyperbolicQ', 'LogQ',
    'ComplexFreeQ', 'InverseFunctionFreeQ', 'FractionalPowerFreeQ',
    'TrigHyperbolicFreeQ', 'IntegralFreeQ',
    'RationalFunctionQ', 'AlgebraicFunctionQ', 'IndependentQ',
    'SimplerQ', 'SumSimplerQ',
    'FunctionOfQ', 'PiecewiseLinearQ', 'EqM', 'ExpressionEqQ',
    'IntLinearQ', 'IntBinomialQ', 'IntQuadraticQ',
    'MonomialQ', 'LinearPairQ',
    'GeneralizedBinomialQ', 'GeneralizedBinomialMatchQ',
    'GeneralizedTrinomialQ', 'GeneralizedTrinomialMatchQ',
    'NiceSqrtQ', 'SimplerSqrtQ', 'FractionalPowerFactorQ',
    'SumBaseQ', 'InverseFunctionQ', 'InertTrigQ', 'InertTrigFreeQ',
    'CalculusFreeQ', 'QuotientOfLinearsQ',
    'PowerOfLinearQ', 'PowerOfLinearMatchQ',
    'FunctionOfExponentialQ',
    'KnownSineIntegrandQ', 'KnownSecantIntegrandQ',
    'KnownTangentIntegrandQ', 'KnownCotangentIntegrandQ',
    'EulerIntegrandQ', 'SubstForFractionalPowerQ',
    'PerfectSquareQ', 'PolynomialInQ', 'FunctionOfTrigOfLinearQ',
    'SimplerIntegrandQ', 'PseudoBinomialPairQ', 'QuadraticProductQ',
    'EveryQ', 'TrigSimplifyQ', 'TryPureTanSubst',
}

_ALL_KNOWN_CONSTRAINTS = _CONSTRAINTS_WOLFRAM | _CONSTRAINTS_RUBI


# Mathematica heads that map to bare-name calls in generated code (via 'from rubi_utils import *')
RUBI_UTILS_MAP: Dict[str, str] = {
    'Subst': 'Subst',
    'Simp': 'Simp',
    'FracPart': 'FracPart',
    'IntPart': 'IntPart',
    'ExpandIntegrand': 'ExpandIntegrand',
    'ExpandToSum': 'ExpandToSum',
    'Coeff': 'Coeff',
    'Coefficient': 'Coefficient',
    'Expon': 'Expon',
    'With': 'With',
    'Module': 'Module',
    'Set': 'Set',
    'CannotIntegrate': 'CannotIntegrate',
    'PolynomialQuotient': 'PolynomialQuotient',
    'PolynomialRemainder': 'PolynomialRemainder',
    'PolynomialDivide': 'PolynomialDivide',
    'Condition': 'Condition',
    'Rule': 'Rule',
    'ReplaceAll': 'ReplaceAll',
    'Unintegrable': 'Unintegrable',
    'IntHide': 'IntHide',
    'Sum': 'Sum',
    'Numerator': 'Numerator',
    'Together': 'Together',
    'GCD': 'GCD',
    'Sign': 'Sign',
    'Quotient': 'Quotient',
    'EllipticPi': 'EllipticPi',
    'NormalizePseudoBinomial': 'NormalizePseudoBinomial',
    'SubstFor': 'SubstFor',
    'FunctionOfExponential': 'FunctionOfExponential',
    'FunctionOfExponentialFunction': 'FunctionOfExponentialFunction',
    'FunctionOfLog': 'FunctionOfLog',
    'IntSum': 'IntSum',
    'Discriminant': 'Discriminant',
    'Block': 'Block',
    'Root': 'Root',
    'SubstPower': 'SubstPower',
    'SubstForInverseFunction': 'SubstForInverseFunction',
    'ExpandTrigExpand': 'ExpandTrigExpand',
    'FunctionOfSquareRootOfQuadratic': 'FunctionOfSquareRootOfQuadratic',
    'InverseFunctionOfLinear': 'InverseFunctionOfLinear',
    'SubstForFractionalPowerOfQuotientOfLinears': 'SubstForFractionalPowerOfQuotientOfLinears',
    "D": "D",
    # Additional Rubi-specific utility functions
    'Dist': 'Dist',
    'Star': 'Star',  # Rubi \[Star]: display-friendly product, parsed natively by SymPy
    'WFApply': 'WFApply',  # re-apply a function-head-wildcard's captured head
    'WFDeriv': 'WFDeriv',  # n-th derivative of a wildcard-bound function
    'SimplifyIntegrand': 'SimplifyIntegrand',
    'FreeFactors': 'FreeFactors',
    'NonfreeFactors': 'NonfreeFactors',
    'ActivateTrig': 'ActivateTrig',
    'DeactivateTrig': 'DeactivateTrig',
    'ExpandTrig': 'ExpandTrig',
    'ExpandTrigReduce': 'ExpandTrigReduce',
    'DerivativeDivides': 'DerivativeDivides',
    'BinomialDegree': 'BinomialDegree',
    'TrinomialDegree': 'TrinomialDegree',
    'LeafCount': 'LeafCount',
    'Part': 'Part',
    'First': 'First',
    'Rest': 'Rest',
    'Head': 'Head',
    'Length': 'Length',
    'If': 'If',
    'Numer': 'Numer',
    'Denom': 'Denom',
    'CompoundExpression': 'CompoundExpression',
    'Apply': 'Apply',
    'Not': 'Not',
    # Additional Rubi utility functions
    'NormalizePowerOfLinear': 'NormalizePowerOfLinear',
    'NormalizeIntegrand': 'NormalizeIntegrand',
    'Exponent': 'Exponent',
    'FullSimplify': 'FullSimplify',
    'Simplify': 'Simplify',
    'FunctionExpand': 'FunctionExpand',
    'ExpandLinearProduct': 'ExpandLinearProduct',
    'Divides': 'Divides',
    'RationalFunctionExpand': 'RationalFunctionExpand',
    'PowerVariableExpn': 'PowerVariableExpn',
    'FunctionOfLinear': 'FunctionOfLinear',
    'SplitProduct': 'SplitProduct',
    # Rt[u,n] — simplest nth root. A deferred rubi_utils node (NOT sympy.root): the
    # exponent n arrives as a wildcard, so it must compute at fire time via Rubi's
    # RtAux simplest-root algorithm, not eagerly as a bare principal root.
    'Rt': 'Rt',
    'PolyGCD': 'PolyGCD',
    'GeneralizedTrinomialDegree': 'GeneralizedTrinomialDegree',
    'ExpandTrigToExp': 'ExpandTrigToExp',
    'Binomial': 'Binomial',
    # Wrappers needed due to argument order / restructuring
    'Gamma': 'Gamma',
    'ProductLog': 'ProductLog',
    'Floor': 'Floor',
    'Hypergeometric2F1': 'Hypergeometric2F1',
    # Rubi utility functions used in replacements (previously only in deprecated RUBI_UTILITY_FUNCTION)
    'MinimumMonomialExponent': 'MinimumMonomialExponent',
    'Distrib': 'Distrib',
    'Apart': 'Apart',
    'ExpandExpression': 'ExpandExpression',
    'FunctionOfTrig': 'FunctionOfTrig',
    'PolynomialInSubst': 'PolynomialInSubst',
    'QuotientOfLinearsParts': 'QuotientOfLinearsParts',
    'SubstForFractionalPowerOfLinear': 'SubstForFractionalPowerOfLinear',
    'TrigSimplify': 'TrigSimplify',
    'RationalFunctionExponents': 'RationalFunctionExponents',
    'Denominator': 'Denominator',
    'Numerator': 'Numerator',
}


_EXTRA_SYMPY_HEADS: Dict[str, str] = {
    # Bessel functions
    'BesselJ': 'sympy.besselj',
    'BesselY': 'sympy.bessely',
    'BesselI': 'sympy.besseli',
    'BesselK': 'sympy.besselk',
    # Error functions
    'Erf': 'sympy.erf',
    'Erfc': 'sympy.erfc',
    'Erfi': 'sympy.erfi',
    # Fresnel integrals
    'FresnelS': 'sympy.fresnels',
    'FresnelC': 'sympy.fresnelc',
    # Exponential integrals
    'ExpIntegralE': 'sympy.expint',
    'ExpIntegralEi': 'sympy.Ei',
    'LogIntegral': 'sympy.li',
    # Trigonometric integrals
    'SinIntegral': 'sympy.Si',
    'CosIntegral': 'sympy.Ci',
    'SinhIntegral': 'sympy.Shi',
    'CoshIntegral': 'sympy.Chi',
    # Gamma and related
    # NOTE: Gamma is NOT here — it needs a 2-arg wrapper (see RUBI_UTILS_MAP)
    'LogGamma': 'sympy.loggamma',
    # Mathematica's Gamma is overloaded by arity; _rewrite_gamma_arity tags the head
    # so each arity can map to the right SymPy function.
    'Gamma$Complete': 'sympy.gamma',
    'Gamma$Upper': 'sympy.uppergamma',
    'PolyGamma': 'sympy.polygamma',
    'Factorial': 'sympy.factorial',
    # Other special functions
    'PolyLog': 'sympy.polylog',
    # Rubi only ever uses the ONE-argument form, which is a straight rename. The
    # two-argument Mathematica form would NOT be: ProductLog[k, z] is LambertW(z, k)
    # (branch index moves from first to last), so if a two-arg use ever appears here
    # this entry must become a reordering wrapper. sympy_wolfram's ProductLog node
    # already handles both; this override exists so rule PATTERNS hold a plain
    # LambertW and therefore match a caller's expression.
    'ProductLog': 'sympy.LambertW',
    'Zeta': 'sympy.zeta',
    'Mod': 'sympy.Mod',
    # Elementary functions not in SYMPY_FUNC_MAP
    'Ceiling': 'sympy.ceiling',
    'Factor': 'sympy.factor',
    'Cancel': 'sympy.cancel',
    'Expand': 'sympy.expand',
    'TrigExpand': 'sympy.expand_trig',
    # Hypergeometric (needs special handling but basic mapping)
    'HypergeometricPFQ': 'sympy.hyper',
    # Unevaluated integral (SymPy native, not a Rubi utility function)
    'Integral': 'sympy.Integral',
}

_CONSTRAINT_LITERAL_HEADS: Set[str] = {'List'}


def _replacement_codegen_target(head: str) -> tuple[str, object]:
    import sympy as _sympy
    if head in _ALL_KNOWN_CONSTRAINTS:
        return head, _sympy.Function(head)
    if head in _EXTRA_SYMPY_HEADS:
        return _EXTRA_SYMPY_HEADS[head], _sympy
    if head in RUBI_UTILS_MAP:
        return RUBI_UTILS_MAP[head], _sympy.Function(head)
    return head, _sympy.Function(head)


def _constraint_codegen_target(head: str) -> tuple[str, object] | None:
    import sympy as _sympy
    if head in _CONSTRAINT_LITERAL_HEADS:
        return None
    if head in _ALL_KNOWN_CONSTRAINTS:
        return head, _sympy.Function(head)
    if head in _EXTRA_SYMPY_HEADS:
        return _EXTRA_SYMPY_HEADS[head], _sympy
    if head in RUBI_UTILS_MAP:
        return RUBI_UTILS_MAP[head], _sympy.Function(head)
    return head, _sympy.Function(head)


def _build_replacement_custom_functions() -> dict:
    """Build custom_functions dict for replacement FFL processing.

    IMPORTANT: We do NOT add entries for heads already in FFLConverter.SYMPY_FUNC_MAP
    or SYMPY_LOGIC_MAP. Those are handled naturally by FFLConverter and should emit
    sympy.xyz(...) directly (e.g. ArcSin -> sympy.asin).
    """
    import sympy as _sympy
    # Get heads already handled by FFLConverter
    sympy_handled = set(FFLConverter.SYMPY_FUNC_MAP.keys()) | set(FFLConverter.SYMPY_LOGIC_MAP.keys())

    custom = {}
    all_heads = set(RUBI_UTILS_MAP) | set(_ALL_KNOWN_CONSTRAINTS) | set(_EXTRA_SYMPY_HEADS)
    for head in sorted(all_heads):
        # Skip heads already handled by FFLConverter's SYMPY_FUNC_MAP / SYMPY_LOGIC_MAP
        # UNLESS they are in RUBI_UTILS_MAP (those need lazy wrappers, not eager sympy.*)
        if head in sympy_handled and head not in RUBI_UTILS_MAP:
            continue
        code_str, obj = _replacement_codegen_target(head)
        custom[head] = (code_str, obj)
    # Use sympy.Function so simplify_code round-trip works (eval→print→eval)
    custom['Int'] = ('Int', _sympy.Function('Int'))
    custom['List'] = ('List', wolfram_objects.List)
    return custom


def _build_constraint_custom_functions() -> dict:
    """Build custom_functions dict for constraint FFL processing.

    IMPORTANT: We do NOT add entries for heads already in FFLConverter.SYMPY_FUNC_MAP
    or SYMPY_LOGIC_MAP. Those are handled naturally by FFLConverter.
    """
    import sympy as _sympy
    # Get heads already handled by FFLConverter
    sympy_handled = set(FFLConverter.SYMPY_FUNC_MAP.keys()) | set(FFLConverter.SYMPY_LOGIC_MAP.keys())

    custom = {}
    all_heads = set(RUBI_UTILS_MAP) | set(_ALL_KNOWN_CONSTRAINTS) | set(_EXTRA_SYMPY_HEADS)
    for head in sorted(all_heads):
        # Skip heads already handled by FFLConverter's SYMPY_FUNC_MAP / SYMPY_LOGIC_MAP
        # UNLESS they are in RUBI_UTILS_MAP (those need lazy wrappers, not eager sympy.*)
        if head in sympy_handled and head not in RUBI_UTILS_MAP:
            continue
        target = _constraint_codegen_target(head)
        if target is None:
            continue
        code_str, obj = target
        custom[head] = (code_str, obj)
    # `Int` can appear inside a CONSTRAINT too -- the Weierstrass rule guards on
    # `CalculusFreeQ[Block[..., Int[...]]]`. Without this it fell through to the
    # generic `sympy.Function('Int')`, i.e. a DIFFERENT head from the integrator's
    # own Int, so the guard inspected something that only looked like an integral.
    custom['Int'] = ('Int', _sympy.Function('Int'))
    return custom


def _build_inert_trig_custom_functions() -> dict:
    """Map Rubi's INERT (lowercase) trig heads to the InertSin/... markers.

    Rubi writes its main trig rule PATTERNS over inert lowercase ``sin``/``cos``/...
    -- deliberately distinct from the active Wolfram ``Sin``/``Cos`` -- and routes
    active integrands to them through a general ``DeactivateTrig`` fallback rule
    (see ``rubi_rules.base_objects`` and the project memory note
    ``rubi-trig-deactivation-dispatch``). The inert markers therefore must NOT be
    (and are not) subclasses of the active ``sympy.sin`` etc.; they are opaque
    ``Function('InertSin')`` heads that only the inert rules match.

    Without this override the FFL converter's default ``func_map`` collapses both
    ``sin`` and ``Sin`` onto ``sympy.sin``, losing the inert/active distinction.
    ``custom_functions`` takes precedence over ``func_map`` in the converter, so
    these entries restore the faithful translation. Used in the pattern, the
    replacement AND the constraint conversion so every occurrence is consistent.
    """
    from rubi_rules.utils.inert_functions import (
        InertSin, InertCos, InertTan, InertCot, InertSec, InertCsc)
    return {
        'sin': ('InertSin', InertSin), 'cos': ('InertCos', InertCos),
        'tan': ('InertTan', InertTan), 'cot': ('InertCot', InertCot),
        'sec': ('InertSec', InertSec), 'csc': ('InertCsc', InertCsc),
    }


_INERT_TRIG_CUSTOM = _build_inert_trig_custom_functions()


def _build_pattern_custom_functions() -> dict:
    """custom_functions for converting a rule's PATTERN (the integrand).

    LAYERING. ``sympy_wolfram`` is an interpreter for the Wolfram language: a head it
    implements is translated to its OWN node, because SymPy's same-named function
    applies its own eager-evaluation rules which are not Mathematica's. ``rubi_rules``
    sits on top and OVERRIDES that for the heads where the two really do agree, so the
    generated rules speak plain SymPy -- `expint`, `LambertW`, `polylog` -- and a
    pattern matches what a caller actually passes to ``rubi_integrate``.

    Patterns used to get only the inert-trig overrides, so they held deferred nodes
    while the REPLACEMENT half of the very same rule held the SymPy function. A
    pattern holding ``ExpIntegralE(n_, ...)`` can never match a caller's
    ``expint(n, ...)``, so those rules were unreachable.
    """
    import sympy as _sympy
    custom = {head: (code, _sympy) for head, code in _EXTRA_SYMPY_HEADS.items()}
    custom.update(_INERT_TRIG_CUSTOM)
    return custom

_REPLACEMENT_CUSTOM = {**_build_replacement_custom_functions(), **_INERT_TRIG_CUSTOM}
_CONSTRAINT_CUSTOM = {**_build_constraint_custom_functions(), **_INERT_TRIG_CUSTOM}
_PATTERN_CUSTOM = _build_pattern_custom_functions()


# =============================================================================
# Defaults
# =============================================================================

DEFAULT_JSON = './rubi_fullformlist_results.json'


# =============================================================================
# Path conversion: JSON file path -> output Python path
# =============================================================================

def _make_output_path(json_file_path: str) -> Optional[str]:
    """Convert a JSON file entry path to a rules/ output Python path."""
    path = json_file_path.replace('\\', '/')
    marker = 'Rubi/IntegrationRules/'
    if marker not in path:
        return None
    rel = path.split(marker, 1)[1]
    parts = [p for p in rel.split('/') if p]
    if not parts:
        return None

    out_parts = ['rules']
    for i, part in enumerate(parts):
        is_last = (i == len(parts) - 1)
        if is_last:
            part = re.sub(r'\.m$', '', part)

        m = re.match(r'^([\d]+(?:\.[\d]+)*(?:\.[a-z])?)[\s.]*(.*)', part)
        if m:
            num = m.group(1).replace('.', '_')
            desc = m.group(2).strip()
            desc_clean = re.sub(r'[^a-z0-9]+', '_', desc.lower()).strip('_')
            if is_last:
                out_parts.append(f'r_{num}.py')
            else:
                out_parts.append(f'r_{num}_{desc_clean}' if desc_clean else f'r_{num}')
        else:
            desc_clean = re.sub(r'[^a-z0-9]+', '_', part.lower()).strip('_')
            out_parts.append(f'{desc_clean}.py' if is_last else desc_clean)

    return '/'.join(out_parts)


# =============================================================================
# JSON reader
# =============================================================================

def load_json_entries(json_path: Path) -> List[dict]:
    """Load the pre-computed fullformlist JSON."""
    with open(json_path, encoding='utf-8') as f:
        return json.load(f)


def _unwrap_load_show_steps(exprs: List) -> List:
    """Replace ``If[TrueQ[LoadShowSteps], <step rule>, <plain rule>]`` by the plain rule.

    Rubi defines 34 of its most GENERAL rules this way -- the ones keyed on a utility
    predicate rather than on a syntactic shape: the ``FunctionOfLog`` log-substitution
    (3.5), ``DeactivateTrig`` dispatch (4.1.0.1), the inert-trig rules (4.7.5), integrand
    simplification (9.1) and the 9.3/9.4 miscellaneous rules. Both branches define the
    SAME rule; the first merely wraps the RHS in ``ShowStep[...]`` so Rubi can narrate it.
    Mathematica evaluates the ``If`` at load time and ``$LoadShowSteps`` is False by
    default, so the THIRD argument is the rule that is actually installed.

    Without this, every one of those rules was invisible to the generator (it only looks
    for a top-level ``SetDelayed``), and their absence is not silent: with no general
    log-substitution rule, ``Int[Erf[Log[x]]/x, x]`` fell through to the narrower and
    upstream-buggy 8.1/8.4 rules. Verified against real Rubi 4.17.3.0, which solves it
    via exactly this rule ("General" in its Steps output).
    """
    out = []
    for expr in exprs:
        if (isinstance(expr, list) and len(expr) == 4 and expr[0] == 'If'
                and expr[1] == ['TrueQ', 'LoadShowSteps']
                and isinstance(expr[3], list) and expr[3] and expr[3][0] == 'SetDelayed'):
            out.append(expr[3])
        else:
            out.append(expr)
    return out



def strip_unused_imports(paths: List[Path]) -> Tuple[int, str]:
    """Remove unused imports from freshly generated modules, with ``ruff``.

    The header of a generated rule module imports the union of every name the emitter
    COULD need, so most modules pull in dozens of names they never use. Rather than
    predict per module which imports survive constraint/replacement shortening -- the
    emitter cannot know before the code exists -- generate first, then let a linter
    delete what is provably unused (pyflakes' F401, via ruff's ``--fix``).

    ``ruff`` is optional: without it the modules are still correct, just noisier, so a
    missing binary is reported and ignored rather than failing the build.

    Returns ``(files_changed, message)``.
    """
    import subprocess
    if not paths:
        return 0, 'no files to clean'
    before = {p: p.read_text(encoding='utf-8') for p in paths}
    cmd = [sys.executable, '-m', 'ruff', 'check', '--isolated',
           '--select', 'F401', '--fix', '--quiet', *[str(p) for p in paths]]
    try:
        subprocess.run(cmd, check=False, capture_output=True, timeout=600)
    except (OSError, subprocess.SubprocessError) as exc:
        return 0, f'skipped ({type(exc).__name__}: {exc}); install ruff to enable'
    changed = sum(1 for p in paths if p.read_text(encoding='utf-8') != before[p])
    return changed, f'{changed} module(s) had unused imports removed'


def group_entries_by_output(entries: List[dict]) -> Dict[str, dict]:
    """Group JSON entries by output path, merging expressions for duplicates."""
    groups: Dict[str, dict] = {}
    for entry in entries:
        fpath = entry.get('file', '')
        exprs = _unwrap_load_show_steps(entry.get('expressions') or [])
        err   = entry.get('file_error')
        out   = _make_output_path(fpath)
        if out is None or (not exprs and not err):
            continue
        if out not in groups:
            rel = fpath.replace('\\', '/')
            if 'IntegrationRules/' in rel:
                rel = rel.split('IntegrationRules/', 1)[1]
            desc = rel.rsplit('/', 1)[-1] if '/' in rel else rel
            desc = re.sub(r'\.m$', '', desc)
            groups[out] = {
                'expressions': [],
                'source_files': [],
                'description': desc,
                'file_error': None,
            }
        groups[out]['expressions'].extend(exprs)
        groups[out]['source_files'].append(os.path.basename(fpath))
        if err:
            groups[out]['file_error'] = err
    return groups


# =============================================================================
# Rule translator (uses FFLConverter from sympy_wolfram)
# =============================================================================

class RubiRuleTranslator:
    """Translate FFL rules into Python source with SymPyReplacementPattern objects."""

    def __init__(self):
        self._converter = FFLConverter()

    def translate_module(self, rules: List, module_name: str, source_file: str = '') -> str:
        """Translate FFL rules into a Python module with SymPyReplacementPattern list."""
        all_non_optional, all_optional, all_symbols = _collect_wildcards_from_rules(
            self._converter, rules)

        header = self._generate_header(module_name, source_file)

        # Generate wildcard declarations
        wc_lines = []
        for name in sorted(all_non_optional | all_optional):
            if name in self._converter.reserved_symbols:
                continue  # the integration variable is declared separately, as `x`
            if name in all_optional:
                wc_lines.append(f"_{name}_ = WildSymbol('{name}', optional_value=IDENTITY_ELEMENT)")
            if name in all_non_optional:
                wc_lines.append(f"{name}_ = WildSymbol('{name}')")
        wc_section = '\n'.join(wc_lines) + '\n\n' if wc_lines else ''

        # Namespace mirroring the generated module, used to validate that each
        # rule's emitted code actually loads (references only defined names).
        # A rule that translates without error can still reference a name the
        # generator does not support (e.g. the `Min` flag, or an `x_` wildcard
        # that collides with the fixed integration variable and is therefore not
        # declared). Such a rule would raise NameError at import time and take the
        # whole module's `RULES` list down with it, so we skip it here instead.
        load_ns: Optional[dict] = {}
        try:
            exec(header + wc_section, load_ns)
        except Exception:
            load_ns = None  # header itself won't exec -> skip per-rule validation

        # Declare the plain (non-wildcard) symbols the rules reference bare -- scoping
        # locals (r/s/k/u), selector symbols, etc. -- so bindings read
        # `Module(List(Set(r, ...)), ...)` instead of building `Symbol('r')` inline.
        # ONLY names NOT already defined in the module are declared: a name that is
        # already an import/utility function (e.g. `D`, `Gamma`) or a wildcard/header
        # symbol must NOT be shadowed by a `Symbol(...)` (that gave
        # `'Symbol' object is not callable` when the rule later calls it).
        import sympy as _sympy
        sym_lines = []
        if load_ns is not None:
            for name in sorted(all_symbols):
                if name in self._converter.reserved_symbols:
                    continue
                # A scope local IS a Symbol, so declare it even when the name shadows
                # a SymPy singleton/import (S/C/E/...) -- rules use it as a symbol, and
                # `sympy.S(...)` etc. stay qualified. Skip only names the header already
                # binds to a Symbol, to avoid a redundant re-declare.
                if isinstance(load_ns.get(name), _sympy.Symbol) and str(load_ns[name]) == name:
                    continue
                sym_lines.append(f"{name} = Symbol('{name}')")
                load_ns[name] = _sympy.Symbol(name)  # visible to per-rule validation
        sym_section = '\n'.join(sym_lines) + '\n\n' if sym_lines else ''

        # Generate rules, numbered by their ordinal position among the module's
        # actual rules (``SetDelayed`` entries) -- NOT by raw expression index.
        # SymPy's parser can split a stray fragment (e.g. an ``Int[...]`` orphaned by
        # a mangled ``\[Star]``) into an extra top-level expression; counting those
        # would shift every following rule's number whenever parsing changes. Numbering
        # only real rules keeps ``rule_number`` == the rule's position as it appears in
        # the source/JSON, stable across such parser fixes.
        rule_lines = []
        skipped = 0
        non_rules = 0
        rule_number = 0
        for rule in rules:
            if not (isinstance(rule, list) and rule and rule[0] == 'SetDelayed'):
                continue  # orphan / non-rule expression: don't number or emit it
            rule_number += 1
            try:
                code = self._translate_rule(rule, rule_number, module_name, load_ns)
                if code:
                    rule_lines.append(code)
                else:
                    # A SetDelayed whose LHS is not ``Int[...]``: a utility PREDICATE
                    # defined inside a rule file (IntLinearQ / IntBinomialQ /
                    # IntQuadraticQ). Not an integration rule, so not a skip -- it is
                    # hand-implemented in rubi_rules/utils/. It still consumes a
                    # rule_number, because numbering must stay aligned with the
                    # source/JSON ordering.
                    non_rules += 1
            except Exception as e:
                skipped += 1
                rule_lines.append(f"    # Rule {rule_number}: SKIPPED - {type(e).__name__}: {e}")

        # rule_number is the count of SetDelayed entries; of those, `non_rules` are
        # predicate definitions rather than integration rules and `skipped` are real
        # rules that could not be translated. (Orphans are excluded above.)
        footer = self._generate_footer(rule_number - skipped - non_rules, skipped, non_rules)
        rules_body = '\n'.join(rule_lines)
        return header + sym_section + wc_section + 'RULES = [\n' + rules_body + '\n' + footer

    # =========================================================================
    # Header / footer
    # =========================================================================

    def _generate_header(self, module_name: str, source_file: str) -> str:
        return f"""# -*- coding: utf-8 -*-
# =============================================================================
# !! AUTO-GENERATED FILE -- DO NOT EDIT !!
#
# Generated by: rubi_rules/codegen/generate.py
# Source: {source_file}
# Module: {module_name}
#
# This file contains Rubi integration rules as SymPyReplacementPattern objects.
# Re-run the generator to update.
# =============================================================================
import sympy
from sympy import Integer, Integral, Lambda, Rational, Symbol, Tuple as SympyTuple
from rubi_rules.utils.rubi_utils import *  # bare-name access; sympy imports below override any conflicts (e.g. Not)
from sympy.logic.boolalg import Or, Not, And
{_sympy_import_line()}

from sympy_matching.wild import WildSymbol, WildHeadApp, WildHeadDeriv, HeadRef, IDENTITY_ELEMENT
from rubi_rules.base_objects import Int, SymPyReplacementPattern
# Inert trig markers (Rubi's lowercase sin/cos/... patterns). Distinct opaque heads,
# NOT subclasses of sympy.sin -- see rubi-trig-deactivation-dispatch project note.
from rubi_rules.utils.inert_functions import (
    InertSin, InertCos, InertTan, InertCot, InertSec, InertCsc)
from rubi_rules.utils import (
    # Wolfram standard constraints
    FreeQ, IntegerQ, OddQ, EvenQ, NumberQ, NumericQ, AtomQ, MemberQ,
    PositiveQ, NegativeQ, PolynomialQ, TrueQ, FalseQ, MatchQ, PrimeQ, UnsameQ,
    # RUBI-specific constraints
    EqQ, NeQ, IGtQ, ILtQ, IGeQ, ILeQ, GtQ, LtQ, GeQ, LeQ, PosQ, NegQ,
    IntegersQ, HalfIntegerQ, FractionQ, RationalQ, ComplexNumberQ, RealNumberQ,
    FractionOrNegativeQ, SqrtNumberQ, PowerQ, ProductQ, SumQ, NonsumQ,
    IntegerPowerQ, FractionalPowerQ, PolyQ, LinearQ, QuadraticQ, BinomialQ,
    TrinomialQ, LinearMatchQ, QuadraticMatchQ, BinomialMatchQ, TrinomialMatchQ,
    TrigQ, HyperbolicQ, InverseTrigQ, InverseHyperbolicQ, LogQ, ComplexFreeQ,
    InverseFunctionFreeQ, FractionalPowerFreeQ, TrigHyperbolicFreeQ, IntegralFreeQ,
    RationalFunctionQ, AlgebraicFunctionQ, IndependentQ, SimplerQ, SumSimplerQ,
    FunctionOfQ, PiecewiseLinearQ, ExpressionEqQ,
    IntLinearQ, IntBinomialQ, IntQuadraticQ,
    MonomialQ, LinearPairQ,
    GeneralizedBinomialQ, GeneralizedBinomialMatchQ,
    GeneralizedTrinomialQ, GeneralizedTrinomialMatchQ,
    NiceSqrtQ, SimplerSqrtQ, FractionalPowerFactorQ,
    SumBaseQ, InverseFunctionQ, InertTrigQ, InertTrigFreeQ,
    CalculusFreeQ, QuotientOfLinearsQ,
    PowerOfLinearQ, PowerOfLinearMatchQ,
    FunctionOfExponentialQ,
    KnownSineIntegrandQ, KnownSecantIntegrandQ,
    KnownTangentIntegrandQ, KnownCotangentIntegrandQ,
    EulerIntegrandQ, SubstForFractionalPowerQ,
    PerfectSquareQ, PolynomialInQ, FunctionOfTrigOfLinearQ,
    SimplerIntegrandQ, PseudoBinomialPairQ, QuadraticProductQ,
    EveryQ, TrigSimplifyQ, EqM, TryPureTanSubst,
)

# --- Integration variable ---
x = Symbol('x')

# --- Rubi global option stubs (default False/placeholder) ---
UseGamma = sympy.Symbol('UseGamma')  # Rubi global option; treated as False in Python
u = Symbol('u')  # Generic integrand placeholder used in some Rubi constraint calls

# --- Rubi selector symbols ---
# Rubi passes Min/Max as bare SYMBOLS, not calls: Expon[Px, x, Min] selects the
# minimum exponent. The code emitter round-trips through SymPy's printer, which
# renders Symbol('Min') as the bare name `Min`, so the name must exist here.
# (A genuine Min[a, b] call is emitted qualified, as sympy.Min(...), so these
# bindings cannot shadow it.)
Min = Symbol('Min')
Max = Symbol('Max')

# --- Wildcard symbols ---
# dot wildcards (must match exactly one expression)
# optional wildcards (can match identity element if absent in commutative ops)

"""

    def _generate_footer(self, n_rules: int, n_skipped: int, n_non_rules: int = 0) -> str:
        extra = (f" ({n_non_rules} non-rule predicate definition"
                 f"{'s' if n_non_rules != 1 else ''} not counted)") if n_non_rules else ""
        return f"""
]

# Summary: {n_rules} rules translated, {n_skipped} skipped{extra}
"""

    # =========================================================================
    # Rule translation
    # =========================================================================

    # -- rule translation, step by step ---------------------------------------
    #
    # _translate_rule() below is the whole pipeline for ONE rule and reads top to
    # bottom; each step is a helper so the flow stays visible:
    #
    #   split        SetDelayed[Int[integrand, x_Symbol], rhs]  ->  parts
    #   lift guards  the /; conditions, including ones nested in a With[...]
    #   head wilds   F_[..] -> WildHeadApp[..] so a wildcard can BE a function head
    #   translate    integrand / replacement / constraints -> Python code strings
    #   validate     the emitted rule actually loads
    #   emit         the SymPyReplacementPattern(...) text

    @staticmethod
    def _split_conditions(rhs):
        """Separate the replacement from its guards.

        A rule body is ``replacement /; condition``, and a ``With[{...}, body /; c]``
        hides a further condition inside the body. Returns (result_ffl, conditions).
        """
        conditions: List[object] = []
        result_ffl = rhs
        if isinstance(rhs, list) and rhs[0] == 'Condition':
            result_ffl, guard = rhs[1], rhs[2]
            conditions.append(guard)
        result_ffl, nested = _extract_nested_with_condition(result_ffl)
        conditions.extend(nested)
        return result_ffl, conditions

    @staticmethod
    def _apply_head_wildcards(integrand_ffl, result_ffl, conditions):
        """Rewrite function-head wildcards everywhere they occur in the rule.

        ``F_[args]`` in the PATTERN becomes ``WildHeadApp[F_, args]``, which MatchPy
        matches with a wildcard operation head (any function matches, and F binds to
        the head). In the REPLACEMENT and the CONSTRAINTS the same head appears as a
        bare name, and becomes ``WFApply[F, args]``, which re-applies the bound head
        on doit(). Conditions need the rewrite too -- e.g.
        ``FunctionOfQ[Derivative[n-1][f][x], u, x]`` -- otherwise the raw non-string
        head aborts the whole rule.
        """
        integrand_ffl, head_names = _extract_fhw_from_pattern(integrand_ffl)
        if head_names:
            head_map = {h: h for h in head_names}
            result_ffl = _rewrite_fhw_in_replacement(result_ffl, head_map)
            conditions = [_rewrite_fhw_in_replacement(c, head_map) for c in conditions]
        return integrand_ffl, result_ffl, conditions

    @staticmethod
    def _wildcard_names(wild_defs):
        """Split the emitted ``m_ = WildSymbol(...)`` lines into (plain, optional).

        The pattern translation is what DISCOVERS a rule's wildcards; the
        replacement and constraints must be told about them, because there they
        appear as bare atoms rather than ``Pattern[...]`` nodes.
        """
        plain, optional = set(), set()
        for definition in wild_defs:
            var_name = definition.split('=')[0].strip()
            if var_name.startswith('_') and var_name.endswith('_'):
                optional.add(var_name[1:-1])
            elif var_name.endswith('_'):
                plain.add(var_name[:-1])
        return plain, optional

    def _translate_constraints(self, conditions, reserved, plain_wilds, opt_wilds,
                               short_ns=None):
        """Translate the guards into constraint code, dropping only what is safe.

        A top-level ``And[...]`` is flattened, since the constraints tuple already
        means conjunction.

        A guard mentioning a function-head wildcard cannot be translated. Rather
        than lose the whole rule we drop ONLY an exclusionary ``Not[...]`` guard:
        removing an exclusion merely broadens which integrands the rule is offered,
        and for these substitution meta-rules the result is still correct (verified
        for rule 2692 -> the FunctionOfExponential family), with the matcher's rule
        ordering keeping it from stealing forms a specific rule handles. A POSITIVE
        requirement (a bare ``MatchQ``, or ``Or[..., MatchQ]``) is never dropped --
        that would broaden the rule unsafely and can yield wrong answers, so such a
        rule stays fully skipped. Whatever is dropped is recorded in a comment.

        Returns (constraints_fragment, dropped_guard_summaries).
        """
        parts: List[str] = []
        dropped: List[str] = []
        short_ns = dict(short_ns) if short_ns else dict(_rubi_override_sympy_names())

        def translate(guard):
            guard = _rewrite_fhw_in_matchq(guard)
            try:
                code, _, _ = ffl_to_sympy_short_code(
                    guard,
                    reserved,
                    namespace=dict(short_ns),
                    custom_functions=_CONSTRAINT_CUSTOM,
                    wildcards=plain_wilds,
                    optional_wildcards=opt_wilds,
                )
                return code
            except ValueError as exc:
                mentions_head_wildcard = ('function-head wildcard' in str(exc)
                                          or 'Non-string function head' in str(exc))
                is_exclusion = isinstance(guard, list) and guard and guard[0] == 'Not'
                if mentions_head_wildcard and is_exclusion:
                    dropped.append(_summarize_ffl_guard(guard))
                    return None
                raise

        for condition in conditions:
            conjuncts = (condition[1:]
                         if isinstance(condition, list) and condition[0] == 'And'
                         else [condition])
            for conjunct in conjuncts:
                code = translate(conjunct)
                if code is not None:
                    parts.append(code)

        fragment = f"({', '.join(parts)},)" if parts else "()"
        return fragment, dropped

    @staticmethod
    def _check_rule_loads(load_ns, probe, module_name, rule_number):
        """Fail translation if the emitted rule would not import.

        A rule can translate cleanly and still reference a name the generator does
        not provide; left in place it would raise at import time and take the whole
        module's RULES list down with it.
        """
        if load_ns is None:
            return
        try:
            eval(compile(probe, f'<{module_name} rule {rule_number}>', 'eval'), load_ns)
        except TypeError as e:
            # A Rubi predicate called with the wrong number of arguments is an
            # upstream typo in the .m source (e.g. `NeQ[e^2-4*d*f]`, missing the
            # `,0`). Mathematica does NOT silently accept it either: Rubi guards
            # every predicate with `CheckArguments`, so the call stays unevaluated,
            # the `&&` guard is not True, and the rule never fires. Skipping it here
            # is therefore faithful to Rubi, not a limitation of this port.
            if 'positional argument' in str(e):
                raise ValueError(
                    f"upstream Rubi arity typo (rule is inert in Mathematica too): "
                    f"{type(e).__name__}: {e}")
            raise ValueError(f"generated rule not loadable: {type(e).__name__}: {e}")
        except Exception as e:
            raise ValueError(f"generated rule not loadable: {type(e).__name__}: {e}")

    def _translate_rule(self, ffl, rule_number: int, module_name: str,
                        load_ns: dict = None) -> Optional[str]:
        """Translate one ``SetDelayed`` FFL rule into SymPyReplacementPattern source text.

        Returns None when `ffl` is not an integration rule at all (see the
        `non_rules` counter in translate_module); raises ValueError when it is one
        but cannot be translated.
        """
        if not (isinstance(ffl, list) and len(ffl) >= 3 and ffl[0] == 'SetDelayed'):
            return None
        ffl = _rewrite_gamma_arity(ffl)
        lhs, rhs = ffl[1], ffl[2]
        if not isinstance(lhs, list) or lhs[0] != 'Int':
            return None  # a utility predicate defined in a rule file, not a rule

        # The integration variable is bound by the rule, so it is reserved rather
        # than a pattern wildcard, and is emitted as the canonical identifier `x`.
        reserved = _reserved_symbols(lhs)
        # Namespace the shortening round-trip verifies against. It must contain
        # everything the MODULE will have at import time, not just SymPy: the printed
        # short form references the module's declared scope locals by their bare names
        # (`k` in `Sum(..., [k, 1, n_/2])`, `r`, `s`, `u`, ...). Without them the
        # verification eval raises NameError and the shortener silently keeps the
        # verbose form -- which is what left the Sum/Star rules unshortened.
        short_ns = dict(_rubi_override_sympy_names())
        if load_ns:
            # ONLY the module's plain Symbols (its declared scope locals `k`/`r`/`s`,
            # the Min/Max ordering flags, ...). The printed short form names them bare,
            # e.g. `Sum(..., [k, 1, n_/2])`, and without them the verification eval
            # raises NameError and the shortener silently keeps the verbose form.
            # Merging the WHOLE module namespace instead would shadow the shortener's
            # own placeholders (`Not`, `Simplify`, ... come back as rubi_utils objects),
            # changing what the code evaluates to and defeating the round-trip for
            # ~1200 expressions -- measured.
            short_ns.update({name: value for name, value in load_ns.items()
                             if isinstance(value, _sympy_Symbol)})
        integrand_ffl = lhs[1]

        result_ffl, conditions = self._split_conditions(rhs)
        integrand_ffl, result_ffl, conditions = self._apply_head_wildcards(
            integrand_ffl, result_ffl, conditions)

        # Each translation below verifies its code by evaluating it, in the dict
        # passed as `namespace`. That dict is filled in place -- base SymPy names,
        # the reserved variable, then every wildcard discovered -- so passing a
        # FRESH dict per call keeps one rule's wildcards out of the next one.
        pattern_code, wild_defs, _symbols = ffl_to_sympy_short_code(
            integrand_ffl, reserved, namespace=dict(short_ns),
            custom_functions=_PATTERN_CUSTOM)

        plain_wilds, opt_wilds = self._wildcard_names(wild_defs)

        replacement_code, _, _symbols = ffl_to_sympy_short_code(
            result_ffl, reserved, namespace=dict(short_ns),
            custom_functions=_REPLACEMENT_CUSTOM,
            wildcards=plain_wilds, optional_wildcards=opt_wilds)

        constraints_frag, dropped_guards = self._translate_constraints(
            conditions, reserved, plain_wilds, opt_wilds, short_ns=short_ns)

        probe = (
            f"SymPyReplacementPattern(pattern=Int({pattern_code}, x), "
            f"constraints={constraints_frag}, replacement={replacement_code}, "
            f"module_name={module_name!r}, rule_number={rule_number})"
        )
        self._check_rule_loads(load_ns, probe, module_name, rule_number)

        lines_out = [f"    # Rule {rule_number}"]
        lines_out += [
            f"    # NOTE: dropped guard (function-head wildcard, not yet translatable): {g}"
            for g in dropped_guards
        ]
        lines_out += [
            f"    SymPyReplacementPattern(",
            f"        pattern=Int({pattern_code}, x),",
            f"        constraints={constraints_frag},",
            f"        replacement={replacement_code},",
            f"        module_name={module_name!r},",
            f"        rule_number={rule_number},",
            f"    ),",
        ]
        return '\n'.join(lines_out)


# =============================================================================
# Generation
# =============================================================================

def generate_all(json_path: Path, base_dir: Path,
                 section_filter: Optional[str] = None) -> None:
    """Generate all rule modules from the JSON."""
    print(f"Loading JSON from: {json_path}")
    entries = load_json_entries(json_path)
    groups  = group_entries_by_output(entries)

    filter_re = re.compile(section_filter) if section_filter else None
    translator = RubiRuleTranslator()

    generated = skipped_empty = skipped_filter = 0
    written_paths: List[Path] = []

    for out_rel, info in sorted(groups.items()):
        if filter_re and not filter_re.search(out_rel):
            skipped_filter += 1
            continue

        exprs = info['expressions']
        if not exprs:
            skipped_empty += 1
            continue

        source_files = info['source_files']
        source_desc  = ', '.join(source_files[:3])
        if len(source_files) > 3:
            source_desc += f' ... ({len(source_files)} total)'

        print(f"  {out_rel}  ({len(exprs)} exprs from {len(source_files)} files)")

        try:
            module_code = translator.translate_module(
                rules=exprs,
                module_name=info['description'],
                source_file=source_desc,
            )
        except Exception as exc:
            print(f"    ERROR translating {out_rel}: {exc}")
            continue

        output_path = base_dir / out_rel
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure __init__.py in every package directory
        for parent in list(output_path.relative_to(base_dir).parents)[:-1]:
            init = base_dir / parent / '__init__.py'
            if not init.exists():
                init.write_text('', encoding="utf-8", newline="\n")

        output_path.write_text(module_code, encoding='utf-8', newline="\n")
        written_paths.append(output_path)

        n_skipped = module_code.count('SKIPPED')
        n_ok      = len(exprs) - n_skipped
        print(f"    -> {n_ok} rules, {n_skipped} skipped")
        generated += 1

    changed, msg = strip_unused_imports(written_paths)
    print(f"Unused-import cleanup: {msg}")

    print(f"\nDone: {generated} modules generated "
          f"({skipped_empty} empty, {skipped_filter} filtered out).")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate MatchPy rules from Rubi fullformlist JSON'
    )
    parser.add_argument(
        '--json', type=Path, default=Path(DEFAULT_JSON),
        help='Path to rubi_fullformlist_results.json'
    )
    parser.add_argument(
        '--output-dir', '-o', type=Path, default=None,
        help='Base output directory (default: rubi_rules/ sibling of codegen/)'
    )
    parser.add_argument(
        '--filter', '-f', default=None, metavar='REGEX',
        help='Only generate output paths matching this regex '
             '(e.g. "r_1_1_1" or "algebraic")'
    )
    args = parser.parse_args()

    if not args.json.exists():
        print(f"ERROR: JSON not found: {args.json}")
        sys.exit(1)

    base_dir = args.output_dir or Path(os.path.dirname(os.path.dirname(__file__)))
    print(f"Output dir: {base_dir}")

    generate_all(args.json, base_dir, section_filter=args.filter)


if __name__ == '__main__':
    main()
