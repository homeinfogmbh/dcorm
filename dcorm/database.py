"""Database definitions."""

from dcorm.engine import Engine


__all__ = ['Database']


class Database:     # pylint: disable=R0903
    """Base class for databases."""

    def __init_subclass__(cls, *, engine: Engine):
        """Sets the database engine."""
        cls.engine = engine
