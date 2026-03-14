"""
ORM model para Product Movement (Movimiento de Producto)
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime
import uuid


class ProductMovementORM(Base):
    """Modelo ORM para movimientos de productos"""
    __tablename__ = "movimientos_productos"
    
    id_movimiento = Column(Integer, primary_key=True, autoincrement=True)
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), nullable=False)
    id_proceso_origen = Column(PG_UUID(as_uuid=True), ForeignKey("procesos.id_proceso"), nullable=False)
    id_proceso_destino = Column(PG_UUID(as_uuid=True), ForeignKey("procesos.id_proceso"), nullable=False)
    cantidad = Column(Float, nullable=False)
    notas = Column(String(500))
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    estado = Column(String(50), nullable=False)  # pendiente, en_transito, completado, cancelado
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    producto = relationship("Product", foreign_keys=[codigo_producto])
    proceso_origen = relationship("ProcessORM", foreign_keys=[id_proceso_origen], back_populates="movimientos_origen")
    proceso_destino = relationship("ProcessORM", foreign_keys=[id_proceso_destino], back_populates="movimientos_destino")
    empresa = relationship("Company", foreign_keys=[id_empresa])
