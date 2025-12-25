from sqlalchemy import String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.master import Master
    from app.models.appointment import Appointment


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"))
    rating: Mapped[int] = mapped_column(Integer)  # 1-5
    comment: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    client: Mapped["User"] = relationship("User", back_populates="reviews")
    master: Mapped["Master"] = relationship("Master", back_populates="reviews")
    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="review", uselist=False)