# -*- coding: utf-8 -*-
"""JSON serialization/deserialization extensions for SymPy objects.

Registers a singledispatch handler for `serialize_wrapped_value` so that
SymPy objects inside SymbolWrapper are serialized using the SymPy invariant:

    obj == obj.func(*obj.args)

For compound expressions (non-atoms), this works directly.
For atoms (Symbol, Integer, Rational, Float), construction args are
extracted separately since their `.args` is empty.
Singletons (pi, E, I, oo, etc.) reconstruct via `func()` alone.

Usage:
    import sympy_matching.json_ext  # registers as side-effect
"""
import importlib

import sympy
from sympy.core.basic import Basic as SympyBasic

from omnimatch.matching.json_serialization import (
    serialize_wrapped_value,
    deserialize_wrapped_value,
    register_wrapped_value_deserializer,
)


# ══════════════════════════════════════════════════════════════════════════════
# SERIALIZATION — register for sympy.Basic
# ══════════════════════════════════════════════════════════════════════════════

def _qualified_name(cls) -> str:
    """Return the fully qualified module.classname for a SymPy class/function."""
    mod = cls.__module__
    if mod is None:
        # Dynamic functions created by sympy.Function('Name') have __module__ == None
        return f"__dynamic__.{cls.__name__}"
    return f"{mod}.{cls.__qualname__}"


def _get_atom_args(obj):
    """Extract the construction arguments for a SymPy atom.

    Atoms have empty .args, so we need type-specific extraction.
    Singletons (where func() == obj) need no extra args.
    """
    # Singletons: func() alone reconstructs them
    try:
        if obj.func() == obj:
            return []
    except (TypeError, ValueError):
        pass

    # Integer: need the int value
    if obj.is_Integer:
        return [int(obj)]

    # Rational: need p and q
    if obj.is_Rational:
        return [int(obj.p), int(obj.q)]

    # Float: need the string representation for precision
    if obj.is_Float:
        return [str(obj)]

    # Symbol: need the name
    if hasattr(obj, 'name'):
        return [obj.name]

    # Unknown atom: empty (will try func() on deserialize)
    return []


@serialize_wrapped_value.register(SympyBasic)
def _serialize_sympy_value(val):
    """Serialize any SymPy object using func + args."""
    from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

    func_path = _qualified_name(val.func)

    if val.is_Atom and not val.args:
        # Atom: store func path + atom-specific construction args
        atom_args = _get_atom_args(val)
        result = {
            '_val_type': 'sympy',
            'func': func_path,
            'atom_args': atom_args,
        }
        # Special handling for WildSymbol: preserve optional_value
        if isinstance(val, WildSymbol):
            opt = val.optional_value
            if opt is IDENTITY_ELEMENT:
                result['optional_value'] = '__IDENTITY_ELEMENT__'
            elif opt is not None:
                result['optional_value'] = serialize_wrapped_value(opt)
        return result
    else:
        # Compound: recursively serialize each arg
        args = [serialize_wrapped_value(a) for a in val.args]
        return {
            '_val_type': 'sympy',
            'func': func_path,
            'args': args,
        }


# ══════════════════════════════════════════════════════════════════════════════
# DESERIALIZATION — register 'sympy' handler
# ══════════════════════════════════════════════════════════════════════════════

def _resolve_sympy_func(func_path: str):
    """Resolve a fully qualified name like 'sympy.core.numbers.Integer' to the class."""
    # Handle dynamic sympy Functions (created by sympy.Function('Name'))
    if func_path.startswith('__dynamic__.'):
        name = func_path[len('__dynamic__.'):]
        return sympy.Function(name)

    parts = func_path.rsplit('.', 1)
    if len(parts) == 2:
        module_path, name = parts
        try:
            module = importlib.import_module(module_path)
            return getattr(module, name)
        except (ImportError, AttributeError):
            pass
    # Fallback: try sympy namespace directly
    name = func_path.split('.')[-1]
    if hasattr(sympy, name):
        return getattr(sympy, name)
    raise ValueError(f"Cannot resolve SymPy function: {func_path}")


