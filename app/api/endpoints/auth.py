from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.core.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello" : "Fucabo!!"}

# 新規登録ページの表示
@router.get("/api/auth/register")
async def register_page():
    return {"message" : "Fucaboの新規登録画面です"}

# 新規登録処理
@router.post("/api/auth/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # 既にメールアドレスが登録されていないか確認
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="既にメールアドレスは登録されています")

    # 新規ユーザーの登録
    new_user = create_user(db=db, user=user)

    # JWTトークンを生成する
    token = create_access_token({"sub":new_user.email})
    return {"user": new_user, "access_token": token, "token_type": "bearer"}

# ログインページの表示
@router.get("/api/auth/login")
async def login_page():
    return {"message" : "メールアドレスとパスワードを入力してください"}

# ログイン処理
@router.post("/api/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # メールアドレスに対応するユーザーをデータベースから取得する
    user = get_user_by_email(db, email=form_data.username)

    # ユーザーが存在しないか、パスワードが正しくない場合
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="メールアドレスまたはパスワードが正しくありません")

    # JWTトークンを生成する
    token = create_access_token({"sub":user.email})
    return {"access_token": token, "token_type": "bearer"}

# ログアウト
@router.post("/api/auth/logout")
async def logout():
    return {"message" : "ログアウトしました"}