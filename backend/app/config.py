from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tableorder"

    # JWT
    JWT_SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 16

    # Auth
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCK_DURATION_MINUTES: int = 15

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
