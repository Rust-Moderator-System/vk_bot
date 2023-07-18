from abc import ABC, abstractmethod

from utils.handlers.exceptions import CMDException


class AbstractAction(ABC):
    EXCEPTION = CMDException

    @abstractmethod
    async def action(self):
        ...

    async def execute(self):
        try:
            return await self.action()
        except Exception:
            self.raise_exception()

    def raise_exception(self):
        raise self.EXCEPTION

