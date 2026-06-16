import argparse
import sys
from typing import List, Optional

from src.cli.config import Command, SubCommand


class CLIRunner:
    """Запускает CLI на основе декларативной конфигурации."""

    def __init__(self, command: Command, command_module: str):
        """
        Args:
            command: Определение команды (Command)
            command_module: Модуль с командами (e.g., 'src.cli.commands')
        """
        self.command = command
        self.command_module = command_module
        self.parser = None

    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Запускает CLI приложение.

        Args:
            args: Аргументы командной строки (по умолчанию sys.argv[1:])

        Returns:
            Код выхода (0 = успех, 1 = ошибка)
        """
        self.parser = self._build_parser()

        if args is None:
            args = sys.argv[1:]

        # Если нет аргументов, показываем помощь
        if not args:
            self.parser.print_help()
            return 0

        parsed_args = self.parser.parse_args(args)

        # Проверяем что выбрана подкоманда
        if not hasattr(parsed_args, "handler"):
            self.parser.print_help()
            return 0

        try:
            return parsed_args.handler(**vars(parsed_args))
        except Exception as e:
            print(f"Error: {e}")
            return 1

    def _build_parser(self) -> argparse.ArgumentParser:
        """Строит argparse парсер на основе конфигурации."""
        parser = argparse.ArgumentParser(
            prog=self.command.name,
            description=self.command.help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        subparsers = parser.add_subparsers(dest="subcommand")

        for subcommand in self.command.subcommands:
            self._add_subcommand(subparsers, subcommand)

        return parser

    def _add_subcommand(self, subparsers, subcommand: SubCommand):
        """Добавляет подкоманду в парсер."""
        subparser = subparsers.add_parser(
            subcommand.name,
            help=subcommand.help,
            description=subcommand.description or subcommand.help,
        )

        # Добавляем аргументы
        for arg in subcommand.arguments:
            subparser.add_argument(
                arg.name,
                help=arg.help,
                type=self._get_type(arg.type),
                nargs="?" if not arg.required else None,
                default=arg.default,
                choices=arg.choices,
            )

        # Добавляем флаги
        for flag in subcommand.flags:
            flag_name = f"--{flag.name}".replace("_", "-")
            short_name = f"-{flag.short}" if flag.short else None

            if short_name:
                subparser.add_argument(
                    short_name,
                    flag_name,
                    help=flag.help,
                    action="store_true" if isinstance(flag.default, bool) else "store",
                    default=flag.default,
                    dest=flag.name.replace("-", "_"),
                )
            else:
                if isinstance(flag.default, bool):
                    subparser.add_argument(
                        flag_name,
                        help=flag.help,
                        action="store_true",
                        default=flag.default,
                        dest=flag.name.replace("-", "_"),
                    )
                else:
                    subparser.add_argument(
                        flag_name,
                        help=flag.help,
                        default=flag.default,
                        dest=flag.name.replace("-", "_"),
                    )

        # Устанавливаем handler
        subparser.set_defaults(
            handler=self._get_handler(subcommand.handler)
        )

    def _get_handler(self, handler_path: str):
        """Получает handler функцию по пути."""
        class_name, method_name = handler_path.split(".")
        module = __import__(self.command_module, fromlist=[class_name])
        handler_class = getattr(module, class_name)
        return getattr(handler_class, method_name)

    @staticmethod
    def _get_type(type_name: str):
        """Преобразует название типа в тип Python."""
        types = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }
        return types.get(type_name, str)
