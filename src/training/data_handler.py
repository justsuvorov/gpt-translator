import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from ..core.interfaces import DataProcessor
from .validator import TranslationDataValidator


class TranslationDataHandler(DataProcessor):
    """Обрабатывает и подготавливает данные для fine-tuning."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.validator = TranslationDataValidator(config)
        self.logger = logging.getLogger(__name__)

    def process(self, input_path: str, output_path: str) -> bool:
        """
        Загружает JSON, валидирует и сохраняет в JSONL формат.

        Args:
            input_path: Путь к исходному JSON файлу
            output_path: Путь для JSONL файла

        Returns:
            True если успешно
        """
        try:
            self.logger.info(f"Loading data from {input_path}")
            data = self._load_json(input_path)

            self.logger.info(f"Validating {len(data)} samples")
            is_valid, errors = self.validator.validate(data)

            if not is_valid:
                self.logger.error("Validation failed:")
                for error in errors:
                    self.logger.error(f"  - {error}")
                return False

            self.logger.info("Validation passed")

            # Сохранение в JSONL формат
            self._save_jsonl(data, output_path)
            self.logger.info(f"Saved {len(data)} samples to {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return False

    def _load_json(self, path: str) -> List[Dict[str, Any]]:
        """Загружает JSON файл."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_jsonl(self, data: List[Dict[str, Any]], path: str) -> None:
        """Сохраняет данные в JSONL формат."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def split_train_validation(
        self, data_path: str, split_ratio: float = 0.2
    ) -> tuple[str, str]:
        """
        Разбивает данные на training и validation наборы.

        Args:
            data_path: Путь к JSONL файлу
            split_ratio: Доля для validation набора

        Returns:
            (train_path, val_path)
        """
        data = self._load_jsonl(data_path)
        split_index = int(len(data) * (1 - split_ratio))

        train_data = data[:split_index]
        val_data = data[split_index:]

        data_dir = Path(data_path).parent
        train_path = str(data_dir / "training_data.jsonl")
        val_path = str(data_dir / "validation_data.jsonl")

        self._save_jsonl(train_data, train_path)
        self._save_jsonl(val_data, val_path)

        self.logger.info(
            f"Split data: {len(train_data)} training, {len(val_data)} validation"
        )

        return train_path, val_path

    def _load_jsonl(self, path: str) -> List[Dict[str, Any]]:
        """Загружает JSONL файл."""
        data = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data
