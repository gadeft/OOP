from lark import Lark

from src.cli import CLI
from src.arg_parser import GRAMMAR, CommandTransformer
from src.file_system import FileSystem
from src.file_manager import FileManager
from src.controler import Controller


def main():
    fs = FileSystem()
    fm = FileManager(fs)

    fm.create_directory("/home")
    fm.create_directory("/home/user")
    fm.change_current_directory("/home/user")

    controller = Controller(fm)
    parser = Lark(GRAMMAR, parser="lalr", transformer=CommandTransformer())
    cli = CLI(parser, controller)

    cli.run()


if __name__ == '__main__':
    main()