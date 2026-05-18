from pydantic import BaseModel, Field
from uuid import UUID


class WarehouseDTO(BaseModel):
    id_warehouse: UUID
    name: str
    description: str | None = None
    location: str | None = None
    is_active: bool = True
    company_id: UUID
    
    @classmethod
    def from_entity(cls, warehouse):
        return cls(
            id_warehouse=warehouse.id_warehouse,
            name=warehouse.name,
            description=warehouse.description,
            location=warehouse.location,
            is_active=warehouse.is_active,
            company_id=warehouse.company_id
        )


class CreateWarehouseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    location: str | None = Field(None, max_length=100)


class UpdateWarehouseDTO(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    location: str | None = Field(None, max_length=100)
    is_active: bool | None = None