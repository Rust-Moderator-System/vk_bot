from vkbottle.bot import BotLabeler
from vkbottle import Bot, Token
from app.handlers import main_handlers, report_handlers
from app.core import settings

class BaseRoomBot(Bot):
    TOKEN: Token
    BOT_LABELERS: list[BotLabeler]
    
    def __init__(self) -> None:
        super().__init__(self.TOKEN)
        self._load_labelers()

    def _load_labelers(self) -> None:
        for labeler in self.BOT_LABELERS:
            self.labeler.load(labeler)



class MainBot(BaseRoomBot):
    TOKEN = settings.MAIN_BOT_TOKEN
    BOT_LABELERS = main_handlers


class ReportBot(BaseRoomBot):
    TOKEN = settings.REPORT_BOT_TOKEN
    BOT_LABELERS = report_handlers


main_bot = MainBot()
report_bot = ReportBot()
