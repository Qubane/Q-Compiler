"""
Compiler classes
"""


from enum import StrEnum


class TagType(StrEnum):
    BUILT_IN = "built-in"
    POINTER = "pointer"
    NUMBER = "number"
