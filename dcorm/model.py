"""Model definition."""

from dataclasses import dataclass
from typing import Any, Optional

from dcorm.alias import Alias
from dcorm.column import Column
from dcorm.database import Database
from dcorm.engine import Engine
from dcorm.path import Path


__all__ = ['ModelType', 'Model']


class ModelType(type):
    """Metaclass for models."""

    @property
    def __schema__(cls) -> str:
        """Returns the database schema."""
        if (database :=  cls.__database__) is not None:
            return database

        return None

    @property
    def __table_path__(cls) -> Path:
        if cls.__schema__ is None:
            return Path(cls.__table_name__)

        return Path(cls.__schema__, cls.__table_name__)

    def __sql__(cls, engine: Engine) -> Engine:
        return engine.sql(cls.__table_path__)


class Model(metaclass=ModelType):
    """Model base class to inherit actual dataclass models from."""

    __database__ = None

    def __init_subclass__(
            cls, *,
            database: Optional[Database] = None,
            table_name: Optional[str] = None
        ):
        """Initialize the model with meta data."""
        dataclass(cls)

        if database is not None:
            cls.__database__ = database

        cls.__table_name__ = table_name or cls.__name__.lower()

        # pylint: disable-next=E1101
        for attribute, field in cls.__dataclass_fields__.items():
            setattr(cls, attribute, Column(cls, field))

    def __setattr__(self, attribute: str, value: Any) -> None:
        """Hook to set special field values."""
        try:
            # pylint: disable-next=E1101
            field = self.__dataclass_fields__[attribute]
        except KeyError:    # Not a field.
            return super().__setattr__(attribute, value)

        if (converter := field.metadata.get('converter')):
            value = converter(value)
        elif not isinstance(value, field.type):
            value = field.type(value)

        return super().__setattr__(attribute, value)

    @classmethod
    def alias(cls, name: Optional[str] = None) -> Alias:
        """Creates a model alias."""
        return Alias(cls, name)
