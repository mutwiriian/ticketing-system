
from pydantic import BaseModel

class TicketDetailsBody(BaseModel):
    seat: int
    ticket_type: str

class TicketDetailsUpdateBody(BaseModel):
    seat: int | None = None
    ticket_type: str | None = None

