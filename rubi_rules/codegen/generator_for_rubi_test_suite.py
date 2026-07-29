#!/usr/bin/env python3
"""Generate Python test modules from the MathematicaSyntaxTestSuite repository.

Parses every ``*.m`` file using SymPy's MathematicaParser, stopping at the
fullformlist stage. Test cases are then converted to SymPy objects using the
same FFL-to-SymPy conversion approach shared with rule generation.

Generated modules contain direct SymPy expressions and no
``sympify('string expression')`` calls.

Usage
-----
    python generator_for_rubi_test_suite.py \
        --rubi-mathematica-test-suite-path /path/to/MathematicaSyntaxTestSuite

Dependencies
------------
    pip install sympy pydantic
"""

from __future__ import annotations

import argparse
import traceback
from pathlib import Path
from typing import Any, List, Optional, Tuple

import sympy
from sympy.parsing.mathematica import MathematicaParser

from sympy_wolfram import ffl_to_sympy_short_code
from sympy_wolfram.interpreter import FFLConverter


_NUMERIC_PREFIX = __import__('re').compile(r"^([\d]+(?:\.[\d]+)*)\s*(.*)")

# The emitted tests are written against a single canonical variable ``x``,
# which is therefore externally bound rather than a pattern wildcard.
_RESERVED = {'x': 'x'}


def _sanitize(name: str, is_file: bool) -> str:
    stem = name[:-2] if is_file and name.endswith('.m') else name
    m = _NUMERIC_PREFIX.match(stem)
    if m:
        num = m.group(1).replace('.', '_')
        desc = __import__('re').sub(r'[^a-z0-9]+', '_', m.group(2).strip().lower()).strip('_')
        return f't_{num}.py' if is_file else (f't_{num}_{desc}' if desc else f't_{num}')
    cleaned = __import__('re').sub(r'[^a-z0-9]+', '_', stem.lower()).strip('_')
    return f'{cleaned}.py' if is_file else cleaned


def _output_path(src: Path, src_root: Path, out_root: Path) -> Path:
    parts = src.relative_to(src_root).parts
    converted = [_sanitize(part, is_file=(index == len(parts) - 1)) for index, part in enumerate(parts)]
    return out_root.joinpath(*converted)


def _remove_comments(text: str) -> str:
    result, depth, i = [], 0, 0
    while i < len(text):
        two = text[i:i + 2]
        if two == '(*':
            depth += 1
            i += 2
        elif two == '*)':
            if depth > 0:
                depth -= 1
            i += 2
        elif depth == 0:
            result.append(text[i])
            i += 1
        else:
            i += 1
    return ''.join(result)


_PARSER = MathematicaParser()


def _parse_to_ffl(path: Path) -> Tuple[Optional[List], Optional[str]]:
    try:
        raw = path.read_text(encoding='utf-8', errors='replace')
        clean = _remove_comments(raw).strip()
        if not clean:
            return [], None
        tokens = _PARSER._from_mathematica_to_tokens(clean)
        ffl = _PARSER._from_tokens_to_fullformlist(tokens)
        if isinstance(ffl, list) and ffl and ffl[0] == 'CompoundExpression':
            return ffl[1:], None
        return [ffl], None
    except Exception as exc:
        tb = traceback.format_exc().splitlines()
        tail = '\n'.join(tb[-4:]) if len(tb) >= 4 else str(exc)
        return None, f'{type(exc).__name__}: {exc}\n{tail}'


def _try_int(val: Any) -> Optional[int]:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _extract_cases(exprs: List, converter: FFLConverter) -> Tuple[List[Tuple], int, set[str]]:
    cases: List[Tuple] = []
    all_symbols = set()
    skipped = 0
    for ffl in exprs:
        if not (isinstance(ffl, list) and len(ffl) == 5 and ffl[0] == 'List'):
            skipped += 1
            continue
        _, integrand_ffl, variable_ffl, num_steps_raw, integral_ffl = ffl
        num_steps = _try_int(num_steps_raw)
        if num_steps is None:
            skipped += 1
            continue
        try:
            integrand_ffl_p = converter.preprocess_test_ffl(integrand_ffl)
            variable_ffl_p = converter.preprocess_test_ffl(variable_ffl)
            integral_ffl_p = converter.preprocess_test_ffl(integral_ffl)
            # Convert to short code strings in one pass; simplify_code validates
            # via its internal eval round-trip and falls back to verbose code.
            i_code, _, __, i_symbols = ffl_to_sympy_short_code(integrand_ffl_p, _RESERVED)
            v_code, _, __, v_symbols = ffl_to_sympy_short_code(variable_ffl_p, _RESERVED)
            r_code, _, __, r_symbols = ffl_to_sympy_short_code(integral_ffl_p, _RESERVED)
            all_symbols.update(i_symbols)
            all_symbols.update(v_symbols)
            all_symbols.update(r_symbols)
        except Exception:
            skipped += 1
            continue
        cases.append((i_code, v_code, num_steps, r_code))
    return cases, skipped, all_symbols


_BASE_OBJECTS = """\
# -*- coding: utf-8 -*-
\"\"\"Core objects for generated Rubi test-suite cases.\"\"\"
from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from sympy import Expr as SymPyExpr
from sympy import Symbol as SymPySymbol


class RubiTestSuiteCase(BaseModel):
    \"\"\"One MathematicaSyntaxTestSuite case translated to Python/SymPy.\"\"\"
    model_config = ConfigDict(arbitrary_types_allowed=True)

    integrand: SymPyExpr
    variable: SymPySymbol
    num_steps: int
    integral: SymPyExpr
"""

