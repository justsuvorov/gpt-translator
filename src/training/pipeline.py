from pathlib import Path
from typing import Any, Dict

from src.core import get_logger
from src.training.data_handler import TranslationDataHandler
from src.training.model import OpenAIModelTrainer


class TrainingPipeline:
    """Основной pipeline для обучения модели."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_handler = TranslationDataHandler(config)
        self.trainer = OpenAIModelTrainer(config)
        self.logger = get_logger(__name__)

    def run(self, data_source: str, wait_for_completion: bool = True) -> str:
        """
        Запускает полный pipeline: подготовка данных -> обучение -> ожидание.

        Args:
            data_source: Путь к исходному JSON файлу
            wait_for_completion: Ждать ли завершения обучения

        Returns:
            ID обученной модели
        """
        self.logger.info("=" * 60)
        self.logger.info("Starting Training Pipeline")
        self.logger.info("=" * 60)

        # Шаг 1: Подготовка данных
        self.logger.info("\n[Step 1] Preparing data...")
        processed_path = self.config["training"]["dataset_path"]
        if not self._prepare_data(data_source, processed_path):
            raise Exception("Data preparation failed")

        # Шаг 2: Запуск обучения
        self.logger.info("\n[Step 2] Starting fine-tuning...")
        job_id = self.trainer.start_training(processed_path)
        self.logger.info(f"Training job ID: {job_id}")

        # Шаг 3: Ожидание завершения (опционально)
        if wait_for_completion:
            self.logger.info("\n[Step 3] Waiting for training completion...")
            model_id = self.trainer.wait_completion(job_id)

            self.logger.info("\n" + "=" * 60)
            self.logger.info(f"✓ Training completed successfully!")
            self.logger.info(f"✓ Model ID: {model_id}")
            self.logger.info("=" * 60)

            return model_id

        else:
            self.logger.info(f"\n[Step 3] Skipped (wait_for_completion=False)")
            self.logger.info(f"Training job ID: {job_id}")
            self.logger.info(
                "Monitor the training with: trainer.get_status('{job_id}')"
            )

            return job_id

    def _prepare_data(self, input_path: str, output_path: str) -> bool:
        """Подготавливает данные для обучения."""
        try:
            if not self.data_handler.process(input_path, output_path):
                return False

            # Разбивка на train/validation
            split_ratio = self.config["training"].get("validation_split", 0.2)
            self.data_handler.split_train_validation(output_path, split_ratio)

            return True

        except Exception as e:
            self.logger.error(f"Data preparation error: {e}")
            return False

    def list_training_jobs(self) -> None:
        """Выводит список всех задач обучения."""
        self.logger.info("\nFine-tuning Jobs:")
        jobs = self.trainer.list_jobs()

        for job in jobs:
            status_emoji = "✓" if job["status"] == "succeeded" else "⏳"
            self.logger.info(
                f"{status_emoji} {job['job_id']:<20} | "
                f"Status: {job['status']:<10} | Model: {job['fine_tuned_model']}"
            )
