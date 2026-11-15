"""
ORM model para Copilot Conversation (conversación del copiloto IA)
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
from datetime import datetime
import uuid


class CopilotConversationORM(Base):
    """Conversación compartida entre el chat interno de TAOX y los canales externos."""

    __tablename__ = "copilot_conversations"

    id_conversation = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=True)
    id_usuario = Column(PG_UUID(as_uuid=True), ForeignKey("users.id_user"), nullable=True)
    canal = Column(String(20), nullable=False, default="web")  # web | telegram | whatsapp (fase 2)
    canal_chat_id = Column(String(64), nullable=True)  # p.ej. chat_id de Telegram
    alerta_id = Column(Integer, ForeignKey("alertas_stock.id_alerta"), nullable=True)
    codigo_producto = Column(String(50), nullable=True)
    titulo = Column(String(200), nullable=True)
    estado = Column(String(20), nullable=False, default="activa")  # activa | archivada
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    mensajes = relationship(
        "CopilotMessageORM",
        back_populates="conversacion",
        cascade="all, delete-orphan",
        order_by="CopilotMessageORM.created_at",
    )
