# src/cache.py
from pathlib import Path


class Cache:
    PARENT_PATH = Path(".").parent / ".cache" / "dict"

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
        return (path / f"{filename}.html").exists()

    @classmethod
    def read_cache(cls, filename: str) -> str:
        """
        read cache

        @param filename:
        @return:
        """
        path = cls.cache_path() / f"{filename}.html"
        html = path.read_text(encoding="utf-8")
        return html

    @classmethod
    def create_cache(cls, filename: str, html: str) -> None:
        path = cls.cache_path() / f"{filename}.html"
        path.write_text(data=html, encoding="utf-8")
