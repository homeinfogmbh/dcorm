"""Definition of container types."""

from collections.abc import ItemsView, KeysView, ValuesView
from itertools import chain, filterfalse
from types import GeneratorType


__all__ = ['CONTAINERS']


CONTAINERS = (
    chain,
    dict,
    filter,
    filterfalse,
    frozenset,
    list,
    map,
    range,
    set,
    tuple,
    GeneratorType,
    ItemsView,
    KeysView,
    ValuesView
)
