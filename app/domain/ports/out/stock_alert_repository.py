"""
Puerto (Interfaz) de Repositorio para Stock Alert
"""
from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities.stock_alert_model import StockAlert
from typing import List


class StockAlertRepository(ABC):
    """Interfaz para repositorio de alertas de stock"""
    
    @abstractmethod
    def get_all_alerts(self, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas de una empresa"""
        pass
    
    @abstractmethod
    def get_alert_by_id(self, id_alerta: int, company_id: str) -> StockAlert:
        """Obtiene una alerta por ID"""
        pass
    
    @abstractmethod
    def get_alerts_by_product(self, codigo_producto: str, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas de un producto"""
        pass
    
    @abstractmethod
    def get_alerts_by_process(self, id_proceso: UUID, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas en un proceso"""
        pass
    
    @abstractmethod
    def get_active_alerts(self, company_id: str) -> List[StockAlert]:
        """Obtiene todas las alertas activas"""
        pass
    
    @abstractmethod
    def get_alerts_by_type(self, tipo_alerta: str, company_id: str) -> List[StockAlert]:
        """Obtiene alertas por tipo (stock_critico, stock_bajo, exceso)"""
        pass
    
    @abstractmethod
    def get_alerts_by_status(self, estado: str, company_id: str) -> List[StockAlert]:
        """Obtiene alertas por estado"""
        pass
    
    @abstractmethod
    def create_alert(self, alert: StockAlert) -> StockAlert:
        """Crea una nueva alerta"""
        pass
    
    @abstractmethod
    def update_alert(self, id_alerta: int, alert_data: dict) -> StockAlert:
        """Actualiza una alerta"""
        pass
    
    @abstractmethod
    def resolve_alert(self, id_alerta: int) -> StockAlert:
        """Marca una alerta como resuelta"""
        pass
    
    @abstractmethod
    def delete_alert(self, id_alerta: int, company_id: str) -> bool:
        """Elimina una alerta"""
        pass
