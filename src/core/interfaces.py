from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DataValidator(ABC):
    """Интерфейс для валидации данных."""

    @abstractmethod
    def validate(self, data: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
        """
        Валидирует данные.

        Args:
            data: Список словарей с данными

        Returns:
            (is_valid, errors) - кортеж с результатом и ошибками
        """
        pass


class DataProcessor(ABC):
    """Интерфейс для обработки данных."""

    @abstractmethod
    def process(self, input_path: str, output_path: str) -> bool:
        """
        Обрабатывает данные из input в output.

        Args:
            input_path: Путь к исходным данным
            output_path: Путь для сохранения обработанных данных

        Returns:
            True если успешно
        """
        pass


class ModelTrainer(ABC):
    """Интерфейс для обучения модели."""

    @abstractmethod
    def start_training(self, data_path: str) -> str:
        """
        Запускает fine-tuning.

        Args:
            data_path: Путь к данным для обучения

        Returns:
            ID задачи обучения
        """
        pass

    @abstractmethod
    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Получает статус обучения.

        Args:
            job_id: ID задачи

        Returns:
            Информация о статусе
        """
        pass

    @abstractmethod
    def wait_completion(self, job_id: str) -> str:
        """
        Ожидает завершения обучения.

        Args:
            job_id: ID задачи

        Returns:
            ID обученной модели
        """
        pass


class Translator(ABC):
    """Интерфейс для перевода текста."""

    @abstractmethod
    def translate(self, text: str, model_id: Optional[str] = None) -> str:
        """
        Переводит текст.

        Args:
            text: Текст для перевода
            model_id: ID модели (опционально)

        Returns:
            Переведенный текст
        """
        pass
