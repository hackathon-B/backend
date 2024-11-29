from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SenderType(str, Enum):
    USER = "user"
    AI = "ai"

# メッセージ作成用スキーマ
class MessageCreate(BaseModel):
    message_text: str
    chat_id: int
    sender_type: SenderType
    
# メッセージ更新用スキーマ
class MessageUpdate(BaseModel):
    message_text: Optional[str] = None
    
# メッセージ応答用スキーマ
class Message(BaseModel):
    message_id: int
    message_text: str
    chat_id: int
    sender_type: SenderType
    
    class Config:
        from_attributes = True
        
# メッセージレスポンス用の新しいスキーマ
class MessageResponse(BaseModel):
    message_id: int
    message_text: str
    sender_type: SenderType
    created_at: datetime
    # chat_title: Optional[str] = None  # 新規チャット作成時のみ含める

    class Config:
        from_attributes = True

# チャットレスポンス用の新しいスキーマ
class ChatMessageResponse(BaseModel):
    chat_id: int
    chat_title: str
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
        
# チャットメッセージ作成用スキーマ
class ReceiveMessage(BaseModel):
    message_text: str
    use_model_id: int = 1