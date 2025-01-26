"""
Sticks all code together
"""


from argparse import ArgumentParser, Namespace
from source.classes import *
from source.lexer import Lexer
from source.parser import Parser
from source.compiler import Compiler


class Application:
    """
    Main application class
    """

    def __init__(self):
        self.args: Namespace | None = None

    def parse_args(self) -> None:
        """
        Parse command line arguments
        """

        parser = ArgumentParser(
            prog="QM Compiler",
            description="Quantum Mini Compiler CLI")

        parser.add_argument("-i", "--input",
                            help="input file",
                            required=True)
        parser.add_argument("-o", "--output",
                            help="compiled bytecode output")
        parser.add_argument("-v", "--verbose",
                            help="verbose output",
                            action="store_true",
                            default=False)

        self.args = parser.parse_args()

    def run(self) -> None:
        """
        Runs the application
        """

        self.parse_args()

        # temp code for testing
        lexer = Lexer()
        with open(self.args.input, "r", encoding="ascii") as file:
            lexer.import_code(file.read())
        lexer.evaluate()

        recursive_scope_print(lexer.global_scope)
        print()

        parser = Parser()
        parser.import_scope(lexer.global_scope)
        parser.parse()

        recursive_scope_print(parser.current_scope)
        print()
