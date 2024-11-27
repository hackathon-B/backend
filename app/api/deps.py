from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.user import User
from app.crud.user import get_user_by_email

# FastAPIの標準HTTPBearerを使用
security = HTTPBearer()

# Bearerトークンを抽出する依存関数
def get_bearer_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    return credentials.credentials

# トークンからカレントユーザーを取得する依存関数
def get_current_user(
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db),    
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした。",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # トークンをデコードしてペイロードを取得する
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # データベースからユーザーを取得する
    user = get_user_by_email(db=db, email=email) #名前つき引数で呼び出し
    if user is None:
        raise credentials_exception
    return user

# データベースセッションを提供する依存関数
def get_db_session() -> Session:
    db = get_db()
    try:
        yield db
    finally:
        db.close()