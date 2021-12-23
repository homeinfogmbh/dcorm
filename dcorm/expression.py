"""Conditional expressions."""

from __future__ import annotations
from typing import Any, NamedTuple, Optional

from dcorm.expression_functions import expression_generator
from dcorm.operators import Operator
from dcorm.sql import sql


__all__ = ['Expression']


@expression_generator
class Expression(NamedTuple):
    """Conditional expression for WHERE clauses."""

    lhs: Any
    operator: Operator
    rhs: Optional[Any] = None   # Compensate for unary operators.

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the expression."""
        if self.rhs is None:    # Compensate for unary operators.
            return f'({sql(self.operator)} {sql(self.lhs)})'

        return f'({sql(self.lhs)} {sql(self.operator)} {sql(self.rhs)})'
