"""Модуль виртуальной файловой системы (VFS) в памяти на базе XML."""

from __future__ import annotations

import base64
import hashlib
import os
import xml.etree.ElementTree as ET


class VFSNode:
    """Узел виртуальной файловой системы (папка или файл)."""

    def __init__(self, name: str, is_dir: bool, content: str = "") -> None:
        """Инициализирует узел VFS."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children: dict[str, VFSNode] = {}


class VFS:
    """Класс управления виртуальной файловой системой в оперативной памяти."""

    def __init__(self) -> None:
        """Инициализирует пустую VFS в памяти."""
        self.name = "default_vfs"
        self.sha256 = "0" * 64
        self.root = VFSNode("/", True)
        self.cwd = "/"

    def load_xml(self, path: str) -> bool:
        """Загружает структуру VFS из XML-файла и вычисляет SHA-256."""
        if not os.path.isfile(path):
            print(f"Ошибка: файл VFS '{path}' не найден")
            return False
        try:
            with open(path, "rb") as file:
                raw_data = file.read()
            self.sha256 = hashlib.sha256(raw_data).hexdigest()
            tree = ET.fromstring(raw_data.decode("utf-8"))
            self.name = tree.attrib.get("name", os.path.basename(path))
            self.root = VFSNode("/", True)
            self._parse_element(tree, self.root)
            self.cwd = "/"
            return True
        except Exception as err:
            print(f"Ошибка загрузки XML VFS: {err}")
            return False

    def _parse_element(self, elem: ET.Element, parent: VFSNode) -> None:
        """Рекурсивно разбирает XML-элементы и строит дерево в памяти."""
        for child in elem:
            name = child.attrib.get("name", "unnamed")
            if child.tag == "dir":
                dir_node = VFSNode(name, True)
                parent.children[name] = dir_node
                self._parse_element(child, dir_node)
            elif child.tag == "file":
                raw_b64 = (child.text or "").strip()
                decoded = base64.b64decode(raw_b64).decode(
                    "utf-8", errors="replace"
                )
                parent.children[name] = VFSNode(name, False, decoded)

    def resolve_path(self, path: str) -> str:
        """Преобразует относительный путь в абсолютный внутри VFS."""
        if not path.startswith("/"):
            path = self.cwd.rstrip("/") + "/" + path
        parts: list[str] = []
        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        return "/" + "/".join(parts)

    def get_node(self, path: str) -> VFSNode | None:
        """Возвращает узел VFS по указанному пути или None."""
        abs_path = self.resolve_path(path)
        if abs_path == "/":
            return self.root
        curr = self.root
        for part in abs_path.strip("/").split("/"):
            if not curr.is_dir or part not in curr.children:
                return None
            curr = curr.children[part]
        return curr