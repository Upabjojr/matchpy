# -*- coding: utf-8 -*-
"""`eager_Apart` applies partial fractions TERMWISE over a sum.

sympy's `apart` recombines an Add over the common denominator before decomposing.
Re-aparting an ALREADY-decomposed sum -- which happens whenever an expansion result
flows back through an Apart call -- then grinds the heuristic GCD through
parameter-heavy giant-integer arithmetic: the 8-term decomposition of
``(c+d x)^7/(a+b x)^7`` took >240 s combined, while each addend alone takes
milliseconds. Partial-fraction decomposition is unique (polynomial part + proper
fractions over the denominator-power basis), so termwise application followed by
Add's like-term collection yields the same decomposition without ever combining.

The pathological case is guarded by a subprocess timeout: if someone reverts to
combined apart, the test FAILS in ~30 s instead of hanging the suite for minutes.
"""
import multiprocessing as mp

from sympy import Rational, Symbol, apart, simplify, together

from sympy_wolfram.functions_eager import eager_Apart

x, a, b, c, d = (Symbol(n) for n in 'xabcd')


def test_termwise_equals_combined_on_a_small_sum():
    """Uniqueness of the decomposition: termwise == combined for proper sums."""
    u = x/(x - 1) + 1/((x - 1)*(x + 1))
    assert simplify(eager_Apart(u, x) - apart(together(u), x)) == 0


def test_result_still_equals_the_input():
    u = (c + d*x)**3/(a + b*x)**3
    assert simplify(together(eager_Apart(u, x)) - u) == 0


def test_non_rational_addends_pass_through():
    from sympy import sin
    u = sin(x) + 1/(x - 1)
    r = eager_Apart(u, x)
    assert r.has(sin)


def _worker(q):
    monster = apart((c + d*x)**7/(a + b*x)**7, x)     # 8 terms, 0.1 s
    r = eager_Apart(monster, x)                        # must NOT recombine
    q.put(simplify(together(r) - together(monster)) == 0)


def test_re_aparting_a_decomposed_sum_is_fast_and_correct():
    """The regression case: apart of an already-decomposed parametric sum.

    Runs in a subprocess with a hard 60 s budget -- combined apart needs >240 s here,
    so a revert fails loudly instead of stalling the suite.
    """
    q = mp.Queue()
    p = mp.Process(target=_worker, args=(q,), daemon=True)
    p.start()
    p.join(60)
    if p.is_alive():
        p.kill()
        p.join()
        raise AssertionError('eager_Apart recombined the sum (killed at 60 s) -- '
                             'the termwise path is gone')
    assert q.get_nowait() is True
