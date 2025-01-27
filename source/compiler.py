"""
Compiling code
"""


from source.classes import *
from source.built_ins import *


class Compiler:
    """
    Compiler class
    """

    code_namespace: CodeNamespace = NamespaceQT()

    def __init__(self):
        self.current_scope: Scope = Scope()

        self.bytecode: list[InstructionN] = list()
        self.pointers: list[Tag] = list()
        self.macros: dict[str, Scope] = dict()
        self.subroutines: dict[str, Scope] = dict()

    def import_scope(self, scope: Scope):
        """
        Imports parsed scope into compiler
        """

        self.current_scope = scope

    def _compile_first_stage(self):
        """
        First internal compilation stage.
        """

    def compile(self):
        """
        Compiles imported code
        """

        self._compile_first_stage()
