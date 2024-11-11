import openai 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.api.deps import get_db, get_current_user
from app.models.message import Message as MessageModel
from app.schemas.message import MessageCreate, MessageUpdate 
from app.crud.chat import crud_chat
from app.crud.message import crud_message
from app.schemas.chat import Chat, ChatCreate

# .envファイルの読み込み
load_dotenv()

router = APIRouter(prefix="/api/chats/{chat_id}/messages")

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# ChatGPT APIを使ってチャットを生成
@router.post("", response_model=MessageModel)
def generate_chat(chat_id: int, prompt: MessageCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # チャットの存在確認とユーザーの検証
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat:
        # チャットが存在しない場合、新しいチャットを作成し、最初のメッセージからタイトルを生成
        title = prompt.content[:10]
        new_chat = ChatCreate(user_id=current_user.user_id, chat_title=title)
        chat = crud_chat.create(db_session=db, obj_in=new_chat)
    elif chat.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    user_message_data = MessageCreate(message_text=prompt.content, chat_id=chat_id, sender_type="user")
    db_user_message = crud_message.create(db_session=db, obj_in=user_message_data)
    
    # OpenAI API を使ってレスポンスを生成
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.content}],
            max_tokens=150
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    # 生成されたレスポンスをメッセージとしてデータベースに保存
    response_text = response.choices[0]['message']['content'].strip()
    ai_message_data = MessageCreate(message_text=response_text, chat_id=chat_id, sender_type="ai")
    db_ai_message = crud_message.create(db_session=db, obj_in=ai_message_data)
    
    all_messages = db.query(MessageModel).filter(MessageModel.chat_id == chat_id).all()
    
    return Chat(**chat.__dict__, messages=[message.__dict__ for message in all_messages])

# 特定のメッセージ変更
@router.put("/{message_id}", response_model=MessageModel)
def update_message(chat_id: int, message_id: int, message: MessageUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat or chat.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_message = crud_message.get(db_session=db, id=message_id)
    if not db_message or db_message.chat_id != chat_id:
        raise HTTPException(status_code=404, detail="Message not found")
    updated_message = crud_message.update(db_session=db, db_obj=db_message, obj_in=message)
    return updated_message

# 特定のメッセージ削除
@router.delete("/{message_id}", response_model=dict)
def delete_message(chat_id: int, message_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    chat = crud_chat.get(db_session=db, id=chat_id)
    if not chat or chat.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Message not found")
    db_message = crud_message.get(db_session=db, id=message_id)
    if not db_message or db_message.chat_id != chat_id:
        raise HTTPException(status_code=404, detail="Message not found")
    if not crud_message.delete_message(db_session=db, message_id=message_id):
        raise HTTPException(status_code=500, detail="Failed to delete message")
    return {"message": "メッセージを削除しました"}