"""Dataclass inspection."""

from typing import Iterator, Union

from dcorm.alias import Alias
from dcorm.column import NOT_SET, Column
from dcorm.model import Model, ModelType


__all__ = ['columns']


def model_columns(model: ModelType) -> Iterator[Column]:
    """Yields columns from a model."""

    for field in model.__dataclass_fields__.values():
        yield Column(model, field)


def record_columns(record: Model) -> Iterator[Column]:
    """Yields columns from a record."""

    for attribute, field in record.__dataclass_fields__.items():
        yield Column(type(record), field, getattr(record, attribute, NOT_SET))


def columns(obj: Union[Alias, Model, ModelType]) -> Iterator[Column]:
    """Yields columns from the model."""

    if isinstance(obj, Model):
        return record_columns(obj)

    if isinstance(obj, (Alias, ModelType)):
        return model_columns(obj)

    raise TypeError(f'Cannot extract columns from {type(obj)}.')
