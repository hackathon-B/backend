from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.crud.base import CRUDBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    # 必要に応じて、以下のようにメソッドを加えたり、オーバーライドする。
    def get_by_user(self, db_session: Session, *, user_id: int) -> List[Chat]:
        return db_session.query(Chat).filter(Chat.user_id == user_id).all()

    def get_by_title(self, db_session: Session, *, user_id: int, title: str) -> Optional[Chat]:
        return db_session.query(Chat).filter(Chat.user_id == user_id, Chat.chat_title == title).first()

    def update_chat_title(self, db_session: Session, *, chat_id: int, new_title: str) -> Optional[Chat]:
        chat = db_session.query(Chat).filter(Chat.chat_id == chat_id).first()
        if chat:
            chat.chat_title = new_title
            db_session.commit()
            db_session.refresh(chat)
        return chat
    
    def delete_chat(self, db_session: Session, *, chat_id: int) -> bool:
        chat = db_session.query(Chat).filter(Chat.chat_id == chat_id).first()
        if chat:
            db_session.delete(chat)
            db_session.commit()
            return True
        return False

crud_chat = CRUDChat(Chat)
