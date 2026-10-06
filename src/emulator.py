"""Модуль эмулятора командной строки ОС (Вариант №33, Финал: Этап 5)."""

from __future__ import annotations

import argparse
import getpass
import os
import socket
import sys

from commands import (
    cmd_cd,
    cmd_clear,
    cmd_head,
    cmd_help,
    cmd_ls,
    cmd_mkdir,
)
from vfs import VFS

EXIT_SUCCESS = 0
MIN_PARTS_COUNT = 1


def get_prompt(vfs: VFS) -> str:
    """Формирует приглашение к вводу на основе реальных данных ОС."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    path_str = "~" if vfs.cwd == "/" else vfs.cwd
    return f"{username}@{hostname}:{path_str}$ "


def parse_input(user_input: str) -> list[str]:
    """Разделяет пользовательский ввод на команду и аргументы по пробелам."""
    return user_input.strip().split()


def handle_vfs_info(vfs: VFS, args: list[str]) -> bool:
    """Выводит имя загруженной VFS и SHA-256 хеш ее данных."""
    if args:
        print("Ошибка: vfs-info не принимает аргументов")
        return False
    print(f"VFS Name: {vfs.name}")
    print(f"SHA-256:  {vfs.sha256}")
    return True


def execute_command(vfs: VFS, command: str, args: list[str]) -> tuple[bool, bool]:
    """Выполняет команду. Возвращает кортеж (продолжать_работу, успех)."""
    if command == "exit":
        if args:
            print("Ошибка: exit: неверные аргументы")
            return True, False
        return False, True
    handlers = {
        "ls": lambda: cmd_ls(vfs, args),
        "cd": lambda: cmd_cd(vfs, args),
        "clear": lambda: cmd_clear(args),
        "head": lambda: cmd_head(vfs, args),
        "mkdir": lambda: cmd_mkdir(vfs, args),
        "help": lambda: cmd_help(args),
        "vfs-info": lambda: handle_vfs_info(vfs, args),
    }
    if command in handlers:
        return True, handlers[command]()
    print(f"Ошибка: неизвестная команда '{command}'")
    return True, False


def run_script(vfs: VFS, script_path: str) -> bool:
    """Выполняет стартовый скрипт до первой ошибки."""
    if not os.path.isfile(script_path):
        print(f"Ошибка: стартовый скрипт '{script_path}' не найден")
        return False
    with open(script_path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue
            print(f"{get_prompt(vfs)}{stripped}")
            parts = parse_input(stripped)
            keep_running, ok = execute_command(vfs, parts[0], parts[1:])
            if not ok:
                print("Ошибка исполнения стартового скрипта. Остановка.")
                return False
            if not keep_running:
                return False
    return True


def run_repl(vfs: VFS) -> None:
    """Запускает основной интерактивный цикл REPL эмулятора."""
    is_running = True
    while is_running:
        try:
            user_input = input(get_prompt(vfs))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        parts = parse_input(user_input)
        if len(parts) < MIN_PARTS_COUNT:
            continue
        is_running, _ = execute_command(vfs, parts[0], parts[1:])


def parse_cli_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки эмулятора."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", default="tests/vfs_deep.xml", help="Путь VFS")
    parser.add_argument("--script", default="", help="Стартовый скрипт")
    return parser.parse_args()


def main() -> None:
    """Точка входа: загружает VFS, запускает скрипт и интерактивный REPL."""
    args = parse_cli_args()
    print(f"[DEBUG] Путь к VFS: {args.vfs}")
    print(f"[DEBUG] Стартовый скрипт: {args.script}")
    vfs = VFS()
    if args.vfs:
        vfs.load_xml(args.vfs)
    if args.script:
        if not run_script(vfs, args.script):
            return
    run_repl(vfs)


if __name__ == "__main__":
    main()
    sys.exit(EXIT_SUCCESS)