from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional


class UserDetailDTO(BaseModel):
    id_user: UUID
    username: str
    email: str
    password: str
    is_active: bool
    role_id: UUID
    company_id: UUID | None = None
    role_name: Optional[str] = None
    company_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, user):
        return cls(
            id_user=user.id_user,
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            role_id=user.role_id,
            company_id=user.company_id
        )

    @classmethod
    def from_orm_with_relations(cls, user_orm):
        role_name = user_orm.role.name if hasattr(user_orm, 'role') and user_orm.role else None
        company_name = user_orm.company.name if hasattr(user_orm, 'company') and user_orm.company else None
        return cls(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id,
            role_name=role_name,
            company_name=company_name
        )
