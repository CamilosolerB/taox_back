from dataclasses import dataclass
from uuid import UUID


@dataclass
class Warehouse:
    id_warehouse: UUID | None
    name: str
    description: str | None
    location: str | None
    is_active: bool
    company_id: str
    created_at: str | None
    updated_at: str | None