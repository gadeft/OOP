from pathvalidate import sanitize_filepath

from src.entities import File, Directory, Path
from src.file_system import FileSystem


MES = "Path contains forbidden characters: {}"


class FileManager:
    def __init__(self, fs: FileSystem) -> None:
        self.fs = fs
        self.current: Directory = self.fs.root

    def resolve_path(self, path: str) -> Path:
        path = Path(path)
        if path.path[0] == "/":
            return path
        curr_path = Path(self.current)

        for name in path.path:
            match name:
                case "~":
                    raise ValueError(MES.format(name))
                case "-":
                    raise ValueError(MES.format(name))

        curr_path.path.pop(0)
        abs_path = sanitize_filepath("/".join(curr_path.path + path.path))
        return Path(abs_path)

    def change_current_directory(self, path: str) -> None:
        path = self.resolve_path(path)
        self.current = self.fs.get(path)

    def create_directory(self, path: str) -> None:
        path = self.resolve_path(path)
        self.fs.create_directory(path.parent, path.name)

    def create_file(self, path: str) -> None:
        path = self.resolve_path(path)
        self.fs.create_file(path.parent, path.name)

    def move(self, source: str, destination: str) -> None:
        source = self.resolve_path(source)
        destination = self.resolve_path(destination)

        src = self.fs.get(source)
        dest = self.fs.get(destination)

        dest.append(src)
        self.fs.delete(source)

    def copy(self, source: str, destination: str) -> None:
        source = self.resolve_path(source)
        destination = self.resolve_path(destination)

        src = self.fs.get(source)
        dest = self.fs.get(destination)

        dest.append(src)

    def delete(self, path: str) -> None:
        path = self.resolve_path(path)
        self.fs.delete(path)

    def write_to_file(self, path: str, content: bytes) -> None:
        path = self.resolve_path(path)
        self.fs.write_to_file(path, content)

    def read_from_file(self, path: str) -> bytes:
        path = self.resolve_path(path)
        file = self.fs.get(path)
        if not isinstance(file, File):
            raise ValueError("Path must refer to a file")
        return file.content

    def size(self, path: str) -> int:
        path = self.resolve_path(path)
        obj = self.fs.get(path)
        return obj.size

    def list_items(self, path: str) -> str:
        path = self.resolve_path(path)
        dir = self.fs.get(path)
        if not isinstance(dir, Directory):
            raise TypeError("Must be a directory")

        res = str()
        for item in dir.content.values():
            res += f"{item.created} {item.last_modified} {item.size} {item.name}\n"

        return res

    def get_current_directory_path(self) -> str:
        return str(Path(self.current))