"""
Use case para obtener todas las alertas de stock
"""
import logging
from typing import List
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)


class GetAllAlertsUseCase:
    """Caso de uso para obtener todas las alertas de stock"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, company_id: str) -> List[StockAlert]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de alertas
        """
        logger.info(f"Obteniendo todas las alertas para la empresa {company_id}")
        alerts = self.alert_repository.get_all_alerts(company_id)
        logger.info(f"Se encontraron {len(alerts)} alertas")
        return alerts
