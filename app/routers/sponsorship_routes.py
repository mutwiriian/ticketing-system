from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from models.sponsorship import (
    SponsorshipBody, SponsorshipUpdateBody,
)

from operations.sponsorship_operations import (
    create_sponsorship, get_sponsorship,
    update_sponsorship, delete_sponsorship
)

from auth.auth import get_current_user

sponsorship_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["sponsorships"])

@sponsorship_router.post("/sponsorship")
async def create_sponsorship_route(
    session: Annotated[AsyncSession, Depends(get_session)],
    sponsorship_body: SponsorshipBody
):
    return await create_sponsorship(
        session=session,
        sponsorship_body=sponsorship_body
)

@sponsorship_router.get("/sponsorship")
async def get_sponsorship_route(
    session: Annotated[AsyncSession, Depends(get_session)],
    sponsorship_id: int
):
    return await get_sponsorship(session=session, sponsorship_id=sponsorship_id)


@sponsorship_router.patch("/sponsorship")
async def update_sponsorship_route(
    session: Annotated[AsyncSession, Depends(get_session)],
        sponsorship_id: int, sponsorship_update_body: SponsorshipUpdateBody
):
     return await update_sponsorship(
        session=session,sponsorship_id=sponsorship_id,
         sponsorship_update_body=sponsorship_update_body
    )

@sponsorship_router.delete("/sponsorship")
async def delete_sponsorship_route(
    session: Annotated[AsyncSession, Depends(get_session)],
    sponsorship_id: int
):
    return await delete_sponsorship(session=session, sponsorship_id=sponsorship_id)

