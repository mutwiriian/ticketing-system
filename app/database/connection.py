from typing import AsyncGenerator

from fastapi import Request

from sqlalchemy import text

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncConnection, async_sessionmaker
)

from auth.config import get_settings

settings = get_settings()

async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_database(connection: AsyncConnection):
    try:
        await connection.execute(text("COMMIT"))

        result = await connection.execute(
            text("select 1 from pg_database where datname = 'tickets'")
        )

        exists = result.scalar()

        if not exists:
            await connection.execute(text("create database tickets"))

    except Exception:
        raise 
