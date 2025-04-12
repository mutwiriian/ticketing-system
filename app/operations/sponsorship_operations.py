from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.sponsorship import SponsorshipBody, SponsorshipUpdateBody
from database.tables import sponsorships_table

async def create_sponsorship(
    session: AsyncSession, 
    sponsorship_body: SponsorshipBody) -> bool:
    stmt = insert(sponsorships_table).values(**sponsorship_body.model_dump())

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


async def get_sponsorship(
        session: AsyncSession, sponsorship_id: int) -> dict | bool:
    stmt = (
            select(sponsorships_table)
            .where(sponsorships_table.c.id == sponsorship_id)
    )

    try:
        result = await session.execute(stmt)
    except SQLAlchemyError as e:
        await session.close()
        print(f"Database error occurred: {e}")
        return False

    result = result.mappings().first()
    if result is None:
        return False
    return dict(result)

async def update_sponsorship(
    session: AsyncSession, sponsorship_id: int, 
    sponsorship_update_body: SponsorshipUpdateBody) -> bool:

    stmt = (
        update(sponsorships_table)
        .where(sponsorships_table.c.id == sponsorship_id)
        .values(**sponsorship_update_body.model_dump(exclude_unset=True))
    )

    try: 
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database errror occurred: {e}")
        return False

    if result.rowcount == 0:
        return False
    return True

async def delete_sponsorship(
        session: AsyncSession, sponsorship_id: int) -> bool:
    stmt = delete(sponsorships_table).where(sponsorships_table.c.id == sponsorship_id)

    try:
        result = await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database error occurres: {e}")
        return False
    if result.rowcount == 0:
        return False

    return True


