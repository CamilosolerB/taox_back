"""
Implementación ORM del repositorio del copiloto (conversaciones y mensajes)
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.copilot_models import CopilotConversation, CopilotMessage
from app.domain.ports.out.copilot_repository import CopilotRepository
from app.infrastructure.db.models.copilot_conversation_orm import CopilotConversationORM
from app.infrastructure.db.models.copilot_message_orm import CopilotMessageORM


class CopilotORMRepository(CopilotRepository):
    """Persistencia de conversaciones y mensajes del copiloto."""

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, conversation: CopilotConversation) -> CopilotConversation:
        orm = CopilotConversationORM(
            id_empresa=conversation.id_empresa,
            id_usuario=conversation.id_usuario,
            canal=conversation.canal,
            canal_chat_id=conversation.canal_chat_id,
            alerta_id=conversation.alerta_id,
            codigo_producto=conversation.codigo_producto,
            titulo=conversation.titulo,
            estado=conversation.estado,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._conv_to_entity(orm)

    def get_conversation(self, id_conversation: UUID, company_id: Optional[str] = None) -> Optional[CopilotConversation]:
        query = self.db.query(CopilotConversationORM).filter(
            CopilotConversationORM.id_conversation == id_conversation
        )
        if company_id is not None:
            query = query.filter(CopilotConversationORM.id_empresa == company_id)
        orm = query.first()
        return self._conv_to_entity(orm) if orm else None

    def get_conversations_by_company(self, company_id: str) -> List[CopilotConversation]:
        rows = (
            self.db.query(CopilotConversationORM)
            .filter(CopilotConversationORM.id_empresa == company_id)
            .order_by(CopilotConversationORM.updated_at.desc())
            .all()
        )
        return [self._conv_to_entity(r) for r in rows]

    def get_latest_conversation_by_channel(self, canal: str, canal_chat_id: str) -> Optional[CopilotConversation]:
        orm = (
            self.db.query(CopilotConversationORM)
            .filter(
                CopilotConversationORM.canal == canal,
                CopilotConversationORM.canal_chat_id == str(canal_chat_id),
            )
            .order_by(CopilotConversationORM.updated_at.desc())
            .first()
        )
        return self._conv_to_entity(orm) if orm else None

    def update_conversation(self, id_conversation: UUID, data: dict) -> Optional[CopilotConversation]:
        orm = (
            self.db.query(CopilotConversationORM)
            .filter(CopilotConversationORM.id_conversation == id_conversation)
            .first()
        )
        if not orm:
            return None
        for key, value in data.items():
            setattr(orm, key, value)
        self.db.commit()
        self.db.refresh(orm)
        return self._conv_to_entity(orm)

    def add_message(self, message: CopilotMessage) -> CopilotMessage:
        orm = CopilotMessageORM(
            id_conversation=message.id_conversation,
            rol=message.rol,
            contenido=message.contenido,
            canal=message.canal,
            proveedor=message.proveedor,
            modelo=message.modelo,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._msg_to_entity(orm)

    def get_messages(self, id_conversation: UUID, company_id: Optional[str] = None) -> List[CopilotMessage]:
        if company_id is not None:
            conv = self.get_conversation(id_conversation, company_id)
            if not conv:
                return []
        rows = (
            self.db.query(CopilotMessageORM)
            .filter(CopilotMessageORM.id_conversation == id_conversation)
            .order_by(CopilotMessageORM.id_mensaje.asc())
            .all()
        )
        return [self._msg_to_entity(r) for r in rows]

    def get_recent_messages(self, id_conversation: UUID, limit: int = 20) -> List[CopilotMessage]:
        rows = (
            self.db.query(CopilotMessageORM)
            .filter(CopilotMessageORM.id_conversation == id_conversation)
            .order_by(CopilotMessageORM.id_mensaje.desc())
            .limit(limit)
            .all()
        )
        return [self._msg_to_entity(r) for r in reversed(rows)]

    def _conv_to_entity(self, orm: CopilotConversationORM) -> CopilotConversation:
        return CopilotConversation(
            id_conversation=orm.id_conversation,
            id_empresa=orm.id_empresa,
            id_usuario=orm.id_usuario,
            canal=orm.canal,
            canal_chat_id=orm.canal_chat_id,
            alerta_id=orm.alerta_id,
            codigo_producto=orm.codigo_producto,
            titulo=orm.titulo,
            estado=orm.estado,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def _msg_to_entity(self, orm: CopilotMessageORM) -> CopilotMessage:
        return CopilotMessage(
            id_mensaje=orm.id_mensaje,
            id_conversation=orm.id_conversation,
            rol=orm.rol,
            contenido=orm.contenido,
            canal=orm.canal,
            proveedor=orm.proveedor,
            modelo=orm.modelo,
            created_at=orm.created_at,
        )
