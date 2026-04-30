"""Factory for TableSession test data."""

from datetime import datetime, timedelta, timezone

import factory

from app.models.session import SessionStatus, TableSession


class SessionFactory(factory.Factory):
    class Meta:
        model = TableSession

    store_id = 1
    table_id = 1
    status = SessionStatus.ACTIVE
    started_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    expires_at = factory.LazyFunction(lambda: datetime.now(timezone.utc) + timedelta(hours=16))
    completed_at = None
