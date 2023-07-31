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
        except Exception as exception:
            self.raise_exception(exception)

    def raise_exception(self, from_exception: Exception):
        raise self.EXCEPTION from from_exception

