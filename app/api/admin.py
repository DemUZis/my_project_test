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
from app.schemes.user import UserInDB, UserCreate, UserUpdate
from app.schemes.service import ServiceCreate, ServiceUpdate, ServiceInDB
from app.schemes.master import MasterCreate, MasterUpdate, MasterInDB
from app.schemes.appointment import AppointmentInDB
from app.schemes.review import ReviewInDB
from app.dependencies import get_current_user


router = APIRouter(prefix="/admin", tags=["admin"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/dashboard")
async def get_admin_dashboard(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin dashboard"
        )
    
    return {"message": "Welcome to admin dashboard"}


@router.post("/services", response_model=ServiceInDB)
async def create_service(
    service: ServiceCreate,
    current_user: UserInDB = Depends(get_current_user),
    service_repository: ServiceRepository = Depends(lambda: ServiceRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create services"
        )
    
    db_service = await service_repository.create(service)
    return db_service


@router.put("/services/{service_id}", response_model=ServiceInDB)
async def update_service(
    service_id: int,
    service_update: ServiceUpdate,
    current_user: UserInDB = Depends(get_current_user),
    service_repository: ServiceRepository = Depends(lambda: ServiceRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update services"
        )
    
    db_service = await service_repository.update(service_id, service_update)
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return db_service


@router.delete("/services/{service_id}")
async def delete_service(
    service_id: int,
    current_user: UserInDB = Depends(get_current_user),
    service_repository: ServiceRepository = Depends(lambda: ServiceRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete services"
        )
    
    success = await service_repository.delete(service_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {"message": "Service deleted successfully"}


@router.get("/services", response_model=List[ServiceInDB])
async def get_services(
    skip: int = 0, 
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
    service_repository: ServiceRepository = Depends(lambda: ServiceRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view services"
        )
    
    services = await service_repository.get_all(skip=skip, limit=limit)
    return services


@router.post("/masters", response_model=MasterInDB)
async def create_master(
    master: MasterCreate,
    current_user: UserInDB = Depends(get_current_user),
    master_repository: MasterRepository = Depends(lambda: MasterRepository(next(get_db()))),
    user_repository: UserRepository = Depends(lambda: UserRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create masters"
        )
    
    # Verify that the user exists
    user = await user_repository.get_by_id(master.user_id)
    if not user or user.role != "master":
        raise HTTPException(
            status_code=status.HTTP_40_BAD_REQUEST,
            detail="User does not exist or is not a master"
        )
    
    db_master = await master_repository.create(master)
    return db_master


@router.put("/masters/{master_id}", response_model=MasterInDB)
async def update_master(
    master_id: int,
    master_update: MasterUpdate,
    current_user: UserInDB = Depends(get_current_user),
    master_repository: MasterRepository = Depends(lambda: MasterRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update masters"
        )
    
    db_master = await master_repository.update(master_id, master_update)
    if not db_master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    return db_master


@router.delete("/masters/{master_id}")
async def delete_master(
    master_id: int,
    current_user: UserInDB = Depends(get_current_user),
    master_repository: MasterRepository = Depends(lambda: MasterRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete masters"
        )
    
    success = await master_repository.delete(master_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    return {"message": "Master deleted successfully"}


@router.get("/masters", response_model=List[MasterInDB])
async def get_masters(
    skip: int = 0, 
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
    master_repository: MasterRepository = Depends(lambda: MasterRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view masters"
        )
    
    masters = await master_repository.get_all(skip=skip, limit=limit)
    return masters


@router.get("/appointments", response_model=List[AppointmentInDB])
async def get_appointments(
    skip: int = 0, 
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user),
    appointment_repository: AppointmentRepository = Depends(lambda: AppointmentRepository(next(get_db())))
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view appointments"
        )
    
    appointments = await appointment_repository.get_all(skip=skip, limit=limit)
    return appointments


@router.get("/statistics")
async def get_statistics(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view statistics"
        )
    
    # This would include more complex statistics in a real implementation
    return {
        "total_appointments": 0,
        "total_revenue": 0.0,
        "total_customers": 0,
        "total_masters": 0,
        "top_services": []
    }


@router.get("/revenue")
async def get_revenue(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view revenue"
        )
    
    # This would include more complex revenue calculations in a real implementation
    return {
        "today_revenue": 0.0,
        "monthly_revenue": 0.0,
        "yearly_revenue": 0.0
    }