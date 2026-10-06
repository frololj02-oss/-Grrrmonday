"""Тесты для проверки парсера Этапа 1."""

from src.emulator import parse_input


def test_parse_input() -> None:
    """Проверяет корректность разделения строки по пробелам."""
    assert parse_input("ls -l /home") == ["ls", "-l", "/home"]