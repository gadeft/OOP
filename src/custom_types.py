from typing import NewType
from datetime import datetime


type Metadata = NewType('Metadata', dict[str, str | int | float | bool | list | datetime | Metadata])