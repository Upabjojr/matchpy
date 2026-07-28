# -*- coding: utf-8 -*-
"""Self-contained EAGER Wolfram-standard helpers (plain functions).

These are the eager implementations of a few Mathematica standard-library
functions whose logic depends *solely* on SymPy.  They used to live in
``rubi_rules.utils.utility_functions``; they are not Rubi-specific, so they live
here and ``utility_functions`` imports them back (the correct layer direction:
rubi_rules -> sympy_wolfram).

Deferred (``MathematicaExpr``) counterpart classes keep the bare Mathematica name
(``LeafCount``, ``Part``, …) and live in ``sympy_wolfram.mathematica_functions``;
the eager functions here carry the ``eager_`` prefix (``eager_LeafCount``, …) and
the deferred classes delegate to them.

Only functions with a purely-SymPy body belong here.  ``First``/``Rest``/
``Numerator``/``Denominator``/``Part``/``Apart``/``Simplify`` used to *look* Rubi-coupled
because their Rubi bodies called ``SumQ``/``ProductQ``/``Sort``/``RationalFunctionQ``/
``Util_Part`` -- but every one of those is itself a generic Wolfram/SymPy operation
(``is_Add``/``is_Mul``/sort-by-``sort_key``/``is_rational_function``/part-extraction),
so the coupling was spurious.  They are inlined below and the functions live here.
"""
import functools as _functools

import sympy
from sympy import (
    Add, Basic, Float, I, Integer, Mul, Pow, Rational, S, Symbol, Tuple,
    expand, oo, postorder_traversal, sympify, together, zoo,
)
from sympy.core.numbers import Exp1
from sympy.core.function import Function
from sympy.polys.partfrac import apart
from sympy.simplify.simplify import fraction, simplify
from sympy.polys.polytools import Poly, quo, rem, invert, cancel, degree, discriminant
from sympy.core.exprtools import factor_terms as _sympy_factor_terms
from sympy.polys.polyerrors import (
    PolynomialError, PolynomialDivisionFailed, UnificationFailed, NotInvertible,
    BasePolynomialError,
)

# MatchPy is a lower layer, so these are safe module-level imports; they back the
# matchpy->sympy coercion used by FreeQ (see _ensure_sympy).
from matchpy.expressions.expressions import Operation as _MatchPyOperation
from matchpy.expressions.expressions import SymbolWrapper as _MatchPySymbolWrapper


def _ensure_sympy(expr):
    """Coerce a MatchPy expression to SymPy if needed; SymPy objects pass through.

    A ``SymbolWrapper`` unwraps to the SymPy value it carries; a MatchPy ``Operation``
    is converted structurally via ``sympy_matching``. This is the bridge that lets the
    Wolfram-standard predicates below accept either a match-bound MatchPy value or a
    plain SymPy expression.
    """
    if isinstance(expr, _MatchPySymbolWrapper):
        return expr.value
    if isinstance(expr, _MatchPyOperation):
        from sympy_matching.conversion import matchpy_to_sympy   # lazy: avoids any load-order edge
        return matchpy_to_sympy(expr)
    return expr


def eager_FreeQ(nodes, var):
    """Mathematica ``FreeQ[expr, form]`` -- True iff ``form`` (``var``) occurs nowhere
    in ``expr``. A list/tuple of ``nodes`` is free iff *every* element is.

    This is a standard Wolfram-library predicate (not Rubi-specific): its body is
    ``expr.has(var)`` over SymPy, with the matchpy->sympy coercion handled by
    :func:`_ensure_sympy`. The ``FreeQ`` *constraint* class in
    ``sympy_wolfram.constraints_wolfram`` (re-exported by
    ``rubi_rules.utils.constraints_wolfram``) delegates here.
    """
    var = _ensure_sympy(var)
    if isinstance(nodes, (tuple, list)):
        return not any(S(_ensure_sympy(expr)).has(var) for expr in nodes)
    nodes = S(_ensure_sympy(nodes))
    return not nodes.has(var)


