"""Model definition."""

from dataclasses import dataclass
from typing import Any, Optional

from dcorm.alias import Alias
from dcorm.database import Database
from dcorm.field import Field
from dcorm.sql import Engine, TableIdentifier


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
    def __table_identifier__(cls) -> TableIdentifier:
        if cls.__schema__ is None:
            return TableIdentifier(cls.__table_name__)

        return TableIdentifier(cls.__schema__, cls.__table_name__)

    def __sql__(cls, engine: Engine) -> Engine:
        return engine.sql(cls.__table_identifier__)


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
            setattr(cls, attribute, Field(cls, field))

    def __setattr__(self, attribute: str, value: Any) -> None:
        """Hook to set special field values."""
        field = self.__dataclass_fields__[attribute]    # pylint: disable=E1101

        if (converter := field.metadata.get('converter')):
            value = converter(value)
        elif not isinstance(value, field.type):
            value = field.type(value)

        super().__setattr__(attribute, value)

    @classmethod
    def alias(cls, name: Optional[str] = None) -> Alias:
        """Creates a model alias."""
        return Alias(cls, name)
