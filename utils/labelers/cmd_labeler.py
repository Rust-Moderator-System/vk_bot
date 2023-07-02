from typing import Any

from utils.handlers import BaseCmdHandler
from vkbottle.bot import BotLabeler, rules


class BaseCmdLabeler(BotLabeler):
    def message(self, handler: type[BaseCmdHandler]) -> None:
        self.message_view.handlers.append(handler())

    def chat_message(self, handler: type[BaseCmdHandler]) -> None:
        handler_instance = handler()
        handler_instance.rules.append(rules.PeerRule())
        self.message_view.handlers.append(handler_instance)
    
    def private_message(self, handler: type[BaseCmdHandler]) -> None:
        handler_instance = handler()
        handler_instance.rules.append(rules.PeerRule(from_chat=False))
        self.message_view.handlers.append(handler_instance)

    def raw_event(self, *args, **kwargs):
        raise NotImplementedError('raw event not available for `CmdLabeler`')