from src.entities import Directory, File


class FileSystem:
    def __init__(self) -> None:
        self.root = Directory(name="root")
