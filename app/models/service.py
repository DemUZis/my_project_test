from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.session import Session
    from app.models.appointment import Appointment


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    duration: Mapped[int] = mapped_column(Integer)  # in minutes
    price: Mapped[float] = mapped_column(Float)

    # Relationships
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="service")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="service")