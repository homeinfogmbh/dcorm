"""SQL statement nodes."""

from dcorm.engine import Engine


__all__ = ['Path']


class Path(list):
    """A model or field path."""

    def __init__(self, *items: str):
        super().__init__(items)

    @property
    def template(self) -> str:
        """Returns the template string."""
        return '.'.join(['%s'] *  len(self))

    def __sql__(self, engine: Engine) -> Engine:
        sql = f'{engine.quote(self.template)}'
        engine._sql.append(sql)         # pylint: disable=W0212
        engine._values.extend(self)     # pylint: disable=W0212
        return engine
