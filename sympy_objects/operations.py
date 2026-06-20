# -*- coding: utf-8 -*-
"""MatchPy OperationHead definitions for SymPy expression types.

Defines a master table (SYMPY_NODES) of all supported SymPy <-> MatchPy mappings.
A for-loop generates OperationHeads and registers bidirectional mappings.

Special heads (ADD, MUL, POW) with commutative/associative/one_identity
properties are defined explicitly; everything else is table-driven.

Usage:
    from sympy_objects.operations import ADD, MUL, POW, SIN, COS
    from sympy_objects.operations import SYMPY_FUNC_TO_HEAD, HEAD_TO_SYMPY_FUNC
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from matchpy.expressions.expressions import OperationHead, Arity

# ─── Mapping from SymPy function classes to OperationHeads ────────────────────
SYMPY_FUNC_TO_HEAD = {}
HEAD_TO_SYMPY_FUNC = {}


def register_sympy_head(sympy_class, head: OperationHead):
    """Register a bidirectional mapping between a SymPy class and an OperationHead."""
    SYMPY_FUNC_TO_HEAD[sympy_class] = head
    HEAD_TO_SYMPY_FUNC[head] = sympy_class


# ─── Special arithmetic operations (need explicit properties) ─────────────────

ADD = OperationHead(
    name='Add',
    arity=Arity.variadic,
    commutative=True,
    associative=True,
    one_identity=True,
)

MUL = OperationHead(
    name='Mul',
    arity=Arity.variadic,
    commutative=True,
    associative=True,
    one_identity=True,
)

POW = OperationHead(
    name='Pow',
    arity=Arity.variadic,  # variadic required so one_identity can collapse POW(x) -> x
    one_identity=True,     # MatchPy treats SymbolWrapper(x) as POW(x) during matching,
                           # enabling optional exponent wildcards to fire for bare bases.
)

EQUALITY = OperationHead(
    name='Eq',
    arity=Arity.binary,
)

# ─── Convenience aliases for commonly-used heads ─────────────────────────────
# These are created here so they can be imported before register_all_heads()
# is called.  register_all_heads() will reuse these exact objects.

SIN = OperationHead(name='sin', arity=Arity.unary)
COS = OperationHead(name='cos', arity=Arity.unary)
TAN = OperationHead(name='tan', arity=Arity.unary)
EXP = OperationHead(name='exp', arity=Arity.unary)
LOG = OperationHead(name='log', arity=Arity.variadic)

# Lookup for register_all_heads() to find pre-existing heads by name
_PREDEFINED_HEADS = {
    'sin': SIN, 'cos': COS, 'tan': TAN, 'exp': EXP, 'log': LOG,
}


# ─── Master table: (sympy_import_path, class_name, arity) ────────────────────
# This table drives all head creation and singledispatch registration.
# Arity is 'u' for unary, 'b' for binary, 'v' for variadic.

SYMPY_NODES = [
    # ── Trigonometric ─────────────────────────────────────────────────────────
    ('sympy.functions.elementary.trigonometric', 'sin', 'u'),
    ('sympy.functions.elementary.trigonometric', 'cos', 'u'),
    ('sympy.functions.elementary.trigonometric', 'tan', 'u'),
    ('sympy.functions.elementary.trigonometric', 'sec', 'u'),
    ('sympy.functions.elementary.trigonometric', 'csc', 'u'),
    ('sympy.functions.elementary.trigonometric', 'cot', 'u'),
    ('sympy.functions.elementary.trigonometric', 'sinc', 'u'),
    # ── Inverse trigonometric ─────────────────────────────────────────────────
    ('sympy.functions.elementary.trigonometric', 'asin', 'u'),
    ('sympy.functions.elementary.trigonometric', 'acos', 'u'),
    ('sympy.functions.elementary.trigonometric', 'atan', 'u'),
    ('sympy.functions.elementary.trigonometric', 'acot', 'u'),
    ('sympy.functions.elementary.trigonometric', 'asec', 'u'),
    ('sympy.functions.elementary.trigonometric', 'acsc', 'u'),
    ('sympy.functions.elementary.trigonometric', 'atan2', 'v'),
    # ── Hyperbolic ────────────────────────────────────────────────────────────
    ('sympy.functions.elementary.hyperbolic', 'sinh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'cosh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'tanh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'coth', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'sech', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'csch', 'u'),
    # ── Inverse hyperbolic ────────────────────────────────────────────────────
    ('sympy.functions.elementary.hyperbolic', 'asinh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'acosh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'atanh', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'acoth', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'asech', 'u'),
    ('sympy.functions.elementary.hyperbolic', 'acsch', 'u'),
    # ── Exponential / logarithmic ─────────────────────────────────────────────
    ('sympy.functions.elementary.exponential', 'exp', 'u'),
    ('sympy.functions.elementary.exponential', 'log', 'v'),  # log(x) or log(x, base)
    ('sympy.functions.elementary.exponential', 'LambertW', 'v'),
    # ── Complex ───────────────────────────────────────────────────────────────
    ('sympy.functions.elementary.complexes', 'Abs', 'u'),
    ('sympy.functions.elementary.complexes', 'sign', 'u'),
    ('sympy.functions.elementary.complexes', 'im', 'u'),
    ('sympy.functions.elementary.complexes', 're', 'u'),
    ('sympy.functions.elementary.complexes', 'conjugate', 'u'),
    ('sympy.functions.elementary.complexes', 'arg', 'u'),
    # ── Miscellaneous elementary ──────────────────────────────────────────────
    ('sympy.functions.elementary.miscellaneous', 'Max', 'v'),
    ('sympy.functions.elementary.miscellaneous', 'Min', 'v'),
    # ── Integer functions ─────────────────────────────────────────────────────
    ('sympy.functions.elementary.integers', 'floor', 'u'),
    ('sympy.functions.elementary.integers', 'ceiling', 'u'),
    ('sympy.functions.elementary.integers', 'frac', 'u'),
    # ── Piecewise ─────────────────────────────────────────────────────────────
    ('sympy.functions.elementary.piecewise', 'Piecewise', 'v'),
    # ── Combinatorial ─────────────────────────────────────────────────────────
    ('sympy.functions.combinatorial.factorials', 'factorial', 'u'),
    ('sympy.functions.combinatorial.factorials', 'factorial2', 'u'),
    ('sympy.functions.combinatorial.factorials', 'binomial', 'b'),
    ('sympy.functions.combinatorial.factorials', 'RisingFactorial', 'b'),
    ('sympy.functions.combinatorial.factorials', 'FallingFactorial', 'b'),
    ('sympy.functions.combinatorial.numbers', 'fibonacci', 'u'),
    ('sympy.functions.combinatorial.numbers', 'lucas', 'u'),
    ('sympy.functions.combinatorial.numbers', 'bernoulli', 'v'),
    ('sympy.functions.combinatorial.numbers', 'bell', 'v'),
    ('sympy.functions.combinatorial.numbers', 'catalan', 'u'),
    # ── Error functions ───────────────────────────────────────────────────────
    ('sympy.functions.special.error_functions', 'erf', 'u'),
    ('sympy.functions.special.error_functions', 'erfc', 'u'),
    ('sympy.functions.special.error_functions', 'erfi', 'u'),
    ('sympy.functions.special.error_functions', 'erf2', 'b'),
    ('sympy.functions.special.error_functions', 'Ei', 'u'),
    ('sympy.functions.special.error_functions', 'expint', 'v'),
    ('sympy.functions.special.error_functions', 'li', 'u'),
    ('sympy.functions.special.error_functions', 'Li', 'u'),
    ('sympy.functions.special.error_functions', 'Si', 'u'),
    ('sympy.functions.special.error_functions', 'Ci', 'u'),
    ('sympy.functions.special.error_functions', 'Shi', 'u'),
    ('sympy.functions.special.error_functions', 'Chi', 'u'),
    ('sympy.functions.special.error_functions', 'fresnelc', 'u'),
    ('sympy.functions.special.error_functions', 'fresnels', 'u'),
    # ── Gamma and related ─────────────────────────────────────────────────────
    ('sympy.functions.special.gamma_functions', 'gamma', 'u'),
    ('sympy.functions.special.gamma_functions', 'loggamma', 'u'),
    ('sympy.functions.special.gamma_functions', 'digamma', 'u'),
    ('sympy.functions.special.gamma_functions', 'trigamma', 'u'),
    ('sympy.functions.special.gamma_functions', 'polygamma', 'v'),
    ('sympy.functions.special.gamma_functions', 'uppergamma', 'b'),
    ('sympy.functions.special.gamma_functions', 'lowergamma', 'b'),
    # ── Beta function ─────────────────────────────────────────────────────────
    ('sympy.functions.special.beta_functions', 'beta', 'v'),
    # ── Hypergeometric ────────────────────────────────────────────────────────
    ('sympy.functions.special.hyper', 'hyper', 'v'),
    ('sympy.functions.special.hyper', 'meijerg', 'v'),
    ('sympy.functions.special.hyper', 'appellf1', 'v'),
    # ── Zeta and polylog ──────────────────────────────────────────────────────
    ('sympy.functions.special.zeta_functions', 'zeta', 'v'),
    ('sympy.functions.special.zeta_functions', 'polylog', 'v'),
    ('sympy.functions.special.zeta_functions', 'lerchphi', 'v'),
    # ── Elliptic integrals ────────────────────────────────────────────────────
    ('sympy.functions.special.elliptic_integrals', 'elliptic_f', 'b'),
    ('sympy.functions.special.elliptic_integrals', 'elliptic_e', 'v'),
    ('sympy.functions.special.elliptic_integrals', 'elliptic_pi', 'v'),
    ('sympy.functions.special.elliptic_integrals', 'elliptic_k', 'u'),
    # ── Bessel functions ──────────────────────────────────────────────────────
    ('sympy.functions.special.bessel', 'besselj', 'b'),
    ('sympy.functions.special.bessel', 'bessely', 'b'),
    ('sympy.functions.special.bessel', 'besseli', 'b'),
    ('sympy.functions.special.bessel', 'besselk', 'b'),
    ('sympy.functions.special.bessel', 'hankel1', 'b'),
    ('sympy.functions.special.bessel', 'hankel2', 'b'),
    ('sympy.functions.special.bessel', 'jn', 'b'),
    ('sympy.functions.special.bessel', 'yn', 'b'),
    ('sympy.functions.special.bessel', 'airyai', 'u'),
    ('sympy.functions.special.bessel', 'airybi', 'u'),
    ('sympy.functions.special.bessel', 'airyaiprime', 'u'),
    ('sympy.functions.special.bessel', 'airybiprime', 'u'),
    # ── Delta / Heaviside ─────────────────────────────────────────────────────
    ('sympy.functions.special.delta_functions', 'DiracDelta', 'v'),
    ('sympy.functions.special.delta_functions', 'Heaviside', 'v'),
    # ── Tensor / signature ────────────────────────────────────────────────────
    ('sympy.functions.special.tensor_functions', 'KroneckerDelta', 'v'),
    # ── Polynomials (special) ─────────────────────────────────────────────────
    ('sympy.functions.special.polynomials', 'legendre', 'b'),
    ('sympy.functions.special.polynomials', 'chebyshevt', 'b'),
    ('sympy.functions.special.polynomials', 'chebyshevu', 'b'),
    ('sympy.functions.special.polynomials', 'hermite', 'b'),
    ('sympy.functions.special.polynomials', 'laguerre', 'b'),
]
"""Master table of SymPy function -> MatchPy head registrations.

