from pydantic import BaseModel

class CreateCompanyDTO(BaseModel):
    name: str
    nit: str
    address: str
    phone: str
    email: str
    is_active: bool = True
