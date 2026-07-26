# -*- coding: utf-8 -*-
"""SymPy-native wildcard symbols for MatchPy patterns.

`WildSymbol` behaves like a normal `sympy.Symbol` inside SymPy expression trees,
so patterns can be written naturally with SymPy syntax. During conversion via
`to_matchpy_expression`, it becomes the appropriate MatchPy wildcard.

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
    constraint variables such as `FreeOf('a', 'x')`.
"""
from sympy import Expr as SympyExpr
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
          ``Wildcard.optional('a', to_matchpy_expression(1))``
        * ``WildSymbol('a_', optional_value=IDENTITY_ELEMENT)`` converts to
          ``Wildcard.optional('a', to_matchpy_expression(<identity>))`` where
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


# ─── Wildcard function heads ──────────────────────────────────────────────────

class HeadRef(SympySymbol):
    """A matched function HEAD, wrapped so it is a substitutable SymPy object.

    A wildcard operation head (see :class:`WildHeadApp`) binds to a real function
    such as ``sin``. A function *class* is not a SymPy expression, so it cannot be
    substituted into a replacement template; this wraps it in a Symbol (named after
    the function) that carries the class, so a replacement can substitute it and
    re-apply it (see ``rubi_rules.utils.rubi_utils.WFApply``).
    """

    def __new__(cls, func, **assumptions):
        name = getattr(func, '__name__', None) or str(func)
        cls._sanitize(assumptions, cls)
        obj = SympySymbol.__xnew__(cls, name, **assumptions)
        object.__setattr__(obj, '_func_class', func)
        return obj

    @property
    def func_class(self):
        """The wrapped SymPy function (callable), e.g. ``sin``."""
        return self._func_class


class WildHeadApp(SympyExpr):
    """Pattern node: a wildcard function HEAD applied to arguments — ``F_[args]``.

    Converts to a MatchPy ``Operation`` whose head is a ``WildcardOperationHead``,
    so it matches an application of ANY function. The head is bound to the head
    wildcard's name, and the arguments are matched by MatchPy in the normal way —
    argument wildcards (and any constraints on them) therefore behave exactly as
    in an ordinary pattern.
    """

    def __new__(cls, head_wild, *args):
        return SympyExpr.__new__(cls, head_wild, *args)

    @property
    def head_wild(self):
        """The wildcard standing for the function head."""
        return self.args[0]

    @property
    def applied_args(self):
        """The arguments the wildcard head is applied to."""
        return self.args[1:]


class WildHeadDeriv(SympyExpr):
    """Pattern node: the n-th derivative of a WILDCARD function — ``Derivative[n_][f_][x_]``.

    Rubi's derivative rules are written over an unknown function: ``f^(n)(x)``.
    In SymPy that subject is ``Derivative(f(x), (x, n))``; this node is the
    corresponding PATTERN, with the function ``f`` and the order ``n`` both
    wildcards. It converts to the same MatchPy shape a real ``Derivative``
    converts to, except that the inner application carries a
    ``WildcardOperationHead`` so ANY function matches (see :class:`WildHeadApp`).

    A plain ``sympy.Derivative(...)`` cannot be used for this: its constructor
    validates and differentiates its arguments, which a wildcard function is not.
    """

    def __new__(cls, head_wild, var, order):
        return SympyExpr.__new__(cls, head_wild, var, order)

    @property
    def head_wild(self):
        """The wildcard standing for the differentiated function."""
        return self.args[0]

    @property
    def var(self):
        """The differentiation variable."""
        return self.args[1]

    @property
    def order(self):
        """The derivative order (typically a wildcard)."""
        return self.args[2]
