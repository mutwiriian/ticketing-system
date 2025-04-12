from pydantic import BaseModel

class SponsorBody(BaseModel):
    name: str

class SponsorUpdateBody(BaseModel):
    name: str | None = None

