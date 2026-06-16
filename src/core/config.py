from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения."""

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
