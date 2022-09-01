# tests/test_cache.py
from pathlib import Path

from src.cache import Cache

PATH = Path("~").expanduser() / ".cache" / "dict"


def test_cache_path():
    cache_path = Cache.cache_path()
    assert str(cache_path) == str(PATH.resolve())
