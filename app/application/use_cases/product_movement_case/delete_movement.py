"""
Use case para eliminar un movimiento
"""
import logging
from app.domain.ports.out.product_movement_repository import ProductMovementRepository

logger = logging.getLogger(__name__)


class DeleteMovementUseCase:
    """Caso de uso para eliminar un movimiento"""
    
    def __init__(self, movement_repository: ProductMovementRepository):
        self.movement_repository = movement_repository
    
    def execute(self, id_movimiento: int, company_id: str) -> bool:
        """
        Ejecuta el caso de uso
        
        Args:
            id_movimiento: ID del movimiento a eliminar
            company_id: ID de la empresa
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            ValueError: Si el movimiento no existe
        """
        logger.info(f"Eliminando movimiento {id_movimiento} de la empresa {company_id}")
        result = self.movement_repository.delete_movement(id_movimiento, company_id)
        
        if not result:
            logger.error(f"No se pudo eliminar el movimiento {id_movimiento}")
            raise ValueError(f"Movimiento con ID {id_movimiento} no existe")
        
        logger.info(f"Movimiento {id_movimiento} eliminado exitosamente")
        return result
