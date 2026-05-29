# from . import FileSystemObject
from src.entities.file_system_object import FileSystemObject # TODO: change to previous import

class File(FileSystemObject):
    content: bytes
    parent: FileSystemObject

    def _eval_size(self) -> int:
        return len(self.content)


if __name__ == "__main__":
    file = File(name="home.,", content=b"hello")
    print(file.content)