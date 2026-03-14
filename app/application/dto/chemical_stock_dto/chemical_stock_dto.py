"""
DTOs for Chemical Stock entity
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChemicalStockCreateDTO(BaseModel):
    """DTO para crear un nuevo stock químico"""
    codigo_producto: str = Field(..., description="Código del producto químico", min_length=1, max_length=50)
    id_proceso: str = Field(..., description="ID del proceso donde está el stock")
    cantidad_actual: float = Field(..., description="Cantidad actual disponible", ge=0)
    cantidad_minima: float = Field(..., description="Cantidad mínima para alertas críticas", gt=0)
    cantidad_maxima: float = Field(..., description="Capacidad máxima del proceso", gt=0)
    unidad_medida: str = Field(..., description="Unidad de medida (ml, g, l, kg, etc)", min_length=1, max_length=20)
    id_empresa: str = Field(..., description="ID de la empresa propietaria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "codigo_producto": "CHEM001",
                "id_proceso": 1,
                "cantidad_actual": 50.0,
                "cantidad_minima": 10.0,
                "cantidad_maxima": 100.0,
                "unidad_medida": "ml",
                "id_empresa": "company-123"
            }
        }


class ChemicalStockUpdateDTO(BaseModel):
    """DTO para actualizar un stock químico"""
    cantidad_actual: Optional[float] = Field(None, description="Cantidad actual", ge=0)
    cantidad_minima: Optional[float] = Field(None, description="Cantidad mínima", gt=0)
    cantidad_maxima: Optional[float] = Field(None, description="Cantidad máxima", gt=0)
    unidad_medida: Optional[str] = Field(None, description="Unidad de medida", min_length=1, max_length=20)
    is_active: Optional[bool] = Field(None, description="Estado del stock")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cantidad_actual": 45.0,
                "cantidad_minima": 15.0,
                "cantidad_maxima": 110.0
            }
        }


class ChemicalStockResponseDTO(BaseModel):
    """DTO para respuestas de stock químico"""
    id_stock_quimico: int
    codigo_producto: str
    id_proceso: str
    cantidad_actual: float
    cantidad_minima: float
    cantidad_maxima: float
    unidad_medida: str
    id_empresa: str
    is_active: bool
    es_stock_critico: bool
    es_stock_bajo: bool
    porcentaje_stock: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_stock_quimico": 1,
                "codigo_producto": "CHEM001",
                "id_proceso": 1,
                "cantidad_actual": 50.0,
                "cantidad_minima": 10.0,
                "cantidad_maxima": 100.0,
                "unidad_medida": "ml",
                "id_empresa": "company-123",
                "is_active": True,
                "es_stock_critico": False,
                "es_stock_bajo": False,
                "porcentaje_stock": 50.0,
                "created_at": "2025-03-01T10:00:00",
                "updated_at": "2025-03-01T10:00:00"
            }
        }
