from datetime import datetime, timedelta
from typing import Optional, Dict, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
import requests

from app.core.config import settings

# パスワードのハッシュ化、検証
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="suto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)

# JWTの設定
SECRET_KEY =settings.SECRET_KEY
ALGORITHM = "HS256"

# OIDCの設定
OIDC_ISSUER = settings.GOOGLE_OIDC_ISSUER
OIDC_CLIENT_ID = settings.GOOGLE_OIDC_CLIENT_ID
OIDC_CLIENT_SECRET = settings.GOOGLE_OIDC_CLIENT_SECRET
OIDC_REDIRECT_URI = settings.GOOGLE_OIDC_REDIRECT_URI



# メタデータを動的に取得する
def get_oidc_metadata() -> Dict[str, str]:
    metadata_url = f"{OIDC_ISSUER}/.well-known/openid-configuration"
    response = requests.get(metadata_url)
    response.raise_for_status()
    return response.json()

# OIDCの公開鍵を取得する
def get_jwks() -> Dict[str, Union[str, int]]:
    jwks_uri = get_oidc_metadata().get("jwks_uri")
    response = requests.get(jwks_uri)
    response.raise_for_status()
    return response.json()

# IDトークンの検証し、ペイロードを取得する
def verify_id_token(id_token: str) -> Dict[str, Union[str, int]]:
    jwks = get_jwks()
    try:
        payload = jwt.decode(
            id_token,
            jwks,
            algorithms=["RS256"],
            audience=OIDC_CLIENT_ID,
            issuer=OIDC_ISSUER,
        )
        return payload
    except JWTError as e:
        raise ValueError(f"IDトークンは無効です。: {str(e)}") from e

# アクセストークンの検証し、ペイロードを取得する
def verify_access_token(access_token: str) -> Optional[Dict[str, Union[str, int]]]:
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(access_token)

    if not unverified_header or "kid" not in unverified_header:
        raise ValueError("トークンに公開鍵のIDが含まれていません。")

    # 公開鍵の検索
    rsa_key = next(
        (
            {"kty": key["kty"],
            "kid": key["kid"],
            "use": key["use"],
            "n": key["n"],
            "e": key["e"]}
            for key in jwks["keys"]
            if key["kid"] == unverified_header["kid"]
        ),
        None,
    )
    if not rsa_key:
        raise ValueError("適切な公開鍵が見つかりませんでした。")
    try:
        payload = jwt.decode(
            access_token,
            rsa_ley,
            algorithms=["RS256"],
            audience=OIDC_CLIENT_ID,
            issuer=OIDC_ISSUER,
        )
        return payload
    except JWTError as e:
        raise ValueError(f"アクセストークンは無効です。: {str(e)}") from e

# 認可コードを使用してIDトークン,アクセストークン,リフレッシュトークンを取得する
def generate_token(auth_code: str) -> Dict[str, str]:
    token_url = get_oidc_metadata().get("token_endpoint")
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": OIDC_CLIENT_ID,
        "client_secret": OIDC_CLIENT_SECRET,
        "redirect_uri": OIDC_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise ValueError("認可コードからトークンの取得に失敗しました。詳細： {response.text}")
    return response.json()

# リフレッシュトークンを取得して新しいトークンを取得する
def refresh_token(refresh_token: str) -> Dict[str, str]:
    token_url = get_oidc_metadata().get("token_endpoint")
    data = {
        "grant_type": "refresh_token",
        "client_id": OIDC_CLIENT_ID,
        "client_secret": OIDC_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise ValueError("トークンの更新に失敗しました。詳細： {response.text}")
    return response.json()

# トークン有効期限のチェックをする
def is_token_expired(token_payload: Dict[str, Union[str, int]]) -> bool:
    exp = token_payload.get("exp")
    if not exp:
        raise ValueError("トークンに有効期限の情報が含まれていません。")
    return datetime.utcfromtimestamp(exp) < datetime.utcnow()