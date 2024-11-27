from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.crud.base import CRUDBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def create(self, db_session: Session, *, obj_in: ChatCreate, user_id: int) -> Chat:
        """チャットを作成"""
        db_obj = Chat(
            chat_title=obj_in.chat_title,
            use_model_id=obj_in.use_model_id,
            user_id=user_id
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

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
