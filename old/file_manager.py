from datetime import date
from unittest import case

from main import FileSystemObject, File, TextFile, ImageFile, Folder


class FileManager:
    def __init__(self):
        self.root = Folder("root", '/', str(date.today()), 0)
        self.current_folder = self.root


    def create_object(self, name, size, obj_type, title=None, height=None, width=None):
        if self.__check_name_exists(name):
            raise NameError(f"Object with this name already exists. The name {name}")

        obj_path = self.current_folder.path + f"/{name}"
        obj_date = str(date.today())
        match obj_type:
            case "folder":
                obj = Folder(name, obj_path, obj_date, size)
            case "file":
                obj = File(name, obj_path, obj_date, size)
            case "text":
                if not title:
                    raise ValueError("title field is required for creating a text file")
                obj = TextFile(name, obj_path, obj_date, size, title)
            case "image":
                if not height:
                    raise ValueError("height field is required for creating an image file")
                if not width:
                    raise ValueError("width field is required for creating an image file")
                obj = ImageFile(name, obj_path, obj_date, size, height, width)
            case _:
                raise ValueError(f"Unknown type {obj_type}")

        self.current_folder.add_object(obj)
        return obj

    def delete_object(self, name):
        obj = self.current_folder.remove_object(name)
        if not obj:
            raise FileNotFoundError(f"Object with this name doesn't exist: {name}")
        obj.delete()

    def rename_object(self, name, new_name):
        obj = self.current_folder.get_object_by_name(name)
        if not obj:
            raise FileNotFoundError(f"Object with this name doesn't exist: {name}")
        obj.rename(new_name)

    def move_object(self, name, new_path):
        obj = self.current_folder.get_object_by_name(name)
        if not obj:
            raise FileNotFoundError(f"Object with this name doesn't exist: {name}")
        obj.path = new_path

    def copy_object(self, src_name, new_name, new_path):
        obj = self.current_folder.get_object_by_name(src_name)
        if not obj:
            raise FileNotFoundError(f"Object with this name doesn't exist: {src_name}")

        params = dict()
        match obj.type:
            case "text":
                params["title"] = obj.title
            case "image":
                params["height"] = obj.height
                params["width"] = obj.width
            case _:
                pass

        new_obj = self.create_object(
            new_name,
            obj.size,
            obj.type,
            **params
        )
        new_obj.path = new_path
        return new_obj


    def __check_name_exists(self, name):
        for obj in self.current_folder.objects:
            if obj.name == name:
                return True
        return False