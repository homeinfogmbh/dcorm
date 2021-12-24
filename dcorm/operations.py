"""Query operations."""

from enum import Enum

from dcorm.literal import unary


__all__ = ['Operation']


class Operation(Enum):
    """Available databse operations."""

    CREATE = unary('CREATE')
    DELETE = unary('DELETE')
    INSERT = unary('INSERT')
    SELECT = unary('SELECT')
    UPDATE = unary('UPDATE')
