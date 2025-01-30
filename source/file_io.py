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

    if isinstance(InstructionN, Instruction16):
        architecture = "QM"
    elif isinstance(InstructionN, Instruction24):
        architecture = "QT"
    else:
        raise Exception

    with open(file, "wb") as f:
        f.write(f"{architecture: >8}".encode("ascii"))  # add small architecture header
        for instruction in data:
            f.write(instruction.__bytes__())
    return f.tell()
