from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import TableSession
from app.repositories.session_repository import SessionRepository
from app.utils.exceptions import NoActiveSessionError


class SessionService:
    def __init__(self, db: AsyncSession):
        self.session_repo = SessionRepository(db)

    async def get_or_create_session(self, store_id: int, table_id: int) -> TableSession:
        session = await self.session_repo.get_active(store_id, table_id)
        if session:
            if session.expires_at < datetime.utcnow():
                await self.session_repo.close_session(session)
                return await self.session_repo.create(store_id, table_id)
            return session
        return await self.session_repo.create(store_id, table_id)

    async def get_active_session(self, store_id: int, table_id: int) -> TableSession | None:
        session = await self.session_repo.get_active(store_id, table_id)
        if session and session.expires_at < datetime.utcnow():
            await self.session_repo.close_session(session)
            return None
        return session

    async def end_session(self, store_id: int, table_id: int) -> TableSession:
        session = await self.session_repo.get_active(store_id, table_id)
        if not session:
            raise NoActiveSessionError()
        return await self.session_repo.close_session(session)
