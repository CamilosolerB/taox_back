from pydantic import BaseModel

class UpdateCompanyDTO(BaseModel):
    name: str | None = None
    nit: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    is_active: bool | None = None
