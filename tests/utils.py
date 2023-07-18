from typing import Any


class MockResponse:
    def __init__(
        self,
        json_data: Any = None,
        status_code: int = 200,
    ):
        self.status_code = status_code
        self.json_data = json_data

    async def json(self):
        return self.json_data
