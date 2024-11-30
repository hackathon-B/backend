from openai import OpenAI, OpenAIError 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from typing import List

from app.api import deps
from app.schemas.message import Message, MessageCreate, MessageUpdate, SenderType, MessageResponse, ChatMessageResponse, ReceiveMessage
from app.crud.chat import crud_chat
from app.crud.message import crud_message
from app.schemas.chat import ChatCreate, ChatWithMessages
from app.models.chat import Chat as ChatModel
from app.models.message import Message as MessageModel

# .envファイルの読み込み
load_dotenv()

router = APIRouter()

# OpenAI APIキーの設定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_ai_response(prompt: str, use_model_id: int) -> str:
    """OpenAI APIを使用してAIレスポンスを生成する"""
    try:
        if use_model_id == 1:
            # chatGPTを使用する場合の処理
            response = client.chat.completions.create(
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                model="gpt-3.5-turbo",
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content
        elif use_model_id == 2:
            # chatGPt4oを使用する場合の処理
            response = client.chat.completions.create(
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                model="gpt-4o",
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content
        # claudeを使用する場合の処理
        elif use_model_id == 3:
            raise NotImplementedError("Claude model is not implemented yet")
        else:
            raise ValueError(f"Invalid model ID: {use_model_id}")
    except OpenAIError as e:
        raise HTTPException(
            status_code=503,
            detail=f"OpenAI service error: {str(e)}"
        )

@router.post("", response_model=ChatMessageResponse)
async def create_message(
    chat_id: int,
    message: ReceiveMessage,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    # 新しいチャットを作成するか、既存のチャットを取得
    if chat_id == 0:
        chat = ChatModel(
            chat_title=message.message_text[:15] + "..." if len(message.message_text) > 15 else message.message_text,
            use_model_id=message.use_model_id,  # 指定したモデルIDを設定
            user_id=current_user.user_id,
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
    else:
        chat = crud_chat.get(db_session=db, id=chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        if chat.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Access forbidden")

    # ユーザーメッセージ保存
    user_message = MessageModel(
        message_text=message.message_text,
        chat_id=chat.chat_id,
        sender_type=SenderType.USER
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # AIレスポンス生成と保存
    ai_response = await generate_ai_response(message.message_text, chat.use_model_id)
    ai_message = MessageModel(
        message_text=ai_response,
        chat_id=chat.chat_id,
        sender_type=SenderType.AI
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    # チャット履歴を取得
    messages = db.query(MessageModel).filter(MessageModel.chat_id == chat.chat_id).order_by(MessageModel.created_at).all()

    # レスポンス用に整形
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

# 特定のメッセージ変更
@router.put("/{message_id}", response_model=Message)
def update_message(
    chat_id: int, 
    message_id: int, 
    message: MessageUpdate, 
    db: Session = Depends(deps.get_db), 
    current_user = Depends(deps.get_current_user)
):
    """メッセージを更新する"""
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat or chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    db_message = crud_message.get(db_session=db, id=message_id)
    if not db_message or db_message.chat_id != chat_id:
        raise HTTPException(status_code=404, detail="Message not found")
    
    updated_message = crud_message.update(
        db_session=db, 
        db_obj=db_message, 
        obj_in=message
    )
    return updated_message

# 特定のメッセージ削除
@router.delete("/{message_id}", response_model=dict)
def delete_message(
    chat_id: int, 
    message_id: int, 
    db: Session = Depends(deps.get_db), 
    current_user = Depends(deps.get_current_user)
):
    """メッセージを削除する"""
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat or chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    try:   
        crud_message.remove(db_session=db, id=message_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Message no found")
    
    return {"status": "success", "message": "Message deleted successfully"}