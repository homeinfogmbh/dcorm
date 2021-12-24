"""Field accessors."""

from __future__ import annotations
from dataclasses import dataclass, Field as _Field
from typing import Any, NamedTuple

from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.expression_base import ExpressionBase
from dcorm.literal import unary
from dcorm.nodes import FieldIdentifier
from dcorm.ordering import Ordering


__all__ = ['NOT_SET', 'Field', 'FieldSelect', 'OrderedField']


COMMA = unary(',')
NOT_SET = object()


@dataclass(eq=False)
class Field(ExpressionBase, typ=Expression):
    """Represents a field bound to a model."""

    table: Any
    field: _Field
    value: Any = NOT_SET

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


class FieldSelect(list):
    """A fields list."""

    def __init__(self, *fields: Field):
        super().__init__(fields)

    def __sql__(self, engine: Engine) -> Engine:
        for index, field in enumerate(self):
            engine.sql(field)

            if index < len(self):
                engine.literal(COMMA)

        return engine


class OrderedField(NamedTuple):
    """Represents a field with an ordering."""

    field: Field
    ordering: Ordering

    def __sql__(self, engine: Engine) -> Engine:
        return engine.sql(self.field).sql(self.ordering)
