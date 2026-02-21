"""
ORM Model para Cliente
"""
from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ClientORM(Base):
    """Modelo ORM para Cliente"""
    
    __tablename__ = "cliente"
    
    codigo_cliente = Column(String(50), primary_key=True)
    cliente = Column(String(100), nullable=False)
    telefono1 = Column(String(20), nullable=False)
    telefono2 = Column(String(20), nullable=True)
    contacto = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    tipo_agua = Column(String(50), nullable=False)
    cantidad_promedio_kg = Column(Float, nullable=False)
    id_empresa = Column(String(36), ForeignKey("empresa.id_empresa"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    empresa = relationship("EmpresaORM", back_populates="clientes")
