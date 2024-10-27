from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel, Emailstr
from typing import List, Optional
import hashlib
import jwt

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "Fucabo!!"}

fake_user_db = {}

# ユーザーモデルの定義
class User(BaseModel):
    email: Emailstr
    password: str
    name: Optional[str] = None

# JWT
SECRET_KEY = "yout_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# トークンをチェックする
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 新規登録ページの表示
@app.get("/api/auth/register")


# 新規登録処理
@app.post("/api/auth/register")
async def user_resister(user: User):
    # すでにメールアドレスが登録されているか確認
    if user.email in fake_user_db:
        raise HTTPException(status_code=400, datail="そのemailはすでに登録されています")

    #ユーザー情報を保存
    fake_user_db[user.email] = {
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "name": user.name
    }
    return {"message": "新規登録が完了しました"}

# ログインページの表示
@app.get("/api/auth/login")
async def login_page():
    return {"message": "ログインページ"}

# ログイン処理
@app.post("/api/auth/login")
async def user_login(email:Emailstr, password: str):
    user = fake_user_db.get(email)
    if not user or user['hash_password'] != hasf_password(password):
        raise HTTPException(status_code=400, datail="メールアドレスまたはパスワードが間違っています")
    
    # ログイン成功時の処理
    return {
        "message": "ログインしました"
        "access token": access_token,
        "token_type": bearer
        }

# ログアウト
@app.post("/api/auth/logout")
async def logout():
    return {"message": "ログアウトしました"}