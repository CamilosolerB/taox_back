from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from app.infrastructure.db.base import Base
import uuid


class WarehouseORM(Base):
    """Modelo ORM para Almacenes"""
    
    __tablename__ = "warehouses"
    
    id_warehouse = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    company_id = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    company = relationship("Company", back_populates="warehouses")
    stocks = relationship("StockWarehouseORM", back_populates="warehouse")