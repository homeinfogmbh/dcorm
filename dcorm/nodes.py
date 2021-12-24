"""SQL statement nodes."""


__all__ = ['FieldIdentifier', 'TableIdentifier']


class FieldIdentifier(list):
    """A field identifier."""

    def __init__(self, *path: str):
        super().__init__(path)


class TableIdentifier(list):
    """A table identifier."""

    def __init__(self, *path: str):
        super().__init__(path)

    def field(self, name: str) -> FieldIdentifier:
        """Returns a field identifier from the table identifier."""
        return FieldIdentifier(*self, name)
