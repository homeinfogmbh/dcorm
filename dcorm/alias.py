"""Model aliases."""

from typing import Any, NamedTuple, Optional


__all__ = ['Alias']


class Alias(NamedTuple):
    """A model alias."""

    model: Any
    name: Optional[str] = None

    def __getattr__(self, attribute: str) -> Any:
        """Delegates to the underlying model."""
        return getattr(self.model, attribute)

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the alias."""
        return self.name