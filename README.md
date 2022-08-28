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

## Flow

だいたいこんな感じ

```python
# main.py
user_inputs = parsing_stdin()

if cache.exists(user_inputs):
    word_json = cache.find_cache(user_inputs)
    word_dict = util.json2dict(word_json)
    cli.prettier(word_json)
    return

weblio_url = "https://..." + user_inputs
html = api.fetch_web_page(weblio_url)
word_dict = scraping.scraping(html)
cache.create_cache(word_dict)
cli.prettier(word_dict)
```

## TODO

### api.py

- [x] Weblio から `html` を取得

### cache.py

- [ ] `html` をいい感じに整形したdict を `json` に出力

### cli.py

- [ ] `json` or `dict` をいい感じに出力 (stdout)

### main.py

- [ ] とりまとめ

### parsing.py

- [x] ユーザーの入力を `parsing` して `str` として出力 `api.py` に渡す

### scraping.py

- [ ] 取得したhtmlを `BeautifulSoup` で 要素抽出
  利用しやすい形に変換(`dict`?)
