import json
import os
from typing import Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_DIR = os.path.abspath(DATA_DIR)

def _path(filename: str) -> str:
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)


def read_json(filename: str) -> Any:
    path = _path(filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []


def write_json(filename: str, data: Any) -> None:
    path = _path(filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def find_by_key(filename: str, key: str, value):
    items = read_json(filename)
    for it in items:
        if it.get(key) == value:
            return it
    return None


def update_item(filename: str, key: str, value, new_item: dict) -> bool:
    items = read_json(filename)
    for i, it in enumerate(items):
        if it.get(key) == value:
            items[i] = new_item
            write_json(filename, items)
            return True
    return False


def delete_item(filename: str, key: str, value) -> bool:
    items = read_json(filename)
    new = [it for it in items if it.get(key) != value]
    if len(new) == len(items):
        return False
    write_json(filename, new)
    return True

def append_item(filename: str, item: dict) -> None:
    items = read_json(filename)
    items.append(item)
    write_json(filename, items)


