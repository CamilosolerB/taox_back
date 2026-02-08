from pydantic import BaseModel


class UpdateProductDTO(BaseModel):
    name: str | None = None
    generic_name: str | None = None
    price: float | None = None
    unit_measure: str | None = None
    unit_price: float | None = None
    min_unit_price: float | None = None
    lead_time_days: int | None = None
    restorage: str | None = None
