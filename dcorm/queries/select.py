"""Select queries."""

from __future__ import annotations
from typing import Iterator, Optional, Union
from warnings import warn

from dcorm.alias import Alias, AliasManager
from dcorm.column import Column, ColumnSelect, OrderedColumn
from dcorm.database import Database
from dcorm.engine import Engine
from dcorm.expression import Expression
from dcorm.inspection import columns
from dcorm.joins import Join, JoinType
from dcorm.literal import binary
from dcorm.model import ModelType
from dcorm.operations import Operation
from dcorm.queries.query import Query
from dcorm.relations import find_relation


__all__ = ['select']


SelectItem = Union[Alias, ModelType, Column]
FROM = binary('FROM')
WHERE = binary('WHERE')


def extract_columns(item: SelectItem) -> Iterator[Column]:
    """Extract columns from the given item."""

    if isinstance(item, Column):
        yield item
        return

    if isinstance(item, (Alias, ModelType)):
        yield from columns(item)
        return

    raise TypeError(f'Cannot extract columns from {type(item)}.')


class SelectQuery(Query):
    """A SELECT query."""

    def __init__(self, first: SelectItem, *other: SelectItem):
        """Returns a selection proxy object."""
        super().__init__(Operation.SELECT)
        self._items = [first, *other]

        if isinstance(first, Column):
            self._from = first.table
        else:
            self._from = first

        self._order_by: list[OrderedColumn] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._alias_manager: AliasManager = AliasManager()

    def __sql__(self, engine: Engine) -> Engine:
        return engine.literal(self._operation).sql(
            ColumnSelect(*self._columns)).literal(FROM).sql(
            self._from).literal(WHERE).sql(self._where)

    @property
    def _columns(self) -> Iterator[Column]:
        """Filters out the selected fields."""
        for item in self._items:
            yield from extract_columns(item)

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

    def order_by(self, *items: Union[Column, OrderedColumn]) -> SelectQuery:
        """Updates the order-by clause."""
        if ordering := self._order_by:
            warn(f'Overriding previous ordering of {ordering}')

        self._order_by = [
            item.asc() if isinstance(item, Column) else item
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
