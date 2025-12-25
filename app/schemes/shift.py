from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShiftBase(BaseModel):
    master_id: int
    date: datetime
    start_time: datetime
    end_time: datetime


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class ShiftInDB(ShiftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True