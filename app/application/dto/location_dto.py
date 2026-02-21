"""
DTOs para Ubicación
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class LocationCreateDTO(BaseModel):
    """DTO para crear una ubicación"""
    ubicacion: str = Field(..., min_length=1, max_length=100, description="Nombre de la ubicación")
    posicion: str = Field(..., min_length=1, max_length=50, description="Posición")
    nivel: str = Field(..., min_length=1, max_length=50, description="Nivel")
    tipo_ubicacion: str = Field(..., min_length=1, max_length=50, description="Tipo de ubicación")
    localizador: str = Field(..., min_length=1, max_length=100, description="Código localizador")
    company_id: UUID = Field(..., description="UUID de la empresa")


class LocationUpdateDTO(BaseModel):
    """DTO para actualizar una ubicación"""
    ubicacion: Optional[str] = Field(None, min_length=1, max_length=100)
    posicion: Optional[str] = Field(None, min_length=1, max_length=50)
    nivel: Optional[str] = Field(None, min_length=1, max_length=50)
    tipo_ubicacion: Optional[str] = Field(None, min_length=1, max_length=50)
    localizador: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class LocationDTO(BaseModel):
    """DTO para respuesta de ubicación"""
    id_ubicacion: int
    ubicacion: str
    posicion: str
    nivel: str
    tipo_ubicacion: str
    localizador: str
    company_id: UUID
    is_active: bool
    
    class Config:
        from_attributes = True
