from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id_user = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(PG_UUID(as_uuid=True), ForeignKey("roles.id_role"), nullable=False)
    company_id = Column(PG_UUID(as_uuid=True), ForeignKey("companies.id_company"), nullable=False)
    role = relationship("Role", back_populates="users")
    company = relationship("Company", back_populates="users")