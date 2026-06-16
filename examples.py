#!/usr/bin/env python3
"""
Примеры использования API проекта.

Usage:
    python examples.py
"""

import logging

from src.core import ConfigLoader
from src.training import TranslationDataHandler, OpenAIModelTrainer, TrainingPipeline
from src.translator import GPTTranslator


def setup_logging():
    """Настраивает логирование."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )


# ============================================================================
# EXAMPLE 1: Валидация и подготовка данных
# ============================================================================
def example_prepare_data():
    """Пример: подготовка данных для обучения."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Prepare Training Data")
    print("=" * 70)

    config_loader = ConfigLoader()
    config = config_loader.get_training_config()

    handler = TranslationDataHandler(config)

    # Обработка JSON в JSONL формат
    success = handler.process(
        input_path="data/raw/example_translations.json",
        output_path="data/processed/training_data.jsonl",
    )

    if success:
        print("✓ Data prepared successfully")
        print("  - Validated samples")
        print("  - Converted to JSONL format")

        # Разбивка на train/validation
        train_path, val_path = handler.split_train_validation(
            "data/processed/training_data.jsonl",
            split_ratio=0.2,
        )

        print(f"✓ Data split:")
        print(f"  - Training: {train_path}")
        print(f"  - Validation: {val_path}")


# ============================================================================
# EXAMPLE 2: Использование переводчика (без fine-tuning)
# ============================================================================
def example_translate_basic():
    """Пример: использование базовой модели для перевода."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Translate with Base Model")
    print("=" * 70)

    config_loader = ConfigLoader()
    config = config_loader.get_main_config()

    translator = GPTTranslator(config)

    texts = [
        "Привет, мир!",
        "Как дела?",
        "Это очень красивый день.",
    ]

    for text in texts:
        print(f"\nRussian: {text}")
        try:
            result = translator.translate(text)
            print(f"English: {result}")
        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 3: Fine-tuning pipeline (requires API key)
# ============================================================================
def example_fine_tuning():
    """Пример: полный pipeline обучения модели."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Fine-tuning Pipeline (requires OPENAI_API_KEY)")
    print("=" * 70)

    config_loader = ConfigLoader()
    main_config = config_loader.get_main_config()
    training_config = config_loader.get_training_config()

    config = {**main_config, **training_config}

    pipeline = TrainingPipeline(config)

    print("\n1. Starting fine-tuning pipeline...")
    print("   Input: data/raw/example_translations.json")

    try:
        # Запуск обучения (без ожидания завершения для примера)
        job_id = pipeline.run(
            data_source="data/raw/example_translations.json",
            wait_for_completion=False,
        )

        print(f"\n✓ Fine-tuning started!")
        print(f"  Job ID: {job_id}")
        print(f"\nTo check status:")
        print(f"  python train.py --job-id {job_id}")
        print(f"\nTo wait for completion:")
        print(f"  python train.py --job-id {job_id} --wait")

    except Exception as e:
        print(f"✗ Error: {e}")
        print("Note: Requires valid OPENAI_API_KEY in .env")


# ============================================================================
# EXAMPLE 4: Проверка статуса обучения
# ============================================================================
def example_check_training_status():
    """Пример: проверка статуса обучения."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Check Training Status")
    print("=" * 70)

    config_loader = ConfigLoader()
    config = config_loader.get_main_config()
    config.update(ConfigLoader().get_training_config())

    trainer = OpenAIModelTrainer(config)

    print("\nTo check status of a training job:")
    print("  1. Get job ID from fine-tuning output (e.g., ft-abc123)")
    print("  2. Call trainer.get_status(job_id)")

    example_job_id = "ft-example123"
    print(f"\nExample:")
    print(f"  status = trainer.get_status('{example_job_id}')")
    print(f"  print(status['status'])  # 'succeeded', 'running', etc.")


# ============================================================================
# EXAMPLE 5: Использование обученной модели
# ============================================================================
def example_use_fine_tuned_model():
    """Пример: использование fine-tuned модели."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Use Fine-tuned Model")
    print("=" * 70)

    config_loader = ConfigLoader()
    config = config_loader.get_main_config()

    # Использование обученной модели
    fine_tuned_model_id = "ft-gpt-4o-mini-2024-07-18-xxx"

    translator = GPTTranslator(config, model_id=fine_tuned_model_id)

    print(f"\nUsing fine-tuned model: {fine_tuned_model_id}")
    print("\nTranslating with fine-tuned model:")
    print("  translator = GPTTranslator(config, model_id='ft-xxx')")
    print("  result = translator.translate('Привет!')")

    # Можно также изменить модель после создания
    translator.set_model("gpt-4o-mini")
    print("\nSwitching back to base model:")
    print("  translator.set_model('gpt-4o-mini')")


