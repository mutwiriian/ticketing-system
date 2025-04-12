from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from models.sponsor import (
    SponsorBody, SponsorUpdateBody
)

from operations.sponsor_operations import (
    create_sponsor, get_sponsor, update_sponsor, delete_sponsor
)

from auth.auth import get_current_user

sponsor_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["sponsors"])

@sponsor_router.post("/sponsor")
async def create_sponsor_route(
        session: Annotated[AsyncSession, Depends(get_session)],
        sponsor: SponsorBody):
    return await create_sponsor(session=session,sponsor=sponsor)

@sponsor_router.get("/sponsor")
async def get_sponsor_route(
    session: Annotated[AsyncSession,Depends(get_session)],  
    sponsor_id: int
):
    sponsor = get_sponsor(session=session,sponsor_id=sponsor_id)
    if sponsor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found!"
            )
    return sponsor


@sponsor_router.patch("/sponsor")
async def update_sponsor_route(
    session: Annotated[AsyncSession, Depends(get_session)],
    sponsor_id: int,sponsor_update_body: SponsorUpdateBody
):
    return await update_sponsor(
        session=session,sponsor_id=sponsor_id,
        sponsor_update_body=sponsor_update_body
    )

@sponsor_router.delete("/sponsor")
async def delete_sponsor_route(
    session: Annotated[AsyncSession, Depends(get_session)],
    sponsor_id: int
):
    return await delete_sponsor(session=session,sponsor_id=sponsor_id)

