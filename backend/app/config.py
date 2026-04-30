"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment variables and .env file."""

    # App
    APP_NAME: str = "table-order-api"
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/table_order_dev"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # JWT
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 16
    JWT_ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list[str] = ["jpg", "jpeg", "png", "webp"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_MAX_DAYS: int = 30

    # Bcrypt
    BCRYPT_ROUNDS: int = 12

    # Login Security
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCK_DURATION_MINUTES: int = 15

    # Session
    SESSION_EXPIRE_HOURS: int = 16

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
