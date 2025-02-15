"""
Basically a small portion of code from 'application.py',
but will be used during preprocessor stage
"""


from source.classes import *
from source.built_ins import *
from source.lexer import Lexer
from source.parser import Parser


class Linker:
    """
    Main linker class
    """

    def __init__(self, namespace: CodeNamespace):
        self.current_scope: Scope | None = None
        self.code_namespace: CodeNamespace = namespace

    def import_code(self, code: str):
        """
        Imports code into linker
        """
