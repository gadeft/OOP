from datetime import datetime
from typing import Callable

from src.custom_types import Metadata


type metadata_field_validator = Callable[[...], bool]


ROOT_FOLDER_NAME = "root"
ALLOWED_FILE_TYPES = {
    "text",
    "image",
    "video",
    "audio",
}


def _validate_path_items(path: list[str]) -> bool:
    for item in path:
        if not isinstance(item, str):
            return False
    return True


def validate_name(name: str) -> bool:
    if not isinstance(name, str):
        raise TypeError('name must be a string')
    if name is None:
        raise ValueError('Name cannot be None')
    if name == "":
        raise ValueError('Name cannot be an empty string')
    if not name.isalnum():
        raise ValueError('Name must contain only alphanumeric characters')
    if len(name) > 255:
        raise ValueError('Name cannot contain more than 255 characters')
    return True

def validate_type(type_name: str) -> bool:
    if not isinstance(type_name, str):
        raise TypeError('type name must be a string')
    if type_name not in ALLOWED_FILE_TYPES:
        raise ValueError('type name must be one of the following: {}'.format(ALLOWED_FILE_TYPES))
    return True

def validate_path(path: list[str]) -> bool:
    if not isinstance(path, list):
        raise TypeError('path must be a list')
    if len(path) == 0:
        raise ValueError('Path cannot be an empty list')
    if not _validate_path_items(path):
        raise ValueError('path must contain a list of strings')
    if path[0] != ROOT_FOLDER_NAME:
        raise ValueError('path must start with root folder, i.e. the first element of path list must be "{}"'.format(ROOT_FOLDER_NAME))
    # if path[-1] != : TODO: implement checking path existence logic
    return True

def validate_datetime(dt: datetime) -> bool:
    if not isinstance(dt, datetime):
        raise TypeError('datetime must be a datetime type')
    return True

def validate_size(size: int) -> bool:
    if not isinstance(size, int):
        raise TypeError('size must be a integer')
    return True


REQUIRED_METADATA_FIELDS: dict[str, metadata_field_validator] = {
    "name": validate_name,
    "type": validate_type,
    "path": validate_path,
    "datetime": validate_datetime,
    "size": validate_size
}


def required_metadata_fields(metadata: Metadata) -> Metadata:
    lacking_fields = list()
    for field, value in REQUIRED_METADATA_FIELDS.items():
        try:
            value(metadata[field])
        except KeyError:
            lacking_fields.append(field)
        except Exception as e:
            raise Exception(e)

    if lacking_fields:
        raise Exception("Lacking required fields: {}".format(lacking_fields))

    return metadata


if __name__ == "__main__": # TODO: Delete
    test_metadata = {
        "name": "1234",
        "type": "text",
        "path": ["root"],
        "datetime": datetime.now(),
        "size": 123,
        "custom_field": "some_value"
    }

    required_metadata_fields(test_metadata)