import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
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


class ConfigLoader:
    """Загружает конфигурацию из YAML файлов."""

    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        load_dotenv()
        self.settings = Settings()

    def load_config(self, filename: str) -> Dict[str, Any]:
        """
        Загружает конфигурацию из YAML файла.

        Args:
            filename: Имя файла конфигурации

        Returns:
            Словарь с конфигурацией
        """
        config_path = self.config_dir / filename

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Подстановка переменных окружения
        config = self._substitute_env_vars(config)

        return config

    def _substitute_env_vars(self, config: Any) -> Any:
        """Подставляет переменные окружения в конфиге."""
        if isinstance(config, dict):
            return {k: self._substitute_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._substitute_env_vars(item) for item in config]
        elif isinstance(config, str):
            if config.startswith("${") and config.endswith("}"):
                env_var = config[2:-1]
                return os.getenv(env_var, config)
            return config
        return config

    def get_main_config(self) -> Dict[str, Any]:
        """Получает основную конфигурацию."""
        return self.load_config("config.yaml")

    def get_training_config(self) -> Dict[str, Any]:
        """Получает конфигурацию обучения."""
        return self.load_config("training_config.yaml")
