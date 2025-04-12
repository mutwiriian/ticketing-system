from pydantic import BaseModel

class TicketBody(BaseModel):
    show: str
    user_id: int
    price: int
    sold: bool
    event_id: int

class TicketUpdate(BaseModel):
    show: str | None = None
    user_id: int | None = None
    price: int | None = None
    sold: bool | None = None
    event_id: int | None = None
