# -*- coding: utf-8 -*-
"""Fixtures for running sympy_matching tests in multiple matching modes.

Modes:
  - one-to-one: omnimatch.matching.one_to_one.match
  - many-to-one: ManyToOneMatcher
  - generated: CodeGenerator-produced code
  - json-roundtrip: ManyToOneMatcher serialized/deserialized via JSON
"""
import sys
import os
from types import ModuleType

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from omnimatch.expressions.expressions import Wildcard, Operation
from omnimatch.matching.one_to_one import match as match_one_to_one
from omnimatch.matching.many_to_one import ManyToOneMatcher
from omnimatch.matching.code_generation import CodeGenerator
from omnimatch.matching.json_serialization import to_json, from_json
from omnimatch.expressions.functions import preorder_iter

import sympy_matching  # ensure json_ext is registered


def pytest_generate_tests(metafunc):
    if 'match' in metafunc.fixturenames:
        metafunc.parametrize('match', ['one-to-one', 'many-to-one', 'generated', 'json-roundtrip'], indirect=True)
    if 'match_many' in metafunc.fixturenames:
        metafunc.parametrize('match_many', ['many-to-one', 'generated', 'json-roundtrip'], indirect=True)


def _xfail_fixed_wc_commutative(patterns):
    """xfail if pattern has fixed wildcards with length > 1 in commutative ops."""
    try:
        pattern = patterns[0]
        commutative = next(
            p for p in preorder_iter(pattern.expression)
            if isinstance(p, Operation) and p.head.commutative
        )
        next(wc for wc in preorder_iter(commutative)
             if isinstance(wc, Wildcard) and wc.min_count > 1)
    except StopIteration:
        pass
    else:
        pytest.xfail('Matcher does not support fixed wildcards with length != 1 in commutative operations')


def match_many_to_one(expression, *patterns):
    _xfail_fixed_wc_commutative(patterns)
    matcher = ManyToOneMatcher(*patterns)
    for _, substitution in matcher.match(expression):
        yield substitution


GENERATED_TEMPLATE = """
# -*- coding: utf-8 -*-
from omnimatch import *
from omnimatch.expressions.expressions import OperationHead, Arity, SymbolWrapper
from omnimatch.expressions.expressions import Operation
from collections import deque

{global_code}

{code}
""".strip()


def match_generated(expression, *patterns):
    matcher = ManyToOneMatcher(*patterns)
    generator = CodeGenerator(matcher)
    gc, code = generator.generate_code()
    full_code = GENERATED_TEMPLATE.format(global_code=gc, code=code)
    compiled = compile(full_code, '', 'exec')
    module = ModuleType("generated_code")
    module.__dict__.update(generator.constraint_objects)
    exec(compiled, module.__dict__)
    for _, substitution in module.match_root(expression):
        yield substitution


def match_json_roundtrip(expression, *patterns):
    _xfail_fixed_wc_commutative(patterns)
    matcher = ManyToOneMatcher(*patterns)
    original_patterns = matcher.patterns[:]
    original_constraints = matcher.constraints[:]
    original_constraint_vars = dict(matcher.constraint_vars)
    json_str = to_json(matcher)
    matcher2 = from_json(json_str)
    # Restore constraint objects (CustomConstraint has non-serializable callables)
    matcher2.patterns = original_patterns
    matcher2.constraints = original_constraints
    matcher2.constraint_vars = original_constraint_vars
    for _, substitution in matcher2.match(expression):
        yield substitution


@pytest.fixture
def match(request):
    if request.param == 'one-to-one':
        return match_one_to_one
    elif request.param == 'many-to-one':
        return match_many_to_one
    elif request.param == 'generated':
        return match_generated
    elif request.param == 'json-roundtrip':
        return match_json_roundtrip
    else:
        raise ValueError(f"Invalid match mode: {request.param}")


@pytest.fixture
def match_many(request):
    if request.param == 'many-to-one':
        return match_many_to_one
    elif request.param == 'generated':
        return match_generated
    elif request.param == 'json-roundtrip':
        return match_json_roundtrip
    else:
        raise ValueError(f"Invalid match mode: {request.param}")
