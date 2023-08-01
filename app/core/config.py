from datetime import timedelta, timezone

from pydantic import AnyUrl, BaseSettings, IPvAnyAddress
from vkbottle import Token


class Settings(BaseSettings):
    DEBUG: bool = True
    TIMEZONE = timezone(timedelta(hours=3), name='Europe/Moscow')

    # VK SETTINTS
    SECRET_KEY: str = 'secret'

    # MAIN BOT
    MAIN_BOT_TOKEN: Token
    MAIN_CONFIRMATION_CODE: str
    WIPE_TIME: int = 14

    # SERVICES SETTINGS
    SERVER_API_URL: str
    RCC_KEY: str

    # WS SETTINGS
    PORT: int = 7777
    HOST: IPvAnyAddress | AnyUrl = '0.0.0.0'
    BEARER_TOKEN: str = 'BEARER'


settings = Settings(_env_file='.env')
