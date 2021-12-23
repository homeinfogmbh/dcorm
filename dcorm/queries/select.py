"""Select queries."""

from __future__ import annotations
from typing import Iterator, Optional, Union
from warnings import warn

from dcorm.alias import Alias, AliasManager
from dcorm.database import Database
from dcorm.expression import Expression
from dcorm.field import Field, OrderedField
from dcorm.inspection import fields
from dcorm.joins import Join, JoinType
from dcorm.model import ModelType
from dcorm.operations import Operation
from dcorm.queries.query import Query
from dcorm.relations import find_relation
from dcorm.sql import sql


__all__ = ['select']


SelectItem = Union[Alias, ModelType, Field]


def extract_fields(item: SelectItem) -> Iterator[Field]:
    """Adds an item to the selections."""

    if isinstance(item, Field):
        yield item
        return

    if isinstance(item, (Alias, ModelType)):
        yield from fields(item)
        return

    raise TypeError(f'Cannot select {type(item)},')


class SelectQuery(Query):
    """A SELECT query."""

    def __init__(self, first: SelectItem, *other: SelectItem):
        """Returns a selection proxy object."""
        super().__init__(Operation.SELECT)
        self._items = [first, *other]

        if isinstance(first, Field):
            self._from = first.table
        else:
            self._from = first

        self._order_by: list[OrderedField] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._alias_manager: AliasManager = AliasManager()

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the query."""
        query = sql(self._operation)
        fields_ = ', '.join(sql(field) for field in self._fields)
        from_ = sql(self._from)
        where = sql(self._where)
        return ' '.join([query, fields_, from_, where])

    @property
    def _fields(self) -> Iterator[Field]:
        """Filters out the selected fields."""
        for item in self._items:
            yield from extract_fields(item)

    @property
    def _aliases(self) -> Iterator[Alias]:
        """Filters out the used aliases."""
        return filter(lambda item: isinstance(item, Alias), self._items)

    def join(self, other: Union[Alias, ModelType],
             typ: JoinType = JoinType.INNER,
             # pylint: disable-next=C0103
             on: Optional[Expression] = None) -> Query:
        """Updates the join."""
        if on is None:
            on = find_relation(self._from, other)

        self._from = Join(self._from, typ, other, on)
        return self

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

    def execute(self, database: Optional[Database] = None):
        """Executes the query."""
        with self._alias_manager as manager:
            manager.register_aliases(self._aliases)
            return super().execute(database=database)


def select(*items: SelectItem) -> SelectQuery:
    """Creates a select quers."""

    return SelectQuery(*items)
