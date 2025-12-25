from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionBase(BaseModel):
    master_id: int
    service_id: int
    date: datetime
    start_time: datetime
    end_time: datetime
    is_available: bool = True


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    is_available: Optional[bool] = None


class SessionInDB(SessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True