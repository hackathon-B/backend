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

# 辞書の登録処理
@app.post("/api/dictionary/register")
def register_dictionary(user_id: int, title: str, content: str):
    if not user_id:
        return {"error": "ユーザーIDが必要です"}
    if not title:
        return {"error": "タイトルが必要です"}
    for dictionary in fake_dictionary_db.values():
        if dictionary["title"] == title:
            return {"error": "同じタイトルがすでに存在します"}
    if not content:
        return {"error": "メモの内容を入力してください"}
    new_id = max(fake_dictionary_db.keys(), default=0) + 1
    fake_dictionary_db[new_id] = {
        "user_id": user_id,
        "title": title,
        "content": content
    }
    return {
        "message": "辞書が正常に登録されました",
        "title": title
    }

# 辞書の検索処理    
@app.get("/api/dictionary/search")
def dictionary_search(title: str):
    search_results = [
        {"id": dictionary_id, "title": dictionary["title"]}
        for dictionary_id, dictionary in fake_dictionary_db.items()
        if title.lower() in dictionary["title"].lower()
    ]
    if not search_results:
        return {"message": "検索結果に該当するものがありませんでした"}
    return search_results  

# 更新用のリクエストデータ構造を定義
class UpdateDictionary(BaseModel):
    title: str
    content: str

# 編集・更新機能のエンドポイント
@app.put("/api/dictionary/{dictionary_id}/update")
def update_dictionary(dictionary_id: int, update_data: UpdateDictionary):
    if dictionary_id not in fake_dictionary_db:
        raise HTTPException(status_code=404, detail="指定された辞書が見つかりません")
    if update_data.title:
        fake_dictionary_db[dictionary_id]["title"] = update_data.title
    else:
        raise HTTPException(status_code=400, detail="タイトルを入力してください")
    if update_data.content:
        fake_dictionary_db[dictionary_id]["content"] = update_data.content
    else:
        raise HTTPException(status_code=400, detail="内容を入力してください")
    
    return {"message": "辞書が正常に更新されました", "updated_data": fake_dictionary_db[dictionary_id]}

