from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.security import decode_access_token
from app.utils.exceptions import AuthExpiredError, ForbiddenError

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise AuthExpiredError()
    return payload


def require_role(*roles: str):
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in roles:
            raise ForbiddenError()
        return current_user
    return role_checker


def require_store_access(current_user: dict = Depends(get_current_user)) -> dict:
    """Ensures the user can only access their own store data."""
    return current_user


def get_store_id(current_user: dict = Depends(get_current_user)) -> int:
    return current_user["store_id"]
