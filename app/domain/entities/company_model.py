from dataclasses import dataclass
from uuid import UUID

@dataclass
class Company:
    id_company: UUID | None
    name: str
    nit: str
    address: str
    phone: str
    email: str
    is_active: bool