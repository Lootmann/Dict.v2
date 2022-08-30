# src/main.py

from api import fetch_html_from_weblio
from cache import Cache
from parsing import parsing


def main():
    input_words = parsing()
    Cache.create_dir()

    if not Cache.find_path(input_words):
        html = fetch_html_from_weblio(input_words)
        Cache.create_cache(input_words, html)
        print("create cache")
        return

    html = Cache.read_cache(input_words)
    print("use cache")
    print(html)


if __name__ == "__main__":
    main()
