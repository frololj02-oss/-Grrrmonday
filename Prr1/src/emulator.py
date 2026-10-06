"""Модуль эмулятора командной строки ОС (Вариант №33, Этап 2)."""

from __future__ import annotations

import argparse
import getpass
import os
import socket
import sys

EXIT_SUCCESS = 0
MIN_PARTS_COUNT = 1
MAX_CD_ARGS = 1


def get_prompt() -> str:
    """Формирует приглашение к вводу на основе реальных данных ОС."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"{username}@{hostname}:~$ "


def parse_input(user_input: str) -> list[str]:
    """Разделяет пользовательский ввод на команду и аргументы по пробелам."""
    return user_input.strip().split()


def handle_ls(args: list[str]) -> bool:
    """Команда-заглушка ls: выводит свое имя и переданные аргументы."""
    print(f"ls {args}")
    return True


def handle_cd(args: list[str]) -> bool:
    """Команда-заглушка cd: проверяет число аргументов и выводит их."""
    if len(args) > MAX_CD_ARGS:
        print("Ошибка: cd: слишком много аргументов")
        return False
    print(f"cd {args}")
    return True


def execute_command(command: str, args: list[str]) -> tuple[bool, bool]:
    """Выполняет команду. Возвращает кортеж (продолжать_работу, успех)."""
    if command == "exit":
        if args:
            print("Ошибка: exit: неверные аргументы")
            return True, False
        return False, True
    if command == "ls":
        return True, handle_ls(args)
    if command == "cd":
        return True, handle_cd(args)
    print(f"Ошибка: неизвестная команда '{command}'")
    return True, False


def run_script(script_path: str) -> bool:
    """Выполняет стартовый скрипт до первой ошибки."""
    if not os.path.isfile(script_path):
        print(f"Ошибка: стартовый скрипт '{script_path}' не найден")
        return False
    with open(script_path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue
            print(f"{get_prompt()}{stripped}")
            parts = parse_input(stripped)
            keep_running, ok = execute_command(parts[0], parts[1:])
            if not ok:
                print("Ошибка исполнения стартового скрипта. Остановка.")
                return False
            if not keep_running:
                return False
    return True


def run_repl() -> None:
    """Запускает основной интерактивный цикл REPL эмулятора."""
    is_running = True
    while is_running:
        try:
            user_input = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print()
            break
        parts = parse_input(user_input)
        if len(parts) < MIN_PARTS_COUNT:
            continue
        is_running, _ = execute_command(parts[0], parts[1:])


def parse_cli_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки эмулятора."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", default="vfs.xml", help="Путь к VFS")
    parser.add_argument("--script", default="", help="Стартовый скрипт")
    return parser.parse_args()


def main() -> None:
    """Точка входа: выводит конфигурацию, запускает скрипт и REPL."""
    args = parse_cli_args()
    print(f"[DEBUG] Путь к VFS: {args.vfs}")
    print(f"[DEBUG] Стартовый скрипт: {args.script}")
    if args.script:
        if not run_script(args.script):
            return
    run_repl()


if __name__ == "__main__":
    main()
    sys.exit(EXIT_SUCCESS)