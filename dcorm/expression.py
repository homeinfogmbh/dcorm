"""Conditional expressions."""

from __future__ import annotations
from typing import Any, NamedTuple, Optional

from dcorm.engine import Engine
from dcorm.expression_functions import expression_generator
from dcorm.operators import Operator


__all__ = ['Expression']


@expression_generator
class Expression(NamedTuple):
    """Conditional expression for WHERE clauses."""

    lhs: Any
    operator: Operator
    rhs: Optional[Any] = None   # Allow for unary operators.

    def __sql__(self, engine: Engine) -> Engine:
        engine.sql(self.lhs).literal(self.operator)

        if self.rhs is not None:
            engine.sql(self.rhs)

        return engine
