"""Field accessors."""

from __future__ import annotations
from dataclasses import dataclass, Field as _Field
from typing import Any, NamedTuple

from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.expression_base import ExpressionBase
from dcorm.literal import unary
from dcorm.ordering import Ordering
from dcorm.path import Path


__all__ = ['NOT_SET', 'Column', 'ColumnSelect', 'OrderedColumn']


COMMA = unary(',')
NOT_SET = object()


@dataclass(eq=False)
class Column(ExpressionBase, typ=Expression):
    """Represents a column bound to a model."""

    table: Any
    field: _Field
    value: Any = NOT_SET

    def asc(self) -> OrderedColumn:
        """Returns an ordered column with ascending ordering."""
        return OrderedColumn(self, Ordering.ASC)

    def desc(self) -> OrderedColumn:
        """Returns an ordered column with descending ordering."""
        return OrderedColumn(self, Ordering.DESC)

    @property
    def name(self) -> str:
        """Returns the column's name."""
        return self.field.metadata.get('column_name', self.field.name)

    @property
    def path(self) -> Path:
        """Returns the column's path."""
        path = self.table.__table_path__
        path.append(self.name)
        return path

    def __sql__(self, engine: Engine) -> Engine:
        return engine.sql(self.path)


class ColumnSelect(list):
    """A fields list."""

    def __init__(self, *columns: Column):
        super().__init__(columns)

    def __sql__(self, engine: Engine) -> Engine:
        for index, column in enumerate(self, start=1):
            engine.sql(column)

            if index < len(self):
                engine.literal(COMMA)

        return engine


class OrderedColumn(NamedTuple):
    """Represents a table column with ordering."""

    field: Column
    ordering: Ordering

    def __sql__(self, engine: Engine) -> Engine:
        return engine.sql(self.field).sql(self.ordering)
