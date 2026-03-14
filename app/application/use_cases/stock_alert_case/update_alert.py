"""
Use case para actualizar una alerta
"""
import logging
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.application.dto.stock_alert_dto import StockAlertUpdateDTO

logger = logging.getLogger(__name__)


class UpdateAlertUseCase:
    """Caso de uso para actualizar una alerta"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, id_alerta: int, alert_dto: StockAlertUpdateDTO) -> StockAlert:
        """
        Ejecuta el caso de uso
        
        Args:
            id_alerta: ID de la alerta a actualizar
            alert_dto: DTO con los datos a actualizar
            
        Returns:
            Alerta actualizada
            
        Raises:
            ValueError: Si la alerta no existe
        """
        logger.info(f"Actualizando alerta {id_alerta}")
        
        update_data = alert_dto.model_dump(exclude_unset=True)
        
        if not update_data:
            logger.warning(f"No hay campos para actualizar en alerta {id_alerta}")
            raise ValueError("Se debe proporcionar al menos un campo para actualizar")
        
        updated_alert = self.alert_repository.update_alert(id_alerta, update_data)
        logger.info(f"Alerta {id_alerta} actualizada exitosamente")
        return updated_alert
