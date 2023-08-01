from vkbottle.bot import Message

from app.actions import GetOnlinePlayersAction, GetPlayersCheckAction, GetRCCPlayersAction
from app.core.constants import DAYS_SHOW_BANS
from app.filtres import execute_filters
from app.filtres.rcc_filtres import (
    RCCFilterActiveBan,
    RCCFilterBanByTime,
    RCCFilterBanReason,
    RCCFilterEmpty,
    RCCFilterNotChecked,
    RCCFilterNotInExclude,
)
from app.renders import RCCBansMessageRender
from services.RCC import RCCPlayer
from utils.handlers import BaseCmdHandler
from utils.labelers import BaseCmdLabeler

players_bans_labeler = BaseCmdLabeler()



@players_bans_labeler.message
class ExcludeSteamids(BaseCmdHandler):
    command_pattern = ['/bans exclude <exclude_steamid>']
    cmd = '/bans exclude'

    help_text = 'Добавить steamid в список игроков, которые не будут отображаться в /bans'

    exclude_steamids: set[str] = set()

    async def handler(self, message: Message, exclude_steamid: str) -> None:
        self.exclude_steamids.add(exclude_steamid)
        await message.reply(f'Добавлено {exclude_steamid} в список исключений `/bans`')


@players_bans_labeler.message
class GetPlayersBans(BaseCmdHandler):
    command_pattern = ['/bans <days:int>', '/bans <days:int> <filter:int>', '/bans', ]
    cmd = '/bans'

    help_text = 'Получить список игроков на сервере с банами'
    render_class = RCCBansMessageRender


    async def handler(self, message: Message) -> list[RCCPlayer]:
        online_players = await GetOnlinePlayersAction().execute()
        self.players_steamid = [player.steamid for player in online_players[:50]]

        rcc_players = await GetRCCPlayersAction(self.players_steamid).execute()

        if self.is_filter:
            return await self.use_filters(rcc_players)
        return rcc_players

    async def use_filters(self, players: list[RCCPlayer]) -> list[RCCPlayer]:
        days_to_show_ban = self.context.get('days', DAYS_SHOW_BANS)
        checks_on_server = await GetPlayersCheckAction(self.players_steamid).execute()
        exclude_steamids = getattr(ExcludeSteamids, 'exclude_steamids', [])
        print(checks_on_server)
        filtres = [
            RCCFilterEmpty(), # Обязательно первым идет
            RCCFilterNotInExclude(exclude_steamids),
            RCCFilterNotChecked(checks_on_server),
            RCCFilterActiveBan(),
            RCCFilterBanByTime(days_to_show_ban),
            RCCFilterBanReason(),
        ]
        return [player for player in players if execute_filters(player, filtres)]

    @property
    def is_filter(self) -> bool:
        return bool(self.context.get('filter', True))