from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseSettings(BaseSettings):
    DB_HOST: str = Field(default="localhost")
    DB_NAME: str = Field(default="rinha2024q1")
    DB_USER: str = Field(default="postgres")
    DB_PASS: str = Field(default="postgres")
    DB_PORT: int = Field(default=5432)
    DB_MAX_CONNECTIONS: int = Field(default=100)
