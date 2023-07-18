from vkbottle.bot import BotLabeler

from app.handlers.bans import bans_labelers
from app.handlers.ping import ping_labeler

labelers = [
    ping_labeler, *bans_labelers,
]
