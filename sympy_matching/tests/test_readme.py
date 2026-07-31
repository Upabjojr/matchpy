# -*- coding: utf-8 -*-
"""Execute every doctest in sympy_matching/README.md.

The README documents Mathematica's pattern semantics and how they are reproduced here.
Documentation that is not executed drifts silently from the code, and this particular
document describes behaviour where a divergence produces a WRONG ANTIDERIVATIVE rather
than an error -- so the examples are run as tests.
"""
import doctest
import pathlib
import warnings

README = pathlib.Path(__file__).resolve().parent.parent / 'README.md'


def test_readme_examples():
    warnings.filterwarnings('ignore')
    assert README.is_file(), f'missing {README}'
    result = doctest.testfile(
        str(README),
        module_relative=False,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
        verbose=False,
    )
    assert result.attempted > 0, 'no doctests were collected from the README'
    assert result.failed == 0, f'{result.failed} of {result.attempted} README examples failed'
