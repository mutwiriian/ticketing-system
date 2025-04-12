from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.sponsor import SponsorBody, SponsorUpdateBody
from database.tables import sponsors_table

async def create_sponsor(session: AsyncSession,
                         sponsor: SponsorBody):
    stmt = insert(sponsors_table).values(**sponsor.model_dump())
    
    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database error occured: {e}")

        return False
    
    if result.rowcount == 0:
        return False
    return True

async def get_sponsor(session: AsyncSession, sponsor_id: int) -> dict | bool:
    stmt = select(sponsors_table).where(sponsors_table.c.id == sponsor_id)

    try:
        result = await session.execute(stmt)
    except SQLAlchemyError as e:
        await session.close()
        print(f"Databse error occurred: {e}")

        return False
    result = result.mappings().first()
    if result is None:
        return False
    return dict(result)

async def update_sponsor(
        session: AsyncSession, sponsor_id: int,
        sponsor_update_body: SponsorUpdateBody) -> bool:
    stmt = (
        update(sponsors_table)
        .where(sponsors_table.c.id == sponsor_id)
        .values(**sponsor_update_body.model_dump(exclude_unset= True))
    )

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database error occurred: {e}")

        return False
    
    if result.rowcount == 0:
        return False

    return True

async def delete_sponsor(session: AsyncSession, sponsor_id: int) -> bool:
    stmt = delete(sponsors_table).where(sponsors_table.c.id == sponsor_id)

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database error occurred {e}")
        return False
    
    if result.rowcount == 0:
        return False
    return True



