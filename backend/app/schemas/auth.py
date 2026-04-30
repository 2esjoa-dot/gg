"""Authentication request/response schemas."""

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    """Admin login request."""

    store_code: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)


class TabletLoginRequest(BaseModel):
    """Tablet (customer) login request."""

    store_code: str = Field(..., min_length=1, max_length=50)
    table_number: int = Field(..., gt=0)
    password: str = Field(..., min_length=4)


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RegisterAdminRequest(BaseModel):
    """Admin account registration request."""

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=4)
    role: str = Field(default="store_admin")
