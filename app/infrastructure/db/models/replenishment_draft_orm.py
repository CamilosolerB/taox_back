"""
ORM model para Replenishment Draft (borrador de reabastecimiento pendiente de revisión)
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime


class ReplenishmentDraftORM(Base):
    """Borrador revisable de reabastecimiento. No genera órdenes de compra."""

    __tablename__ = "replenishment_drafts"

    id_borrador = Column(Integer, primary_key=True, autoincrement=True)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    alerta_id = Column(Integer, ForeignKey("alertas_stock.id_alerta"), nullable=True)
    id_conversation = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("copilot_conversations.id_conversation", ondelete="SET NULL"),
        nullable=True,
    )
    codigo_producto = Column(String(50), nullable=False)
    cantidad_sugerida = Column(Float, nullable=True)
    unidad_medida = Column(String(20), nullable=True)
    proveedor_sugerido = Column(String(50), nullable=True)
    notas = Column(String(500), nullable=True)
    estado = Column(String(30), nullable=False, default="pendiente_revision")
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.id_user"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
