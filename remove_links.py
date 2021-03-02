# 入力1 対象はてなブログ記事のURL
# 入力2 対象はてなブログ記事のHTML編集本文(クリップボードにコピーしておく)
# 処理 キーワードリンクが張られている記事内の全単語Xを、[]X[]という形に置換する
# 出力 置換後のHTML編集本文(クリップボードに格納される)

import requests, re, pyperclip
from bs4 import BeautifulSoup

blog_url = 'https://yon4.hatenablog.com/entry/2021/01/30/041707' # はてなブログ記事のURL

# はてなブログ記事の｢HTML編集｣本文
# 記事ソースの本文(<div class="entry-content"> の内部)は、HTML編集で表示される内容とは異なることに注意
blog_html = pyperclip.paste()
print("クリップボードのHTML本文を取得しました")

res = requests.get(blog_url)
soup = BeautifulSoup(res.text, 'html.parser')
soup_html = BeautifulSoup(blog_html, 'html.parser')
print("指定されたURLの記事にアクセスしました")

# 下線リンクが張られた単語一覧を取得
linked_keywords = set(url.get_text() for url in soup.find_all('a') if "http://d.hatena.ne.jp/keyword/" in str(url.get('href')))

for lk in linked_keywords:
    for with_lk in soup_html.find_all(text=re.compile(".*" + lk + ".*")):
        s = with_lk.string
        if s[0] != "[" or s[-1] != "]": # Twitter埋め込みなどのコマンドを置換候補から除く
            replace_text = s.replace(lk, "[]" + lk + "[]")
            with_lk.replace_with(replace_text)

pyperclip.copy(str(soup_html))
print("キーワードリンク除去処理したHTML本文がクリップボードにコピーされました")