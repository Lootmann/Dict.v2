# src/cache.py
import json
from pathlib import Path


class Cache:
    """
    Cache Manager

    NOTE: PARENT_PATH should be '~/.cache/dict'
    """

    PARENT_PATH = Path("~/.cache/dict").expanduser()

    @classmethod
    def cache_path(cls) -> Path:
        """
        get cache_path

        TODO: Path(".").parent is temporary path while developing
            finally cache_path is '~/.cache/dict/'

        @return: pathlib.Path - cache path
        """
        cache_path = cls.PARENT_PATH.resolve()
        return cache_path

    @classmethod
    def create_dir(cls):
        """
        create cache dir

        .mkdir(parents=True) means when middle dir(/.cache/middle/middle/dict/) is not created,
            create all dirs automatically
        """
        cache_path = cls.cache_path()
        if not cache_path.exists():
            cache_path.mkdir(parents=True)

    @classmethod
    def find_path(cls, filename: str) -> bool:
        """
        find cache path

        @param filename: str
        @return: return True when cache file is found
        """
        path = cls.cache_path()
        return (path / f"{filename}.json").exists()

    @classmethod
    def read_cache(cls, filename: str) -> dict:
        """
        read cache

        @param filename:
        @return:
        """
        path = cls.cache_path() / f"{filename}.json"

        with path.open(encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def create_cache(cls, filename: str, parsed_html: dict) -> None:
        path = cls.cache_path() / f"{filename}.json"

        with path.open("w", encoding="utf-8") as f:
            json.dump(parsed_html, f, indent=2, ensure_ascii=False)
