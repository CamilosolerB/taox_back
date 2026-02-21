"""
DTOs para Cliente
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ClientCreateDTO(BaseModel):
    """DTO para crear un cliente"""
    codigo_cliente: str = Field(..., min_length=1, max_length=50, description="Código único del cliente")
    cliente: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    telefono1: str = Field(..., min_length=7, max_length=20, description="Teléfono principal")
    telefono2: Optional[str] = Field(None, min_length=7, max_length=20, description="Teléfono secundario")
    contacto: str = Field(..., min_length=1, max_length=100, description="Persona de contacto")
    correo: str = Field(..., description="Email del cliente")
    ciudad: str = Field(..., min_length=1, max_length=100, description="Ciudad")
    tipo_agua: str = Field(..., min_length=1, max_length=50, description="Tipo de agua")
    cantidad_promedio_kg: float = Field(..., gt=0, description="Cantidad promedio en kg")
    company_id: UUID = Field(..., description="UUID de la empresa")


class ClientUpdateDTO(BaseModel):
    """DTO para actualizar un cliente"""
    cliente: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono1: Optional[str] = Field(None, min_length=7, max_length=20)
    telefono2: Optional[str] = Field(None, min_length=7, max_length=20)
    contacto: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[str] = None
    ciudad: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_agua: Optional[str] = Field(None, min_length=1, max_length=50)
    cantidad_promedio_kg: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class ClientDTO(BaseModel):
    """DTO para respuesta de cliente"""
    codigo_cliente: str
    cliente: str
    telefono1: str
    telefono2: Optional[str]
    contacto: str
    correo: str
    ciudad: str
    tipo_agua: str
    cantidad_promedio_kg: float
    company_id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True
