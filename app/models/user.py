from sqlalchemy import String, Boolean, Integer, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.review import Review
    from app.models.master import Master


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))  # 'client', 'master', 'admin'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="client")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="client")
    master_profile: Mapped["Master"] = relationship("Master", back_populates="user", uselist=False, cascade="all, delete-orphan")