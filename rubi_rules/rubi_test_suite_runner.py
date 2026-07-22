# -*- coding: utf-8 -*-
"""Run the generated Rubi test-suite corpus through ``rubi_integrate``.

The corpus lives in ``rubi_rules/rubi_test_suite/`` as ``RubiTestSuiteCase``
entries (integrand, variable, num_steps, integral). This module walks it, tries
to integrate each case, and tallies the outcome.

Normally driven by ``run_rubi_test_suite.sh``, which supplies a timestamped
output path; it can also be run directly:

    python3 -m rubi_rules.rubi_test_suite_runner --limit 200 --out /tmp/run.log

Statuses
--------
SOLVED           complete antiderivative (no residual ``Int``, no CannotIntegrate)
UNSOLVED         returned, but still contains an unevaluated ``Int``
CANNOTINTEGRATE  the ruleset explicitly gave up
TIMEOUT          exceeded the per-integral time limit
ERROR            raised

Only SOLVED counts as solvable. Correctness of the antiderivative is NOT checked
here -- that is what the pytest suite does; this measures coverage.
"""
from __future__ import annotations

import argparse
import gc
import glob
import importlib.util
import os
import random
import signal
import sys
import time
from datetime import datetime, timezone

import sympy
from sympy import Function

SUITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rubi_test_suite')

STATUSES = ('SOLVED', 'UNSOLVED', 'CANNOTINTEGRATE', 'TIMEOUT', 'ERROR')


class _Timeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise _Timeout()


def _rss_mb() -> float:
    """Resident set size of this process, in MiB (0.0 if unavailable)."""
    try:
        with open('/proc/self/status', encoding='ascii') as fh:
            for line in fh:
                if line.startswith('VmRSS:'):
                    return int(line.split()[1]) / 1024.0
    except OSError:
        pass
    return 0.0


def _reclaim_memory():
    """Try to give memory back: drop SymPy's caches and collect garbage.

    MEASURED: this recovers very little. On a loaded rule set, 40 integrations grow
    RSS by ~150 MiB and a full clear_cache()+gc gives back ~2 MiB, so the growth is
    NOT in SymPy's expression cache. It is worth attempting before giving up, but
    the real protection is the hard stop in run(): a sweep grows ~3.75 MiB per test,
    so a few thousand tests will exhaust memory and must be halted deliberately
    rather than be OOM-killed with no summary.
    """
    try:
        from sympy.core.cache import clear_cache
        clear_cache()
    except Exception:                                    # noqa: BLE001
        pass
    gc.collect()


def discover(file_glob: str = 't_*.py'):
    """Return (files, cases) for the corpus, without integrating anything.

    Kept separate from the run so the total can be reported up front -- a full
    sweep takes hours and it matters to know the size before committing to it.
    """
    files = sorted(glob.glob(os.path.join(SUITE_DIR, '**', file_glob), recursive=True))
    cases = []
    for path in files:
        for case in _load_cases(path):
            cases.append((path, case))
    return files, cases


def _load_cases(path: str):
    name = 'rubi_suite_' + os.path.basename(path)[:-3] + str(abs(hash(path)) % 99999)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:                                    # noqa: BLE001
        return []                                        # unloadable file: no cases
    return getattr(module, 'TEST_CASES', []) or []


def classify(integrand, variable, timeout: int):
    """Integrate one case and return (status, detail)."""
    from rubi_rules.base_objects import rubi_integrate, Int as RubiInt

    signal.alarm(timeout)
    try:
        result = rubi_integrate(integrand, variable)
    except _Timeout:
        return 'TIMEOUT', ''
    except RecursionError:
        return 'ERROR', 'RecursionError'
    except Exception as exc:                             # noqa: BLE001
        return 'ERROR', f'{type(exc).__name__}: {exc}'
    finally:
        signal.alarm(0)

    text = str(result)
    if 'CannotIntegrate' in text:
        return 'CANNOTINTEGRATE', ''
    if result.has(RubiInt) or result.has(Function('Int')) or 'Int(' in text:
        return 'UNSOLVED', ''
    return 'SOLVED', ''