# ============================================================================
# EXAMPLE 6: Использование PyEdifice приложения
# ============================================================================
def example_gui_app():
    """Пример: запуск GUI приложения."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Launch GUI Application")
    print("=" * 70)

    print("\nTo launch GUI:")
    print("  from src.core import ConfigLoader")
    print("  from src.translator import GPTTranslator, TranslatorApp")
    print("")
    print("  config_loader = ConfigLoader()")
    print("  config = config_loader.get_main_config()")
    print("")
    print("  translator = GPTTranslator(config)")
    print("  app = TranslatorApp(translator, config)")
    print("  app.run()")
    print("")
    print("Or from command line:")
    print("  python translate.py --gui")
    print("  python translate.py --model ft-xxx123 --gui")


# ============================================================================
# EXAMPLE 7: Архитектура и классы
# ============================================================================
def example_architecture():
    """Пример: использование интерфейсов и классов."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Architecture & Interfaces")
    print("=" * 70)

    print("""
Core Components:

1. Configuration (src/core/config.py)
   - ConfigLoader: Загружает YAML конфиги с подстановкой env vars
   - Settings: Pydantic модель для переменных окружения

2. Interfaces (src/core/interfaces.py)
   - DataValidator: Интерфейс для валидации данных
   - DataProcessor: Интерфейс для обработки данных
   - ModelTrainer: Интерфейс для обучения моделей
   - Translator: Интерфейс для перевода текста

3. Training (src/training/)
   - TranslationDataValidator: Валидирует JSON для обучения
   - TranslationDataHandler: Конвертирует JSON в JSONL, делит на train/val
   - OpenAIModelTrainer: Управляет fine-tuning через OpenAI API
   - TrainingPipeline: Оркестрирует весь процесс обучения

4. Translation (src/translator/)
   - GPTTranslator: Использует OpenAI API для перевода
   - TranslatorApp: PyEdifice GUI приложение

Декларативная архитектура:
- Все параметры в YAML конфигах
- Классы реализуют интерфейсы
- Одна точка входа для обучения (train.py)
- Одна точка входа для приложения (translate.py)
    """)


# ============================================================================
# MAIN
# ============================================================================
def main():
    """Запуск примеров."""
    setup_logging()

    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "   GPT Translator - API Usage Examples".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    try:
        # Example 1: Prepare data
        example_prepare_data()

        # Example 2: Basic translation
        # example_translate_basic()  # Requires API key

        # Example 3: Fine-tuning
        # example_fine_tuning()  # Requires API key

        # Example 4: Check status
        example_check_training_status()

        # Example 5: Use fine-tuned model
        example_use_fine_tuned_model()

        # Example 6: GUI
        example_gui_app()

        # Example 7: Architecture
        example_architecture()

        print("\n" + "=" * 70)
        print("Examples completed!")
        print("=" * 70)
        print("\nFor more information:")
        print("  - Read README.md for full documentation")
        print("  - Read QUICKSTART.md for quick setup guide")
        print("  - Run test_components.py to verify installation")
        print("  - Run train.py --help for training options")
        print("  - Run translate.py --help for translation options")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
