from vkbottle.bot import Message

from utils.handlers import BaseCmdHandler
from utils.handlers.exceptions import TestCMDExpcetion
from utils.labelers import BaseCmdLabeler

ping_labeler = BaseCmdLabeler()


@ping_labeler.message
class PingHandler(BaseCmdHandler):
    command_pattern = ['/ping <text>', '/ping']
    cmd = '/ping'

    help_text = 'Команда, которая вернет тот текст, который ты написал боту'

    async def handler(self, message: Message, text: str = 'pong') -> str:
        if text == 'exception':
            raise TestCMDExpcetion()
        return text
