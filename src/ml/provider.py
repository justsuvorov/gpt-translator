from typing import Any, Dict, Optional

from openai import OpenAI

from src.core import get_logger


class OpenAIModelProvider:
    """Предоставляет доступ к моделям OpenAI."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = OpenAI(api_key=config["openai"]["api_key"])
        self.base_model = config["openai"]["model"]
        self.logger = get_logger(__name__)

    def get_client(self) -> OpenAI:
        """Получает OpenAI клиент."""
        return self.client

    def get_base_model(self) -> str:
        """Получает имя базовой модели."""
        return self.base_model

    def get_config(self) -> Dict[str, Any]:
        """Получает конфигурацию."""
        return self.config
