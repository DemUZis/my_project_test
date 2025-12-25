from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MasterBase(BaseModel):
    user_id: int
    name: str
    specialization: str
    bio: Optional[str] = None


class MasterCreate(MasterBase):
    pass


class MasterUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None


class MasterInDB(MasterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True