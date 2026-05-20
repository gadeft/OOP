from typing import Self

from src.entities.record import Record
from src.entities.file import File


class Directory(File):
    def __init__(self, parent: Self | None = None):
        if not isinstance(parent, Directory) and parent is not None:
            raise TypeError('Parent must be of type Directory.')
        self.parent = parent
        self.__size = 0
        self.__content: list[Record] = []

    def __repr__(self):
        if len(self.__content) == 0:
            return ''
        representation = '\n'
        for record in self.__content:
            representation += record.__repr__() + '\n'
        return representation


    @property
    def size(self) -> int:
        return self.__size

    @property
    def content(self) -> tuple[Record, ...]:
        return tuple(self.__content)


    def get_by_name(self, name) -> Record | None:
        for record in self.__content:
            if record.name == name:
                return record
        return None

    def remove_by_name(self, name) -> Record | None:
        record = self.get_by_name(name)
        if not record:
            raise FileNotFoundError(f"Record {name} not found")
        self.__content.remove(record)
        self.__size -= record.size
        return record

    def append(self, record: Record) -> None:
        same_name_record = self.get_by_name(record.name)
        if not (same_name_record is None):
            raise FileExistsError(f"Name {record.name} already exists")
        self.__content.append(record)
        self.__size += record.size

    def delete(self) -> None:
        """Deleting links to this directory from all nested directories"""
        for record in self.__content:
            if isinstance(record.payload, Directory):
                del record.payload.parent