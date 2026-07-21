#!/usr/bin/env python3
"""
parse_rubi_to_ffl.py
--------------------
Parse every Wolfram Mathematica .m rule file in the Rubi repository
recursively using SymPy's MathematicaParser.  For each file it extracts
individual expressions, converts them to the **fullformlist** intermediate
representation, and collects all parsing failures with full error details.

Output format is identical to rubi_fullformlist_results.json produced by
the companion notebook.

Usage
-----
    # With explicit path:
    python parse_rubi_to_ffl.py --rubi-folder-path /path/to/Rubi
    python parse_rubi_to_ffl.py --rubi-folder-path /path/to/Rubi \\
                                --output-path /tmp/results.json

    # Zero-args (uses _DEFAULT_RUBI_ROOT below):
    python parse_rubi_to_ffl.py

Dependencies
------------
    pip install sympy
"""

import argparse
import json
import re
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sympy
from sympy.parsing.mathematica import MathematicaParser


_DEFAULT_RUBI_ROOT = Path(
    "../Rubi"
)


# ---------------------------------------------------------------------------
# Comment stripping
# ---------------------------------------------------------------------------

def _remove_comments(text: str) -> str:
    """Remove (* ... *) comment blocks, handling nesting correctly."""
    result, depth, i = [], 0, 0
    while i < len(text):
        if text[i : i + 2] == "(*":
            depth += 1
            i += 2
        elif text[i : i + 2] == "*)":
            if depth > 0:
                depth -= 1
            i += 2
        elif depth == 0:
            result.append(text[i])
            i += 1
        else:
            i += 1
    return "".join(result)


# ---------------------------------------------------------------------------
# File parser
# ---------------------------------------------------------------------------

_GLOBAL_PARSER = MathematicaParser()


