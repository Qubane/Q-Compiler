"""
File reading and writing implementations.
"""


from source.classes import *
from source.built_ins import *


def dump(data: list[InstructionN], file: str, namespace: CodeNamespace) -> int:
    """
    Dumps instruction data to a file
    :param data: instruction data
    :param file: dump filepath
    :param namespace: used instruction namespace
    :return: amount of bytes that were written
    """

    if isinstance(namespace, NamespaceQT):
        used_namespace = "QT"
    elif isinstance(namespace, NamespaceQMr11):
        used_namespace = "QM"
    else:
        raise Exception

    with open(file, "wb") as f:
        f.write(used_namespace.encode("ascii") + b'\x00')  # add small architecture header
        for instruction in data:
            f.write(instruction.__bytes__())
        return f.tell()
