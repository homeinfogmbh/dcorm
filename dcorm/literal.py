"""SQL literals."""

from typing import NamedTuple


__all__ = ['Literal', 'binary', 'unary']


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


def binary(keyword: str) -> Literal:
    """Return a literal for a binary operator."""

    return Literal(keyword, space_left=True, space_right=True)


def unary(keyword: str) -> Literal:
    """Return a literal for a unary operator."""

    return Literal(keyword, space_right=True)
