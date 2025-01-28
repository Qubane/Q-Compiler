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

        Finds all subroutine and macros definitions
        """

        idx = -1
        while idx < len(self.current_scope)-1:
            idx += 1
            word = self.current_scope[idx]

            if word[0].value == "macro":
                self.macros[word[1].value] = MacroScope([
                    self.current_scope.pop(idx),
                    self.current_scope.pop(idx)])
                idx -= 1
            elif word[0].value == "subr":
                self.subroutines[word[1].value] = SubroutineScope([
                    self.current_scope.pop(idx),
                    self.current_scope.pop(idx)])
                idx -= 1

    def compile(self):
        """
        Compiles imported code
        """

        self._compile_first_stage()
