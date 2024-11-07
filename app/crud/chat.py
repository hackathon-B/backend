from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.crud.base import CRUDBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    # 必要に応じて、以下のようにメソッドを加えたり、オーバーライドする。
    def get_by_user(self, db_session: Session, *, user_id: int) -> List[Chat]:
        return db_session.query(Chat).filter(Chat.user_id == user_id).all()

    def get_chat_details(self, db_session: Session, *, chat_id: int) -> Optional[Chat]:
        # 特定のチャットの情報を取得
        chat = (
            db_session.query(Chat)
            .options(
                joinedload(Chat.parent_chat),  # 親チャットをロード
                joinedload(Chat.child_chats),  # 子チャットをロード
                joinedload(Chat.messages)      # チャットに含まれるメッセージをロード
            )
            .filter(Chat.chat_id == chat_id)
            .first()
        )
        return chat 

    def update_chat(self, db_session: Session, *, chat_id: int, new_title: Optional[str] = None, new_model_id: Optional[int] = None) -> Optional[Chat]:
        chat = db_session.query(Chat).filter(Chat.chat_id == chat_id).first()
        if chat:
            if new_title is not None:
                chat.chat_title = new_title
            if new_model_id is not None:
                chat.model_id = new_model_id
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
