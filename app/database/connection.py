from typing import AsyncGenerator

from sqlalchemy import text

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import (
        AsyncEngine, AsyncSession, 
        AsyncConnection, async_sessionmaker
)

DB_URL = "postgresql+asyncpg://postgres:postgres@172.22.0.1:5432/tickets"

async_engine: AsyncEngine = create_async_engine(url=DB_URL,echo=True,pool_size=10,max_overflow=20)

async_session = async_sessionmaker(async_engine)

async def get_async_engine() -> AsyncEngine:
    return async_engine

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
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
