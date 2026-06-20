# -*- coding: utf-8 -*-
"""Contains several pattern constraint classes.

A pattern constraint is used to further filter which subjects a pattern matches.

The most common use would be the :class:`CustomConstraint`, which wraps a lambda or function to act as a constraint:

>>> a_symbol_constraint = CustomConstraint(lambda x: x.name.startswith('a'))
>>> pattern = Pattern(x_, a_symbol_constraint)
>>> is_match(Symbol('a1'), pattern)
True
>>> is_match(Symbol('b1'), pattern)
False

There is also the :class:`EqualVariablesConstraint` which will try to unify the substitutions of the variables and only
match if it succeeds:

>>> equal_constraint = EqualVariablesConstraint('x', 'y')
>>> pattern = Pattern(f(x_, y_), equal_constraint)
>>> is_match(f(a, a), pattern)
True
>>> is_match(f(a, b), pattern)
False

You can also create a subclass of the :class:`Constraint` class to create your own custom constraint type.
"""
import inspect
from collections import OrderedDict
from typing import Callable, FrozenSet, Dict
from functools import cached_property

from pydantic import BaseModel, ConfigDict, PrivateAttr

from . import substitution
from ..utils import get_short_lambda_source


__all__ = ['Constraint', 'EqualVariablesConstraint', 'CustomConstraint', 'FreeQ']


