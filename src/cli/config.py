"""Декларативная конфигурация CLI команд."""

from typing import Any, Callable, Dict, List, Optional


class Argument:
    """Определение аргумента CLI."""

    def __init__(
        self,
        name: str,
        help: str,
        type: str = "str",
        required: bool = False,
        default: Optional[Any] = None,
        choices: Optional[List[str]] = None,
    ):
        self.name = name
        self.help = help
        self.type = type
        self.required = required
        self.default = default
        self.choices = choices


class Flag:
    """Определение флага CLI."""

    def __init__(
        self,
        name: str,
        help: str,
        short: Optional[str] = None,
        default: bool = False,
    ):
        self.name = name
        self.help = help
        self.short = short
        self.default = default


class SubCommand:
    """Определение подкоманды CLI."""

    def __init__(
        self,
        name: str,
        handler: Callable,
        help: str,
        description: str = "",
        arguments: Optional[List[Argument]] = None,
        flags: Optional[List[Flag]] = None,
    ):
        self.name = name
        self.handler = handler
        self.help = help
        self.description = description
        self.arguments = arguments or []
        self.flags = flags or []


class Command:
    """Определение команды CLI."""

    def __init__(
        self,
        name: str,
        help: str,
        subcommands: Optional[List[SubCommand]] = None,
        arguments: Optional[List[Argument]] = None,
        flags: Optional[List[Flag]] = None,
    ):
        self.name = name
        self.help = help
        self.subcommands = subcommands or []
        self.arguments = arguments or []
        self.flags = flags or []


# ============================================================================
# TRAINING COMMAND
# ============================================================================

TRAINING_COMMAND = Command(
    name="train",
    help="Fine-tune GPT model for translations",
    subcommands=[
        SubCommand(
            name="start",
            handler="TrainingCommands.start_training",
            help="Start training with data",
            description="Start training with JSON file containing translation pairs",
            arguments=[
                Argument(
                    name="data",
                    help="Path to JSON file with training data",
                    required=True,
                ),
            ],
            flags=[
                Flag(
                    name="wait",
                    help="Wait for training to complete",
                    short="w",
                ),
                Flag(
                    name="log-level",
                    help="Logging level (DEBUG, INFO, WARNING, ERROR)",
                    default="INFO",
                ),
            ],
        ),
        SubCommand(
            name="status",
            handler="TrainingCommands.check_status",
            help="Check status of training job",
            arguments=[
                Argument(
                    name="job-id",
                    help="Fine-tuning job ID",
                    required=True,
                ),
            ],
            flags=[
                Flag(
                    name="log-level",
                    help="Logging level",
                    default="INFO",
                ),
            ],
        ),
        SubCommand(
            name="list",
            handler="TrainingCommands.list_jobs",
            help="List all fine-tuning jobs",
            flags=[
                Flag(
                    name="log-level",
                    help="Logging level",
                    default="INFO",
                ),
            ],
        ),
    ],
)


# ============================================================================
# TRANSLATION COMMAND
# ============================================================================

TRANSLATION_COMMAND = Command(
    name="translate",
    help="Translate text using fine-tuned GPT model",
    subcommands=[
        SubCommand(
            name="gui",
            handler="TranslationCommands.launch_gui",
            help="Launch PyEdifice GUI application",
            flags=[
                Flag(
                    name="model",
                    help="Fine-tuned model ID to use",
                ),
                Flag(
                    name="log-level",
                    help="Logging level",
                    default="INFO",
                ),
            ],
        ),
        SubCommand(
            name="text",
            handler="TranslationCommands.translate_text",
            help="Translate single text",
            arguments=[
                Argument(
                    name="text",
                    help="Text to translate",
                    required=True,
                ),
            ],
            flags=[
                Flag(
                    name="model",
                    help="Model ID to use",
                ),
                Flag(
                    name="output",
                    help="Save output to file",
                ),
                Flag(
                    name="log-level",
                    help="Logging level",
                    default="INFO",
                ),
            ],
        ),
        SubCommand(
            name="file",
            handler="TranslationCommands.translate_file",
            help="Translate file",
            arguments=[
                Argument(
                    name="file",
                    help="File path to translate",
                    required=True,
                ),
            ],
            flags=[
                Flag(
                    name="model",
                    help="Model ID to use",
                ),
                Flag(
                    name="output",
                    help="Save output to file",
                ),
                Flag(
                    name="log-level",
                    help="Logging level",
                    default="INFO",
                ),
            ],
        ),
    ],
)
