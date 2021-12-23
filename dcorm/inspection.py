"""Dataclass inspection."""

from dataclasses import MISSING
from typing import Iterator, Union

from dcorm.field import Field
from dcorm.model import Model, ModelType


__all__ = ['fields']


def model_fields(model: ModelType) -> Iterator[Field]:
    """Yields fields from a model."""

    for field in model.__dataclass_fields__.values():
        yield Field(model, field)


def record_fields(record: Model) -> Iterator[Field]:
    """Yields fields from a record."""

    for attribute, field in record.__dataclass_fields__.items():
        yield Field(type(record), field, getattr(record, attribute, MISSING))


def fields(obj: Union[ModelType, Model]) -> Iterator[Field]:
    """Yields fields from the model."""

    if isinstance(obj, ModelType):
        return model_fields(obj)

    if isinstance(obj, Model):
        return record_fields(obj)

    raise TypeError(f'Cannot extract fields from {type(obj)}.')
