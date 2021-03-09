# [][]スマブラ[]SP[] 要バグ修正
# スマブラとスマブラSPで両方ヒットしている
# 他の単語に内包されている単語を除く処理が必要


# 入力1 対象はてなブログ記事のURL
# 入力2 対象はてなブログ記事のHTML編集本文
# 処理 キーワードリンクが張られている記事内の全単語Xを、[]X[]という形に置換する
# 出力 置換後のHTML編集本文(クリップボードに格納される)

import requests, re, pyperclip
from bs4 import BeautifulSoup

blog_url = input("キーワードリンクを除去したい記事のURLを入力してください : ")

# 記事サイトソースの本文(<div class="entry-content"> の内部)は、HTML編集で表示される内容とは異なる
_ = input("記事のHTML編集本文を全てコピーした後、Enterキーを押してください")
blog_html = pyperclip.paste()

res = requests.get(blog_url)
soup = BeautifulSoup(res.text, 'html.parser')
soup_html = BeautifulSoup(blog_html, 'html.parser')

# キーワードリンクが張られた単語一覧を取得
linked_keywords = set(url.get_text() for url in soup.find_all('a') if "http://d.hatena.ne.jp/keyword/" in str(url.get('href')))

for lk in linked_keywords:
    for with_lk in soup_html.find_all(text=re.compile(".*" + lk + ".*")):
        s = with_lk.string
        if s[0] != "[" or s[-1] != "]": # Twitter埋め込みなどのコマンドを置換候補から除く
            with_lk.replace_with(s.replace(lk, "[]" + lk + "[]")) # リンク付きキーワードを[]で囲む

pyperclip.copy(str(soup_html))
print("キーワードリンク除去処理済のHTML本文がコピーされました")