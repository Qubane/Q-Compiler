"""
Compiling code
"""


import logging
from source.classes import *
from source.built_ins import *
from source.linker import Linker


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
        Generates a formatted macro scope
        """

        macro = self.macros[name].__copy__()

        # macro with multiple args
        if len(macro[0]) > 2:
            # translation dictionary
            for old, new in zip(macro[0][3:], args):
                self._match_and_replace(macro[1], old, new)
        return macro[1]

    def _generate_subr_scope(self, name: str):
        """
        Generates a formatted subroutine scope
        """

        subr = self.subroutines[name].__copy__()

        # subroutine with multiple args
        if len(subr[0]) > 2:
            # blindly add pop instructions to scope
            for arg in subr[0][3:]:
                # store instruction
                subr[1].insert(0, Word([
                    Tag(self.code_namespace.variable_making[0], TagType.BUILT_IN),
                    arg
                ]))
                # pop instruction
                subr[1].insert(0, Word([
                    Tag(self.code_namespace.stack_operations["pop"], TagType.BUILT_IN),
                ]))
        return subr[1]

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

    def _preprocess_stage(self):
        """
        Preprocessor stage.

        Processes all INTERNAL tag types
        """

        idx = -1
        while idx < len(self.current_scope)-1:
            idx += 1
            word = self.current_scope[idx]

            # skip all scopes
            if isinstance(word, Scope):
                continue

            # skip all non internal tag types
            if word[0].type is not TagType.INTERNAL:
                continue

            # delete preprocessor instruction
            word = self.current_scope.pop(idx)
            idx -= 1

            instruction = word[0].value[1:]
            if instruction == "define":
                old_tag = word[1]

                # generic defines
                if len(word) == 3:
                    new_tag = word[2]

                # defines with more than 2 arguments
                else:
                    # try to evaluate the expression
                    expression = " ".join(x.value for x in word[2:])
                    expression = expression.replace("__", "")  # there is no good reason to use '__'
                    try:
                        evaluated = int(eval(expression)) % (self.code_namespace.max_int + 1)
                    except Exception as err:
                        raise CompilerSyntaxError(f"Unable to process '{expression}'", line=word.line)

                    # generate new tag according to newly calculated value
                    new_tag = Tag(str(evaluated), TagType.POINTER)

                self._match_and_replace(self.current_scope, old_tag, new_tag)

            elif instruction == "include":
                if len(word) != 2:
                    raise CompilerSyntaxError("Incorrect number of arguments", line=word.line)

                linker = Linker(self.code_namespace)
                # TODO: proper relative to source code paths
                raise CompilerNotImplementedError(line=word.line)

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
                self.subroutines[word[1].value][1] = self._generate_subr_scope(word[1].value)
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
                pointer_name: str = word[1].value[1:] if is_pointer else word[1].value

                # check if it's numeric
                is_numeric = True
                if pointer_name.isnumeric():  # simple numeric
                    word[1].value = pointer_name
                elif pointer_name[:2] in GeneralNamespace.number_prefixes:  # prefixed numeric
                    # try converting prefixed to just decimal
                    converted = None
                    try:
                        converted = int(pointer_name[2:], GeneralNamespace.number_prefixes[pointer_name[:2]])
                    except ValueError:
                        pass

                    # if number wasn't converted -> error occurred -> reraise it as CompilerError
                    if converted is None:
                        raise CompilerValueError(f"Unable to convert numeric value '{pointer_name}'",
                                                 line=word.line)

                    # that may be a bit confusing to do it here
                    word[1].value = str(converted)
                elif pointer_name[0].isdigit():  # raise error if first character is a digit
                    raise CompilerValueError(f"Unable to convert numeric value '{pointer_name}'",
                                             line=word.line)
                else:  # it's a variable pointer
                    is_numeric = False

                # a non numeric value
                if not is_numeric:
                    if pointer_name in self.pointers:  # pointer value was already defined
                        instruction_value = replace(self.pointers[pointer_name])
                    elif (pointer_name in self.subroutines or
                          pointer_name in self.address_pointers):  # define pointer
                        self.pointers[pointer_name] = Tag(pointer_name, TagType.POINTER)
                        instruction_value = self.pointers[pointer_name]
                    elif pointer_name in self.macros:  # I don't know what that would be
                        raise CompilerNotImplementedError(line=word.line)
                    else:  # define pointer as generic integer
                        if word[0].value not in self.code_namespace.variable_making:
                            raise CompilerNameError(f"Accessing undefined variable '{word[0].value}'",
                                                    line=word.line)
                        self.pointer_counter += 1
                        self.pointers[pointer_name] = Tag(self.pointer_counter, TagType.POINTER)
                        instruction_value = self.pointers[pointer_name]

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
                # check for syntax error
                if word[1].value != "uses":
                    raise CompilerSyntaxError("Missing keyword 'uses'", line=word.line)

                scope = self._generate_macro_scope(word[0].value, word[2:])  # generate formatted macro scope
                for word in scope[::-1]:  # insert into 'to be processed' scope part
                    self.current_scope.insert(0, word)
                self._compile_first_stage()

            # subroutines with arguments
            elif word[0].value == self.code_namespace.subr_operations["call"] and len(word) > 2:
                # check for syntax error
                if word[2].value != "uses":
                    raise CompilerSyntaxError("Missing keyword 'uses'", line=word.line)

                # append cut call instruction
                self.current_scope.insert(0, Word(word[:2], line=word.line))

                # generate instructions to push arguments into stack
                for arg in word[-1:2:-1]:
                    self.current_scope.insert(0, Word([
                        Tag(self.code_namespace.stack_operations["push"], TagType.BUILT_IN)
                    ], line=word.line))
                    self.current_scope.insert(0, Word([
                        Tag(self.code_namespace.variable_loading["load"], TagType.BUILT_IN),
                        arg
                    ], line=word.line))

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

        # append subroutines at the end of the instruction list
        for subroutine_name, subroutine_scope in self.subroutines.items():
            scope = subroutine_scope.__copy__()
            subroutine_pointers[subroutine_name] = len(self.instructions)
            for word in scope[1]:
                self.current_scope.add(word)
            pre_compilation_pointers = set(self.pointers)
            pre_compilation_counter = self.pointer_counter
            self._compile_first_stage()
            self._compile_second_stage()
            self._compile_third_stage()
            post_compilation_pointers = set(self.pointers)
            post_compilation_counter = self.pointer_counter

            # delete created by subroutine variables, and reset pointer counter by same amount
            pointer_diff = post_compilation_pointers - pre_compilation_pointers
            self.pointer_counter -= post_compilation_counter - pre_compilation_counter
            for pointer in pointer_diff:
                self.pointers.pop(pointer)

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

    def _trivial_optimization(self):
        """
        Trivial optimization stage.

        Removes unnecessary 'load' / stack instructions
        """

        accumulator = Tag("ACC", TagType.UNDEFINED)
        modified = False

        idx = 0
        while idx < len(self.instructions):
            instruction = self.instructions[idx]
            idx += 1

            # if instruction is variable loading
            if instruction.opcode.value in self.code_namespace.variable_loading.values():
                # if there are no modifying instructions before previous load
                # remove this instruction
                if accumulator == instruction.value and not modified:
                    idx -= 1
                    self.instructions.pop(idx)

                # update values
                accumulator = instruction.value
                modified = False

            elif instruction.opcode.value not in self.code_namespace.non_modifying_operations:
                modified = True

    def compile(self):
        """
        Compiles imported code
        """

        self._preprocess_stage()

        self._compile_first_stage()
        self._compile_second_stage()
        self._compile_third_stage()
        self._compile_forth_stage()

        # self._trivial_optimization()
        self._compile_fifth_stage()

        if len(self.instructions) > 0xFFFF:
            raise CompilerError("Address overflow. Too many instruction!")
