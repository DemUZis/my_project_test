from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.service import Service
from app.schemes.service import ServiceCreate, ServiceUpdate


class ServiceRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, service_data: ServiceCreate) -> Service:
        service = Service(
            name=service_data.name,
            description=service_data.description,
            duration=service_data.duration,
            price=service_data.price
        )
        self.db_session.add(service)
        await self.db_session.commit()
        await self.db_session.refresh(service)
        return service

    async def get_by_id(self, service_id: int) -> Optional[Service]:
        result = await self.db_session.execute(
            select(Service).where(Service.id == service_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Service]:
        result = await self.db_session.execute(
            select(Service)
            .offset(skip)
            .limit(limit)
            .order_by(Service.id)
        )
        return result.scalars().all()

    async def update(self, service_id: int, service_data: ServiceUpdate) -> Optional[Service]:
        service = await self.get_by_id(service_id)
        if service:
            for field, value in service_data.dict(exclude_unset=True).items():
                setattr(service, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(service)
        return service

    async def delete(self, service_id: int) -> bool:
        service = await self.get_by_id(service_id)
        if service:
            await self.db_session.delete(service)
            await self.db_session.commit()
            return True
        return False