from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.schemas.user import UserCreate, PasswordResetRequest, PasswordReset
from app.models.user import User
from app.core.security import create_access_token, verify_password, hash_password
from app.core.config import settings
# from app.core.email import send_reset_email
from app.api.deps import get_db

router = APIRouter()

# ユーザー登録
@router.post("/register", summary="新規ユーザー登録")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="このメールアドレスは既に登録されています。")
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "ユーザー登録が完了しました。"}

# ログイン
@router.post("/login", summary="ログイン")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="メールアドレスまたはパスワードが間違っています。")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# パスワードリセットのリクエスト
@router.post("/password-reset/request", summary="パスワードリセットリクエスト")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="指定されたメールアドレスは存在しません。")
    reset_token = create_access_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    send_reset_email(request.email, reset_token)
    return {"message": "パスワード再設定用のメールを送信しました。"}

# パスワードリセット
@router.post("/password-reset/confirm", summary="パスワードリセット")
def confirm_password_reset(reset: PasswordReset, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == reset.token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="トークンが無効または期限切れです。")
    user.hashed_password = hash_password(reset.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return {"message": "パスワードが正常にリセットされました。"}