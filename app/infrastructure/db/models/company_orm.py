from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
import uuid

class Company(Base):
    __tablename__ = "companies"
    id_company = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    nit = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    users = relationship("User", back_populates="company")
    products = relationship("Product", back_populates="company")