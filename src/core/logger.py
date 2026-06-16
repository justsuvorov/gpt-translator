import sys
from pathlib import Path

from loguru import logger as _logger


class Logger:
    """Централизованный логгер на основе loguru."""

    _configured = False

    @classmethod
    def configure(cls, log_level: str = "INFO", log_dir: str = "logs") -> None:
        """
        Настраивает логгер.

        Args:
            log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
            log_dir: Директория для логов
        """
        if cls._configured:
            return

        # Создание директории логов
        Path(log_dir).mkdir(exist_ok=True)

        # Удаление стандартного обработчика
        _logger.remove()

        # Консольный вывод
        _logger.add(
            sys.stdout,
            level=log_level,
            format="<level>{time:HH:mm:ss}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
            colorize=True,
        )

        # Логи в файл (общий)
        _logger.add(
            f"{log_dir}/app.log",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="500 MB",
            retention="7 days",
        )

        # Логи в файл (по ошибкам)
        _logger.add(
            f"{log_dir}/errors.log",
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="500 MB",
            retention="7 days",
        )

        cls._configured = True

    @classmethod
    def get(cls, name: str = None):
        """Получить логгер."""
        return _logger.bind(name=name or "app")


# Удобный импорт
def get_logger(name: str = None):
    """
    Получить логгер для модуля.

    Args:
        name: Имя модуля/логгера

    Returns:
        Объект логгера loguru
    """
    if name is None:
        name = "app"
    return _logger.bind(name=name)
