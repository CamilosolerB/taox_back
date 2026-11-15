"""
ORM model para Telegram Link Code (código temporal de vinculación)
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime


class TelegramLinkCodeORM(Base):
    """Código de un solo uso para vincular el chat de Telegram con un usuario TAOX."""

    __tablename__ = "telegram_link_codes"

    code = Column(String(12), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id_user"), nullable=False)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
