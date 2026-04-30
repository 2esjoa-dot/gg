"""Order number generation using PostgreSQL sequence for concurrency safety."""

from datetime import date

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def generate_order_number(db: AsyncSession, store_id: int) -> str:
    """Generate a unique order number in format ORD-YYYYMMDD-NNNN.

    Uses PostgreSQL sequence per store per day for concurrency-safe numbering.
    """
    today = date.today()
    date_str = today.strftime("%Y%m%d")
    seq_name = f"order_seq_s{store_id}_{date_str}"

    # Create sequence if not exists (idempotent)
    await db.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {seq_name} START 1"))
    result = await db.execute(text(f"SELECT nextval('{seq_name}')"))
    seq_val = result.scalar_one()

    return f"ORD-{date_str}-{seq_val:04d}"
