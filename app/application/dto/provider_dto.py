"""
DTOs para Proveedor
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID


class ProviderCreateDTO(BaseModel):
    """DTO para crear un proveedor"""
    cad_proveedor: str = Field(..., min_length=1, max_length=50, description="Código único del proveedor")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del proveedor")
    contacto: str = Field(..., min_length=1, max_length=100, description="Persona de contacto")
    direccion: str = Field(..., min_length=1, max_length=255, description="Dirección")
    telefono: str = Field(..., min_length=7, max_length=20, description="Teléfono")
    celular: str = Field(..., min_length=7, max_length=20, description="Celular")
    web: Optional[str] = Field(None, max_length=255, description="Sitio web")
    correo: EmailStr = Field(..., description="Email del proveedor")
    company_id: UUID = Field(..., description="UUID de la empresa")


class ProviderUpdateDTO(BaseModel):
    """DTO para actualizar un proveedor"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    contacto: Optional[str] = Field(None, min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, min_length=7, max_length=20)
    celular: Optional[str] = Field(None, min_length=7, max_length=20)
    web: Optional[str] = Field(None, max_length=255)
    correo: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class ProviderDTO(BaseModel):
    """DTO para respuesta de proveedor"""
    cad_proveedor: str
    nombre: str
    contacto: str
    direccion: str
    telefono: str
    celular: str
    web: Optional[str]
    correo: str
    company_id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_entity(cls, provider):
        """Convierte entidad Provider a ProviderDTO"""
        return cls(
            cad_proveedor=provider.cad_proveedor,
            nombre=provider.nombre,
            contacto=provider.contacto,
            direccion=provider.direccion,
            telefono=provider.telefono,
            celular=provider.celular,
            web=provider.web,
            correo=provider.correo,
            company_id=provider.id_empresa,
            is_active=provider.is_active
        )
