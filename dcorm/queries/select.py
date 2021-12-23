"""Select queries."""

from __future__ import annotations
from itertools import chain
from typing import Iterator, Optional, Union
from warnings import warn

from dcorm.field import Field, OrderedField
from dcorm.inspection import fields
from dcorm.model import Model
from dcorm.operations import Operation
from dcorm.queries.query import Query


__all__ = ['Query']


SelectItem = Union[Model, Field]


def extract_fields(item: SelectItem) -> Iterator[Field]:
    """Adds an item to the selections."""

    if isinstance(item, Field):
        yield item
        return

    if isinstance(item, Model):
        yield from fields(item)
        return

    raise TypeError(f'Cannot select {type(item)},')


class SelectQuery(Query):
    """A SELECT query."""

    def __init__(self, *items: SelectItem):
        """Returns a selection proxy object."""
        super().__init__(Operation.SELECT)
        self._select = list(chain(extract_fields(item) for item in items))
        self._order_by: list[OrderedField] = []
        self._limit: Optional[int] = None
        self._offset: []

    def order_by(self, *items: Union[Field, OrderedField]) -> SelectQuery:
        """Updates the order-by clause."""
        if ordering := self._order_by:
            warn(f'Overriding previous ordering of {ordering}')

        self._order_by = [
            item.asc() if isinstance(item, Field) else item
            for item in items
        ]
        return self

    def limit(self, limit: int) -> SelectQuery:
        """Updates the limit."""
        if (previous := self._limit) is not None:
            warn(f'Overriding previous limit of {previous}')

        self._limit = limit

    def offset(self, offset: int) -> SelectQuery:
        """Sets the offset."""
        if (previous := self._offset) is not None:
            warn(f'Overriding previous offset of {previous}')

        self._offset = offset
