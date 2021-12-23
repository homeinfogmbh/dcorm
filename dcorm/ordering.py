"""Ordering type definition."""

from enum import Enum


__all__ = ['Ordering']


class Ordering(Enum):
    """Available orderings."""

    ASC = 'ASC'
    DESC = 'DESC'

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the ordering."""
        return self.value
