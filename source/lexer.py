"""
Lexer code
"""


from source.classes import *


class Lexer:
    """
    Lexer class
    """

    def __init__(self):
        self.global_scope: GlobalScope = GlobalScope(list())