def head_to_class(obj):
    """Resolve a function HEAD to its SymPy class, or ``None`` if not resolvable.

    A function-head wildcard ``F_[...]`` binds its head to a
    :class:`~sympy_matching.wild.HeadRef` (a ``Symbol`` subclass carrying the SymPy
    class as ``.func_class``); a head-membership/identity test compares it against a
    list of function *classes* (either literal ``HeadRef``s the codegen emits, or bare
    classes like ``sin`` used inside ``TrigQ``/``HyperbolicQ``). This unwraps both to
    the underlying class so they compare, e.g. ``MemberQ[{asin, acos}, F]`` fires when
    ``F`` bound to ``asin``.

    Mathematica→SymPy *name* translation is done upstream by the code generator (it
    emits ``HeadRef(sympy.asin)`` for ``ArcSin``), so no name table is needed here.
    """
    fc = getattr(obj, 'func_class', None)     # HeadRef -> the class it wraps
    if fc is not None:
        return fc
    if isinstance(obj, type):                 # a bare SymPy function class
        return obj
    return None


def eager_LeafCount(expr):
    """Mathematica LeafCount[expr] — number of nodes in the expression tree."""
    return len(list(postorder_traversal(expr)))


def _term_exponent(term, form):
    """Power of ``form`` in a single multiplicative ``term`` (form itself -> 1,
    ``form**e`` -> e, any other factor -> 0, even one that merely contains ``form``
    like ``sin(form)`` -- exactly as Mathematica treats it)."""
    e = S.Zero
    for f in Mul.make_args(term):
        if f == form:
            e += 1
        elif f.is_Pow and f.base == form:
            e += f.exp
    return e


def _exponent_multiset(expr, form):
    """Exponents of ``form`` in ``expr`` viewed as a rational function.

    Matches Mathematica's ``Exponent``: writing ``expr = num/den`` (via
    ``Together``), the exponent set is ``{e - deg(den) : e over terms of num}``,
    i.e. every numerator-term exponent shifted down by the denominator's degree.
    So ``Exponent[x/(a+b x)^2, x] = 1 - 2 = -1`` and ``Exponent[Sqrt[x]+x, x] = 1``
    -- NOT restricted to polynomials the way a ``PolynomialQ`` guard would be.
    """
    num, den = fraction(together(sympify(expr)))
    ne = [_term_exponent(t, form) for t in Add.make_args(expand(num))]
    de = [_term_exponent(t, form) for t in Add.make_args(expand(den))]
    shift = max(de) if de else S.Zero
    return [e - shift for e in ne] or [S.Zero]


def eager_Exponent(expr, form, h=None):
    """Mathematica ``Exponent[expr, form]`` / ``Exponent[expr, form, h]``.

    Returns the maximum (default) or minimum (``h`` = ``Min``) power of ``form``
    in ``expr``, treating ``expr`` as a rational function -- so it is correct for
    non-polynomials (``Sqrt[x]+x -> 1``, ``1/x+x -> 1``, ``Sin[x] x^2 -> 2``),
    unlike a polynomial-only implementation which wrongly returns 0 for those.

    This is what Rubi's ``Expon[u, x] := Exponent[Together[u], x]`` needs; the
    ``Together`` is already folded in here.
    """
    exps = _exponent_multiset(expr, form)
    is_min = h is not None and (getattr(h, 'name', None) == 'Min' or str(h) == 'Min')
    try:
        return min(exps) if is_min else max(exps)
    except TypeError:
        # Non-comparable (symbolic) exponents -- fall back to 0 rather than crash.
        return S.Zero


def eager_Length(expr):
    """Mathematica Length[expr] — number of elements."""
    if isinstance(expr, (tuple, list, sympy.Tuple)):
        return len(expr)
    return len(expr.args)


