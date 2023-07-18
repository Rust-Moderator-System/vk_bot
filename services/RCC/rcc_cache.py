from services.RCC import RCCPlayer
from utils import Singleton


class RCCPlayerCache(Singleton):
    def __init__(self):
        self._cache = {}

    def get(self, steamid: str):
        return self._cache.get(steamid)

    def set(self, steamid: str, value: RCCPlayer):
        self._cache[steamid] = value

    def exists(self, steamid: str):
        return steamid in self._cache

    def clear(self):
        self._cache.clear()

    def get_full(self):
        return self._cache
