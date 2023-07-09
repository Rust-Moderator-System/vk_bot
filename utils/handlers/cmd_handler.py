import inspect
from typing import Any

from vbml import Pattern
from vkbottle.bot import Message, rules
from vkbottle.dispatch import ABCHandler, ABCRule

from app.renders import ABCMessageRender


class BaseCmdHandler(ABCHandler):
    command_pattern: list[str] | str
    cmd: str 
    help_text: str | None = None
    rules: list[ABCRule] | None = None
    render_class: type[ABCMessageRender] | None = None

    blocking: bool = True
    REPLY: bool = False

    def __init__(self):
        assert self.cmd and self.command_pattern, 'Нужно определить оба атрибута'
        self.pattern_rule = rules.VBMLRule(self.command_pattern)
        self.rules = self.rules or []
        self.help_text = self.get_help_text()

        self.context = {}
        self._help_context = {'help': True} 

    async def filter(self, event: Message) -> bool | dict:
        if not event.text.startswith(self.cmd):
            return False
        parsed_pattern = await self.parse_command(event)
        if parsed_pattern is False or self.is_help_command(event):
            return self._help_context
        self.context.update(parsed_pattern)
        context_result = await self.get_context(event)
        if context_result is False:
            return False
        return self.context
            
    async def handle(self, event: Message, **context) -> Any:
        if context.get('help'):
            return await self.send_help(event)
        acceptable_keys = list(inspect.signature(self.handler).parameters.keys())[1:]
        acceptable_context = {k: v for k, v in context.items() if k in acceptable_keys}
        data = await self.handler(event, **acceptable_context)
        if data:
            text = self.render(data) if self.render_class else data
            await self.send_message(event, text)

             
    async def handler(self, message: Message) -> Any:
        ...

    def render(self, data: Any) -> str:
        return self.render_class(data).render()
    
    async def send_message(self, message: Message, text: str) -> None:
        if self.REPLY:
            return await message.reply(text)
        return await message.answer(text)
    
    async def send_help(self, message: Message) -> None:
        await message.answer(self.help_text)

    async def get_context(self, event: Message) -> None | bool:
        for rule in self.rules:
            result = await rule.check(event)
            if result is False or result is None:
                return False
            elif result is True:
                continue
            self.context.update(result)

    async def parse_command(self, event: Message) -> str | bool | None:
        return await self.pattern_rule.check(event)
    
    def is_help_command(self, event: Message) -> bool:
        only_args_text = event.text.replace(self.cmd, '').strip()
        if only_args_text == 'help':
            return True
        return False
    
    def get_help_text(self) -> str:
        if self.help_text:
            return self.format_help_text()
        return self._get_command_pattern_str()

    def format_help_text(self) -> str:
        command_pattern_str = self._get_command_pattern_str()
        return f'{command_pattern_str}\n{self.help_text}'
    

    def _get_command_pattern_str(self) -> str:
        if isinstance(self.command_pattern, list):
            return self.command_pattern[0]
        elif isinstance(self.command_pattern, str):
            return self.command_pattern
        return self.command_pattern