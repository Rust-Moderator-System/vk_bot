import pytest
from _pytest.monkeypatch import MonkeyPatch

from services.server import ServerAPI
from tests.test_services.factories import PlayerFactory
from tests.utils import MockResponse
from utils.http.client import HTTPClient


@pytest.fixture
def player():
    return PlayerFactory.build()


@pytest.fixture
def players(count_instance: int):
    return PlayerFactory.batch(count_instance)


@pytest.fixture
def server_api():
    return ServerAPI()


@pytest.fixture
def mock_get_online_players(monkeypatch: MonkeyPatch):
    async def mock_get_online_players(*args, **kwargs):
        json_response = [player.dict() for player in PlayerFactory.batch(3)]
        return MockResponse(json_response)

    monkeypatch.setattr(HTTPClient, 'raw_request', mock_get_online_players)
