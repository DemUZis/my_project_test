from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.master import Master
from app.schemes.master import MasterCreate, MasterUpdate


class MasterRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, master_data: MasterCreate) -> Master:
        master = Master(
            user_id=master_data.user_id,
            name=master_data.name,
            specialization=master_data.specialization,
            bio=master_data.bio
        )
        self.db_session.add(master)
        await self.db_session.commit()
        await self.db_session.refresh(master)
        return master

    async def get_by_id(self, master_id: int) -> Optional[Master]:
        result = await self.db_session.execute(
            select(Master)
            .options(selectinload(Master.user))
            .options(selectinload(Master.appointments))
            .options(selectinload(Master.reviews))
            .options(selectinload(Master.shifts))
            .options(selectinload(Master.sessions))
            .where(Master.id == master_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Master]:
        result = await self.db_session.execute(
            select(Master).where(Master.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Master]:
        result = await self.db_session.execute(
            select(Master)
            .options(selectinload(Master.user))
            .offset(skip)
            .limit(limit)
            .order_by(Master.id)
        )
        return result.scalars().all()

    async def update(self, master_id: int, master_data: MasterUpdate) -> Optional[Master]:
        master = await self.get_by_id(master_id)
        if master:
            for field, value in master_data.dict(exclude_unset=True).items():
                setattr(master, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(master)
        return master

    async def delete(self, master_id: int) -> bool:
        master = await self.get_by_id(master_id)
        if master:
            await self.db_session.delete(master)
            await self.db_session.commit()
            return True
        return False