def eager_Complex(a, b):
    """Mathematica Complex[re, im] — construct a complex number a + I*b."""
    return a + I * b


def _sort(args):
    """Wolfram ``Sort`` for an argument sequence — canonical ``sort_key`` order."""
    return sorted(args, key=lambda t: t.sort_key())


def _eager_simplify_impl(expr):
    from sympy_wolfram.objects import MathematicaExpr
    if isinstance(expr, Basic) and expr.has(MathematicaExpr):
        try:
            expr = expr.doit()
        except (AttributeError, TypeError):
            return expr
    # RATIONAL fast path: for a pure rational function, ``cancel`` already yields
    # the canonical p/q normal form that Simplify is used for downstream (ZeroQ /
    # FreeQ / sign guards). Full sympy.simplify additionally runs trig/radical/
    # power passes that cannot fire here, yet cost seconds each on the large
    # many-symbol coefficients partial-fraction expansion produces (profiled: 30
    # Simplify calls = 50s inside one ExpandIntegrand). ``factor_terms`` is kept
    # when it shrinks the result, mirroring simplify's shortest-form preference.
    if isinstance(expr, Basic) and expr.free_symbols:
        try:
            if expr.is_rational_function(*expr.free_symbols):
                res = cancel(expr)
                try:
                    ft = _sympy_factor_terms(res)
                    if ft.count_ops() <= res.count_ops():
                        res = ft
                except (AttributeError, TypeError, PolynomialError):
                    pass
                # Like Mathematica's Simplify, never return a LARGER form than the
                # input: cancel expands products of sums ((x^2+3)^2 -> quartic),
                # which is only an improvement when it actually shrinks the tree
                # (or reveals a cancellation).
                if res.count_ops() <= expr.count_ops():
                    return res
                return expr
        except (AttributeError, TypeError, PolynomialError):
            pass
    try:
        return simplify(expr)
    except (AttributeError, TypeError):
        return expr
    except RecursionError:
        # Defensive backstop: sympy.simplify can still recurse past the interpreter
        # limit on a pathological input. simplify is only a NORMALISATION here (PosQ/
        # TogetherSimplify/ExpandLinearProduct), so fall back to the unsimplified input
        # -- correct, just less tidy -- rather than crash the integrator. (The main
        # offender, fractional-bound Sum nodes, is fixed at source in SumWolfram.)
        return expr


_eager_simplify_cached = _functools.lru_cache(maxsize=50000)(_eager_simplify_impl)


def eager_Simplify(expr):
    """Mathematica ``Simplify[expr]`` (eager).

    First resolves any unevaluated deferred ``MathematicaExpr`` nodes (a product of
    such nodes drives ``sympy.simplify``'s nc_simplify into unbounded recursion), then
    delegates to ``sympy.simplify``.  A ``Boolean`` (e.g. a ``BinomialDegree`` returning
    ``False`` on a non-binomial) sitting inside an arithmetic node has no numeric value,
    so we return the expression unevaluated rather than crash.

    MEMOISED (bounded): Simplify is a pure function of its argument, and rule-guard
    evaluation during the integration DFS calls it on the SAME expressions thousands of
    times -- profiling a slow trig/sqrt integral showed ~9.6k simplify calls consuming
    over half the runtime. The cache falls back to a direct call on unhashable input.
    """
    try:
        return _eager_simplify_cached(expr)
    except TypeError:          # unhashable argument -> compute directly
        return _eager_simplify_impl(expr)


def eager_First(expr, d=None):
    """Mathematica ``First[expr]`` — first element (``d`` unused, kept for arity)."""
    if isinstance(expr, (tuple, list, Tuple)):
        return expr[0]
    if isinstance(expr, Symbol):
        return expr
    if expr.is_Add or expr.is_Mul:
        return _sort(expr.args)[0]
    return expr.args[0]


