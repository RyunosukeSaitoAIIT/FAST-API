# FAST-API

tree構造は以下の通り。
.
|-- main.py
 -- templates
    |-- login.html
    |-- profile.html
    -- next_page.html

1 directory, 4 files

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
