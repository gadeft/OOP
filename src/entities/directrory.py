from __future__ import annotations

from pydantic import Field, ConfigDict

from . import FileSystemObject


class Directory(FileSystemObject):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content: dict[str, FileSystemObject] = Field(default_factory=dict)
    parent: Directory | None = None

    def _eval_size(self) -> None:
        size = 0
        for obj in self.content.values():
            size += obj.size
        self.size = size
        if isinstance(self.parent, Directory):
            self.parent._eval_size()

    def get_by_name(self, name: str) -> FileSystemObject | None:
        return self.content.get(name)

    def append(self, obj: FileSystemObject) -> None:
        if self.get_by_name(obj.name):
            raise FileExistsError(f"File \"{obj.name}\" already exists")
        self.content.update({obj.name: obj})

        self.size += obj.size
        if isinstance(self.parent, Directory):
            self.parent._eval_size()

    def remove_by_name(self, name: str) -> FileSystemObject | None:
        obj = self.get_by_name(name)
        if obj is None:
            raise FileNotFoundError(f"File \"{name}\" not found")
        self.content.pop(name)

        self.size -= obj.size
        if isinstance(self.parent, Directory):
            self.parent._eval_size()