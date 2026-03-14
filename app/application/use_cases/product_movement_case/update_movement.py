"""
Use case para actualizar un movimiento
"""
import logging
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository
from app.application.dto.product_movement_dto import ProductMovementUpdateDTO

logger = logging.getLogger(__name__)


class UpdateMovementUseCase:
    """Caso de uso para actualizar un movimiento"""
    
    def __init__(self, movement_repository: ProductMovementRepository):
        self.movement_repository = movement_repository
    
    def execute(self, id_movimiento: int, movement_dto: ProductMovementUpdateDTO) -> ProductMovement:
        """
        Ejecuta el caso de uso
        
        Args:
            id_movimiento: ID del movimiento a actualizar
            movement_dto: DTO con los datos a actualizar
            
        Returns:
            Movimiento actualizado
            
        Raises:
            ValueError: Si el movimiento no existe
        """
        logger.info(f"Actualizando movimiento {id_movimiento}")
        
        update_data = movement_dto.model_dump(exclude_unset=True)
        
        if not update_data:
            logger.warning(f"No hay campos para actualizar en movimiento {id_movimiento}")
            raise ValueError("Se debe proporcionar al menos un campo para actualizar")
        
        updated_movement = self.movement_repository.update_movement(id_movimiento, update_data)
        logger.info(f"Movimiento {id_movimiento} actualizado exitosamente")
        return updated_movement
