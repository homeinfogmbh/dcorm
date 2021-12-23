"""Relations management."""

from typing import Union

from dcorm.alias import Alias
from dcorm.expression import Expression
from dcorm.model import Model


__all__ = ['find_relation']


RelationType = Union[Alias, Model]


def find_relation(lhs: RelationType, rhs: RelationType) -> Expression:
    """Returns a relation between the given models or aliases."""

    raise NotImplementedError()
