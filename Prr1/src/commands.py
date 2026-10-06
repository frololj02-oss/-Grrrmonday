"""Модуль реализации команд оболочки ОС (Вариант №33, Этапы 4 и 5)."""

from __future__ import annotations

from vfs import VFS, VFSNode

DEFAULT_HEAD_LINES = 10
MAX_ARGS_SINGLE = 1
CLEAR_LINES_COUNT = 30


def cmd_ls(vfs: VFS, args: list[str]) -> bool:
    """Выводит список файлов и папок в указанной директории VFS."""
    if len(args) > MAX_ARGS_SINGLE:
        print("Ошибка: ls: слишком много аргументов")
        return False
    target = args[0] if args else vfs.cwd
    node = vfs.get_node(target)
    if node is None:
        print(f"Ошибка: ls: '{target}': нет такого файла или каталога")
        return False
    if not node.is_dir:
        print(node.name)
        return True
    items = sorted(node.children.keys())
    print("  ".join(items))
    return True


def cmd_cd(vfs: VFS, args: list[str]) -> bool:
    """Изменяет текущую рабочую директорию в VFS."""
    if len(args) > MAX_ARGS_SINGLE:
        print("Ошибка: cd: слишком много аргументов")
        return False
    target = args[0] if args else "/"
    node = vfs.get_node(target)
    if node is None:
        print(f"Ошибка: cd: '{target}': нет такого каталога")
        return False
    if not node.is_dir:
        print(f"Ошибка: cd: '{target}': не является каталогом")
        return False
    vfs.cwd = vfs.resolve_path(target)
    return True


def cmd_clear(args: list[str]) -> bool:
    """Очищает экран консоли."""
    if args:
        print("Ошибка: clear: не принимает аргументов")
        return False
    print("\n" * CLEAR_LINES_COUNT)
    return True


def cmd_head(vfs: VFS, args: list[str]) -> bool:
    """Выводит первые строки текстового файла из VFS."""
    if not args:
        print("Ошибка: head: укажите имя файла")
        return False
    count = DEFAULT_HEAD_LINES
    file_arg = args[0]
    if args[0] == "-n":
        if len(args) < 3 or not args[1].isdigit():
            print("Ошибка: head: неверный формат опции -n")
            return False
        count = int(args[1])
        file_arg = args[2]
    node = vfs.get_node(file_arg)
    if node is None or node.is_dir:
        print(f"Ошибка: head: невозможно открыть '{file_arg}'")
        return False
    lines = node.content.splitlines()[:count]
    for line in lines:
        print(line)
    return True


def cmd_mkdir(vfs: VFS, args: list[str]) -> bool:
    """Создает новую директорию в памяти VFS."""
    if len(args) != MAX_ARGS_SINGLE:
        print("Ошибка: mkdir: укажите ровно одно имя директории")
        return False
    abs_path = vfs.resolve_path(args[0])
    if vfs.get_node(abs_path) is not None:
        print(f"Ошибка: mkdir: '{args[0]}' уже существует")
        return False
    parent_path = "/" + "/".join(abs_path.strip("/").split("/")[:-1])
    dir_name = abs_path.strip("/").split("/")[-1]
    parent = vfs.get_node(parent_path)
    if parent is None or not parent.is_dir:
        print(f"Ошибка: mkdir: родительский каталог не найден")
        return False
    parent.children[dir_name] = VFSNode(dir_name, True)
    return True


def cmd_help(args: list[str]) -> bool:
    """Выводит справочную информацию обо всех поддерживаемых командах."""
    if args:
        print("Ошибка: help: не принимает аргументов")
        return False
    help_lines = [
        "Доступные команды эмулятора (Вариант №33):",
        "  ls [путь]         - Вывод содержимого каталога VFS",
        "  cd [путь]         - Смена текущего каталога VFS",
        "  head [-n N] файл  - Вывод первых строк файла",
        "  clear             - Очистка экрана терминала",
        "  mkdir <имя>       - Создание нового каталога в памяти VFS",
        "  vfs-info          - Вывод имени VFS и хеша SHA-256",
        "  help              - Вывод этой справки",
        "  exit              - Выход из эмулятора",
    ]
    print("\n".join(help_lines))
    return True