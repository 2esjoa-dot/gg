"""Table session management service."""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.session import SessionStatus
from app.repositories.session_repository import SessionRepository
from app.repositories.table_repository import TableRepository
from app.schemas.session import SessionCompleteResponse, SessionResponse
from app.utils.exceptions import NoActiveSessionError, NotFoundError

logger = logging.getLogger(__name__)


class SessionService:
    """Handles table session lifecycle: create, complete, expire."""

    def __init__(self):
        self.session_repo = SessionRepository()
        self.table_repo = TableRepository()

    async def get_or_create_session(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> SessionResponse:
        """Get the active session for a table, or create a new one.

        Also handles expired session cleanup.
        """
        # Check for valid active session
        session = await self.session_repo.get_active_session(db, store_id, table_id)
        if session:
            return SessionResponse.model_validate(session)

        # Check for expired active session and close it
        expired = await self.session_repo.get_expired_active_session(db, store_id, table_id)
        if expired:
            expired.status = SessionStatus.COMPLETED
            expired.completed_at = expired.expires_at
            await db.flush()
            logger.info("Expired session closed: session_id=%d", expired.id)

        # Create new session
        expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.SESSION_EXPIRE_HOURS)
        new_session = await self.session_repo.create(
            db,
            store_id=store_id,
            table_id=table_id,
            status=SessionStatus.ACTIVE,
            expires_at=expires_at,
        )
        await db.commit()
        return SessionResponse.model_validate(new_session)

    async def complete_session(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> SessionCompleteResponse:
        """Complete (end) the active session for a table."""
        # Verify table exists
        table = await self.table_repo.get_by_id(db, table_id)
        if not table or table.store_id != store_id:
            raise NotFoundError("테이블")

        session = await self.session_repo.get_active_session(db, store_id, table_id)
        if not session:
            raise NoActiveSessionError()

        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.now(timezone.utc)
        await db.commit()

        logger.info("Session completed: session_id=%d table_id=%d", session.id, table_id)
        return SessionCompleteResponse(session_id=session.id)

    async def get_active_session_for_table(
        self, db: AsyncSession, store_id: int, table_id: int
    ) -> SessionResponse | None:
        """Get the current active session for a table, if any."""
        session = await self.session_repo.get_active_session(db, store_id, table_id)
        if not session:
            return None
        return SessionResponse.model_validate(session)
