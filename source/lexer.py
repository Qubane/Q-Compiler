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
        self.global_scope: GlobalScope = GlobalScope(list())
