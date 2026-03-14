"""
DTOs for Product Movement entity
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductMovementCreateDTO(BaseModel):
    """DTO para crear un nuevo movimiento"""
    codigo_producto: str = Field(..., description="Código del producto", min_length=1, max_length=50)
    id_proceso_origen: str = Field(..., description="ID del proceso de origen")
    id_proceso_destino: str = Field(..., description="ID del proceso de destino")
    cantidad: float = Field(..., description="Cantidad a mover", gt=0)
    notas: Optional[str] = Field(None, description="Notas adicionales del movimiento", max_length=500)
    id_empresa: str = Field(..., description="ID de la empresa propietaria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "codigo_producto": "CHEM001",
                "id_proceso_origen": 1,
                "id_proceso_destino": 2,
                "cantidad": 10.5,
                "notas": "Movimiento de producción a préstamo",
                "id_empresa": "company-123"
            }
        }


class ProductMovementUpdateDTO(BaseModel):
    """DTO para actualizar un movimiento"""
    estado: Optional[str] = Field(None, description="Estado del movimiento (pendiente, en_transito, completado, cancelado)")
    notas: Optional[str] = Field(None, description="Notas adicionales", max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "completado",
                "notas": "Movimiento realizado exitosamente"
            }
        }


class ProductMovementResponseDTO(BaseModel):
    """DTO para respuestas de movimiento"""
    id_movimiento: int
    codigo_producto: str
    id_proceso_origen: str
    id_proceso_destino: str
    cantidad: float
    notas: Optional[str]
    id_empresa: str
    estado: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_movimiento": 1,
                "codigo_producto": "CHEM001",
                "id_proceso_origen": "550e8400-e29b-41d4-a716-446655440001",
                "id_proceso_destino": "550e8400-e29b-41d4-a716-446655440002",
                "cantidad": 10.5,
                "notas": "Movimiento de producción a préstamo",
                "id_empresa": "company-123",
                "estado": "completado",
                "created_at": "2025-03-01T10:00:00",
                "updated_at": "2025-03-01T10:30:00"
            }
        }
