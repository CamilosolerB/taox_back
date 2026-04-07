"""
Use case para crear un nuevo movimiento de producto
Incluye lógica para generar alertas si el stock cruza umbrales
"""
import logging
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.domain.ports.out.stock_warehouse_repository import StockWarehouseRepository
from app.domain.ports.out.product_repository import ProductRepository
from app.domain.ports.out.stock_alert_repository import StockAlertRepository
from app.domain.entities.stock_alert_model import StockAlert
from app.domain.entities.stock_warehouse_model import StockWarehouse
from app.application.dto.product_movement_dto import ProductMovementCreateDTO
from datetime import datetime

logger = logging.getLogger(__name__)


class CreateMovementUseCase:
    """Caso de uso para crear un nuevo movimiento de producto"""
    
    def __init__(
        self,
        movement_repository: ProductMovementRepository,
        stock_warehouse_repository: StockWarehouseRepository,
        product_repository: ProductRepository,
        stock_alert_repository: StockAlertRepository
    ):
        self.movement_repository = movement_repository
        self.stock_warehouse_repository = stock_warehouse_repository
        self.product_repository = product_repository
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
        
        # Validar stock disponible si es una deducción (salida o traslado)
        self._validate_stock_availability(movement_dto)
        
        movement = ProductMovement(
            codigo_producto=movement_dto.codigo_producto,
            id_proceso_origen=movement_dto.id_proceso_origen,
            id_proceso_destino=movement_dto.id_proceso_destino,
            tipo_movimiento=movement_dto.tipo_movimiento,
            cantidad=movement_dto.cantidad,
            notas=movement_dto.notas,
            id_empresa=movement_dto.id_empresa,
            estado="pendiente"
        )
        
        created_movement = self.movement_repository.create_movement(movement)
        logger.info(f"Movimiento creado con ID {created_movement.id_movimiento}")
        
        # Procesar actualización de inventarios
        self._update_stock_for_movement(movement_dto)

        # Generar alertas si es necesario
        self._check_and_generate_alerts(movement_dto)
        
        return created_movement

    def _validate_stock_availability(self, movement_dto: ProductMovementCreateDTO) -> None:
        """
        Verifica que haya stock suficiente antes de registrar una salida o traslado
        """
        tipo = movement_dto.tipo_movimiento
        if tipo in ['salida', 'traslado']:
            stock = self.stock_warehouse_repository.get_stock_by_product(
                movement_dto.codigo_producto, movement_dto.id_empresa
            )
            cantidad_disponible = stock.cantidad if stock else 0
            if cantidad_disponible < movement_dto.cantidad:
                logger.error(f"Stock insuficiente en almacén global: {cantidad_disponible} < {movement_dto.cantidad}")
                raise ValueError(f"Stock insuficiente en almacén global. Disponible: {cantidad_disponible}, Solicitado: {movement_dto.cantidad}")

    def _update_stock_for_movement(self, movement_dto: ProductMovementCreateDTO) -> None:
        """
        Actualiza el stock basado en el tipo de movimiento (entrada, salida, traslado)
        """
        try:
            tipo = movement_dto.tipo_movimiento
            
            if tipo == 'salida':
                stock_origen = self.stock_warehouse_repository.get_stock_by_product(
                    movement_dto.codigo_producto, movement_dto.id_empresa
                )
                if stock_origen:
                    stock_origen.cantidad -= movement_dto.cantidad
                    self.stock_warehouse_repository.update_stock(stock_origen.codigo_producto, stock_origen)
            
            if tipo == 'entrada':
                stock_destino = self.stock_warehouse_repository.get_stock_by_product(
                    movement_dto.codigo_producto, movement_dto.id_empresa
                )
                if stock_destino:
                    stock_destino.cantidad += movement_dto.cantidad
                    self.stock_warehouse_repository.update_stock(stock_destino.codigo_producto, stock_destino)
                else:
                    new_stock = StockWarehouse(
                        codigo_producto=movement_dto.codigo_producto,
                        cantidad=movement_dto.cantidad,
                        id_empresa=movement_dto.id_empresa
                    )
                    self.stock_warehouse_repository.create_stock(new_stock)
        except Exception as e:
            logger.error(f"Error actualizando stock global por movimiento {tipo}: {str(e)}")

    def _check_and_generate_alerts(self, movement_dto: ProductMovementCreateDTO) -> None:
        """
        Verifica el stock del proceso destino y genera alertas si es necesario
        
        Args:
            movement_dto: DTO del movimiento creado
        """
        try:
            product = self.product_repository.get_product_by_id(movement_dto.codigo_producto)
            if not product or getattr(product, 'limite_critico', None) is None:
                return
                
            stock = self.stock_warehouse_repository.get_stock_by_product(
                movement_dto.codigo_producto, movement_dto.id_empresa
            )
            
            if not stock:
                return
            
            limite = product.limite_critico
            
            # Verificar si el stock es crítico
            if stock.cantidad <= limite:
                logger.warning(f"Stock crítico detectado para {movement_dto.codigo_producto}")
                self._create_alert(
                    movement_dto, stock, limite, "stock_critico",
                    f"Stock crítico global: {stock.cantidad} <= {limite}"
                )
            
            # Verificar si el stock es bajo (pero no crítico, consideraremos < 1.5 veces el limite como bajo)
            elif stock.cantidad <= (limite * 1.5):
                logger.warning(f"Stock bajo detectado para {movement_dto.codigo_producto}")
                self._create_alert(
                    movement_dto, stock, limite, "stock_bajo",
                    f"Stock bajo global: {stock.cantidad} <= {limite * 1.5}"
                )
        
        except Exception as e:
            logger.error(f"Error verificando stock después del movimiento: {str(e)}")
    
    def _create_alert(self, movement_dto: ProductMovementCreateDTO, stock, limite_referencia: float, tipo_alerta: str, descripcion: str) -> None:
        """
        Crea una alerta de stock
        
        Args:
            movement_dto: DTO del movimiento
            stock: Entidad de stock global
            limite_referencia: El valor de referencia como limite_critico
            tipo_alerta: Tipo de alerta a crear
            descripcion: Descripción de la alerta
        """
        try:
            alert = StockAlert(
                codigo_producto=movement_dto.codigo_producto,
                id_proceso=movement_dto.id_proceso_destino or movement_dto.id_proceso_origen, # Lo usamos referencial
                tipo_alerta=tipo_alerta,
                cantidad_actual=stock.cantidad,
                cantidad_referencia=limite_referencia,
                id_empresa=movement_dto.id_empresa,
                estado="activa",
                descripcion=descripcion
            )
            
            self.stock_alert_repository.create_alert(alert)
            logger.info(f"Alerta de {tipo_alerta} creada para {movement_dto.codigo_producto}")
        
        except Exception as e:
            logger.error(f"Error creando alerta: {str(e)}")
