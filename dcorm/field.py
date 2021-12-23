"""Field accessors."""

from __future__ import annotations
from dataclasses import MISSING, Field as _Field
from typing import Any, NamedTuple

from dcorm.ordering import Ordering
from dcorm.sql import sql


__all__ = ['Field']


class Field(NamedTuple):
    """Represents a field bound to a model."""

    table: Any
    field: _Field
    value: Any = MISSING

    def asc(self) -> OrderedField:
        """Returns an ordered field with ascending ordering."""
        return OrderedField(self, Ordering.ASC)

    def desc(self) -> OrderedField:
        """Returns an ordered field with descending ordering."""
        return OrderedField(self, Ordering.DESC)


class OrderedField(NamedTuple):
    """Represents a field with an ordering."""

    field: Field
    ordering: Ordering

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the ordering."""
        return f'{sql(self.field)} {sql(self.ordering)}'
