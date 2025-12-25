from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.appointment import Appointment
from app.schemes.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, appointment_data: AppointmentCreate) -> Appointment:
        appointment = Appointment(
            client_id=appointment_data.client_id,
            session_id=appointment_data.session_id,
            service_id=appointment_data.service_id,
            master_id=appointment_data.master_id,
            status=appointment_data.status
        )
        self.db_session.add(appointment)
        await self.db_session.commit()
        await self.db_session.refresh(appointment)
        return appointment

    async def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        result = await self.db_session.execute(
            select(Appointment)
            .options(selectinload(Appointment.client))
            .options(selectinload(Appointment.master))
            .options(selectinload(Appointment.service))
            .options(selectinload(Appointment.session))
            .where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_client_id(self, client_id: int) -> List[Appointment]:
        result = await self.db_session.execute(
            select(Appointment)
            .options(selectinload(Appointment.master))
            .options(selectinload(Appointment.service))
            .options(selectinload(Appointment.session))
            .where(Appointment.client_id == client_id)
        )
        return result.scalars().all()

    async def get_by_master_id(self, master_id: int) -> List[Appointment]:
        result = await self.db_session.execute(
            select(Appointment)
            .options(selectinload(Appointment.client))
            .options(selectinload(Appointment.service))
            .options(selectinload(Appointment.session))
            .where(Appointment.master_id == master_id)
        )
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        result = await self.db_session.execute(
            select(Appointment)
            .options(selectinload(Appointment.client))
            .options(selectinload(Appointment.master))
            .options(selectinload(Appointment.service))
            .options(selectinload(Appointment.session))
            .offset(skip)
            .limit(limit)
            .order_by(Appointment.id)
        )
        return result.scalars().all()

    async def update(self, appointment_id: int, appointment_data: AppointmentUpdate) -> Optional[Appointment]:
        appointment = await self.get_by_id(appointment_id)
        if appointment:
            for field, value in appointment_data.dict(exclude_unset=True).items():
                setattr(appointment, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(appointment)
        return appointment

    async def delete(self, appointment_id: int) -> bool:
        appointment = await self.get_by_id(appointment_id)
        if appointment:
            await self.db_session.delete(appointment)
            await self.db_session.commit()
            return True
        return False