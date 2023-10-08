from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from datetime import datetime, timedelta
import hashlib

app = FastAPI()

# セッションミドルウェアを追加
app.add_middleware(SessionMiddleware, secret_key="your-secret-key", max_age=1800)  # 1800秒（30分）有効
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

templates = Jinja2Templates(directory="templates")

# ダミーのユーザーデータベースを作成
fake_users_db = {
    "ryu": {
        "username": "ryu",
        "password_hash": hashlib.sha256("saito".encode()).hexdigest(),
        "login_attempts": 0,
        "locked": False,
        "lockout_time": None,
    }
}

# ロックアウトの閾値
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = timedelta(minutes=1)  # ロックアウト期間（1分）

# ログイン用のエンドポイント
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=400, detail="ユーザー名またはパスワードが正しくありません")

    if user["locked"]:
        # ロックアウト中の場合、ロックアウト期間をチェック
        if user["lockout_time"] + LOCKOUT_DURATION > datetime.now():
            raise HTTPException(status_code=401, detail="アカウントがロックアウトされました")
        else:
            # ロックアウト期間が過ぎた場合、ロックアウト情報をリセット
            user["locked"] = False
            user["lockout_time"] = None
            user["login_attempts"] = 0

    # パスワードをSHA-256ハッシュ化して比較
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] != password_hash:
        user["login_attempts"] += 1
        if user["login_attempts"] >= MAX_LOGIN_ATTEMPTS:
            # ログイン試行回数が閾値に達した場合、アカウントをロックアウト
            user["locked"] = True
            user["lockout_time"] = datetime.now()
        raise HTTPException(status_code=400, detail="ユーザー名またはパスワードが正しくありません")

    # ログイン成功時にセッションにユーザー情報を保存
    request.session["user"] = username
    user["login_attempts"] = 0  # ログイン成功時にロックアウトカウンタをリセット
    return RedirectResponse(url="/profile", status_code=303)  # リダイレクト時に GET メソッドを使用

# プロフィールページ
@app.get("/profile")
async def profile(request: Request):
    # セッションからユーザー情報を取得
    username = request.session.get("user")
    if username is None:
        raise HTTPException(status_code=401, detail="ログインしていません")

    return templates.TemplateResponse("profile.html", {"request": request, "username": username})

# 次ページ
@app.get("/next_page")
async def next_page(request: Request):
    # セッションからユーザー情報を取得
    username = request.session.get("user")
    if username is None:
        raise HTTPException(status_code=401, detail="ログインしていません")

    # "次へ" ページのテンプレートをレンダリング
    return templates.TemplateResponse("next_page.html", {"request": request, "username": username})

# ログアウト
@app.get("/logout")
async def logout(request: Request):
    # セッションからユーザー情報を削除してログアウト
    request.session.clear()
    return RedirectResponse(url="/login")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
