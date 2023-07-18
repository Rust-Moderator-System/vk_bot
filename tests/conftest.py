from typing import Final

import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests.utils import MockResponse
from utils.http.client import HTTPClient

pytest_plugins = ('pytest_asyncio',)


COUNT_INSTANCE: Final[int] = 3


@pytest.fixture
def count_instance():
    return COUNT_INSTANCE


@pytest.fixture
def mock_empty_dict_response(monkeypatch: MonkeyPatch):
    async def mock_empty_response(*args, **kwargs):
        return MockResponse({})

    monkeypatch.setattr(HTTPClient, 'raw_request', mock_empty_response)
