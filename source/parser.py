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
        """

    def parse(self):
        """
        Parses imported scope
        """

        self._parse_first_stage()
