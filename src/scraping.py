# src/scraping.py
import unicodedata

from bs4 import BeautifulSoup as bs


class Scraper:
    """
    Scraping Manager
    """

    def __init__(self, html: str):
        """
        NOTE:
            必要な要素は id="main" 配下に一つを除いてすべて存在している
            ただ単語がWeblioに存在しているかどうかは id="anoOnnanoko" で確認する必要があり
            id="main" の範囲外に存在しているため こういった実装にしている

        @param html: fetched Weblio html
        """
        _soup = bs(html, "lxml")
        self._exists = _soup.find(id="anoOnnanoko")
        self._soup = _soup.find(id="main")

    @property
    def exists(self) -> bool:
        return self._exists is None

    def get_headword(self) -> str:
        """
        get headword class="midashigo"

        @return: str - headword
        """
        headword = self._soup.find(class_="midashigo")
        return unicodedata.normalize("NFKC", headword.get_text().strip())

    def get_description(self) -> str:
        """
        get word description
        <span> class="content-explanation ej"

        @return: str - description
        """
        description = self._soup.find(class_="content-explanation ej")
        return description.get_text().strip()

    def __str__(self) -> str:
        """NOTE: temporary method, never use it on product"""
        return self._soup.prettify()
