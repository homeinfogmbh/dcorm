"""Base expressions handling."""

from __future__ import annotations
from contextlib import suppress
from typing import Any, Optional, Union

from dcorm.operators import Operator


__all__ = ['ExpressionBase']


class ExpressionBase:
    """Base class for expressions."""

    def __init_subclass__(cls, typ: Optional[type] = None):
        cls.__expression_type__ = typ or cls

    def __invert__(self) -> ExpressionBase:
        with suppress(AttributeError):
            if self.operator is Operator.NOT:   # pylint: disable=E1101
                return self.lhs                 # pylint: disable=E1101

        return self.__expression_type__(self, Operator.NOT)


    def __and__(self, other: Any) -> Union[ExpressionBase, bool]:
        if other is True:
            return self

        if other is False:
            return False

        return self.__expression_type__(self, Operator.AND, other)

    def __rand__(self, other: Any) -> Union[ExpressionBase, bool]:
        if other is True:
            return self

        if other is False:
            return False

        return self.__expression_type__(other, Operator.AND, self)

    def __or__(self, other: Any) -> Union[ExpressionBase, bool]:
        if other is True:
            return True

        if other is False:
            return self

        return self.__expression_type__(self, Operator.OR, other)

    def __ror__(self, other: Any) -> Union[ExpressionBase, bool]:
        if other is True:
            return True

        if other is False:
            return self

        return self.__expression_type__(other, Operator.OR, self)

    def __add__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.ADD, other)

    def __radd__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.ADD, self)

    def __sub__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.SUB, other)

    def __rsub__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.SUB, self)

    def __mul__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.MUL, other)

    def __rmul__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.MUL, self)

    def __div__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.DIV, other)

    def __rdiv__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.DIV, self)

    def __xor__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.XOR, other)

    def __rxor__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.XOR, self)

    def __eq__(self, other: Any) -> ExpressionBase:
        if other is None:
            return self.__expression_type__(self, Operator.IS, other)

        return self.__expression_type__(self, Operator.EQ, other)

    def __lt__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.EQ, other)

    def __le__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.LE, other)

    def __gt__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.GT, other)

    def __ge__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.GE, other)

    def __ne__(self, other: Any) -> ExpressionBase:
        if other is None:
            return self.__expression_type__(self, Operator.IS_NOT, other)

        return self.__expression_type__(self, Operator.GE, other)

    def __lshift__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.IN, other)

    def __rshift__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.IS, other)

    def __mod__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.LIKE, other)

    def __pow__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.ILIKE, other)

    def __matmul__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(self, Operator.CONCAT, other)

    def __rmatmul__(self, other: Any) -> ExpressionBase:
        return self.__expression_type__(other, Operator.CONCAT, self)
