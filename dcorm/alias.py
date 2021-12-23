"""Model aliases."""

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from dcorm.field import Field
from dcorm import sql


__all__ = ['Alias', 'AliasManager']


@dataclass
class Alias:
    """A model alias."""

    model: Any
    name: Optional[str] = None

    def __getattr__(self, attribute: str) -> Any:
        """Delegates to the underlying model."""
        if isinstance(value := getattr(self.model, attribute), Field):
            return Field(self, value.field, value.value)

        if isinstance(value, type(self)):
            value.model = self.model

        return value

    @property
    def __namespace__(self) -> str:
        """Returns the alias name."""
        return self.name

    @property
    def __sql__(self) -> str:
        """Returns an SQL representation of the alias."""
        if self.name is None:
            raise RuntimeError('Alias name not set:', self)

        return f'{sql(self.model)} AS `{self.name}`'


class AliasManager:
    """Context manager to handle aliases."""

    def __init__(self):
        super().__init__()
        self.aliases = {}

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.aliases.clear()

    def get_unique_alias(self, alias: Alias) -> str:
        """Generates a unique alias."""
        counter = 1

        while (name := f't{counter}') in self.aliases:
            counter += 1

        alias.name = name
        return name

    def get_alias_name(self, alias: Alias) -> str:
        """Returns an alias name."""
        if alias.name is None:
            return self.get_unique_alias(alias)

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
