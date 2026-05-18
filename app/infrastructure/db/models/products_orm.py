from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id_product = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    generic_name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    unit_measure = Column(String, nullable=False)
    unit_price = Column(String, nullable=False)
    min_unit_price = Column(String, nullable=False)
    lead_time_days = Column(String, nullable=False)
    restorage = Column(String, nullable=False)
    limite_critico = Column(Float, nullable=False, server_default='0.0')
    warehouse_id = Column(PG_UUID(as_uuid=True), ForeignKey("procesos.id_proceso"), nullable=True)
    company_id = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    fds = Column(String, nullable=True)
    fds_url = Column(String, nullable=True)
    company = relationship("Company", back_populates="products")
    product_proveedores = relationship("ProductProviderORM", back_populates="producto")
    stock_ubicaciones = relationship("StockLocationORM", back_populates="producto")
    stock_almacen = relationship("StockWarehouseORM", back_populates="producto")
    warehouse = relationship("ProcessORM", foreign_keys=[warehouse_id], back_populates="productos")