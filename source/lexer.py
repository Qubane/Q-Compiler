"""
Lexer code
"""


from source.classes import *
from source.built_ins import *


class Lexer:
    """
    Lexer class
    """

    code_namespace: CodeNamespace = NamespaceQT()

    def __init__(self):
        self.raw_code: str = ""
        self.current_scope: GlobalScope = GlobalScope()

    def import_code(self, code: str) -> None:
        """
        Imports code into Lexer
        :param code: code string
        """

        self.raw_code = code.replace(f"\n{' ' * 4}", "\n\t")

    def _eval_first_stage(self):
        """
        First internal evaluation stage.

        In this stage code is analyzed letter-by-letter.
        Each complete code-word is compiled into Tag class.
        After newline, all tags on the line make a complete Word class.
        All words are appended to global scope, no additional scopes are generated.
        """

        line_count = 1

        buffer = ""
        word = Word()

        is_commented = False

        for char in self.raw_code:
            if char == "\n":
                is_commented = False
            if is_commented:
                continue

            if char == " ":  # tag separator
                if buffer:
                    word.tags.append(Tag(buffer))
                    buffer = ""
            elif char == "\n" or char == "\t" or char == ";":  # special characters
                if char == ";":  # comments
                    is_commented = True
                if buffer:  # append last tag from buffer
                    word.add(Tag(buffer))
                if len(word.tags) > 0:  # make and append the word
                    word.line = line_count
                    self.current_scope.add(word)
                    word = Word()
                    buffer = ""
                if char == "\t":  # level up
                    word.insert(0, Tag(">", TagType.INTERNAL))
                if char == "\n":  # increment line counter
                    line_count += 1
            else:  # any other character
                buffer += char

    def _eval_second_stage(self):
        """
        Second internal evaluation stage.

        In this stage everything is analyzed tag-by-tag.
        Every tag is simply being assigned a type
        """

        for word in self.current_scope:
            word: Word  # help type hinting
            for tag in word:
                if tag.type is not TagType.UNDEFINED:
                    continue
                if tag.value in GeneralNamespace.definitions:
                    tag.type = GeneralNamespace.definitions[tag.value].type
                elif tag.value in self.code_namespace.definitions:
                    tag.type = self.code_namespace.definitions[tag.value].type
                elif tag.value.isnumeric():  # simple decimal numbers
                    tag.type = TagType.NUMBER
                    tag.value = int(tag.value)
                elif tag.value[:2] in NamespaceGeneral.number_prefixes:  # non decimal numbers
                    tag.type = TagType.NUMBER
                    try:
                        tag.value = int(tag.value[2:], NamespaceGeneral.number_prefixes[tag.value[:2]])
                    except ValueError:
                        raise CompilerValueError(
                            "Unable to convert number",
                            line=word.line)
                else:
                    tag.type = TagType.POINTER

    def evaluate(self):
        """
        Evaluates imported code
        """

        self._eval_first_stage()
        self._eval_second_stage()
