from enum import Enum

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "development"
    PROD = "production"
    TEST = "test"


class Settings(BaseSettings):
    # --- APP SETTINGS ---
    PROJECT_NAME: str = "OwnIt-Backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: Environment = Environment.DEV

    # --- DATABASE SETTINGS ---
    # Sync — Alembic only
    DB_URL: PostgresDsn = "postgresql+psycopg2://admin:secret@database:5432/ownit_db"  # type: ignore
    TEST_DB_URL: PostgresDsn = (
        "postgresql+psycopg2://admin:secret@database:5432/ownit_test_db"  # type: ignore
    )
    # Async — application
    ASYNC_DB_URL: str = "postgresql+asyncpg://admin:secret@database:5432/ownit_db"
    ASYNC_TEST_DB_URL: str = (
        "postgresql+asyncpg://admin:secret@database:5432/ownit_test_db"
    )

    DB_ECHO_SQL: bool = False  # Set to True in .env to see SQL in console

    # --- REDIS SETTINGS ---
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_TEST_URL: str = "redis://redis:6379/1"
    REDIS_MAX_CONNECTIONS: int | None = None

    # --- SECURITY ---
    SECRET_KEY: str = None  # type: ignore # Required — no default, must be set in .env

    # --- LOGGING ---
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == Environment.DEV


# Global instance of Settings
settings = Settings()
