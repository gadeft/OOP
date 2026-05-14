from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, AfterValidator

from src.custom_types import Metadata
from src.validators import required_metadata_fields


class File(BaseModel):
    metadata: Annotated[Metadata, AfterValidator(required_metadata_fields)]
    payload: str

metadata = {
    "name": "SuperCoolImage",
    "type": "image",
    "path": ["root"],
    "datetime": datetime.now(),
    "size": 123,
    "width": 123,
    "height": 123,
}
print(File(metadata=metadata, payload='Hello World!'))