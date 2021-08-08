from pyparsing import Word, alphas, Optional, Suppress, ZeroOrMore, oneOf, Combine, printables, nums
import re


class FindSP:
    FIND_START = re.compile('^CREATE.*PROC|^ALTER.*PROC', re.IGNORECASE)
    FIND_END = re.compile(r'^AS|^BEGIN|^\)', re.IGNORECASE)
    CLEAR_TRASH = re.compile(r'[\[\]/\\*]')
    VARIABLE_START_WITH = '@'


class GetAttrs:
    FIND_NAME = Optional(
        Suppress('ALTER')
    ) + Optional(
        Word(alphas) + Suppress(Optional('.')) + Optional(Word(printables))
    )

    FIND_ATTRS = Optional(
        Suppress(',')
    ) + Optional(
        Suppress('(')
    ) + Optional(
        Suppress(')')
    ) + Optional(
        Combine('@' + ZeroOrMore(Word(printables)))
    ) + Optional(
        ZeroOrMore(
            Word(''.join(c for c in printables if c != '-'))
        )
    ) + Optional('=') + Optional(
        Word(alphas + nums)
    ) + Optional(Suppress(','))
