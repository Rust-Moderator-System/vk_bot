import dataclasses
import time

from app.core.constants import RUST_SERVERS_NAMES
from services.RCC import RCCBan, RCCPlayer

from .abc import ABCMessageRender


@dataclasses.dataclass
class RCCBansMessageRender(ABCMessageRender):
    players: list[RCCPlayer]

    now_time: float = dataclasses.field(default_factory=time.time)

    def render(self) -> str:
        if not self.players:
            return 'На сервере нет игроков с банами'
        text = 'Игроки с банами\n'
        for player in self.players:
            bans_info = self._get_bans_info(player.bans)
            text += f'{player.steamid}: {bans_info}\n'
        return text

    def _get_bans_info(self, bans: list[RCCBan]) -> str:
        text = ''
        for ban in bans:
            after_ban_time = self._get_after_ban_time(ban)
            server_name = self._short_server_name(ban.server_name)
            text += f'{server_name}({after_ban_time})'
        return text

    def _get_after_ban_time(self, ban: RCCBan) -> str:
        time_passed = self.now_time - ban.ban_date
        return str(int(time_passed // 86400))

    def _short_server_name(self, full_server_name: str) -> str:
        lower_server_name = full_server_name.lower()
        for short_server_name in RUST_SERVERS_NAMES:
            if short_server_name.lower() in lower_server_name:
                return short_server_name

        if 'GLOBAL' in full_server_name:
            return full_server_name.replace('[GLOBAL]', '')[0:15]
        return full_server_name[:15]