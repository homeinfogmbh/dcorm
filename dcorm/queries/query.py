"""Basic SQL queries."""

from __future__ import annotations
from typing import Any, Optional, Union

from dcorm.database import Database
from dcorm.expression import Expression
from dcorm.operations import Operation


__all__ = ['Query']


class Query:    # pylint: disable=R0903
    """An SQL query."""

    def __init__(self, operation: Operation):
        self._operation: Operation = operation
        self._where: Union[Expression, bool] = True

    def where(self, expression: Union[Expression, bool]) -> Query:
        """Updates the where clause."""
        self._where &= expression
        return self

    def execute(self, database: Optional[Database] = None) -> Any:
        """Executes the query."""
        raise NotImplementedError()
