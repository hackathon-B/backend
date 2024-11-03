from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import requests
from app.core.security import create_access_token
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

# Google認証リクエストを開始
@router.get("/api/auth/google/login")
def google_login():

    # Google OAuthのエンドポイント
    google_auth_endpoint = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        "&scope=openid%20email%20profile"
    ).format(
        client_id=settings.GOOGLE_CLIENT_ID,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )
    return {"google_auth_url" : google_auth_endpoint}

# Googleからコールバックを受ける
@router.get("/api/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    # Googleからアクセストークンを取得
    token_response = requests.post(token_url, data=token_data)
    if not token_response.ok:
        raise HTTPException(status_code=400, detail="Googleトークンの取得に失敗しました")
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # Google APIからユーザー情報を取得
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": access_token}
    )
    if not user_info_response.ok:
        raise HTTPException(status_code=400, datail="Googleからユーザー情報を取得できませんでした")
    user_info = user_info_response.json()

    # データベース内にユーザーが存在するか確認
    email = user_info.get("email")
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        # ユーザーが存在しない場合、新規作成する処理
        new_user = create_user(db, user_info)
        db_user = new_user

    # JWTトークンを生成して返す
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
