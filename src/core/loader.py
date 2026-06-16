from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from src.core import get_logger


class ConfigLoader:
    """Загружает конфигурацию из YAML файлов."""

    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.logger = get_logger(__name__)
        load_dotenv()

    def load_all(self) -> Dict[str, Any]:
        """
        Загружает все конфигурации в один словарь.

        Returns:
            Объединённая конфигурация (main + training)
        """
        self.logger.debug("Loading all configurations")
        main_config = self.load_config("config.yaml")
        training_config = self.load_config("training_config.yaml")
        return {**main_config, **training_config}

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

        self.logger.debug(f"Loading config from {filename}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Подстановка переменных окружения
        config = self._substitute_env_vars(config)

        return config

    @staticmethod
    def _substitute_env_vars(config: Any) -> Any:
        """Подставляет переменные окружения в конфиге."""
        import os

        if isinstance(config, dict):
            return {k: ConfigLoader._substitute_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [ConfigLoader._substitute_env_vars(item) for item in config]
        elif isinstance(config, str):
            if config.startswith("${") and config.endswith("}"):
                env_var = config[2:-1]
                return os.getenv(env_var, config)
            return config
        return config
