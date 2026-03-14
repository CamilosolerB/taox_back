"""
ORM model para Process (Proceso)
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.infrastructure.db.base import Base
from datetime import datetime
import uuid


class ProcessORM(Base):
    """Modelo ORM para procesos"""
    __tablename__ = "procesos"
    
    id_proceso = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500))
    tipo_proceso = Column(String(50), nullable=False)  # produccion, prestamo, almacenamiento, descarte
    id_empresa = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    empresa = relationship("Company")
    movimientos_origen = relationship("ProductMovementORM", foreign_keys="ProductMovementORM.id_proceso_origen", back_populates="proceso_origen")
    movimientos_destino = relationship("ProductMovementORM", foreign_keys="ProductMovementORM.id_proceso_destino", back_populates="proceso_destino")
    stocks = relationship("ChemicalStockORM", back_populates="proceso")
