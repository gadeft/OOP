from abc import ABC, abstractmethod


class File(ABC):
    @property
    @abstractmethod
    def size(self):
        pass
