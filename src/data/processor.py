from pathlib import Path
from typing import Any, Dict

from src.core import get_logger
from src.data.loaders import JSONLConverter, JSONLoader
from src.training.validator import TranslationDataValidator


class DataProcessor:
    """Обрабатывает и подготавливает данные для fine-tuning."""

    def __init__(
        self,
        json_loader: JSONLoader,
        jsonl_converter: JSONLConverter,
        data_validator: TranslationDataValidator,
    ):
        self.json_loader = json_loader
        self.jsonl_converter = jsonl_converter
        self.validator = data_validator
        self.logger = get_logger(__name__)

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
            data = self.json_loader.load(input_path)

            self.logger.info(f"Validating {len(data)} samples")
            is_valid, errors = self.validator.validate(data)

            if not is_valid:
                self.logger.error("Validation failed:")
                for error in errors:
                    self.logger.error(f"  - {error}")
                return False

            self.logger.info("Validation passed")

            # Сохранение в JSONL формат
            self.jsonl_converter.to_jsonl(data, output_path)
            self.logger.info(f"Saved {len(data)} samples to {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Processing failed: {e}", exc_info=True)
            return False

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
        self.logger.info(f"Splitting data with ratio {split_ratio}")

        data = self.jsonl_converter.from_jsonl(data_path)
        split_index = int(len(data) * (1 - split_ratio))

        train_data = data[:split_index]
        val_data = data[split_index:]

        data_dir = Path(data_path).parent
        train_path = str(data_dir / "training_data.jsonl")
        val_path = str(data_dir / "validation_data.jsonl")

        self.jsonl_converter.to_jsonl(train_data, train_path)
        self.jsonl_converter.to_jsonl(val_data, val_path)

        self.logger.info(
            f"Split data: {len(train_data)} training, {len(val_data)} validation"
        )

        return train_path, val_path
