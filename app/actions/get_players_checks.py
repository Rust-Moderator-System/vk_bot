import dataclasses
from app.actions.abstract import AbstractAction
from app.actions.exceptions import CantGetPlayersChecks
from services.server import Player
from services.server.server_api import ServerAPI


@dataclasses.dataclass
class GetPlayersCheckAction(AbstractAction):
    steamids: list[str]

    SERVER_API: type[ServerAPI] = ServerAPI
    EXCEPTION = CantGetPlayersChecks

    async def action(self) -> list[Player]:
        return await self.SERVER_API().get_players_checks(self.steamids)    