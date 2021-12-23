"""SQL statement generation."""

from contextlib import suppress
from typing import Any

from dcorm.containers import CONTAINERS


__all__ = ['sql']


def sql(obj: Any) -> str:
    """Reutrns an SQL representation of the given object."""

    with suppress(AttributeError):
        return obj.__sql__

    if isinstance(obj, str):
        return obj

    if isinstance(obj, bool):
        return str(int(obj))

    if isinstance(obj, (int, float)):
        return str(obj)

    if isinstance(obj, CONTAINERS):
        return f"({', '.join(sql(item) for item in obj)})"

    raise TypeError(f'Cannot convert {type(obj)} to SQL.')
