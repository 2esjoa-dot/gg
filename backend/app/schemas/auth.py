from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)


class TabletLoginRequest(BaseModel):
    store_code: str = Field(..., min_length=1, max_length=50)
    table_number: int = Field(..., gt=0)
    password: str = Field(..., min_length=4)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=4)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
