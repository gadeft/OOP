from src.entities import Directory, File, FileSystemObject, Path


class FileSystem:
    def __init__(self) -> None:
        self.root = Directory(name="root")


    def get(self, path: Path) -> FileSystemObject:
        if not path.resolved:
            raise ValueError(f"Path must be resolved")

        curr = self.root
        for name in path.path:
            if name == '/':
                continue
            try:
                curr = curr.content[name]
            except KeyError:
                raise ValueError(f"Not found: {name} in {curr.name}")

        return curr

    def create_directory(self, parent_path: Path, name: str) -> Directory:
        parent = self.get(parent_path)
        if not isinstance(parent, Directory):
            raise ValueError(f"Parent is not a directory: {parent}")

        directory = Directory(name=name, parent=parent)
        parent.append(directory)
        return directory

    def create_file(self, parent_path: Path, name: str) -> File:
        parent = self.get(parent_path)
        if not isinstance(parent, Directory):
            raise ValueError(f"Parent is not a directory: {parent}")

        file = File(name=name, parent=parent)
        parent.append(file)
        return file

    def delete(self, path: Path) -> None:
        if path.parent is None:
            raise ValueError("You cannot delete a root directory")
        parent = self.get(path.parent)
        if not isinstance(parent, Directory):
            raise ValueError(f"Parent is not a directory: {parent}")

        parent.remove_by_name(path.name)

    def write_to_file(self, path: Path, content: bytes) -> None:
        file = self.get(path)
        if not isinstance(file, File):
            raise ValueError(f"File is a directory: {file}")

        file.write(content)