from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from app.infrastructure.db.base import Base


class ClientORM(Base):
    
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
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    company = relationship("Company", back_populates="clientes")
