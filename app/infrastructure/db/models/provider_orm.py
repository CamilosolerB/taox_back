from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from app.infrastructure.db.base import Base


class ProviderORM(Base):
    
    __tablename__ = "proveedor"
    
    cad_proveedor = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=False)
    celular = Column(String(20), nullable=False)
    web = Column(String(255), nullable=True)
    correo = Column(String(100), nullable=False)
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    empresa = relationship("Company", back_populates="proveedores")
    producto_proveedores = relationship("ProductProviderORM", back_populates="proveedor")
