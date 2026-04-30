from datetime import datetime
from decimal import Decimal
import enum

from sqlalchemy import String, Integer, DateTime, ForeignKey, Numeric, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix_session_orders", "session_id", "created_at"),
        Index("ix_table_active_orders", "store_id", "table_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("table_sessions.id"), nullable=False)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 0), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
