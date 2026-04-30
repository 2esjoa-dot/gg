"""Health check endpoint."""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """Check application and database health."""
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"
        logger.exception("Database health check failed")

    status = "healthy" if db_status == "connected" else "unhealthy"
    status_code = 200 if status == "healthy" else 503

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=status_code,
        content={"status": status, "version": "1.0.0", "database": db_status},
    )
