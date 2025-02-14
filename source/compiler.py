"""
Compiling code
"""


import logging
from source.classes import *
from source.built_ins import *


LOGGER = logging.getLogger("compiler")


class Compiler:
    """
    Compiler class
    """

    code_namespace: CodeNamespace = NamespaceQT()

    def __init__(self):
        self.current_scope: Scope = Scope()

        self.bytecode: list[InstructionN] = list()
        self.instructions: list[TaggedInstruction | Tag] = list()

        self.pointers: dict[str, Tag] = dict()
        self.address_pointers: dict[str, Tag] = dict()
        self.pointer_counter: int = -1

        self.macros: dict[str, Scope] = dict()
        self.subroutines: dict[str, Scope] = dict()

    def import_scope(self, scope: Scope):
        """
        Imports parsed scope into compiler
        """

        self.current_scope = scope

    def import_data(self, **kwargs):
        """
        Imports compiler data.
        Used during recursive compilation step
        """

        self.pointers: dict[str, Tag] = kwargs.get("pointers", dict())
        self.address_pointers: dict[str, Tag] = kwargs.get("address_pointers", dict())
        self.pointer_counter: int = kwargs.get("pointer_counter", -1)

        self.macros: dict[str, Scope] = kwargs.get("macros", dict())
        self.subroutines: dict[str, Scope] = kwargs.get("subroutines", dict())

    def _generate_macro_scope(self, name: str, args: list[Tag]):
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

        return namespace.instruction_class(
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

            # keywords
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

            # address pointer
            elif word[0].type is TagType.POINTER and word[0].value[0] == "@":
                self.address_pointers[word[0].value] = word[0]

    def _compile_second_stage(self):
        """
        Second internal compilation stage.

        Compiles words into TaggedInstructions.
        Grants address values to variable pointers.
        Grants scope references to subroutine pointers.
        Inserts macro code into current scope for processing.
        Inserts address pointer tags for jumps.
        """

        while len(self.current_scope):
            word = self.current_scope.pop(0)

            # instructions with arguments
            if word[0].value in self.code_namespace.definitions and len(word) == 2:
                # check if it's a pointer
                is_pointer = word[1].value[0] == "$"
                value: str = word[1].value[1:] if is_pointer else word[1].value

                # check if it's numeric
                is_numeric = True
                if value.isnumeric():  # simple numeric
                    pass
                elif value[:2] in GeneralNamespace.number_prefixes:  # prefixed numeric
                    # try converting prefixed to just decimal
                    converted = None
                    try:
                        converted = int(value[2:], GeneralNamespace.number_prefixes[value[:2]])
                    except ValueError:
                        pass

                    # if number wasn't converted -> error occurred -> reraise it as CompilerError
                    if converted is None:
                        raise CompilerValueError(f"Unable to convert numeric value '{value}'", line=word.line)

                    # that may be a bit confusing to do it here
                    word[1].value = f"{'$' if is_pointer else ''}{converted}"
                elif value[0].isdigit():  # raise error if first character is a digit
                    raise CompilerValueError(f"Unable to convert numeric value '{value}'", line=word.line)
                else:  # it's a variable pointer
                    is_numeric = False

                # a non numeric value
                if not is_numeric:
                    if word[1].value in self.pointers:  # pointer value was already defined
                        instruction_value = replace(self.pointers[word[1].value])
                    elif (word[1].value in self.subroutines or
                          word[1].value in self.address_pointers):  # define pointer
                        self.pointers[word[1].value] = Tag(word[1].value, TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]
                    elif word[1].value in self.macros:  # I don't know what that would be
                        raise CompilerNotImplementedError(line=word.line)
                    else:  # define pointer as generic integer
                        if word[0].value not in self.code_namespace.variable_making:
                            raise CompilerNameError(f"Accessing undefined variable '{word[0].value}'",
                                                    line=word.line)
                        self.pointer_counter += 1
                        self.pointers[word[1].value] = Tag(self.pointer_counter, TagType.POINTER)
                        instruction_value = self.pointers[word[1].value]

                # a numeric value
                else:
                    instruction_value = replace(word[1])
                self.instructions.append(TaggedInstruction(
                    flag=is_pointer,
                    value=instruction_value,
                    opcode=word[0]))

            # instructions without arguments
            elif word[0].value in self.code_namespace.definitions and len(word) == 1:
                self.instructions.append(TaggedInstruction(
                    flag=False,
                    value=Tag(0, TagType.INTERNAL),
                    opcode=word[0]))

            # macros
            elif word[0].type is TagType.POINTER and word[0].value in self.macros:
                scope = self._generate_macro_scope(word[0].value, word[2:])  # generate formatted macro scope
                for word in scope[::-1]:  # insert into 'to be processed' scope part
                    self.current_scope.insert(0, word)
                self._compile_first_stage()

            # address pointers
            elif word[0].type is TagType.POINTER and word[0].value in self.address_pointers:
                self.instructions.append(word[0])

    def _compile_third_stage(self):
        """
        Third internal compilation stage.

        Generates address pointers and inserts them at correct places
        """

        # search for all address pointers
        address_pointers = {}
        for index, instruction in enumerate(self.instructions):
            # skip all non-tags
            if not isinstance(instruction, Tag):
                continue
            address_pointers[instruction.value] = index

        # replace all address pointer tags references
        idx = 0
        while idx < len(self.instructions):
            instruction = self.instructions[idx]
            idx += 1

            # delete hanging address pointers & correct pointers being offset
            if isinstance(instruction, Tag):
                idx -= 1
                self.instructions.pop(idx)

                # correct pointers
                for pointer_name, pointer_address in address_pointers.items():
                    if pointer_address > idx:
                        address_pointers[pointer_name] = pointer_address - 1

        for instruction in self.instructions:
            # make address pointers
            if instruction.value.value in address_pointers:
                instruction.value.value = address_pointers[instruction.value.value]
                instruction.flag = False

    def _compile_forth_stage(self):
        """
        Forth internal compilation stage.

        Inserts subroutines at the end of the 'self.current_scope'.
        Sets memory flag to False for subroutine calls and store instructions
        """

        # subroutine name -> address table
        subroutine_pointers = {}

        # insert subroutines at the end of the instruction list
        for subroutine_name, subroutine_scope in self.subroutines.items():
            scope = subroutine_scope.__copy__()
            subroutine_pointers[subroutine_name] = len(self.instructions)
            for word in scope[1]:
                self.current_scope.add(word)
            self._compile_second_stage()

        # go through TaggedInstructions and replace references to 'subroutine_scope' with addresses
        # from 'locations' table
        for instruction in self.instructions:
            # make subroutine pointers
            if instruction.value.value in subroutine_pointers:
                instruction.value.value = subroutine_pointers[instruction.value.value]
                instruction.flag = False
            # 2 - store or SRA instructions for Quantum CPU's
            if self.code_namespace.definitions[instruction.opcode.value].opcode == 2:
                instruction.flag = False

    def _compile_fifth_stage(self):
        """
        Fifth internal compilation stage.

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
        self._compile_fifth_stage()
