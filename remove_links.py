# Copyright (c) 2021 YON
# This software is released under the MIT License, see LICENSE.

# 入力1 対象はてなブログ記事のURL
# 入力2 対象はてなブログ記事のHTML編集本文(クリップボードから取得)
# 処理 キーワードリンクが張られている記事内の全単語Xを、[]X[]という形に置換する
# 出力 置換後のHTML編集本文(クリップボードに格納される)

import re
import requests, pyperclip
from bs4 import BeautifulSoup

blog_url = input("キーワードリンクを除去したいはてなブログ記事のURLを入力し、Enterキーを押してください : ")
res = requests.get(blog_url)
soup = BeautifulSoup(res.text, 'html.parser')

# 記事サイトソースの本文(<div class="entry-content"> の内部)は、HTML編集で表示される内容とは異なる
_ = input("記事の｢HTML編集｣本文をコピーし、Enterキーを押してください")
blog_html = pyperclip.paste()
soup_html = BeautifulSoup(blog_html, 'html.parser')

# キーワードリンクが張られた単語一覧を取得し、辞書順に並べる
linked_keywords = sorted(list(set(url.get_text() for url in soup.find_all('a') if "http://d.hatena.ne.jp/keyword/" in str(url.get('href')))))

for lk in linked_keywords:
    for with_lk in soup_html.find_all(text=re.compile(".*" + lk + ".*")):
        s = with_lk.string
        if s[0] != "[" or s[-1] != "]": # Twitter埋め込みなどのコマンドを置換候補から除く
            with_lk.replace_with(s.replace("[]" + lk + "[]", lk).replace(lk, "[]" + lk + "[]")) # リンク付き単語を[]で囲む。2重付与しないよう既に囲まれたものを戻してから

pyperclip.copy(str(soup_html))
_ = input("リンク除去処理済のHTML本文がコピーされました。Enterキーを押して終了してください")