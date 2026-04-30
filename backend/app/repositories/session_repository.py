"""TableSession repository for database operations."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import SessionStatus, TableSession
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[TableSession]):
    """Repository for TableSession entity operations."""

    def __init__(self):
        super().__init__(TableSession)

    async def get_active_session(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> TableSession | None:
        """Find the active session for a specific table."""
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(TableSession).where(
                TableSession.store_id == store_id,
                TableSession.table_id == table_id,
                TableSession.status == SessionStatus.ACTIVE,
                TableSession.expires_at > now,
            )
        )
        return result.scalar_one_or_none()

    async def get_expired_active_session(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> TableSession | None:
        """Find an expired but still marked active session."""
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(TableSession).where(
                TableSession.store_id == store_id,
                TableSession.table_id == table_id,
                TableSession.status == SessionStatus.ACTIVE,
                TableSession.expires_at <= now,
            )
        )
        return result.scalar_one_or_none()

    async def get_completed_sessions(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> list[TableSession]:
        """Get completed sessions for a table, ordered by completion time desc."""
        result = await db.execute(
            select(TableSession)
            .where(
                TableSession.store_id == store_id,
                TableSession.table_id == table_id,
                TableSession.status == SessionStatus.COMPLETED,
            )
            .order_by(TableSession.completed_at.desc())
        )
        return list(result.scalars().all())
