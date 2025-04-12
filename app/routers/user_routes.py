from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database.connection import get_session
from models.user import UserBody, UserUpdateBody
from models.auth import Token

from auth.auth import generate_token

from operations.user_operations import (
        create_user, get_user_by_id,
        update_user, delete_user
)

from auth.auth import get_current_user

user_router = APIRouter(tags=["users"])

@user_router.post("/user")
async def create_user_route(
        session: Annotated[AsyncSession, Depends(get_session)], 
        user: UserBody) -> bool:
    return await create_user(session=session,user=user)

@user_router.get("/user")
async def get_user_route(
        session: Annotated[AsyncSession, Depends(get_session)],
        user_id: int = Depends(get_current_user)
):
    return await get_user_by_id(session=session,user_id=user_id)

@user_router.patch("/user")
async def update_user_route(
    session:Annotated[AsyncSession, Depends(get_session)],
    user_update_body: UserUpdateBody,
    user_id: int = Depends(get_current_user)
):
    return await update_user(
        session=session,
        user_id=user_id,
        user_update_body=user_update_body
    )

@user_router.delete("/user")
async def delete_user_route(
        session: Annotated[AsyncSession,Depends(get_session)],
        user_id: int = Depends(get_current_user)

):
    return await delete_user(
        session=session,
        user_id=user_id
    )

@user_router.post("/token")
async def login_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    token = await generate_token(
        session=session,
        form_data=form_data
        )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return token
