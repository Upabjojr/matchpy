# -*- coding: utf-8 -*-
"""Execute every doctest in sympy_matching's Markdown documentation (README + docs/).

Documentation that is not executed drifts silently from the code; these documents
describe behaviour where a divergence produces wrong results rather than errors, so
every example runs as a test.
"""
import doctest
import pathlib
import warnings

import pytest

PKG = pathlib.Path(__file__).resolve().parent.parent
DOCS = sorted([PKG / 'README.md'] + list((PKG / 'docs').glob('*.md')))


@pytest.mark.parametrize('doc', DOCS, ids=lambda p: p.name)
def test_doc_examples(doc):
    warnings.filterwarnings('ignore')
    result = doctest.testfile(
        str(doc),
        module_relative=False,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
        verbose=False,
    )
    assert result.attempted > 0, f'no doctests collected from {doc.name}'
    assert result.failed == 0, f'{result.failed} of {result.attempted} examples failed in {doc.name}'
