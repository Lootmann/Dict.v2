# tests/test_parsing.py
from unittest.mock import patch

import pytest

from src.parsing import parsing


def test_parse():
    with patch("sys.argv", ["src/main.py", "hello"]):
        words = parsing()

        assert words == "hello"


def test_parse_multiple_word():
    with patch("sys.argv", ["src/main.py", "hello", "world"]):
        words = parsing()

        assert words == "hello world"


def test_parse_without_args(capsys):
    with patch("sys.argv", ["src/main.py"]):
        with pytest.raises(SystemExit):
            parsing()
