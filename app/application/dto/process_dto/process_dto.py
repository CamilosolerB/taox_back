"""
DTOs for Process entity
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProcessCreateDTO(BaseModel):
    """DTO para crear un nuevo proceso"""
    nombre: str = Field(..., description="Nombre del proceso", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Descripción del proceso", max_length=500)
    tipo_proceso: str = Field(..., description="Tipo de proceso (produccion, prestamo, almacenamiento, descarte)")
    id_empresa: str = Field(..., description="ID de la empresa propietaria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Producción de químicos",
                "descripcion": "Área destinada a la producción de químicos",
                "tipo_proceso": "produccion",
                "id_empresa": "company-123"
            }
        }


class ProcessUpdateDTO(BaseModel):
    """DTO para actualizar un proceso"""
    nombre: Optional[str] = Field(None, description="Nombre del proceso", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Descripción del proceso", max_length=500)
    tipo_proceso: Optional[str] = Field(None, description="Tipo de proceso")
    is_active: Optional[bool] = Field(None, description="Estado del proceso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Producción modificada",
                "is_active": True
            }
        }


class ProcessResponseDTO(BaseModel):
    """DTO para respuestas de proceso"""
    id_proceso: str
    nombre: str
    descripcion: Optional[str]
    tipo_proceso: str
    id_empresa: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_proceso": "550e8400-e29b-41d4-a716-446655440001",
                "nombre": "Producción de químicos",
                "descripcion": "Área de producción",
                "tipo_proceso": "produccion",
                "id_empresa": "company-123",
                "is_active": True,
                "created_at": "2025-03-01T10:00:00",
                "updated_at": "2025-03-01T10:00:00"
            }
        }
