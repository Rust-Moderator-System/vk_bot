import dataclasses
import time

from app.core.constants import AVAILABLE_BAN_REASONS, NOT_AVAILABLE_BAN_REASONS, RCC_SERVER_NAMES, SECONDS_IN_DAY
from app.filtres.abc import ABCFilter
from services.RCC import RCCBan, RCCPlayer


@dataclasses.dataclass
class RCCFilterNotInExclude(ABCFilter):
    exclude_steamids: set[str]

    def filter(self, player: RCCPlayer) -> bool:
        return not player.steamid in self.exclude_steamids


class RCCFilterEmpty(ABCFilter):
    def filter(self, player: RCCPlayer) -> bool:
        return player.steamid and player.bans

@dataclasses.dataclass

class RCCFilterNotChecked(ABCFilter):
    checks_on_server: dict[str, int]

    def filter(self, player: RCCPlayer) -> bool:
        last_bans: RCCBan = max(player.bans, key=lambda ban: ban.ban_time)
        if server_check := self.checks_on_server.get(last_bans.server_name):
            if server_check > last_bans.ban_time:
                return False

        for check in player.checks:
            if not check.server_name:
                continue
            if not check.server_name.lower() in RCC_SERVER_NAMES:
                continue
            if check.time > last_bans.ban_time:
                return False
        return True


@dataclasses.dataclass
class RCCFilterBanByTime(ABCFilter):
    days: int

    def filter(self, player: RCCPlayer) -> bool:
        bans = player.bans
        available_time = time.time() - self.days * SECONDS_IN_DAY
        bans = [ban for ban in bans if ban.ban_time > available_time]
        player.bans = bans
        return bool(bans)


@dataclasses.dataclass
class RCCFilterBanExcludeServers(ABCFilter):
    exclude_servers: list[str]

    def __post_init__(self):
        self.exclude_servers = [server.lower() for server in self.exclude_servers]

    def filter(self, player: RCCPlayer) -> bool:
        bans = player.bans
        bans = [ban for ban in bans if not ban.server_name.lower() in self.exclude_servers]
        player.bans = bans
        return bool(bans)


@dataclasses.dataclass
class RCCFilterBanReason(ABCFilter):
    available_reasons: list[str] = dataclasses.field(default_factory=lambda: AVAILABLE_BAN_REASONS)
    not_available_reasons: list[str] = dataclasses.field(default_factory=lambda: NOT_AVAILABLE_BAN_REASONS)

    def __post_init__(self):
        self.available_reasons = [reason.lower() for reason in self.available_reasons]
        self.not_available_reasons = [reason.lower() for reason in self.not_available_reasons]

    def filter(self, player: RCCPlayer) -> bool:
        bans = player.bans
        bans = [ban for ban in bans if ban.reason.lower() in self.available_reasons]
        bans = [ban for ban in bans if not ban.reason.lower() in self.not_available_reasons]
        player.bans = bans
        return bool(bans)


class RCCFilterActiveBan(ABCFilter):
    def filter(self, player: RCCPlayer) -> bool:
        bans = player.bans
        bans = [ban for ban in bans if not ban.active]
        player.bans = bans
        return bool(bans)
