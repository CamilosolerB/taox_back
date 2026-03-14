"""
ORM model para Chemical Stock (Stock Químico)
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime
import uuid


class ChemicalStockORM(Base):
    """Modelo ORM para stock de químicos"""
    __tablename__ = "stock_quimicos"
    
    id_stock_quimico = Column(Integer, primary_key=True, autoincrement=True)
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), nullable=False)
    id_proceso = Column(PG_UUID(as_uuid=True), ForeignKey("procesos.id_proceso"), nullable=False)
    cantidad_actual = Column(Float, nullable=False, default=0)
    cantidad_minima = Column(Float, nullable=False)
    cantidad_maxima = Column(Float, nullable=False)
    unidad_medida = Column(String(20), nullable=False)  # ml, g, l, kg, etc
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    producto = relationship("Product", foreign_keys=[codigo_producto])
    proceso = relationship("ProcessORM", back_populates="stocks", foreign_keys=[id_proceso])
    empresa = relationship("Company", foreign_keys=[id_empresa])
    alertas = relationship("StockAlertORM", back_populates="stock")
