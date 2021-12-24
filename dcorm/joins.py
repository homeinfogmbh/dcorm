"""Join types."""

from __future__ import annotations
from enum import Enum
from typing import NamedTuple, Optional, Union

from dcorm.alias import Alias
from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.model import Model


__all__ = ['JoinType', 'Join']


SQL = '{0} {1} {2} ON {3}'


class JoinType(Enum):
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


class Join(NamedTuple):
    """Represents a join between two tables."""

    lhs: Union[Alias, Model, Join]
    type: JoinType
    rhs: Union[Alias, Model]
    on: Optional[Expression] = None

    def join(self, other: Union[Alias, Model],
             typ: JoinType = JoinType.INNER,
             # pylint: disable-next=C0103
             on: Optional[Expression] = None) -> Join:
        """Returns a subsequent join."""
        return type(self)(self, typ, other, on)

    def __sql__(self, engine: Engine) -> Engine:
        engine.sql(self.lhs).literal(self.type).sql(self.rhs)

        if self.on is not None:
            engine.literal('ON').sql(self.on)

        return engine
