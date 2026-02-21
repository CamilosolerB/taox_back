"""
ORM Model para Ubicación
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class LocationORM(Base):
    """Modelo ORM para Ubicación"""
    
    __tablename__ = "ubicacion"
    
    id_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    ubicacion = Column(String(100), nullable=False)
    posicion = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)
    tipo_ubicacion = Column(String(50), nullable=False)
    localizador = Column(String(100), nullable=False)
    id_empresa = Column(String(36), ForeignKey("empresa.id_empresa"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    empresa = relationship("EmpresaORM", back_populates="ubicaciones")
    stock_ubicaciones = relationship("StockLocationORM", back_populates="ubicacion")
