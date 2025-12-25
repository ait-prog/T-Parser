"""Утилиты для работы с файлами и директориями"""
from pathlib import Path

def ensure_dirs():
    """Создает необходимые директории если их нет"""
    maps_dir = Path("temp_maps")
    maps_dir.mkdir(exist_ok=True)
    return maps_dir