def eager_Rest(expr):
    """Mathematica ``Rest[expr]`` — all elements but the first."""
    if isinstance(expr, (tuple, list, Tuple)):
        return expr[1:]
    if expr.is_Add or expr.is_Mul:
        return expr.func(*_sort(expr.args)[1:])
    # Generic head: Mathematica Rest[f[a, b, ...]] = f[b, ...]. The old
    # `expr.args[1]` was only correct for 2-argument heads (where the rebuilt
    # one-arg node auto-evaluates, e.g. Rest[b^-1] -> -1) and silently DROPPED
    # the tail for 3+-argument heads (hyper, Subst, Int, ...).
    rest = expr.args[1:]
    if len(rest) == 1:
        return rest[0]
    try:
        return expr.func(*rest)
    except (TypeError, ValueError):
        return rest


def eager_Numerator(u):
    """Mathematica ``Numerator[expr]`` — numerator, recursing through integer powers."""
    u = eager_Simplify(u)
    if isinstance(u, Pow) and isinstance(u.exp, Integer):
        if u.exp > 0:
            return Pow(eager_Numerator(u.base), u.exp)
        if u.exp < 0:
            return Pow(eager_Denominator(u.base), -1 * u.exp)
    elif isinstance(u, Add):
        u = together(u)
    return fraction(u)[0]


def eager_Denominator(var):
    """Mathematica ``Denominator[expr]`` — denominator, recursing through integer powers."""
    var = eager_Simplify(var)
    if isinstance(var, Pow) and isinstance(var.exp, Integer):
        if var.exp > 0:
            return Pow(eager_Denominator(var.base), var.exp)
        if var.exp < 0:
            return Pow(eager_Numerator(var.base), -1 * var.exp)
    elif isinstance(var, Add):
        var = together(var)
    return fraction(var)[1]


class Util_Part(Function):
    """Helper for :func:`eager_Part` — deferred until its index simplifies to an integer."""

    def doit(self):
        i = eager_Simplify(self.args[0])
        if len(self.args) > 2:
            lst = list(self.args[1:])
        else:
            lst = self.args[1]
        if isinstance(i, (int, Integer)):
            # An out-of-range index (or a Part of something with no such part) stays
            # UNEVALUATED, as in Mathematica, where `False[[3]]` merely warns and
            # returns unevaluated. Rubi leans on that: guards like
            # `EqQ[FunctionOfSquareRootOfQuadratic[u,x][[3]], 2]` are evaluated for
            # every integrand, and the helper returns False for most of them -- the
            # part access is then meaningless and the guard must simply fail, not
            # raise. Propagating IndexError instead aborted the whole match.
            try:
                if isinstance(lst, (tuple, list)):
                    return lst[i - 1]
                if getattr(lst, 'is_Atom', False):
                    return lst
                return lst.args[i - 1]
            except (IndexError, TypeError, AttributeError):
                return self
        return self


def eager_Part(lst, i):
    """Mathematica ``Part[expr, i]`` — 1-based part extraction (``i = -1`` = last)."""
    if isinstance(lst, (tuple, list)):
        return Util_Part(i, *lst).doit()
    return Util_Part(i, lst).doit()


def eager_ProductLog(*args):
    """Mathematica ``ProductLog[z]`` / ``ProductLog[k, z]`` — the Lambert W function.

    THE ARGUMENT ORDER IS REVERSED between the two systems: Mathematica takes the
    branch index FIRST (``ProductLog[k, z]``), SymPy takes it LAST (``LambertW(z, k)``).
    Verified on 12.2: ``N[ProductLog[-1, -0.1]] == -3.577152063957297``.

    Stays symbolic for symbolic input, as Mathematica does (``ProductLog[1]`` is not
    evaluated); the previous implementation called ``.evalf()`` unconditionally.
    """
    args = [sympify(a) for a in args]
    if len(args) == 2:
        k, z = args
        return sympy.LambertW(z, k)
    return sympy.LambertW(args[0])


