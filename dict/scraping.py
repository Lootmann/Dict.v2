# src/scraping.py
import unicodedata
from typing import Dict, List

from bs4 import BeautifulSoup as bs
from bs4 import NavigableString


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
        word_info.update(self.get_conjugation_table())
        word_info.update(self.get_examples())
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

        some (wrong) idioms have no description,
        at this time, return empty string "",

        @return: str - description
        """
        description = self._soup.find(class_="content-explanation ej")
        if description is not None:
            return description.get_text().strip()
        return ""

    def get_conjugation_table(self) -> Dict[str, Dict[str, str]]:
        """
        find conjugation table class='conjugateRowR'

        conjugate table has 2 types.

        1. a word has conjugateRowL and conjugateRowR
        2. a word has only conjugateRowR (RowL is empty)

        @return: dict - { part_of_speech: spell, ... }
        """
        tableL = self._soup.find_all("td", class_="conjugateRowL")
        tableR = self._soup.find_all("td", class_="conjugateRowR")

        # no conjugations
        if not tableL and not tableR:
            return {}

        conjugation_table = {}

        # only conjugateRowR
        if len(tableL) == 1:
            # and when the word has this pattern, tableR is one elem of list.
            for th, td in zip(tableR[0].find_all("th"), tableR[0].find_all("td")):
                conjugation_table[th.get_text().split()[0]] = td.get_text().split()[0]
            return {"conjugation_table": conjugation_table}

        else:
            # both RowL and RowR
            for a, span in zip(tableR[0].find_all("a"), tableR[0].find_all("span")):
                a_str = a.get_text().strip()
                span_str = span.get_text().strip()

                conjugation_table[span_str[1:-1]] = a_str

            conjugation_table["原形"] = self.get_headword()
            return {"conjugation_table": conjugation_table}

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
        articles = self._soup.find_all(class_="Kejje")

        if not articles:
            return {}

        d_part_of_speech: Dict[str, str | List[str]] = {}
        part_of_speech = ""
        lines = []

        for article in articles:
            for item in article.find_all("div", "level0"):
                # part of speech article header
                if pos := item.find(class_="KnenjSub"):
                    part_of_speech = pos.contents[1]
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

    def get_examples(self) -> Dict[str, List[str]]:
        """
        get examples
        Weblio have many shitty structures, examples are 3 pattern of html attributes

        pattern 1. 例文検索結果
            #hideDictPrsEGRKJ

        pattern 2. を含む例文一覧
            #hideDictPrsKENEJ
            #hideDictPrsJSTKG
            #hideDictPrsJMDCT

        pattern 3. に類似した例文
            #hideDictPrsWERBJ


        @return: Dict[]
        """
        examples = {
            "結果例文": [],  # pattern 1
            "含む例文": [],  # pattern 2
            "類似例文": [],  # pattern 3
        }

        result_exs = self._soup.select("#hideDictPrsEGRKJ > div.mainBlock.hlt_SNTCE > div.kijiWrp > div.kiji")

        contain_exs1 = self._soup.select("#hideDictPrsKENEJ > div.mainBlock.hlt_SNTCE > div.kijiWrp > div.kiji")
        contain_exs2 = self._soup.select("#hideDictPrsJSTKG > div.mainBlock.hlt_SNTCE > div.kijiWrp > div.kiji")
        contain_exs3 = self._soup.select("#hideDictPrsJMDCT > div.mainBlock.hlt_SNTCE > div.kijiWrp > div.kiji")

        similar_exs = self._soup.select("#hideDictPrsWERBJ > div.mainBlock.hlt_WERBJ > div.kijiWrp > div.kiji")

        if result_exs:
            kiji = result_exs[0]
            examples["結果例文"] += self._get_examples_by_result(kiji)

        if contain_exs1:
            kiji = contain_exs1[0]
            examples["含む例文"] += self._get_examples_by_result(kiji)

        if contain_exs2:
            kiji = contain_exs2[0]
            examples["含む例文"] += self._get_examples_by_result(kiji)

        if contain_exs3:
            kiji = contain_exs3[0]
            examples["含む例文"] += self._get_examples_by_result(kiji)

        if similar_exs:
            examples["類似例文"] += self._get_examples_by_similar(similar_exs[0])

        print()

        return examples

    def _get_examples_by_result(self, kiji) -> List[str]:
        result = []
        for qotC in kiji.find_all("div", class_="qotC"):
            words = []
            means = []

            for child in qotC:
                class_name = child["class"][0]
                if class_name == "qotCE":
                    for elem in child:
                        if elem.name == "b" and elem.get("class", None) is not None:
                            continue

                        if elem.name == "span":
                            continue

                        word = elem.get_text().strip()

                        if type(elem) == NavigableString and word == "":
                            continue

                        if word != "":
                            words.append(word)

                if class_name == "qotCJ":
                    for elem in child:
                        word = elem.get_text().strip()
                        if elem.name != "span" and word != "":
                            means.append(word)

            result.append(" ".join(words) + " : " + " ".join(means))

        return result

    def _get_examples_by_similar(self, kiji) -> List[str]:
        result = []

        japanese = kiji.find_all("div", class_="werbjJ")
        english = kiji.find_all("div", class_="werbjE")

        for jpa, eng in zip(japanese, english):
            words = []
            means = []

            for elem in jpa:
                if elem.name == "p":
                    words.append(elem.get_text())

            for elem in eng:
                if elem.name == "p":
                    means.append(elem.get_text())

            result.append("".join(words) + " : " + "".join(means))

        return result

    def __str__(self) -> str:
        """NOTE: temporary method, never use it on product"""
        return self._soup.prettify()
