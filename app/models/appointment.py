from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.master import Master
    from app.models.service import Service
    from app.models.session import Session


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    status: Mapped[str] = mapped_column(String(20), default="booked")  # 'booked', 'completed', 'cancelled'

    # Relationships
    client: Mapped["User"] = relationship("User", back_populates="appointments")
    master: Mapped["Master"] = relationship("Master", back_populates="appointments")
    service: Mapped["Service"] = relationship("Service", back_populates="appointments")
    session: Mapped["Session"] = relationship("Session", back_populates="appointment")