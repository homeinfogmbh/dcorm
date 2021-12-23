"""SQL literals."""

from typing import NamedTuple


__all__ = ['Literal']


class Literal(NamedTuple):
    """An SQL literal."""

    value: str
    space_left: bool = False
    space_right: bool = False

    def __str__(self):
        if self.space_left:
            if self.space_right:
                return f' {self.value} '

            return f' {self.value}'

        if self.space_right:
            return f'{self.value} '

        return self.value
