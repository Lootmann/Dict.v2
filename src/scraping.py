# src/scraping.py
import unicodedata
from typing import Dict, List

from bs4 import BeautifulSoup as bs


class Scraper:
    """
    Scraping Manager
    """

    def __init__(self, html: str):
        """
        NOTE:
            必要な要素は id="main" 配下に一つを除いてすべて存在している
            html の容量がすごく多いのでなるべく軽くするために id="main" のみを取得している
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

    def construct(self) -> Dict:
        word_info: Dict = {
            "headword": self.get_headword(),
            "description": self.get_description(),
        }
        word_info.update(self.get_part_of_speech())

        return word_info

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

    def get_part_of_speech(self) -> Dict[str, List[str]]:
        """
        get part of speeches
        all word infos have 'level0', level0 is under class_="Kejje" div

        Kejje
            level0:(one chunk)
                KnenjSub
            level0:
                lvlNH: number of meaning
                lvlB: meaning
            level0:
                lvlNH: number of meaning
                lvlB: meaning

            level0:
                KnenjSub(one chunk)
            table.KejjeYr
                Example

        NOTE: NEED REFACTORING :^)
        @return: Dict[str, str | List[str]]
        """
        article = self._soup.find(class_="Kejje")

        if not article:
            return {}

        d_part_of_speech: Dict[str : str | List[str]] = {}
        part_of_speech = ""
        lines = []

        for item in article.find_all("div", "level0"):
            # part of speech article header
            if pos := item.find(class_="KnenjSub"):
                part_of_speech = pos.contents[2].get_text().strip()
                d_part_of_speech[part_of_speech] = []

            if pos := item.find(class_="lvlNH"):
                for elem in pos:
                    number = elem.get_text().strip()
                    if number:
                        lines.append(elem.get_text().strip() + ". ")
                    else:
                        lines.append("   ")

            if pos := item.find(class_="lvlB"):
                for elem in pos:
                    lines.append(elem.get_text().strip())

                d_part_of_speech[part_of_speech].append("".join(lines))
                lines = []

            p = item.select_one("p")
            div = item.select_one("div")
            b = item.select_one("b")

            # when 'item' has 'no' div, this means 'item' has one meaning
            # - level0
            #   - a
            #   - a
            #   - ...
            if p is None and div is None and b is None:
                line = []
                for elem in item:
                    line.append(elem.get_text().strip())
                d_part_of_speech[part_of_speech].append("".join(line))

        # add last line
        if len(lines) != 0:
            d_part_of_speech[part_of_speech].append("".join(lines))

        return d_part_of_speech

    def __str__(self) -> str:
        """NOTE: temporary method, never use it on product"""
        return self._soup.prettify()
