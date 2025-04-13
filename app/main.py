from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.tables import metadata

from database.connection import create_database

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from auth.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    temp_engine = create_async_engine(
        url=settings.TEMP_DB_URL,
        isolation_level="AUTOCOMMIT"
        )

    try:
        async with temp_engine.connect() as temp_conn:
            await create_database(connection=temp_conn)
    finally:
        await temp_engine.dispose()

    app.state.engine = create_async_engine(url=settings.DB_URL,echo=True,pool_size=10,max_overflow=20)
    app.state.async_session = async_sessionmaker(app.state.engine)

    async with app.state.engine.begin() as connection:
        await connection.run_sync(metadata.create_all)
    
    yield

    await app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)

from routers.event_routes import event_router
from routers.sponsor_routes import sponsor_router
from routers.sponsorship_routes import sponsorship_router
from routers.ticket_routes import ticket_router
from routers.user_routes import user_router

app.include_router(event_router)
app.include_router(sponsor_router)
app.include_router(sponsorship_router)
app.include_router(ticket_router)
app.include_router(user_router)
