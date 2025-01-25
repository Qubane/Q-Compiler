"""
Build-in variables for Lexer type defining
"""


from source.classes import *


class General:
    """
    General built-ins, independent of CPU chosen to compile for
    """

    definitions: dict[str, TagType] = {
        "macro": TagType.BUILT_IN,
        "subr": TagType.BUILT_IN,
        "uses": TagType.BUILT_IN,
    }


class QMr11:
    """
    Quantum Mini rev. 1.1 built-ins
    """


class QMr2:
    """
    Quantum Mini rev. 2 built-ins
    """
