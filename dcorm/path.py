"""SQL statement nodes."""

from dcorm.engine import Engine
from dcorm.literal import Literal


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
        engine.literal(Literal(f'{engine.quote(self.template)}'))

        for value in self:
            engine.value(value, raw=True)

        return engine
