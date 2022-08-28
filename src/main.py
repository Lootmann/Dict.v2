# src/main.py

from api import fetch_html_from_weblio
from parsing import parsing


def main():
    input_words = parsing()
    html = fetch_html_from_weblio(input_words)
    print(html)


if __name__ == "__main__":
    main()
