#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate MatchPy integration rules from the Rubi pre-computed JSON.

Usage (from matchpy-wip/matchpy/ directory):
    python -B -m rubi_rules.codegen.generate [--json PATH] [--output-dir DIR] [--filter REGEX]

The script reads the pre-computed fullformlist JSON produced from the Rubi
Mathematica repository and translates every entry into a Python module of
RubiRulePattern definitions.

Defaults:
    --json     : rubi_fullformlist_results.json
    --output-dir: rubi_rules/  (auto-detected relative to this script)
    --filter   : no filter — generate everything
"""
import argparse
import copy
import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict

from rubi_rules.utils import rubi_utils
from sympy_wolfram import FFLConverter, mathematica_expressions
from sympy_wolfram.mathematica_parser import ffl_to_sympy_short_code


# =============================================================================
# Rubi-specific FFL helpers (operate on Int[integrand, x_Symbol] structure)
# =============================================================================

def _extract_fixed_var_from_lhs(lhs) -> str:
    """Extract fixed variable name from Int[..., x_Symbol] LHS."""
    if isinstance(lhs, list) and lhs[0] == 'Int' and len(lhs) >= 3:
        var_pat = lhs[2]
        if isinstance(var_pat, list) and var_pat[0] == 'Pattern':
            return var_pat[1]
    return 'x'


def _collect_wildcards_from_rules(converter, rules):
    """Pre-scan FFL rules to collect all wildcard names.

    Assumes rules are SetDelayed[Int[...], ...] structure.
    Returns (non_optional_set, optional_set).
    """
    all_non_optional = set()
    all_optional = set()
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
        converter.fixed_var = _extract_fixed_var_from_lhs(lhs)
        try:
            converter.convert(lhs[1], is_pattern=True)
        except Exception:
            pass
        try:
            converter.convert(rhs, is_pattern=True)
        except Exception:
            pass
        all_non_optional.update(converter.wildcards_non_optional)
        all_optional.update(converter.wildcards_optional)
    return all_non_optional, all_optional


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
    "D": "D",
    # Additional Rubi-specific utility functions
    'Dist': 'Dist',
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
    'Complex': 'Complex',
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
    'PolyGamma': 'sympy.polygamma',
    'Factorial': 'sympy.factorial',
    # Other special functions
    'PolyLog': 'sympy.polylog',
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
    custom['List'] = ('List', mathematica_expressions.List)
    return custom


def _build_constraint_custom_functions() -> dict:
    """Build custom_functions dict for constraint FFL processing.

    IMPORTANT: We do NOT add entries for heads already in FFLConverter.SYMPY_FUNC_MAP
    or SYMPY_LOGIC_MAP. Those are handled naturally by FFLConverter.
    """
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
    return custom


_REPLACEMENT_CUSTOM = _build_replacement_custom_functions()
_CONSTRAINT_CUSTOM = _build_constraint_custom_functions()


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


def group_entries_by_output(entries: List[dict]) -> Dict[str, dict]:
    """Group JSON entries by output path, merging expressions for duplicates."""
    groups: Dict[str, dict] = {}
    for entry in entries:
        fpath = entry.get('file', '')
        exprs = entry.get('expressions') or []
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
    """Translate FFL rules into Python source with RubiRulePattern objects."""

    def __init__(self):
        self._converter = FFLConverter()

    def translate_module(self, rules: List, module_name: str, source_file: str = '') -> str:
        """Translate FFL rules into a Python module with RubiRulePattern list."""
        all_non_optional, all_optional = _collect_wildcards_from_rules(self._converter, rules)

        header = self._generate_header(module_name, source_file)

        # Generate wildcard declarations
        wc_lines = []
        for name in sorted(all_non_optional | all_optional):
            if name == self._converter.fixed_var:
                continue
            if name in all_optional:
                wc_lines.append(f"_{name}_ = WildSymbol('{name}', optional_value=IDENTITY_ELEMENT)")
            if name in all_non_optional:
                wc_lines.append(f"{name}_ = WildSymbol('{name}')")
        wc_section = '\n'.join(wc_lines) + '\n\n' if wc_lines else ''

        # Build eval namespace with wildcard symbols for simplification
        import sympy
        eval_ns = dict(self._converter.eval_ns)
        eval_ns['x'] = sympy.Symbol('x')
        eval_ns['SympyTuple'] = sympy.Tuple
        for name in all_non_optional:
            eval_ns[f'{name}_'] = sympy.Symbol(f'{name}_')
        for name in all_optional:
            eval_ns[f'_{name}_'] = sympy.Symbol(f'_{name}_')

        # Generate rules (1-indexed)
        rule_lines = []
        skipped = 0
        for i, rule in enumerate(rules):
            try:
                code = self._translate_rule(rule, i + 1, module_name, eval_ns)
                if code:
                    rule_lines.append(code)
                else:
                    skipped += 1
            except Exception as e:
                skipped += 1
                rule_lines.append(f"    # Rule {i + 1}: SKIPPED - {type(e).__name__}: {e}")

        footer = self._generate_footer(len(rules) - skipped, skipped)
        rules_body = '\n'.join(rule_lines)
        return header + wc_section + 'RULES = [\n' + rules_body + '\n' + footer

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
# This file contains Rubi integration rules as RubiRulePattern objects.
# Re-run the generator to update.
# =============================================================================
import sympy
from sympy import Integer, Integral, Lambda, Rational, Symbol, Tuple as SympyTuple, Eq, Ne, Lt, Gt, Le, Ge, log, sqrt, pi, I, oo
from rubi_rules.utils.rubi_utils import *  # bare-name access; sympy imports below override any conflicts (e.g. Not)
from sympy.logic.boolalg import Or, Not, And
from sympy import (sin, cos, tan, sec, csc, cot, asin, acos, atan, atan2, asec, acsc, acot,
                   sinh, cosh, tanh, sech, csch, coth, asinh, acosh, atanh, asech, acsch, acoth,
                   exp, Abs, diff, denom, frac, floor, root, simplify,
                   elliptic_e, elliptic_f, hyper, appellf1)

from sympy_objects.wild import WildSymbol, IDENTITY_ELEMENT
from rubi_rules.base_objects import Int, RubiRulePattern
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

# --- Wildcard symbols ---
# dot wildcards (must match exactly one expression)
# optional wildcards (can match identity element if absent in commutative ops)

"""

    def _generate_footer(self, n_rules: int, n_skipped: int) -> str:
        return f"""
]

# Summary: {n_rules} rules translated, {n_skipped} skipped
"""

    # =========================================================================
    # Rule translation
    # =========================================================================

    def _translate_rule(self, ffl, rule_number: int, module_name: str,
                        eval_ns: dict = None) -> Optional[str]:
        """Translate a single SetDelayed FFL rule into a RubiRulePattern string."""
        if not isinstance(ffl, list) or not ffl or ffl[0] != 'SetDelayed':
            return None
        if len(ffl) < 3:
            return None

        lhs = ffl[1]
        rhs = ffl[2]

        if not isinstance(lhs, list) or lhs[0] != 'Int':
            return None

        # Determine integration variable
        fixed_var = _extract_fixed_var_from_lhs(lhs)

        integrand_ffl = lhs[1]

        # Extract top-level and nested replacement conditions.
        condition_ffls: List[object] = []
        result_ffl = rhs
        if isinstance(rhs, list) and rhs[0] == 'Condition':
            result_ffl = rhs[1]
            condition_ffls.append(rhs[2])
        result_ffl, nested_condition_ffls = _extract_nested_with_condition(result_ffl)
        condition_ffls.extend(nested_condition_ffls)

        # --- Pattern: use ffl_to_sympy_short_code (discovers wildcards) ---
        pattern_code, _ns, wild_defs, _symbols = ffl_to_sympy_short_code(
            integrand_ffl,
            fixed_var=fixed_var,
        )

        # Extract wildcard names from wild_defs for propagation
        non_opt_wildcards: set = set()
        opt_wildcards: set = set()
        for d in wild_defs:
            var_name = d.split('=')[0].strip()
            if var_name.startswith('_') and var_name.endswith('_'):
                opt_wildcards.add(var_name[1:-1])
            elif var_name.endswith('_'):
                non_opt_wildcards.add(var_name[:-1])

        # --- Replacement: use ffl_to_sympy_short_code with custom_functions ---
        replacement_code, _, _, _symbols = ffl_to_sympy_short_code(
            result_ffl,
            fixed_var=fixed_var,
            custom_functions=_REPLACEMENT_CUSTOM,
            wildcards=non_opt_wildcards,
            optional_wildcards=opt_wildcards,
        )

        # --- Constraints: use ffl_to_sympy_short_code with custom_functions ---
        # If condition is And[...], flatten into separate constraint items
        # (the constraints tuple already implies conjunction).
        constraint_parts: List[str] = []
        for condition_ffl in condition_ffls:
            if isinstance(condition_ffl, list) and condition_ffl[0] == 'And':
                # Flatten top-level And into separate constraints.
                for child in condition_ffl[1:]:
                    code, _, _, _symbols = ffl_to_sympy_short_code(
                        child,
                        fixed_var=fixed_var,
                        custom_functions=_CONSTRAINT_CUSTOM,
                        wildcards=non_opt_wildcards,
                        optional_wildcards=opt_wildcards,
                    )
                    constraint_parts.append(code)
            else:
                code, _, _, _symbols = ffl_to_sympy_short_code(
                    condition_ffl,
                    fixed_var=fixed_var,
                    custom_functions=_CONSTRAINT_CUSTOM,
                    wildcards=non_opt_wildcards,
                    optional_wildcards=opt_wildcards,
                )
                constraint_parts.append(code)
        constraint_str = ', '.join(constraint_parts)

        # Build the RubiRulePattern entry
        lines_out = []
        lines_out.append(f"    # Rule {rule_number}")
        lines_out.append(f"    RubiRulePattern(")
        lines_out.append(f"        pattern=Int({pattern_code}, x),")
        if constraint_str:
            lines_out.append(f"        constraints=({constraint_str},),")
        else:
            lines_out.append(f"        constraints=(),")
        lines_out.append(f"        replacement={replacement_code},")
        lines_out.append(f"        module_name={module_name!r},")
        lines_out.append(f"        rule_number={rule_number},")
        lines_out.append(f"    ),")
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

        n_skipped = module_code.count('SKIPPED')
        n_ok      = len(exprs) - n_skipped
        print(f"    -> {n_ok} rules, {n_skipped} skipped")
        generated += 1

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
