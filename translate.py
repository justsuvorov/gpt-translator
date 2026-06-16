#!/usr/bin/env python3
"""
Translator app entry point для использования переводчика.

Usage:
    python translate.py --gui                      # Запуск GUI приложения
    python translate.py --text "Hello"             # Перевести текст
    python translate.py --file input.txt           # Перевести из файла
    python translate.py --model ft-xxx123 --gui    # Использовать fine-tuned модель
"""

import argparse
import sys
from pathlib import Path

from src.core import ConfigLoader, Logger, get_logger
from src.translator import GPTTranslator, TranslatorApp





def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(
        description="Translate text using fine-tuned GPT model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch GUI application
  python translate.py --gui

  # Translate single text
  python translate.py --text "Hello world"

  # Translate file
  python translate.py --file data.txt

  # Use fine-tuned model
  python translate.py --model ft-xxx123 --gui

  # Translate with specific model
  python translate.py --text "Hello" --model gpt-4o-mini
        """,
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch PyEdifice GUI application",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Text to translate",
    )

    parser.add_argument(
        "--file",
        type=str,
        help="File with text to translate",
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Model ID to use (fine-tuned or default)",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Save output to file",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Инициализация логирования
    Logger.configure(log_level=args.log_level)
    logger = get_logger(__name__)

    try:
        # Загрузка конфигурации
        config_loader = ConfigLoader()
        config = config_loader.get_main_config()

        # Создание переводчика
        translator = GPTTranslator(config, model_id=args.model)

        # GUI режим
        if args.gui:
            logger.info("Launching GUI application...")
            app = TranslatorApp(translator, config)
            app.run()
            return 0

        # Перевод текста
        elif args.text:
            logger.info(f"Translating text...")
            result = translator.translate(args.text)

            logger.info("=" * 60)
            logger.info("RESULT:")
            logger.info("=" * 60)
            print(result)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {args.output}")

            return 0

        # Перевод файла
        elif args.file:
            if not Path(args.file).exists():
                logger.error(f"File not found: {args.file}")
                return 1

            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()

            logger.info(f"Translating file: {args.file}")
            result = translator.translate(text)

            logger.info("=" * 60)
            logger.info("RESULT:")
            logger.info("=" * 60)
            print(result)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {args.output}")
            else:
                output_path = Path(args.file).stem + "_translated.txt"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)
                logger.info(f"Saved to: {output_path}")

            return 0

        else:
            parser.print_help()
            return 1

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
