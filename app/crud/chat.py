from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.crud.base import CRUDBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def get_by_user(self, db_session: Session, *, user_id: int) -> List[Chat]:
        """ユーザーに関する全てのチャットを取得"""
        return db_session.query(Chat).filter(Chat.user_id == user_id).all()

    def get_chat_details(self, db_session: Session, *, chat_id: int) -> Optional[Chat]:
        """特定のチャットの情報を取得"""
        return (
            db_session.query(Chat)
            .options(
                joinedload(Chat.messages)  # チャットに含まれるメッセージをロード
            )
            .filter(Chat.chat_id == chat_id)
            .first()
        )

crud_chat = CRUDChat(Chat)
