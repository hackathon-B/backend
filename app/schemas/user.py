from pydantic import BaseModel, EmailStr, Field

# ユーザーに共通する基本情報におけるスキーマを定義
class UserBase(BaseModel):
    email: EmailStr

# ユーザー作成時のスキーマを定義
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=16, description="パスワードは8文字以上16文字以内で設定してください。")

# ログイン時のスキーマを定義
class UserLogin(UserBase):
    password: str

# ユーザー情報更新時のスキーマを定義
class UserUpdate(BaseModel):
    username: str
    email: str

# トークン生成時のスキーマを定義
class Token(BaseModel):
    access_token: str
    token_typr: str

# パスワードリセットリクエスト時のスキーマを定義
class PasswordResetRequest(BaseModel):
    email: EmailStr

# パスワードリセット時のスキーマを定義
class PasswordReset(BaseModel):
    token: str
    new_password: str
