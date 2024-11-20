from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.schemas.message import MessageCreate, MessageUpdate
from app.models.chat import Chat as ChatModel
from app.models.message import Message as MessageModel
from app.api.deps import get_db, get_current_user
from app.crud.chat import crud_chat
from app.models.user import User

router = APIRouter()

# 新しいチャットを作成
@router.post("/", response_model=Chat)
def create_chat(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    chat_in: ChatCreate
) -> Chat:
    chat = ChatModel(
        chat_title=chat_in.chat_title,
        use_model_id=chat_in.use_model_id,
        user_id=current_user.id,
        parent_chat_id=chat_in.parent_chat_id
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

# 特定のチャット取得
@router.get("/{chat_id}", response_model=Chat)
def get_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = crud_chat.get(db_session=db, id=chat_id)
    if chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat")
    return chat

# 全てのチャット取得
@router.get("/", response_model=List[Chat])
def get_all_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_chat.get_by_user(db_session=db, user_id=current_user.user_id)

# 特定のチャット変更
@router.patch("/{chat_id}", response_model=Chat)
def update_chat(chat_id: int, chat: ChatUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_chat = crud_chat.get(db_session=db, id=chat_id)
    if db_chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this chat")
    return crud_chat.update_chat(db_session=db, chat_id=chat_id, new_title=chat.chat_title, new_model_id=chat.use_model_id)

# 特定のチャット削除
@router.delete("/{chat_id}", response_model=dict)
def delete_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not crud_chat.delete_chat(db_session=db, chat_id=chat_id):
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "チャットを削除しました"}
