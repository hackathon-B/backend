from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate
from app.crud.base import CRUDBase

class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def get_by_chat(self, db_session: Session, *, chat_id: int) -> List[Message]:
        # 特定のチャットに関連するすべてのメッセージを取得
        try:
            return db_session.query(Message).filter(Message.chat_id == chat_id).all()
        except Exception as e:
            db_session.rollback()
            raise e
    
# updateとdeleteはbaseクラスのメソッドで代用可能
    
crud_message = CRUDMessage(Message)