from pydantic import AnyUrl, BaseSettings, IPvAnyAddress
from vkbottle import Token


class Settings(BaseSettings):
    DEBUG: bool = True

    # VK SETTINTS
    SECRET_KEY: str = 'secret'

    ## MAIN BOT
    MAIN_BOT_TOKEN: Token
    MAIN_CONFIRMATION_CODE: str

    # SERVICES SETTINGS
    SERVER_API_URL: str
    RCC_KEY: str

    # WS SETTINGS
    PORT: int = 7777
    HOST: IPvAnyAddress | AnyUrl = '0.0.0.0'
    BEARER_TOKEN: str = 'BEARER'


settings = Settings(_env_file='.env')
