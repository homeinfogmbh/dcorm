"""Query operators."""

from enum import Enum


__all__ = ['Operator']


class Operator(Enum):
    """Query operators."""

    AND = 'AND'
    OR = 'OR'
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    BIN_AND = '&'
    BIN_OR = '|'
    XOR = '#'
    MOD = '%'
    EQ = '='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    NE = '!='
    IN = 'IN'
    NOT_IN = 'NOT IN'
    IS = 'IS'
    IS_NOT = 'IS NOT'
    LIKE = 'LIKE'
    ILIKE = 'ILIKE'
    BETWEEN = 'BETWEEN'
    REGEXP = 'REGEXP'
    IREGEXP = 'IREGEXP'
    CONCAT = '||'
    BITWISE_NEGATION = '~'

    @property
    def __sql__(self) -> str:
        """Returns the SQL representation of the operator."""
        return self.value
