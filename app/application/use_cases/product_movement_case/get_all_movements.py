"""
Use case para obtener todos los movimientos de productos
"""
import logging
from typing import List
from app.domain.entities.product_movement_model import ProductMovement
from app.domain.ports.out.product_movement_repository import ProductMovementRepository

logger = logging.getLogger(__name__)


class GetAllMovementsUseCase:
    """Caso de uso para obtener todos los movimientos"""
    
    def __init__(self, movement_repository: ProductMovementRepository):
        self.movement_repository = movement_repository
    
    def execute(self, company_id: str) -> List[ProductMovement]:
        """
        Ejecuta el caso de uso
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de movimientos
        """
        logger.info(f"Obteniendo todos los movimientos para la empresa {company_id}")
        movements = self.movement_repository.get_all_movements(company_id)
        logger.info(f"Se encontraron {len(movements)} movimientos")
        return movements
