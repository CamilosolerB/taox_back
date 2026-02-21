"""
ORM Models para Stock (Ubicación y Almacén)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class StockLocationORM(Base):
    """Modelo ORM para Stock en Ubicación"""
    
    __tablename__ = "stock_ubicacion"
    
    id_ubicacion = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), primary_key=True)
    codigo_producto = Column(String(50), ForeignKey("producto.codigo_producto"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=0)
    id_empresa = Column(String(36), ForeignKey("empresa.id_empresa"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    ubicacion = relationship("LocationORM", back_populates="stock_ubicaciones")
    producto = relationship("ProductoORM", back_populates="stock_ubicaciones")
    empresa = relationship("EmpresaORM", back_populates="stock_ubicaciones")


class StockWarehouseORM(Base):
    """Modelo ORM para Stock en Almacén"""
    
    __tablename__ = "stock_almacen"
    
    codigo_producto = Column(String(50), ForeignKey("producto.codigo_producto"), primary_key=True)
    cantidad = Column(Integer, nullable=False, default=0)
    id_empresa = Column(String(36), ForeignKey("empresa.id_empresa"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    producto = relationship("ProductoORM", back_populates="stock_almacen")
    empresa = relationship("EmpresaORM", back_populates="stock_almacenes")
