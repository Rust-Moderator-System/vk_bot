from vkbottle import Bot, Token
from vkbottle.bot import BotLabeler

from app.core import settings
from app.handlers import labelers


class BaseBot(Bot):
    TOKEN: Token
    BOT_LABELERS: list[BotLabeler]

    def __init__(self) -> None:
        super().__init__(self.TOKEN)
        self._load_labelers()

    def _load_labelers(self) -> None:
        for labeler in self.BOT_LABELERS:
            self.labeler.load(labeler)


class MainBot(BaseBot):
    TOKEN = settings.MAIN_BOT_TOKEN
    BOT_LABELERS = labelers


main_bot = MainBot()
