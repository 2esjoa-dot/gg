"""SQLAlchemy model base and imports."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Import all models so Alembic can detect them
from app.models.store import Store  # noqa: E402, F401
from app.models.user import User  # noqa: E402, F401
from app.models.table import Table  # noqa: E402, F401
from app.models.session import TableSession  # noqa: E402, F401
from app.models.category import Category  # noqa: E402, F401
from app.models.menu_item import MenuItem  # noqa: E402, F401
from app.models.order import Order  # noqa: E402, F401
from app.models.order_item import OrderItem  # noqa: E402, F401
