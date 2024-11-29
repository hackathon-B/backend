from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse, ChatMessageResponse
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
        user_id=current_user.user_id,
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

# 特定のチャット取得
@router.get("/{chat_id}", response_model=ChatMessageResponse)
def get_chat(
    chat_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # チャットの取得
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat")

    # チャットに関連するメッセージを時系列順で取得
    messages = db.query(MessageModel).filter(
        MessageModel.chat_id == chat_id
    ).order_by(MessageModel.created_at).all()

    # レスポンスの整形
    return ChatMessageResponse(
        chat_id=chat.chat_id,
        chat_title=chat.chat_title,
        messages=[
            MessageResponse(
                message_id=msg.message_id,
                message_text=msg.message_text,
                sender_type=msg.sender_type,
                created_at=msg.created_at
            ) for msg in messages
        ]
    )

# 全てのチャット取得
@router.get("/", response_model=List[Chat])
def get_all_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_chat.get_by_user(db_session=db, user_id=current_user.user_id)

# 特定のチャット変更
@router.patch("/{chat_id}", response_model=Chat)
def update_chat(
    chat_id: int, 
    chat: ChatUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_chat = crud_chat.get(db_session=db, id=chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if db_chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this chat")
    
    try:
        updated_chat = crud_chat.update_chat(
            db_session=db,
            chat_id=chat_id,
            new_title=chat.chat_title,
            new_model_id=chat.use_model_id
        )
        return updated_chat
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 特定のチャット削除
@router.delete("/{chat_id}", response_model=dict)
def delete_chat(
    chat_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # まずチャットの存在とユーザーの権限を確認
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # チャットの所有者かどうかを確認
    if chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this chat")
    
    # 権限の確認が済んだら削除を実行
    if not crud_chat.delete_chat(db_session=db, chat_id=chat_id):
        raise HTTPException(status_code=404, detail="Failed to delete chat")
    
    return {"message": "チャットを削除しました"}
