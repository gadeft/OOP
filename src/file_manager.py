from copy import copy

from src.entities import Record, Directory, File
from src.path_parser import absolute_path


class FileManager:
    def __init__(self):
        self.__root = Directory()
        self.__root_record = Record(
            name="root",
            file_type="dir",
            payload=self.__root
        )

    def get_record_by_path(self, path: str) -> Record:
        path: list[str] = absolute_path(path)

        if path[0] == '':
            return self.__root_record
        #
        # path_iter = iter(path)
        # current = self.__root.get_by_name(next(path_iter))
        current = self.__root_record
        for name in path:
            try:
                current = current.payload.get_by_name(name)
            except:
                raise FileNotFoundError
            if current is None:
                raise FileNotFoundError
        return current

    def get_parent_record_by_path(self, path: str) -> Record | None:
        path: list[str] = absolute_path(path)

        if path[0] == '':
            return None

        path_str = '/' + '/'.join(path[:-1])
        parent_record = self.get_record_by_path(path_str)
        if not isinstance(parent_record.payload, Directory):
            raise FileNotFoundError("Parent must be a directory")
        return parent_record

    def create_file(self, path: str, name: str, file_type: str, payload: bytes | Directory) -> Record:
        if file_type == 'dir':
            raise Exception("You cannot create directory using this function")

        parent = self.get_record_by_path(path).payload

        if not isinstance(parent, Directory):
            raise TypeError("Path must refer to a directory")

        record = Record(
            name=name,
            file_type=file_type,
            payload=payload,
        )
        parent.append(record)

        return copy(record)

    def create_directory(self, path: str, name: str) -> Record:
        parent = self.get_record_by_path(path).payload

        if not isinstance(parent, Directory):
            raise TypeError("Path must refer to a directory")

        directory = Directory(parent)
        directory_record = Record(
            name=name,
            file_type="dir",
            payload=directory,
        )
        parent.append(directory_record)
        return copy(directory_record)

    def delete(self, path: str) -> None:
        current_record = self.get_record_by_path(path)
        parent_record = self.get_parent_record_by_path(path)

        current_record = parent_record.payload.remove_by_name(current_record.name)
        if isinstance(current_record.payload, Directory):
            current_record.payload.delete()

    def change_path(self, path: str, new_dir_path: str) -> Record:
        try:
            current_record = self.get_record_by_path(path)
        except FileNotFoundError:
            raise FileNotFoundError("The path to the object does not exist")
        try:
            new_parent_record = self.get_record_by_path(new_dir_path)
        except FileNotFoundError:
            raise FileNotFoundError("The path to the parent directory does not exist")
        if not isinstance(new_parent_record.payload, Directory):
            raise TypeError("new_dir_path must refer to a directory")

        current_parent_record = self.get_parent_record_by_path(path)
        current_parent_record.payload.remove_by_name(current_record.name)
        new_parent_record.payload.append(current_record)

        return copy(current_record)

    def rename(self, path: str, new_name: str) -> Record:
        current_record = self.get_record_by_path(path)
        current_record.name = new_name
        return copy(current_record)

    def copy(self, path: str, new_dir_path: str, new_name: str | None = None) -> Record:
        try:
            current_record = self.get_record_by_path(path)
        except FileNotFoundError:
            raise FileNotFoundError("The path to the object does not exist")
        try:
            new_parent_record = self.get_record_by_path(new_dir_path)
        except FileNotFoundError:
            raise FileNotFoundError("The path to the parent directory does not exist")
        if not isinstance(new_parent_record.payload, Directory):
            raise TypeError("new_dir_path must refer to a directory")

        new_record = copy(current_record)
        if new_name is not None:
            new_record.name = new_name

        new_parent_record.payload.append(new_record)
        return copy(current_record)

    def change_file_content(self, path: str, new_content: str) -> Record:
        current_record = self.get_record_by_path(path)

        if not isinstance(current_record.payload, bytes):
            raise FileNotFoundError("The path must refer to a file")

        current_record.payload = bytes(new_content, encoding="utf-8")
        return copy(current_record)
