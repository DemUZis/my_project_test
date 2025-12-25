from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment import Appointment
    from app.models.review import Review
    from app.models.shift import Shift
    from app.models.session import Session


class Master(Base):
    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    specialization: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="master_profile")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="master")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="master")
    shifts: Mapped[list["Shift"]] = relationship("Shift", back_populates="master")
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="master")