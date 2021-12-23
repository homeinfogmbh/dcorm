"""SQL statement generation."""

from contextlib import suppress
from typing import Any


__all__ = ['sql']


def sql(obj: Any) -> str:
    """Reutrns an SQL representation of the given object."""

    with suppress(AttributeError):
        return obj.__sql__

    if isinstance(obj, bool):
        return sql(int(obj))

    if isinstance(obj, (int, float)):
        return str(obj)

    raise TypeError(f'Cannot convert {type(obj)} to SQL.')