def parse_m_file(path: Path) -> Tuple[Optional[List], Optional[str]]:
    """
    Read *path*, strip comments, and parse the entire content as one
    Mathematica program.  Returns:

      (list_of_fullformlists, None)  – one item per top-level expression
      (None, error_message)          – if the parser raises

    The tokeniser + fullformlist builder handle multi-line expressions
    natively, so we never need to pre-split on newlines.  A file with N
    top-level rules is parsed as a single
    ``CompoundExpression[rule1, rule2, ..., ruleN]``; we unwrap that into
    a plain Python list of individual fullformlist items.
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        clean = _remove_comments(raw).strip()
        if not clean:
            return [], None
        # Rubi co-opts Wolfram's ``\[Star]`` infix operator as a display-friendly
        # product. SymPy's parser has no rule for ``\[Star]`` and parses it as a
        # POSTFIX operator; when ``\[Star]`` and its right operand are on the SAME
        # line the operand survives (as a flat ``Times[.., [tail,'Star'], .., v]``
        # that codegen's _reconstruct_star rebuilds into ``Star[u, v]``), but when
        # the ``\[Star]`` ends a source LINE before the next factor
        # (``Simp[...] \[Star]\n Int[...]``) the right operand is silently DROPPED --
        # turning an integral into a non-integral (a wrong answer). Join that
        # line-continuation (collapse the whitespace after ``\[Star]`` to a single
        # space) so every ``\[Star]`` is inline and its operand is preserved; the
        # ``Star`` marker itself is kept and rebuilt downstream into a Star[u, v]
        # node (whose runtime behaviour is defined in rubi_utils).
        clean = re.sub(r"\\\[Star\]\s+", r"\\[Star] ", clean)
        # Wolfram's POSTFIX derivative shorthand ``f_'[x_]``. SymPy's parser has no
        # rule for the ``'`` operator either, and mis-associates it: the whole
        # surrounding Plus/Times collapses into a bogus application whose head is
        # ``Derivative[f_]``, which then fails translation. Rubi writes the SAME
        # thing canonically as ``Derivative[1][f_][x_]`` elsewhere in these very
        # files, and Mathematica confirms the two forms are *identical*:
        #   FullForm[Hold[f_'[x_]]] === FullForm[Hold[Derivative[1][f_][x_]]]
        # so rewriting to the canonical spelling is exact, not an approximation.
        # It also routes these rules through the normal Derivative[n_][f_][x_] path.
        clean = re.sub(r"\b([A-Za-z][A-Za-z0-9]*_)'", r"Derivative[1][\1]", clean)
        tokens = _GLOBAL_PARSER._from_mathematica_to_tokens(clean)
        ffl = _GLOBAL_PARSER._from_tokens_to_fullformlist(tokens)
        # Multiple top-level expressions arrive as CompoundExpression[e1, e2, ...]
        if isinstance(ffl, list) and ffl and ffl[0] == "CompoundExpression":
            return ffl[1:], None
        return [ffl], None  # single expression
    except Exception as exc:
        tb = traceback.format_exc().splitlines()
        tail = "\n".join(tb[-4:]) if len(tb) >= 4 else str(exc)
        return None, f"{type(exc).__name__}: {exc}\n{tail}"


# ---------------------------------------------------------------------------
# JSON serialisation helper
# ---------------------------------------------------------------------------

def _make_serialisable(obj: Any) -> Any:
    """Recursively ensure every object is JSON-serialisable."""
    if isinstance(obj, list):
        return [_make_serialisable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _make_serialisable(v) for k, v in obj.items()}
    try:
        json.dumps(obj)  # test
        return obj
    except (TypeError, ValueError):
        return repr(obj)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Parse every .m rule file in a cloned Rubi repository to "
            "SymPy fullformlist JSON."
        ),
    )
    ap.add_argument(
        "--rubi-folder-path",
        required=False,
        metavar="PATH",
        type=Path,
        default=_DEFAULT_RUBI_ROOT,
        help=(
            f"Root of the cloned Rubi repository "
            f"(default: {_DEFAULT_RUBI_ROOT})."
        ),
    )
    ap.add_argument(
        "--output-path",
        metavar="PATH",
        type=Path,
        default=None,
        help=(
            "Where to write the JSON output. "
            "Defaults to <rubi-folder-path>/rubi_fullformlist_results.json"
        ),
    )
    args = ap.parse_args()

    rubi_root: Path = args.rubi_folder_path.resolve()
    if not rubi_root.exists():
        print(f"ERROR: --rubi-folder-path not found: {rubi_root}", file=sys.stderr)
        sys.exit(1)

    output_path: Path = (
        args.output_path
        if args.output_path is not None
        else rubi_root / "rubi_fullformlist_results.json"
    )

    parse_rubi_folder_recursively(rubi_root, output_path)


def parse_rubi_folder_recursively(rubi_root: Path, output_path: Path | None = None) -> None:

    if output_path is None:
        output_path = rubi_root / "rubi_fullformlist_results.json"

    print(f"Python  {sys.version.split()[0]}")
    print(f"SymPy   {sympy.__version__}")
    print(f"Root    {rubi_root}")
    print(f"Output  {output_path}")

    # ── Discover and parse ───────────────────────────────────────────────────
    m_files = sorted(rubi_root.rglob("*.m"))
    print(f"\nFound {len(m_files)} .m file(s) under {rubi_root}\n")

    file_results: List[Dict] = []
    for filepath in m_files:
        ffls, error = parse_m_file(filepath)
        file_results.append({
            "file":        str(filepath.relative_to(rubi_root)),
            "file_error":  error,
            "expressions": ffls or [],
        })

    # ── Summary ──────────────────────────────────────────────────────────────
    n_ok     = sum(1 for r in file_results if not r["file_error"])
    n_failed = sum(1 for r in file_results if r["file_error"])
    n_exprs  = sum(len(r["expressions"]) for r in file_results)

    print("=" * 50)
    print(f"  Files parsed OK  : {n_ok}")
    print(f"  Files failed     : {n_failed}")
    print(f"  Expressions total: {n_exprs}")
    print("=" * 50)

    # ── Error report ─────────────────────────────────────────────────────────
    failed = [r for r in file_results if r["file_error"]]
    if failed:
        print(f"\n{'='*60}\nFILES THAT FAILED TO PARSE ({len(failed)})\n{'='*60}")
        for r in failed:
            err_short = r["file_error"].replace("\n", " ")[:200]
            print(f"\n  File : {r['file']}")
            print(f"  Error: {err_short}")

        error_types: Dict[str, int] = defaultdict(int)
        for r in failed:
            key = r["file_error"].splitlines()[0][:80]
            error_types[key] += 1

        print(f"\n{'='*60}\nERROR TYPES\n{'='*60}")
        for err, count in sorted(error_types.items(), key=lambda x: -x[1]):
            print(f"  {count:4d}x  {err}")

    # ── Write JSON ───────────────────────────────────────────────────────────
    serialised = _make_serialisable(file_results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(serialised, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nResults written to {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
