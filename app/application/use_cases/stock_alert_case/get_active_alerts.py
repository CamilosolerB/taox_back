"""
Use case para obtener alertas activas
"""
import logging
from typing import List
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)


class GetActiveAlertsUseCase:
    """Caso de uso para obtener todas las alertas activas"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, company_id: str) -> List[StockAlert]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de alertas activas
        """
        logger.info(f"Obteniendo alertas activas para la empresa {company_id}")
        alerts = self.alert_repository.get_active_alerts(company_id)
        logger.info(f"Se encontraron {len(alerts)} alertas activas")
        return alerts
