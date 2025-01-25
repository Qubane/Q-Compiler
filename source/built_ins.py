"""
Build-in variables for Lexer type defining
"""


from source.classes import *


class DefineNamespace:
    """
    Base class for definition namespaces
    """

    definitions: dict[str, TagType] = dict()

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self.definitions
        return False

    def __getitem__(self, item):
        return self.definitions.__getitem__(item)


class CodeNamespace(DefineNamespace):
    """
    Namespace for code definitions
    """


class NamespaceGeneral(DefineNamespace):
    """
    General built-ins, independent of CPU chosen to compile for
    """

    definitions: dict[str, TagType] = {
        "macro": TagType.BUILT_IN,
        "subr": TagType.BUILT_IN,
        "uses": TagType.BUILT_IN,
    }

    number_prefixes: set[str] = {"0b", "0x"}


GeneralNamespace = NamespaceGeneral()


class NamespaceQMr11(CodeNamespace):
    """
    Quantum Mini rev. 1.1 built-ins
    """

    definitions: dict[str, TagType] = {
        "NOP": TagType.BUILT_IN,
        "LRA": TagType.BUILT_IN,
        "SRA": TagType.BUILT_IN,
        "CALL": TagType.BUILT_IN,
        "RET": TagType.BUILT_IN,
        "JMP": TagType.BUILT_IN,
        "JMPP": TagType.BUILT_IN,
        "JMPZ": TagType.BUILT_IN,
        "JMPN": TagType.BUILT_IN,
        "JMPC": TagType.BUILT_IN,
        "CCF": TagType.BUILT_IN,
        "LRP": TagType.BUILT_IN,
        "CCP": TagType.BUILT_IN,
        "CRP": TagType.BUILT_IN,
        "PUSH": TagType.BUILT_IN,
        "POP": TagType.BUILT_IN,
        "AND": TagType.BUILT_IN,
        "OR": TagType.BUILT_IN,
        "XOR": TagType.BUILT_IN,
        "NOT": TagType.BUILT_IN,
        "LSC": TagType.BUILT_IN,
        "RSC": TagType.BUILT_IN,
        "CMP": TagType.BUILT_IN,
        "CMPU": TagType.BUILT_IN,
        "ADC": TagType.BUILT_IN,
        "SBC": TagType.BUILT_IN,
        "INC": TagType.BUILT_IN,
        "DEC": TagType.BUILT_IN,
        "ABS": TagType.BUILT_IN,
        "MUL": TagType.BUILT_IN,
        "DIV": TagType.BUILT_IN,
        "MOD": TagType.BUILT_IN,
        "TSE": TagType.BUILT_IN,
        "TCE": TagType.BUILT_IN,
        "ADD": TagType.BUILT_IN,
        "SUB": TagType.BUILT_IN,
        "RPL": TagType.BUILT_IN,
        "MULH": TagType.BUILT_IN,
        "UI": TagType.BUILT_IN,
        "UO": TagType.BUILT_IN,
        "UOC": TagType.BUILT_IN,
        "UOCR": TagType.BUILT_IN,
        "LRB": TagType.BUILT_IN,
        "SRP": TagType.BUILT_IN,
        "TAB": TagType.BUILT_IN,
        "PRW": TagType.BUILT_IN,
        "PRR": TagType.BUILT_IN,
        "INT": TagType.BUILT_IN,
        "HALT": TagType.BUILT_IN,
    }


class NamespaceQT(CodeNamespace):
    """
    Quantum Tera (cutie :3) built-ins
    """

    definitions: dict[str, TagType] = {
        "nop": TagType.BUILT_IN,
        "load": TagType.BUILT_IN,
        "store": TagType.BUILT_IN,
        "loadp": TagType.BUILT_IN,
        "loadpr": TagType.BUILT_IN,
        "storep": TagType.BUILT_IN,
        "push": TagType.BUILT_IN,
        "pop": TagType.BUILT_IN,
        "call": TagType.BUILT_IN,
        "return": TagType.BUILT_IN,
        "jump": TagType.BUILT_IN,
        "jumpc": TagType.BUILT_IN,
        "clf": TagType.BUILT_IN,
        "and": TagType.BUILT_IN,
        "or": TagType.BUILT_IN,
        "xor": TagType.BUILT_IN,
        "lsl": TagType.BUILT_IN,
        "lsr": TagType.BUILT_IN,
        "rol": TagType.BUILT_IN,
        "ror": TagType.BUILT_IN,
        "comp": TagType.BUILT_IN,
        "add": TagType.BUILT_IN,
        "sub": TagType.BUILT_IN,
        "addc": TagType.BUILT_IN,
        "subc": TagType.BUILT_IN,
        "inc": TagType.BUILT_IN,
        "dec": TagType.BUILT_IN,
        "mul": TagType.BUILT_IN,
        "div": TagType.BUILT_IN,
        "mod": TagType.BUILT_IN,
        "portw": TagType.BUILT_IN,
        "portr": TagType.BUILT_IN,
        "interupt": TagType.BUILT_IN,
        "halt": TagType.BUILT_IN,
    }
