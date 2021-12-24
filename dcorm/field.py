"""Field accessors."""

from __future__ import annotations
from dataclasses import MISSING, dataclass, Field as _Field
from typing import Any, NamedTuple

from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.expression_base import ExpressionBase
from dcorm.nodes import FieldIdentifier
from dcorm.ordering import Ordering
from dcorm.sql import sql


__all__ = ['Field', 'OrderedField']


@dataclass(eq=False)
class Field(ExpressionBase, typ=Expression):
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

    @property
    def name(self) -> str:
        """Returns the field name."""
        return self.field.metadata.get('column_name', self.field.name)

    @property
    def identifier(self) -> FieldIdentifier:
        """Returns the field identifier."""
        return self.table.__table_identifier__.field(self.name)

    def __sql__(self, engine: Engine) -> Engine:
        return engine.sql(self.identifier)


class OrderedField(NamedTuple):
    """Represents a field with an ordering."""

    field: Field
    ordering: Ordering

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the ordering."""
        return f'{sql(self.field)} {sql(self.ordering)}'
