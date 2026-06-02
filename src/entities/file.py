from datetime import datetime

from pydantic import Field

from . import FileSystemObject, Directory


class File(FileSystemObject):
    parent: Directory

    content: bytes = Field(default=b'')

    def _eval_size(self) -> None:
        self.size = len(self.content)
        self.parent._eval_size()

    def write(self, data: bytes):
        self.content = data
        self._eval_size()
        self.last_modified = datetime.now()
