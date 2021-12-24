"""SQL statement generation and base engine."""

from contextlib import suppress
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

from dcorm.containers import CONTAINERS


__all__ = ['sql', 'SQL', 'Engine', 'FieldIdentifier', 'TableIdentifier']


def sql(obj: Any) -> str:   # pylint: disable=R0911
    """Reutrns an SQL representation of the given object for printing."""

    if obj is None:
        return 'NULL'

    with suppress(AttributeError):
        return obj.__sql__

    if isinstance(obj, str):
        return obj

    if isinstance(obj, bool):
        return str(int(obj))

    if isinstance(obj, bytes):
        try:
            return obj.decode('utf8')
        except UnicodeDecodeError:
            return obj.decode('raw_unicode_escape')

    if isinstance(obj, (date, datetime, time)):
        return obj.isoformat()

    if isinstance(obj, (int, float, Decimal)):
        return str(obj)

    if isinstance(obj, CONTAINERS):
        return f"({', '.join(sql(item) for item in obj)})"

    raise TypeError(f'Cannot convert {type(obj)} to SQL.')


@dataclass
class SQL:
    """An SQL object."""

    formatstring: str
    parameters: list[str] = field(default_factory=list)


class Engine:   # pylint: disable=R0903
    """An SQL engine."""

    def sql(self, obj: Any) -> SQL:
        """Returns an SQL object from any given object."""
        raise NotImplementedError()


class FieldIdentifier(list):
    """A field identifier."""

    def __init__(self, *path: str):
        super().__init__(path)


class TableIdentifier(list):
    """A table identifier."""

    def __init__(self, *path: str):
        super().__init__(path)

    def field(self, name: str) -> FieldIdentifier:
        """Returns a field identifier from the table identifier."""
        return FieldIdentifier(*self, name)
