from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserDTO(BaseModel):
    id_user: UUID | None
    username: str
    email: str
    password: str
    is_active: bool
    role_id: UUID
    company_id: UUID

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, user_orm):
        return cls(
            id_user=user_orm.id_user,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password,
            is_active=user_orm.is_active,
            role_id=user_orm.role_id,
            company_id=user_orm.company_id
        )
