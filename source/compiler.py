"""
Compiling code
"""


from source.classes import *
from source.built_ins import *


class Compiler:
    """
    Compiler class
    """

    def __init__(self):
        self.current_scope: Scope = Scope()

    def import_scope(self, scope: Scope):
        """
        Imports parsed scope into compiler
        """

        self.current_scope = scope
