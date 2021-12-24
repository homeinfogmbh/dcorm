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
        return engine.raw_value(f'{engine.quote(self.template)}', self)
