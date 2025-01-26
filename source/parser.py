"""
Compiling code
"""


from source.classes import *
from source.built_ins import *


class Parser:
    """
    Parser class
    """

    def __init__(self):
        self.global_scope: GlobalScope = GlobalScope()

    def import_scope(self, scope: Scope):
        """
        Imports scope into parser
        """

        self.global_scope = scope

    def _parse_first_stage(self):
        """
        First stage of parsing

        Basic syntax checking stage
        """

        for word in self.global_scope:
            word: Word  # help type hinting

            # check 'macro' and 'subr' keywords
            if word[0].value in ["macro", "subr"] and word[1].type is not TagType.POINTER:
                raise CompilerSyntaxError(
                    f"built-in '{word[0].value}' followed by a non-pointer argument",
                    line=word.line)

            # check 'uses' keyword
            for idx, tag in enumerate(word):
                tag: Tag  # help type hinting
                if tag.value == "uses":
                    break
            for tag in word[idx+1:]:
                if tag.type is not TagType.POINTER:
                    raise CompilerSyntaxError(
                        f"built-in '{word[idx].value}' followed by a non-pointer argument(s)",
                        line=word.line)

    def _parse_second_stage(self):
        """
        Second stage of parsing
        """

    def parse(self):
        """
        Parses imported scope
        """

        self._parse_first_stage()
        self._parse_second_stage()
