"""Application Settings."""
import secrets
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class LogLevel(str, Enum):
    """Log Levels enumeration."""

    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"

    def __str__(self) -> str:
        """Override __str__ builtin."""
        return self.value


class Settings(BaseSettings):
    """Flask Application Settings."""

    LOG_FMT: str = "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s"
    LOG_DATEFMT: str = "%Y-%m-%d %H:%M:%S %z"
    LOG_LEVEL: LogLevel = LogLevel.INFO

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MONGODB_DB: str
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str

    MONGODB_URI: Optional[str] = None

    @validator("MONGODB_URI", pre=True)
    def assemble_mongodb_uri(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        """Create MongoDB URI."""
        if v:
            return v
        username = values.get("MONGODB_USERNAME")
        password = values.get("MONGODB_PASSWORD")
        host = values.get("MONGODB_HOST")
        port = values.get("MONGODB_PORT")
        return f"mongodb://{username}:{password}@{host}:{port}"

    class Config:
        """Config for pydantic."""

        case_sensitive = True


SETTINGS = Settings()
