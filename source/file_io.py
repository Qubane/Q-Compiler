"""
File reading and writing implementations.
"""


from source.classes import *


def dump(data: list[InstructionN], file: str) -> int:
    """
    Dumps instruction data to a file
    :param data: instruction data
    :param file: dump filepath
    :return: amount of bytes that were written
    """