def eager_Identity(z):
    """Mathematica ``Identity[z]`` — returns its argument unchanged.

    Rubi uses it to keep a coefficient from being folded away too early, as in
    ``Int[-u_, x] := Identity[-1]*Int[u, x]`` (9.1 Integrand simplification rules).
    """
    return sympify(z)


def eager_ExpIntegralEi(z):
    """Mathematica ``ExpIntegralEi[z]`` — the exponential integral Ei(z)."""
    return sympy.Ei(sympify(z))


def eager_LogIntegral(z):
    """Mathematica ``LogIntegral[z]`` — the logarithmic integral li(z).

    ``LogIntegral[1] == -Infinity`` in Mathematica; SymPy's ``li(1)`` agrees.
    """
    return sympy.li(sympify(z))


def eager_Factorial(z):
    """Mathematica ``Factorial[z]`` (``z!``).

    SymPy's ``factorial`` leaves a non-integer argument unevaluated, where Mathematica
    reduces it via the Gamma function (``Factorial[1/2] == Sqrt[Pi]/2``, verified on
    12.2). Route explicit non-integers through ``gamma(z+1)``; a symbolic argument
    stays ``factorial(z)``, which is Mathematica's ``z!``.
    """
    z = sympify(z)
    if z.is_number and not (z.is_integer and z.is_nonnegative):
        return sympy.gamma(z + 1)
    return sympy.factorial(z)


def eager_Zeta(*args):
    """Mathematica ``Zeta[s]`` / ``Zeta[s, a]`` (Riemann / Hurwitz zeta)."""
    return sympy.zeta(*[sympify(a) for a in args])


def eager_PolyGamma(*args):
    """Mathematica ``PolyGamma[z]`` / ``PolyGamma[n, z]``.

    The one-argument form is Mathematica's digamma, i.e. exactly ``PolyGamma[0, z]``.
    """
    args = [sympify(a) for a in args]
    if len(args) == 1:
        return sympy.polygamma(S.Zero, args[0])
    return sympy.polygamma(*args)


def eager_BesselJ(n, z):
    """Mathematica ``BesselJ[n, z]`` — Bessel function of the first kind."""
    return sympy.besselj(sympify(n), sympify(z))


def eager_ExpIntegralE(n, z):
    """Mathematica ``ExpIntegralE[n, z]`` — the exponential integral E_n(z).

    Kept SYMBOLIC unless an argument is inexact, mirroring Mathematica: it returns
    ``ExpIntegralE[2, 3/2]`` unevaluated but ``ExpIntegralE[2, 1.5]`` numerically. The
    previous implementation called ``.evalf()`` unconditionally, which both forced
    machine precision on exact input and cost a last-digit disagreement with MMA.
    """
    n, z = sympify(n), sympify(z)
    result = sympy.expint(n, z)
    if any(a.is_Float for a in (n, z)):
        return result.evalf()
    return result


def eager_Root(poly, k):
    """Mathematica ``Root[poly, k]`` — the k-th root of *poly*, indexed from 1.

    Mathematica orders the roots real-first-ascending, then the complex ones; SymPy's
    ``CRootOf`` uses the SAME order but indexes from 0, so the only translation needed
    is ``k-1``. Verified against Mathematica 12.2 on ``x^3-x-1``, ``x^4-1`` and
    ``x^2+1`` (all roots, in order).

    Mathematica displays a root in radicals when it can (``Root[x^2-2,1]`` prints as
    ``-Sqrt[2]``); we return the ``CRootOf``, which is the same number and stays exact.
    """
    poly = sympify(poly)
    k = sympify(k)
    if not k.is_Integer:
        return None
    gens = sorted(poly.free_symbols, key=str)
    try:
        return sympy.CRootOf(poly, int(k) - 1)
    except (BasePolynomialError, IndexError, ValueError, NotImplementedError):
        pass
    # A polynomial with symbolic coefficients has no CRootOf; solve for the variable
    # and index into the result, which is what Rubi's uses of Root actually need.
    if len(gens) == 1:
        try:
            roots = sympy.solve(sympy.Eq(poly, 0), gens[0])
            if roots and 1 <= int(k) <= len(roots):
                return roots[int(k) - 1]
        except (NotImplementedError, ValueError, TypeError):
            pass
    return None


