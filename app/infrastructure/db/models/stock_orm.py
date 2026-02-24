from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from app.infrastructure.db.base import Base


class StockLocationORM(Base):
    __tablename__ = "stock_ubicacion"
    
    id_ubicacion = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), primary_key=True)
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=0)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    ubicacion = relationship("LocationORM", back_populates="stock_ubicaciones")
    producto = relationship("Product", back_populates="stock_ubicaciones")
    empresa = relationship("Company", back_populates="stock_ubicaciones")


class StockWarehouseORM(Base):
    """Modelo ORM para Stock en Almacén"""
    
    __tablename__ = "stock_almacen"
    
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=0)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    producto = relationship("Product", back_populates="stock_almacen")
    empresa = relationship("Company", back_populates="stock_almacenes")
