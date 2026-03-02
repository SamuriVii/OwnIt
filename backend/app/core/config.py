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
    DB_URL: PostgresDsn = "postgresql+psycopg2://admin:secret@db:5432/ownit_db"  # type: ignore
    DB_ECHO_SQL: bool = False  # Set to True in .env to see SQL in console

    # --- SECURITY ---
    SECRET_KEY: str = "change-me-in-production"

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
