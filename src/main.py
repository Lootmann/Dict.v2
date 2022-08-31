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

        print("create cache")

        if scraper.exists:
            Cache.create_cache(input_words, str(scraper))
            print(str(scraper)[:20])
        else:
            Cache.create_cache(input_words, str("not found"))
            print("not found")

        return

    print("use cache")
    cache_file = Cache.read_cache(input_words)
    print(cache_file[:20])


if __name__ == "__main__":
    main()
