from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.message import Message

class ChatBase(BaseModel):
    chat_title: str
    use_model_id: int 
    parent_chat_id: Optional[int] = None
    
class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    chat_title: Optional[str] = None
    use_model_id: Optional[int] = None
    
class ChatInDBBase(ChatBase):
    chat_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class Chat(ChatInDBBase):
    pass

class ChatWithMessages(ChatInDBBase):
    messages: List[Message] = []
    
