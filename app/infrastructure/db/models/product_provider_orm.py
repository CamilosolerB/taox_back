"""
ORM Model para Producto-Proveedor
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ProductProviderORM(Base):
    
    __tablename__ = "producto_proveedor"
    
    codigo_producto = Column(String(50), ForeignKey("products.id_product"), primary_key=True)
    cad_proveedor = Column(String(50), ForeignKey("proveedor.cad_proveedor"), primary_key=True)
    es_principal = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    producto = relationship("Product", back_populates="proveedores")
    proveedor = relationship("ProviderORM", back_populates="producto_proveedores")