def run(out_path: str, file_glob: str = 't_*.py', limit: int = 0,
        timeout: int = 8, seed=None, shuffle: bool = True,
        mem_limit_mb: int = 4096, echo=print) -> dict:
    """Run the corpus, writing a full record to *out_path*. Returns the tally."""
    signal.signal(signal.SIGALRM, _on_alarm)

    echo('Discovering corpus ...')
    files, cases = discover(file_glob)

    # Load the rule set BEFORE the timed loop. It takes ~35s, and if it happened
    # inside the first classify() call it would run under that test's alarm: the
    # first test would be charged for the load (and could be recorded as a spurious
    # TIMEOUT), and a signal could interrupt the load itself.
    echo('Loading the Rubi rule set (once) ...')
    t_load = time.time()
    from rubi_rules.base_objects import rubi_integrate as _warm
    _warm(sympy.Symbol('x'), sympy.Symbol('x'))
    echo(f'  rule set ready in {time.time() - t_load:.0f}s')

    total_available = len(cases)

    # Shuffle BEFORE applying --limit. The corpus is stored in curriculum order
    # (all of t_1_algebraic first, ...), so a truncated in-order run samples one
    # family and its solve-rate is not representative of the whole corpus.
    if shuffle:
        if seed is None:
            seed = random.randrange(2 ** 32)
        random.Random(seed).shuffle(cases)
    if limit:
        cases = cases[:limit]

    # The loaded rule set alone occupies ~1.2 GiB, so the limit is meaningless
    # unless it clears that floor with room for the run itself. Refuse an
    # unsatisfiable limit up front instead of "stopping early" on the first check.
    baseline_mb = _rss_mb()
    floor_mb = int(baseline_mb + 256)
    if mem_limit_mb < floor_mb:
        raise SystemExit(
            f'--mem-limit-mb {mem_limit_mb} is below the {floor_mb} MiB floor: the '
            f'rule set alone already holds {baseline_mb:.0f} MiB. Raise the limit.')
    # Reclaiming barely helps (see _reclaim_memory), so the soft threshold sits high;
    # it is a last attempt before the hard stop, not the main defence.
    mem_soft_mb = max(int(mem_limit_mb * 0.9), floor_mb)

    started = datetime.now(timezone.utc)
    header = [
        f'# Rubi test-suite run',
        f'# started            : {started.isoformat(timespec="seconds")}',
        f'# suite directory    : {SUITE_DIR}',
        f'# file glob          : {file_glob}',
        f'# files discovered   : {len(files)}',
        f'# tests discovered   : {total_available}',
        f'# tests to run       : {len(cases)}' + ('  (--limit applied)' if limit else ''),
        f'# per-test timeout   : {timeout}s  (rule-set load excluded)',
        f'# order              : ' + (f'shuffled, seed={seed}' if shuffle else 'corpus order'),
        f'# memory limit       : {mem_limit_mb} MiB'
        f'  (rule set baseline {baseline_mb:.0f} MiB;'
        f' reclaim above {mem_soft_mb} MiB)',
        '#',
        '# STATUS | file | num_steps | integrand | detail',
    ]
    echo('\n'.join(header))

    counts = dict.fromkeys(STATUSES, 0)
    stopped_early = ''
    t0 = time.time()
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(header) + '\n')
        fh.flush()
        for i, (path, case) in enumerate(cases, 1):
            rel = os.path.relpath(path, SUITE_DIR)
            try:
                status, detail = classify(case.integrand, case.variable, timeout)
            except Exception as exc:                     # noqa: BLE001
                status, detail = 'ERROR', f'harness: {type(exc).__name__}: {exc}'
            counts[status] += 1
            steps = getattr(case, 'num_steps', '')
            fh.write(f'{status} | {rel} | {steps} | {case.integrand} | {detail}\n')
            fh.flush()                                   # partial runs stay useful
            if i % 25 == 0:
                rss = _rss_mb()
                if rss > mem_soft_mb:
                    _reclaim_memory()
                    after = _rss_mb()
                    echo(f'  [memory] {rss:.0f} MiB -> {after:.0f} MiB after reclaim')
                    if after > mem_limit_mb:
                        stopped_early = (
                            f'STOPPED EARLY at test {i}: {after:.0f} MiB still above '
                            f'the {mem_limit_mb} MiB limit after reclaiming')
                        echo('# ' + stopped_early)
                        fh.write('# ' + stopped_early + '\n')
                        break
            if i % 100 == 0:
                echo(f'  {i}/{len(cases)}  rss={_rss_mb():.0f}MiB  '
                     + '  '.join(f'{s}={counts[s]}' for s in STATUSES))

        elapsed = time.time() - t0
        ran = sum(counts.values())
        summary = [
            '',
            '# ' + '=' * 68,
            f'# TOTAL TESTS RUN     : {ran}',
            f'# tests discovered    : {total_available} (in {len(files)} files)',
        ]
        for status in STATUSES:
            pct = (100.0 * counts[status] / ran) if ran else 0.0
            summary.append(f'#   {status:<16}: {counts[status]:>6}  ({pct:5.1f}%)')
        solvable = (100.0 * counts['SOLVED'] / ran) if ran else 0.0
        summary += [
            f'# SOLVABLE            : {solvable:.1f}%',
            f'# elapsed             : {elapsed:.0f}s',
            f'# peak RSS            : {_rss_mb():.0f} MiB',
            f'# order               : ' + (f'shuffled, seed={seed}' if shuffle else 'corpus order'),
            f'# finished            : {datetime.now(timezone.utc).isoformat(timespec="seconds")}',
            '# ' + '=' * 68,
        ]
        if stopped_early:
            summary.insert(1, '# ' + stopped_early)
        fh.write('\n'.join(summary) + '\n')
    echo('\n'.join(summary))
    echo(f'\nRun saved to: {out_path}')

    counts['_total_run'] = ran
    counts['_total_discovered'] = total_available
    counts['_files'] = len(files)
    counts['_elapsed'] = elapsed
    return counts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', required=True, help='path of the run log to write')
    parser.add_argument('--glob', default='t_*.py',
                        help="which corpus files to run (default 't_*.py'; use "
                             "'*_problems.py' for the independent suites)")
    parser.add_argument('--limit', type=int, default=0,
                        help='run only the first N tests (0 = all)')
    parser.add_argument('--timeout', type=int, default=8,
                        help='per-test time limit in seconds (default 8)')
    parser.add_argument('--seed', type=int, default=None,
                        help='seed for the shuffle (recorded in the log; pass it '
                             'back to reproduce a run exactly)')
    parser.add_argument('--no-shuffle', action='store_true',
                        help='run in corpus order instead of shuffling')
    parser.add_argument('--mem-limit-mb', type=int, default=6144,
                        help='stop cleanly if RSS stays above this after '
                             'attempting to reclaim (default 6144 MiB; the '
                             'rule set alone needs ~1.2 GiB and a sweep adds '
                             '~3.75 MiB per test)')
    parser.add_argument('--count-only', action='store_true',
                        help='report how many tests exist and exit')
    args = parser.parse_args(argv)

    if args.count_only:
        files, cases = discover(args.glob)
        print(f'files: {len(files)}   tests: {len(cases)}')
        return 0

    run(args.out, file_glob=args.glob, limit=args.limit, timeout=args.timeout,
        seed=args.seed, shuffle=not args.no_shuffle,
        mem_limit_mb=args.mem_limit_mb)
    return 0


if __name__ == '__main__':
    sys.exit(main())
