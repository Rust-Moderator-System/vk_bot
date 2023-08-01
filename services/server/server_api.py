from typing import Final

from app.core import settings
from services.server import Player
from utils.http.api_client import APIClient


class ServerAPI:
    API_URL: Final[str] = settings.SERVER_API_URL

    ONLINE_PLAYERS_ENDPOINT: Final[str] = 'getOnlinePlayers.php'
    GET_PLAYERS_CHECK_ENDPOINT: Final[str] = 'getPlayersChecks.php'

    def __init__(self):
        self.client = APIClient(base_url=self.API_URL)

    async def get_online_players(self, first_join: int = 0) -> list[Player]:
        return await self.client.get(
            url=self.ONLINE_PLAYERS_ENDPOINT,
            query={'first_join': first_join},
            response_model=list[Player],
        )
    
    async def get_players_checks(self, steamids: list[str]) -> dict[str, int]:
        """Возвращает словарь, где ключ - steamid, а значение - время начало последней проверки"""
        return await self.client.post(
            url=self.GET_PLAYERS_CHECK_ENDPOINT,
            body={'ids': steamids},
            response_model=dict,
        )
