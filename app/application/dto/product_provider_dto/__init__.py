"""
DTOs para Producto-Proveedor
"""
from pydantic import BaseModel, Field
from typing import Optional


class ProductProviderCreateDTO(BaseModel):
    """DTO para crear relación producto-proveedor"""
    codigo_producto: str = Field(..., min_length=1, max_length=50, description="Código del producto")
    cad_proveedor: str = Field(..., min_length=1, max_length=50, description="Código del proveedor")
    es_principal: bool = Field(False, description="¿Es el proveedor principal?")
    precio: Optional[float] = Field(None, description="Precio del producto ofrecido por este proveedor")


class ProductProviderUpdateDTO(BaseModel):
    """DTO para actualizar relación producto-proveedor"""
    es_principal: Optional[bool] = None
    precio: Optional[float] = Field(None, description="Precio del producto ofrecido por este proveedor")


class ProductProviderDTO(BaseModel):
    """DTO para respuesta de producto-proveedor"""
    codigo_producto: str
    cad_proveedor: str
    es_principal: bool
    precio: Optional[float] = None
    
    class Config:
        from_attributes = True
