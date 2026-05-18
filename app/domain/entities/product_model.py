from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class Product:
    id_product: str | None
    name: str
    generic_name: str
    price: float
    unit_measure: str
    unit_price: float
    min_unit_price: float
    lead_time_days: int
    restorage: str
    limite_critico: float
    warehouse_id: UUID | None = field(default=None)
    company_id: UUID = field(default=None)
    fds: str | None = None
    fds_url: str | None = None