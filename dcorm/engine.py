"""SQL engine configuration."""

from __future__ import annotations
from contextlib import suppress
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union

from dcorm.csq import CSQParens
from dcorm.field_types import FieldType
from dcorm.literal import Literal
from dcorm.nodes import TableIdentifier, FieldIdentifier
from dcorm.operators import Operator


__all__ = ['Engine']


@dataclass
class Engine:   # pylint: disable=R0902
    """An SQL engine."""

    field_types: dict[str, FieldType] = field(default_factory=dict)
    operators: dict[Operator, Operator] = field(default_factory=dict)
    param: str = '?'
    quote: str = '""'
    csq_parens: CSQParens = CSQParens.NEVER
    for_update: bool = False
    index_schema_prefix: bool = False
    index_using_precedes_table: bool = False
    limit_max: Optional[int] = None
    nulls_ordering: bool = False
    _sql: list[str] = field(default_factory=list)
    _values: list[str] = field(default_factory=list)

    def conflict_statement(self, on_conflict, query):
        """Handle statement conflicts."""
        raise NotImplementedError()

    def conflict_update(self, on_conflict, query):
        """Handle update conflicts."""
        raise NotImplementedError()

    def value(self, value: Any) -> Engine:
        """Set a value."""
        if isinstance(value, (bool, float, int)):
            self._sql.append('%s')
            self._values.append(value)

        if isinstance(value, str):
            self._sql.append("'%s'")
            self._values.append(value)

        raise TypeError(f'Cannot serialize value: {type(value)}')


    def add_table_identifier(self, ident: TableIdentifier) -> Engine:
        """Adds a table identifier."""
        self._sql.append('.'.join(['%s'] * len(ident)))
        self._values.extend(ident)
        return self

    def add_field_identifier(self, ident: FieldIdentifier) -> Engine:
        """Adds a field identifier."""
        self._sql.append('.'.join(['%s'] * len(ident)))
        self._values.extend(ident)
        return self

    def sql(self, obj: Any) -> Engine:
        """Returns an SQL object from any given object."""
        with suppress(AttributeError):
            return obj.__sql__(self)

        if isinstance(obj, TableIdentifier):
            return self.add_table_identifier(obj)

        if isinstance(obj, FieldIdentifier):
            return self.add_field_identifier(obj)

        return self.value(obj)

        #raise TypeError(f'Invalid SQL node: {type(obj)}')

    def literal(self, obj: Union[Enum, Literal]) -> Engine:
        """Processes a literal."""
        if isinstance(obj, Enum):
            return self.literal(obj.value)

        if isinstance(obj, Literal):
            self._sql.append(str(obj))
            return self

        raise TypeError(f'Invalid literal type: {type(obj)}')

    def query(self) -> tuple[str, list[str]]:
        """Returns the query parameters."""
        return (''.join(self._sql), self._values)

    def query_string(self) -> str:
        """Returns the query string."""
        template, values = self.query()
        return template % tuple(values)
