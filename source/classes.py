"""
Compiler classes
"""


from typing import Any
from enum import StrEnum
from dataclasses import dataclass
from source.exceptions import *


class TagType(StrEnum):
    UNDEFINED = "undefined"
    INTERNAL = "internal"
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

    value: Any | None = None
    type: TagType = TagType.UNDEFINED


class Word:
    """
    Instruction word
    """

    def __init__(self, tags: list[Tag] | None = None):
        self.tags: list[Tag] = tags if tags is not None else list()
        self.line: int = -1

    def __iter__(self):
        return self.tags.__iter__()

    def __len__(self):
        return len(self.tags)

    def __getitem__(self, item):
        return self.tags.__getitem__(item)

    def __repr__(self):
        return " ".join(f"[{tag.value}]" for tag in self.tags)

    def add(self, tag: Tag):
        """
        Adds a tag to word
        """

        if isinstance(tag, Tag):
            self.tags.append(tag)
        else:
            raise CompilerError("Attempted to append wrong type to word")

    def pop(self, index: int):
        return self.tags.pop(index)


class Scope:
    """
    Scope of instruction words
    """

    def __init__(self, words: list | None = None):
        self.words: list[Word | Scope] = words if words is not None else list()

    def __iter__(self):
        return self.words.__iter__()

    def __getitem__(self, item):
        return self.words.__getitem__(item)

    def __len__(self):
        return len(self.words)

    def add(self, word: Word | Any):
        """
        Adds a word / scope to scope
        """

        if isinstance(word, (Word, Scope)):
            self.words.append(word)
        else:
            raise CompilerError("Attempted to append wrong type to scope")

    def pop(self, index: int):
        return self.words.pop(index)

    def insert(self, index: int, item: Any):
        self.words.insert(index, item)


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
