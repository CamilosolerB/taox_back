"""
ORM model para Telegram Update (idempotencia de actualizaciones entrantes)
"""
from sqlalchemy import Column, BigInteger, DateTime
from app.infrastructure.db.base import Base
from datetime import datetime


class TelegramUpdateORM(Base):
    """Registra cada update_id procesado para garantizar entrega única."""

    __tablename__ = "telegram_updates"

    update_id = Column(BigInteger, primary_key=True)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
