from abc import ABC, abstractmethod


class FileSystemObject(ABC):

    def __init__(self, name, path, date, size):
        self.name = name
        self.path = path
        self.date = date
        self.size = size
        self.__deleted = False
        self.__type: str | None = None


    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def date(self):
        return self.__date

    @property
    def size(self):
        return self.__size

    @property
    def deleted(self):
        return self.__deleted


    @deleted.setter
    def deleted(self, deleted):
        self.__deleted = deleted

    @name.setter
    def name(self, name):
        self.__name = name

    @path.setter
    def path(self, path):
        self.__path = path

    @date.setter
    def date(self, date):
        self.__date = date

    @size.setter
    def size(self, size):
        self.__size = size


    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def rename(self, new_name):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def copy(self):
        pass


class File(FileSystemObject):
    def __init__(self, name, path, date, size):
        super().__init__(name, path, date, size)
        self.__type = "file"


    @property
    def type(self):
        return self.__type


    def get_info(self):
        print(f"File info: \nName: {self.name}, \nPath: {self.path}, \nDate: {self.date}, \nSize: {self.size}")

    def rename(self, new_name):
        self.name = new_name

    def delete(self):
        self.deleted = True

    def copy(self):
        return File(self.name, self.path, self.date, self.size)


class TextFile(FileSystemObject):
    def __init__(self, name, path, date, size, title):
        super().__init__(name, path, date, size)
        self.title = title
        self.__type = "text"

    @property
    def title(self):
        return self.__title

    @property
    def type(self):
        return self.__type

    @title.setter
    def title(self, title):
        self.__title = title


    def get_info(self):
        print(f"Text file info: \nTitle: {self.title} \nName: {self.name}, \nPath: {self.path}, \nDate: {self.date}, \nSize: {self.size}")

    def rename(self, new_name):
        self.name = new_name

    def delete(self):
        self.deleted = True

    def copy(self):
        return TextFile(self.name, self.path, self.date, self.size, self.title)


class ImageFile(FileSystemObject):
    def __init__(self, name, path, date, size, height, width):
        super().__init__(name, path, date, size)
        self.height = height
        self.width = width
        self.__type = "image"

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def type(self):
        return self.__type

    @height.setter
    def height(self, height):
        self.__height = height

    @width.setter
    def width(self, width):
        self.__width = width


    def get_info(self):
        print(f"File info: \nName: {self.name}, \nPath: {self.path}, \nDate: {self.date}, \nSize: {self.size}, \nHeight: {self.height}, \nWidth: {self.width}")

    def rename(self, new_name):
        self.name = new_name

    def delete(self):
        self.deleted = True

    def copy(self):
        return ImageFile(self.name, self.path, self.date, self.size, self.height, self.width)


class Folder(FileSystemObject):
    def __init__(self, name, path, date, size):
        super().__init__(name, path, date, size)
        self.__number_of_files = 0
        self.__objects: list[FileSystemObject] = []
        self.__type = "folder"

    @property
    def number_of_files(self):
        return self.__number_of_files

    @property
    def objects(self):
        return self.__objects.copy()

    @property
    def type(self):
        return self.__type


    def get_object_by_name(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def add_object(self, item: FileSystemObject):
        for obj in self.objects:
            if obj.name == item.name:
                raise ValueError(f"Duplicate object name: {item.name}")
        self.__number_of_files += 1
        self.__objects.append(item)

    def remove_object(self, name):
        obj = self.get_object_by_name(name)

        if obj is None:
            return None

        self.__objects.remove(obj)
        self.__number_of_files -= 1
        return obj

    def get_info(self):
        print(f"File info: \nName: {self.name}, \nPath: {self.path}, \nDate: {self.date}, \nSize: {self.size} \nNumber of files in this folder: {self.number_of_files}")

    def show_contents(self):
        if self.__number_of_files == 0:
            print("Folder is empty")
            return

        for obj in self.__objects:
            obj.get_info()
            print()

    def rename(self, new_name):
        self.name = new_name

    def delete(self):
        self.deleted = True
        for obj in self.__objects:
            obj.delete()
        self.__number_of_files = 0

    def copy(self):
        folder_copy = Folder(self.name, self.path, self.date, self.size)
        for obj in self.__objects:
            folder_copy.add_object(obj.copy())
        return folder_copy

if __name__ == "__main__":
    file = File("file", "C:\\", "22.04.2026", 100)
    text_file = TextFile("text_file", "C:\\", "22.04.2026", 300, "Title")
    img = ImageFile("img", "C:\\", "22.04.2026", 500, 100, 200)
    folder = Folder("folder", "C:\\", "22.04.2026", 100)

    file.get_info()
    print("\n--------------------------------\n")
    text_file.get_info()
    print("\n--------------------------------\n")
    img.get_info()
    print("\n--------------------------------\n")
    folder.get_info()
    print("\n--------------------------------\n")

    folder.add_object(file)
    folder.add_object(text_file)
    folder.add_object(img)

    folder.show_contents()
