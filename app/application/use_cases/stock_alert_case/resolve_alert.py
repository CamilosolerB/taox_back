"""
Use case para resolver una alerta
"""
import logging
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)


class ResolveAlertUseCase:
    """Caso de uso para resolver una alerta"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, id_alerta: int) -> StockAlert:
        """
        Ejecuta el caso de uso
        
        Args:
            id_alerta: ID de la alerta a resolver
            
        Returns:
            Alerta resuelta
            
        Raises:
            ValueError: Si la alerta no existe
        """
        logger.info(f"Resolviendo alerta {id_alerta}")
        
        resolved_alert = self.alert_repository.resolve_alert(id_alerta)
        logger.info(f"Alerta {id_alerta} resuelta exitosamente")
        return resolved_alert
