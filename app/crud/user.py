from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from typing import Optional
from datetime import datetime

# 新規ユーザーの作成
def create_user(user: UserCreate, db: Session) -> User:
    hashed_password = hashed_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー認証
def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# emailによるユーザー検索
def get_user_by_email(db: Session, email: str) -> Optional[User]:  # 引数の順序を変更
    return db.query(User).filter(User.email == email).first()

# リセットトークンによるユーザー検索
def get_user_by_reset_token(token: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.reset_token == token).first()

# パスワード更新
def update_password(user: User, new_password: str, db: Session) -> User:
    user.hashed_password = hashed_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    db.refresh(user)
    return user