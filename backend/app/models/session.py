from datetime import datetime
import enum

from sqlalchemy import DateTime, Integer, ForeignKey, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class TableSession(Base):
    __tablename__ = "table_sessions"
    __table_args__ = (
        Index("ix_active_session", "store_id", "table_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    status: Mapped[SessionStatus] = mapped_column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    table = relationship("Table", back_populates="sessions")
