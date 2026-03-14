"""
Use case para crear una nueva alerta de stock
"""
import logging
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.application.dto.stock_alert_dto import StockAlertCreateDTO

logger = logging.getLogger(__name__)


class CreateAlertUseCase:
    """Caso de uso para crear una nueva alerta de stock"""
    
    def __init__(self, alert_repository: StockAlertRepository):
        self.alert_repository = alert_repository
    
    def execute(self, alert_dto: StockAlertCreateDTO) -> StockAlert:
        """
        Ejecuta el caso de uso
        
        Args:
            alert_dto: DTO con los datos de la alerta
            
        Returns:
            Alerta creada
        """
        logger.info(f"Creando nueva alerta para producto {alert_dto.codigo_producto}")
        
        alert = StockAlert(
            codigo_producto=alert_dto.codigo_producto,
            id_proceso=alert_dto.id_proceso,
            tipo_alerta=alert_dto.tipo_alerta,
            cantidad_actual=alert_dto.cantidad_actual,
            cantidad_referencia=alert_dto.cantidad_referencia,
            id_empresa=alert_dto.id_empresa,
            estado="activa",
            descripcion=alert_dto.descripcion
        )
        
        created_alert = self.alert_repository.create_alert(alert)
        logger.info(f"Alerta creada exitosamente con ID {created_alert.id_alerta}")
        return created_alert
