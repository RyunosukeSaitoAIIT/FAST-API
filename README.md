# FAST-API

## ライブラリのインストール
多分以下で大丈夫なはず。
<pre>
pip install fastapi starlette Jinja2 python-oauthlib pydantic starlette-session starlette-middleware-trustedhost
</pre>

## How to  
1. コマンドプロンプト(ターミナル)で以下を実行
<pre>
uvicorn main:app --reload
</pre>
2. ブラウザバーに「127.0.0.1:8000/login」を入力する

## tree構造  
以下の通り。
<pre>
.
|-- main.py
 -- templates
    |-- login.html
    |-- profile.html
    -- next_page.html

1 directory, 4 files
</pre>

### login.html
認証画面  
ユーザ名: ryu, パスワード: saito  
・PasswordをSha256で暗号化  
・パスワードを3回間違えるとロックアウト  

### profile.html
メインページ相当  
・login.htmlよりセッションを引き継ぎ

### next_page.html
メインページからのページ遷移  
・profile.htmlよりセッションを引き継ぎ  
・戻るボタンでprofile.htmlページへ戻れる  


