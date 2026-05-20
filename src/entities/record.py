from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.entities.file import File


class Record(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(max_length=100)
    file_type: str = Field(max_length=5)
    payload: bytes | File

    size: int = Field(default=0)
    created: datetime = Field(default=datetime.now())
    last_modified: datetime = Field(default=datetime.now())

    def model_post_init(self, __context):
        if isinstance(self.payload, File):
            self.size = self.payload.size
        else:
            self.size = len(self.payload)


    def __repr__(self):
        return (f'name: {self.name}, '
                f'file_type: {self.file_type}, '
                f'payload: ({self.payload}), '
                f'size: {self.size}, '
                f'created: {self.created.strftime("%Y-%m-%d %H:%M:%S")}, '
                f'last_modified: {self.last_modified.strftime("%Y-%m-%d %H:%M:%S")}, ')