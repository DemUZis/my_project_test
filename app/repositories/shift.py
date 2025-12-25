from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.shift import Shift
from app.schemes.shift import ShiftCreate, ShiftUpdate
from datetime import datetime


class ShiftRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, shift_data: ShiftCreate) -> Shift:
        shift = Shift(
            master_id=shift_data.master_id,
            date=shift_data.date,
            start_time=shift_data.start_time,
            end_time=shift_data.end_time
        )
        self.db_session.add(shift)
        await self.db_session.commit()
        await self.db_session.refresh(shift)
        return shift

    async def get_by_id(self, shift_id: int) -> Optional[Shift]:
        result = await self.db_session.execute(
            select(Shift)
            .options(selectinload(Shift.master))
            .where(Shift.id == shift_id)
        )
        return result.scalar_one_or_none()

    async def get_by_master_id(self, master_id: int) -> List[Shift]:
        result = await self.db_session.execute(
            select(Shift)
            .options(selectinload(Shift.master))
            .where(Shift.master_id == master_id)
        )
        return result.scalars().all()

    async def get_by_master_and_date(self, master_id: int, date: datetime) -> List[Shift]:
        result = await self.db_session.execute(
            select(Shift)
            .options(selectinload(Shift.master))
            .where(Shift.master_id == master_id)
            .where(Shift.date == date)
        )
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Shift]:
        result = await self.db_session.execute(
            select(Shift)
            .options(selectinload(Shift.master))
            .offset(skip)
            .limit(limit)
            .order_by(Shift.id)
        )
        return result.scalars().all()

    async def update(self, shift_id: int, shift_data: ShiftUpdate) -> Optional[Shift]:
        shift = await self.get_by_id(shift_id)
        if shift:
            for field, value in shift_data.dict(exclude_unset=True).items():
                setattr(shift, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(shift)
        return shift

    async def delete(self, shift_id: int) -> bool:
        shift = await self.get_by_id(shift_id)
        if shift:
            await self.db_session.delete(shift)
            await self.db_session.commit()
            return True
        return False