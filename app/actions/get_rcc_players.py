import dataclasses

from app.actions.abstract import AbstractAction
from app.actions.exceptions import CantGetRCCPlayerInfo
from services.RCC import RCCPlayer
from services.RCC.rcc_api import RustCheatCheckAPI


@dataclasses.dataclass
class GetRCCPlayersAction(AbstractAction):
    steamids: list[str]

    RCC_API: type[RustCheatCheckAPI] = RustCheatCheckAPI
    EXCEPTION = CantGetRCCPlayerInfo

    async def action(self) -> list[RCCPlayer]:
        return await self.RCC_API().get_players(self.steamids)
