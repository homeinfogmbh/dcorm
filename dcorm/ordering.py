"""Ordering type definition."""

from enum import Enum

from dcorm.literal import Literal


__all__ = ['Ordering']


class Ordering(Enum):
    """Available orderings."""

    ASC = Literal('ASC', space_left=True)
    DESC = Literal('DESC', space_left=True)
