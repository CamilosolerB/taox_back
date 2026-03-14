"""
DTOs for Stock Alert entity
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StockAlertCreateDTO(BaseModel):
    """DTO para crear una nueva alerta de stock"""
    codigo_producto: str = Field(..., description="Código del producto con alerta", min_length=1, max_length=50)
    id_proceso: str = Field(..., description="ID del proceso afectado")
    tipo_alerta: str = Field(..., description="Tipo de alerta (stock_critico, stock_bajo, exceso)")
    cantidad_actual: float = Field(..., description="Cantidad actual", ge=0)
    cantidad_referencia: float = Field(..., description="Cantidad de referencia (mínima, máxima, etc)", ge=0)
    id_empresa: str = Field(..., description="ID de la empresa propietaria")
    descripcion: Optional[str] = Field(None, description="Descripción detallada de la alerta", max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "codigo_producto": "CHEM001",
                "id_proceso": 1,
                "tipo_alerta": "stock_critico",
                "cantidad_actual": 5.0,
                "cantidad_referencia": 10.0,
                "id_empresa": "company-123",
                "descripcion": "El stock ha caído por debajo del mínimo permitido"
            }
        }


class StockAlertUpdateDTO(BaseModel):
    """DTO para actualizar una alerta de stock"""
    estado: Optional[str] = Field(None, description="Estado de la alerta (activa, resuelta, ignorada)")
    descripcion: Optional[str] = Field(None, description="Descripción de la alerta", max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "resuelta",
                "descripcion": "Stock repuesto a niveles normales"
            }
        }


class StockAlertResponseDTO(BaseModel):
    """DTO para respuestas de alerta de stock"""
    id_alerta: int
    codigo_producto: str
    id_proceso: str
    tipo_alerta: str
    cantidad_actual: float
    cantidad_referencia: float
    id_empresa: str
    estado: str
    descripcion: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_alerta": 1,
                "codigo_producto": "CHEM001",
                "id_proceso": 1,
                "tipo_alerta": "stock_critico",
                "cantidad_actual": 5.0,
                "cantidad_referencia": 10.0,
                "id_empresa": "company-123",
                "estado": "activa",
                "descripcion": "El stock ha caído por debajo del mínimo permitido",
                "resolved_at": None,
                "created_at": "2025-03-01T10:00:00",
                "updated_at": "2025-03-01T10:00:00"
            }
        }
