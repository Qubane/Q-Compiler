"""
Lexer code
"""


from source.classes import *


class CharacterIterator:
    def __init__(self, string: str):
        self.string: str = string
        self._count: int = -1

    def next(self) -> str | None:
        self._count += 1
        return self.string[self._count] if self._count < len(self.string) else None

    def prev(self) -> str | None:
        self._count -= 1
        return self.string[self._count] if self._count > -1 else None

    def is_done(self):
        if self._count+1 >= len(self.string):
            return True
        return False

    @property
    def count(self) -> int:
        return self._count


class Lexer:
    """
    Lexer class
    """

    def __init__(self):
        self.raw_code: str = ""
        self.global_scope: GlobalScope = GlobalScope(list())

    def import_code(self, code: str) -> None:
        """
        Imports code into Lexer
        :param code: code string
        """

        self.raw_code = code.replace(f"\n{' ' * 4}", "\n\t")

    def evaluate(self):
        """
        Evaluates imported code
        """

        line_count = 1

        buffer = ""
        word = Word()

        iterator = CharacterIterator(self.raw_code)
        while not iterator.is_done():
            char = iterator.next()

            if char == " ":
                if buffer:
                    word.tags.append(Tag(buffer))
                    buffer = ""
            elif char == "\n" or char == "\t":
                if char == "\t":
                    word.tags.append(Tag(">", TagType.INTERNAL))
                if buffer:
                    word.tags.append(Tag(buffer))
                    word.line = line_count
                    self.global_scope.add(word)
                    word = Word()
                    buffer = ""
                if char == "\n":
                    line_count += 1
            else:
                buffer += char
