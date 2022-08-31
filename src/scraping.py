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
            self._soup で必要不可欠な要素だけを取得
            そうすると 'self._exists' で anoOnnanoko が取得できなくなるため
            やむなくこういった実装にしている

        FIXME:
            exists() を scraping の前処理で実施して False だったら
            以降の処理を全部省くというのもあり というかそっちのほうがよさそう
            すべての関数に self._exists を書いていくのは明らかに実装がおかしい

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

        @return: str
        """
        if not self.exists:
            return ""

        headword = self._soup.find(class_="midashigo")
        return unicodedata.normalize("NFKC", headword.get_text().strip())

    def get_description(self) -> str:
        if not self.exists:
            return ""

        description = self._soup.find(class_="content-explanation ej")
        return description.get_text().strip()

    def __str__(self) -> str:
        """NOTE: temporary method, never use it on product"""
        return self._soup.prettify()
