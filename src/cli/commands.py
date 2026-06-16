from typing import Optional

from src.core import ConfigLoader, Logger, get_logger
from src.data import DataProcessor, JSONLConverter, JSONLoader
from src.handlers.training import TrainingHandler
from src.handlers.translation import (
    FileTranslationHandler,
    GUITranslationHandler,
    TextTranslationHandler,
)
from src.ml import FineTuner, OpenAIModelProvider
from src.training.validator import TranslationDataValidator
from src.translator.translator import GPTTranslator


class TrainingCommands:
    """Команды для обучения модели."""

    @staticmethod
    def start_training(
        data: str,
        wait: bool = False,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Запускает обучение модели с composition pattern."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            # Загрузка конфигурации один раз
            config = ConfigLoader().load_all()

            # Composition: строим стек компонентов снизу вверх
            json_loader = JSONLoader()
            jsonl_converter = JSONLConverter()
            data_validator = TranslationDataValidator(config)
            data_processor = DataProcessor(json_loader, jsonl_converter, data_validator)

            model_provider = OpenAIModelProvider(config)
            model_trainer = FineTuner(model_provider)

            # Главный Handler оркестрирует всё
            training_handler = TrainingHandler(data_processor, model_trainer, config)

            # Выполнение
            result = training_handler.start(data, wait=wait)
            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def check_status(
        job_id: str,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Проверяет статус обучения."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config = ConfigLoader().load_all()

            model_provider = OpenAIModelProvider(config)
            model_trainer = FineTuner(model_provider)

            training_handler = TrainingHandler(None, model_trainer, config)
            training_handler.check_status(job_id)

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1

    @staticmethod
    def list_jobs(log_level: str = "INFO", **kwargs) -> int:
        """Выводит список всех задач обучения."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config = ConfigLoader().load_all()

            model_provider = OpenAIModelProvider(config)
            model_trainer = FineTuner(model_provider)

            training_handler = TrainingHandler(None, model_trainer, config)
            training_handler.list_jobs()

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1


class TranslationCommands:
    """Команды для перевода."""

    @staticmethod
    def launch_gui(
        model: Optional[str] = None,
        log_level: str = "INFO",
        **kwargs,
    ) -> int:
        """Запускает GUI приложение с composition pattern."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config = ConfigLoader().load_all()

            # Composition: модель -> переводчик -> GUI handler
            model_provider = OpenAIModelProvider(config)
            translator = GPTTranslator(config, model_id=model)

            gui_handler = GUITranslationHandler(translator, config)
            gui_handler.launch()

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
        """Переводит текст с composition pattern."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config = ConfigLoader().load_all()

            # Composition: модель -> переводчик -> текст handler
            model_provider = OpenAIModelProvider(config)
            translator = GPTTranslator(config, model_id=model)

            text_handler = TextTranslationHandler(translator, config)
            text_handler.translate(text, output=output)

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
        """Переводит файл с composition pattern."""
        logger = get_logger(__name__)

        try:
            Logger.configure(log_level=log_level)

            config = ConfigLoader().load_all()

            # Composition: модель -> переводчик -> файл handler
            model_provider = OpenAIModelProvider(config)
            translator = GPTTranslator(config, model_id=model)

            file_handler = FileTranslationHandler(translator, config)
            file_handler.translate(file, output=output)

            return 0

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return 1
