from typing import NewType

from pydantic import BaseModel

from src.custom_types import Metadata
from src.entities.file import File


type PayloadFolder = NewType("PayloadFolder", list[File | Folder])


class Folder(BaseModel):
    metadata: Metadata
    payload: PayloadFolder