from fastapi import APIRouter, Depends, HTTPExpection, Request
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


    )

    return {"google_auth_url" : google_auth_endpoint}

# Googleからコールバックを受ける
@router.get("/api/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = ""
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_url": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