def _deserialize_sympy_value(data):
    """Deserialize a SymPy object from func + args."""
    from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

    func = _resolve_sympy_func(data['func'])

    if 'atom_args' in data:
        # Atom reconstruction
        atom_args = data['atom_args']

        # Special handling for WildSymbol: restore optional_value
        if func is WildSymbol or (isinstance(func, type) and issubclass(func, WildSymbol)):
            opt_data = data.get('optional_value')
            if opt_data == '__IDENTITY_ELEMENT__':
                return WildSymbol(*atom_args, optional_value=IDENTITY_ELEMENT)
            elif opt_data is not None:
                opt_val = deserialize_wrapped_value(opt_data)
                return WildSymbol(*atom_args, optional_value=opt_val)
            return WildSymbol(*atom_args)

        return func(*atom_args)
    else:
        # Compound reconstruction: recursively deserialize each arg
        args = [deserialize_wrapped_value(a) for a in data.get('args', [])]
        return func(*args)


# Install the deserializer through the public registration API.
register_wrapped_value_deserializer('sympy', _deserialize_sympy_value)


# =============================================================================
# Python tuple serialization -- for multi-variable constraint args
# =============================================================================
# SymPyMatchingConstraint.__new__ (sympy_matching/constraint.py) normalises list
# args to tuples so that constraint.args is always hashable (required by SymPy
# Basic.__hash__). When a constraint such as the Wolfram FreeQ(['a', 'b'], x) is
# serialised its first arg is the Python tuple (Symbol('a'), Symbol('b')) and
# needs its own handler.

@serialize_wrapped_value.register(tuple)
def _serialize_python_tuple(val):
    """Serialize a plain Python tuple used in constraint args."""
    return {
        '_val_type': 'python_tuple',
        'items': [serialize_wrapped_value(item) for item in val],
    }


def _deserialize_python_tuple(data):
    """Deserialize a Python tuple from its serialized form."""
    return tuple(deserialize_wrapped_value(item) for item in data['items'])


register_wrapped_value_deserializer('python_tuple', _deserialize_python_tuple)


# ══════════════════════════════════════════════════════════════════════════════
# Shared deserialization — for rules where pattern/replacement must share wilds
# ══════════════════════════════════════════════════════════════════════════════

def deserialize_sympy_expr(data, wild_cache=None):
    """Deserialize a SymPy expression, sharing WildSymbol instances via cache.

    Args:
        data: Serialized dict (output of serialize_wrapped_value).
        wild_cache: Optional dict {name: WildSymbol}. If provided, WildSymbol
            instances are looked up/stored here so that the same name always
            yields the same object. This is critical for rules where pattern
            and replacement must share the same WildSymbol identity.

    Returns:
        Deserialized SymPy expression.
    """
    if wild_cache is None:
        return deserialize_wrapped_value(data)
    return _deserialize_with_cache(data, wild_cache)


def _deserialize_with_cache(data, wild_cache):
    """Internal: recursively deserialize using wild_cache for WildSymbol sharing."""
    from sympy_matching.wild import WildSymbol, IDENTITY_ELEMENT

    if not isinstance(data, dict):
        return data

    val_type = data.get('_val_type')
    if val_type != 'sympy':
        return deserialize_wrapped_value(data)

    func_path = data['func']

    if 'atom_args' in data:
        # Atom
        func = _resolve_sympy_func(func_path)

        # WildSymbol: use cache
        if func is WildSymbol or (isinstance(func, type) and issubclass(func, WildSymbol)):
            name = data['atom_args'][0]
            if name in wild_cache:
                return wild_cache[name]
            # Create new WildSymbol with optional_value
            opt_data = data.get('optional_value')
            if opt_data == '__IDENTITY_ELEMENT__':
                ws = WildSymbol(name, optional_value=IDENTITY_ELEMENT)
            elif opt_data is not None:
                opt_val = deserialize_wrapped_value(opt_data)
                ws = WildSymbol(name, optional_value=opt_val)
            else:
                ws = WildSymbol(name)
            wild_cache[name] = ws
            return ws

        atom_args = data['atom_args']
        return func(*atom_args)
    else:
        # Compound: recursively deserialize each arg with cache
        args = [_deserialize_with_cache(a, wild_cache) for a in data.get('args', [])]
        func = _resolve_sympy_func(func_path)
        return func(*args)
