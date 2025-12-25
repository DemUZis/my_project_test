from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import async_session_maker
from app.repositories.user import UserRepository
from app.repositories.master import MasterRepository
from app.repositories.session import SessionRepository
from app.repositories.appointment import AppointmentRepository
from app.repositories.review import ReviewRepository
from app.schemes.user import UserInDB
from app.schemes.master import MasterInDB
from app.schemes.session import SessionUpdate, SessionInDB
from app.schemes.appointment import AppointmentInDB, AppointmentUpdate
from app.dependencies import get_current_user


router = APIRouter(prefix="/masters", tags=["masters"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/profile", response_model=MasterInDB)
async def get_master_profile(
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    master_repository = MasterRepository(db)
    master = await master_repository.get_by_user_id(current_user.id)
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master profile not found"
        )
    
    return master


@router.get("/schedule", response_model=List[SessionInDB])
async def get_master_schedule(
    date: str,  # Format: YYYY-MM-DD
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_40_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    master_repository = MasterRepository(db)
    master = await master_repository.get_by_user_id(current_user.id)
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master profile not found"
        )
    
    session_repository = SessionRepository(db)
    sessions = await session_repository.get_by_master_and_date(master.id, date_obj)
    return sessions


@router.get("/appointments", response_model=List[AppointmentInDB])
async def get_master_appointments(
    current_user: UserInDB = Depends(get_current_user),
    appointment_repository: AppointmentRepository = Depends(lambda: AppointmentRepository(next(get_db())))
):
    master_repository = MasterRepository(next(get_db()))
    master = await master_repository.get_by_user_id(current_user.id)
    
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master profile not found"
        )
    
    appointments = await appointment_repository.get_by_master_id(master.id)
    return appointments


@router.put("/sessions/{session_id}/availability")
async def update_session_availability(
    session_id: int,
    session_update: SessionUpdate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session_repository = SessionRepository(db)
    session = await session_repository.get_by_id(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify that the session belongs to the current master
    master_repository = MasterRepository(db)
    master = await master_repository.get_by_user_id(current_user.id)
    
    if not master or session.master_id != master.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this session"
        )
    
    # Update session availability
    updated_session = await session_repository.update(session_id, session_update)
    return updated_session