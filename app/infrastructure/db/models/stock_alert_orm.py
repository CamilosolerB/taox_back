"""
ORM model para Stock Alert (Alerta de Stock)
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime
import uuid


class StockAlertORM(Base):
    """Modelo ORM para alertas de stock"""
    __tablename__ = "alertas_stock"
    
    id_alerta = Column(Integer, primary_key=True, autoincrement=True)
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), nullable=False)
    id_proceso = Column(PG_UUID(as_uuid=True), ForeignKey("procesos.id_proceso"), nullable=False)
    id_stock_quimico = Column(Integer, ForeignKey("stock_quimicos.id_stock_quimico"))
    tipo_alerta = Column(String(50), nullable=False)  # stock_critico, stock_bajo, exceso
    cantidad_actual = Column(Float, nullable=False)
    cantidad_referencia = Column(Float, nullable=False)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    estado = Column(String(50), nullable=False)  # activa, resuelta, ignorada
    descripcion = Column(String(500))
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    producto = relationship("Product", foreign_keys=[codigo_producto])
    proceso = relationship("ProcessORM", foreign_keys=[id_proceso])
    stock = relationship("ChemicalStockORM", back_populates="alertas", foreign_keys=[id_stock_quimico])
    empresa = relationship("Company", foreign_keys=[id_empresa])
