from pathlib import Path
from typing import Any, Dict

from src.core import get_logger
from src.data import DataProcessor
from src.ml import FineTuner


class TrainingHandler:
    """Оркестрирует процесс обучения модели."""

    def __init__(
        self,
        data_processor: DataProcessor,
        model_trainer: FineTuner,
        config: Dict[str, Any],
    ):
        self.data_processor = data_processor
        self.model_trainer = model_trainer
        self.config = config
        self.logger = get_logger(__name__)

    def start(self, data_source: str, wait: bool = False) -> str:
        """
        Запускает полный pipeline: подготовка данных -> обучение -> ожидание.

        Args:
            data_source: Путь к исходному JSON файлу
            wait: Ждать ли завершения обучения

        Returns:
            ID модели или ID задачи обучения
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
        job_id = self.model_trainer.start_training(processed_path)
        self.logger.info(f"Training job ID: {job_id}")

        # Шаг 3: Ожидание завершения (опционально)
        if wait:
            self.logger.info("\n[Step 3] Waiting for training completion...")
            model_id = self.model_trainer.wait_completion(job_id)

            self.logger.info("\n" + "=" * 60)
            self.logger.info(f"✓ Training completed successfully!")
            self.logger.info(f"✓ Model ID: {model_id}")
            self.logger.info("=" * 60)

            return model_id
        else:
            self.logger.info(f"\n[Step 3] Skipped (wait=False)")
            self.logger.info(f"Training job ID: {job_id}")
            self.logger.info(f"Monitor the training with: train.py status --job-id {job_id}")

            return job_id

    def check_status(self, job_id: str) -> Dict[str, Any]:
        """Проверяет статус обучения."""
        self.logger.info(f"Checking status of job: {job_id}")
        status = self.model_trainer.get_status(job_id)

        self.logger.info(f"Job ID: {status['job_id']}")
        self.logger.info(f"Status: {status['status']}")
        self.logger.info(f"Model: {status['fine_tuned_model']}")

        return status

    def list_jobs(self) -> None:
        """Выводит список всех задач обучения."""
        self.logger.info("\nFine-tuning Jobs:")
        jobs = self.model_trainer.list_jobs()

        for job in jobs:
            status_emoji = "✓" if job["status"] == "succeeded" else "⏳"
            self.logger.info(
                f"{status_emoji} {job['job_id']:<20} | "
                f"Status: {job['status']:<10} | Model: {job['fine_tuned_model']}"
            )

    def _prepare_data(self, input_path: str, output_path: str) -> bool:
        """Подготавливает данные для обучения."""
        try:
            if not self.data_processor.process(input_path, output_path):
                return False

            # Разбивка на train/validation
            split_ratio = self.config["training"].get("validation_split", 0.2)
            self.data_processor.split_train_validation(output_path, split_ratio)

            return True

        except Exception as e:
            self.logger.error(f"Data preparation error: {e}", exc_info=True)
            return False
