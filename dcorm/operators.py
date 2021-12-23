"""Query operators."""

from enum import Enum

from dcorm.literal import Literal


__all__ = ['Operator']


def unary(keyword: str) -> Literal:
    """Return a literal for a unary operator."""

    return Literal(keyword, space_right=True)


def binary(keyword: str) -> Literal:
    """Return a literal for a binary operator."""

    return Literal(keyword, space_left=True, space_right=True)


class Operator(Enum):
    """Query operators."""

    NOT = unary('NOT')
    AND = binary('AND')
    OR = binary('OR')
    ADD = binary('+')
    SUB = binary('-')
    MUL = binary('*')
    DIV = binary('/')
    BIN_AND = binary('&')
    BIN_OR = binary('|')
    XOR = binary('#')
    MOD = binary('%')
    EQ = binary('=')
    LT = binary('<')
    LE = binary('<=')
    GT = binary('>')
    GE = binary('>=')
    NE = binary('!=')
    IN = binary('IN')
    NOT_IN = binary('NOT IN')
    IS = binary('IS')
    IS_NOT = binary('IS NOT')
    LIKE = binary('LIKE')
    ILIKE = binary('ILIKE')
    #BETWEEN = 'BETWEEN'    # Trinary!
    #REGEXP = 'REGEXP'      # How is this used?
    #IREGEXP = 'IREGEXP'
    CONCAT = binary('||')
    BITWISE_NEGATION = unary('~')
