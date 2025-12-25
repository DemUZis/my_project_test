from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.repositories.service import ServiceRepository
from app.repositories.master import MasterRepository
from app.repositories.session import SessionRepository
from app.repositories.appointment import AppointmentRepository
from app.repositories.review import ReviewRepository
from app.schemes.user import UserInDB, UserCreate, UserUpdate
from app.schemes.service import ServiceCreate, ServiceUpdate, ServiceInDB
from app.schemes.master import MasterCreate, MasterUpdate, MasterInDB
from app.schemes.appointment import AppointmentInDB
from app.schemes.review import ReviewInDB


class AdminService:
    def __init__(
        self,
        user_repository: UserRepository,
        service_repository: ServiceRepository,
        master_repository: MasterRepository,
        session_repository: SessionRepository,
        appointment_repository: AppointmentRepository,
        review_repository: ReviewRepository
    ):
        self.user_repository = user_repository
        self.service_repository = service_repository
        self.master_repository = master_repository
        self.session_repository = session_repository
        self.appointment_repository = appointment_repository
        self.review_repository = review_repository

    async def create_service(self, service_data: ServiceCreate) -> ServiceInDB:
        return await self.service_repository.create(service_data)

    async def update_service(self, service_id: int, service_update: ServiceUpdate) -> ServiceInDB:
        service = await self.service_repository.get_by_id(service_id)
        if not service:
            raise ValueError("Service not found")
        return await self.service_repository.update(service_id, service_update)

    async def delete_service(self, service_id: int) -> bool:
        return await self.service_repository.delete(service_id)

    async def get_services(self, skip: int = 0, limit: int = 100) -> List[ServiceInDB]:
        return await self.service_repository.get_all(skip=skip, limit=limit)

    async def create_master(self, master_data: MasterCreate) -> MasterInDB:
        # Verify that the user exists
        user = await self.user_repository.get_by_id(master_data.user_id)
        if not user or user.role != "master":
            raise ValueError("User does not exist or is not a master")
        return await self.master_repository.create(master_data)

    async def update_master(self, master_id: int, master_update: MasterUpdate) -> MasterInDB:
        master = await self.master_repository.get_by_id(master_id)
        if not master:
            raise ValueError("Master not found")
        return await self.master_repository.update(master_id, master_update)

    async def delete_master(self, master_id: int) -> bool:
        return await self.master_repository.delete(master_id)

    async def get_masters(self, skip: int = 0, limit: int = 100) -> List[MasterInDB]:
        return await self.master_repository.get_all(skip=skip, limit=limit)

    async def get_appointments(self, skip: int = 0, limit: int = 100) -> List[AppointmentInDB]:
        return await self.appointment_repository.get_all(skip=skip, limit=limit)

    async def get_statistics(self):
        # This would include more complex statistics in a real implementation
        return {
            "total_appointments": 0,
            "total_revenue": 0.0,
            "total_customers": 0,
            "total_masters": 0,
            "top_services": []
        }

    async def get_revenue(self):
        # This would include more complex revenue calculations in a real implementation
        return {
            "today_revenue": 0.0,
            "monthly_revenue": 0.0,
            "yearly_revenue": 0.0
        }