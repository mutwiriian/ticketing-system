from typing import Annotated

from fastapi import Depends, HTTPException, status

import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from models.user import UserBody, UserUpdateBody
from database.tables import users_table

from auth.security import hash_password, oauth2_scheme
from auth.config import get_settings

settings = get_settings()

db_exception = HTTPException(
    detail="Database error occcured",
    status_code=status.HTTP_400_BAD_REQUEST
)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> int:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token,key=settings.SECRET,algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credential_exception
        return int(user_id)
    except InvalidTokenError:
        raise credential_exception

async def create_user(
        session: AsyncSession, user: UserBody) -> bool:
    user_dict = user.model_dump()
    hashed_password = hash_password(user_dict["password"])
        
    user_dict.update({"password": hashed_password})

    stmt = insert(users_table).values(user_dict)

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError:
        await session.close()
        raise db_exception
    
    if result.rowcount == 0:
        raise db_exception
    return True
    
async def get_user_by_id(session: AsyncSession, user_id: int) -> dict:
    stmt = select(users_table).where(users_table.c.id == user_id)

    try:
        result = await session.execute(stmt)
        user = result.mappings().first()

        if user is None:
                raise db_exception
        return dict(user)

    except SQLAlchemyError:
        await session.close()
        raise db_exception
    
async def get_user_by_name(session: AsyncSession,username: str) -> dict:
    stmt = select(users_table).where(users_table.c.user_name == username)

    try:
        result = await session.execute(stmt)
        user = result.mappings().first()

        if user is None:
                raise db_exception
        print(dict(user))
        return dict(user)

    except SQLAlchemyError:
        await session.close()
        raise db_exception
     
async def update_user(
    session:AsyncSession,
    user_id: int,
    user_update_body: UserUpdateBody
) -> bool:
    stmt = (
        update(users_table)
        .where(users_table.c.id == user_id)
        .values(**user_update_body.model_dump(exclude_unset=True))
    )

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise db_exception
    
    if result.rowcount == 0:
        raise db_exception
    
    return True

async def delete_user(
    session: AsyncSession,
    user_id: int
) -> bool:
    stmt = (
        delete(users_table)
        .where(users_table.c.id == user_id)
    )

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError:
        await session.close()
        raise db_exception

    if result.rowcount == 0:
        raise db_exception
    return True
