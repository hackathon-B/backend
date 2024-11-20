from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.auth_utils import generate_token, verify_id_token
from app.core.security import create_access_token
from app.core.config import settings
from app.models.user import User
from app.api.deps import get_db
import requests

router = APIRouter(prefix="/auth/google", tags=["Google Authentication"])

# レスポンス用のモデルを定義
class GoogleLoginResponse(BaseModel):
    auth_url: str

class GoogleCallbackResponse(BaseModel):
    access_token: str
    token_type: str

# GoogleのOAuth2.0認証ページへのリダイレクトURLを作成
@router.get("/login", response_model=GoogleLoginResponse, summary="Google OAuth ログインページを取得")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=email profile"
    )
    return {"auth_url": google_auth_url}

# Googleからコールバックを受ける
@router.get("/callback", response_model=GoogleCallbackResponse, summary="Google OAuth コールバックを処理")
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

    if token_response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Google認証に失敗しました。 {token_response.text}")

    # Googleアカウント情報を取得
    access_token = token_response_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="アクセストークンが取得できませんでした。")

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(
        user_info_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if user_info_response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Googleユーザー情報の取得に失敗しました。 {user_info_response.text}")
    
    user_info = user_info_response.json()
    google_id = user_info.get("id")
    email = user_info.get("email")

    if not google_id or not email:
        raise HTTPException(status_code=sta.HTTP_400_BAD_REQUEST, detail="Googleアカウント情報に必要なデータが含まれていません。")

    # 既存ユーザーの確認または新規ユーザーを作成
    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        user = User(email=email, google_id=google_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    # アクセストークンの発行
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}