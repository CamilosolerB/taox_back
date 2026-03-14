"""
Entidad de Dominio para Stock de Químicos
"""
from uuid import UUID
from datetime import datetime


class ChemicalStock:
    """Registra el stock de un químico en un proceso específico"""
    
    def __init__(
        self,
        codigo_producto: str,
        id_proceso: UUID,
        cantidad_actual: int,
        cantidad_minima: int,
        cantidad_maxima: int,
        id_empresa: UUID,
        id_stock_quimico: int = None,
        unidad_medida: str = 'ml',  # ml, g, l, kg, etc
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id_stock_quimico = id_stock_quimico
        self.codigo_producto = codigo_producto
        self.id_proceso = id_proceso
        self.cantidad_actual = cantidad_actual
        self.cantidad_minima = cantidad_minima
        self.cantidad_maxima = cantidad_maxima
        self.id_empresa = id_empresa
        self.unidad_medida = unidad_medida
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @property
    def es_stock_critico(self) -> bool:
        """Retorna True si el stock está por debajo del mínimo"""
        return self.cantidad_actual < self.cantidad_minima
    
    @property
    def es_stock_bajo(self) -> bool:
        """Retorna True si el stock está entre 25-50% del mínimo"""
        threshold = self.cantidad_minima * 0.5
        return self.cantidad_actual < threshold and not self.es_stock_critico
    
    @property
    def porcentaje_stock(self) -> float:
        """Retorna el porcentaje de ocupación del máximo"""
        if self.cantidad_maxima == 0:
            return 0
        return (self.cantidad_actual / self.cantidad_maxima) * 100
    
    def __repr__(self):
        status = "🔴 CRÍTICO" if self.es_stock_critico else "🟡 BAJO" if self.es_stock_bajo else "🟢 OK"
        return f"ChemicalStock(producto='{self.codigo_producto}', proceso_id={self.id_proceso}, cantidad={self.cantidad_actual}/{self.cantidad_maxima} {status})"
