from typing import Any, Callable

from src.file_manager import FileManager


class Controller:
    def __init__(self, fm: FileManager):
        self.fm = fm
        self.command_funcs: dict[str, Callable[[dict], Any]] = {
            "mkdir": self.make_directory,
            "touch": self.make_file,
            "ls": self.list_items,
            "cat": self.read_from_file,
            "mv": self.move,
            "cp": self.copy,
            "write": self.write_to_file,
            "rm": self.delete,
            "cd": self.change_current_directory
        }

    def run_command(self, command: dict) -> Any:
        cmd = command["command"]
        return self.command_funcs[cmd](command)

    def make_directory(self, args: dict) -> Any:
        return self.fm.create_directory(args["path"])

    def make_file(self, args: dict) -> Any:
        return self.fm.create_file(args["path"])

    def list_items(self, args: dict) -> Any:
        path = args["path"]
        if path is None:
            path = '.'
        return self.fm.list_items(path)

    def read_from_file(self, args: dict) -> Any:
        return str(self.fm.read_from_file(args["path"]))

    def move(self, args: dict) -> Any:
        return self.fm.move(args["source"], args["destination"])

    def copy(self, args: dict) -> Any:
        return self.fm.copy(args["source"], args["destination"])

    def write_to_file(self, args: dict) -> Any:
        text = input()
        return self.fm.write_to_file(args["path"], text.encode("utf-8"))

    def delete(self, args: dict) -> Any:
        return self.fm.delete(args["path"])

    def change_current_directory(self, args: dict) -> Any:
        return self.fm.change_current_directory(args["path"])

    def get_current_directory(self) -> Any:
        return self.fm.get_current_directory_path()