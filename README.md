# Dict.v2

English to Japanese Dictionary from Weblio API

CLI からさくっと使える簡易辞書の実装

よく使うアプリになるはずなので とにかく簡単に利用でき利用できるように実装する

## Usage

今の所こんな感じ

```bash
$ dict hello world

>>> 'hello world'
>>>
>>> [意味]
>>>  こんにちは、世界。プログラミングの初心者が必ず最初に入力する文章のこと。
>>> ...
```

## Env

- src/
  - api.py
    - fetch html from Weblio API
  - cache.py
    - cached html files or other jsonize html
  - main.py
    - entry point
  - parsing.py
    - parsing user inputs
  - scraping.py
    - scrape fetch html page

## TODO

### api.py

- [x] Weblio から `html` を取得

### cache.py

- [x] find cache
- [x] create cache
- [x] check where cache is existed
- [x] create cache dir(keep cached files)

### cli.py

- [ ] `json` or `dict` をいい感じに出力 (stdout)

### main.py

- [ ] とりまとめ

### parsing.py

- [x] ユーザーの入力を `parsing` して `str` として出力 `api.py`
      に渡す

### scraping.py

- [ ] 取得した html を `BeautifulSoup` で 要素抽出
- [ ] html -> scraping -> dict -> json(cache) でよいはず ?
