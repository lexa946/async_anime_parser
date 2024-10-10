from pydantic import BaseModel


class SAnimeSeria(BaseModel):
    name: str
    url: str
    episode: str
    season: str|None = None

