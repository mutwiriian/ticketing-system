from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from models.event import (
    EventBody, EventUpdateBody
)

from operations.event_operations import (
    create_event, get_event, get_events_with_sponsors,
    update_event, delete_event
)

from auth.auth import get_current_user

event_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["events"])

@event_router.post("/event", response_model=None)
async def create_event_route(
    session:Annotated[AsyncSession,Depends(get_session)],
    event: EventBody
    ):
    return await create_event(
        session=session,
        event=event
    )

@event_router.get("/event")
async def get_event_route(
        session: Annotated[AsyncSession, Depends(get_session)],
        event_id: int):
    event = await get_event(session=session,event_id=event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found!"
        )
    
    return event

@event_router.get("/events_with_sponsors")
async def get_events_with_sponsor_route(session: Annotated[AsyncSession,Depends(get_session)]):
    return await get_events_with_sponsors(session=session)

@event_router.patch("/event")
async def update_event_route(
        session: Annotated[AsyncSession, Depends(get_session)],
        event_id: int, event_update_body: EventUpdateBody):
    return await update_event(
        session=session,event_id=event_id,
        event_update_body=event_update_body)

@event_router.delete("/event")
async def delete_event_route(
        session: Annotated[AsyncSession,Depends(get_session)],
        event_id: int):
    return await delete_event(session=session,event_id=event_id)


