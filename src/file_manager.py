from src.entities import File, Directory
from src.file_system import FileSystem


class FileManager:
    def __init__(self, fs: FileSystem) -> None:
        self.fs = fs
        self.current: Directory = self.fs.root