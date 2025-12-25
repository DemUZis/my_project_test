from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.repositories.master import MasterRepository
from app.repositories.session import SessionRepository
from app.repositories.appointment import AppointmentRepository
from app.repositories.review import ReviewRepository
from app.schemes.user import UserInDB
from app.schemes.master import MasterInDB
from app.schemes.session import SessionUpdate, SessionInDB
from app.schemes.appointment import AppointmentInDB, AppointmentUpdate
from app.schemes.review import ReviewInDB


class MasterService:
    def __init__(
        self,
        user_repository: UserRepository,
        master_repository: MasterRepository,
        session_repository: SessionRepository,
        appointment_repository: AppointmentRepository,
        review_repository: ReviewRepository
    ):
        self.user_repository = user_repository
        self.master_repository = master_repository
        self.session_repository = session_repository
        self.appointment_repository = appointment_repository
        self.review_repository = review_repository

    async def get_master_profile(self, current_user: UserInDB) -> MasterInDB:
        master = await self.master_repository.get_by_user_id(current_user.id)
        if not master:
            raise ValueError("Master profile not found")
        return master

    async def get_master_schedule(self, date: str, current_user: UserInDB) -> List[SessionInDB]:
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        master = await self.master_repository.get_by_user_id(current_user.id)
        if not master:
            raise ValueError("Master profile not found")
        
        return await self.session_repository.get_by_master_and_date(master.id, date_obj)

    async def get_master_appointments(self, current_user: UserInDB) -> List[AppointmentInDB]:
        master = await self.master_repository.get_by_user_id(current_user.id)
        if not master:
            raise ValueError("Master profile not found")
        
        return await self.appointment_repository.get_by_master_id(master.id)

    async def update_session_availability(self, session_id: int, session_update: SessionUpdate, current_user: UserInDB) -> SessionInDB:
        session = await self.session_repository.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
        
        # Verify that the session belongs to the current master
        master = await self.master_repository.get_by_user_id(current_user.id)
        if not master or session.master_id != master.id:
            raise ValueError("Not authorized to update this session")
        
        # Update session availability
        return await self.session_repository.update(session_id, session_update)