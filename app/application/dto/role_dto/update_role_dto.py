from pydantic import BaseModel

class UpdateRoleDTO(BaseModel):
    name: str | None = None
