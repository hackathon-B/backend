from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import inspect

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

    def update_chat(
        self, 
        db_session: Session, 
        *, 
        chat_id: int, 
        new_title: Optional[str] = None,
        new_model_id: Optional[int] = None
    ) -> Chat:
        """チャットの情報を更新する"""
        chat = db_session.query(Chat).filter(Chat.chat_id == chat_id).first()
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")
            
        if new_title is not None:
            chat.chat_title = new_title
        if new_model_id is not None:
            chat.use_model_id = new_model_id
            
        db_session.add(chat)
        try:
            db_session.commit()
            db_session.refresh(chat)
        except Exception as e:
            db_session.rollback()
            raise e
        
        return chat

    def delete_chat(self, db_session: Session, *, chat_id: int) -> bool:
        """チャットを削除する"""
        try:
            chat = db_session.query(Chat).filter(Chat.chat_id == chat_id).first()
            if not chat:
                return False
            
            db_session.delete(chat)
            db_session.commit()
            return True
        except Exception:
            db_session.rollback()
            return False


crud_chat = CRUDChat(Chat)
