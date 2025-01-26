"""
Compiler exceptions
"""


class CompilerError(Exception):
    """
    Base class for compiler exceptions
    """

    def __init__(self, *args, line: int = 0):
        super().__init__(*args)
        self.line: int = line


class CompilerSyntaxError(CompilerError):
    """
    Syntax error called by compiler
    """
