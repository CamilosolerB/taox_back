from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ProductDTO(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, product):
        return cls(
            id_product=product.id_product,
            name=product.name,
            generic_name=product.generic_name,
            price=product.price,
            unit_measure=product.unit_measure,
            unit_price=product.unit_price,
            min_unit_price=product.min_unit_price,
            lead_time_days=product.lead_time_days,
            restorage=product.restorage,
            limite_critico=product.limite_critico,
            warehouse_id=product.warehouse_id if hasattr(product, 'warehouse_id') else None,
            company_id=product.company_id,
            fds=product.fds if hasattr(product, 'fds') else None,
            fds_url=product.fds_url if hasattr(product, 'fds_url') else None
        )
