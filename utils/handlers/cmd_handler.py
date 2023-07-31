import inspect
from typing import Any

from vkbottle.bot import Message, rules
from vkbottle.dispatch import ABCHandler, ABCRule
from loguru import logger

from utils.handlers.exceptions import CMDException
from utils.handlers.mixins import CmdHelpMixin, ExceptionHandleMixin, GetContextMixin, RenderMixin


class BaseCmdHandler(ABCHandler, GetContextMixin, CmdHelpMixin, RenderMixin, ExceptionHandleMixin):
    command_pattern: list[str] | str
    cmd: str
    rules: list[ABCRule] | None = None

    blocking: bool = True
    REPLY: bool = False

    def __init__(self):
        assert self.cmd and self.command_pattern, 'Нужно определить оба атрибута'

        self.pattern_rule = rules.VBMLRule(self.command_pattern)
        self.rules = self.rules or []
        self.help_text = self.get_help_text()

        self.context = {}

    async def filter(self, event: Message) -> bool | dict:
        self.context.clear()
        if not event.text.startswith(self.cmd):
            return False
        parsed_pattern = await self.parse_command(event)
        if parsed_pattern is False or self.is_help_command(event):
            return self.help_context
        self.context.update(parsed_pattern)
        context_result = await self.get_context(event)
        if context_result is False:
            return False
        return self.context

    async def handle(self, event: Message, **context) -> Any:
        try:
            await self.execute_handler(event, **context)
        except CMDException as exception:
            await self.send_exception(event, exception)
            logger.exception(exception)


    async def execute_handler(self, event: Message, **context) -> None:
        if context.get('help'):
            return await self.send_help(event)
        acceptable_keys = list(inspect.signature(self.handler).parameters.keys())[1:]
        acceptable_context = {k: v for k, v in context.items() if k in acceptable_keys}
        data = await self.handler(event, **acceptable_context)
        if self.render_class:
            text = self.render(data) if self.render_class else data
            await self.send_message(event, text)

    async def handler(self, message: Message, **context) -> Any:
        ...

    async def send_message(self, message: Message, text: str) -> None:
        if self.REPLY:
            return await message.reply(text)
        return await message.answer(text)

    async def parse_command(self, event: Message) -> str | bool | None:
        return await self.pattern_rule.check(event)
