from typing import Any

from vkbottle.bot import Message

from app.renders.abc import ABCMessageRender
from utils.handlers.exceptions import CMDException


class GetContextMixin:
    async def get_context(self, event: Message) -> None | bool:
        for rule in self.rules:
            result = await rule.check(event)
            if result is False or result is None:
                return False
            elif result is True:
                continue
            self.context.update(result)


class CmdHelpMixin:
    help_text: str | None = None
    help_context = {'help': True}

    async def send_help(self, message: Message) -> None:
        await message.answer(self.help_text)

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


class RenderMixin:
    render_class: type[ABCMessageRender] | None = None

    def render(self, data: Any) -> str:
        return self.render_class(data).render()


class ExceptionHandleMixin:
    async def send_exception(self, message: Message, exception: CMDException) -> None:
        await message.answer(exception.message)
