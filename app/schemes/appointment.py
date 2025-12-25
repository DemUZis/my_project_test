from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppointmentBase(BaseModel):
    client_id: int
    session_id: int
    service_id: int
    master_id: int
    status: str = "booked"  # 'booked', 'completed', 'cancelled'


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    status: Optional[str] = None


class AppointmentInDB(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True