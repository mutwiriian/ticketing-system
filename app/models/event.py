from pydantic import BaseModel

class EventBody(BaseModel):
    name: str

class EventUpdateBody(BaseModel):
    name: str | None = None

class Event(EventBody):
    id: int

