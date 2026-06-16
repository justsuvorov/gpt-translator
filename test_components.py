#!/usr/bin/env python3
"""
Simple tests для проверки компонентов.

Usage:
    python test_components.py
"""

import json
from pathlib import Path

from src.core import ConfigLoader, Logger
from src.training import TranslationDataValidator, TranslationDataHandler


def test_config_loader():
    """Тест загрузки конфигурации."""
    print("\n" + "=" * 60)
    print("TEST: Config Loader")
    print("=" * 60)

    try:
        loader = ConfigLoader()
        main_config = loader.get_main_config()
        training_config = loader.get_training_config()

        print("✓ Main config loaded")
        print(f"  - App: {main_config['app']['name']}")
        print(f"  - Model: {main_config['openai']['model']}")

        print("✓ Training config loaded")
        print(f"  - Min samples: {training_config['validation']['min_samples']}")
        print(f"  - Max samples: {training_config['validation']['max_samples']}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_data_validator():
    """Тест валидатора данных."""
    print("\n" + "=" * 60)
    print("TEST: Data Validator")
    print("=" * 60)

    try:
        loader = ConfigLoader()
        config = loader.get_training_config()
        validator = TranslationDataValidator(config)

        # Валидные данные
        valid_data = [
            {
                "messages": [
                    {"role": "system", "content": "You are a translator."},
                    {"role": "user", "content": "Привет"},
                ],
                "completion": " Hello",
            }
        ]

        is_valid, errors = validator.validate(valid_data)
        if is_valid:
            print("✓ Valid data passed validation")
        else:
            print(f"✗ Valid data failed: {errors}")
            return False

        # Невалидные данные - пустое completion
        invalid_data = [
            {
                "messages": [
                    {"role": "system", "content": "You are a translator."},
                    {"role": "user", "content": "Привет"},
                ],
                "completion": "",
            }
        ]

        is_valid, errors = validator.validate(invalid_data)
        if not is_valid:
            print("✓ Invalid data correctly rejected")
            print(f"  Errors: {errors[0]}")
        else:
            print("✗ Invalid data was not rejected")
            return False

        # Невалидные данные - отсутствие поля
        invalid_data = [
            {
                "messages": [
                    {"role": "system", "content": "You are a translator."},
                    {"role": "user", "content": "Привет"},
                ]
            }
        ]

        is_valid, errors = validator.validate(invalid_data)
        if not is_valid:
            print("✓ Missing completion correctly detected")
        else:
            print("✗ Missing field was not detected")
            return False

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_data_handler():
    """Тест обработчика данных."""
    print("\n" + "=" * 60)
    print("TEST: Data Handler")
    print("=" * 60)

    try:
        loader = ConfigLoader()
        config = loader.get_training_config()
        handler = TranslationDataHandler(config)

        # Проверка наличия примера файла
        example_file = "data/raw/example_translations.json"
        if not Path(example_file).exists():
            print(f"✗ Example file not found: {example_file}")
            return False

        print(f"✓ Example file found: {example_file}")

        # Загрузка и обработка
        output_file = "data/processed/test_data.jsonl"

        success = handler.process(example_file, output_file)

        if success:
            print(f"✓ Data processed successfully")
            print(f"  Output: {output_file}")

            # Проверка JSONL файла
            if Path(output_file).exists():
                with open(output_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    print(f"  Lines: {len(lines)}")

                print("✓ JSONL file created")
            else:
                print("✗ JSONL file not created")
                return False

            return True
        else:
            print("✗ Data processing failed")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Запуск тестов."""
    Logger.configure(log_level="WARNING")

    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   GPT Translator - Component Tests".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    results = {
        "Config Loader": test_config_loader(),
        "Data Validator": test_data_validator(),
        "Data Handler": test_data_handler(),
    }

    # Итоги
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