_PKG_INIT = '"""Generated Rubi MathematicaSyntaxTestSuite modules."""\n'


def _collect_symbols_from_ns(ns: dict[str, Any]) -> set:
    """Return names of plain Symbol bindings in a converter eval namespace."""
    return {name for name, val in ns.items() if type(val) is sympy.Symbol}


def _render_symbol_declarations(symbol_names: List[str]) -> List[str]:
    if not symbol_names:
        return []
    if len(symbol_names) == 1:
        return [
            '# Free symbols used by round-trippable string expressions.',
            f"{symbol_names[0]} = symbols({symbol_names[0]!r})",
            '',
        ]
    return [
        '# Free symbols used by round-trippable string expressions.',
        f"{', '.join(symbol_names)} = symbols({' '.join(symbol_names)!r})",
        '',
    ]


def _render_module(cases: list[Tuple], rel_source: str, converter: FFLConverter, symbol_set: set[str]) -> str:
    # cases: (integrand_code, variable_code, num_steps, integral_code) — already rendered.
    # Symbol names are collected from the converter's eval_ns (accumulated during _extract_cases).
    symbol_names = sorted(_collect_symbols_from_ns(converter.eval_ns))
    lines = [
        '# -*- coding: utf-8 -*-',
        '"""Generated from MathematicaSyntaxTestSuite.',
        '',
        f'Source: {rel_source}',
        '"""',
        '',
        'from sympy import *',
        'import sympy',
        '',
        'from sympy_wolfram.mathematica_functions import (',
        '    ExpIntegralEi, LogIntegral, ProductLog, Identity,',
        ')',
        'from sympy_wolfram.objects import Gamma',
        '',
        'from rubi_rules.rubi_test_suite.base_test_objects import RubiTestSuiteCase',
        '',
        f'SOURCE_FILE = {rel_source!r}',
        '',
    ]
    lines.extend(_render_symbol_declarations(symbol_names))
    lines.extend(_render_symbol_declarations(sorted(symbol_set)))
    lines.extend([
        '# Third tuple element: number of Rubi integration steps used.',
        'TEST_CASES = [',
    ])
    for i_code, v_code, num_steps, r_code in cases:
        lines.append(
            '    RubiTestSuiteCase(\n'
            f'        integrand={i_code},\n'
            f'        variable={v_code},\n'
            f'        num_steps={num_steps},\n'
            f'        integral={r_code},\n'
            '    ),'
        )
    lines.append(']\n')
    return '\n'.join(lines)


def generate_test_suite(source_root: Path, output_root: Path) -> List[Tuple]:
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / '__init__.py').write_text(_PKG_INIT, encoding='utf-8', newline="\n")
    (output_root / 'base_test_objects.py').write_text(_BASE_OBJECTS, encoding='utf-8', newline="\n")

    file_stats = []
    for src in sorted(source_root.rglob('*.m')):
        ffl_exprs, parse_error = _parse_to_ffl(src)
        # Fresh converter per file so symbol scope stays file-local.
        # 'x' is the canonical variable of the emitted tests, so it is bound
        # externally rather than being a pattern wildcard.
        converter = FFLConverter(reserved_symbols=_RESERVED)
        if parse_error:
            cases, skipped, symbol_set = [], 0, set()
        else:
            cases, skipped, symbol_set = _extract_cases(ffl_exprs or [], converter)

        out = _output_path(src, source_root, output_root)
        out.parent.mkdir(parents=True, exist_ok=True)

        current = out.parent
        while current != output_root.parent:
            init_f = current / '__init__.py'
            if not init_f.exists():
                init_f.write_text('', encoding='utf-8', newline="\n")
            current = current.parent

        rel_src = src.relative_to(source_root).as_posix()
        out.write_text(_render_module(cases, rel_src, converter, symbol_set), encoding='utf-8', newline="\n")
        file_stats.append((src, out, len(cases), skipped))
    return file_stats


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description='Generate Python Rubi test-suite modules from MathematicaSyntaxTestSuite.'
    )
    ap.add_argument(
        '--rubi-mathematica-test-suite-path',
        required=True,
        type=Path,
        metavar='PATH',
        help='Root of the cloned MathematicaSyntaxTestSuite repository.',
    )
    ap.add_argument(
        '--output-root',
        type=Path,
        default=None,
        metavar='PATH',
        help='Override output directory (default: rubi_rules/rubi_test_suite/ next to this script).',
    )
    return ap


def main() -> None:
    args = _build_parser().parse_args()

    source_root = args.rubi_mathematica_test_suite_path.resolve()
    if not source_root.exists():
        raise SystemExit(f'ERROR: path not found: {source_root}')

    default_out = Path(__file__).resolve().parent.parent / 'rubi_test_suite'
    output_root = args.output_root.resolve() if args.output_root else default_out

    print(f'SymPy   {sympy.__version__}')
    print(f'Source  {source_root}')
    print(f'Output  {output_root}')
    print()

    stats = generate_test_suite(source_root, output_root)

    total_cases = sum(s[2] for s in stats)
    total_skipped = sum(s[3] for s in stats)

    print(f'Files   : {len(stats)}')
    print(f'Cases   : {total_cases}')
    print(f'Skipped : {total_skipped}')
    print('\nSample:')
    for src, out, n_c, n_s in stats[:5]:
        print(f'  {src.relative_to(source_root)}')
        print(f'    -> {out.relative_to(output_root)}  ({n_c} cases, {n_s} skipped)')


if __name__ == '__main__':
    main()
