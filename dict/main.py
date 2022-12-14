# dict/main.py
from dict.api import fetch_html_from_weblio
from dict.cache import Cache
from dict.cli import CLI
from dict.parsing import parsing
from dict.scraping import Scraper


def main():
    input_words = parsing()
    Cache.create_dir()

    if not Cache.find_path(input_words):
        html = fetch_html_from_weblio(input_words)
        scraper = Scraper(html=html)

        CLI.title("create cache :D")

        if scraper.exists:
            Cache.create_cache(input_words, scraper.construct())
        else:
            Cache.create_cache(input_words, {"NotFound": ":^)"})
        CLI.print(Cache.read_cache(input_words))
    else:
        CLI.title("use cache :P")
        CLI.print(Cache.read_cache(input_words))


if __name__ == "__main__":
    main()
