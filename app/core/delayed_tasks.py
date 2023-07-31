import asyncio
from datetime import datetime, timedelta

from loguru import logger

from app.core import settings
from services.server.server_api import ServerAPI
from services.RCC.rcc_api import RustCheatCheckAPI
from services.RCC.rcc_cache import RCCPlayerCache


FRIDAY = 4
MONDAY = 0


class CheckJoinedPlayersOnServer:
    SECONDS_TO_CHECK_JOINED_PLAYERS = 10 * 60 # 10 minutes

    def __init__(self) -> None:
        self._previous_check_players_online: set[int] | None = None
        self._server_api = ServerAPI
        self._rcc_api = RustCheatCheckAPI()
    
    async def __call__(self):
        while True:
            await asyncio.sleep(self.SECONDS_TO_CHECK_JOINED_PLAYERS)
            await self._check_joined_players()
    
    async def _check_joined_players(self) -> None:
        logger.info('Checks joined players')
        online_players_steamid = await self._server_api.get_online_players()
        joined_players = self._get_joined_players(online_players_steamid)
        self._set_new_joined_players(joined_players)
        await self._rcc_api.get_players(joined_players)  # only for cache

    def _get_joined_players(self, online_players_steamids: list[int]) -> list[int]:
        if self._previous_check_players_online is None:
            return online_players_steamids

        joined_players = [
            steamid for steamid in online_players_steamids if steamid not in self._previous_check_players_online
        ]
        return joined_players

    def _set_new_joined_players(self, joined_players: list[int]) -> None:
            self._previous_check_players_online = set(joined_players)


class ClearRCCCacheEveryWipe:
    def __init__(self) -> None:
        self._rcc_cache = RCCPlayerCache()

    async def __call__(self) -> None:
            while True:
                await asyncio.sleep(self._seconds_to_next_wipe())
                self._rcc_cache.clear()

    def _seconds_to_next_wipe(self) -> int:
        next_wipe = self.get_next_wipe_day()
        time_now = datetime.now(tz=settings.TIMEZONE)
        seconds_to_next_wipe = (next_wipe - time_now).total_seconds()
        logger.info(f'Seconds to next wipe {seconds_to_next_wipe}')
        return seconds_to_next_wipe

    def get_next_wipe_day(self) -> datetime:
            time_now = datetime.now(tz=settings.TIMEZONE)
            if time_now.weekday() > FRIDAY:
                return self._monday_wipe_date(time_now)
            else:
                return self._friday_wipe_date(time_now)

    def _monday_wipe_date(self, time_now: datetime) -> datetime:
        days_to_monday = self._days_to_next_day(time_now, MONDAY)
        wipe_day = time_now + timedelta(days=days_to_monday)
        return datetime(
            year=wipe_day.year,
            month=wipe_day.month,
            day=wipe_day.day,
            hour=settings.WIPE_TIME,
            tzinfo=settings.TIMEZONE,
        )

    def _friday_wipe_date(self, time_now: datetime) -> datetime:
        days_to_friday = self._days_to_next_day(time_now, FRIDAY)
        wipe_day = time_now + timedelta(days=days_to_friday)
        return datetime(
            year=wipe_day.year,
            month=wipe_day.month,
            day=wipe_day.day,
            hour=settings.WIPE_TIME,
            tzinfo=settings.TIMEZONE,
        )

    def _days_to_next_day(self, date_now: datetime, day_of_week: int) -> int:
        days_to_day_of_week = day_of_week - date_now.weekday()
        if days_to_day_of_week <= 0:
            days_to_day_of_week += 7
        return days_to_day_of_week

def run_delayed_tasks() -> None:
    for task in delayed_tasks:
        asyncio.ensure_future(task())



delayed_tasks = [ClearRCCCacheEveryWipe(), CheckJoinedPlayersOnServer()]