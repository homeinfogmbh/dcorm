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

    def __add__(self, other: Any) -> Expression:
        return type(self)(self, Operator.ADD, other)

    def __radd__(self, other: Any) -> Expression:
        return type(self)(other, Operator.ADD, self)

    def __sub__(self, other: Any) -> Expression:
        return type(self)(self, Operator.SUB, other)

    def __rsub__(self, other: Any) -> Expression:
        return type(self)(other, Operator.SUB, self)

    def __mul__(self, other: Any) -> Expression:
        return type(self)(self, Operator.MUL, other)

    def __rmul__(self, other: Any) -> Expression:
        return type(self)(other, Operator.MUL, self)

    def __div__(self, other: Any) -> Expression:
        return type(self)(self, Operator.DIV, other)

    def __rdiv__(self, other: Any) -> Expression:
        return type(self)(other, Operator.DIV, self)

    def __xor__(self, other: Any) -> Expression:
        return type(self)(self, Operator.XOR, other)

    def __rxor__(self, other: Any) -> Expression:
        return type(self)(other, Operator.XOR, self)

    def __mod__(self, other: Any) -> Expression:
        return type(self)(self, Operator.MOD, other)

    def __rmod__(self, other: Any) -> Expression:
        return type(self)(other, Operator.MOD, self)

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the expression."""
        if self.rhs is None:    # Compensate for unary operators.
            return f'({sql(self.operator)} {sql(self.lhs)})'

        return f'({sql(self.lhs)} {sql(self.operator)} {sql(self.rhs)})'
