from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core import get_logger


class Command(ABC):
    """Абстрактная команда CLI."""

    name: str
    description: str
    help: str

    @abstractmethod
    def execute(self, **kwargs) -> int:
        """
        Выполняет команду.

        Returns:
            Код выхода (0 = успех, 1 = ошибка)
        """
        pass


class TrainingCommands:
    """Команды для обучения модели."""

    @staticmethod
    def start_training(
        data: str,
        wait: bool = False,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Запускает обучение модели."""
        from src.core import ConfigLoader, Logger
        from src.training import TrainingPipeline
        from pathlib import Path

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            if not Path(data).exists():
                logger.error(f"Data file not found: {data}")
                return 1

            logger.info(f"Starting training with data from: {data}")

            config_loader = ConfigLoader()
            main_config = config_loader.get_main_config()
            training_config = config_loader.get_training_config()
            config = {**main_config, **training_config}

            pipeline = TrainingPipeline(config)
            model_id = pipeline.run(data, wait_for_completion=wait)

            if wait:
                logger.info(f"✓ Model successfully trained: {model_id}")
            else:
                logger.info(f"✓ Training job started")
                logger.info(f"  Job ID: {model_id}")
                logger.info(f"  Check status with: --job-id {model_id}")

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def check_status(job_id: str, log_level: str = "INFO", **kwargs) -> int:
        """Проверяет статус обучения."""
        from src.core import ConfigLoader, Logger
        from src.training import OpenAIModelTrainer

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)
            logger.info(f"Checking status of job: {job_id}")

            config_loader = ConfigLoader()
            main_config = config_loader.get_main_config()
            training_config = config_loader.get_training_config()
            config = {**main_config, **training_config}

            trainer = OpenAIModelTrainer(config)
            status = trainer.get_status(job_id)

            logger.info(f"Job ID: {status['job_id']}")
            logger.info(f"Status: {status['status']}")
            logger.info(f"Model: {status['fine_tuned_model']}")

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def list_jobs(log_level: str = "INFO", **kwargs) -> int:
        """Выводит список всех задач обучения."""
        from src.core import ConfigLoader, Logger
        from src.training import TrainingPipeline

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config_loader = ConfigLoader()
            main_config = config_loader.get_main_config()
            training_config = config_loader.get_training_config()
            config = {**main_config, **training_config}

            pipeline = TrainingPipeline(config)
            pipeline.list_training_jobs()

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1


class TranslationCommands:
    """Команды для перевода."""

    @staticmethod
    def launch_gui(model: Optional[str] = None, log_level: str = "INFO", **kwargs) -> int:
        """Запускает GUI приложение."""
        from src.core import ConfigLoader, Logger
        from src.translator import GPTTranslator, TranslatorApp

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config_loader = ConfigLoader()
            config = config_loader.get_main_config()

            translator = GPTTranslator(config, model_id=model)
            app = TranslatorApp(translator, config)
            app.run()

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def translate_text(
        text: str,
        model: Optional[str] = None,
        output: Optional[str] = None,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Переводит текст."""
        from src.core import ConfigLoader, Logger
        from src.translator import GPTTranslator

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)
            logger.info("Translating text...")

            config_loader = ConfigLoader()
            config = config_loader.get_main_config()

            translator = GPTTranslator(config, model_id=model)
            result = translator.translate(text)

            logger.info("=" * 60)
            logger.info("RESULT:")
            logger.info("=" * 60)
            print(result)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {output}")

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def translate_file(
        file: str,
        model: Optional[str] = None,
        output: Optional[str] = None,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Переводит файл."""
        from pathlib import Path
        from src.core import ConfigLoader, Logger
        from src.translator import GPTTranslator

        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            if not Path(file).exists():
                logger.error(f"File not found: {file}")
                return 1

            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

            logger.info(f"Translating file: {file}")

            config_loader = ConfigLoader()
            config = config_loader.get_main_config()

            translator = GPTTranslator(config, model_id=model)
            result = translator.translate(text)

            logger.info("=" * 60)
            logger.info("RESULT:")
            logger.info("=" * 60)
            print(result)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {output}")
            else:
                output_path = Path(file).stem + "_translated.txt"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {output_path}")

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1
