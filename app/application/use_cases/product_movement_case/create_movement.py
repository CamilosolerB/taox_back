"""
Use case para crear un nuevo movimiento de producto
Incluye lógica para generar alertas si el stock cruza umbrales
"""
import logging
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.domain.ports.out.chemical_stock_repository import ChemicalStockRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.domain.entities.stock_alert_model import StockAlert
from app.application.dto.product_movement_dto import ProductMovementCreateDTO
from datetime import datetime

logger = logging.getLogger(__name__)


class CreateMovementUseCase:
    """Caso de uso para crear un nuevo movimiento de producto"""
    
    def __init__(
        self,
        movement_repository: ProductMovementRepository,
        chemical_stock_repository: ChemicalStockRepository,
        stock_alert_repository: StockAlertRepository
    ):
        self.movement_repository = movement_repository
        self.chemical_stock_repository = chemical_stock_repository
        self.stock_alert_repository = stock_alert_repository
    
    def execute(self, movement_dto: ProductMovementCreateDTO) -> ProductMovement:
        """
        Ejecuta el caso de uso
        
        Crea un movimiento y verifica si genera alertas de stock
        
        Args:
            movement_dto: DTO con los datos del movimiento
            
        Returns:
            Movimiento creado
        """
        logger.info(f"Creando nuevo movimiento para producto {movement_dto.codigo_producto}")
        
        movement = ProductMovement(
            codigo_producto=movement_dto.codigo_producto,
            id_proceso_origen=movement_dto.id_proceso_origen,
            id_proceso_destino=movement_dto.id_proceso_destino,
            cantidad=movement_dto.cantidad,
            notas=movement_dto.notas,
            id_empresa=movement_dto.id_empresa,
            estado="pendiente"
        )
        
        created_movement = self.movement_repository.create_movement(movement)
        logger.info(f"Movimiento creado con ID {created_movement.id_movimiento}")
        
        # Generar alertas si es necesario
        self._check_and_generate_alerts(movement_dto)
        
        return created_movement
    
    def _check_and_generate_alerts(self, movement_dto: ProductMovementCreateDTO) -> None:
        """
        Verifica el stock del proceso destino y genera alertas si es necesario
        
        Args:
            movement_dto: DTO del movimiento creado
        """
        try:
            stock = self.chemical_stock_repository.get_stock_by_product_and_process(
                movement_dto.codigo_producto,
                movement_dto.id_proceso_destino,
                movement_dto.id_empresa
            )
            
            if not stock:
                logger.debug(f"No hay stock registrado para {movement_dto.codigo_producto} en proceso {movement_dto.id_proceso_destino}")
                return
            
            # Verificar si el stock es crítico
            if stock.es_stock_critico:
                logger.warning(f"Stock crítico detectado para {movement_dto.codigo_producto}")
                self._create_alert(
                    movement_dto,
                    stock,
                    "stock_critico",
                    f"Stock crítico: {stock.cantidad_actual} < {stock.cantidad_minima}"
                )
            
            # Verificar si el stock es bajo (pero no crítico)
            elif stock.es_stock_bajo:
                logger.warning(f"Stock bajo detectado para {movement_dto.codigo_producto}")
                self._create_alert(
                    movement_dto,
                    stock,
                    "stock_bajo",
                    f"Stock bajo: {stock.cantidad_actual} < {stock.cantidad_minima * 0.5}"
                )
        
        except Exception as e:
            logger.error(f"Error verificando stock después del movimiento: {str(e)}")
    
    def _create_alert(self, movement_dto: ProductMovementCreateDTO, stock, tipo_alerta: str, descripcion: str) -> None:
        """
        Crea una alerta de stock
        
        Args:
            movement_dto: DTO del movimiento
            stock: Entidad de stock
            tipo_alerta: Tipo de alerta a crear
            descripcion: Descripción de la alerta
        """
        try:
            alert = StockAlert(
                codigo_producto=movement_dto.codigo_producto,
                id_proceso=movement_dto.id_proceso_destino,
                tipo_alerta=tipo_alerta,
                cantidad_actual=stock.cantidad_actual,
                cantidad_referencia=stock.cantidad_minima,
                id_empresa=movement_dto.id_empresa,
                estado="activa",
                descripcion=descripcion
            )
            
            self.stock_alert_repository.create_alert(alert)
            logger.info(f"Alerta de {tipo_alerta} creada para {movement_dto.codigo_producto}")
        
        except Exception as e:
            logger.error(f"Error creando alerta: {str(e)}")
