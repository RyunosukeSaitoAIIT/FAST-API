# FAST-API

多分以下でライブラリのインストールは大丈夫なはず。
<pre>
pip install fastapi starlette Jinja2 python-oauthlib pydantic starlette-session starlette-middleware-trustedhost
</pre>

tree構造は以下の通り。
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
・PasswordをSha256で暗号化  
・パスワードを3回間違えるとロックアウト  

### profile.html
メインページ相当  
・login.htmlよりセッションを引き継ぎ

### next_page.html
メインページからのページ遷移  
・profile.htmlよりセッションを引き継ぎ  
・戻るボタンでprofile.htmlページへ戻れる  


