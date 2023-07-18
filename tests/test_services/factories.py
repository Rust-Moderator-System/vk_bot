from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from services.server import Player
from utils.random_gen import gen_steamid


class PlayerFactory(ModelFactory):
    __model__ = Player

    steamid = Use(gen_steamid)
