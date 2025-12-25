from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.database import async_session_maker
from app.repositories.user import UserRepository
from app.repositories.service import ServiceRepository
from app.repositories.master import MasterRepository
from app.repositories.session import SessionRepository
from app.repositories.appointment import AppointmentRepository
from app.repositories.review import ReviewRepository
from app.schemes.user import UserInDB
from app.schemes.service import ServiceInDB
from app.schemes.master import MasterInDB
from app.schemes.session import SessionInDB
from app.schemes.appointment import AppointmentCreate, AppointmentInDB
from app.schemes.review import ReviewCreate, ReviewInDB
from app.dependencies import get_current_user


router = APIRouter(prefix="/clients", tags=["clients"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/services", response_model=List[ServiceInDB])
async def get_services(
    skip: int = 0, 
    limit: int = 100, 
    service_repository: ServiceRepository = Depends(lambda: ServiceRepository(next(get_db())))
):
    services = await service_repository.get_all(skip=skip, limit=limit)
    return services


@router.get("/masters", response_model=List[MasterInDB])
async def get_masters(
    skip: int = 0, 
    limit: int = 100, 
    master_repository: MasterRepository = Depends(lambda: MasterRepository(next(get_db())))
):
    masters = await master_repository.get_all(skip=skip, limit=limit)
    return masters


@router.get("/sessions/available", response_model=List[SessionInDB])
async def get_available_sessions(
    master_id: int,
    date: str,  # Format: YYYY-MM-DD
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
    
    session_repository = SessionRepository(db)
    available_sessions = await session_repository.get_available_by_master_and_date(master_id, date_obj)
    return available_sessions


@router.post("/appointments/book", response_model=AppointmentInDB)
async def book_appointment(
    appointment: AppointmentCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Ensure the client can only book for themselves
    if appointment.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot book appointment for another user"
        )
    
    appointment_repository = AppointmentRepository(db)
    session_repository = SessionRepository(db)
    
    # Check if session exists and is available
    session = await session_repository.get_by_id(appointment.session_id)
    if not session or not session.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is not available"
        )
    
    # Create the appointment
    db_appointment = await appointment_repository.create(appointment)
    
    # Update session availability
    session.is_available = False
    await db.commit()
    await db.refresh(session)
    
    return db_appointment


@router.get("/appointments/my", response_model=List[AppointmentInDB])
async def get_my_appointments(
    current_user: UserInDB = Depends(get_current_user),
    appointment_repository: AppointmentRepository = Depends(lambda: AppointmentRepository(next(get_db())))
):
    appointments = await appointment_repository.get_by_client_id(current_user.id)
    return appointments


@router.post("/reviews", response_model=ReviewInDB)
async def create_review(
    review: ReviewCreate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Ensure the client can only create reviews for themselves
    if review.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create review for another user"
        )
    
    review_repository = ReviewRepository(db)
    db_review = await review_repository.create(review)
    return db_review