from __future__ import annotations

from pydantic import validate_call
from pathvalidate import validate_filepath, sanitize_filepath, is_valid_filepath, ValidationError

from src.file_system import FileSystem
from src.entities import Directory, File


class Path:
    # @validate_call # TODO: fix the problem with pydantic error here
    def __init__(self, path: str, *, fs: FileSystem, current: Directory) -> None:
        self.path: list[str] = self.parse(sanitize_filepath(path), root_name=fs.root.name)
        self.fs = fs
        self.current = current


    @property
    def parent(self) -> Path | None:
        if not self.path[0] == fs.root.name:
            self.path = self.resolve()
        if len(self.path) == 1:
            return None
        return Path(str(self.path[:-1]), fs=self.fs, current=self.current)


    # def resolve(self) -> list[str]:
    #     absolute_path = list()
    #     if self.path[0] == "..":
    #



    @staticmethod
    def check(path: str) -> bool:
        """Checks if the path is valid"""
        return is_valid_filepath(path, platform="windows")

    @staticmethod
    def parse(path: str, root_name: str = "root") -> list[str]:
        new_path = path.split("/")
        if new_path[0] == "": # The same as the path starts with a '/'
            new_path[0] = root_name
        return new_path


if __name__ == '__main__':
    fs = FileSystem()
    current = fs.root

    path = Path("../home/../user/./", fs=fs, current=current)
    print(path.path)
    print(Path.check('/'.join(path.path)))