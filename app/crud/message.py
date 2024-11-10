from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate
from app.crud.base import CRUDBase

class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def get_by_chat(self, db_session: Session, *, chat_id: int) -> List[Message]:
        # 特定のチャットに関連するすべてのメッセージを取得
        return db_session.query(Message).filter(Message.chat_id == chat_id).all()
    
    def update_message(self, db_session: Session, *, message_id: int, update_data: MessageUpdate) -> Optional[Message]:
        # 特定のメッセージを更新
        message = db_session.query(Message).filter(Message.message_id == message_id).first()
        if message:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(message, key, value)
            db_session.commit()
            db_session.refresh(message)
        return message
    
    def delete_message(self, db_session: Session, *, message_id: int) -> bool:
        # 特定のメッセージを削除
        message = db_session.query(Message).filter(Message.message_id == message_id).first()
        if message:
            db_session.delete(message)
            db_session.commit()
            return True
        return False
    
crud_message = CRUDMessage(Message)