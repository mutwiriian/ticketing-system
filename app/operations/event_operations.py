from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.event import (
    EventBody, EventUpdateBody
)
from database.tables import events_table,sponsors_table, sponsorships_table
from operations.user_operations import db_exception

async def create_event(session: AsyncSession,event: EventBody) -> bool:
    stmt = insert(events_table).values(**event.model_dump())
    try:
        result =  await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise db_exception

    if result.rowcount == 0:
        return False
    return True

async def get_event(session: AsyncSession, event_id: int) -> dict | bool:
    stmt = select(events_table).where(events_table.c.id == event_id)
    
    try:
        result = await session.execute(stmt)
    except SQLAlchemyError as e:
        await session.close()
        raise db_exception

    result = result.mappings().first()
    if result is None:
        return False
    
    return dict(result)

async def get_events_with_sponsors(session: AsyncSession):
    # stmt = (
    #     select(events_table,sponsorships_table)
    #     .where(events_table.c.id == sponsorships_table.c.event_id)
    # )
    stmt = (
        select(
            events_table.c.name.label("event_name"),
            sponsors_table.c.name.label("sponsor_name"),
            sponsorships_table.c.amount).select_from(
            events_table.join(
                sponsorships_table,
                events_table.c.id == sponsorships_table.c.id
            ).join(
                sponsors_table,
                sponsors_table.c.id == sponsorships_table.c.sponsor_id
            )
        )
    )

    try:
        result = await session.execute(stmt)
    except SQLAlchemyError as e:
        await session.close()
        raise db_exception
    
    events = result.mappings().all()
    return events

async def update_event(
        session: AsyncSession,event_id:
        int, event_update_body: EventUpdateBody) -> bool:
    stmt = (
        update(events_table)
        .where(events_table.c.id == event_id)
        .values(
            **event_update_body.model_dump(exclude_unset=True)
        )
    )
    
    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise db_exception
    
    if result.rowcount == 0:
        return False
    return True

async def delete_event(session: AsyncSession,event_id: int) -> bool:
    stmt = delete(events_table).where(events_table.c.id == event_id)

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise db_exception

    if result.rowcount == 0:
        return False
    return True
