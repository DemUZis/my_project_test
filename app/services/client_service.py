from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.repositories.service import ServiceRepository
from app.repositories.master import MasterRepository
from app.repositories.session import SessionRepository
from app.repositories.appointment import AppointmentRepository
from app.repositories.review import ReviewRepository
from app.schemes.user import UserInDB
from app.schemes.service import ServiceInDB
from app.schemes.master import MasterInDB
from app.schemes.session import SessionInDB, SessionUpdate
from app.schemes.appointment import AppointmentCreate, AppointmentInDB
from app.schemes.review import ReviewCreate, ReviewInDB


class ClientService:
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

    async def get_services(self, skip: int = 0, limit: int = 100) -> List[ServiceInDB]:
        return await self.service_repository.get_all(skip=skip, limit=limit)

    async def get_masters(self, skip: int = 0, limit: int = 100) -> List[MasterInDB]:
        return await self.master_repository.get_all(skip=skip, limit=limit)

    async def get_available_sessions(self, master_id: int, date: str) -> List[SessionInDB]:
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        return await self.session_repository.get_available_by_master_and_date(master_id, date_obj)

    async def book_appointment(self, appointment_data: AppointmentCreate, current_user: UserInDB) -> AppointmentInDB:
        # Ensure the client can only book for themselves
        if appointment_data.client_id != current_user.id:
            raise ValueError("Cannot book appointment for another user")
        
        # Check if session exists and is available
        session = await self.session_repository.get_by_id(appointment_data.session_id)
        if not session or not session.is_available:
            raise ValueError("Session is not available")
        
        # Create the appointment
        appointment = await self.appointment_repository.create(appointment_data)
        
        # Update session availability
        session_update = SessionUpdate(is_available=False)
        await self.session_repository.update(session.id, session_update)
        
        return appointment

    async def get_my_appointments(self, current_user: UserInDB) -> List[AppointmentInDB]:
        return await self.appointment_repository.get_by_client_id(current_user.id)

    async def create_review(self, review_data: ReviewCreate, current_user: UserInDB) -> ReviewInDB:
        # Ensure the client can only create reviews for themselves
        if review_data.client_id != current_user.id:
            raise ValueError("Cannot create review for another user")
        
        return await self.review_repository.create(review_data)