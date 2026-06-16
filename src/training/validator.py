import json
from typing import Any, Dict, List

from src.core import get_logger
from src.core.interfaces import DataValidator


class TranslationDataValidator(DataValidator):
    """Валидирует данные для обучения переводчика."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("validation", {})
        self.logger = get_logger(__name__)

    def validate(self, data: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
        """Валидирует список образцов для обучения."""
        errors = []

        # Проверка количества образцов
        min_samples = self.config.get("min_samples", 5)
        max_samples = self.config.get("max_samples", 10000)

        if len(data) < min_samples:
            errors.append(f"Too few samples: {len(data)} < {min_samples}")

        if len(data) > max_samples:
            errors.append(f"Too many samples: {len(data)} > {max_samples}")

        # Проверка каждого образца
        required_fields = self.config.get("required_fields", ["messages", "completion"])
        for i, item in enumerate(data):
            item_errors = self._validate_item(item, i, required_fields)
            errors.extend(item_errors)

        is_valid = len(errors) == 0
        return is_valid, errors

    def _validate_item(
        self, item: Dict[str, Any], index: int, required_fields: List[str]
    ) -> List[str]:
        """Валидирует один образец."""
        errors = []

        # Проверка обязательных полей
        for field in required_fields:
            if field not in item:
                errors.append(f"Sample {index}: missing required field '{field}'")

        if "messages" in item:
            messages = item["messages"]
            if not isinstance(messages, list):
                errors.append(f"Sample {index}: 'messages' must be a list")
            elif len(messages) < 2:
                errors.append(f"Sample {index}: 'messages' must have at least 2 items")
            else:
                # Проверка структуры messages
                for msg_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        errors.append(
                            f"Sample {index}: message {msg_idx} is not a dict"
                        )
                    elif "role" not in msg or "content" not in msg:
                        errors.append(
                            f"Sample {index}: message {msg_idx} missing 'role' or 'content'"
                        )

        if "completion" in item:
            completion = item["completion"]
            if not isinstance(completion, str):
                errors.append(f"Sample {index}: 'completion' must be a string")
            elif not completion.strip():
                errors.append(f"Sample {index}: 'completion' is empty")

        return errors
