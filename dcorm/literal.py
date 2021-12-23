"""SQL literals."""

from typing import NamedTuple


__all__ = ['Literal']


class Literal(NamedTuple):
    """An SQL literal."""

    keyword: str
    space_left: bool = False
    space_right: bool = False

    def __str__(self):
        if self.space_left:
            if self.space_right:
                return f' {self.keyword} '

            return f' {self.keyword}'

        if self.space_right:
            return f'{self.keyword} '

        return self.keyword
