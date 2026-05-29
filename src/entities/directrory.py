from pydantic import Field

from . import FileSystemObject


class Directory(FileSystemObject):
    content: dict[str, FileSystemObject] = Field(default_factory=dict)

    def _eval_size(self) -> int:
        size = 0
        for obj in self.content.values():
            size += obj.size
        return size


    def get_by_name(self, name: str) -> FileSystemObject | None:
        return self.content.get(name)

    def append(self, obj: FileSystemObject) -> None:
        if self.get_by_name(obj.name):
            raise FileExistsError(f"File \"{obj.name}\" already exists")
        self.content.update({obj.name: obj})
        self.size += obj.size

    def remove_by_name(self, name: str) -> FileSystemObject | None:
        obj = self.get_by_name(name)
        if obj is None:
            raise FileNotFoundError(f"File \"{name}\" not found")
        self.content.pop(name)
        self.size -= obj.size