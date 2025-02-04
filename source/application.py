"""
Sticks all code together
"""


import os
import logging
from time import sleep
from argparse import ArgumentParser, Namespace
from source.classes import *
from source.lexer import Lexer
from source.file_io import dump
from source.parser import Parser
from source.compiler import Compiler
from source.built_ins import NamespaceQMr11, NamespaceQT, CodeNamespace


LOGGER = logging.getLogger()


class Application:
    """
    Main application class
    """

    def __init__(self):
        self.args: Namespace | None = None
        self.code_namespace: CodeNamespace | None = None

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
        parser.add_argument("--namespace",
                            help="code namespace",
                            choices=["QT", "QM"],
                            default="QT")
        parser.add_argument("--live",
                            help="compiles the file every 250 ms",
                            action="store_true",
                            default=False)

        self.args = parser.parse_args()

    def compile_input(self):
        """
        Compiles file
        """

        # read file
        with open(self.args.input, "r", encoding="ascii") as file:
            code = file.read()

        # Lexing stage
        lexer = Lexer()
        lexer.code_namespace = self.code_namespace
        lexer.import_code(code)
        lexer.evaluate()

        # Parsing stage
        parser = Parser()
        parser.import_scope(lexer.current_scope)
        parser.parse()

        # Compilation stage
        compiler = Compiler()
        compiler.code_namespace = self.code_namespace
        compiler.import_scope(parser.current_scope)
        compiler.compile()

        for idx, instruction in enumerate(compiler.bytecode):
            # line index
            output = f"{idx:04X}    "

            # instruction bytecode
            if isinstance(self.code_namespace, NamespaceQT):
                output += f"{'1' if instruction.flag else '0'} {instruction.value:04X} {instruction.opcode:02X}    "
            elif isinstance(self.code_namespace, NamespaceQMr11):
                output += f"{'1' if instruction.flag else '0'} {instruction.value:02X} {instruction.opcode:02X}    "

            # instruction name
            output += f"{compiler.instructions[idx].opcode.value: <7}"

            # instruction value
            if instruction.value:  # if value is above zero
                if isinstance(self.code_namespace, NamespaceQT):
                    output += f"0x{instruction.value:04X}   # {instruction.value}"
                elif isinstance(self.code_namespace, NamespaceQMr11):
                    output += f"0x{instruction.value:02X}   # {instruction.value}"
            LOGGER.info(output)

        # check output argument, and dump to file
        if self.args.output:
            bytes_written = dump(compiler.bytecode, self.args.output, self.code_namespace)
            LOGGER.info(f"{bytes_written} bytes written to '{self.args.output}'")

    def run(self) -> None:
        """
        Runs the application
        """

        # parse arguments
        self.parse_args()

        # setup logging
        kwargs = {"style": "{", "format": "{levelname}:{name}: {message}"}
        if self.args.verbose:
            logging.basicConfig(**kwargs, level=logging.INFO)
        else:
            logging.basicConfig(**kwargs)

        # used namespace
        match self.args.namespace:
            case "QM":
                self.code_namespace = NamespaceQMr11()
            case _:
                self.code_namespace = NamespaceQT()

        # compile
        while True:
            # clear screen
            if os.name == "nt":  # windows
                os.system("cls")
            else:  # unix
                os.system("clear")
            print("\x1b[0m", end="")

            # compile input
            try:
                self.compile_input()
            except CompilerError as err:
                print(f"\x1b[31m{err}; line: {err.line}", end="", flush=True)

            # if live updates are turned off -> break
            if not self.args.live:
                break

            # wait
            sleep(0.25)
