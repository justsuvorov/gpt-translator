#!/usr/bin/env python3
"""
Fine-tuning entry point с composition pattern архитектурой.

Usage:
    python train.py start --data data/raw/example_translations.json
    python train.py start --data data/raw/my_translations.json --wait
    python train.py status --job-id ft-abcd1234
    python train.py list
"""

import sys

from src.cli import TRAINING_COMMAND, CLIRunner


def main() -> int:
    """Запускает CLI для обучения."""
    runner = CLIRunner(TRAINING_COMMAND, "src.cli.commands")
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
