from vkbottle.bot import BotLabeler

from .ping import ping_labeler

handlers: list[BotLabeler] = [ping_labeler]