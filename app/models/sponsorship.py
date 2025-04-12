from pydantic import BaseModel

class SponsorshipBody(BaseModel):
    event_id: int
    sponsor_id: int
    amount: float

class SponsorshipUpdateBody(BaseModel):
    amount: float | None = None
