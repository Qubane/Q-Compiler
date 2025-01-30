"""
Build-in variables for Lexer type defining
"""


from source.classes import *


class Definition:
    """
    Container for TagType and opcode
    """

    def __init__(self, type_: TagType, opcode: int):
        self.type: TagType = type_
        self.opcode: int = opcode


class DefineNamespace:
    """
    Base class for definition namespaces
    """

    definitions: dict[str, Definition] = dict()


class CodeNamespace(DefineNamespace):
    """
    Namespace for code definitions
    """

    instruction_class = InstructionN


class NamespaceGeneral(DefineNamespace):
    """
    General built-ins, independent of CPU chosen to compile for
    """

    definitions: dict[str, Definition] = {
        "macro": Definition(TagType.BUILT_IN, -1),
        "subr": Definition(TagType.BUILT_IN, -1),
        "uses": Definition(TagType.BUILT_IN, -1),
    }

    number_prefixes: dict[str, int] = {
        "0b": 2,
        "0x": 16
    }


GeneralNamespace = NamespaceGeneral()


class NamespaceQMr11(CodeNamespace):
    """
    Quantum Mini rev. 1.1 built-ins
    """

    instruction_class = Instruction16
    definitions: dict[str, Definition] = {
        "NOP": Definition(TagType.BUILT_IN, 0),
        "LRA": Definition(TagType.BUILT_IN, 1),
        "SRA": Definition(TagType.BUILT_IN, 2),
        "CALL": Definition(TagType.BUILT_IN, 3),
        "RET": Definition(TagType.BUILT_IN, 4),
        "JMP": Definition(TagType.BUILT_IN, 5),
        "JMPP": Definition(TagType.BUILT_IN, 6),
        "JMPZ": Definition(TagType.BUILT_IN, 7),
        "JMPN": Definition(TagType.BUILT_IN, 8),
        "JMPC": Definition(TagType.BUILT_IN, 9),
        "CCF": Definition(TagType.BUILT_IN, 10),
        "LRP": Definition(TagType.BUILT_IN, 11),
        "CCP": Definition(TagType.BUILT_IN, 12),
        "CRP": Definition(TagType.BUILT_IN, 13),
        "PUSH": Definition(TagType.BUILT_IN, 14),
        "POP": Definition(TagType.BUILT_IN, 15),
        "AND": Definition(TagType.BUILT_IN, 16),
        "OR": Definition(TagType.BUILT_IN, 17),
        "XOR": Definition(TagType.BUILT_IN, 18),
        "NOT": Definition(TagType.BUILT_IN, 19),
        "LSC": Definition(TagType.BUILT_IN, 20),
        "RSC": Definition(TagType.BUILT_IN, 21),
        "CMP": Definition(TagType.BUILT_IN, 22),
        "CMPU": Definition(TagType.BUILT_IN, 23),
        "ADC": Definition(TagType.BUILT_IN, 32),
        "SBC": Definition(TagType.BUILT_IN, 33),
        "INC": Definition(TagType.BUILT_IN, 34),
        "DEC": Definition(TagType.BUILT_IN, 35),
        "ABS": Definition(TagType.BUILT_IN, 36),
        "MUL": Definition(TagType.BUILT_IN, 37),
        "DIV": Definition(TagType.BUILT_IN, 38),
        "MOD": Definition(TagType.BUILT_IN, 39),
        "TSE": Definition(TagType.BUILT_IN, 40),
        "TCE": Definition(TagType.BUILT_IN, 41),
        "ADD": Definition(TagType.BUILT_IN, 42),
        "SUB": Definition(TagType.BUILT_IN, 43),
        "RPL": Definition(TagType.BUILT_IN, 44),
        "MULH": Definition(TagType.BUILT_IN, 45),
        "UI": Definition(TagType.BUILT_IN, 48),
        "UO": Definition(TagType.BUILT_IN, 49),
        "UOC": Definition(TagType.BUILT_IN, 50),
        "UOCR": Definition(TagType.BUILT_IN, 51),
        "LRB": Definition(TagType.BUILT_IN, 52),
        "SRP": Definition(TagType.BUILT_IN, 53),
        "TAB": Definition(TagType.BUILT_IN, 54),
        "PRW": Definition(TagType.BUILT_IN, 112),
        "PRR": Definition(TagType.BUILT_IN, 113),
        "INT": Definition(TagType.BUILT_IN, 126),
        "HALT": Definition(TagType.BUILT_IN, 127),
    }


class NamespaceQT(CodeNamespace):
    """
    Quantum Tera (cutie :3) built-ins
    """

    instruction_class = Instruction24
    definitions: dict[str, Definition] = {
        "nop": Definition(TagType.BUILT_IN, 0),
        "load": Definition(TagType.BUILT_IN, 1),
        "store": Definition(TagType.BUILT_IN, 2),
        "loadp": Definition(TagType.BUILT_IN, 3),
        "loadpr": Definition(TagType.BUILT_IN, 4),
        "storep": Definition(TagType.BUILT_IN, 5),
        "push": Definition(TagType.BUILT_IN, 6),
        "pop": Definition(TagType.BUILT_IN, 7),
        "call": Definition(TagType.BUILT_IN, 8),
        "return": Definition(TagType.BUILT_IN, 9),
        "jump": Definition(TagType.BUILT_IN, 10),
        "jumpc": Definition(TagType.BUILT_IN, 11),
        "clf": Definition(TagType.BUILT_IN, 12),
        "and": Definition(TagType.BUILT_IN, 16),
        "or": Definition(TagType.BUILT_IN, 17),
        "xor": Definition(TagType.BUILT_IN, 18),
        "lsl": Definition(TagType.BUILT_IN, 19),
        "lsr": Definition(TagType.BUILT_IN, 20),
        "rol": Definition(TagType.BUILT_IN, 21),
        "ror": Definition(TagType.BUILT_IN, 22),
        "comp": Definition(TagType.BUILT_IN, 23),
        "add": Definition(TagType.BUILT_IN, 32),
        "sub": Definition(TagType.BUILT_IN, 33),
        "addc": Definition(TagType.BUILT_IN, 34),
        "subc": Definition(TagType.BUILT_IN, 35),
        "inc": Definition(TagType.BUILT_IN, 36),
        "dec": Definition(TagType.BUILT_IN, 37),
        "mul": Definition(TagType.BUILT_IN, 38),
        "div": Definition(TagType.BUILT_IN, 39),
        "mod": Definition(TagType.BUILT_IN, 40),
        "portw": Definition(TagType.BUILT_IN, 96),
        "portr": Definition(TagType.BUILT_IN, 97),
        "interupt": Definition(TagType.BUILT_IN, 126),
        "halt": Definition(TagType.BUILT_IN, 127),
    }
