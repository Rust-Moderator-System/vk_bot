from abc import ABC, abstractmethod


class ABCFilter(ABC):
    @abstractmethod
    def filter(self, data):
        ...


    def __call__(self, *args, **kwargs):
        return self.filter(*args, **kwargs)