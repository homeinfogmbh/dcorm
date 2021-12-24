"""Compund sub-queries modes."""

from enum import Enum


__all__ = ['CSQParens']


class CSQParens(Enum):
    """Options for parentheses around compound subqueries."""

    NEVER = auto()
    ALWAYS = auto()
    UNNESTED = auto()
