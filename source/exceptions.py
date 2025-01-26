"""
Compiler exceptions
"""


class CompilerError(Exception):
    """
    Base class for compiler exceptions
    """


class CompilerSyntaxError(CompilerError):
    """
    Syntax error called by compiler
    """
