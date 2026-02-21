"""
Entidad de dominio para Producto-Proveedor
"""
from typing import Optional
from datetime import datetime


class ProductProvider:
    """
    Entidad Producto-Proveedor (PRODUCTO_PROVEEDOR)
    
    Relación entre Producto y Proveedor. Un producto puede tener múltiples proveedores
    y un proveedor puede suministrar múltiples productos.
    """
    
    def __init__(
        self,
        codigo_producto: str,
        cad_proveedor: str,
        es_principal: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.codigo_producto = codigo_producto
        self.cad_proveedor = cad_proveedor
        self.es_principal = es_principal
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        principal = "principal" if self.es_principal else "secundario"
        return f"<ProductProvider producto={self.codigo_producto}, proveedor={self.cad_proveedor} ({principal})>"
