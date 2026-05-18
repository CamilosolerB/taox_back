from pydantic import BaseModel

class UpdateCompanyDTO(BaseModel):
    name: str | None = None
    nit: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    logo: str | None = None
    is_active: bool | None = None
    # Datos opcionales para actualizar el administrador de la empresa
    admin_username: str | None = None
    admin_email: str | None = None
    admin_password: str | None = None
