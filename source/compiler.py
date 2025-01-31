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
        self.instructions: list[TaggedInstruction] = list()

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

    @staticmethod
    def _convert_tagged2byte(instruction: TaggedInstruction, namespace: CodeNamespace) -> InstructionN:
        """
        Converts 'instruction' to bytecode restricted instruction
        """

        return InstructionN(
            flag=instruction.flag,
            value=int(instruction.value.value),  # make sure it's int
            opcode=namespace.definitions[instruction.opcode.value].opcode)

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

        Compiles words into TaggedInstructions.
        Grants address values to variable pointers.
        Grants scope references to subroutine pointers.
        Inserts macro code into current scope for processing.
        """

        while len(self.current_scope):
            word = self.current_scope.pop(0)

            # instructions with arguments
            if word[0].value in self.code_namespace.definitions and len(word) == 2:
                memory_flag = word[1].type is TagType.POINTER
                if memory_flag:  # it's a pointer
                    if word[1].value in self.pointers:  # pointer value was already defined
                        instruction_value = replace(self.pointers[word[1].value])
                    elif word[1].value in self.subroutines:  # define pointer as subroutine scope reference
                        self.pointers[word[1].value] = Tag(word[1].value, TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]
                    elif word[1].value in self.macros:  # I don't know what that would be
                        raise CompilerNotImplementedError(line=word.line)
                    else:  # define pointer as generic integer
                        self.pointer_counter += 1
                        self.pointers[word[1].value] = Tag(self.pointer_counter, TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]
                else:  # it's a number
                    instruction_value = replace(word[1])
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
                scope = self._generate_macro_scope(0, word[0].value, word[2:])  # generate factored macro scope
                for word in scope[::-1]:  # insert into 'to be processed' scope part
                    self.current_scope.insert(0, word)

    def _compile_third_stage(self):
        """
        Third internal compilation stage.

        Inserts subroutines at the end of the 'self.current_scope'.
        Grants proper address pointers to operations that reference subroutines.
        Recalls second compilation stage to process the inserted code.
        Sets memory flag to False for subroutine calls and store instructions
        """

        # subroutine name -> address table
        locations = {}

        # insert subroutines at the end of the instruction list
        for subroutine_name, subroutine_scope in self.subroutines.items():
            scope = subroutine_scope.__copy__()
            locations[subroutine_name] = len(self.instructions)
            for word in scope[1]:
                self.current_scope.add(word)
            self._compile_second_stage()

        # go through TaggedInstructions and replace references to 'subroutine_scope' with addresses
        # from 'locations' table
        for instruction in self.instructions:
            if instruction.value.value in locations:
                instruction.value.value = locations[instruction.value.value]
                instruction.flag = False
            # 2 - store or SRA instructions for Quantum CPU's
            if self.code_namespace.definitions[instruction.opcode.value].opcode == 2:
                instruction.flag = False

    def _compile_forth_stage(self):
        """
        Forth internal compilation stage.

        Converts TaggedInstructions to InstructionN class.
        If 'self.code_namespace' is set to QM lineage of cpu's, then the output is Instruction16
        If 'self.code_namespace' is set to QT lineage of cpu's, then the output is Instruction24
        """

        for instruction in self.instructions:
            self.bytecode.append(
                self._convert_tagged2byte(instruction, self.code_namespace))

    def compile(self):
        """
        Compiles imported code
        """

        self._compile_first_stage()
        self._compile_second_stage()
        self._compile_third_stage()
        self._compile_forth_stage()
