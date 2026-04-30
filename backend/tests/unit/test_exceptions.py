"""Unit tests for custom exception classes."""

from app.utils.exceptions import (
    AccountLockedError,
    AppException,
    AuthenticationError,
    AuthorizationError,
    DuplicateError,
    InvalidStatusError,
    NoActiveSessionError,
    NotFoundError,
    TokenExpiredError,
    ValidationError,
)


class TestAppException:
    """Tests for base AppException."""

    def test_base_exception_attributes(self):
        exc = AppException(code="TEST", message="test message", status_code=400)
        assert exc.code == "TEST"
        assert exc.message == "test message"
        assert exc.status_code == 400
        assert exc.details is None

    def test_base_exception_with_details(self):
        exc = AppException(code="TEST", message="msg", status_code=400, details={"field": "error"})
        assert exc.details == {"field": "error"}


class TestAuthExceptions:
    """Tests for authentication-related exceptions."""

    def test_authentication_error_defaults(self):
        exc = AuthenticationError()
        assert exc.status_code == 401
        assert exc.code == "AUTH_INVALID"

    def test_account_locked_error(self):
        exc = AccountLockedError(remaining_minutes=10)
        assert exc.status_code == 401
        assert exc.code == "AUTH_LOCKED"
        assert "10분" in exc.message

    def test_token_expired_error(self):
        exc = TokenExpiredError()
        assert exc.status_code == 401
        assert exc.code == "AUTH_EXPIRED"

    def test_authorization_error(self):
        exc = AuthorizationError()
        assert exc.status_code == 403
        assert exc.code == "FORBIDDEN"


class TestBusinessExceptions:
    """Tests for business logic exceptions."""

    def test_not_found_error(self):
        exc = NotFoundError("매장")
        assert exc.status_code == 404
        assert "매장" in exc.message

    def test_duplicate_error(self):
        exc = DuplicateError("매장 코드")
        assert exc.status_code == 409
        assert "매장 코드" in exc.message

    def test_validation_error(self):
        exc = ValidationError(message="가격은 양수여야 합니다")
        assert exc.status_code == 422

    def test_invalid_status_error(self):
        exc = InvalidStatusError()
        assert exc.status_code == 400

    def test_no_active_session_error(self):
        exc = NoActiveSessionError()
        assert exc.status_code == 400
        assert exc.code == "NO_ACTIVE_SESSION"
