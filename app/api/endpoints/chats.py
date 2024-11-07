from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.schemas.message import MessageCreate, MessageUpdate
from app.models.chat import Chat as ChatModel
from app.models.message import Message as MessageModel
from app.api.deps import get_db, get_current_user
from app.crud.chat import crud_chat

router = APIRouter(prefix="/api/chats")

# 新しいチャットを作成
@router.post("", response_model=Chat)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return crud_chat.create(db_session=db, obj_in=chat)

# 特定のチャット取得
@router.get("/{chat_id}", response_model=Chat)
def get_chat(chat_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    chat = crud_chat.get(db_session=db, id=chat_id)
    if chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat")
    return chat

# 全てのチャット取得
@router.get("", response_model=List[Chat])
def get_all_chats(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return crud_chat.get_by_user(db_session=db, user_id=current_user.user_id)

# 特定のチャット変更
@router.patch("/{chat_id}", response_model=Chat)
def update_chat(chat_id: int, chat: ChatUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_chat = crud_chat.get(db_session=db, id=chat_id)
    if db_chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this chat")
    return crud_chat.update_chat(db_session=db, chat_id=chat_id, new_title=chat.chat_title, new_model_id=chat.use_model_id)

# 特定のチャット削除
@router.delete("/{chat_id}", response_model=dict)
def delete_chat(chat_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if not crud_chat.delete_chat(db_session=db, chat_id=chat_id):
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "チャットを削除しました"}

# 新規メッセージ作成
@router.post("/{chat_id}/messages", response_model=MessageModel)
def add_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    chat = db.query(ChatModel).filter(ChatModel.chat_id == chat_id, ChatModel.user_id == current_user.user_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_message = MessageModel(**message.dict(), chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# 特定のメッセージ変更
@router.put("/{chat_id}/messages/{message_id}", response_model=MessageModel)
def update_message(chat_id: int, message_id: int, message: MessageUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    chat = db.query(ChatModel).filter(ChatModel.chat_id == chat_id, ChatModel.user_id == current_user.user_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_message = db.query(MessageModel).filter(MessageModel.message_id == message_id, MessageModel.chat_id == chat_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    for key, value in message.dict(exclude_unset=True).items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message
