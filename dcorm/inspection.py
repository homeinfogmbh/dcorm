"""Dataclass inspection."""

from typing import Iterator, Union

from dcorm.alias import Alias
from dcorm.field import NOT_SET, Field
from dcorm.model import Model, ModelType


__all__ = ['fields']


def model_fields(model: ModelType) -> Iterator[Field]:
    """Yields fields from a model."""

    for field in model.__dataclass_fields__.values():
        yield Field(model, field)


def record_fields(record: Model) -> Iterator[Field]:
    """Yields fields from a record."""

    for attribute, field in record.__dataclass_fields__.items():
        yield Field(type(record), field, getattr(record, attribute, NOT_SET))


def fields(obj: Union[Alias, Model, ModelType]) -> Iterator[Field]:
    """Yields fields from the model."""

    if isinstance(obj, Model):
        return record_fields(obj)

    if isinstance(obj, (Alias, ModelType)):
        return model_fields(obj)

    raise TypeError(f'Cannot extract fields from {type(obj)}.')
