import pytest

from services.server import ServerAPI
from services.server.models import Player


@pytest.mark.asyncio
async def test_get_online_players(server_api: ServerAPI, count_instance: int, mock_get_online_players):
    players = await server_api.get_online_players()

    assert len(players) == count_instance
    assert all(isinstance(player, Player) for player in players)


@pytest.mark.asyncio
async def test_get_online_players_empty(server_api: ServerAPI, mock_empty_dict_response):
    players = await server_api.get_online_players()

    assert len(players) == 0
