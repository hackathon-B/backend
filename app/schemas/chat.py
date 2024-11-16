from datetime import datetime
from pypdantic import BaseModel, Field
from typing import Optional, List

class ChatBase(BaseModel):
    chat_title: str
    use_model_id: int 
    parent_chat_id: Optional[int] = None
    
class ChatCreate(ChatBase):
    user_id: int
    
class ChatUpdate(BaseModel):
    chat_title: Optional[str] = None
    use_model_id: Optional[int] = None
    
class ChatInDBBase(ChatBase):
    chat_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class Chat(ChatInDBBase):
    pass

class ChatWithMessages(ChatInDBBase):
    messages: List[Message] = []
    