class Constraint(BaseModel):  # pylint: disable=too-few-public-methods
    """Base for pattern constraints.

    A constraint is essentially a callback, that receives the match :class:`Substitution` and returns a :class:`bool`
    indicating whether the match is valid.

    You have to override all the abstract methods if you wish to create your own subclass.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __call__(self, match: substitution.Substitution) -> bool:  # pylint: disable=missing-raises-doc
        """Return True, iff the constraint is fulfilled by the substitution.

        Override this in your subclass to define the actual constraint behavior.

        Args:
            match:
                The (current) match substitution. Note that the matching is done from left to right, so not all
                variables may have a value yet. You need to override `variables` so that the constraint gets
                called once all the variables it depends on have a value assigned to them.

        Returns:
            True, iff the constraint is fulfilled by the substitution.
        """
        raise NotImplementedError

    def __eq__(self, other):
        """Constraints need to be equatable."""
        raise NotImplementedError

    def __hash__(self):
        """Constraints need to be hashable."""
        raise NotImplementedError

    @property
    def variables(self) -> FrozenSet[str]:
        """The names of the variables the constraint depends upon.

        Used by matchers to decide when a constraint can be evaluated (which is when all
        the dependency variables have been assigned a value). If the set is empty, the constraint will
        only be evaluated once the whole match is complete.
        """
        return frozenset()

    def with_renamed_vars(self, renaming: Dict[str, str]) -> 'Constraint':  # pylint: disable=missing-raises-doc
        """Return a *copy* of the constraint with renamed variables.
        This is called when the variables in the expression are renamed and hence the ones in the constraint have to be
        renamed as well. A later invocation of :meth:`__call__` will have the new variable names.
        You will have to implement this if your constraint needs to use the variables of the match substitution.
        Note that this can be called multiple times and you might have to account for that.
        Also, this should not modify the original constraint but rather return a copy.
        Args:
            renaming:
                A dictionary mapping old names to new names.
        Returns:
            A copy of the constraint with renamed variables.
        """
        raise NotImplementedError


class EqualVariablesConstraint(Constraint):  # pylint: disable=too-few-public-methods
    """A constraint that ensure multiple variables are equal.

    The constraint tries to unify the substitutions for the variables and is fulfilled iff that succeeds.
    """
    _variables: FrozenSet[str] = PrivateAttr(default_factory=frozenset)

    def __init__(self, *variables: str, **kwargs) -> None:
        """
        Args:
            *variables: The names of the variables to check for equality.
        """
        super().__init__(**kwargs)
        self._variables = frozenset(variables)

    @property
    def variables(self):
        return self._variables

    def __call__(self, match: substitution.Substitution) -> bool:
        subst = substitution.Substitution()
        for name in self._variables:
            try:
                subst.try_add_variable('_', match[name])
            except ValueError:
                return False
        return True

    def __str__(self):
        return '({!s})'.format(' == '.join(sorted(self._variables)))

    def __repr__(self):
        return 'EqualVariablesConstraint({!s})'.format(' == '.join(sorted(self._variables)))

    def __eq__(self, other):
        return isinstance(other, EqualVariablesConstraint) and self._variables == other._variables

    def __hash__(self):
        return hash(self._variables)

    def with_renamed_vars(self, renaming):
        return EqualVariablesConstraint(*(renaming.get(v, v) for v in self.variables))


class CustomConstraint(Constraint):  # pylint: disable=too-few-public-methods
    """Wrapper for lambdas of functions as constraints.

    The parameter names have to be the same as the the variable names in the expression:

    >>> constraint = CustomConstraint(lambda x, y: x.name < y.name)
    >>> pattern = Pattern(f(x_, y_), constraint)
    >>> is_match(f(a, b), pattern)
    True
    >>> is_match(f(b, a), pattern)
    False

    The ordering of the parameters is not important. You only need to have the parameters needed for the constraint,
    not all variables occurring in the pattern.

    Note, that the matching happens from left left to right, so not all variables may have been assigned a value when
    constraint is called. For constraints over multiple variables you should attach the constraint to the last
    variable occurring in the pattern or a surrounding operation.
    """
    constraint: Callable[..., bool]
    _variables: OrderedDict = PrivateAttr(default_factory=OrderedDict)

    def __init__(self, constraint: Callable[..., bool], **kwargs) -> None:
        """
        Args:
            constraint:
                The constraint callback.

        Raises:
            ValueError:
                If the callback has positional-only or variable parameters (\\*args and \\*\\*kwargs).
        """
        super().__init__(constraint=constraint, **kwargs)

        signature = inspect.signature(constraint)
        variables = OrderedDict()

        for param in signature.parameters.values():
            if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD or param.kind == inspect.Parameter.KEYWORD_ONLY:
                variables[param.name] = param.name
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                raise ValueError("Constraint cannot have variable keyword arguments ({})".format(param.name))
            else:
                raise ValueError(
                    "Constraint cannot have positional-only or variable positional arguments ({})".format(param.name)
                )

        self._variables = variables

    @cached_property
    def variables(self):
        return frozenset(self._variables.values())

    def __call__(self, match: substitution.Substitution) -> bool:
        try:
            args = dict((name, match[var_name]) for name, var_name in self._variables.items())
        except KeyError:
            return True  # Not all variables bound yet; constraint will be re-checked later
        return self.constraint(**args)

    def _get_name(self):
        try:
            return get_short_lambda_source(self.constraint) or self.constraint.__name__
        except Exception:
            return 'UNKNOWN'

    def __str__(self):
        return '({!s})'.format(self._get_name())

    def __repr__(self):
        return 'CustomConstraint({!s})'.format(self._get_name())

    def __eq__(self, other):
        return (
            isinstance(other, CustomConstraint) and self.constraint == other.constraint and
            self._variables == other._variables
        )

    def __hash__(self):
        return hash(self.constraint)

    def with_renamed_vars(self, renaming):
        cc = CustomConstraint(self.constraint)
        for param_name in cc._variables.keys():
            old_name = self._variables[param_name]
            cc._variables[param_name] = renaming.get(old_name, old_name)
        return cc


class FreeQ(Constraint):
    """Constraint that checks an expression is free of a given symbol.

    FreeQ(variable, symbol_name) succeeds when the expression bound to `variable`
    does NOT contain a Symbol with name `symbol_name` anywhere in its tree.

    This is analogous to Mathematica's FreeQ[expr, x].

    Optimized over a CustomConstraint because:
    - Uses a dedicated iterative traversal with early exit (no generator overhead)
    - No lambda/closure indirection
    - Proper __repr__ for debugging and code generation

    Example::

        >>> from matchpy import *
        >>> x_ = Wildcard.dot('x')
        >>> y_ = Wildcard.dot('y')
        >>> f = Operation.new('f', Arity.binary)
        >>> # y must not contain symbol 'x'
        >>> pattern = Pattern(f(x_, y_), FreeQ('y', 'x'))
        >>> is_match(f(Symbol('x'), Symbol('a')), pattern)
        True
        >>> is_match(f(Symbol('x'), Symbol('x')), pattern)
        False
    """

    variable: str
    symbol_name: str

    def __init__(self, variable: str, symbol_name: str, **kwargs) -> None:
        """
        Args:
            variable:
                The name of the pattern variable whose bound expression will be checked.
            symbol_name:
                The name of the symbol that must NOT appear anywhere in the expression.
        """
        super().__init__(variable=variable, symbol_name=symbol_name, **kwargs)

    @cached_property
    def variables(self) -> FrozenSet[str]:
        return frozenset({self.variable})

    def __call__(self, match: substitution.Substitution) -> bool:
        try:
            expr = match[self.variable]
        except KeyError:
            return True  # Variable not yet bound; will be re-checked later

        return self._is_free(expr)

    def _is_free(self, expr) -> bool:
        """Check that expr does not contain an atom with the given name.

        Uses an explicit stack for tree traversal (no recursion limit issues,
        no generator overhead) and exits immediately upon finding the symbol.
        Checks both Symbol (by name) and SymbolWrapper (by str(value)).
        """
        from .expressions import Symbol, SymbolWrapper, Operation

        # Handle sequence variable values (tuples, lists, Multisets)
        if isinstance(expr, (tuple, list)):
            stack = list(expr)
        else:
            stack = [expr]

        while stack:
            node = stack.pop()
            if isinstance(node, Symbol):
                if node.name == self.symbol_name:
                    return False
            elif isinstance(node, SymbolWrapper):
                if node.name == self.symbol_name:
                    return False
            elif isinstance(node, Operation):
                stack.extend(node.operands)
            elif isinstance(node, (tuple, list)):
                stack.extend(node)
        return True

    def __str__(self):
        return 'FreeQ({}, {})'.format(self.variable, self.symbol_name)

    def __repr__(self):
        return 'FreeQ({!r}, {!r})'.format(self.variable, self.symbol_name)

    def __eq__(self, other):
        return (
            isinstance(other, FreeQ) and
            self.variable == other.variable and
            self.symbol_name == other.symbol_name
        )

    def __hash__(self):
        return hash(('FreeQ', self.variable, self.symbol_name))

    def with_renamed_vars(self, renaming: Dict[str, str]) -> 'FreeQ':
        new_variable = renaming.get(self.variable, self.variable)
        return FreeQ(new_variable, self.symbol_name)
