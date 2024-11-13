from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.core.auth_utils import create_access_token
from app.db.session import get_db
import requests

router = APIRouter()

# GoogleのOAuth2.0認証ページへのリダイレクトURLを作成
@router.get("/api/auth/google/login")
def google_login():

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=email%20profile"       
    )
    return {"suth_url": google_auth_url}

# Googleからコールバックを受ける
@router.get("/api/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    # Googleからアクセストークンを取得
    token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
    token_response_data = token_response.json()

    if "access_token" not in token_response_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, datail="Google認証に失敗しました。")

    # Googleアカウント情報を取得
    access_token = token_response_data["access_token"]
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    # 既存ユーザーの確認または新規ユーザーを作成
    user = db.query(User).filter(User.google_id == user_info["id"]).first()
    if not user:
        user = User(email=user_info["email"], google_id=user_info["id"])
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # アクセストークンの発行
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
