import dataclasses

from app.actions.abstract import AbstractAction
from app.actions.exceptions import CantGetOnlinePlayers
from services.server import Player
from services.server.server_api import ServerAPI


@dataclasses.dataclass
class GetOnlinePlayersAction(AbstractAction):
    first_join: int = 0

    SERVER_API: type[ServerAPI] = ServerAPI
    EXCEPTION = CantGetOnlinePlayers

    async def action(self) -> list[Player]:
        return await self.SERVER_API().get_online_players(self.first_join)
