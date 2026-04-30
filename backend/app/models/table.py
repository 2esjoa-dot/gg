from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Table(Base):
    __tablename__ = "tables"
    __table_args__ = (UniqueConstraint("store_id", "table_number", name="uq_store_table_number"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    table_number: Mapped[int] = mapped_column(Integer, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="tables")
    sessions = relationship("TableSession", back_populates="table")
