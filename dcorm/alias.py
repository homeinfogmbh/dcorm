"""Model aliases."""

from typing import Any, Iterable, NamedTuple, Optional


__all__ = ['Alias', 'AliasManager']


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


class AliasManager:
    """Context manager to handle aliases."""

    def __init__(self):
        super().__init__()
        self.aliases = {}

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.aliases.clear()

    def get_unique_alias(self) -> str:
        """Generates a unique alias."""
        counter = 1

        while (name := f't{counter}') in self.aliases:
            counter += 1

        return name

    def get_alias_name(self, alias: Alias) -> str:
        """Returns an alias name."""
        if alias.name is None:
            return self.get_unique_alias()

        return alias.name

    def register_alias(self, alias: Alias) -> None:
        """Registers an alias."""
        if (name := self.get_alias_name(alias)) in self.aliases:
            raise RuntimeError(f'Duplicate alias: {name}')

        self.aliases[name] = alias

    def register_aliases(self, aliases: Iterable[Alias]) -> None:
        """Sets the aliases."""
        for alias in aliases:
            self.register_alias(alias)
