"""
Compiler classes
"""


from typing import Any
from enum import StrEnum
from dataclasses import dataclass, replace
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

    def __init__(self, tags: list[Tag] | None = None, line: int = -1):
        self.tags: list[Tag] = tags if tags is not None else list()
        self.line: int = line

    def __copy__(self):
        return self.__class__([replace(tag) for tag in self.tags], self.line)

    def __iter__(self):
        return self.tags.__iter__()

    def __len__(self):
        return len(self.tags)

    def __getitem__(self, item):
        return self.tags.__getitem__(item)

    def __setitem__(self, key, value):
        return self.tags.__setitem__(key, value)

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

    def insert(self, index: int, item: Any):
        self.tags.insert(index, item)


class Scope:
    """
    Scope of instruction words
    """

    def __init__(self, words: list | None = None):
        self.words: list[Word | Scope] = words if words is not None else list()

    def __copy__(self):
        return self.__class__([word.__copy__() for word in self.words])

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


def recursive_scope_print(scope: Scope, level: int = 0):
    """
    Recursively prints scopes and scopes within scopes
    """

    for word in scope:
        if isinstance(word, Scope):
            recursive_scope_print(word, level + 1)
            continue
        print("  " * level, f"{word.line: <3}", " ".join(f"[{tag.value: >12} {tag.type: <9}]" for tag in word))


class TaggedInstruction:
    """
    Like instruction, except it uses tags
    """

    def __init__(self, flag: bool, value: Tag, opcode: Tag):
        self.flag: bool = flag
        self.value: Tag = value
        self.opcode: Tag = opcode

    def __repr__(self):
        return f"{'1' if self.flag else '0'} {self.value.__repr__(): <32} {self.opcode.__repr__(): <32}"


class InstructionN:
    """
    Base class for Quantum architecture
    """

    def __init__(self, flag: bool, value: int, opcode: int):
        self.flag: bool = flag
        self.value: int = value
        self.opcode: int = opcode

    def __repr__(self):
        return f"{'1' if self.flag else '0'} {str(self.value): <3} {self.opcode: <3}"

    def __bytes__(self):
        return self.flag.to_bytes(1) + self.value.to_bytes(4) + self.value.to_bytes(1)


class Instruction16(InstructionN):
    """
    16 bit instruction for MQ cpu's
    """

    def __init__(self, flag: bool, value: int, opcode: int):
        super().__init__(
            flag,
            value & 0b1111_1111,
            opcode & 0b111_1111)

    def __repr__(self):
        return f"{'1' if self.flag else '0'} {bin(self.value)[2:]:0>8} {bin(self.opcode)[2:]:0>7}"

    def __bytes__(self):
        return self.flag.to_bytes(1) + self.value.to_bytes(1) + self.value.to_bytes(1)


class Instruction24(InstructionN):
    """
    24 bit instruction for QT cpu's
    """

    def __init__(self, flag: bool, value: int, opcode: int):
        super().__init__(
            flag,
            value & 0b1111_1111_1111_1111,
            opcode & 0b111_1111)

    def __repr__(self):
        return f"{'1' if self.flag else '0'} {bin(self.value)[2:]:0>16} {bin(self.opcode)[2:]:0>7}"

    def __bytes__(self):
        return self.flag.to_bytes(1) + self.value.to_bytes(2) + self.value.to_bytes(1)
