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
        with open(self.args.input, "r", encoding="ascii") as file:
            code = file.read()

        lexer = Lexer()
        lexer.import_code(code)
        lexer.evaluate()

        print("[LEXER STAGE START]")
        recursive_scope_print(lexer.current_scope)
        print("[LEXER STAGE END]\n")

        parser = Parser()
        parser.import_scope(lexer.current_scope)
        parser.parse()

        print("[PARSER STAGE START]")
        recursive_scope_print(parser.current_scope)
        print("[PARSER STAGE END]\n")

        compiler = Compiler()
        compiler.import_scope(parser.current_scope)
        compiler.compile()

        print("[COMPILER STAGE START]")
        # recursive_scope_print(compiler.current_scope)
        for instruction in compiler.instructions:
            print(instruction)
        print("[COMPILER STAGE END]")
