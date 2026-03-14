"""
Use case para obtener un movimiento por ID
"""
import logging
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository

logger = logging.getLogger(__name__)


class GetMovementByIdUseCase:
    """Caso de uso para obtener un movimiento por ID"""
    
    def __init__(self, movement_repository: ProductMovementRepository):
        self.movement_repository = movement_repository
    
    def execute(self, id_movimiento: int, company_id: str) -> ProductMovement:
        """
        Ejecuta el caso de uso
        
        Args:
            id_movimiento: ID del movimiento
            company_id: ID de la empresa
            
        Returns:
            Movimiento encontrado
            
        Raises:
            ValueError: Si el movimiento no existe
        """
        logger.info(f"Obteniendo movimiento {id_movimiento} de la empresa {company_id}")
        movement = self.movement_repository.get_movement_by_id(id_movimiento, company_id)
        if not movement:
            logger.error(f"Movimiento {id_movimiento} no encontrado")
            raise ValueError(f"Movimiento con ID {id_movimiento} no existe")
        return movement
