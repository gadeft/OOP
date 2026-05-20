

def absolute_path(path: str) -> list[str] | None:
    if not path.startswith('/'):
        return None
    if path.endswith('/') and not len(path) == 1:
        path = path[:-1]
    result = path.split('/')[1:] # removing empty string at the start
    return result
