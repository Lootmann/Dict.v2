# tests/test_scraping.py
import unittest
from typing import Dict

from src.cache import Cache
from src.scraping import Scraper


class TestScraping(unittest.TestCase):
    soups: Dict[str, Scraper] = {}

    @classmethod
    def setUpClass(cls) -> None:
        """
        cls.soups is heavy objects, so run once for the whole class.
        """
        words = ["hello", "hoge", "take", "beautifulness", "kjsdhfkjds"]

        for word in words:
            if Cache.find_path(word):
                cls.soups[word] = Scraper(Cache.read_cache(word))
            else:
                raise ValueError("wow", word)

    def test_exists(self):
        tests = [
            ("hello", True),
            ("hoge", True),
            ("take", True),
            ("beautifulness", True),
            ("kjsdhfkjds", False),
        ]

        for word, boolean in tests:
            assert TestScraping.soups[word].exists is boolean

    def test_headword(self):
        tests = [
            ("hello", "hello"),
            ("hoge", "hoge"),
            ("take", "take"),
            ("beautifulness", "beautifulness"),
            ("kjsdhfkjds", ""),
        ]

        for word, headword in tests:
            if TestScraping.soups[word].exists:
                assert TestScraping.soups[word].get_headword() == headword

    def test_get_description(self):
        tests = [
            ("hello", "お(ー)い!、もし!、やあ!、よお!、こんにちは!、もしもし!、おや!、あら!"),
            ("hoge", "とくに意味もないときに使う変数名"),
            ("take", "(手などで)取る、(…を)取る、つかむ、(…を)抱く、抱き締める、(わな・えさなどで)捕らえる、捕縛する、捕虜にする、(…を)(…で)捕らえる、占領する"),
            ("beautifulness", "器量よし"),
            ("kjsdhfkjds", ""),
        ]

        for word, description in tests:
            if TestScraping.soups[word].exists:
                assert TestScraping.soups[word].get_description() == description
