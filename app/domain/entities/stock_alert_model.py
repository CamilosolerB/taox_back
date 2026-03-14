"""
Entidad de Dominio para Alertas de Stock
"""
from uuid import UUID
from datetime import datetime


class StockAlert:
    """Representa una alerta de stock crítico"""
    
    def __init__(
        self,
        codigo_producto: str,
        id_proceso: UUID,
        tipo_alerta: str,  # 'stock_critico', 'stock_bajo', 'exceso'
        cantidad_actual: int,
        cantidad_referencia: int,
        id_empresa: UUID,
        id_alerta: int = None,
        estado: str = 'activa',  # 'activa', 'resuelta', 'ignorada'
        descripcion: str = None,
        resolved_at: datetime = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id_alerta = id_alerta
        self.codigo_producto = codigo_producto
        self.id_proceso = id_proceso
        self.tipo_alerta = tipo_alerta
        self.cantidad_actual = cantidad_actual
        self.cantidad_referencia = cantidad_referencia
        self.id_empresa = id_empresa
        self.estado = estado
        self.descripcion = descripcion
        self.resolved_at = resolved_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def marcar_resuelta(self):
        """Marca la alerta como resuelta"""
        self.estado = 'resuelta'
        self.resolved_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        emoji = "🔴" if self.tipo_alerta == 'stock_critico' else "🟡" if self.tipo_alerta == 'stock_bajo' else "🟢"
        return f"StockAlert({emoji} {self.tipo_alerta}, producto='{self.codigo_producto}', estado='{self.estado}')"
