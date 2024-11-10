from pydantic import BaseModel
from typing import Optional

# メッセージ作成用スキーマ
class MessageCreate(BaseModel):
    message_text: str
    chat_id: int
    
# メッセージ更新用スキーマ
class MessageUpdate(BaseModel):
    message_text: Optional[str] = None
    
# メッセージ応答用スキーマ
class Message(BaseModel):
    message_id: int
    message_text: str
    chat_id: int
    
    class Config:
        orm_mode = True
        

