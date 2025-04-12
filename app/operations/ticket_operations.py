from fastapi import Depends 

from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.ticket import (
    TicketBody, TicketUpdate,
)
from models.ticket_details import(
    TicketDetailsBody, TicketDetailsUpdateBody,
)
from database.tables import tickets_table, ticket_details_table
from operations.user_operations import db_exception

from auth.security import get_current_user

async def create_ticket(
    session: AsyncSession,
    ticket: TicketBody,
    ticket_details: TicketDetailsBody | None,
    user_id: int =  Depends(get_current_user)
) -> bool:
    tickets_stmt = (
        insert(tickets_table)
        .values(
            **ticket.model_dump(),
            user_id = user_id
        ).returning(tickets_table.c.id)
    )
    
    try:
        ticket_id = await session.execute(tickets_stmt)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise db_exception

    if ticket_id is None:
        return False

    if ticket_details is not None:
        stmt = (
            insert(ticket_details_table)
            .values(
                 **ticket_details.model_dump(),
                ticket_id=ticket_id
            )
        )
        
        try:
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:
                    return False
        except SQLAlchemyError:
            await session.rollback()
            raise db_exception

    
    else:
        stmt = (
            insert(ticket_details_table)
            .values(
                seat=None,
                ticket_type=None
            )
        )
        
        try:
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:
                return False
        except SQLAlchemyError:
                await session.rollback()

                return False
   
    return True

async def get_ticket(session: AsyncSession,ticket_id: int) -> dict | bool:
    stmt = (
        select(tickets_table)
        .where(tickets_table.c.id == ticket_id)
    )

    try:
        result = await session.execute(stmt)
    except SQLAlchemyError as e:
        await session.close()
        print(f"Database error occurred: {e}")
        return False
        
    ticket = result.mappings().first()
    if ticket is None:
        return False
    return dict(ticket)


async def update_ticket(session: AsyncSession,
                        ticket_id: int, update_data: TicketUpdate) -> bool:
    stmt = (
        update(tickets_table)
        .where(tickets_table.c.id == ticket_id)
        .values(**update_data.model_dump(exclude_unset=True))
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

async def update_ticket_details(
    session: AsyncSession,
    ticket_id: int,
    ticket_details_update_body: TicketDetailsUpdateBody
) -> bool:
    stmt = (
        update(ticket_details_table)
        .where(ticket_details_table.c.id == ticket_id)
        .values(**ticket_details_update_body.model_dump(exclude_unset=True))
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

async def delete_ticket(session: AsyncSession, ticket_id: int) -> bool:
    stmt = delete(tickets_table).where(tickets_table.c.id == ticket_id)

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

async def sell_ticket_to_user(session: AsyncSession, user_name: str) -> bool:
    stmt = (
        update(tickets_table)
        .where(
            and_(
                tickets_table.c.user_name == user_name,
                tickets_table.c.sold == False
            )
        ).values(
            sold=True
        )
    )

    result = await session.execute(stmt)

    await session.commit()

    if result.rowcount == 0:
        return False
    return True
