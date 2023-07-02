import inspect
from typing import Any

from vkbottle.bot import Message, rules
from vbml import Pattern
from vkbottle.dispatch import ABCHandler, ABCRule

from app.renders import ABCMessageRender


class BaseCmdHandler(ABCHandler):
    command_pattern: str
    cmd: str 
    help_text: str | None = None
    rules: list[ABCRule] | None = None
    render: type[ABCMessageRender] | None = None

    blocking: bool = True
    REPLY: bool = False

    def __init__(self):
        assert self.cmd and self.command_pattern, 'Нужно определить оба атрибута'
        self.pattern = Pattern(self.command_pattern)
        self.rules = self.rules or []
        self.help_text = self.help_text or self.command_pattern

        self.context = {}

    async def filter(self, event: Message):
        if not event.text.startswith(self.cmd):
            return False
        parsed_pattern = await self.parse_command(event)
        if not parsed_pattern:
            return await self.send_help(event)
        self.context.update(parsed_pattern)
        await self.get_context(event)
        return self.context
            
    async def handle(self, event: Message, **context) -> Any:
        acceptable_keys = list(inspect.signature(self.handler).parameters.keys())[1:]
        acceptable_context = {k: v for k, v in context.items() if k in acceptable_keys}
        return await self.handler(event, **acceptable_context)
                    
    async def handler(self, message: Message) -> Any:
        ...

    async def get_context(self, event) -> None:
        for rule in self.rules:
            result = await rule.check(event)
            if result is False or result is None:
                return False
            elif result is True:
                continue
            self.context.update(result)
        
    async def send_help(self, event: Message) -> False:
        await event.reply(self.help_text)
        return False

    async def parse_command(self, event: Message) -> str | bool | None:
        return await rules.VBMLRule(self.pattern).check(event)