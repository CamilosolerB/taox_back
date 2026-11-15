"""
ORM model para Telegram Account (vinculación de cuenta de Telegram con usuario TAOX)
"""
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
from datetime import datetime


class TelegramAccountORM(Base):
    """Asocia un chat de Telegram con un usuario y empresa de TAOX."""

    __tablename__ = "telegram_accounts"

    id_cuenta = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id_user"), nullable=False, unique=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)
    telegram_username = Column(String(100), nullable=True)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=True)
    linked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    usuario = relationship("User", foreign_keys=[user_id])
    empresa = relationship("Company", foreign_keys=[id_empresa])
