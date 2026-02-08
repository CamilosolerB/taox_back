from pydantic import BaseModel
from uuid import UUID

class RoleDTO(BaseModel):
    id_role: UUID
    name: str

    @classmethod
    def from_entity(cls, role_orm):
        return cls(
            id_role=role_orm.id_role,
            name=role_orm.name
        )