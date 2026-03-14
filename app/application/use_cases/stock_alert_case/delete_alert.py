"""
Use case para eliminar una alerta
"""
import logging
from app.domain.ports.out.stock_alert_repository import StockAlertRepository

logger = logging.getLogger(__name__)


class DeleteAlertUseCase:
    """Caso de uso para eliminar una alerta"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, id_alerta: int, company_id: str) -> bool:
        """
        Ejecuta el caso de uso
        
        Args:
            id_alerta: ID de la alerta a eliminar
            company_id: ID de la empresa
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si la alerta no existe
        """
        logger.info(f"Eliminando alerta {id_alerta} de la empresa {company_id}")
        result = self.alert_repository.delete_alert(id_alerta, company_id)
        
        if not result:
            logger.error(f"No se pudo eliminar la alerta {id_alerta}")
            raise ValueError(f"Alerta con ID {id_alerta} no existe")
        
        logger.info(f"Alerta {id_alerta} eliminada exitosamente")
        return result
