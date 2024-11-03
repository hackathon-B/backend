from pydantic import BaseModel
from typing import Optional

class AIModelBase(BaseModel):
    ai_model_name: str
    description: Optional[str] = None
    
class AIModelInDBBase(AIModelBase):
    ai_model_id: int
    
    class Config:
        orm_mode = True
        
class AIModel(AIModelInDBBase):
    pass