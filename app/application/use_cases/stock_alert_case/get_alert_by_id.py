"""
Use case para obtener una alerta por ID
"""
import logging
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)


class GetAlertByIdUseCase:
    """Caso de uso para obtener una alerta por ID"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, id_alerta: int, company_id: str) -> StockAlert:
        """
        Ejecuta el caso de uso
        
        Args:
            id_alerta: ID de la alerta
            company_id: ID de la empresa
            
        Returns:
            Alerta encontrada
            
        Raises:
            ValueError: Si la alerta no existe
        """
        logger.info(f"Obteniendo alerta {id_alerta} de la empresa {company_id}")
        alert = self.alert_repository.get_alert_by_id(id_alerta, company_id)
        if not alert:
            logger.error(f"Alerta {id_alerta} no encontrada")
            raise ValueError(f"Alerta con ID {id_alerta} no existe")
        return alert
