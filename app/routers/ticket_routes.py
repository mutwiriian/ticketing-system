from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from models.ticket import (
    TicketBody, TicketUpdate
)
from models.ticket_details import TicketDetailsBody

from operations.ticket_operations import (
    create_ticket, get_ticket, 
    update_ticket, delete_ticket,
    sell_ticket_to_user
)

from auth.security import get_current_user

ticket_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["tickets"])

@ticket_router.post("/ticket")
async def create_ticket_route(
    ticket: TicketBody, ticket_details: TicketDetailsBody,
    session: Annotated[AsyncSession,Depends(get_session)]
):
    return await create_ticket(
        session=session,
        ticket=ticket,
        ticket_details=ticket_details
    )

@ticket_router.get("/ticket")
async def get_ticket_route(
    ticket_id: int, 
    session: Annotated[AsyncSession,Depends(get_session)]
):
    ticket = await get_ticket(session=session,ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found!"
        )

    return ticket

@ticket_router.patch("/ticket")
async def update_ticket_route(
    ticket_id: int,
    update_data: TicketUpdate,
    session: Annotated[AsyncSession,Depends(get_session)]
):
    return await update_ticket(
        session=session,
        ticket_id=ticket_id,
        update_data=update_data
    )

@ticket_router.delete("/ticket")
async def delete_ticket_route(
    ticket_id: int,
    session: Annotated[AsyncSession,Depends(get_session)]
):
    return await delete_ticket(
        session=session,ticket_id=ticket_id
    )


@ticket_router.post("/sell_ticket")
async def sell_ticket_route(
        session: Annotated[AsyncSession, Depends(get_session)],
        user_name: str
):
    return await sell_ticket_to_user(
        session=session,
        user_name=user_name
    )
