"""Database field types."""

from enum import Enum


__all__ = ['FieldType']


class FieldType(Enum):
    """Database field types."""

    AUTO = 'INTEGER'
    BIGAUTO = 'BIGINT'
    BIGINT = 'BIGINT'
    BLOB = 'BLOB'
    BOOL = 'BOOLEAN'
    CHAR = 'CHAR'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    DECIMAL = 'DECIMAL'
    DEFAULT = ''
    DOUBLE = 'REAL'
    FLOAT = 'REAL'
    INT = 'INTEGER'
    SMALLINT = 'SMALLINT'
    TEXT = 'TEXT'
    TIME = 'TIME'
    UUID = 'TEXT'
    UUIDB = 'BLOB'
    VARCHAR = 'VARCHAR'
