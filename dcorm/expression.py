"""Conditional expressions."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from dcorm.engine import Engine
from dcorm.expression_base import ExpressionBase
from dcorm.operators import Operator


__all__ = ['Expression']


@dataclass(eq=False)
class Expression(ExpressionBase):
    """Conditional expression for WHERE clauses."""

    lhs: Any
    operator: Operator
    rhs: Optional[Any] = None   # Allow for unary operators.

    def __sql__(self, engine: Engine) -> Engine:
        engine.sql(self.lhs).literal(self.operator)

        if self.rhs is not None:
            engine.sql(self.rhs)

        return engine
