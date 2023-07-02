from vkbottle.bot import Message
from utils.handlers import BaseCmdHandler
from utils.labelers import BaseCmdLabeler


ping_labeler = BaseCmdLabeler()


@ping_labeler.message
class PingHandler(BaseCmdHandler):
    command_pattern = '/ping <text>'
    cmd = '/ping'

    async def handler(self, message: Message, text: str) -> None:
        await message.answer(text)
