"""
DTOs para Stock (Ubicación y Almacén)
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# Stock Ubicación DTOs
class StockLocationCreateDTO(BaseModel):
    """DTO para crear stock en ubicación"""
    id_ubicacion: int = Field(..., description="ID de la ubicación")
    codigo_producto: str = Field(..., min_length=1, max_length=50, description="Código del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad")
    company_id: UUID = Field(..., description="UUID de la empresa")


class StockLocationUpdateDTO(BaseModel):
    """DTO para actualizar stock en ubicación"""
    cantidad: int = Field(..., gt=0, description="Cantidad")


class StockLocationDTO(BaseModel):
    """DTO para respuesta de stock en ubicación"""
    id_ubicacion: int
    codigo_producto: str
    cantidad: int
    
    class Config:
        from_attributes = True


# Stock Almacén DTOs
class StockWarehouseCreateDTO(BaseModel):
    """DTO para crear stock en almacén"""
    codigo_producto: str = Field(..., min_length=1, max_length=50, description="Código del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad")
    company_id: UUID = Field(..., description="UUID de la empresa")


class StockWarehouseUpdateDTO(BaseModel):
    """DTO para actualizar stock en almacén"""
    cantidad: int = Field(..., gt=0, description="Cantidad")


class StockWarehouseDTO(BaseModel):
    """DTO para respuesta de stock en almacén"""
    codigo_producto: str
    cantidad: int
    
    class Config:
        from_attributes = True
