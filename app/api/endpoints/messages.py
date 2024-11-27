from openai import OpenAI, OpenAIError 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.api import deps
from app.schemas.message import Message, MessageCreate, MessageUpdate, SenderType
from app.crud.chat import crud_chat
from app.crud.message import crud_message
from app.schemas.chat import ChatCreate, ChatWithMessages

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
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        elif use_model_id == 2:
            # claudeを使用する場合の処理
            raise NotImplementedError("Claude model is not implemented yet")
        elif use_model_id == 3:
            # geminiを使用する場合の処理
            raise NotImplementedError("Gemini model is not implemented yet")
        else:
            raise ValueError(f"Invalid model ID: {use_model_id}")
    except OpenAIError as e:
        raise HTTPException(
            status_code=503,
            detail=f"OpenAI service error: {str(e)}"
        )

@router.post("/", response_model=ChatWithMessages)
async def create_message(
    chat_id: int, 
    message: MessageCreate, 
    db: Session = Depends(deps.get_db), 
    current_user = Depends(deps.get_current_user)
):
    """新しいメッセージを作成し、AIレスポンスを生成する"""
    # チャットの存在確認とユーザーの検証
    chat = crud_chat.get(db_session=db, id=chat_id)
    
    if not chat:
        # チャットが存在しない場合、新しいチャットを作成
        chat_create = ChatCreate(
            chat_title=message.message_text[:15] + "..." if len(message.message_text) > 15 else message.message_text,
            user_id=current_user.user_id, 
            use_model_id=1 # デフォルトのモデルID
        )
        chat = crud_chat.create(db_session=db, obj_in=chat_create)
    elif chat.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # ユーザーメッセージの保存
    user_message_data = MessageCreate(
        message_text=message.message_text, 
        chat_id=chat_id, 
        sender_type=SenderType.USER
    )
    crud_message.create(db_session=db, obj_in=user_message_data)
    
    # AIレスポンスの生成と保存
    ai_response = await generate_ai_response(message.message_text, chat.use_model_id)
    ai_message_data = MessageCreate(
        message_text=ai_response,
        chat_id=chat_id,
        sender_type=SenderType.AI
    )
    crud_message.create(db_session=db, obj_in=ai_message_data)
    
    # 更新されたチャット情報を返す
    return crud_chat.get_chat_details(db_session=db, chat_id=chat_id)

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