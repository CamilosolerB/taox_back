from dataclasses import dataclass
from uuid import UUID
@dataclass

class User:
    id_user: UUID | None
    username: str
    email: str
    password: str
    is_active: bool
    role_id: UUID | None
    company_id: UUID | None