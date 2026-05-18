from pydantic import BaseModel

class CreateCompanyDTO(BaseModel):
    name: str
    nit: str
    address: str
    phone: str
    email: str
    is_active: bool = True
    logo: str | None = None
    # Datos del administrador de la empresa
    admin_username: str
    admin_email: str
    admin_password: str
