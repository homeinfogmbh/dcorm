"""SQL engine configuration."""

from __future__ import annotations
from contextlib import suppress
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union

from dcorm.csq import CSQParens
from dcorm.field_types import FieldType
from dcorm.literal import Literal
from dcorm.operators import Operator


__all__ = ['Engine']


@dataclass
class Engine:   # pylint: disable=R0902
    """An SQL engine."""

    field_types: dict[str, FieldType] = field(default_factory=dict)
    operators: dict[Operator, Operator] = field(default_factory=dict)
    param: str = '?'
    quotes: str = '"{}"'
    csq_parens: CSQParens = CSQParens.NEVER
    for_update: bool = False
    index_schema_prefix: bool = False
    index_using_precedes_table: bool = False
    limit_max: Optional[int] = None
    nulls_ordering: bool = False
    _sql: list[str] = field(default_factory=list)
    _values: list[str] = field(default_factory=list)

    def quote(self, string: str) -> str:
        """Quotes the given string."""
        return self.quotes.format(string)

    def value(self, value: Any, *, raw: bool = False) -> Engine:
        """Set a value."""
        if isinstance(value, (bool, float, int)):
            if not raw:
                self._sql.append('%s')

            self._values.append(value)
        elif isinstance(value, str):
            if not raw:
                self._sql.append("'%s'")

            self._values.append(value)
        else:
            raise TypeError(f'Cannot serialize value: {type(value)}')

        return self

    def sql(self, obj: Any) -> Engine:
        """Returns an SQL object from any given object."""
        with suppress(AttributeError):
            return obj.__sql__(self)

        return self.value(obj)

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
