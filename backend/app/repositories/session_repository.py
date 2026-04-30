from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import TableSession, SessionStatus


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, store_id: int, table_id: int) -> TableSession:
        session = TableSession(
            store_id=store_id,
            table_id=table_id,
            status=SessionStatus.ACTIVE,
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=16),
        )
        self.db.add(session)
        await self.db.flush()
        return session

    async def get_active(self, store_id: int, table_id: int) -> TableSession | None:
        result = await self.db.execute(
            select(TableSession).where(
                and_(
                    TableSession.store_id == store_id,
                    TableSession.table_id == table_id,
                    TableSession.status == SessionStatus.ACTIVE,
                )
            )
        )
        return result.scalar_one_or_none()

    async def close_session(self, session: TableSession) -> TableSession:
        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.utcnow()
        await self.db.flush()
        return session
