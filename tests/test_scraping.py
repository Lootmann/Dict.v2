# tests/test_scraping.py
import unittest
from pathlib import Path
from typing import Dict

from src.scraping import Scraper


class TestScraping(unittest.TestCase):
    soups: Dict[str, Scraper] = {}

    @classmethod
    def setUpClass(cls) -> None:
        """
        cls.soups is heavy objects, so run once for the whole class.

        test cache file are on
            ~/.cache/dict/<word>.html
        """
        words = ["hello", "hoge", "take", "beautifulness", "set", "kjsdhfkjds"]

        for word in words:
            path = (Path(".") / ".cache" / "dict").expanduser()
            filepath = path / f"{word}.html"

            if filepath.exists():
                cls.soups[word] = Scraper(filepath.read_text())
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

    def test_get_part_of_speech(self):
        """
        NOTE: I don't know how to test get_part_of_speech
        """
        tests = [
            # ("hello", {"word": []}),
            # ("take", {"word": []}),
            ("hoge", {}),
            ("beautifulness", {}),
            ("kjsdhfkjds", "hige"),
        ]

        for word, part_of_speech in tests:
            if TestScraping.soups[word].exists:
                assert TestScraping.soups[word].get_part_of_speech() == part_of_speech

    def test_construct(self):
        """
        NOTE: HOW :D ?
        """
        tests = [
            "hello",
            # "take",
            "hoge",
            "beautifulness",
        ]

        for word in tests:
            if TestScraping.soups[word].exists:
                TestScraping.soups[word].construct()

    def test_get_conjugation_table(self):
        tests = [
            ("hello", {}),
            ("take", {"原形": "take", "現在分詞": "taking", "過去形": "took", "過去分詞": "taken", "三人称単数現在": "takes"}),
            ("set", {"原形": "set", "現在分詞": "setting", "過去形": "set", "過去分詞": "set", "三人称単数現在": "sets"}),
        ]

        for word, table in tests:
            if TestScraping.soups[word].exists:
                assert TestScraping.soups[word].get_conjugation_table() == table
