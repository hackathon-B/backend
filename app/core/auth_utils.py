from datetime import datetime
from typing import Optional, Dict, Union
from jose import jwt, JWTError
import requests
from app.core.config import settings

# OIDCの設定
OIDC_ISSUER = settings.OIDC_ISSUER
OIDC_CLIENT_ID = settings.OIDC_CLIENT_ID
OIDC_CLIENT_SECRET = settings.OIDC_CLIENT_SECRET
OIDC_REDIRECT_URI = settings.OIDC_REDIRECT_URI

# OIDCメタデータを動的に取得する
def get_oidc_metadata() -> Dict[str, str]:
    metadata_url = f"{OIDC_ISSUER}/.well-known/openid-configuration"
    response = requests.get(metadata_url)
    response.raise_for_status()
    return response.json()

# OIDCの公開鍵(JWKS)を取得し、トークンの検証に使用する
def get_jwks() -> Dict[str, Union[str, int]]:
    jwks_uri = get_oidc_metadata().get("jwks_uri")
    response = requests.get(jwks_uri)
    response.raise_for_status()
    return response.json()

# OIDCのIDトークンの検証し、ペイロードを取得する
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
        raise ValueError(f"IDトークンは無効です。 {str(e)}") from e

# アクセストークンの検証し、ペイロードを取得する
def verify_access_token(access_token: str) -> Optional[Dict[str, Union[str, int]]]:
    jwks = get_jwks()
    try:
        payload = jwks.decode(
            access_token,
            jwks,
            algorithms=["RS256"],
            audience=OIDC_CLIENT_ID,
            issuer=OIDC_ISSUER,
        )
        return payload
    except JWTError:
        return None

# リフレッシュトークンを使用して新しいIDトークン・アクセストークンを取得する
def refresh_token(refresh_token: str) -> Dict[str, str]:
    token_url = get_oidc_metadata().get("token_endpoint")
    data = {
        "grant_type": "refresh_token",
        "client_id": OIDC_CLIENT_ID,
        "client_secret": OIDC_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    response = requests.post(token_url, data=data)
    if response.status_code !=200:
        raise ValueError(f"リフレッシュトークンの更新に失敗しました。： {response.text}")
    return response.json()

# 認可コードを使用してIDトークン、アクセストークン、リフレッシュトークンを取得する
def generate_token(auth_code: str) -> Dict[str, str]:
    token_url =get_oidc_metadata().get("token_endpoint")
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": OIDC_REDIRECT_URI,
        "client_id": OIDC_CLIENT_ID,
        "client_secret": OIDC_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    if response.status_code !=200:
        raise ValueError(f"認可コードからトークンの取得に失敗しました。： {response.text}")
        return response.json()

# トークン有効期限のチェックする
def is_token_expired(token_payload: Dict[str, Union[str, int]]) -> bool:
    exp = token_payload.get("exp")
    if not exp:
        raise ValueError("トークンに有効期限の情報が含まれていません。")
    return datetime.utcfromtimestamp(exp) < datetime.utccnow()