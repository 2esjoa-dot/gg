"""Authentication and authorization middleware."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.utils.exceptions import AuthenticationError, AuthorizationError, TokenExpiredError
from app.utils.security import decode_access_token

# Paths that do not require authentication
PUBLIC_PATHS = {"/docs", "/redoc", "/openapi.json", "/health", "/uploads"}

# Role-to-path prefix mapping
ROLE_PATH_MAP = {
    "tablet": "/api/customer/",
    "store_admin": "/api/admin/",
    "hq_admin": "/api/hq/",
}


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT-based authentication and role-based authorization."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Skip auth for public paths
        if self._is_public(path):
            return await call_next(request)

        # Skip auth for non-API paths (static files, etc.)
        if not path.startswith("/api/"):
            return await call_next(request)

        # Extract token
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationError()

        token = auth_header[7:]
        payload = decode_access_token(token)
        if payload is None:
            raise TokenExpiredError()

        # Check role-based access
        role = payload.get("role", "")
        if not self._check_role_access(role, path):
            raise AuthorizationError()

        # Set user context on request state
        request.state.user = payload
        request.state.store_id = payload.get("store_id")
        request.state.role = role

        return await call_next(request)

    @staticmethod
    def _is_public(path: str) -> bool:
        """Check if the path is public (no auth required)."""
        for public_path in PUBLIC_PATHS:
            if path == public_path or path.startswith(public_path + "/"):
                return True
        return False

    @staticmethod
    def _check_role_access(role: str, path: str) -> bool:
        """Verify the role has access to the requested path."""
        allowed_prefix = ROLE_PATH_MAP.get(role)
        if allowed_prefix is None:
            return False
        return path.startswith(allowed_prefix)
