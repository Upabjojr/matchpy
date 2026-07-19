# -*- coding: utf-8 -*-
"""Backwards-compatibility shim.

All head registrations are now driven by the master SYMPY_NODES table in
operations.py and performed by conversion.py's `register_all_heads()` call.

This module remains only so that existing `from .registered_heads import ...`
statements continue to work.  New code should import from operations.py directly.
"""
from .operations import SYMPY_FUNC_TO_HEAD, HEAD_TO_SYMPY_FUNC, register_sympy_head
