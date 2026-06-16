import time
from typing import Any, Dict, Optional

from openai import OpenAI

from src.core import get_logger
from src.core.interfaces import ModelTrainer





class OpenAIModelTrainer(ModelTrainer):
    """Управляет fine-tuning моделей OpenAI."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = OpenAI(api_key=config["openai"]["api_key"])
        self.base_model = config["fine_tuning"]["model"]
        self.suffix = config["fine_tuning"].get("suffix", "translation")
        self.logger = get_logger(__name__)

    def start_training(self, data_path: str) -> str:
        """
        Запускает fine-tuning на OpenAI.

        Args:
            data_path: Путь к JSONL файлу с данными

        Returns:
            ID задачи обучения
        """
        try:
            self.logger.info(f"Uploading training data from {data_path}")

            # Загрузка файла
            with open(data_path, "rb") as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune",
                )
            file_id = response.id
            self.logger.info(f"File uploaded: {file_id}")

            # Запуск fine-tuning
            self.logger.info(f"Starting fine-tuning with model {self.base_model}")
            job = self.client.fine_tuning.jobs.create(
                training_file=file_id,
                model=self.base_model,
                suffix=self.suffix,
            )

            job_id = job.id
            self.logger.info(f"Fine-tuning job created: {job_id}")

            return job_id

        except Exception as e:
            self.logger.error(f"Failed to start training: {e}")
            raise

    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Получает статус задачи обучения.

        Args:
            job_id: ID задачи

        Returns:
            Словарь со статусом и информацией
        """
        try:
            job = self.client.fine_tuning.jobs.retrieve(job_id)

            status_info = {
                "job_id": job.id,
                "status": job.status,
                "model": job.model,
                "fine_tuned_model": job.fine_tuned_model or "Not ready",
                "created_at": job.created_at,
                "finished_at": job.finished_at,
            }

            self.logger.info(f"Job {job_id} status: {job.status}")

            return status_info

        except Exception as e:
            self.logger.error(f"Failed to get status: {e}")
            raise

    def wait_completion(
        self, job_id: str, check_interval: int = 30, max_wait: int = 86400
    ) -> str:
        """
        Ожидает завершения обучения.

        Args:
            job_id: ID задачи
            check_interval: Интервал проверки в секундах
            max_wait: Максимальное время ожидания в секундах

        Returns:
            ID обученной модели
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_info = self.get_status(job_id)

            if status_info["status"] == "succeeded":
                model_id = status_info["fine_tuned_model"]
                self.logger.info(f"Training completed! Model ID: {model_id}")
                return model_id

            elif status_info["status"] == "failed":
                raise Exception(f"Training failed for job {job_id}")

            elif status_info["status"] == "cancelled":
                raise Exception(f"Training cancelled for job {job_id}")

            self.logger.info(
                f"Training in progress... Status: {status_info['status']}"
            )
            time.sleep(check_interval)

        raise Exception(f"Training timeout for job {job_id}")

    def list_jobs(self) -> list[Dict[str, Any]]:
        """Получает список всех задач обучения."""
        try:
            jobs = self.client.fine_tuning.jobs.list()
            return [
                {
                    "job_id": job.id,
                    "status": job.status,
                    "model": job.model,
                    "fine_tuned_model": job.fine_tuned_model or "Not ready",
                }
                for job in jobs.data
            ]
        except Exception as e:
            self.logger.error(f"Failed to list jobs: {e}")
            raise
