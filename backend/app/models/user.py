from datetime import datetime
import enum

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    STORE_ADMIN = "store_admin"
    HQ_ADMIN = "hq_admin"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("store_id", "username", name="uq_store_username"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="users")
