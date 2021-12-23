"""Functions to concatenate typs."""

from functools import partial
from typing import Any, Callable, Optional, Union

from dcorm.operators import Operator


__all__ = ['expression_generator']


def op_not(typ: type) -> Callable:
    """Generates and NOT operator method."""

    def inner(self) -> Union[typ, bool]:
        return typ(self, Operator.NOT)

    return inner


def op_and(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and AND operator method."""

    def inner(self, other: Any) -> Union[typ, bool]:
        if other is True:
            return self

        if other is False:
            return False

        if inverse:
            return typ(other, Operator.AND, self)

        return typ(self, Operator.AND, other)

    return inner


def op_or(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and OR operator method."""

    def inner(self, other: Any) -> Union[typ, bool]:
        if other is True:
            return True

        if other is False:
            return self

        if inverse:
            return typ(other, Operator.OR, self)

        return typ(self, Operator.OR, other)

    return inner


def op_add(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and ADD operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.ADD, self)

        return typ(self, Operator.ADD, other)

    return inner


def op_sub(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and SUB operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.SUB, self)

        return typ(self, Operator.SUB, other)

    return inner


def op_mul(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and MUL operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.MUL, self)

        return typ(self, Operator.MUL, other)

    return inner


def op_div(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and DIV operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.DIV, self)

        return typ(self, Operator.DIV, other)

    return inner


def op_xor(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and XOR operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.XOR, self)

        return typ(self, Operator.XOR, other)

    return inner


def op_eq(typ: type) -> Callable:
    """Generates and EQ operator method."""

    def inner(self, other: Any) -> typ:
        if other is None:
            return typ(self, Operator.IS, other)

        return typ(self, Operator.EQ, other)

    return inner


def op_lt(typ: type) -> Callable:
    """Generates and LT operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.EQ, other)

    return inner


def op_le(typ: type) -> Callable:
    """Generates and LE operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.LE, other)

    return inner


def op_gt(typ: type) -> Callable:
    """Generates and GT operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.GT, other)

    return inner


def op_ge(typ: type) -> Callable:
    """Generates and GE operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.GE, other)

    return inner


def op_ne(typ: type) -> Callable:
    """Generates and NE operator method."""

    def inner(self, other: Any) -> typ:
        if other is None:
            return typ(self, Operator.IS_NOT, other)

        return typ(self, Operator.GE, other)

    return inner


def op_in(typ: type) -> Callable:
    """Generates and IN operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.IN, other)

    return inner


def op_is(typ: type) -> Callable:
    """Generates and IS operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.IS, other)

    return inner


def op_like(typ: type) -> Callable:
    """Generates and LIKE operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.LIKE, other)

    return inner


def op_ilike(typ: type) -> Callable:
    """Generates and ILIKE operator method."""

    def inner(self, other: Any) -> typ:
        return typ(self, Operator.ILIKE, other)

    return inner


def op_concat(typ: type, *, inverse: bool = False) -> Callable:
    """Generates and CONCAT operator method."""

    def inner(self, other: Any) -> typ:
        if inverse:
            return typ(other, Operator.CONCAT, self)

        return typ(self, Operator.CONCAT, other)

    return inner


METHODS = {
    '__invert__': op_not,
    '__and__': op_and,
    '__rand__': partial(op_and, inverse=True),
    '__or__': op_or,
    '__ror__': partial(op_or, inverse=True),
    '__add__': op_add,
    '__radd__': partial(op_add, inverse=True),
    '__sub__': op_sub,
    '__rsub__': partial(op_sub, inverse=True),
    '__mul__': op_mul,
    '__rmul__': partial(op_mul, inverse=True),
    '__div__': op_div,
    '__rdiv__': partial(op_div, inverse=True),
    '__xor__': op_xor,
    '__rxor__': partial(op_xor, inverse=True),
    '__eq__': op_eq,
    '__lt__': op_lt,
    '__le__': op_le,
    '__gt__': op_gt,
    '__ge__': op_ge,
    '__ne__': op_ne,
    '__lshift__': op_in,
    '__rshift__': op_is,
    '__mod__': op_like,
    '__pow__': op_ilike,
    '__matmul__': op_concat,
    '__rmatmul__': partial(op_concat, inverse=True),
}


def expression_generator(cls: Optional[type] = None, /, *,
                         typ: Optional[type] = None) -> type:
    """Decorates the class with the above magic methods."""

    def inner(target: Optional[type] = None) -> type:
        for method, function in METHODS.items():
            setattr(target, method, function(typ))

        return target

    if cls is None:
        return inner

    typ = cls
    return inner(cls)
