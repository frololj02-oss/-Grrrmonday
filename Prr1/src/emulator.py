"""Модуль эмулятора командной строки ОС (Вариант №33, Этап 1)."""

import getpass
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


def handle_ls(args: list[str]) -> None:
    """Команда-заглушка ls: выводит свое имя и переданные аргументы."""
    print(f"ls {args}")


def handle_cd(args: list[str]) -> None:
    """Команда-заглушка cd: проверяет число аргументов и выводит их."""
    if len(args) > MAX_CD_ARGS:
        print("Ошибка: cd: слишком много аргументов")
        return
    print(f"cd {args}")


def execute_command(command: str, args: list[str]) -> bool:
    """Выполняет команду. Возвращает False при вызове exit, иначе True."""
    if command == "exit":
        if args:
            print("Ошибка: exit: неверные аргументы")
            return True
        return False
    if command == "ls":
        handle_ls(args)
    elif command == "cd":
        handle_cd(args)
    else:
        print(f"Ошибка: неизвестная команда '{command}'")
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
        is_running = execute_command(parts[0], parts[1:])


if __name__ == "__main__":
    run_repl()
    sys.exit(EXIT_SUCCESS)