from abc import ABC, abstractmethod


class ABCMessageRender(ABC):
    @abstractmethod
    def render(self) -> str:
        ...
