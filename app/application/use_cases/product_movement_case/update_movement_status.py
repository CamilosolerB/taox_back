"""
Use case para cambiar el estado de un movimiento
"""
import logging
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository

logger = logging.getLogger(__name__)

# Estados válidos para transiciones
VALID_STATES = {"pendiente", "en_transito", "completado", "cancelado"}


class UpdateMovementStatusUseCase:
    """Caso de uso para actualizar el estado de un movimiento"""
    
    def __init__(self, movement_repository: ProductMovementRepository):
        self.movement_repository = movement_repository
    
    def execute(self, id_movimiento: int, nuevo_estado: str) -> ProductMovement:
        """
        Ejecuta el caso de uso
        
        Args:
            id_movimiento: ID del movimiento
            nuevo_estado: Nuevo estado del movimiento
            
        Returns:
            Movimiento con estado actualizado
            
        Raises:
            ValueError: Si el estado no es válido
        """
        if nuevo_estado not in VALID_STATES:
            logger.error(f"Estado inválido: {nuevo_estado}")
            raise ValueError(f"Estado debe ser uno de: {', '.join(VALID_STATES)}")
        
        logger.info(f"Actualizando estado del movimiento {id_movimiento} a {nuevo_estado}")
        updated_movement = self.movement_repository.update_movement_status(id_movimiento, nuevo_estado)
        logger.info(f"Movimiento {id_movimiento} cambió a estado {nuevo_estado}")
        return updated_movement
