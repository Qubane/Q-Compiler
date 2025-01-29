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

        self.instructions: list[TaggedInstruction | Tag] = list()

        self.pointers: dict[str, Tag] = dict()
        self.pointer_counter: int = -1

        self.macros: dict[str, Scope] = dict()
        self.subroutines: dict[str, Scope] = dict()

    def import_scope(self, scope: Scope):
        """
        Imports parsed scope into compiler
        """

        self.current_scope = scope

    def _generate_macro_scope(self, index: int, name: str, args: list[Tag]):
        """
        Insert a macro at a given index
        """

        macro = self.macros[name].__copy__()

        # macro with multiple args
        if len(macro[0]) > 2:
            # translation dictionary
            for old, new in zip(macro[0][3:], args):
                self._match_and_replace(macro[1], old, new)
        return macro[1]

    def _match_and_replace(self, scope: Scope, old: Tag, new: Tag):
        """
        Match and replace all tags within scope from old to new
        """

        for word in scope:
            if isinstance(word, Word):
                for idx, tag in enumerate(word):
                    if tag == old:
                        word[idx] = new
            else:
                self._match_and_replace(word, old, new)

    def _compile_first_stage(self):
        """
        First internal compilation stage.

        Finds all subroutine and macros definitions
        """

        idx = -1
        while idx < len(self.current_scope) - 1:
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

    def _compile_second_stage(self):
        """
        Second internal compilation stage.
        """

        idx = -1
        while idx < len(self.current_scope) - 1:
            idx += 1
            word = self.current_scope[idx]

            # instructions with arguments
            if word[0].value in self.code_namespace.definitions and len(word) == 2:
                memory_flag = word[1].type is TagType.POINTER
                if memory_flag:
                    if word[1].value in self.pointers:
                        instruction_value = self.pointers[word[1].value]
                    elif word[1].value in self.subroutines:
                        self.pointers[word[1].value] = Tag(self.subroutines[word[1].value], TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]
                    elif word[1].value in self.macros:
                        raise CompilerNotImplementedError(line=word.line)
                    else:
                        self.pointer_counter += 1
                        self.pointers[word[1].value] = Tag(self.pointer_counter, TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]
                else:
                    instruction_value = word[1]
                self.instructions.append(TaggedInstruction(
                    flag=memory_flag,
                    value=instruction_value,
                    opcode=word[0]))

            # instructions without arguments
            elif word[0].value in self.code_namespace.definitions and len(word) == 1:
                self.instructions.append(TaggedInstruction(
                    flag=False,
                    value=Tag(0, TagType.NUMBER),
                    opcode=word[0]))

            # macros
            elif word[0].type is TagType.POINTER and word[0].value in self.macros:
                self.current_scope.pop(idx)
                scope = self._generate_macro_scope(idx, word[0].value, word[2:])
                for word in scope[::-1]:
                    self.current_scope.insert(idx, word)
                idx -= 1

    def compile(self):
        """
        Compiles imported code
        """

        self._compile_first_stage()

        for val in self.subroutines.values():
            recursive_scope_print(val)
        for val in self.macros.values():
            recursive_scope_print(val)

        self._compile_second_stage()
