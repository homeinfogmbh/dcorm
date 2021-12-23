"""Query operations."""

from enum import Enum


__all__ = ['Operation']


class Operation(Enum):
    """Available databse operations."""

    CREATE = 'CREATE'
    DELETE = 'DELETE'
    INSERT = 'INSERT'
    SELECT = 'SELECT'
    UPDATE = 'UPDATE'

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the operation."""
        return self.value
