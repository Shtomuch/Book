from typing import Any, ClassVar

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/bookdb"
    )
    secret_key: str = Field(default="change-me-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    environment: str = Field(default="development")

    api_v1_prefix: ClassVar[str] = "/api/v1"
    project_name: ClassVar[str] = "Book Management System"
    version: ClassVar[str] = "0.1.0"

    @field_validator("database_url", mode="before")
    @classmethod
    def validate_database_url(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.replace("postgresql://", "postgresql+asyncpg://")
        return v


settings = Settings()