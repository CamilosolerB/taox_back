from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base
import uuid

class Role(Base):
    __tablename__ = "roles"

    id_role = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    users = relationship("User", back_populates="role")