# -*- coding: utf-8 -*-
"""Lightweight typed base replacing Pydantic ``BaseModel``.

`TypedModel` declares fields via class annotations (like a dataclass), assigns
them in ``__init__(**kwargs)``, applies defaults, and enforces a **shallow**
``isinstance`` type-check per field at construction time — Python does not
otherwise check that an assigned value matches the field's declared type.

The check is deliberately shallow (outer type only; e.g. ``List[Expression]`` is
checked as ``isinstance(value, list)``, not element-by-element) and is compiled
once per field, so it stays cheap on the matcher's hot construction path. This is
a fraction of Pydantic's per-instance schema validation cost while still catching
"wrong type assigned to field".

Use ``field(default_factory=...)`` for mutable defaults (list/dict/set), exactly
like ``dataclasses.field`` / Pydantic ``Field``.
"""
import typing

_MISSING = object()
_NoneType = type(None)


class _FieldSpec:
    __slots__ = ('default', 'default_factory')

    def __init__(self, default=_MISSING, default_factory=None):
        self.default = default
        self.default_factory = default_factory


def field(*, default=_MISSING, default_factory=None):
    """Declare a field default (mirrors ``dataclasses.field`` / Pydantic ``Field``)."""
    return _FieldSpec(default, default_factory)


def _make_checker(typ):
    """Compile ``(type_name, predicate)`` for a field annotation, or ``None`` to skip.

    Returns ``None`` for ``Any``/``object``, forward refs, ``TypeVar``, and unions
    that include a non-class member (checked leniently). Generic aliases are
    reduced to their origin (``List[X]`` -> ``list``).
    """
    if typ is None or typ is typing.Any or typ is object:
        return None
    if type(typ) is type:
        return (typ.__name__, lambda v, t=typ: isinstance(v, t))
    origin = typing.get_origin(typ)
    if origin is None:
        return None  # ForwardRef / TypeVar / special form -> no check
    if origin is typing.Union:
        args = typing.get_args(typ)
        if any(a is not _NoneType and type(a) is not type for a in args):
            return None  # a member is a forward ref etc. -> be lenient
        concrete = tuple(a for a in args if a is not _NoneType)
        has_none = _NoneType in args
        name = ' | '.join(a.__name__ for a in concrete) + (' | None' if has_none else '')

        def _check_union(v, concrete=concrete, has_none=has_none):
            if v is None:
                return has_none
            return isinstance(v, concrete)

        return (name, _check_union)
    if type(origin) is type:
        return (getattr(origin, '__name__', str(origin)), lambda v, o=origin: isinstance(v, o))
    return None


def _resolve_fields(cls):
    """(name -> (_FieldSpec, checker)) for ``cls`` across its MRO; cached on the class."""
    cached = cls.__dict__.get('__typed_fields__')
    if cached is not None:
        return cached
    fields = {}
    for klass in reversed(cls.__mro__):  # base-to-derived so subclasses override
        for name, typ in klass.__dict__.get('__annotations__', {}).items():
            if name.startswith('_'):  # private attrs are not fields
                continue
            if typ is typing.ClassVar or typing.get_origin(typ) is typing.ClassVar:
                # ClassVar (bare `ClassVar` has no typing origin, `ClassVar[T]`
                # does). A subclass may redefine an inherited field as a ClassVar
                # (a fixed class-level value); it then stops being an instance field.
                fields.pop(name, None)
                continue
            raw_default = klass.__dict__.get(name, _MISSING)
            if isinstance(raw_default, _FieldSpec):
                spec = raw_default
            elif raw_default is _MISSING:
                spec = _FieldSpec()
            else:
                spec = _FieldSpec(default=raw_default)
            fields[name] = (spec, _make_checker(typ))
    cls.__typed_fields__ = fields
    return fields


class TypedModel:
    """Base for annotation-declared, type-checked value objects (replaces BaseModel)."""

    def __init__(self, **kwargs):
        for name, (spec, checker) in _resolve_fields(type(self)).items():
            if name in kwargs:
                value = kwargs.pop(name)
            elif spec.default_factory is not None:
                value = spec.default_factory()
            elif spec.default is not _MISSING:
                value = spec.default
            else:
                raise TypeError("{}: missing required argument '{}'".format(type(self).__name__, name))
            if checker is not None and not checker[1](value):
                raise TypeError("{}.{} expected {}, got {}".format(
                    type(self).__name__, name, checker[0], type(value).__name__))
            object.__setattr__(self, name, value)
        if kwargs:
            # Ignore leftover kwargs that name a class-level attribute (e.g. a
            # field a subclass turned into a ClassVar, still passed by a base
            # __init__); error only on genuinely unknown names.
            unexpected = [k for k in kwargs if not hasattr(type(self), k)]
            if unexpected:
                raise TypeError("{}: unexpected keyword arguments {}".format(
                    type(self).__name__, unexpected))
