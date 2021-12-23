"""Conditional expressions."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Union

from dcorm.operators import Operator
from dcorm.sql import sql


__all__ = ['Expression']


@dataclass
class Expression:
    """Conditional expression for WHERE clauses."""

    lhs: Any
    operator: Operator
    rhs: Optional[Any] = None   # Compensate for unary operators.

    def __and__(self, other: Any) -> Union[Expression, bool]:
        if other is True:
            return self

        if other is False:
            return False

        return type(self)(self, Operator.AND, other)

    def __rand__(self, other: Any) -> Union[Expression, bool]:
        if other is True:
            return self

        if other is False:
            return False

        return type(self)(other, Operator.AND, self)

    def __or__(self, other: Any) -> Union[Expression, bool]:
        if other is True:
            return True

        if other is False:
            return self

        return type(self)(self, Operator.OR, other)

    def __ror__(self, other: Any) -> Union[Expression, bool]:
        if other is True:
            return True

        if other is False:
            return self

        return type(self)(other, Operator.OR, self)

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the expression."""
        if self.rhs is None:    # Compensate for unary operators.
            return f'({sql(self.operator)} {sql(self.lhs)})'

        return f'({sql(self.lhs)} {sql(self.operator)} {sql(self.rhs)})'
