from pydantic import BaseModel, Emailstr, Field

# ユーザーに共通する基本情報におけるスキーマを定義
class UserBase(BaseModel):
    email: Emailstr

# ユーザー作成時のスキーマを定義
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=16, description="パスワードは8文字以上16文字以内で設定してください。")

# ログイン時のスキーマを定義
class UserLogin(UserBase):
    password: str

# トークン生成時のスキーマを定義
class Token(BaseModel):
    access_token: str
    token_typr: str
