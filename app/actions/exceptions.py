from typing import Final

from utils.handlers.exceptions import CMDException


class CantGetOnlinePlayers(CMDException):
    message: Final[str] = 'Не удалось получить список игроков онлайн'


class CantGetRCCPlayerInfo(CMDException):
    message: Final[str] = 'Не удалось получить информацию об игроках из чекера'


class CantGetPlayersChecks(CMDException):
    message: Final[str] = 'Не удалось получить информацию о проверках игроков'