from datetime import datetime, timedelta
from typing import Optional, Dict, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# パスワードのハッシュ化するための設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWTの設定
SECRET_KEY =settings.SECRET_KEY
ALGORITHM = "HS256"

# パスワードのハッシュ化する
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ハッシュ化したパスワードを検証する
def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)

# アクセストークンを生成する
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # 修正

# アクセストークンの検証し、ペイロードを取得する
def verify_access_token(access_token: str) -> Optional[Dict[str, Union[str, int]]]:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# トークン有効期限のチェックをする
def is_token_expired(token_payload: Dict[str, Union[str, int]]) -> bool:
    exp = token_payload.get("exp")
    if not exp:
        raise ValueError("トークンに有効期限の情報が含まれていません。")
    return datetime.utcfromtimestamp(exp) < datetime.utcnow()