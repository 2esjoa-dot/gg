"""Global exception handler middleware."""

import logging

from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.utils.exceptions import AppException

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Catch all exceptions and return consistent JSON error responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except AppException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "code": exc.code,
                        "message": exc.message,
                        "details": exc.details,
                    }
                },
            )
        except RequestValidationError as exc:
            return JSONResponse(
                status_code=422,
                content={
                    "error": {
                        "code": "VALIDATION",
                        "message": "유효성 검증에 실패했습니다",
                        "details": exc.errors(),
                    }
                },
            )
        except Exception:
            logger.exception("Unhandled exception")
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "SERVER_ERROR",
                        "message": "서버 내부 오류가 발생했습니다",
                        "details": None,
                    }
                },
            )
