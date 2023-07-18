from pydantic import BaseModel


class Player(BaseModel):
    last_nickname: str
    first_join: int
    steamid: str
    server: int
