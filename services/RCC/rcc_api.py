import asyncio
from typing import Final

from app.core import settings
from services.RCC import RCCPlayer
from services.RCC.rcc_cache import RCCPlayerCache
from utils.http.api_client import APIClient


class RustCheatCheckAPI:
    API_URL: Final[str] = 'https://rustcheatcheck.ru/panel/api/'
    API_KEY: Final[str] = settings.RCC_KEY

    GET_PLAYER_ACTION: Final[str] = 'getInfo'

    def __init__(self):
        self.client = APIClient(base_url=self.API_URL)
        self._players_cache = RCCPlayerCache()

    async def get_player(self, steamid: str) -> RCCPlayer:
        if player := self._players_cache.get(steamid):
            return player
        player = await self.client.get(
                '',
                query=self._get_query(self.GET_PLAYER_ACTION, player=steamid),
                response_model=RCCPlayer,
            )
        self._players_cache.set(steamid, player)
        return player

    async def get_players(self, steamids: list[str]) -> list[RCCPlayer]:
        tasks = []
        for steamid in steamids:
            tasks.append(asyncio.ensure_future(self.get_player(steamid)))
        return await asyncio.gather(*tasks, return_exceptions=False)

    def _get_query(self, action: str, **kwargs):
        return {'action': action, 'key': self.API_KEY, **kwargs}
