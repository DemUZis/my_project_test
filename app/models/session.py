from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.master import Master
    from app.models.service import Service
    from app.models.appointment import Appointment


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    master: Mapped["Master"] = relationship("Master", back_populates="sessions")
    service: Mapped["Service"] = relationship("Service", back_populates="sessions")
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="session", uselist=False, cascade="all, delete-orphan")