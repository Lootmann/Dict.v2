# src/scraping.py
from bs4 import BeautifulSoup as bs


def scraping(html: str) -> str:
    """
    scrape html to dict/json

    @param html:
    @return: str
    """
    soup = bs(html, "lxml")

    return soup.prettify()
