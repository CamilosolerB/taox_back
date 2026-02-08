from dataclasses import dataclass
from uuid import UUID

@dataclass
class Role:
    id_role: UUID | None
    name: str