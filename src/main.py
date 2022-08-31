# src/main.py
from api import fetch_html_from_weblio
from cache import Cache
from parsing import parsing
from scraping import Scraper


def main():
    input_words = parsing()
    Cache.create_dir()

    if not Cache.find_path(input_words):
        html = fetch_html_from_weblio(input_words)
        scraper = Scraper(html=html)
        Cache.create_cache(input_words, str(scraper))
        print("create cache")
        print(str(scraper)[:20])
        return

    print("use cache")
    cache_file = Cache.read_cache(input_words)

    scraper = Scraper(html=cache_file)
    if not scraper.exists:
        print(f"{input_words} not found :^)")
        return

    print(scraper.get_headword())


if __name__ == "__main__":
    main()
