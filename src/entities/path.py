from __future__ import annotations

from pathvalidate import sanitize_filepath

from . import Directory, FileSystemObject


class Path:
    def __init__(self, path_or_file: str | FileSystemObject) -> None:
        if isinstance(path_or_file, str):
            self.path: list[str] = self.parse(sanitize_filepath(path_or_file))

        elif isinstance(path_or_file, FileSystemObject):
            self.path: list[str] = self._get_path_of_file(path_or_file)

    def __str__(self) -> str:
        result = "/".join(self.path)
        try:
            if result[0] == '/' and result[1] == '/':
                result = result[1:]
        except IndexError:
            pass
        return result


    @property
    def name(self) -> str:
        return self.path[-1]

    @property
    def parent(self) -> Path | None:
        if len(self.path) == 1 and self.path[0] == "/":
            return None
        if self.path[0] == "/":
            parent_path = "/" + "/".join(self.path[1:-1])
        else:
            parent_path = "/" + "/".join(self.path[:-1])
        return Path(parent_path)

    @property
    def resolved(self) -> bool:
        iter_path = iter(self.path)
        # This part may be not needed
        for name in iter_path:
            match name:
                case '..':
                    return False
                case '~':
                    return False
        return True


    @staticmethod
    def parse(path: str) -> list[str]:
        new_path = path.split("/")
        if new_path[0] == "": # The same as the path starts with a '/'
            new_path[0] = "/"
        return new_path


    def _get_path_of_file(self, file: FileSystemObject, path: list[str] | None = None) -> list[str]:
        if path is None:
            path = []
        if file.parent is None:
            path.append("/")
            return list(reversed(path))
        else:
            path.append(file.name)
            return self._get_path_of_file(file.parent, path)