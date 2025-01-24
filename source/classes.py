"""
Compiler classes
"""


from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class TagType(StrEnum):
    BUILT_IN = "built-in"
    POINTER = "pointer"
    NUMBER = "number"

    def __repr__(self):
        return self.value


@dataclass
class Tag:
    """
    TagType - value pair
    """

    type: TagType
    value: Any | None = None


class Word:
    """
    Instruction word
    """

    def __init__(self, tags: list[Tag]):
        self.tags: list[Tag] = tags


class Scope:
    """
    Scope of instruction words
    """

    def __init__(self, words: list[Word]):
        self.words: list[Word] = words


class MacroScope(Scope):
    """
    Special type of scope used for macros
    """


class SubroutineScope(Scope):
    """
    Special type of scope used for subroutines
    """


class GlobalScope(Scope):
    """
    Global scope
    """
