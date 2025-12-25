from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.session import Session
from app.schemes.session import SessionCreate, SessionUpdate
from datetime import datetime


class SessionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, session_data: SessionCreate) -> Session:
        session = Session(
            master_id=session_data.master_id,
            service_id=session_data.service_id,
            date=session_data.date,
            start_time=session_data.start_time,
            end_time=session_data.end_time,
            is_available=session_data.is_available
        )
        self.db_session.add(session)
        await self.db_session.commit()
        await self.db_session.refresh(session)
        return session

    async def get_by_id(self, session_id: int) -> Optional[Session]:
        result = await self.db_session.execute(
            select(Session)
            .options(selectinload(Session.master))
            .options(selectinload(Session.service))
            .options(selectinload(Session.appointment))
            .where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_available_by_master_and_date(self, master_id: int, date: datetime) -> List[Session]:
        result = await self.db_session.execute(
            select(Session)
            .options(selectinload(Session.master))
            .options(selectinload(Session.service))
            .where(Session.master_id == master_id)
            .where(Session.date == date)
            .where(Session.is_available == True)
        )
        return result.scalars().all()

    async def get_by_master_and_date(self, master_id: int, date: datetime) -> List[Session]:
        result = await self.db_session.execute(
            select(Session)
            .options(selectinload(Session.master))
            .options(selectinload(Session.service))
            .options(selectinload(Session.appointment))
            .where(Session.master_id == master_id)
            .where(Session.date == date)
        )
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Session]:
        result = await self.db_session.execute(
            select(Session)
            .options(selectinload(Session.master))
            .options(selectinload(Session.service))
            .offset(skip)
            .limit(limit)
            .order_by(Session.id)
        )
        return result.scalars().all()

    async def update(self, session_id: int, session_data: SessionUpdate) -> Optional[Session]:
        session = await self.get_by_id(session_id)
        if session:
            for field, value in session_data.dict(exclude_unset=True).items():
                setattr(session, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(session)
        return session

    async def delete(self, session_id: int) -> bool:
        session = await self.get_by_id(session_id)
        if session:
            await self.db_session.delete(session)
            await self.db_session.commit()
            return True
        return False