from typing import Never

from vkbottle.bot import BotLabeler, rules

from utils.handlers import BaseCmdHandler


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

    def raw_event(self, *args, **kwargs) -> Never:
        raise NotImplementedError('raw event not available for `CmdLabeler`')
