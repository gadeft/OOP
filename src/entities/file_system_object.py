from __future__ import annotations

from datetime import datetime
from typing import Any
from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pathvalidate import validate_filename


class FileSystemObject(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    content: bytes | dict[str, FileSystemObject]
    parent: FileSystemObject | None = None

    created: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    size: int = Field(default_factory=int)

    @field_validator("name", mode="after")
    @classmethod
    def validate_content(cls, value: str) -> str:
        try:
            validate_filename(value, platform="linux")
            return value
        except ValueError as e:
            raise e

    def model_post_init(self, context: Any, /) -> None:
        self.size = self._eval_size()


    @abstractmethod
    def _eval_size(self) -> int:
        pass