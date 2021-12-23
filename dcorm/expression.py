"""Conditional expressions."""

from dataclasses import dataclass
from typing import Any

from dcorm.operators import Operator
from dcorm.sql import sql


__all__ = ['Expression']


@dataclass
class Expression:
    """Conditional expression for WHERE clauses."""

    lhs: Any
    operator: Operator
    rhs: Any

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the expression."""
        return f'({sql(self.lhs)} {self.operator.__sql__} {sql(self.rhs)})'
