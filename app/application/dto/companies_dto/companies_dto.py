from pydantic import BaseModel
from uuid import UUID

class CompanyDTO(BaseModel):
    id_company: UUID
    name: str
    nit: str
    address: str
    phone: str
    email: str
    is_active: bool

    @classmethod
    def from_entity(cls, company_orm):
        return cls(
            id_company=company_orm.id_company,
            name=company_orm.name,
            nit=company_orm.nit,
            address=company_orm.address,
            phone=company_orm.phone,
            email=company_orm.email,
            is_active=company_orm.is_active
        )