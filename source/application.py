"""
Sticks all code together
"""


from argparse import ArgumentParser, Namespace
from source.classes import *
from source.lexer import Lexer
from source.file_io import dump
from source.parser import Parser
from source.compiler import Compiler
from source.built_ins import NamespaceQMr11, NamespaceQT


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
        # parser.add_argument("-v", "--verbose",
        #                     help="verbose output",
        #                     action="store_true",
        #                     default=False)
        parser.add_argument("--namespace",
                            help="code namespace",
                            choices=["QT", "QM"],
                            default="QT")

        self.args = parser.parse_args()

    def run(self) -> None:
        """
        Runs the application
        """

        # parse arguments
        self.parse_args()

        # used namespace
        match self.args.namespace:
            case "QM":
                namespace = NamespaceQMr11()
            case _:
                namespace = NamespaceQT()

        # input file
        with open(self.args.input, "r", encoding="ascii") as file:
            code = file.read()

        # Lexing stage
        lexer = Lexer()
        lexer.code_namespace = namespace
        lexer.import_code(code)
        lexer.evaluate()

        print("[LEXER STAGE START]")
        recursive_scope_print(lexer.current_scope)
        print("[LEXER STAGE END]\n")

        # Parsing stage
        parser = Parser()
        parser.import_scope(lexer.current_scope)
        parser.parse()

        print("[PARSER STAGE START]")
        recursive_scope_print(parser.current_scope)
        print("[PARSER STAGE END]\n")

        # Compilation stage
        compiler = Compiler()
        compiler.code_namespace = namespace
        compiler.import_scope(parser.current_scope)
        compiler.compile()

        print("[COMPILER STAGE START]")
        for idx, instruction in enumerate(compiler.bytecode):
            print(
                f"{idx:04x}:    "
                f"{'1' if instruction.flag else '0'} {instruction.value:02X} {instruction.opcode:02X}    "
                f"{compiler.instructions[idx].opcode.value: <7}", end="")
            if instruction.value:  # if value is above zero
                print(f"0x{instruction.value:02X}   # {instruction.value}")
            else:
                print()
        print("[COMPILER STAGE END]", end="\n\n")

        # check output argument, and dump to file
        if self.args.output:
            bytes_written = dump(compiler.bytecode, self.args.output, namespace)
            print(f"{bytes_written} bytes written to '{self.args.output}'")