Each entry is (module_path, class_name, arity_code) where arity_code is:
  'u' = unary, 'b' = binary, 'v' = variadic.
"""

_ARITY_MAP = {'u': Arity.unary, 'b': Arity.binary, 'v': Arity.variadic}


def _resolve_sympy_class(module_path: str, class_name: str):
    """Import and return a SymPy class by its dotted module path and name."""
    import importlib
    mod = importlib.import_module(module_path)
    return getattr(mod, class_name)


def register_all_heads():
    """Create OperationHeads for all entries in SYMPY_NODES and register them.

    Also registers the special heads (ADD, MUL, POW, EQUALITY) with their
    corresponding SymPy classes.

    Pre-defined heads (SIN, COS, TAN, EXP, LOG) are reused by name so that
    imports of these constants get the same objects stored in the registry.
    """
    import sympy

    # Register special heads first
    register_sympy_head(sympy.Add, ADD)
    register_sympy_head(sympy.Mul, MUL)
    register_sympy_head(sympy.Pow, POW)
    register_sympy_head(sympy.Eq, EQUALITY)

    # Register all table-driven heads
    for module_path, class_name, arity_code in SYMPY_NODES:
        try:
            sympy_cls = _resolve_sympy_class(module_path, class_name)
        except (ImportError, AttributeError):
            # Skip classes not available in this SymPy version
            continue
        if sympy_cls in SYMPY_FUNC_TO_HEAD:
            continue  # already registered (e.g. by a special head)
        # Reuse pre-defined head if it exists, otherwise create a new one
        if class_name in _PREDEFINED_HEADS:
            head = _PREDEFINED_HEADS[class_name]
        else:
            arity = _ARITY_MAP[arity_code]
            head = OperationHead(name=class_name, arity=arity)
        register_sympy_head(sympy_cls, head)
