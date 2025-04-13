from pydantic import BaseModel

class TicketBody(BaseModel):
    show: str
    price: int
    sold: bool = False
    event_id: int

class TicketUpdate(BaseModel):
    show: str | None = None
    price: int | None = None
    sold: bool | None = False
    event_id: int | None = None
