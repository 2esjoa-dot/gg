"""Custom exception classes and error codes for the application."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, code: str, message: str, status_code: int = 400, details: dict | None = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class AuthenticationError(AppException):
    """Authentication failure (401)."""

    def __init__(self, code: str = "AUTH_INVALID", message: str = "인증 정보가 올바르지 않습니다"):
        super().__init__(code=code, message=message, status_code=401)


class AccountLockedError(AppException):
    """Account locked due to too many login attempts (401)."""

    def __init__(self, remaining_minutes: int):
        super().__init__(
            code="AUTH_LOCKED",
            message=f"계정이 잠겨있습니다. {remaining_minutes}분 후 재시도해 주세요",
            status_code=401,
        )


class TokenExpiredError(AppException):
    """JWT token has expired (401)."""

    def __init__(self):
        super().__init__(code="AUTH_EXPIRED", message="토큰이 만료되었습니다", status_code=401)


class AuthorizationError(AppException):
    """Authorization failure - insufficient permissions (403)."""

    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(code="FORBIDDEN", message=message, status_code=403)


class NotFoundError(AppException):
    """Resource not found (404)."""

    def __init__(self, resource: str = "리소스"):
        super().__init__(code="NOT_FOUND", message=f"{resource}을(를) 찾을 수 없습니다", status_code=404)


class DuplicateError(AppException):
    """Duplicate resource (409)."""

    def __init__(self, resource: str = "데이터"):
        super().__init__(code="DUPLICATE", message=f"이미 존재하는 {resource}입니다", status_code=409)


class ValidationError(AppException):
    """Validation failure (422)."""

    def __init__(self, message: str = "유효성 검증에 실패했습니다", details: dict | None = None):
        super().__init__(code="VALIDATION", message=message, status_code=422, details=details)


class InvalidStatusError(AppException):
    """Invalid status transition (400)."""

    def __init__(self, message: str = "허용되지 않는 상태 변경입니다"):
        super().__init__(code="INVALID_STATUS", message=message, status_code=400)


class NoActiveSessionError(AppException):
    """No active session found (400)."""

    def __init__(self):
        super().__init__(code="NO_ACTIVE_SESSION", message="활성 세션이 없습니다", status_code=400)
