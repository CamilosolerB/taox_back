from pydantic import BaseModel
from uuid import UUID


class CreateProductDTO(BaseModel):
    id_product: str
    name: str
    generic_name: str
    price: float
    unit_measure: str
    unit_price: float
    min_unit_price: float
    lead_time_days: int
    restorage: str
    limite_critico: float
    warehouse_id: UUID | None = None
    company_id: UUID
    fds: str | None = None
    fds_url: str | None = None
