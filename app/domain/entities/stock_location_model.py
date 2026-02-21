"""
Entidad de dominio para Stock en Ubicación
"""
from typing import Optional
from datetime import datetime


class StockLocation:
    """
    Entidad Stock Ubicación (STOCK_UBICACION)
    
    Representa la cantidad de un producto en una ubicación específica del almacén.
    """
    
    def __init__(
        self,
        id_ubicacion: int,
        codigo_producto: str,
        cantidad: int,
        id_empresa: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id_ubicacion = id_ubicacion
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.id_empresa = id_empresa
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"<StockLocation ubicacion={self.id_ubicacion}, producto={self.codigo_producto}, qty={self.cantidad}>"
