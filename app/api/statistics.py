from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.database.database import async_session_maker
from app.repositories.appointment import AppointmentRepository
from app.repositories.service import ServiceRepository
from app.repositories.master import MasterRepository
from app.repositories.user import UserRepository
from app.schemes.user import UserInDB
from app.dependencies import get_current_user


router = APIRouter(prefix="/statistics", tags=["statistics"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/dashboard")
async def get_dashboard_stats(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access statistics"
        )
    
    db = next(get_db())
    
    # Total appointments
    appointment_repository = AppointmentRepository(db)
    all_appointments = await appointment_repository.get_all(skip=0, limit=10000)
    total_appointments = len(all_appointments)
    
    # Completed appointments
    completed_appointments = len([appt for appt in all_appointments if appt.status == "completed"])
    
    # Total revenue (assuming we have price data in appointments or services)
    # For now, using a placeholder calculation
    total_revenue = completed_appointments * 1500  # Placeholder value
    
    # Total customers
    user_repository = UserRepository(db)
    all_users = await user_repository.get_all(skip=0, limit=1000)
    total_customers = len([user for user in all_users if user.role == "client"])
    
    # Total masters
    master_repository = MasterRepository(db)
    all_masters = await master_repository.get_all(skip=0, limit=1000)
    total_masters = len(all_masters)
    
    # Top services (placeholder implementation)
    service_repository = ServiceRepository(db)
    all_services = await service_repository.get_all(skip=0, limit=1000)
    top_services = [{"name": service.name, "count": 10} for service in all_services[:5]]  # Placeholder
    
    return {
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "total_masters": total_masters,
        "top_services": top_services
    }


@router.get("/revenue")
async def get_revenue_stats(
    period: str = "month",  # Options: day, week, month, year
    current_user: UserInDB = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access revenue statistics"
        )
    
    db = next(get_db())
    appointment_repository = AppointmentRepository(db)
    all_appointments = await appointment_repository.get_all(skip=0, limit=10000)
    
    # Filter for completed appointments only
    completed_appointments = [appt for appt in all_appointments if appt.status == "completed"]
    
    # Calculate revenue based on period
    now = datetime.utcnow()
    if period == "day":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "year":
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid period. Use day, week, month, or year."
        )
    
    period_appointments = [
        appt for appt in completed_appointments 
        if appt.created_at >= start_date
    ]
    
    # Placeholder revenue calculation
    period_revenue = len(period_appointments) * 1500  # Placeholder value
    
    return {
        f"{period}_revenue": period_revenue,
        "period": period,
        "start_date": start_date.isoformat(),
        "appointment_count": len(period_appointments)
    }


@router.get("/appointments")
async def get_appointment_stats(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access appointment statistics"
        )
    
    db = next(get_db())
    appointment_repository = AppointmentRepository(db)
    all_appointments = await appointment_repository.get_all(skip=0, limit=10000)
    
    total_appointments = len(all_appointments)
    completed_appointments = len([appt for appt in all_appointments if appt.status == "completed"])
    cancelled_appointments = len([appt for appt in all_appointments if appt.status == "cancelled"])
    upcoming_appointments = total_appointments - completed_appointments - cancelled_appointments
    
    # Appointments by service
    service_count = {}
    for appt in all_appointments:
        service_name = f"Service {appt.service_id}"  # In a real app, we'd fetch the actual service name
        if service_name in service_count:
            service_count[service_name] += 1
        else:
            service_count[service_name] = 1
    
    # Appointments by master
    master_count = {}
    for appt in all_appointments:
        master_name = f"Master {appt.master_id}"  # In a real app, we'd fetch the actual master name
        if master_name in master_count:
            master_count[master_name] += 1
        else:
            master_count[master_name] = 1
    
    return {
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "upcoming_appointments": upcoming_appointments,
        "appointments_by_service": service_count,
        "appointments_by_master": master_count
    }