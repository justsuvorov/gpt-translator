import json
from pathlib import Path
from typing import Any, Dict, List

from src.core import get_logger


class JSONLoader:
    """Загружает JSON файлы."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def load(self, path: str) -> List[Dict[str, Any]]:
        """
        Загружает JSON файл.

        Args:
            path: Путь к JSON файлу

        Returns:
            Список словарей
        """
        self.logger.debug(f"Loading JSON from {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.logger.debug(f"Loaded {len(data)} items")
        return data


class JSONLConverter:
    """Конвертирует данные в JSONL формат."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def to_jsonl(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Конвертирует список в JSONL формат.

        Args:
            data: Список словарей
            output_path: Путь для сохранения
        """
        self.logger.debug(f"Converting to JSONL: {output_path}")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        self.logger.debug(f"Saved {len(data)} lines to JSONL")

    def from_jsonl(self, path: str) -> List[Dict[str, Any]]:
        """
        Загружает JSONL файл.

        Args:
            path: Путь к JSONL файлу

        Returns:
            Список словарей
        """
        self.logger.debug(f"Loading JSONL from {path}")

        data = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))

        self.logger.debug(f"Loaded {len(data)} items")
        return data
