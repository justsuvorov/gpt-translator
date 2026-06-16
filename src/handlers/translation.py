from pathlib import Path
from typing import Any, Dict, Optional

from src.core import get_logger
from src.translator.translator import GPTTranslator


class TextTranslationHandler:
    """Обрабатывает перевод текста."""

    def __init__(self, translator: GPTTranslator, config: Dict[str, Any]):
        self.translator = translator
        self.config = config
        self.logger = get_logger(__name__)

    def translate(self, text: str, output: Optional[str] = None) -> str:
        """
        Переводит текст.

        Args:
            text: Текст для перевода
            output: Опциональный путь для сохранения

        Returns:
            Переведённый текст
        """
        self.logger.info("Translating text...")

        result = self.translator.translate(text)

        self.logger.info("=" * 60)
        self.logger.info("RESULT:")
        self.logger.info("=" * 60)
        print(result)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            self.logger.info(f"Saved to: {output}")

        return result


class FileTranslationHandler:
    """Обрабатывает перевод файла."""

    def __init__(self, translator: GPTTranslator, config: Dict[str, Any]):
        self.translator = translator
        self.config = config
        self.logger = get_logger(__name__)

    def translate(self, file_path: str, output: Optional[str] = None) -> str:
        """
        Переводит файл.

        Args:
            file_path: Путь к файлу
            output: Опциональный путь для сохранения

        Returns:
            Переведённый текст
        """
        if not Path(file_path).exists():
            self.logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.logger.info(f"Translating file: {file_path}")

        result = self.translator.translate(text)

        self.logger.info("=" * 60)
        self.logger.info("RESULT:")
        self.logger.info("=" * 60)
        print(result)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            self.logger.info(f"Saved to: {output}")
        else:
            output_path = Path(file_path).stem + "_translated.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)
            self.logger.info(f"Saved to: {output_path}")

        return result


class GUITranslationHandler:
    """Обрабатывает запуск GUI приложения."""

    def __init__(self, translator: GPTTranslator, config: Dict[str, Any]):
        self.translator = translator
        self.config = config
        self.logger = get_logger(__name__)

    def launch(self) -> None:
        """Запускает GUI приложение."""
        from src.translator.app import TranslatorApp

        self.logger.info("Launching GUI application...")

        app = TranslatorApp(self.translator, self.config)
        app.run()
