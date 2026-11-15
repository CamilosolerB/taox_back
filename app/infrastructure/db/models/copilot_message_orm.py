"""
ORM model para Copilot Message (mensaje del copiloto IA)
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
from datetime import datetime


class CopilotMessageORM(Base):
    """Mensaje individual de una conversación del copiloto."""

    __tablename__ = "copilot_messages"

    id_mensaje = Column(Integer, primary_key=True, autoincrement=True)
    id_conversation = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("copilot_conversations.id_conversation", ondelete="CASCADE"),
        nullable=False,
    )
    rol = Column(String(20), nullable=False)  # user | assistant | system
    contenido = Column(Text, nullable=False)
    canal = Column(String(20), nullable=True)
    proveedor = Column(String(40), nullable=True)
    modelo = Column(String(80), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversacion = relationship("CopilotConversationORM", back_populates="mensajes")
