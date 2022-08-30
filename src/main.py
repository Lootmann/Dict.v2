# src/main.py

from api import fetch_html_from_weblio
from cache import Cache
from parsing import parsing
from scraping import scraping


def main():
    input_words = parsing()
    Cache.create_dir()

    if not Cache.find_path(input_words):
        html = fetch_html_from_weblio(input_words)
        scraped = scraping(html)
        Cache.create_cache(input_words, scraped)
        print("create cache")
        print(scraped.split("\n")[:3])
        return

    scraped = Cache.read_cache(input_words)
    print("use cache")
    print(scraped.split("\n")[:3])


if __name__ == "__main__":
    main()
