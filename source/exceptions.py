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


class CompilerValueError(CompilerError):
    """
    Error when converting NUMBER tag to true int
    """


class CompilerIndentationError(CompilerError):
    """
    Indentation error called by compiler
    """
