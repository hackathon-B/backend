from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.schemas.user import UserUpdate
from app.models.user import User
from app.core.security import hash_password
from app.db.session import get_db


router = APIRouter()

# ユーザー情報の取得

@router.get("")
def get_user_info(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,

        # チャットの情報を取得？ここでは不要 izumi
        # "created_at": current_user.created_at,
        # "updated_at": current_user.updated_at,
    }

# ユーザー情報の更新
@router.patch("")
def update_user_info(
    user_update: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if user_update.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています。"
            )
        current_user.email = user_update.email

    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)
    return {
        "message": "ユーザー情報が正常に更新されました。",
        "user": {
            "user_id": current_user.user_id,
            "email": current_user.email,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at,
        },
    }

# ユーザーアカウントを削除
@router.delete("")
def delete_user_account(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "ユーザーアカウントが正常に削除されました。"}