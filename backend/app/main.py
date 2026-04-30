"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.middleware.auth import AuthMiddleware
from app.middleware.exception_handler import ExceptionHandlerMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.routers import admin_auth, admin_tables, customer_auth, customer_session, health, hq
from app.utils.logging_config import setup_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware registration (last registered = first executed)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # Router registration
    prefix = settings.API_PREFIX
    app.include_router(health.router)
    app.include_router(hq.router, prefix=f"{prefix}/hq", tags=["HQ - Store"])
    app.include_router(admin_auth.router, prefix=f"{prefix}/admin/auth", tags=["Admin - Auth"])
    app.include_router(admin_tables.router, prefix=f"{prefix}/admin/tables", tags=["Admin - Table"])
    app.include_router(customer_auth.router, prefix=f"{prefix}/customer/auth", tags=["Customer - Auth"])
    app.include_router(customer_session.router, prefix=f"{prefix}/customer/session", tags=["Customer - Session"])

    # Static files for uploads
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

    return app


app = create_app()
