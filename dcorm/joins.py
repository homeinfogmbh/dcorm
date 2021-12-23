"""Join types."""

from enum import Enum


__all__ = ['Join']


class Join(Enum):
    """Available JOIN types."""

    INNER = 'INNER JOIN'
    LEFT_OUTER = 'LEFT OUTER JOIN'
    RIGHT_OUTER = 'RIGHT OUTER JOIN'
    FULL = 'FULL JOIN'
    FULL_OUTER = 'FULL OUTER JOIN'
    CROSS = 'CROSS JOIN'
    NATURAL = 'NATURAL JOIN'
    LATERAL = 'LATERAL'
    LEFT_LATERAL = 'LEFT JOIN LATERAL'

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the JOIN."""
        return self.value