def eager_Discriminant(p, x):
    """Mathematica ``Discriminant[poly, x]`` — the discriminant of *poly* in *x*.

    Matches Mathematica on the degenerate cases, which SymPy's ``discriminant`` does
    NOT (all verified against Mathematica 12.2):

    * degree 0 (constant in *x*) -> ``p**-2``; SymPy returns 0.
      ``Discriminant[5, x] == 1/25``, ``Discriminant[c, x] == c^-2``,
      ``Discriminant[a+b, x] == (a+b)^-2``.
    * the zero polynomial -> ``0``.
    * not a polynomial in *x* (``Sin[x]``) -> unevaluated. Mathematica emits
      ``Discriminant::poly2`` and returns the expression unchanged; returning None
      here leaves the deferred node in place, which is the same thing.
    """
    p = sympify(p)
    x = sympify(x)
    try:
        poly = Poly(p, x)
    except BasePolynomialError:      # PolynomialError / GeneratorsNeeded / ...
        return None
    if poly.is_zero:
        return S.Zero
    if poly.degree() == 0:
        return S.One / p ** 2
    try:
        return discriminant(p, x)
    except (PolynomialError, BasePolynomialError):
        return None


def _eager_apart_impl(u, x):
    u = sympify(u)
    if u.is_rational_function(x):
        return apart(u, x)
    return u


_eager_apart_cached = _functools.lru_cache(maxsize=20000)(_eager_apart_impl)


def eager_Apart(u, x):
    """Mathematica ``Apart[expr, x]`` — partial-fraction decomposition in ``x``.

    Only rational functions of ``x`` decompose; anything else is returned unchanged
    (matching Mathematica, and guarding SymPy's ``apart`` which raises on non-rational
    input).  The rational-function test is SymPy's own ``is_rational_function`` -- the
    generic equivalent of what Rubi's ``RationalFunctionQ`` computes here.

    MEMOISED (bounded): sympy's ``apart`` over denominators that factor only through
    algebraic extensions is very expensive -- profiling Int[(x^4+1)/(x^8+3x^4+1)]
    showed 65% of the runtime inside apart on the same expressions, re-requested
    throughout the DFS. Unhashable input falls back to a direct call.
    """
    try:
        return _eager_apart_cached(u, x)
    except TypeError:
        return _eager_apart_impl(u, x)


def eager_PositiveQ(var):
    """Mathematica ``PositiveQ[expr]`` — True iff ``expr`` is a positive real number.

    Standard Wolfram predicate: after :func:`eager_Simplify`, a comparable value is tested
    ``> 0``; ``ComplexInfinity``/``Infinity`` and non-comparable (e.g. complex) values
    are not positive.
    """
    var = eager_Simplify(_ensure_sympy(var))
    if var in (zoo, oo):
        return False
    if var.is_comparable:
        res = var > 0
        if not res.is_Relational:
            return res
    return False


def eager_IntegerQ(var):
    """Mathematica ``IntegerQ[expr]`` — True iff ``expr`` is an explicit integer."""
    var = eager_Simplify(_ensure_sympy(var))
    if isinstance(var, (int, Integer)):
        return True
    else:
        return var.is_Integer


