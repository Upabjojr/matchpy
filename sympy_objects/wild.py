# -*- coding: utf-8 -*-
"""SymPy-native wildcard symbols for MatchPy patterns.

`WildSymbol` behaves like a normal `sympy.Symbol` inside SymPy expression trees,
so patterns can be written naturally with SymPy syntax. During conversion via
`to_expression`, it becomes the appropriate MatchPy wildcard.

Examples:
    a_ = WildSymbol('a_')
    b_ = WildSymbol('b_', optional_value=0)
    c_ = WildSymbol('c_', optional_value=IDENTITY_ELEMENT)
    x = Symbol('x')

    # IDENTITY_ELEMENT resolves to the identity of the parent operation:
    # 0 for Add, 1 for Mul.  So c_ in `c_ + x` defaults to 0, while
    # c_ in `c_ * x` defaults to 1.

Naming convention:
    If the SymPy symbol name ends with a trailing underscore, that underscore is
    stripped when deriving the MatchPy variable name. For example,
    `WildSymbol('a_')` becomes a wildcard with MatchPy variable name `'a'`.
    This makes SymPy-side names like `a_`, `b_`, `c_` line up with MatchPy
    constraint variables such as `FreeQ('a', 'x')`.
"""
from sympy import Symbol as SympySymbol


# ─── Sentinel for context-dependent identity defaults ─────────────────────────

class _IdentityElementType:
    """Sentinel indicating the optional default equals the parent operation's identity.

    Use the module-level singleton ``IDENTITY_ELEMENT`` — do not instantiate directly.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'IDENTITY_ELEMENT'

    def __bool__(self):
        # Ensure truthiness so `is_optional` stays True
        return True


IDENTITY_ELEMENT = _IdentityElementType()
"""Sentinel: when used as ``optional_value``, the default is resolved at
conversion time to the identity element of the enclosing SymPy operation
(0 for Add, 1 for Mul)."""


# ─── WildSymbol ───────────────────────────────────────────────────────────────

class WildSymbol(SympySymbol):
    """A SymPy symbol that converts to a MatchPy wildcard.

    Parameters:
        name: SymPy-side symbol name. A trailing underscore is allowed and is
            stripped from the MatchPy variable name.
        optional_value: When not None, conversion uses MatchPy's optional
            wildcard semantics with this default value.  May be
            ``IDENTITY_ELEMENT`` for context-dependent defaults.

    Notes:
        * ``WildSymbol('a_')`` converts to ``Wildcard.dot('a')``
        * ``WildSymbol('a_', optional_value=1)`` converts to
          ``Wildcard.optional('a', to_expression(1))``
        * ``WildSymbol('a_', optional_value=IDENTITY_ELEMENT)`` converts to
          ``Wildcard.optional('a', to_expression(<identity>))`` where
          ``<identity>`` is determined by the enclosing operation (0 for Add,
          1 for Mul).
    """

    _wild_count = 0

    def __new__(cls, name, optional_value=None, **assumptions):
        cls._wild_count += 1
        cls._sanitize(assumptions, cls)
        obj = SympySymbol.__xnew__(cls, name, **assumptions)
        wildcard_name = name[:-1] if isinstance(name, str) and name.endswith('_') else name
        if not wildcard_name:
            raise ValueError('WildSymbol name must not be empty after stripping a trailing underscore.')
        object.__setattr__(obj, '_wildcard_name', wildcard_name)
        object.__setattr__(obj, '_optional_value', optional_value)
        object.__setattr__(obj, '_wild_index', cls._wild_count)
        return obj

    def _hashable_content(self):
        return super()._hashable_content() + (self._wild_index,)

    @property
    def wildcard_name(self):
        """MatchPy variable name derived from the SymPy symbol name."""
        return self._wildcard_name

    @property
    def optional_value(self):
        """Optional default value used when converting to MatchPy."""
        return self._optional_value

    @property
    def is_optional(self):
        """Whether this symbol should convert to a MatchPy optional wildcard."""
        return self._optional_value is not None
