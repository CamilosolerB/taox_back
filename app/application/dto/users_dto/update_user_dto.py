from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UpdateUserDTO(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    role_id: UUID | None = None
    company_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)
