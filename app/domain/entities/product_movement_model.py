"""
Entidad de Dominio para Movimiento de Producto
"""
from uuid import UUID
from datetime import datetime


class ProductMovement:
    """Registra el movimiento de un producto entre procesos"""
    
    def __init__(
        self,
        codigo_producto: str,
        id_proceso_origen: UUID,
        id_proceso_destino: UUID,
        cantidad: int,
        id_movimiento: int = None,
        notas: str = None,
        id_empresa: UUID = None,
        estado: str = 'completado',  # 'pendiente', 'en_transito', 'completado', 'cancelado'
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id_movimiento = id_movimiento
        self.codigo_producto = codigo_producto
        self.id_proceso_origen = id_proceso_origen
        self.id_proceso_destino = id_proceso_destino
        self.cantidad = cantidad
        self.notas = notas
        self.id_empresa = id_empresa
        self.estado = estado
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def __repr__(self):
        return f"ProductMovement(id={self.id_movimiento}, producto='{self.codigo_producto}', cantidad={self.cantidad}, estado='{self.estado}')"