def eager_MemberQ(l, u):
    """Mathematica ``MemberQ[list, form]`` — True iff ``form`` occurs in ``list``.

    Head-membership: a function-head wildcard ``F_[...]`` binds its head to a
    :class:`~sympy_matching.wild.HeadRef` carrying the SymPy class, while the
    membership list may be written either as ``HeadRef`` literals (emitted by the
    codegen) or as bare function classes (``TrigQ``/``HyperbolicQ``/``InverseTrigQ``
    pass ``[sin, cos, ...]``). Both spellings are reconciled via :func:`head_to_class`
    so ``MemberQ[{ArcSin, ArcCos, ...}, F]`` fires when ``F`` bound to ``asin``/``acos``.
    """
    members = list(l) if isinstance(l, (tuple, list)) else list(l.args)
    from sympy_matching.wild import HeadRef
    if isinstance(u, HeadRef):
        uc = head_to_class(u)
        return uc is not None and any(head_to_class(m) == uc for m in members)
    return u in members


def eager_AtomQ(expr):
    """Mathematica ``AtomQ[expr]`` — True iff ``expr`` has no subexpressions."""
    expr = _ensure_sympy(expr)
    expr = sympify(expr)
    if isinstance(expr, (tuple, list, Tuple)):
        return False
    if expr in [None, True, False, Exp1]:  # [None, True, False] are atoms in mathematica and _E is also an atom
        return True
    else:
        return expr.is_Atom


def eager_NumberQ(u):
    """Mathematica ``NumberQ[u]`` — True iff ``u`` is an EXPLICIT number."""
    # Mathematica NumberQ[u]: True iff u is an EXPLICIT number -- Integer, Rational,
    # Real, or Complex[a,b] with explicit real/imaginary parts (so I, 3*I, 2+3*I are
    # numbers, but Pi, E, Sqrt[2], (-1)^(1/4), Sqrt[2]*I are NOT).
    #
    # SymPy's ``is_number`` is broader: it is True for every constant, including
    # radicals and symbolic constants. Using it made NumberQ[(-1)^(1/4)] wrongly True,
    # so NumericFactor took its NumberQ branch and returned a complex-looking value
    # (really Sqrt[2]) instead of Mathematica's 1 -- which then crashed a `< 0` test in
    # SignOfFactor. Match Mathematica: explicit real, or explicit a+b*I.
    if isinstance(u, (int, float, complex)):
        return True
    u = sympify(u)
    if isinstance(u, (Integer, Rational, Float)):
        return True
    if u.is_number:
        try:
            re_u, im_u = u.as_real_imag()
        except (TypeError, ValueError, AttributeError):
            return False
        return (im_u != 0
                and isinstance(re_u, (Integer, Rational, Float))
                and isinstance(im_u, (Integer, Rational, Float)))
    return False


def eager_PolynomialQ(u, x=None):
    """Mathematica ``PolynomialQ[u]`` / ``PolynomialQ[u, x]`` — polynomial test."""
    if x is None:
        return u.is_polynomial()
    if isinstance(x, Pow):
        if isinstance(x.exp, Integer):
            deg = degree(u, x.base)
            if u.is_polynomial(x):
                if deg % x.exp != 0:
                    return False
                try:
                    p = Poly(u, x.base)
                except PolynomialError:
                    return False

                c_list = p.all_coeffs()
                coeff_list = c_list[:-1:x.exp]
                coeff_list += [c_list[-1]]
                for i in coeff_list:
                    if not i == 0:
                        index = c_list.index(i)
                        c_list[index] = 0

                if all(i == 0 for i in c_list):
                    return True
                else:
                    return False

            else:
                return False

        elif isinstance(x.exp, (Float, Rational)):  # not full - proof
            if eager_FreeQ(simplify(u), x.base) and eager_Exponent(u, x.base) == 0:
                if not all(eager_FreeQ(u, i) for i in x.base.free_symbols):
                    return False

    if isinstance(x, Mul):
        return all(eager_PolynomialQ(u, i) for i in x.args)

    return u.is_polynomial(x)


