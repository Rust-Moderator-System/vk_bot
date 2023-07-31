from pydantic import BaseModel, Field


class Player(BaseModel):
    last_nickname: str = Field(alias='nickname')
    first_join: int
    steamid: str = Field(alias='steam_id')
    server: int
