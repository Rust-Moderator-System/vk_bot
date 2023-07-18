from services.RCC import RCCPlayer
from utils import Singleton


class RCCPlayerCache(Singleton):
    def __init__(self):
        self._cache = {}

    def get(self, steamid: str) -> RCCPlayer | None:
        return self._cache.get(steamid)

    def set(self, steamid: str, value: RCCPlayer) -> None:
        self._cache[steamid] = value

    def exists(self, steamid: str) -> bool:
        return steamid in self._cache

    def clear(self) -> None:
        self._cache.clear()

    def get_full(self) -> dict[str, RCCPlayer]:
        return self._cache
