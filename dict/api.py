# dict/api.py

import time

import requests


def fetch_html_from_weblio(words: str) -> str:
    time.sleep(1)

    url = "https://ejje.weblio.jp/content/{}".format(words)

    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.Timeout as e:
        raise SystemExit(e)
    except requests.exceptions.TooManyRedirects as e:
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