def _is_rational_in(p, x):
    """True iff p is a proper rational function of x with x in its DENOMINATOR (e.g.
    (A+Bx)/x^2), as opposed to a polynomial in x or something transcendental in x
    (log(x), ...). Only that case needs Laurent division."""
    _, den = fraction(together(p))
    return den != 1 and x in getattr(den, 'free_symbols', set())


def _polynomial_remainder_impl(p, q, x):
    if _is_rational_in(p, x):
        num, den = fraction(together(p))
        try:
            den_inv = invert(Poly(den, x), Poly(q, x)).as_expr()
            return rem(num * den_inv, q, x)
        except (PolynomialError, PolynomialDivisionFailed, UnificationFailed, NotInvertible):
            return S.Zero
    try:
        return rem(p, q, x)
    except BasePolynomialError:
        return p


_polynomial_remainder_cached = _functools.lru_cache(maxsize=20000)(_polynomial_remainder_impl)


def eager_PolynomialRemainder(p, q, x):
    """Mathematica ``PolynomialRemainder[p, q, x]``.

    * p a polynomial in x -> ordinary remainder.
    * p transcendental in x (log(x), ...) -> Mathematica treats it as degree 0, so it is
      its own remainder mod a positive-degree q (SymPy raises; fall back to p).
    * p a RATIONAL function of x -- Rubi's ``Pq*(c x)^m`` with m<0, so ``p=(A+Bx)/x^2`` --
      -> reduce p MODULO q in K[x]/(q): with ``p = num/den`` and den invertible mod q
      (``gcd(den,q)=1``; e.g. den a power of x and ``q(0)!=0``), ``p ≡ num*den^(-1)`` (mod q).
      If den shares a factor with q there is no finite reduction and the remainder is 0
      (the quotient absorbs everything). Cross-checked vs real Rubi. The old code did an
      ordinary division here and returned the whole input p (quotient 0), zeroing integrals.

    MEMOISED (bounded): a pure function of (p, q, x); rule guards evaluate it on the
    same operands many times per DFS (profiled at 35% of a rational-function integral,
    each call doing a fraction-field ``invert``/``rem``). Unhashable input falls back
    to a direct call.
    """
    p = sympify(p)
    q = sympify(q)
    try:
        return _polynomial_remainder_cached(p, q, x)
    except TypeError:
        return _polynomial_remainder_impl(p, q, x)


def _polynomial_quotient_impl(p, q, x):
    if _is_rational_in(p, x):
        r = eager_PolynomialRemainder(p, q, x)
        try:
            return cancel((p - r) / q)
        except (PolynomialError, ZeroDivisionError):
            return p / q
    try:
        return quo(p, q, x)
    except BasePolynomialError:
        return S.Zero


_polynomial_quotient_cached = _functools.lru_cache(maxsize=20000)(_polynomial_quotient_impl)


def eager_PolynomialQuotient(p, q, x):
    """Mathematica ``PolynomialQuotient[p, q, x]``. Polynomial p -> SymPy ``quo``;
    transcendental p in x -> 0 (degree 0); RATIONAL p -> Laurent quotient
    ``(p - PolynomialRemainder[p,q,x])/q`` (e.g.
    ``PolynomialQuotient[(A+Bx)/x^2, a+b x^2] = (A+Bx)/(a x^2)``). See PolynomialRemainder.

    MEMOISED (bounded) like PolynomialRemainder -- same repeat-heavy guard usage.
    """
    p = sympify(p)
    q = sympify(q)
    try:
        return _polynomial_quotient_cached(p, q, x)
    except TypeError:
        return _polynomial_quotient_impl(p, q, x)


def eager_Not(var):
    """Mathematica Not[expr] — logical negation (tolerant of bool/None/Relational)."""
    if isinstance(var, bool):
        return not var
    elif var is None:
        return None
    elif isinstance(var, Basic) and var.is_Relational:
        var = False
    return not var
