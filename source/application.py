"""
Sticks all code together
"""


from argparse import ArgumentParser, Namespace
from source.lexer import Lexer


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

        for word in lexer.global_scope:
            print(f"{word.line: <3}", " ".join(f"[{tag.value: >12} {tag.type: <9}]" for tag in word))
