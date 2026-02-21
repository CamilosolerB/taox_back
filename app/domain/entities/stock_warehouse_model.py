"""
Entidad de dominio para Stock en Almacén
"""
from typing import Optional
from datetime import datetime


class StockWarehouse:
    """
    Entidad Stock Almacén (STOCK_ALMACEN)
    
    Representa la cantidad total de un producto en el almacén.
    """
    
    def __init__(
        self,
        codigo_producto: str,
        cantidad: int,
        id_empresa: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.id_empresa = id_empresa
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"<StockWarehouse producto={self.codigo_producto}, qty={self.cantidad}>"
