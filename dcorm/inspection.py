"""Dataclass inspection."""

from dataclasses import Field as _Field
from typing import Any, Iterator, NamedTuple, Union

from dcorm.model import Model, ModelType


__all__ = ['NOT_SET', 'fields']


NOT_SET = object()


class Field(NamedTuple):
    """Represents a field bound to a model."""

    model: Model
    field: _Field
    value: Any = NOT_SET


def model_fields(model: ModelType) -> Iterator[Field]:
    """Yields fields from a model."""

    for field in model.__dataclass_fields__.values():
        yield Field(model, field)


def record_fields(record: Model) -> Iterator[Field]:
    """Yields fields from a record."""

    for attribute, field in record.__dataclass_fields__.items():
        yield Field(type(record), field, getattr(record, attribute, NOT_SET))


def fields(obj: Union[ModelType, Model]) -> Iterator[Field]:
    """Yields fields from the model."""

    if isinstance(obj, ModelType):
        return model_fields(obj)

    if isinstance(obj, Model):
        return record_fields(obj)

    raise TypeError(f'Cannot extract fields from {type(obj)}.')
