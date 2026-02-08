from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserDetailDTO(BaseModel):
    id_user: UUID
    username: str
    email: str
    password: str
    is_active: bool
    role_id: UUID
    company_id: UUID

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
