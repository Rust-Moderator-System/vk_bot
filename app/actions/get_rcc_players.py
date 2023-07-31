import dataclasses

from loguru import logger
from app.actions.abstract import AbstractAction
from app.actions.exceptions import CantGetRCCPlayerInfo
from services.RCC import RCCPlayer
from services.RCC.rcc_api import RustCheatCheckAPI


@dataclasses.dataclass
class GetRCCPlayersAction(AbstractAction):
    steamids: list[str]

    RCC_API: type[RustCheatCheckAPI] = RustCheatCheckAPI
    EXCEPTION = CantGetRCCPlayerInfo
    PLAYERS_STEP = 30

    async def action(self) -> list[RCCPlayer]:
        players = []
        for i in range(0, len(self.steamids), self.PLAYERS_STEP):
            players.extend(await self.RCC_API().get_players(self.steamids[i:i + self.PLAYERS_STEP]))
        return players
    
    def raise_exception(self, from_exception: Exception):
        logger.exception(from_exception)
    
