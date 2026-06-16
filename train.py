#!/usr/bin/env python3
"""
Fine-tuning entry point для обучения модели переводов.

Usage:
    python train.py --data data/raw/example_translations.json
    python train.py --data data/raw/my_translations.json --wait
    python train.py --job-id <job_id> --check-status
"""

import argparse
import sys
from pathlib import Path

from src.core import ConfigLoader, Logger, get_logger
from src.training import TrainingPipeline


def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(
        description="Fine-tune GPT model for translations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start training with default settings
  python train.py --data data/raw/example_translations.json

  # Start training and wait for completion
  python train.py --data data/raw/example_translations.json --wait

  # Check status of existing job
  python train.py --job-id ft-abcd1234

  # List all training jobs
  python train.py --list-jobs
        """,
    )

    parser.add_argument(
        "--data",
        type=str,
        help="Path to JSON file with training data",
    )

    parser.add_argument(
        "--job-id",
        type=str,
        help="Check status of specific training job",
    )

    parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for training to complete",
    )

    parser.add_argument(
        "--list-jobs",
        action="store_true",
        help="List all fine-tuning jobs",
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
        main_config = config_loader.get_main_config()
        training_config = config_loader.get_training_config()

        # Объединение конфигов
        config = {**main_config, **training_config}

        pipeline = TrainingPipeline(config)

        # Запуск обучения
        if args.data:
            if not Path(args.data).exists():
                logger.error(f"Data file not found: {args.data}")
                return 1

            logger.info(f"Starting training with data from: {args.data}")
            model_id = pipeline.run(args.data, wait_for_completion=args.wait)

            if args.wait:
                logger.info(f"✓ Model successfully trained: {model_id}")
            else:
                logger.info(f"✓ Training job started, check status with: --job-id {model_id}")

            return 0

        # Проверка статуса
        elif args.job_id:
            logger.info(f"Checking status of job: {args.job_id}")
            status = pipeline.trainer.get_status(args.job_id)

            logger.info(f"Job ID: {status['job_id']}")
            logger.info(f"Status: {status['status']}")
            logger.info(f"Model: {status['fine_tuned_model']}")

            return 0

        # Список всех задач
        elif args.list_jobs:
            logger.info("Fine-tuning jobs:")
            pipeline.list_training_jobs()

            return 0

        else:
            parser.print_help()
            return 1

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
