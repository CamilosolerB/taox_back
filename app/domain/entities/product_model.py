from dataclasses import dataclass
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
    company_id: UUID