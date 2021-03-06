"""Join types."""

from __future__ import annotations
from enum import Enum
from typing import NamedTuple, Optional, Union

from dcorm.alias import Alias
from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.literal import binary
from dcorm.model import Model


__all__ = ['JoinType', 'Join']


ON = binary('ON')


class JoinType(Enum):
    """Available JOIN types."""

    INNER = binary('INNER JOIN')
    LEFT_OUTER = binary('LEFT OUTER JOIN')
    RIGHT_OUTER = binary('RIGHT OUTER JOIN')
    FULL = binary('FULL JOIN')
    FULL_OUTER = binary('FULL OUTER JOIN')
    CROSS = binary('CROSS JOIN')
    NATURAL = binary('NATURAL JOIN')
    LATERAL = binary('LATERAL')
    LEFT_LATERAL = binary('LEFT JOIN LATERAL')


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
            engine.literal(ON).sql(self.on)

        return engine
