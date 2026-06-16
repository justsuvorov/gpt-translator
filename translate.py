#!/usr/bin/env python3
"""
Translator app entry point для использования переводчика.

Usage:
    python translate.py gui
    python translate.py gui --model ft-xxx123
    python translate.py text "Привет, мир!"
    python translate.py text "Hello" --model ft-xxx123
    python translate.py file input.txt --output output.txt
"""

import sys

from src.cli import TRANSLATION_COMMAND, CLIRunner


def main():
    """Запускает CLI для перевода."""
    runner = CLIRunner(TRANSLATION_COMMAND, "src.cli.commands")
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
